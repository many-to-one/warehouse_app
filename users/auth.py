from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from database import database
from . import schemas, models
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

import os
from dotenv import load_dotenv
load_dotenv()

# to get a string like this run:
# python generate_secret_key.py
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password: str):
    return pwd_context.hash(password)



async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    user = result.scalar_one_or_none()
    return user



async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))  # Await the query execution
    user = result.scalar_one_or_none()  # Get one user or none
    return user



async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    print('user', user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def new_password(db: AsyncSession, email: str, old_password: str, new_password: str):
    user = await get_user_by_email(db, email)
    print('user', user)
    if not user:
        return False
    if verify_password(old_password, user.hashed_password):
        password = get_password_hash(new_password)
    return password


# For RESTFULL API
# async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(database.get_db)):
#For template logic
async def get_current_user(token, db: AsyncSession = Depends(database.get_db)):

    bt = await is_token_blacklisted(token, db)
    if bt:
        raise HTTPException(status_code=403, detail="Token is blacklisted")
                            
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



async def is_token_blacklisted(token: str, db: AsyncSession) -> bool: 
    result = await db.execute(select(models.TokenBlacklist))
    blacklisted_tokens = result.scalars().all()
    return token in blacklisted_tokens