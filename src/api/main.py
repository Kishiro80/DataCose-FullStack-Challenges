# main.py

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import models
from app.auth.router import router as auth_router
from app.auth.services import check_jwt_token, get_current_user
from app.author.router import router as author_router
from app.books.router import router as books_router
from app.config import engine
from app.user.router import router as user_router

app = FastAPI()
allowed_origins = [
    "http://localhost:3000",
    "https://example.com",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Set this to True if you allow cookies with CORS requests
    # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_methods=["*"],
    # You can specify specific headers (e.g., ["Authorization"])
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Middleware function to check JWT token for all routes


@app.middleware("http")
async def check_authentication(request, call_next):
    # Check if the requested route should be excluded from authentication
    excluded_paths = ["/auth/", "/user/create/"]

    # Check if the requested route should be excluded from authentication
    for path in excluded_paths:
        # print(request.url.path)
        if request.url.path == path or request.url.path.startswith(path):
            # print("pass")
            return await call_next(request)

    # Apply JWT token validation logic
    try:
        await check_jwt_token(request)
        return await call_next(request)
    except HTTPException as h:
        return JSONResponse(status_code=h.status_code, content={"detail": h.detail})
    except Exception as e:
        print("crash on checking jwt token", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


# Include the routers in the main app
app.include_router(user_router)
app.include_router(author_router)
app.include_router(books_router)
app.include_router(auth_router)
# ... Define more routes or include routers for other entities ...
# Run the app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
