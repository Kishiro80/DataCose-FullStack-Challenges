# auth.py
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.crud import CRUDBase
from app.database import get_db
from app.models import User
from app.user.schemas import createSchema, responseSchema, updateSchema

model = User
crud_fn = CRUDBase[model, createSchema, responseSchema, updateSchema](model=model)
# This should be a secure and secret key for hashing and verifying passwords
PASSWORD_HASH_SECRET = "your-secret-password-hash-secret"

# Create an instance of the CryptContext class for password hashing
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Sample user data (you should replace this with your database logic)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        # Hashed password for "testpassword"
        "password": "$2b$12$xEVdR7dMoCtmf7kFL9jsj.LHki.L3IY.UuCNF1GjXelNqeyd1lG3m",
    },
}


def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hasher.hash(password)


# Function to authenticate a user based on username and password


def authenticate_user(db: Session, username: str, password: str):
    # In your route handler
    user = crud_fn.get_multi_with_condition(db, condition=f"username = '{username}'", skip=0, limit=1)
    print(user[0])
    if user is None or not verify_password(password, user[0].password):
        return None  # User not found or password is incorrect
    del user[0].password
    return user[0]  # Return a User object if authentication succeeds


# Function to create an access token (JWT) for an authenticated user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# dependencies.py


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode and verify the token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user claims (e.g., username) from the token payload
        id: str = payload.get("id")
        user = crud_fn.get_multi_with_condition(db, condition=f"id = '{id}'", skip=0, limit=1)[0]
        print(user)
        if user.username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # For this example, we create a User object with a username
        user = user

        return user
    except JWTError:
        # Token validation failed; raise an HTTPException with a 401 status code
        raise HTTPException(status_code=401, detail="Token validation failed")


# Middleware function to check the validity of JWT tokens in incoming requests


async def check_jwt_token(request: Request):
    # Retrieve the token from the "Authorization" header
    print(1)
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")

    print(1)
    # Check if the token starts with "Bearer "
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    print(1)
    # Extract the token without the "Bearer " prefix
    token = token.split(" ")[1]

    print(1)
    try:
        print(1)
        # Verify and decode the token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = decoded_token  # Attach the user data to the request state

    except JWTError:
        print(1)
        raise HTTPException(status_code=401, detail="Token validation failed")
