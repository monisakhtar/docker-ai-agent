from typing import List

from fastapi import APIRouter, Depends
router = APIRouter()
from sqlmodel import Session, select
from .models import ChatMessage, ChatMessagePayload, ChatMessageResponse
from api.db import get_session

@router.get("/")
def chat_root():
    return {"message": "Welcome to the Chat API!"}

@router.get("/recent", response_model=List[ChatMessageResponse])
def chat_recent_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results

@router.post("/", response_model=ChatMessage)
def chat_create_message(payload: ChatMessagePayload,
                        session: Session = Depends(get_session)):
    data = payload.model_dump()
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
