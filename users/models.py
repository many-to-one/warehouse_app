from sqlalchemy import Column, Integer, String, Boolean
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


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)



class ProductsList(Base):
    __tablename__ = 'products_list'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ean = Column(String, index=True)
    count = Column(Integer, index=True)


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
        ]  