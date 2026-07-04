from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.db import init_db
from api.chat.routing import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    init_db()
    yield

app= FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats", tags=["chat"])

@app.get("/")
def read_root():
    return {"Hello": "World FastAPI"}