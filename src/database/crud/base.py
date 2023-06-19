from typing import Any, Dict, Generic, List, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD class with default methods to Create, Read, Update, Delete (CRUD).
    
    Keyword arguments:
    ModelType -- SQLAlchemy model class
    CreateSchemaType -- Pydantic model class used to create new records
    UpdateSchemaType -- Pydantic model class used to update existing records

    Return: return_description
    """
    
    def __init__(self, model: ModelType):
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.

        Keyword arguments:
            db -- Database session
            obj_in -- Pydantic model class used to create new records
        Return: SQLAlchemy model class
        """
        
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj  # type: ignore

    def get(self, db: Session, id: int) -> ModelType | None:
        """
        Retrieve a record from the database.

        Keyword arguments:
            db -- Database session
            id -- ID of the record to retrieve
        Return: SQLAlchemy model class or None
        """        
        result = db.query(self.model).filter(self.model.id == id).first()
        return result if result else None

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        """
        Retrieve multiple records from the database.

        Keyword arguments:
            db -- Database session
            skip -- Number of records to skip
            limit -- Number of records to retrieve
        Return: List of SQLAlchemy model classes or None
        """         
        result = (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )
        return result if result else None  # type: ignore

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update a record in the database.

        Keyword arguments:
            db -- Database session
            db_obj -- SQLAlchemy model class
            obj_in -- Pydantic model class used to update existing records
        Return: SQLAlchemy model class
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete a record from the database.

        Keyword arguments:
            db -- Database session
            id -- ID of the record to delete
        Return: SQLAlchemy model class of the deleted record
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        db.delete(obj)
        db.commit()
        return obj  # type: ignore
