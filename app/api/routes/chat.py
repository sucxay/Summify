"""
Chat endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_chat_service
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    document_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    document_id: Optional[str]


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    result = chat_service.send_message(
        message=request.message,
        conversation_id=request.conversation_id,
        document_id=request.document_id,
    )
    return result


@router.get("/history/{conversation_id}")
async def get_history(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service),
):
    history = chat_service.get_conversation_history(conversation_id)
    return {"conversation_id": conversation_id, "history": history}


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service),
):
    success = chat_service.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted", "conversation_id": conversation_id}