from flask import Blueprint, request

from api.response import to_json, error_json
from bll.link_identity_bll import LinkIdentityBLL
from models.link_identity_service_model import LinkIdentityRequest


link_identity_bp = Blueprint("link_identity_bp", __name__)


@link_identity_bp.route("/link-identity", methods=["POST"])
def link_identity():
    """Pridruzi/azuriraj identitete (email, Google, Telegram, ime...) postojeceg korisnika.
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
            UserEmail:
              type: string
              example: test@example.com
            UserGoogleID:
              type: string
              example: google-abc-123
            UserTelegramID:
              type: string
              example: telegram-987654
    responses:
      200:
        description: LinkIdentityResponse
        schema:
          type: object
          properties:
            Success: { type: boolean }
            Message: { type: string }
            ApplicationUserID: { type: integer }
      400:
        description: Missing required fields
    """
    body = request.get_json(silent=True) or {}
    req = LinkIdentityRequest.from_dict(body)

    if req.ApplicationID is None or not req.UserIdentificator:
        return error_json("ApplicationID and UserIdentificator are required.", 400)

    if (
        req.UserName is None
        and req.Name is None
        and req.LastName is None
        and req.UserEmail is None
        and req.UserGoogleID is None
        and req.UserTelegramID is None
    ):
        return error_json(
            "At least one of UserName, Name, LastName, UserEmail, UserGoogleID, UserTelegramID must be provided.",
            400,
        )

    response = LinkIdentityBLL.link_identity(req)
    return to_json(response)
