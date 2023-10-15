from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.author.schemas import cleanResponseSchema as authorschema
from app.book.schemas import createSchema, responseSchema, updateSchema
from app.crud import CRUDBase
from app.database import get_db
from app.models import Author, Book

model = Book
root = "book"

createSchema = createSchema
responseSchema = responseSchema
updateSchema = updateSchema
crud_fn = CRUDBase[model, createSchema, responseSchema, updateSchema](model=model)


router = APIRouter()


@router.post(f"/{root}/create/")
async def create(input: createSchema, db: Session = Depends(get_db)):
    data = crud_fn.create(db, input)
    return data


# , response_model=responseSchema


@router.get(f"/{root}/id/")
async def read(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    return data


# , response_model=list[responseSchema]


def get_books_with_author_info(db: Session, skip: int = 0, limit: int = 100):
    books = crud_fn.get_multi(db, skip=skip, limit=limit)
    result = []
    for book in books:
        author = db.query(Author).filter(Author.id == book.author_id).first()
        print(book, author)
        if author:
            book_response = responseSchema(
                id=book.id,
                title=book.title,
                num_pages=book.num_pages,
                author=authorschema(id=author.id, name=author.name),
            )
        else:
            book_response = responseSchema(id=book.id, title=book.title, num_pages=book.num_pages)
        result.append(book_response)
    return result


@router.get(f"/{root}/all/")
async def get_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_books_with_author_info(db, skip, limit)


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
