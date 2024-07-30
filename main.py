from fastapi import Depends, FastAPI
from routers import users, authentication
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return {"message": "Hello World here"}
