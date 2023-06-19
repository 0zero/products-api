from logging import INFO, basicConfig, getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.crud.order import CRUDOrder
from src.database.models.order import Order
from src.database.schemas.order import OrderCreate, OrderDBBase, OrderUpdate
from src.database.session import get_db

logger = getLogger(__name__)
basicConfig(level=INFO)

router = APIRouter(
    tags=["orders"],
    responses={404: {"description": "No order found, sorry!"}},
)

# TODO: Add GET MANY endpoint


def _copy_over_quantities(order_in: OrderCreate, order_ref: Order) -> OrderCreate:
    """
    Helper function to copy over quantities from a previous order to the new order

    input params:
        order_in: OrderCreate pydantic class containing all the data
                    pertaining to the order to be created
        order_ref: OrderDBBase pydantic class containing all the referenced order data from
                    which we will copy over quantities
    return: OrderCreate pydantic class containing all the updated data
            pertaining to the order to be created and referenced order data
    """
    ref_object = OrderDBBase(
        id=order_ref.id,  # type: ignore
        References=order_ref.References,  # type: ignore
        Type=order_ref.Type,  # type: ignore
        Products=order_ref.Products,  # type: ignore
        Organisation_id=order_ref.Organisation_id,  # type: ignore
    )
    dict_in = order_in.dict(exclude_unset=True)
    dict_ref = ref_object.dict(exclude_unset=True)

    for key, value in dict_ref.items():
        if key in dict_in and dict_in[key] is None:
            dict_in[key] = value

    return OrderCreate(**dict_in)


# POST endpoints
@router.post("/api/order", response_model=OrderDBBase, status_code=201)
async def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderDBBase:
    """
    POST endpoint to persist an Order to a Postgres database

    input params:
        order_in: OrderCreate pydantic class containing all the data
                    pertaining to the order to be created
        db: database session so that we can connect to our database

    return: OrderDBBase pydantic class containing all
            the data pertaining to the order
    """

    order_crud = CRUDOrder(Order)  # type: ignore
    if order_in.References:
        msg = (
            f"References {str(order_in.References)} found, copying over "
            "quantities that aren't specified in the order_in object."
        )
        logger.info(msg)
        ref_order = order_crud.get(db=db, id=order_in.References)
        if ref_order:
            updated_order_in = _copy_over_quantities(order_in, ref_order)
            return order_crud.create(db=db, obj_in=updated_order_in)

    return order_crud.create(db=db, obj_in=order_in)


# GET endpoints
@router.get(
    "/api/order/{order_id}",
    response_model=OrderDBBase,
    status_code=200,
)
async def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
) -> OrderDBBase:
    """
    GET endpoint to retrieve an Order from a Postgres database

    input params:
        order_id: The ID of the order to retrieve
        db: database session so that we can connect to our database
    return: OrderDBBase pydantic class containing all
            the data pertaining to the order
    """
    order_crud = CRUDOrder(Order)  # type: ignore
    order = order_crud.get(db=db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    return order


# DELETE endpoints
@router.delete(
    "/api/order/{order_id}",
    response_model=OrderDBBase,
    status_code=200,
)
async def delete_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
) -> OrderDBBase:
    """
    DELETE endpoint to remove an Order from a Postgres database

    input params:
        order_id: The ID of the order to delete
        db: database session so that we can connect to our database
    return: OrderDBBase pydantic class containing all
            the data pertaining to the order
    """
    order_crud = CRUDOrder(Order)  # type: ignore
    order = order_crud.remove(db=db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    return order


# PUT endpoints
@router.put(
    "/api/order/{order_id}",
    response_model=OrderDBBase,
    status_code=201,
)
async def update_order_by_id(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
) -> OrderDBBase:
    """
    PUT endpoint to update an Order in a Postgres database

    input params:
        order_id: The ID of the order to update
        order_in: OrderUpdate pydantic class containing all the data
                    pertaining to the order to be updated
        db: database session so that we can connect to our database
    return: OrderDBBase pydantic class containing all
            the data pertaining to the order
    """
    order_crud = CRUDOrder(Order)  # type: ignore
    db_order: Order | None = order_crud.get(db=db, id=order_id)

    # TODO: do we need to copy over quantities here if a reference is added?
    if db_order:
        order = order_crud.update(db=db, db_obj=db_order, obj_in=order_in)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    return order