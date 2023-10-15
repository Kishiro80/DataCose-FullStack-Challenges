from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.author.schemas import createSchema, responseSchema, updateSchema
from app.crud import CRUDBase
from app.database import get_db
from app.models import Author, Book

model = Author
root = "author"

createSchema = createSchema
responseSchema = responseSchema
updateSchema = updateSchema
crud_fn = CRUDBase[model, createSchema, responseSchema, updateSchema](model=model)


router = APIRouter()


@router.post(f"/{root}/create/")
async def create(input: createSchema, db: Session = Depends(get_db)):
    data = crud_fn.create(db, input)
    print(data)
    return data


#


@router.get(f"/{root}/id/", response_model=responseSchema)
async def read(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    return data


# , response_model=list[responseSchema]


@router.get(f"/{root}/all/")
async def reads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datas = crud_fn.get_multi(db, skip=skip, limit=limit)
    return datas


@router.get(f"/{root}/bookCount/")
async def readAndCount(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subquery = (
        db.query(Author.id.label("author_id"), func.count(Book.id).label("book_count"))
        .outerjoin(Author.book)
        .group_by(Author.id)
        .subquery()
    )

    authors = (
        db.query(Author, subquery.c.book_count)
        .options(joinedload(Author.book))
        .outerjoin(subquery, Author.id == subquery.c.author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    author_data = [{**author.__dict__, "book_count": book_count} for author, book_count in authors]

    return author_data


# , response_model=list[responseSchema]


@router.get(f"/{root}/search/")
async def searchs(query: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datas = crud_fn.get_multi_with_condition(db, condition=query, skip=skip, limit=limit)
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


@router.delete(f"/{root}/")
async def delete(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    crud_fn.delete(db, data)
    return None
