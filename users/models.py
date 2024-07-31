from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.database import Base
from sqladmin import ModelView

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]  # Columns to display in the list view
    form_columns = [User.username, User.email, User.hashed_password]  # Columns to display in the form view