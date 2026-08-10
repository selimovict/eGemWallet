from models.base_service_model import BaseServiceModel


class LinkIdentityRequest(BaseServiceModel):
    """Ulazni parametri za dbo.ApplicationUser_LinkIdentity."""

    def __init__(self):
        self.ApplicationID = None
        self.UserIdentificator = None
        self.UserName = None
        self.Name = None
        self.LastName = None
        self.UserEmail = None
        self.UserGoogleID = None
        self.UserTelegramID = None


class LinkIdentityResponse(BaseServiceModel):
    """Rezultat iz dbo.ApplicationUser_LinkIdentity (prvi result set)."""

    def __init__(self):
        self.Success = None
        self.Message = None
        self.ApplicationUserID = None
