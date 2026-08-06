from dal.database import Database
from models.get_balance_service_model import GetBalanceRequest, GetBalanceResponse



class GetBalanceBLL:

    @staticmethod
    def get_balance(request: GetBalanceRequest) -> GetBalanceResponse:
        query = """
            EXEC dbo.Wallet_GetBalance
                @ApplicationID = %(ApplicationID)s,
                @UserID        = %(UserID)s,
                @CurrencyCode  = %(CurrencyCode)s
        """

        params = {
            "ApplicationID": request.ApplicationID,
            "UserID":        request.UserID,
            "CurrencyCode":  request.CurrencyCode,
        }

        row = Database.query_single(query, params)
        return GetBalanceResponse.from_row(row)
