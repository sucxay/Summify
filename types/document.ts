export type UploadStatus = 'idle' | 'dragging' | 'uploading' | 'success' | 'error';

export type DocumentMetadata = {
  title?: string;
  author?: string;
  subject?: string;
  keywords?: string;
  creator?: string;
  page_count?: number;
  total_words?: number;
  file_size_mb?: number;
  source_path?: string;
  file_name?: string;
  document_id?: string;
  chunk_count?: number;
  [key: string]: unknown;
};

export type DocumentUploadResponse = {
  document_id: string;
  metadata: DocumentMetadata;
  chunk_count: number;
  status: string;
};

export type DocumentListResponse = {
  documents: string[];
  total: number;
};

export type DocumentListItem = {
  documentId: string;
  label: string;
  source: 'backend-list' | 'upload-response';
  metadata?: DocumentMetadata;
};

export type DeleteDocumentResponse = {
  status: string;
  document_id: string;
};
