from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from sqladmin import Admin

from routers import users, authentication, products
from users.models import ProductAdmin, TokenBlacklistAdmin, UserAdmin
from database.database import async_engine

app = FastAPI()


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
async def root():
    return {"message": "Hello World here"}

