from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from routers import users, authentication, products
from users import auth, schemas
from users.models import ProductAdmin, TokenBlacklistAdmin, UserAdmin
from database.database import async_engine, get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(products.router)

admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TokenBlacklistAdmin)
admin.add_view(ProductAdmin)

@app.middleware("http")
async def admin_auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/static"):
        token = request.cookies.get("access_token")
        is_admin = request.cookies.get("is_admin")
        print('################ request.cookies ++ ################', request.cookies)
        print('################ request.cookies is_admin ################', is_admin)
        if not token or is_admin == "False":
            return RedirectResponse(url="/login")  
        
    response = await call_next(request)
    return response            
            
        


@app.get("/")
async def root(request: Request, db: AsyncSession = Depends(get_db)):

    username = request.cookies.get("username")
    user_id = request.cookies.get("user_id")
    access_token = request.cookies.get("access_token")
    # print('################ user_id ################', user_id)
    user = await auth.get_current_user(access_token, db)
    print('################ user__ ################', user)
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={
                "username": username,
                "user_id": user_id,
            }
    )

@app.get("/login")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"id": 1}
    )

