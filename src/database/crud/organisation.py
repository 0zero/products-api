from src.database.crud.base import CRUDBase
from src.database.models.organisation import Organisation
from src.database.schemas.organisation import OrganisationCreate, OrganisationUpdate

# TODO: Add Get Many with filters


class CRUDOrganisation(CRUDBase[Organisation, OrganisationCreate, OrganisationUpdate]):
    """
    Organisation CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    """

    def __init__(self, model: Organisation):
        super().__init__(model)
