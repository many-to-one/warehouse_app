from pydantic import BaseModel, EmailStr
from typing import Optional

class ProductBase(BaseModel):
    id: int
    title: str
    ean: str
    count: int


class ProductCreateForm(BaseModel):
    title: str
    ean: str
    count: int