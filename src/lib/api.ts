import { API_BASE_URL, type ChatHistoryResponse, type ChatRequest, type ChatResponse, type DocumentListResponse, type DocumentUploadResponse, type SummaryRequest, type SummaryResponse } from '../types/api';

export async function listDocuments(): Promise<DocumentListResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/documents/`);
  if (!response.ok) {
    throw new Error('Failed to load documents.');
  }
  return (await response.json()) as DocumentListResponse;
}

export async function uploadDocument(file: File): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/v1/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error((payload && typeof payload.detail === 'string' ? payload.detail : 'Upload failed.') || 'Upload failed.');
  }

  return payload as DocumentUploadResponse;
}

export async function deleteDocument(documentId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/documents/${documentId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Failed to delete document.');
  }
}

export async function generateSummary(payload: SummaryRequest): Promise<SummaryResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/summary/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const payloadResponse = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(
      payloadResponse && typeof payloadResponse.detail === 'string'
        ? payloadResponse.detail
        : 'Summary generation failed.',
    );
  }

  return payloadResponse as SummaryResponse;
}

export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const payloadResponse = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(
      payloadResponse && typeof payloadResponse.detail === 'string'
        ? payloadResponse.detail
        : 'Chat request failed.',
    );
  }

  return payloadResponse as ChatResponse;
}

export async function getConversationHistory(conversationId: string): Promise<ChatHistoryResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/chat/history/${conversationId}`);
  const payloadResponse = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      payloadResponse && typeof payloadResponse.detail === 'string'
        ? payloadResponse.detail
        : 'Unable to load conversation history.',
    );
  }

  return payloadResponse as ChatHistoryResponse;
}
