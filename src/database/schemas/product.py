from pydantic import BaseModel


class ProductDBBase(BaseModel):
    id: int
    Category: str
    Variety: str
    Packaging: str

    class Config:
        orm_mode = True
