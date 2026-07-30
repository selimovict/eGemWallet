from dal.database import Database
from models.register_user_service_model import RegisterUserRequest, RegisterUserResponse


class RegisterUserBLL:

    @staticmethod
    def register(request: RegisterUserRequest) -> RegisterUserResponse:
        query = """
            EXEC dbo.ApplicationUser_Register
                @ApplicationID     = %(ApplicationID)s,
                @UserIdentificator = %(UserIdentificator)s,
                @UserName          = %(UserName)s,
                @Name              = %(Name)s,
                @LastName          = %(LastName)s,
                @CountryCode       = %(CountryCode)s,
                @CurrencyCode      = %(CurrencyCode)s,
                @PromotionCode     = %(PromotionCode)s
        """

        params = {
            "ApplicationID":     request.ApplicationID,
            "UserIdentificator": request.UserIdentificator,
            "UserName":          request.UserName,
            "Name":              request.Name,
            "LastName":          request.LastName,
            "CountryCode":       request.CountryCode,
            "CurrencyCode":      request.CurrencyCode,
            "PromotionCode":     request.PromotionCode,
        }

        row = Database.query_single(query, params)
        return RegisterUserResponse.from_row(row)
