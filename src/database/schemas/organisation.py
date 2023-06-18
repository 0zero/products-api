from pydantic import BaseModel

from src.database.models.base import OrganisationTypeEnum


class OrganisationCreate(BaseModel):
    Name: str
    Type: OrganisationTypeEnum


class OrganisationDBBase(OrganisationCreate):
    id: int

    class Config:
        orm_mode = True
