from models.base_service_model import BaseServiceModel


class RegisterUserRequest(BaseServiceModel):
    """Ulazni parametri za dbo.ApplicationUser_Register."""

    def __init__(self):
        self.ApplicationID = None
        self.UserIdentificator = None
        self.UserName = None
        self.Name = None
        self.LastName = None
        self.CountryCode = None
        self.CurrencyCode = "USD"
        self.PromotionCode = "WELCOME1000"


class RegisterUserResponse(BaseServiceModel):
    """Rezultat iz dbo.ApplicationUser_Register (prvi result set)."""

    def __init__(self):
        self.Success = None
        self.Message = None
        self.ApplicationUserID = None
        self.WalletID = None
        self.ApplicationUserGuid = None
        self.CurrencyCode = None
