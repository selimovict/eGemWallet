from dal.database import Database
from models.link_identity_service_model import LinkIdentityRequest, LinkIdentityResponse


class LinkIdentityBLL:

    @staticmethod
    def link_identity(request: LinkIdentityRequest) -> LinkIdentityResponse:
        query = """
            EXEC dbo.ApplicationUser_LinkIdentity
                @ApplicationID     = %(ApplicationID)s,
                @UserIdentificator = %(UserIdentificator)s,
                @UserName          = %(UserName)s,
                @Name              = %(Name)s,
                @LastName          = %(LastName)s,
                @UserEmail         = %(UserEmail)s,
                @UserGoogleID      = %(UserGoogleID)s,
                @UserTelegramID    = %(UserTelegramID)s
        """

        params = {
            "ApplicationID":     request.ApplicationID,
            "UserIdentificator": request.UserIdentificator,
            "UserName":          request.UserName,
            "Name":              request.Name,
            "LastName":          request.LastName,
            "UserEmail":         request.UserEmail,
            "UserGoogleID":      request.UserGoogleID,
            "UserTelegramID":    request.UserTelegramID,
        }

        row = Database.query_single(query, params)
        return LinkIdentityResponse.from_row(row)
