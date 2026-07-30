from flask import Blueprint, request

from api.response import to_json, error_json
from bll.register_user_bll import RegisterUserBLL
from models.register_user_service_model import RegisterUserRequest


register_user_bp = Blueprint("register_user_bp", __name__)


@register_user_bp.route("/register", methods=["POST"])
def register_user():
    """Registruj novog korisnika (kreira ApplicationUser + Wallet).
    ---
    tags:
      - User
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - ApplicationID
            - UserIdentificator
          properties:
            ApplicationID:
              type: integer
              example: 1
            UserIdentificator:
              type: string
              example: test-user-001
            UserName:
              type: string
              example: tester
            Name:
              type: string
              example: Test
            LastName:
              type: string
              example: User
            CountryCode:
              type: string
              example: BA
            CurrencyCode:
              type: string
              default: USD
              example: USD
            PromotionCode:
              type: string
              default: WELCOME1000
              example: WELCOME1000
    responses:
      200:
        description: RegisterUserResponse
        schema:
          type: object
          properties:
            Success: { type: boolean }
            Message: { type: string }
            ApplicationUserID: { type: integer }
            WalletID: { type: integer }
            ApplicationUserGuid: { type: string }
            CurrencyCode: { type: string }
      400:
        description: Missing required fields
    """
    body = request.get_json(silent=True) or {}
    req = RegisterUserRequest.from_dict(body)

    if req.ApplicationID is None or not req.UserIdentificator:
        return error_json("ApplicationID and UserIdentificator are required.", 400)

    response = RegisterUserBLL.register(req)
    return to_json(response)
