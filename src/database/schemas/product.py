from pydantic import BaseModel


class ProductCreate(BaseModel):
    Category: str
    Variety: str
    Packaging: str


class ProductDBBase(ProductCreate):
    id: int

    class Config:
        orm_mode = True
