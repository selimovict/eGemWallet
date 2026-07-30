from dal.database import Database
from models.put_amount_service_model import PutAmountRequest, PutAmountResponse


class PutAmountBLL:

    @staticmethod
    def put_amount(request: PutAmountRequest) -> PutAmountResponse:
        query = """
            EXEC dbo.Wallet_Bet
                @ApplicationID         = %(ApplicationID)s,
                @UserID                = %(UserID)s,
                @CurrencyCode          = %(CurrencyCode)s,
                @Stake                 = %(Stake)s,
                @WinAmount             = %(WinAmount)s,
                @ExternalTransactionID = %(ExternalTransactionID)s,
                @Description           = %(Description)s
        """

        params = {
            "ApplicationID":         request.ApplicationID,
            "UserID":                request.UserID,
            "CurrencyCode":          request.CurrencyCode,
            "Stake":                 request.Stake,
            "WinAmount":             request.WinAmount,
            "ExternalTransactionID": request.ExternalTransactionID,
            "Description":           request.Description,
        }

        row = Database.query_single(query, params)
        return PutAmountResponse.from_row(row)
