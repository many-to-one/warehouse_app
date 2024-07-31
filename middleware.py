# # middleware.py
# from fastapi import FastAPI, HTTPException, Request, Depends
# from fastapi.responses import RedirectResponse
# from starlette.middleware.base import BaseHTTPMiddleware
# from sqlalchemy.ext.asyncio import AsyncSession
# from users.auth import get_current_user
# from database.database import get_db
# from users.models import User

# class AdminAuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Skip middleware for non-admin routes
#         if not request.url.path.startswith("/admin"):
#             response = await call_next(request)
#             return response
        
#         # Attempt to get the current user
#         token = request.cookies.get("access_token")
#         if not token:
#             return RedirectResponse(url="/login")
        
#         try:
#             user: User = await get_current_user(token=token, db=Depends(get_db))
#             request.state.user = user
#         except HTTPException:
#             return RedirectResponse(url="/login")
        
#         response = await call_next(request)
#         return response

