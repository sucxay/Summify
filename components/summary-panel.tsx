'use client';

import { Copy, LoaderCircle, RotateCcw, Sparkles, Trash2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import type { DocumentListItem } from '@/types/document';
import type { SummaryResponse, SummaryType } from '@/types/summary';

type SummaryPanelProps = {
  documentId: string | null;
  documents: DocumentListItem[];
  summaryType: SummaryType;
  summaryTypeOptions: Array<{ value: SummaryType; label: string }>;
  query: string;
  result: SummaryResponse | null;
  isGenerating: boolean;
  error: string | null;
  copied: boolean;
  onChangeSummaryType: (value: SummaryType) => void;
  onChangeQuery: (value: string) => void;
  onGenerate: () => void;
  onRegenerate: () => void;
  onClear: () => void;
  onCopy: () => void;
};

export function SummaryPanel({
  documentId,
  documents,
  summaryType,
  summaryTypeOptions,
  query,
  result,
  isGenerating,
  error,
  copied,
  onChangeSummaryType,
  onChangeQuery,
  onGenerate,
  onRegenerate,
  onClear,
  onCopy,
}: SummaryPanelProps) {
  const currentDocument = documents.find((item) => item.documentId === documentId) ?? null;

  return (
    <section className="min-h-0 bg-white">
      <div className="border-b border-border/80 px-5 py-5 md:px-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted">Summary</div>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-ink">Current Document</h2>
          </div>
          <div className="rounded-full border border-border bg-panel px-3 py-1.5 text-xs font-medium text-muted">
            {currentDocument?.label ?? 'Select a document'}
          </div>
        </div>
      </div>

      <div className="scrollbar-thin min-h-0 overflow-y-auto px-5 py-5 md:px-6">
        <div className="grid gap-5">
          <section className="rounded-panel border border-border bg-panel/55 p-5">
            <div className="flex flex-wrap gap-2">
              {summaryTypeOptions.map((option) => {
                const active = option.value === summaryType;
                return (
                  <button
                    type="button"
                    key={option.value}
                    onClick={() => onChangeSummaryType(option.value)}
                    className={`rounded-full border px-4 py-2 text-sm font-medium capitalize transition ${
                      active ? 'border-accent bg-accent text-white shadow-lift' : 'border-border bg-white text-ink hover:border-accent/35'
                    }`}
                  >
                    {option.label.replace('_', ' ')}
                  </button>
                );
              })}
            </div>

            <div className="mt-5 grid gap-3">
              <label htmlFor="summary-query" className="text-sm font-semibold text-ink">
                Prompt
              </label>
              <textarea
                id="summary-query"
                value={query}
                onChange={(event) => onChangeQuery(event.target.value)}
                rows={4}
                placeholder="Describe what the summary should focus on."
                className="min-h-[7.5rem] rounded-panel border border-border bg-white px-4 py-3 text-sm leading-6 text-ink outline-none transition focus:border-accent focus:ring-4 focus:ring-accentSoft"
              />
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={onGenerate}
                disabled={!documentId || isGenerating}
                className="inline-flex h-11 items-center gap-2 rounded-xl bg-ink px-4 text-sm font-semibold text-white transition hover:bg-[#0f1727] disabled:cursor-not-allowed disabled:bg-muted"
              >
                {isGenerating ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                {isGenerating ? 'Generating...' : 'Generate Summary'}
              </button>
              <button
                type="button"
                onClick={onClear}
                className="inline-flex h-11 items-center gap-2 rounded-xl border border-border bg-white px-4 text-sm font-semibold text-ink transition hover:border-accent hover:text-accent"
              >
                <Trash2 className="h-4 w-4" />
                Clear Output
              </button>
            </div>

            {error ? (
              <div className="mt-4 rounded-panel border border-danger/20 bg-dangerSoft px-4 py-3 text-sm leading-6 text-danger">
                {error}
              </div>
            ) : null}
          </section>

          <section className="rounded-panel border border-border bg-white">
            <div className="flex items-center justify-between border-b border-border/80 px-5 py-4">
              <div>
                <div className="text-sm font-semibold text-ink">Summary Output</div>
                <div className="mt-1 text-sm text-muted">Markdown from the backend is rendered directly in the workspace.</div>
              </div>

              {result ? (
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={onCopy}
                    className="inline-flex h-10 items-center gap-2 rounded-xl border border-border bg-white px-3 text-sm font-semibold text-ink transition hover:border-accent hover:text-accent"
                  >
                    <Copy className="h-4 w-4" />
                    {copied ? 'Copied' : 'Copy'}
                  </button>
                  <button
                    type="button"
                    onClick={onRegenerate}
                    disabled={isGenerating}
                    className="inline-flex h-10 items-center gap-2 rounded-xl border border-border bg-white px-3 text-sm font-semibold text-ink transition hover:border-accent hover:text-accent disabled:opacity-50"
                  >
                    <RotateCcw className={`h-4 w-4 ${isGenerating ? 'animate-spin' : ''}`} />
                    Regenerate
                  </button>
                </div>
              ) : null}
            </div>

            <div className="min-h-[24rem] px-5 py-5">
              {!documentId ? (
                <div className="rounded-panel border border-dashed border-border bg-panel px-5 py-8 text-sm leading-6 text-muted">
                  Select or upload a document to generate a summary.
                </div>
              ) : isGenerating ? (
                <div className="space-y-4">
                  {[0, 1, 2, 3].map((item) => (
                    <div key={item} className="h-4 animate-pulse rounded-full bg-panel" />
                  ))}
                </div>
              ) : result ? (
                <div>
                  <div className="mb-5 flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-accentSoft px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-accentStrong">
                      {result.summary_type}
                    </span>
                    <span className="rounded-full bg-panel px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-muted">
                      {result.document_id ?? 'All documents'}
                    </span>
                  </div>
                  <article className="prose prose-slate max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.summary}</ReactMarkdown>
                  </article>
                </div>
              ) : (
                <div className="rounded-panel border border-dashed border-border bg-panel px-5 py-8 text-sm leading-6 text-muted">
                  No summary generated yet.
                </div>
              )}
            </div>
          </section>
        </div>
      </div>
    </section>
  );
}
