from dal.database import Database
from models.user_identity_service_model import UserIdentityRequest, UserIdentityResponse


class UserIdentityBLL:

    @staticmethod
    def get_by_identificator(request: UserIdentityRequest) -> UserIdentityResponse | None:
        sql = """
            SELECT TOP 1
                ApplicationUserID,
                ApplicationID,
                UserIdentificator,
                CreatedDateTime,
                UserName,
                Name,
                LastName,
                CountryCode,
                ApplicationUserGuid,
                UserEmail,
                UserGoogleID,
                UserTelegramID
            FROM dbo.ApplicationUser
            WHERE ApplicationID     = %(ApplicationID)s
              AND UserIdentificator = %(UserIdentificator)s
        """

        params = {
            "ApplicationID":     request.ApplicationID,
            "UserIdentificator": request.UserIdentificator,
        }

        row = Database.query_single(sql, params)
        return UserIdentityResponse.from_row(row) if row else None
