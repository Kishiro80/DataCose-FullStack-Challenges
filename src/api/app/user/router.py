from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.services import get_password_hash
from app.crud import CRUDBase
from app.database import get_db
from app.models import User
from app.user.schemas import createSchema, responseSchema, updateSchema

model = User
createSchema = createSchema
responseSchema = responseSchema
updateSchema = updateSchema
crud_fn = CRUDBase[model, createSchema, responseSchema, updateSchema](model=model)


router = APIRouter()


root = "user"


@router.post(f"/{root}/create/")
async def create(input: createSchema, db: Session = Depends(get_db)):
    # Hash the user's password before creating the user
    hashed_password = get_password_hash(input.password)
    user_data = input.dict()
    user_data["password"] = hashed_password

    # Create the user with the hashed password
    try:
        user = crud_fn.create(db, createSchema(**user_data))
        return user
    except:
        return {"status": "fail"}


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


@router.delete(f"/{root}/{{id}}/")
async def delete(id: int, db: Session = Depends(get_db)):
    data = crud_fn.get(db, id)
    if data is None:
        raise HTTPException(status_code=404, detail=f"{root} not found")
    crud_fn.delete(db, data)
    return None
