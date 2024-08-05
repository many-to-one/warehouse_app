from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from users import auth, crud
from database.database import get_db
from users.models import TokenBlacklist
from users.schemas import *
from users.auth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/token", response_model=Token,)
async def login_for_access_token(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    ):
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    user.is_active = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Strict')
    response.set_cookie(key="username", value=user.username, secure=True, samesite='Strict')
    response.set_cookie(key="is_admin", value=user.is_admin, httponly=True, secure=True, samesite='Strict')
    # print('################ cookies ################', response.body.decode)
   
    return {
            "access_token": access_token, 
            "token_type": "bearer"
        }

