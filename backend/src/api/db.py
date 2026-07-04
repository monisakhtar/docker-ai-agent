import os
import sqlmodel
from sqlmodel import Session, SQLModel

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("`DATABASE_URL` environment variable is not set.")

# FIX: Only modify the URL if it doesn't already have the +psycopg driver specified
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session