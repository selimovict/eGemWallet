from flask import Blueprint, request

from api.response import to_json, error_json
from bll.user_identity_bll import UserIdentityBLL
from models.user_identity_service_model import UserIdentityRequest


user_identity_bp = Blueprint("user_identity_bp", __name__)


@user_identity_bp.route("/identity-by-identificator", methods=["POST"])
def user_identity_by_identificator():
    """Vraca podatke o korisniku na osnovu ApplicationID i UserIdentificator.
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
    responses:
      200:
        description: UserIdentityResponse
        schema:
          type: object
          properties:
            ApplicationUserID:    { type: integer }
            ApplicationID:        { type: integer }
            UserIdentificator:    { type: string }
            CreatedDateTime:      { type: string }
            UserName:             { type: string }
            Name:                 { type: string }
            LastName:             { type: string }
            CountryCode:          { type: string }
            ApplicationUserGuid:  { type: string }
            UserEmail:            { type: string }
            UserGoogleID:         { type: string }
            UserTelegramID:       { type: string }
      400:
        description: Missing required fields
      404:
        description: Identificator not found
    """
    body = request.get_json(silent=True) or {}
    req  = UserIdentityRequest.from_dict(body)

    if req.ApplicationID is None or not req.UserIdentificator:
        return error_json("ApplicationID and UserIdentificator are required.", 400)

    user = UserIdentityBLL.get_by_identificator(req)

    if user is None:
        return error_json("Registered identificator does not exist.", 404)

    return to_json(user)
