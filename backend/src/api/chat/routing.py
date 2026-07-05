from email import message
from typing import List

from fastapi import APIRouter, Depends, HTTPException
router = APIRouter()
from sqlmodel import Session, select
from .models import ChatMessage, ChatMessagePayload 
from api.db import get_session
from api.ai.services import generate_email
from api.ai.schemas import EmailMessageSchema, SupervisorMessageSchema
from api.ai.agents import get_supervisor

@router.get("/")
def chat_root():
    return {"message": "Welcome to the Chat API!"}

@router.get("/recent", response_model=EmailMessageSchema)
def chat_recent_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results

@router.post("/", response_model=SupervisorMessageSchema)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session)
    ):
    data = payload.model_dump() # pydantic -> dict
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()

    supe = get_supervisor()
    msg_data = {
        "messages": [
            {"role": "user",
            "content": f"{payload.message}" 
          },
        ]
    }
    result = supe.invoke(msg_data, {"configurable": {"thread_id": thread_id}})
    if not result:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    messages = result.get("messages")
    if not messages:
        raise HTTPException(status_code=400, detail="Error with supervisor")
    return messages[-1]