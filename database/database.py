# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
 
# SQLALCHEMY_DATABASE_URL = "sqlite:///./warehouse.db"
 
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# Base = declarative_base()

# def get_db():

#     db = SessionLocal()
#     try:
#        yield db
#     finally:
#         db.close()

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./async_warehouse.db"

Base = declarative_base()

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session


# POSTGRESQL EXAMPLE
# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv

# Base = declarative_base()
# load_dotenv()

# DB_USER= "your database user"
# DB_PASSWORD= "your database password"
# DB_HOST= "your database host"
# DB_PORT= "your database port"
# DB_NAME= "your database name"

# class AsyncDatabaseSession:
#     def __init__(self):
#         self._session = None
#         self._engine = None
#     def __getattr__(self, name):
#             return getattr(self._session, name)
#     def init(self):
#             self._engine = create_async_engine(
#                 f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
#                 future=True,
#                 echo=True,
#             )
#             self._session = sessionmaker(
#                 self._engine, expire_on_commit=False, class_=AsyncSession
#             )()
#     async def create_all(self):
#         self._engine.begin

# db=AsyncDatabaseSession()

# database = create_engine(Config.SYNC_DB_CONFIG,echo=True)


# postgress from chatgpt:
# import os
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from dotenv import load_dotenv

# Base = declarative_base()
# load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# class AsyncDatabaseSession:
#     def __init__(self):
#         self._session = None
#         self._engine = None

#     def __getattr__(self, name):
#         return getattr(self._session, name)

#     def init(self):
#         self._engine = create_async_engine(
#             f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
#             future=True,
#             echo=True,
#         )
#         self._session = sessionmaker(
#             self._engine, expire_on_commit=False, class_=AsyncSession
#         )

#     async def get_session(self) -> AsyncSession:
#         async with self._session() as session:
#             yield session

#     async def create_all(self):
#         async with self._engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)

# db = AsyncDatabaseSession()
# db.init()

# # You can call this method to create all tables
# # await db.create_all()
