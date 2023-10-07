

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models import Book
from app.books.schemas import createSchema, responseSchema,  updateSchema
from app.crud import CRUDBase
from app.database import get_db

model = Book
root = 'books'

createSchema = createSchema
responseSchema = responseSchema
updateSchema = updateSchema
crud_fn = CRUDBase[model, createSchema,
                   responseSchema, updateSchema](model=model)


router = APIRouter()


@router.post(f"/{root}/create/")
async def create(input: createSchema, db: Session = Depends(get_db)):
    data = crud_fn.create(db, input)
    return data

# , response_model=responseSchema


@router.get(f"/{root}/{{id}}/")
async def read(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    return data

# , response_model=list[responseSchema]


@router.get(f"/{root}/")
async def reads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datas = crud_fn.get_multi(db, skip=skip, limit=limit)
    return datas

# , response_model=list[responseSchema]


@router.get(f"/{root}/search/")
async def searchs(query: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datas = crud_fn.get_multi_with_condition(
        db, condition=query, skip=skip, limit=limit)
    return datas

# , response_model=responseSchema


@router.put(f"/{root}/{{id}}/")
async def update(id: int, input: updateSchema, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    data = crud_fn.update(db, data, input)
    return data

# , response_model=None


@router.delete(f"/{root}/{{id}}/")
async def delete(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    crud_fn.delete(db, data)
    return None
