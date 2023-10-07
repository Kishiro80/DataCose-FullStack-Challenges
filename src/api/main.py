# main.py

from app import models
from app.config import engine
from app.user.router import router as user_router
from app.author.router import router as author_router
from app.books.router import router as books_router
from fastapi import FastAPI, HTTPException

app = FastAPI()


def authenticate(request):
    # Implement your authentication logic here
    user_id = 0  # Replace with your actual authentication logic

    if not user_id:

        print("cant")
        raise HTTPException(
            status_code=401, detail="Authentication failed")

    # Store the authenticated user information in the Request state
    request.state.user_id = user_id


@app.middleware("http")
async def check_authentication(request, call_next):
    # Check if the requested route should be excluded from authentication
    # if request.url.path in ["/author/4/", "/login"]:
    #     return await call_next(request)

    # # Apply authentication logic
    # authenticate(request)

    response = await call_next(request)
    return response

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include the routers in the main app
app.include_router(user_router)
app.include_router(author_router)
app.include_router(books_router)
# ... Define more routes or include routers for other entities ...

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
