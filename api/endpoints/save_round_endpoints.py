from flask import Blueprint, request

from api.response import to_json, error_json
from bll.save_round_bll import SaveRoundBLL


save_round_bp = Blueprint("save_round_bp", __name__)


@save_round_bp.route("/save-round", methods=["POST"])
def save_round():
    """Snimi rezultat spin runde (Spin API response) u GamePlayRound tabelu.
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
            - success
            - game_id
            - player_id
            - bet_per_line
            - lines
            - total_bet
            - total_win
            - balance
            - currency
          properties:
            success:
              type: boolean
              example: true
            game_id:
              type: string
              example: venom_of_the_nile_paylines
            player_id:
              type: string
              example: guest_2ba3dffeac4442539ba0beb007acabd5
            bet_per_line:
              type: number
              example: 0.05
            lines:
              type: integer
              example: 20
            total_bet:
              type: number
              example: 1.0
            total_win:
              type: number
              example: 0.45
            base_win:
              type: number
              example: 0.45
            scatter_win:
              type: number
              example: 0.0
            free_spins_win:
              type: number
              example: 0.0
            balance:
              type: number
              example: 999.0
            currency:
              type: string
              example: PTS
            message:
              type: string
              example: OK
            feature:
              type: object
              properties:
                triggered:
                  type: boolean
                  example: false
    responses:
      200:
        description: SaveRoundResponse
        schema:
          type: object
          properties:
            RoundID: { type: integer }
            ExternalRoundIdentifier: { type: string }
            Success: { type: boolean }
            Message: { type: string }
      400:
        description: Missing required fields
    """
    body = request.get_json(silent=True) or {}

    if not body.get("game_id") or not body.get("player_id"):
        return error_json("game_id and player_id are required.", 400)

    if body.get("total_bet") is None:
        return error_json("total_bet is required.", 400)

    response = SaveRoundBLL.save(body)
    return to_json(response)
