from models.base_service_model import BaseServiceModel


class GetBalanceRequest(BaseServiceModel):
    """Ulazni parametri za dbo.Wallet_GetBalance."""

    def __init__(self):
        self.ApplicationID = None
        self.UserID = None
        self.CurrencyCode = None


class GetBalanceResponse(BaseServiceModel):
    """Rezultat iz dbo.Wallet_GetBalance (jedan red)."""

    def __init__(self):
        self.ApplicationID = None
        self.UserID = None
        self.CurrencyCode = None

        self.WalletExists = None
        self.WalletID = None
        self.RealBalance = None
        self.BonusBalance = None
        self.TotalBalance = None
        self.WalletUpdated = None

        self.HasActivePromotion = None
        self.UserPromotionID = None
        self.PromotionCode = None
        self.PromotionName = None
        self.PromotionTypeName = None
        self.PromotionActionID = None
        self.PromotionCurrency = None

        self.FreeSpinsGranted = None
        self.FreeSpinsRemaining = None
        self.BonusGranted = None
        self.BonusRemaining = None

        self.WagerRequired = None
        self.WagerCompleted = None
        self.WagerRemaining = None
        self.WagerProgressPct = None

        self.MaxCashOut = None
        self.MaxBet = None
        self.ActivatedDate = None
        self.ExpireDate = None
        self.DaysToExpire = None
