from typing import Generic, TypeVar

from sqlalchemy import text  # Import the text function
from sqlalchemy.orm import Session

CreateSchemaType = TypeVar("CreateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ModelType = TypeVar("ModelType")


# Dependency to get the database session


class CRUDBase(Generic[ModelType, CreateSchemaType, ResponseSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: CreateSchemaType) -> ResponseSchemaType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> ResponseSchemaType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[ResponseSchemaType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi_with_condition(
        self,
        db: Session,
        condition: str = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ResponseSchemaType]:
        query = db.query(self.model)
        if condition:
            query = query.filter(text(condition))
        return query.offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ResponseSchemaType:
        for field in obj_in.dict(exclude_unset=True):
            setattr(db_obj, field, obj_in.dict()[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()
