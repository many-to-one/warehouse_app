# from fastapi import APIRouter, Depends, HTTPException, Request
# from fastapi.responses import RedirectResponse

# from users.auth import get_current_user, oauth2_scheme

# router = APIRouter(
#         prefix="/admin", 
#         tags=["admin"]
#     )

# @router.middleware("http")
# async def admin_auth_middleware(request: Request, call_next):
#     if request.url.path.startswith("/admin") and not request.url.path.startswith("/admin/static"):
#         # token = request.cookies.get("access_token")
#         token: str = Depends(oauth2_scheme), 
#         if not token:
#             return RedirectResponse(url="/login")
#         try:
#             user = await get_current_user(token=token)
#             request.state.user = user
#         except HTTPException:
#             return RedirectResponse(url="/login")
#     response = await call_next(request)
#     return response
