from logging import INFO, basicConfig, getLogger
from typing import Any, Dict, List, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query, status
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


def _copy_over_quantities(
    order_in: OrderCreate, order_ref: Order
) -> Tuple[OrderCreate, Dict[str, Any]]:
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

    fields_updated_by_reference = {}
    for key, value in dict_ref.items():
        if key in dict_in and dict_in[key] is None:
            dict_in[key] = value
            fields_updated_by_reference[key] = value

    return OrderCreate(**dict_in), fields_updated_by_reference


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
            updated_order_in, updated_details = _copy_over_quantities(
                order_in, ref_order
            )
            logger.info(
                f"Updated order_in object from reference with the following: {updated_details}"
            )
            return order_crud.create(db=db, obj_in=updated_order_in)

    order_created, product_ids_created = order_crud.create_new_order(
        db=db, obj_in=order_in
    )

    logger.info(
        f"Order {order_created.id} created with {str(len(product_ids_created))} "
        "new products: {product_ids_created}."
    )
    return order_created


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


@router.get("/api/order", response_model=List[OrderDBBase], status_code=200)
async def get_all_orders(
    db: Session = Depends(get_db),
    skip: int = Query(
        default=0,
        description=("How many Orders to skip before returning the remaining Orders"),
        ge=0,
    ),
    limit: int = Query(
        default=10,
        description="Limit the number of Orders displayed on each page",
        ge=1,
    ),
) -> List[Order]:
    """
    GET endpoint to retrieve all Orders from a Postgres database

    input params:
        db: database session so that we can connect to our database
        skip: How many Orders to skip before returning the remaining Orders
        limit: Limit the number of Orders displayed on each page
    return: List of OrderDBBase pydantic class containing all the
            data pertaining to the order
    """
    order_crud = CRUDOrder(Order)  # type: ignore
    orders = order_crud.get_multi(db=db, skip=skip, limit=limit)
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found"
        )
    return orders


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
