export type ChatRequest = {
  message: string;
  conversation_id?: string | null;
  document_id?: string | null;
};

export type ChatResponse = {
  conversation_id: string;
  message: string;
  document_id: string | null;
};

export type ChatMessage = {
  role: string;
  content: string;
};

export type ChatHistoryResponse = {
  conversation_id: string;
  history: ChatMessage[];
};

export type DeleteConversationResponse = {
  status: string;
  conversation_id: string;
};
