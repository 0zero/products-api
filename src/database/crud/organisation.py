from src.database.crud.base import CRUDBase
from src.database.models.organisation import Organisation
from src.database.schemas.organisation import OrganisationDBBase, OrganisationCreate
from src.database.models.base import OrganisationTypeEnum

from sqlalchemy.orm import Session


class CRUDOrganisation(CRUDBase[Organisation, OrganisationCreate, OrganisationCreate]):
    def __init__(self, model: Organisation):
        super().__init__(model)
