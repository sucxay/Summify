export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000';

export type SummaryType = 'general' | 'executive' | 'bullet_points' | 'key_findings' | 'action_items';

export type DocumentUploadResponse = {
  document_id: string;
  metadata: Record<string, unknown>;
  chunk_count: number;
  status: string;
};

export type DocumentListResponse = {
  documents: string[];
  total: number;
};

export type SummaryRequest = {
  query: string;
  document_id?: string | null;
  summary_type: SummaryType;
  top_k: number;
};

export type SummaryResponse = {
  query: string;
  summary: string;
  document_id?: string | null;
  summary_type: SummaryType;
};

export type ChatRequest = {
  message: string;
  conversation_id?: string | null;
  document_id?: string | null;
};

export type ChatResponse = {
  conversation_id: string;
  message: string;
  document_id?: string | null;
};

export type ChatMessage = {
  role: 'user' | 'assistant';
  content: string;
};

export type ChatHistoryResponse = {
  conversation_id: string;
  history: ChatMessage[];
};
