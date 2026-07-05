from typing import List

from fastapi import APIRouter, Depends
router = APIRouter()
from sqlmodel import Session, select
from .models import ChatMessage, ChatMessagePayload 
from api.db import get_session
from api.ai.services import generate_email
from api.ai.schemas import EmailMessageSchema

@router.get("/")
def chat_root():
    return {"message": "Welcome to the Chat API!"}

@router.get("/recent", response_model=EmailMessageSchema)
def chat_recent_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results

@router.post("/", response_model=EmailMessageSchema)
def chat_create_message(payload: ChatMessagePayload,
                        session: Session = Depends(get_session)):
    
    data = payload.model_dump()
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)

    response = generate_email(payload.message)
    return response
