from models.base_service_model import BaseServiceModel


class UserIdentityRequest(BaseServiceModel):
    """Ulazni parametri za SELECT iz dbo.ApplicationUser."""

    def __init__(self):
        self.ApplicationID = None
        self.UserIdentificator = None


class UserIdentityResponse(BaseServiceModel):
    """Svi podaci o korisniku iz dbo.ApplicationUser."""

    def __init__(self):
        self.ApplicationUserID = None
        self.ApplicationID = None
        self.UserIdentificator = None
        self.CreatedDateTime = None
        self.UserName = None
        self.Name = None
        self.LastName = None
        self.CountryCode = None
        self.ApplicationUserGuid = None
        self.UserEmail = None
        self.UserGoogleID = None
        self.UserTelegramID = None
