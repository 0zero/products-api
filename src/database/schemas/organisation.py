from pydantic import BaseModel

from src.database.models.base import OrganisationTypeEnum


class OrganisationDBBase(BaseModel):
    id: int
    Name: str
    Type: OrganisationTypeEnum

    class Config:
        orm_mode = True
