from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.future import select
from users import auth, schemas, crud
from users.schemas import *
from database.database import get_db
from users.models import *
from users.auth import oauth2_scheme
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
        response: Response,
        user: schemas.UserBase = Depends(auth.get_current_user),
        user_form: UserLogOut = Depends(UserLogOut),
        token: str = Depends(oauth2_scheme), 
        db: AsyncSession = Depends(get_db)
    ):
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="username")
    response.delete_cookie(key="is_admin")
    user.is_active == False
    await db.commit()
    return {"message": "You have been logged out."}


@router.get("/user/{user_id}", response_model=UserDisplay)
async def get_user(
        user_id: int, 
        db: AsyncSession = Depends(get_db),
        user: schemas.UserBase = Depends(auth.get_current_user),
    ):
    # user = await crud.get_user_by_id(db, user_id=user_id)
    # print('###### current_user ##########', user)

    return user


@router.get("/all", response_model=List[UserDisplay])
async def get_user(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserBase = Depends(auth.get_current_user),
    ):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.patch("/put_user/{user_id}", response_model=UserDisplay)
async def put_user(
        user_id: int,
        request: UserBase,
        db: AsyncSession = Depends(get_db),
        user: schemas.UserBase = Depends(auth.get_current_user),
    ):
    # user = await crud.get_user_by_id(db, user_id=user_id)
    
    if request.username is not None:
        user.username = request.username
    if request.email is not None:
        user.email = request.email

    db.add(user)
    await db.commit()  
    await db.refresh(user)

    return user


@router.delete("/deletet_user/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user: schemas.UserBase = Depends(auth.get_current_user)
):
    # user = await crud.get_user_by_id(db, user_id=user_id)
    
    db.delete(user)
    await db.commit()
    
    return {"detail": "User deleted successfully!"}


@router.post("/change_password/{user_id}")
async def change_password(
    user_id: int,
    request: ChangePassword,
    db: AsyncSession = Depends(get_db),
    user: schemas.UserBase = Depends(auth.get_current_user),
):
    # user = await crud.get_user_by_id(db, user_id=user_id)
    new_password = await auth.new_password(
        db,
        request.email,
        request.old_password,
        request.new_password,
    )
    
    user.hashed_password = new_password
    await db.commit()
    
    return {"message": "The password has been changed successfully!"}
