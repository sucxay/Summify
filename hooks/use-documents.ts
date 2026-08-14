'use client';

import { useCallback, useMemo, useState } from 'react';

import { ApiError } from '@/lib/api/client';
import * as documentsApi from '@/lib/api/documents';
import type {
  DocumentListItem,
  DocumentMetadata,
  DocumentUploadResponse,
  UploadStatus,
} from '@/types/document';

const SUPPORTED_EXTENSIONS = ['pdf', 'doc', 'docx'];
const WORKING_EXTENSIONS = ['pdf'];

function getDocumentLabel(documentId: string, metadata?: DocumentMetadata): string {
  if (typeof metadata?.file_name === 'string' && metadata.file_name.trim()) {
    return metadata.file_name;
  }
  return documentId;
}

function mergeDocuments(
  listedIds: string[],
  uploadedDocuments: Record<string, DocumentUploadResponse>,
): DocumentListItem[] {
  const items: DocumentListItem[] = listedIds.map((documentId) => ({
    documentId,
    label: getDocumentLabel(documentId, uploadedDocuments[documentId]?.metadata),
    source: 'backend-list',
    metadata: uploadedDocuments[documentId]?.metadata,
  }));

  for (const [documentId, uploaded] of Object.entries(uploadedDocuments)) {
    if (listedIds.includes(documentId)) {
      continue;
    }

    items.unshift({
      documentId,
      label: getDocumentLabel(documentId, uploaded.metadata),
      source: 'upload-response',
      metadata: uploaded.metadata,
    });
  }

  return items;
}

export function useDocuments() {
  const [documentIds, setDocumentIds] = useState<string[]>([]);
  const [uploadedDocuments, setUploadedDocuments] = useState<Record<string, DocumentUploadResponse>>({});
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isDeleting, setIsDeleting] = useState<string | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const documents = useMemo(
    () => mergeDocuments(documentIds, uploadedDocuments),
    [documentIds, uploadedDocuments],
  );

  const refreshDocuments = useCallback(async (isManualRefresh = false) => {
    setError(null);
    if (isManualRefresh) {
      setIsRefreshing(true);
    } else {
      setIsLoading(true);
    }

    try {
      const response = await documentsApi.listDocuments();
      setDocumentIds(Array.isArray(response.documents) ? response.documents : []);
      setSelectedDocumentId((current) => {
        if (current && response.documents.includes(current)) {
          return current;
        }
        return current ?? response.documents[0] ?? null;
      });
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Unable to load documents.';
      setError(message);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  const uploadDocument = useCallback(async (file: File) => {
    const extension = file.name.split('.').pop()?.toLowerCase() ?? '';

    if (!SUPPORTED_EXTENSIONS.includes(extension)) {
      const allowed = SUPPORTED_EXTENSIONS.map((item) => item.toUpperCase()).join(', ');
      setUploadStatus('error');
      setError(`Unsupported file type. Allowed file types: ${allowed}.`);
      throw new ApiError('Unsupported file type.', 400);
    }

    if (!WORKING_EXTENSIONS.includes(extension)) {
      setUploadStatus('error');
      const message = 'This backend currently processes PDF documents only. DOC and DOCX uploads are not wired through ingestion yet.';
      setError(message);
      throw new ApiError(message, 400, null, 'unsupported_by_backend');
    }

    setUploadStatus('uploading');
    setUploadProgress(0);
    setError(null);

    try {
      const response = await documentsApi.uploadDocument(file, setUploadProgress);
      setUploadedDocuments((current) => ({
        ...current,
        [response.document_id]: response,
      }));
      setDocumentIds((current) => (current.includes(response.document_id) ? current : [response.document_id, ...current]));
      setSelectedDocumentId(response.document_id);
      setUploadStatus('success');
      await refreshDocuments(true);
      return response;
    } catch (cause) {
      setUploadStatus('error');
      const message = cause instanceof Error ? cause.message : 'Upload failed.';
      setError(message);
      throw cause;
    }
  }, [refreshDocuments]);

  const deleteDocument = useCallback(async (documentId: string) => {
    setIsDeleting(documentId);
    setError(null);

    try {
      await documentsApi.deleteDocument(documentId);
      setDocumentIds((current) => current.filter((item) => item !== documentId));
      setUploadedDocuments((current) => {
        const next = { ...current };
        delete next[documentId];
        return next;
      });
      setSelectedDocumentId((current) => (current === documentId ? null : current));
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Unable to delete document.';
      setError(message);
      throw cause;
    } finally {
      setIsDeleting(null);
    }
  }, []);

  return {
    documents,
    selectedDocumentId,
    setSelectedDocumentId,
    isLoading,
    isRefreshing,
    isDeleting,
    uploadStatus,
    uploadProgress,
    error,
    setError,
    refreshDocuments,
    uploadDocument,
    deleteDocument,
  };
}
