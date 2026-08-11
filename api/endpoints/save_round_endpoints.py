from flask import Blueprint, request

from api.response import to_json, error_json
from bll.save_round_bll import SaveRoundBLL


save_round_bp = Blueprint("save_round_bp", __name__)


@save_round_bp.route("/save-round", methods=["POST"])
def save_round():
    """Snimi rezultat spin runde u GamePlayRound i izvrsi wallet bet.

    **Tok obrade (redoslijed):**

    1. Validacija obaveznih polja
    2. INSERT u `dbo.GamePlayRound` — `BetProcessed = 0`
    3. Resolve `ApplicationUserID`:
       - Ako je `UserID` (integer) poslan u requestu (top-level ili unutar `BetJSON`) — koristi se direktno
       - Inace: SELECT iz `dbo.ApplicationUser` WHERE `ApplicationID` + `player_id`
    4. Poziv `dbo.Wallet_Bet` sa parametrima iz `BetJSON` ili deriviranim iz spin fielda
    5. UPDATE `BetProcessed = 1` i `BetJSON` = wallet response (ako bet uspije)

    **Napomene:**

    - `ApplicationID` i `CurrencyCode` mogu biti na top nivou ili unutar `BetJSON` objekta
    - `BetJSON.ExternalTransactionID` se koristi za wallet bet ako je poslan; inace se koristi `ExternalRoundIdentifier`
    - `BetJSON.Description` se koristi za wallet bet ako je poslan; inace `game_id`
    - Dupli `external_round_identifier` ne vraca gresku — vraca podatke vec spasenog round-a
    - `BalanceBefore` se racuna automatski: `balance + total_bet - total_win`
    - `FreeSpin = 1` ako `feature.triggered = true` (scatter) ili `purchase_type = "free_spins"` (feature buy)
    - Cijeli raw request body se sprema u `GameJSON`; `BetJSON` kolona se nakon wallet poziva prepisuje sa wallet response-om

    ---
    tags:
      - Game
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - game_id
            - player_id
            - total_bet
            - total_win
            - balance
            - currency
            - success
          properties:
            UserID:
              type: integer
              description: >
                ApplicationUserID (integer) iz dbo.ApplicationUser.
                Ako je poslan, koristi se direktno za wallet bet bez dodatnog DB lookup-a.
                Moze biti i unutar BetJSON objekta.
              example: 15
            external_round_identifier:
              type: string
              description: >
                Jedinstveni identifikator runde iz eksternog sistema.
                Ako nije poslan, baza generise GUID automatski (DEFAULT NEWID()).
                Ako se posalje isti identifier dva puta, vraca se vec spaseni round bez greske.
              example: "84802198-7063-4459-9c9b-10e66d9d3a04"
            success:
              type: boolean
              description: Da li je Spin API uspjesno izvrsio spin.
              example: true
            game_id:
              type: string
              description: >
                Jedinstveni identifikator igre iz Spin API-ja.
                Koristi se kao MachineID i MachineName u bazi.
                Koristi se kao Description za wallet bet ako BetJSON.Description nije poslan.
              example: spin_realms
            theme_id:
              type: string
              description: Identifikator teme igre (opcionalno, sprema se unutar GameJSON).
              example: venom_of_the_nile
            player_id:
              type: string
              description: >
                Identifikator igraca iz Spin API-ja. Odgovara polju UserIdentificator
                u dbo.ApplicationUser. Koristi se za DB lookup ApplicationUserID
                ako UserID nije direktno poslan u requestu.
              example: player_121d46f4d3754249a757d8129bf56453
            bet_per_line:
              type: number
              format: decimal
              description: Iznos uloga po jednoj liniji.
              example: 0.05
            lines:
              type: integer
              description: Broj aktivnih paylinea u spinu.
              example: 20
            total_bet:
              type: number
              format: decimal
              description: >
                Ukupni ulog (bet_per_line * lines).
                Prosljedjuje se kao Stake u wallet bet.
              example: 1.0
            total_win:
              type: number
              format: decimal
              description: >
                Ukupni dobitak u ovom spinu.
                Prosljedjuje se kao WinAmount u wallet bet. 0.0 ako nema dobitka.
              example: 0.5
            base_win:
              type: number
              format: decimal
              description: Dobitak iskljucivo od payline kombinacija (bez scatter i free spinova).
              example: 0.5
            scatter_win:
              type: number
              format: decimal
              description: Dobitak od scatter simbola. 0.0 ako nema scatter dobitka.
              example: 0.0
            free_spins_win:
              type: number
              format: decimal
              description: >
                Ukupni dobitak tokom svih free spin rundi unutar ovog spina.
                Popunjava se kada feature.triggered = true ili purchase_type = "free_spins".
              example: 0.0
            balance:
              type: number
              format: decimal
              description: >
                Stanje igraca NAKON spina (BalanceAfter u bazi).
                BalanceBefore se racuna automatski: balance + total_bet - total_win.
              example: 1004.75
            currency:
              type: string
              description: Valuta igre iz Spin API-ja (game currency). Sprema se u kolonu Currency.
              example: PTS
            message:
              type: string
              description: Statusna poruka iz Spin API-ja.
              example: OK
            purchase_type:
              type: string
              description: >
                Prisutno samo kod Feature Buy spina. Vrijednost "free_spins" oznacava
                da je igrac kupio free spinove. U tom slucaju FreeSpin = 1,
                FreeSpinSource = "purchase".
              example: free_spins
            reels:
              type: array
              description: >
                Lista kolona (reels) sa simbolima iz Spin API-ja.
                Sprema se u ReelsJSON. NULL u bazi ako nije poslan ili prazna lista.
              items:
                type: object
                properties:
                  symbols:
                    type: array
                    description: Simboli u koloni (odozgo prema dolje).
                    items:
                      type: string
              example:
                - symbols: ["Treasure", "Queen", "Ten"]
                - symbols: ["Ten", "Ace", "Queen"]
                - symbols: ["Ten", "Scarab", "Queen"]
                - symbols: ["Scarab", "Ace", "Treasure"]
                - symbols: ["King", "Queen", "Ten"]
            feature:
              type: object
              description: >
                Podaci o bonus featureu iz Spin API-ja. Sprema se u FeatureJSON.
                Ako triggered = true, FreeSpin = 1 i FreeSpinSource = "scatter_trigger".
                NULL u bazi ako nije poslan ili prazan objekat.
              properties:
                triggered:
                  type: boolean
                  description: Da li je free spin feature aktiviran u ovom spinu.
                  example: false
                scatter_count:
                  type: integer
                  description: Broj scatter simbola koji su triggerovali feature.
                  example: 3
                awarded_spins:
                  type: integer
                  description: Broj dodijeljenih free spinova.
                  example: 10
                feature_total_win:
                  type: number
                  description: Ukupni dobitak tokom svih free spin rundi.
                  example: 2.0
                free_spins:
                  type: array
                  description: Lista detalja za svaki pojedinacni free spin.
                  items:
                    type: object
                    properties:
                      index:
                        type: integer
                        example: 1
                      win:
                        type: number
                        example: 0.5
                      remaining:
                        type: integer
                        example: 9
                      retriggered:
                        type: boolean
                        example: false
                      added_spins:
                        type: integer
                        example: 0
                      scatter_count:
                        type: integer
                        example: 0
                      reels:
                        type: array
                        items:
                          type: object
                      details:
                        type: array
                        items:
                          type: object
              example:
                triggered: false
            feature_buy:
              type: object
              description: >
                Prisutan samo kod Feature Buy spina (igrac kupio free spinove).
                Sprema se u FeatureBuyJSON. NULL u bazi ako nije poslan.
                Ako je prisutan, FreeSpin = 1, FreeSpinSource = "purchase".
              properties:
                purchase_type:
                  type: string
                  example: free_spins
                display_name:
                  type: string
                  example: Buy Free Spins
                multiplier:
                  type: number
                  example: 2.0
                scatter_count:
                  type: integer
                  example: 3
                base_total_bet:
                  type: number
                  example: 1.0
                trigger_display_only:
                  type: boolean
                  example: true
                trigger_grid_win:
                  type: number
                  example: 0.0
            details:
              type: array
              description: >
                Lista dobitnih kombinacija iz Spin API-ja. Sprema se u DetailsJSON.
                NULL u bazi ako je prazna lista ili nije poslana.
              items:
                type: object
                properties:
                  win_type:
                    type: string
                    description: Tip dobitka (npr. "paylines").
                    example: paylines
                  line_index:
                    type: integer
                    description: Indeks payline-a (0-based).
                    example: 8
                  payline:
                    type: array
                    description: Pozicije simbola po kolonama za ovu payline kombinaciju.
                    items:
                      type: integer
                    example: [1, 2, 2, 2, 1]
                  line_symbols:
                    type: array
                    description: Simboli koji cine dobitnu kombinaciju.
                    items:
                      type: string
                    example: ["Queen", "Queen", "Queen", "Treasure", "Queen"]
                  symbol:
                    type: string
                    description: Dobitni simbol.
                    example: Queen
                  matched_reels:
                    type: integer
                    description: Broj kolona u kojima se simbol poklapa.
                    example: 3
                  payout_multiplier:
                    type: number
                    description: Multiplikator isplate za ovaj simbol i broj podudaranja.
                    example: 10.0
                  win_amount:
                    type: number
                    description: Iznos dobitka za ovu payline kombinaciju.
                    example: 0.5
              example:
                - win_type: paylines
                  line_index: 8
                  payline: [1, 2, 2, 2, 1]
                  line_symbols: ["Queen", "Queen", "Queen", "Treasure", "Queen"]
                  symbol: Queen
                  matched_reels: 3
                  payout_multiplier: 10.0
                  win_amount: 0.5
            BetJSON:
              type: object
              description: >
                Parametri za poziv dbo.Wallet_Bet. Ako je poslan, ApplicationID,
                CurrencyCode i UserID se citaju iz ovog objekta (ako nisu na top nivou).
                ExternalTransactionID i Description se koriste direktno za wallet bet.
                NAPOMENA: Nakon obrade, BetJSON kolona u bazi se prepisuje sa wallet response-om.
                Originalni BetJSON iz requesta ostaje sacuvan unutar GameJSON.
              properties:
                ApplicationID:
                  type: integer
                  description: ID aplikacije za wallet bet.
                  example: 1
                CurrencyCode:
                  type: string
                  description: Kod valute za wallet bet.
                  example: PTS
                UserID:
                  type: integer
                  description: ApplicationUserID za wallet bet.
                  example: 15
                Stake:
                  type: number
                  description: Iznos uloga (obicno jednak total_bet).
                  example: 1.0
                WinAmount:
                  type: number
                  description: Iznos dobitka (obicno jednak total_win).
                  example: 0.5
                ExternalTransactionID:
                  type: string
                  description: >
                    Informativno polje. Server uvijek koristi RoundID iz GamePlayRound
                    kao ExternalTransactionID za wallet bet (ignorise se ako je poslan).
                  example: "spinrealms:spin:d6e48e5d3493cf0054567dc96cfa90c05e703b3462483933fe5d6fd58d7f0c35"
                Description:
                  type: string
                  description: >
                    Opis transakcije za wallet. Ako nije poslan, koristi se game_id.
                  example: "Spin Realms round 582d68d4d7944cc3a8b04495b02e63fa"
              example:
                ApplicationID: 1
                CurrencyCode: PTS
                UserID: 15
                Stake: 1.0
                WinAmount: 0.5
                ExternalTransactionID: "spinrealms:spin:d6e48e5d3493cf0054567dc96cfa90c05e703b3462483933fe5d6fd58d7f0c35"
                Description: "Spin Realms round 582d68d4d7944cc3a8b04495b02e63fa"
    responses:
      200:
        description: >
          Round je uspjesno spasem u bazu (ili vec postoji sa istim external_round_identifier).
        schema:
          type: object
          properties:
            RoundID:
              type: integer
              description: Interni ID runde iz dbo.GamePlayRound (IDENTITY bigint kolona).
              example: 101
            ExternalRoundIdentifier:
              type: string
              description: >
                GUID runde — poslan od klijenta ili automatski generisan od strane baze (NEWID()).
              example: "84802198-7063-4459-9c9b-10e66d9d3a04"
            BetProcessed:
              type: boolean
              description: >
                true — Wallet_Bet je uspjesno izvrsem (Stake skinut, WinAmount pripizan).
                false — Bet nije obradjen (player_id nije nadjenu ApplicationUser,
                ApplicationID nije poslan, ili je Wallet_Bet vratio gresku).
                U slucaju greske, detalji greske se cuvaju u BetJSON koloni u bazi.
              example: true
            Success:
              type: boolean
              description: true ako je round uspjesno spasem u bazu.
              example: true
            Message:
              type: string
              description: >
                "Round saved." — novi round uspjesno kreiran.
                "Round already saved." — round sa istim external_round_identifier vec postoji.
                "Insert failed." — greska pri INSERT-u (row nije vratio OUTPUT).
              example: Round saved.
      400:
        description: Nedostaju obavezna polja.
        schema:
          type: object
          properties:
            error:
              type: string
              example: game_id and player_id are required.
      500:
        description: >
          Greska na SQL Serveru (constraint violation koji nije dupli kljuc,
          greska u Wallet_Bet SP-u koja nije uhvacena, i sl.).
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unexpected error. Try again."
    """
    body = request.get_json(silent=True) or {}

    if not body.get("game_id") or not body.get("player_id"):
        return error_json("game_id and player_id are required.", 400)

    if body.get("total_bet") is None:
        return error_json("total_bet is required.", 400)

    response = SaveRoundBLL.save(body)
    return to_json(response)
