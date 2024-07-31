from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import auth
from users.schemas import *
from users.crud import *
from users.models import *
from sqlalchemy.future import select


async def create_user(db: AsyncSession, user_form: UserCreateForm):
    hashed_password = auth.get_password_hash(user_form.password)
    db_user = User(
        username=user_form.username, 
        email=user_form.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()  # Extract the first user from the result
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
