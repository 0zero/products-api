from logging import INFO, basicConfig, getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.crud.product import CRUDProduct
from src.database.models.product import Product
from src.database.schemas.product import ProductCreate, ProductDBBase, ProductUpdate
from src.database.session import get_db

logger = getLogger(__name__)
basicConfig(level=INFO)

router = APIRouter(
    tags=["products"], responses={404: {"description": "No products found, sorry!"}}
)

# TODO: Add GET MANY endpoint


# POST endpoints
@router.post("/api/product", response_model=ProductDBBase, status_code=201)
async def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductDBBase:
    """
    POST endpoint to persist a Product to a Postgres database

    input params:
        product_in: ProductCreate pydantic class containing all the data
                    pertaining to the product to be created
        db: database session so that we can connect to our database

    return: ProductDBBase pydantic class containing all the data pertaining to the product
    """
    product_crud = CRUDProduct(Product)  # type: ignore

    return product_crud.create(db=db, obj_in=product_in)


# GET endpoints
@router.get("/api/product/{product_id}", response_model=ProductDBBase, status_code=200)
async def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductDBBase:
    """
    GET endpoint to retrieve a Product from a Postgres database

    input params:
        product_id: The ID of the product to retrieve
        db: database session so that we can connect to our database
    return: ProductDBBase pydantic class containing all the data pertaining to the product
    """
    product_crud = CRUDProduct(Product)  # type: ignore
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# DELETE endpoints
@router.delete(
    "/api/product/{product_id}", response_model=ProductDBBase, status_code=200
)
async def delete_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
) -> ProductDBBase:
    """
    DELETE endpoint to remove a Product from a Postgres database

    input params:
        product_id: The ID of the product to delete
        db: database session so that we can connect to our database
    return: ProductDBBase pydantic class containing all the data pertaining to the product
    """
    product_crud = CRUDProduct(Product)  # type: ignore
    product = product_crud.remove(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


# PUT endpoints
@router.put("/api/product/{product_id}", response_model=ProductDBBase, status_code=201)
async def update_product_by_id(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
) -> ProductDBBase:
    """
    PUT endpoint to update a Product in a Postgres database

    input params:
        product_id: The ID of the product to update
        product_in: ProductUpdate pydantic class containing all the data
                    pertaining to the product to be updated
        db: database session so that we can connect to our database
    return: ProductDBBase pydantic class containing all the data pertaining to the product
    """
    product_crud = CRUDProduct(Product)  # type: ignore
    db_product: Product | None = product_crud.get(db=db, id=product_id)

    if db_product:
        product = product_crud.update(db=db, db_obj=db_product, obj_in=product_in)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product
