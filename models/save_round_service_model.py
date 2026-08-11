from models.base_service_model import BaseServiceModel


class SaveRoundResponse(BaseServiceModel):
    """Rezultat INSERT-a u dbo.GamePlayRound."""

    def __init__(self):
        self.RoundID = None
        self.ExternalRoundIdentifier = None
        self.Success = None
        self.Message = None
