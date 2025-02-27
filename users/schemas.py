from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_active: bool
    created_at: datetime

class UserLoginForm(BaseModel):
    username: str
    password: str


class UserCreateForm(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserEditForm(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None



class UserDisplay(BaseModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserLogOut(BaseModel):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ChangePassword(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
