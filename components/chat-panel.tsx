'use client';

import type { RefObject } from 'react';
import { LoaderCircle, SendHorizontal } from 'lucide-react';

import type { ChatMessage } from '@/types/chat';

type ChatPanelProps = {
  documentId: string | null;
  conversationId: string | null;
  messages: ChatMessage[];
  input: string;
  isSending: boolean;
  error: string | null;
  scrollRef: RefObject<HTMLDivElement>;
  onInputChange: (value: string) => void;
  onSend: () => void;
};

export function ChatPanel({
  documentId,
  conversationId,
  messages,
  input,
  isSending,
  error,
  scrollRef,
  onInputChange,
  onSend,
}: ChatPanelProps) {
  return (
    <section className="flex min-h-0 flex-col">
      <div className="border-b border-border/80 px-5 py-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-[11px] font-semibold uppercase tracking-[0.24em] text-muted">Chat</div>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight text-ink">Ask about this document</h2>
          </div>
          <div className="rounded-full border border-border bg-panel px-3 py-1.5 text-xs font-medium text-muted">
            {conversationId ?? 'New conversation'}
          </div>
        </div>
      </div>

      <div className="flex min-h-0 flex-1 flex-col px-5 py-5">
        <div ref={scrollRef} className="scrollbar-thin min-h-0 flex-1 space-y-3 overflow-y-auto rounded-panel border border-border bg-panel/55 p-4">
          {!documentId ? (
            <div className="rounded-panel border border-dashed border-border bg-white px-5 py-6 text-sm leading-6 text-muted">
              Choose a document before starting chat.
            </div>
          ) : messages.length === 0 ? (
            <div className="rounded-panel border border-dashed border-border bg-white px-5 py-6 text-sm leading-6 text-muted">
              Ask a question about the selected document to create a conversation.
            </div>
          ) : (
            messages.map((message, index) => {
              const isUser = message.role === 'user';
              return (
                <div
                  key={`${message.role}-${index}-${message.content.slice(0, 24)}`}
                  className={`max-w-[90%] rounded-[1.1rem] px-4 py-3 text-sm leading-6 ${
                    isUser ? 'ml-auto bg-ink text-white' : 'border border-border bg-white text-ink'
                  }`}
                >
                  {message.content}
                </div>
              );
            })
          )}

          {isSending ? (
            <div className="inline-flex items-center gap-2 rounded-[1.1rem] border border-border bg-white px-4 py-3 text-sm text-muted">
              <LoaderCircle className="h-4 w-4 animate-spin" />
              Waiting for the backend...
            </div>
          ) : null}
        </div>

        {error ? (
          <div className="mt-4 rounded-panel border border-danger/20 bg-dangerSoft px-4 py-3 text-sm leading-6 text-danger">
            {error}
          </div>
        ) : null}

        <div className="mt-4 grid gap-3">
          <label htmlFor="chat-input" className="text-sm font-semibold text-ink">
            Message
          </label>
          <div className="flex gap-3">
            <textarea
              id="chat-input"
              value={input}
              onChange={(event) => onInputChange(event.target.value)}
              rows={4}
              placeholder="Ask a question grounded in the selected document."
              className="min-h-[7rem] flex-1 rounded-panel border border-border bg-white px-4 py-3 text-sm leading-6 text-ink outline-none transition focus:border-accent focus:ring-4 focus:ring-accentSoft"
            />
            <button
              type="button"
              onClick={onSend}
              disabled={isSending || !documentId}
              className="inline-flex h-12 w-12 shrink-0 items-center justify-center self-end rounded-xl bg-accent text-white transition hover:bg-accentStrong disabled:cursor-not-allowed disabled:bg-muted"
              aria-label="Send chat message"
            >
              <SendHorizontal className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
