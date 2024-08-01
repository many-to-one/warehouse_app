from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.future import select
from database.database import get_db
from users import auth
from warehouse.pr_schemas import *
# from warehouse.pr_models import *
from warehouse import pr_crud
from users.schemas import UserBase
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
        prefix="/products", 
        tags=["products"]
    )


@router.post("/create_product", response_model=ProductBase)
async def create_product(
        product_form: ProductCreateForm = Depends(ProductCreateForm), 
        db: AsyncSession = Depends(get_db),
        user: UserBase = Depends(auth.get_current_user),
    ):

    print('################ user ################', user.is_admin)
    if  user.is_admin:
        return await pr_crud.create_product(db=db, product_form=product_form)
    else:
        raise HTTPException(status_code=400, detail="Permission deny")


@router.get("/all_products", response_model=List[ProductBase])
async def all_products(
        db: AsyncSession = Depends(get_db),
        user: UserBase = Depends(auth.get_current_user),
    ):
    # print('################ user ################', user.is_admin)
    return await pr_crud.all_products(db=db)
    