"""
Chat Service - Conversational interface with document context.
"""
from typing import Optional, List, Dict, Any
import logging

from app.rag.pipeline import RAGPipeline

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline
        self._conversations: Dict[str, List[Dict[str, str]]] = {}

    def send_message(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        document_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        if conversation_id and conversation_id in self._conversations:
            history = self._conversations[conversation_id]
        else:
            history = []

        result = self.rag_pipeline.chat(
            message=message,
            document_id=document_id,
        )

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": result["summary"]})

        if not conversation_id:
            import uuid
            conversation_id = str(uuid.uuid4())

        self._conversations[conversation_id] = history

        return {
            "conversation_id": conversation_id,
            "message": result["summary"],
            "document_id": document_id,
        }

    def get_conversation_history(
        self, conversation_id: str
    ) -> List[Dict[str, str]]:
        return self._conversations.get(conversation_id, [])

    def delete_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False