from flask import Blueprint, request

from api.response import to_json, error_json
from bll.put_amount_bll import PutAmountBLL
from models.put_amount_service_model import PutAmountRequest


put_amount_bp = Blueprint("put_amount_bp", __name__)


@put_amount_bp.route("/bet", methods=["POST"])
def put_amount():
    """Izvrsi bet nad walletom (Stake se skida, WinAmount pripisuje).
    ---
    tags:
      - Wallet
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - ApplicationID
            - UserID
            - CurrencyCode
            - Stake
          properties:
            ApplicationID:
              type: integer
              example: 1
            UserID:
              type: integer
              example: 2
            CurrencyCode:
              type: string
              example: USD
            Stake:
              type: number
              example: 10.00
            WinAmount:
              type: number
              default: 0
              example: 0.00
            ExternalTransactionID:
              type: string
              example: tx-0001
            Description:
              type: string
              example: Round win
    responses:
      200:
        description: PutAmountResponse
        schema:
          type: object
          properties:
            Success: { type: boolean }
            Message: { type: string }
            WalletID: { type: integer }
            RealBalance: { type: number }
            BonusBalance: { type: number }
            StakeFromBonus: { type: number }
            StakeFromReal: { type: number }
            PromotionOutcome: { type: string }
            UserPromotionID: { type: integer }
            WagerCompleted: { type: number }
            WagerRequired: { type: number }
            BonusConverted: { type: number }
            BonusForfeited: { type: number }
      400:
        description: Missing required fields
    """
    body = request.get_json(silent=True) or {}
    req = PutAmountRequest.from_dict(body)

    if (
        req.ApplicationID is None
        or req.UserID is None
        or not req.CurrencyCode
        or req.Stake is None
    ):
        return error_json("ApplicationID, UserID, CurrencyCode and Stake are required.", 400)

    response = PutAmountBLL.put_amount(req)
    return to_json(response)
