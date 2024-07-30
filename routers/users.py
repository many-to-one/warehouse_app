from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from users import auth, schemas, crud, database
from users.schemas import *
from users.database import get_db
from users.models import *
from users.auth import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
        prefix="/users", 
        tags=["users"]
    )



@router.post("/registration/", response_model=UserDisplay)
async def create_user(
        user_form: UserCreateForm = Depends(UserCreateForm), 
        db: AsyncSession = Depends(get_db)
    ):
    user = await auth.get_user_by_email(db, email=user_form.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user_form=user_form)


@router.post("/logout/{user_id}")
async def logout(
        token: str = Depends(oauth2_scheme), 
        db: AsyncSession = Depends(get_db)
    ):
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    await db.commit()
    return {"message": "You have been logged out."}


@router.get("/user/{user_id}", response_model=UserDisplay)
async def get_user(
        user_id: int, 
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
        # current_user: schemas.UserBase = Depends(auth.get_current_user),
    ):
    db_user = await crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/all", response_model=List[UserDisplay])
async def get_user(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserBase = Depends(await auth.get_current_user),
    ):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/put_user/{user_id}", response_model=List[UserDisplay])
async def put_user(
        user_id: int,
        request: UserBase,
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserBase = Depends(await  auth.get_current_user),
    ):
    user = await crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return user
