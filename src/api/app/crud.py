from functools import wraps
from app.config import SessionLocal
from app.config import Base
from typing import TypeVar, Generic, Type, Optional, List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session


def get_db(request: Request = Depends()):
    return request.state.db


CreateSchemaType = TypeVar("CreateSchemaType")
ResponseSchemaType = TypeVar("ResponseSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ModelType = TypeVar("ModelType")


# Dependency to get the database session

class CRUDBase(Generic[ModelType, CreateSchemaType, ResponseSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self,  db: Session, obj_in: CreateSchemaType) -> ResponseSchemaType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    # db: Session = Depends(get_db)

    def get(self, db: Session, id: int) -> Optional[ResponseSchemaType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ResponseSchemaType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_multi_with_condition(
        self,   db: Session, condition: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[ResponseSchemaType]:
        query = db.query(self.model)
        if condition:
            query = query.filter(condition)
        return query.offset(skip).limit(limit).all()

    def update(
        self,   db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ResponseSchemaType:
        for field in obj_in.dict(exclude_unset=True):
            setattr(db_obj, field, obj_in.dict()[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> None:
        db.delete(db_obj)
        db.commit()


# def crud_routes(
#     router: APIRouter,
#     model: Type[ModelType],
#     root: str,
#     create_schema: Type[CreateSchemaType],
#     response_schema: Type[ResponseSchemaType],
#     update_schema: Type[UpdateSchemaType],
#     crud_fn: CRUDBase[ModelType, CreateSchemaType,
#                       ResponseSchemaType, UpdateSchemaType]
# ):
#     def decorator(func):
#         @router.post(f"/{root}/create/", response_model=response_schema)
#         async def create(input: create_schema, db: Session = Depends(get_db)):
#             data = crud_fn.create(db, input)
#             return data

#         @router.get(f"/{root}/{{id}}/", response_model=response_schema)
#         async def read(id: int, db: Session = Depends(get_db)):
#             data = crud_fn.get(db, id)
#             if data is None:
#                 raise HTTPException(
#                     status_code=404, detail=f"{root} not found")
#             return data

#         @router.get(f"/{root}/", response_model=list[response_schema])
#         async def reads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#             datas = crud_fn.get_multi(db, skip=skip, limit=limit)
#             return datas

#         @router.get(f"/{root}/search/", response_model=list[response_schema])
#         async def searchs(query: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#             datas = crud_fn.get_multi_with_condition(
#                 db, condition=query, skip=skip, limit=limit)
#             return datas

#         @router.put(f"/{root}/{{id}}/", response_model=response_schema)
#         async def update(id: int, input: update_schema, db: Session = Depends(get_db)):
#             data = crud_fn.get(db, id)
#             if data is None:
#                 raise HTTPException(
#                     status_code=404, detail=f"{root} not found")
#             data = crud_fn.update(db, data, input)
#             return data

#         @router.delete(f"/{root}/{{id}}/", response_model=None)
#         async def delete(id: int, db: Session = Depends(get_db)):
#             data = crud_fn.get(db, id)
#             if data is None:
#                 raise HTTPException(
#                     status_code=404, detail=f"{root} not found")
#             crud_fn.delete(db, data)
#             return None

#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # You can add additional functionality here if needed
#             return func(*args, **kwargs)

#         return wrapper

#     return decorator
# limitation, cannot do this since i cant get the Depends to work.
