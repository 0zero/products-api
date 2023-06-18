from sqlalchemy.orm import Session

from src.database.crud.base import CRUDBase
from src.database.models.base import OrganisationTypeEnum
from src.database.models.organisation import Organisation
from src.database.schemas.organisation import OrganisationCreate, OrganisationDBBase


class CRUDOrganisation(CRUDBase[Organisation, OrganisationCreate, OrganisationCreate]):
    def __init__(self, model: Organisation):
        super().__init__(model)
