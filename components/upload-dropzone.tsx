'use client';

import { useMemo, useRef, useState } from 'react';
import { FileUp, LoaderCircle } from 'lucide-react';

import type { UploadStatus } from '@/types/document';

type UploadDropzoneProps = {
  uploadStatus: UploadStatus;
  uploadProgress: number;
  onUpload: (file: File) => Promise<unknown>;
};

const copyByStatus: Record<UploadStatus, { title: string; detail: string }> = {
  idle: {
    title: 'Drop PDF/DOC/DOCX here',
    detail: 'or click to browse',
  },
  dragging: {
    title: 'Release to Upload',
    detail: 'Files will be sent to the FastAPI backend immediately.',
  },
  uploading: {
    title: 'Uploading...',
    detail: 'The document is being saved and processed.',
  },
  success: {
    title: 'Upload Complete',
    detail: 'The latest backend response has been applied to the workspace.',
  },
  error: {
    title: 'Upload Failed',
    detail: 'Review the error state below before trying again.',
  },
};

export function UploadDropzone({ uploadStatus, uploadProgress, onUpload }: UploadDropzoneProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const effectiveStatus: UploadStatus = isDragging ? 'dragging' : uploadStatus;

  const copy = useMemo(() => copyByStatus[effectiveStatus], [effectiveStatus]);

  const handleFiles = async (files: FileList | null) => {
    const file = files?.[0];
    if (!file) {
      return;
    }
    try {
      await onUpload(file);
    } catch {
      return;
    }
  };

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(event) => {
        event.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(event) => {
        event.preventDefault();
        setIsDragging(false);
        void handleFiles(event.dataTransfer.files);
      }}
      className={`group rounded-panel border border-dashed px-4 py-5 transition ${
        effectiveStatus === 'dragging'
          ? 'border-accent bg-accentSoft/80 shadow-lift'
          : effectiveStatus === 'error'
            ? 'border-danger bg-dangerSoft/60'
            : effectiveStatus === 'success'
              ? 'border-success bg-successSoft/70'
              : 'border-border bg-panel hover:border-accent/55 hover:bg-accentSoft/40'
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        className="hidden"
        onChange={(event) => {
          void handleFiles(event.target.files);
          event.target.value = '';
        }}
      />

      <div className="flex items-start gap-3">
        <div className="mt-1 inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-white/90 text-accent shadow-sm">
          {effectiveStatus === 'uploading' ? (
            <LoaderCircle className="h-5 w-5 animate-spin" />
          ) : (
            <FileUp className="h-5 w-5" />
          )}
        </div>

        <div className="min-w-0 flex-1">
          <div className="text-sm font-semibold text-ink">{copy.title}</div>
          <div className="mt-1 text-sm text-muted">{copy.detail}</div>

          <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/90">
            <div
              className={`h-full rounded-full transition-all ${
                effectiveStatus === 'error'
                  ? 'bg-danger'
                  : effectiveStatus === 'success'
                    ? 'bg-success'
                    : 'bg-accent'
              }`}
              style={{ width: `${effectiveStatus === 'idle' ? 12 : Math.max(uploadProgress, effectiveStatus === 'success' ? 100 : 18)}%` }}
            />
          </div>

          <div className="mt-2 text-xs font-medium uppercase tracking-[0.16em] text-muted">
            Accepted in UI: PDF, DOC, DOCX
          </div>
        </div>
      </div>
    </div>
  );
}
