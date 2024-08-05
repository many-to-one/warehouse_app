from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.future import select
from database.database import get_db
from users import auth
from warehouse.pr_schemas import *
# from warehouse.pr_models import *
from warehouse import pr_crud, pr_schemas
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


@router.post("/edit_product/{id}", response_model=ProductBase)
async def edit_product(
        request: ProductEditForm, 
        id: int,
        db: AsyncSession = Depends(get_db),
        user: UserBase = Depends(auth.get_current_user),
    ):

    product = await pr_crud.get_product(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    print('################ product ################',product)
    if  user.is_admin:
        if request.title is not None:
            product.title = request.title
        if request.ean is not None:
            print('################ request.ean ################', request.ean)
            product.ean = request.ean
        if request.count is not None:
            product.count = request.count
        db.add(product)
        await db.commit()  
        await db.refresh(product)

        return product
        
    else:
        raise HTTPException(status_code=400, detail="Permission deny")
    

@router.post("/delete_product/{id}")
async def edit_product(
        id: int,
        db: AsyncSession = Depends(get_db),
        user: UserBase = Depends(auth.get_current_user),
    ):
        product = await pr_crud.get_product(db=db, id=id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if  user.is_admin:
            await db.delete(product)
            await db.commit()
            await db.flush()
            return {"message": "The product is deleted successfully!"}
        else:
            raise HTTPException(status_code=400, detail="Permission deny")