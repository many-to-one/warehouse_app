from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from users import auth, schemas, crud
from users.schemas import *
from database.database import get_db
from users.models import *
from users.auth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession

templates = Jinja2Templates(directory="templates")


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


@router.post("/login/")
async def login_view(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"id": 1}
    )


@router.post("/logout")
async def logout(
        response: Response,
        user: schemas.UserBase = Depends(auth.get_current_user),
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ):
    blacklisted_token = TokenBlacklist(token=token)
    db.add(blacklisted_token)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="username")
    response.delete_cookie(key="is_admin")
    user.is_active = False
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "You have been logged out."}


@router.get("/user/{user_id}", response_model=UserBase)
async def get_user(
        user_id: int, 
        db: AsyncSession = Depends(get_db),
        user_: schemas.UserBase = Depends(auth.get_current_user),
    ):
    user = await crud.get_user_by_id(db, user_id=user_id)
    # print('###### current_user ##########', user)

    return user


@router.get("/all", response_model=List[UserBase])
async def get_user(
        db: AsyncSession = Depends(get_db),
        current_user: schemas.UserBase = Depends(auth.get_current_user),
    ):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.patch("/put_user", response_model=UserDisplay)
async def put_user(
        request: UserEditForm,
        response: Response,
        # user_form: UserCreateForm = Depends(UserCreateForm),
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


@router.delete("/delete_user_by_id/{user_id}")
async def delete_user_by_id(
    response: Response,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user: schemas.UserBase = Depends(auth.get_current_user)
):
    if user.is_admin == True:
        user_ = await crud.get_user_by_id(db, user_id=user_id)
        # print('########## user #############', user_.username)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="username")
        response.delete_cookie(key="is_admin")
        user.is_active == False
        
        await db.delete(user_)
        await db.commit()
        await db.flush()
        
        return {"detail": "User deleted successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Permission deny")
    

@router.delete("/delete_user_by_himself")
async def delete_user_by_himself(
    response: Response,
    db: AsyncSession = Depends(get_db),
    user: schemas.UserBase = Depends(auth.get_current_user)
):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="username")
    response.delete_cookie(key="is_admin")
    user.is_active == False
    await db.delete(user)
    await db.commit()
    await db.flush()

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
