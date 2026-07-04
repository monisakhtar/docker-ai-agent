import os
import sqlmodel
from sqlmodel import Session, SQLModel

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("`DATABASE_URL` environment variable is not set.")

DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session