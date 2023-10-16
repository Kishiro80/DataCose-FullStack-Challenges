# from app import models
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth.router import router as auth_router
from app.auth.services import check_jwt_token
from app.author.router import router as author_router
from app.book.router import router as book_router

# from app.config import engine
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
    allow_credentials=True,
    allow_methods=["*"],
)


# Create database tables
# models.Base.metadata.create_all(bind=engine)

# Middleware function to check JWT token for all routes


@app.middleware("http")
async def check_authentication(request, call_next):
    # Check if the requested route should be excluded from authentication
    excluded_paths = ["/auth/", "/user/create/"]
    # print("checking 1", request.method)

    if request.method == "OPTIONS":
        return JSONResponse(
            content=None,
            headers={"Access-Control-Allow-Headers ": "*",
                     "Access-Control-Allow-Origin": "*",
                     "Access-Control-Allow-Methods":"*"},
                     
        )
    # Check if the requested route should be excluded from authentication
    for path in excluded_paths:
        # print(request.url.path)
        if request.url.path == path or request.url.path.startswith(path):
            # print("pass")
            return await call_next(request)

    # Apply JWT token validation logic
    try:
        # token = request.headers.get("Authorization")
        # print(token)
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
app.include_router(book_router)
app.include_router(auth_router)

# ... Define more routes or include routers for other entities ...
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
