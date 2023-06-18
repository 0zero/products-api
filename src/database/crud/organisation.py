from src.database.crud.base import CRUDBase
from src.database.models.organisation import Organisation
from src.database.schemas.organisation import OrganisationDBBase
from src.database.models.base import OrganisationTypeEnum

from sqlalchemy.orm import Session

class CRUDOrganisation(CRUDBase):
    def __init__(self, model: Organisation):
        super().__init__(model)
