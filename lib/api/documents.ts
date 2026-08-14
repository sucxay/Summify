import { requestJson, uploadMultipart } from '@/lib/api/client';
import type {
  DeleteDocumentResponse,
  DocumentListResponse,
  DocumentUploadResponse,
} from '@/types/document';

export function listDocuments(): Promise<DocumentListResponse> {
  return requestJson<DocumentListResponse>('/api/v1/documents/');
}

export function uploadDocument(
  file: File,
  onProgress?: (progress: number) => void,
): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  return uploadMultipart<DocumentUploadResponse>('/api/v1/documents/upload', formData, onProgress);
}

export function deleteDocument(documentId: string): Promise<DeleteDocumentResponse> {
  return requestJson<DeleteDocumentResponse>(`/api/v1/documents/${documentId}`, {
    method: 'DELETE',
  });
}
