'use client';

import { RefreshCcw, Trash2, X } from 'lucide-react';

import { UploadDropzone } from '@/components/upload-dropzone';
import type { DocumentListItem, UploadStatus } from '@/types/document';

type DocumentSidebarProps = {
  documents: DocumentListItem[];
  selectedDocumentId: string | null;
  onSelectDocument: (documentId: string) => void;
  onRefresh: () => void;
  onUpload: (file: File) => Promise<unknown>;
  onDelete: (documentId: string) => void;
  error: string | null;
  isLoading: boolean;
  isRefreshing: boolean;
  isDeleting: string | null;
  uploadStatus: UploadStatus;
  uploadProgress: number;
  isOpen: boolean;
  onClose: () => void;
};

function renderSourceBadge(source: DocumentListItem['source']) {
  return source === 'backend-list' ? 'Indexed' : 'Recent Upload';
}

export function DocumentSidebar({
  documents,
  selectedDocumentId,
  onSelectDocument,
  onRefresh,
  onUpload,
  onDelete,
  error,
  isLoading,
  isRefreshing,
  isDeleting,
  uploadStatus,
  uploadProgress,
  isOpen,
  onClose,
}: DocumentSidebarProps) {
  return (
    <>
      <div
        className={`fixed inset-0 z-30 bg-ink/35 transition md:hidden ${isOpen ? 'pointer-events-auto opacity-100' : 'pointer-events-none opacity-0'}`}
        onClick={onClose}
      />

      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-[min(86vw,var(--sidebar-width))] flex-col border-r border-border bg-white transition-transform duration-200 md:static md:w-[var(--sidebar-width)] ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        <div className="flex items-center justify-between border-b border-border/80 px-5 py-5">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted">Workspace</div>
            <h1 className="mt-2 text-2xl font-semibold tracking-tight text-ink">SUMMIFY</h1>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border text-muted md:hidden"
            aria-label="Close document sidebar"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="border-b border-border/80 px-4 py-4">
          <UploadDropzone uploadStatus={uploadStatus} uploadProgress={uploadProgress} onUpload={onUpload} />
          <div className="mt-3 text-xs leading-5 text-muted">
            The backend routes expose PDF, DOC, and DOCX upload entry points. Current ingestion succeeds reliably for PDF.
          </div>
        </div>

        <div className="flex items-center justify-between border-b border-border/80 px-5 py-4">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-muted">Documents</div>
            <div className="mt-1 text-sm text-ink">{documents.length} visible in this session</div>
          </div>
          <button
            type="button"
            onClick={onRefresh}
            disabled={isRefreshing}
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-white text-muted transition hover:border-accent hover:text-accent disabled:opacity-50"
            aria-label="Refresh documents"
          >
            <RefreshCcw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>
        </div>

        <div className="scrollbar-thin flex-1 overflow-y-auto px-3 py-3">
          {isLoading ? (
            <div className="space-y-3 px-2">
              {[0, 1, 2, 3].map((item) => (
                <div key={item} className="h-20 animate-pulse rounded-panel bg-panel" />
              ))}
            </div>
          ) : documents.length === 0 ? (
            <div className="rounded-panel border border-dashed border-border bg-panel px-4 py-5 text-sm leading-6 text-muted">
              No documents are visible from `GET /api/v1/documents/` yet. New uploads will still use the real `document_id` returned by the backend.
            </div>
          ) : (
            <div className="space-y-2">
              {documents.map((document) => {
                const isActive = document.documentId === selectedDocumentId;
                return (
                  <div
                    key={document.documentId}
                    className={`w-full rounded-panel border px-4 py-4 text-left transition ${
                      isActive ? 'border-accent bg-accentSoft/80 shadow-lift' : 'border-border bg-white hover:border-accent/40 hover:bg-panel'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <button
                          type="button"
                          onClick={() => onSelectDocument(document.documentId)}
                          className="w-full text-left"
                        >
                          <div className="truncate text-sm font-semibold text-ink">{document.label}</div>
                          <div className="mt-1 truncate text-xs text-muted">{document.documentId}</div>
                        </button>
                      </div>
                      <button
                        type="button"
                        onClick={() => onDelete(document.documentId)}
                        disabled={isDeleting === document.documentId}
                        className="inline-flex h-9 w-9 items-center justify-center rounded-xl border border-border bg-white text-muted transition hover:border-danger hover:text-danger disabled:opacity-50"
                        aria-label={`Delete document ${document.documentId}`}
                      >
                        <Trash2 className={`h-4 w-4 ${isDeleting === document.documentId ? 'animate-pulse' : ''}`} />
                      </button>
                    </div>

                    <div className="mt-3 flex items-center gap-2">
                      <span className="rounded-full bg-white/90 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted">
                        {renderSourceBadge(document.source)}
                      </span>
                      {typeof document.metadata?.page_count === 'number' ? (
                        <span className="rounded-full bg-white/90 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted">
                          {document.metadata.page_count} pages
                        </span>
                      ) : null}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {error ? (
          <div className="border-t border-border/80 px-4 py-4">
            <div className="rounded-panel border border-danger/20 bg-dangerSoft px-4 py-3 text-sm leading-6 text-danger">
              {error}
            </div>
          </div>
        ) : null}
      </aside>
    </>
  );
}
