from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .pr_schemas import *
from .pr_crud import *
from .pr_models import *
from users.models import ProductsList
from sqlalchemy.future import select


async def create_product(
            db: AsyncSession, 
            product_form: ProductCreateForm,
        ):

    new_product = ProductsList(
        title=product_form.title, 
        ean=product_form.ean, 
        count=product_form.count
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def all_products(db: AsyncSession):

    result = await db.execute(select(ProductsList))
    products = result.scalars().all()

    if products is None:
        raise HTTPException(status_code=404, detail="No products")
    
    return products