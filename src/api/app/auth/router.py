from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.services import authenticate_user, create_access_token, get_current_user
from app.user.schemas import responseSchema,   changePassSchema
from app.database import get_db

root = "auth"
router = APIRouter()

# Endpoint for user login and to generate access token


@router.post(f"/{root}/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    print(form_data.username, form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint to get the current user's data


@router.get(f"/{root}/users/me", response_model=responseSchema)
async def read_users_me(current_user: responseSchema = Depends(get_current_user)):
    return current_user

# Endpoint to logout (optional)


@router.post(f"/{root}/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

# Optional endpoint to refresh the access token (if using JWT token with expiration)


@router.post(f"/{root}/refresh")
async def refresh_access_token(current_user: responseSchema = Depends(get_current_user)):
    access_token = create_access_token(data={"sub": current_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Optional endpoint to change password (if needed)


@router.post(f"/{root}/change-password")
async def change_password(current_user: changePassSchema = Depends(get_current_user)):
    # You can implement password change logic here
    return {"message": "Password changed successfully"}
