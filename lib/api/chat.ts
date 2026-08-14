import { requestJson } from '@/lib/api/client';
import type {
  ChatHistoryResponse,
  ChatRequest,
  ChatResponse,
  DeleteConversationResponse,
} from '@/types/chat';

export function sendMessage(payload: ChatRequest): Promise<ChatResponse> {
  return requestJson<ChatResponse>('/api/v1/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
}

export function getConversationHistory(conversationId: string): Promise<ChatHistoryResponse> {
  return requestJson<ChatHistoryResponse>(`/api/v1/chat/history/${conversationId}`);
}

export function deleteConversation(conversationId: string): Promise<DeleteConversationResponse> {
  return requestJson<DeleteConversationResponse>(`/api/v1/chat/${conversationId}`, {
    method: 'DELETE',
  });
}
