from logging import INFO, basicConfig, getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.crud.organisation import CRUDOrganisation
from src.database.models.organisation import Organisation
from src.database.schemas.organisation import (
    OrganisationCreate,
    OrganisationDBBase,
    OrganisationUpdate,
)
from src.database.session import get_db

logger = getLogger(__name__)
basicConfig(level=INFO)

router = APIRouter(
    tags=["organisations"],
    responses={404: {"description": "No organisations found, sorry!"}},
)

# TODO: Add GET MANY endpoint


# POST endpoints
@router.post("/api/organisation", response_model=OrganisationDBBase, status_code=201)
async def create_organisation(
    organisation_in: OrganisationCreate,
    db: Session = Depends(get_db),
) -> OrganisationDBBase:
    """
    POST endpoint to persist a Organisation to a Postgres database

    input params:
        organisation_in: OrganisationCreate pydantic class containing all the data
                    pertaining to the organisation to be created
        db: database session so that we can connect to our database

    return: OrganisationDBBase pydantic class containing all
            the data pertaining to the organisation
    """
    organisation_crud = CRUDOrganisation(Organisation)  # type: ignore
    return organisation_crud.create(db=db, obj_in=organisation_in)


# GET endpoints
@router.get(
    "/api/organisation/{organisation_id}",
    response_model=OrganisationDBBase,
    status_code=200,
)
async def get_organisation_by_id(
    organisation_id: int,
    db: Session = Depends(get_db),
) -> OrganisationDBBase:
    """
    GET endpoint to retrieve a Organisation from a Postgres database

    input params:
        organisation_id: The ID of the Organisation to retrieve
        db: database session so that we can connect to our database
    return: OrganisationDBBase pydantic class containing all
            the data pertaining to the organisation
    """
    organisation_crud = CRUDOrganisation(Organisation)  # type: ignore
    organisation = organisation_crud.get(db=db, id=organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found"
        )
    return organisation


# DELETE endpoints
@router.delete(
    "/api/organisation/{organisation_id}",
    response_model=OrganisationDBBase,
    status_code=200,
)
async def delete_organisation_by_id(
    organisation_id: int,
    db: Session = Depends(get_db),
) -> OrganisationDBBase:
    """
    DELETE endpoint to remove a organisation from a Postgres database

    input params:
        organisation_id: The ID of the organisation to delete
        db: database session so that we can connect to our database
    return: OrganisationDBBase pydantic class containing all
            the data pertaining to the organisation
    """
    organisation_crud = CRUDOrganisation(Organisation)  # type: ignore
    organisation = organisation_crud.remove(db=db, id=organisation_id)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="organisation not found"
        )
    return organisation


# PUT endpoints
@router.put(
    "/api/organisation/{organisation_id}",
    response_model=OrganisationDBBase,
    status_code=201,
)
async def update_organisation_by_id(
    organisation_id: int,
    organisation_in: OrganisationUpdate,
    db: Session = Depends(get_db),
) -> OrganisationDBBase:
    """
    PUT endpoint to update a organisation in a Postgres database

    input params:
        organisation_id: The ID of the organisation to update
        organisation_in: OrganisationUpdate pydantic class containing all the data
                    pertaining to the organisation to be updated
        db: database session so that we can connect to our database
    return: OrganisationDBBase pydantic class containing all
            the data pertaining to the organisation
    """
    organisation_crud = CRUDOrganisation(Organisation)  # type: ignore
    db_organisation: Organisation | None = organisation_crud.get(
        db=db, id=organisation_id
    )

    if db_organisation:
        organisation = organisation_crud.update(
            db=db, db_obj=db_organisation, obj_in=organisation_in
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found"
        )
    return organisation
