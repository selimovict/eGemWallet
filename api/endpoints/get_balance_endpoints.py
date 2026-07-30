from flask import Blueprint, request

from api.response import to_json, error_json
from bll.get_balance_bll import GetBalanceBLL
from models.get_balance_service_model import GetBalanceRequest


get_balance_bp = Blueprint("get_balance_bp", __name__)


@get_balance_bp.route("/balance", methods=["POST"])
def get_balance():
    """Vrati stanje walleta + info o aktivnoj promociji.
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
    responses:
      200:
        description: GetBalanceResponse
        schema:
          type: object
          properties:
            ApplicationID: { type: integer }
            UserID: { type: integer }
            CurrencyCode: { type: string }
            WalletExists: { type: boolean }
            WalletID: { type: integer }
            RealBalance: { type: number }
            BonusBalance: { type: number }
            TotalBalance: { type: number }
            WalletUpdated: { type: string, format: date-time }
            HasActivePromotion: { type: boolean }
            UserPromotionID: { type: integer }
            PromotionCode: { type: string }
            PromotionName: { type: string }
            PromotionTypeName: { type: string }
            PromotionActionID: { type: integer }
            PromotionCurrency: { type: string }
            FreeSpinsGranted: { type: integer }
            FreeSpinsRemaining: { type: integer }
            BonusGranted: { type: number }
            BonusRemaining: { type: number }
            WagerRequired: { type: number }
            WagerCompleted: { type: number }
            WagerRemaining: { type: number }
            WagerProgressPct: { type: number }
            MaxCashOut: { type: number }
            MaxBet: { type: number }
            ActivatedDate: { type: string, format: date-time }
            ExpireDate: { type: string, format: date-time }
            DaysToExpire: { type: integer }
      400:
        description: Missing required fields
    """
    body = request.get_json(silent=True) or {}
    req = GetBalanceRequest.from_dict(body)

    if req.ApplicationID is None or req.UserID is None or not req.CurrencyCode:
        return error_json("ApplicationID, UserID and CurrencyCode are required.", 400)

    response = GetBalanceBLL.get_balance(req)
    return to_json(response)
