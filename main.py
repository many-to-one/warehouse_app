from fastapi import Depends, FastAPI, HTTPException
from routers import users, authentication
from sqladmin import Admin

from users.auth import get_current_user, oauth2_scheme
from users.models import UserAdmin
from database.database import async_engine, get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


app.include_router(users.router)
app.include_router(authentication.router)

admin = Admin(app, async_engine)
# admin.add_view(UserAdmin)

from fastapi import Request
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from users.auth import SECRET_KEY, ALGORITHM
@app.middleware("http")
async def admin_auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/static"):
        # Extract the token from the request
        # token = await oauth2_scheme(request)
        # token = request.cookies.get("access_token")
        # token: str = Depends(oauth2_scheme)
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # username: str = payload.get("sub")
        user = request.cookies
        print('################ user ################', user)
        # if not token:
        #     return RedirectResponse(url="/login")

        
        # Get a database session
        # async with get_db() as db:
        #     try:
        #         user = await get_current_user(token=token, db=db)
        #         print('################ user ################', user)
        #         request.state.user = user
        #     except HTTPException:
        #         return RedirectResponse(url="/login")
                
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Hello World here"}

