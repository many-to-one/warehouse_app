from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    id: int
    title: str
    ean: str
    count: int
    created_at: datetime
    edited_at: datetime


class ProductCreateForm(BaseModel):
    title: str
    ean: str
    count: int


class ProductEditForm(BaseModel):
    title: Optional[str] = None
    ean: Optional[str] = None
    count: Optional[int] = None