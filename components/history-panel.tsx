'use client';

import { History, RefreshCcw } from 'lucide-react';

import type { ChatMessage } from '@/types/chat';

type HistoryPanelProps = {
  conversationId: string | null;
  history: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  historyMeta: string;
  onRefresh: () => void;
};

export function HistoryPanel({
  conversationId,
  history,
  isLoading,
  error,
  historyMeta,
  onRefresh,
}: HistoryPanelProps) {
  return (
    <section className="border-t border-border/80 bg-white">
      <div className="flex items-center justify-between border-b border-border/80 px-5 py-4">
        <div>
          <div className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted">History</div>
          <div className="mt-1 text-sm text-ink">{historyMeta}</div>
        </div>
        <button
          type="button"
          onClick={onRefresh}
          disabled={!conversationId || isLoading}
          className="inline-flex h-10 items-center gap-2 rounded-xl border border-border bg-white px-3 text-sm font-semibold text-ink transition hover:border-accent hover:text-accent disabled:opacity-50"
        >
          <RefreshCcw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      <div className="scrollbar-thin h-full overflow-y-auto px-5 py-4">
        {error ? (
          <div className="rounded-panel border border-danger/20 bg-dangerSoft px-4 py-3 text-sm leading-6 text-danger">
            {error}
          </div>
        ) : null}

        {isLoading ? (
          <div className="space-y-3">
            {[0, 1, 2].map((item) => (
              <div key={item} className="h-14 animate-pulse rounded-panel bg-panel" />
            ))}
          </div>
        ) : history.length === 0 ? (
          <div className="rounded-panel border border-dashed border-border bg-panel px-4 py-6 text-sm leading-6 text-muted">
            The backend does not attach timestamps or metadata to history entries. When a conversation exists, this panel renders the raw `history` array from `GET /api/v1/chat/history/{'{conversation_id}'}`.
          </div>
        ) : (
          <div className="space-y-3">
            {history.map((message, index) => (
              <div key={`${message.role}-${index}-${message.content.slice(0, 24)}`} className="rounded-panel border border-border bg-panel/55 px-4 py-3">
                <div className="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[0.18em] text-muted">
                  <History className="h-3.5 w-3.5" />
                  {message.role}
                </div>
                <div className="mt-2 text-sm leading-6 text-ink">{message.content}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
