from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from database.database import Base
from sqladmin import ModelView

# from warehouse.pr_models import Product

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    edited_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)



class ProductsList(Base):
    __tablename__ = 'products_list'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ean = Column(String, index=True)
    count = Column(Integer, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    edited_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserAdmin(ModelView, model=User):
    column_list = [
            User.id, 
            User.username, 
            User.email,
            User.is_active,
            User.is_admin,
        ]  
    form_columns = [
            User.id,
            User.username, 
            User.email, 
            User.is_active,
            User.is_admin,
            User.created_at,
            User.edited_at,
        ]  
    

class TokenBlacklistAdmin(ModelView, model=TokenBlacklist):
    column_list = [
        TokenBlacklist.id,
    ]  
    form_columns = [
        TokenBlacklist.id,
        TokenBlacklist.token,
    ]  


class ProductAdmin(ModelView, model=ProductsList):
    column_list = [
            ProductsList.id, 
            ProductsList.title, 
            ProductsList.ean,
            ProductsList.count,
        ]  
    form_columns = [
            ProductsList.id, 
            ProductsList.title, 
            ProductsList.ean,
            ProductsList.count,
            ProductsList.created_at,
            ProductsList.edited_at,
        ]  