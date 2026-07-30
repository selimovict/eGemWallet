from models.base_service_model import BaseServiceModel


class PutAmountRequest(BaseServiceModel):
    """Ulazni parametri za dbo.Wallet_Bet."""

    def __init__(self):
        self.ApplicationID = None
        self.UserID = None
        self.CurrencyCode = None
        self.Stake = None
        self.WinAmount = 0
        self.ExternalTransactionID = None
        self.Description = None


class PutAmountResponse(BaseServiceModel):
    """Rezultat iz dbo.Wallet_Bet."""

    def __init__(self):
        self.Success = None
        self.Message = None
        self.WalletID = None
        self.RealBalance = None
        self.BonusBalance = None
        self.StakeFromBonus = None
        self.StakeFromReal = None
        self.PromotionOutcome = None
        self.UserPromotionID = None
        self.WagerCompleted = None
        self.WagerRequired = None
        self.BonusConverted = None
        self.BonusForfeited = None
