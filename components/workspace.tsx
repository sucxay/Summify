'use client';

import { useEffect, useState } from 'react';
import { Menu } from 'lucide-react';

import { ChatPanel } from '@/components/chat-panel';
import { DocumentSidebar } from '@/components/document-sidebar';
import { HistoryPanel } from '@/components/history-panel';
import { SummaryPanel } from '@/components/summary-panel';
import { useChat } from '@/hooks/use-chat';
import { useDocuments } from '@/hooks/use-documents';
import { useSummary } from '@/hooks/use-summary';

export function Workspace() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const documents = useDocuments();
  const summary = useSummary();
  const chat = useChat(documents.selectedDocumentId);
  const refreshDocuments = documents.refreshDocuments;

  useEffect(() => {
    void refreshDocuments();
  }, [refreshDocuments]);

  return (
    <main className="min-h-screen p-3 md:p-5">
      <div className="mx-auto flex min-h-[calc(100vh-1.5rem)] max-w-[1600px] overflow-hidden rounded-[1.75rem] border border-white/70 bg-white/85 shadow-soft backdrop-blur md:min-h-[calc(100vh-2.5rem)]">
        <DocumentSidebar
          documents={documents.documents}
          selectedDocumentId={documents.selectedDocumentId}
          onSelectDocument={(documentId) => {
            documents.setSelectedDocumentId(documentId);
            setIsSidebarOpen(false);
          }}
          onRefresh={() => void documents.refreshDocuments(true)}
          onUpload={documents.uploadDocument}
          onDelete={(documentId) => void documents.deleteDocument(documentId)}
          error={documents.error}
          isLoading={documents.isLoading}
          isRefreshing={documents.isRefreshing}
          isDeleting={documents.isDeleting}
          uploadStatus={documents.uploadStatus}
          uploadProgress={documents.uploadProgress}
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
        />

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex items-center justify-between border-b border-border/80 px-4 py-4 md:px-6 lg:hidden">
            <button
              type="button"
              onClick={() => setIsSidebarOpen(true)}
              className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-white text-ink transition hover:border-accent hover:text-accent"
              aria-label="Open document sidebar"
            >
              <Menu className="h-4 w-4" />
            </button>
            <div className="text-right">
              <div className="text-[11px] font-semibold uppercase tracking-[0.22em] text-muted">Current Document</div>
              <div className="max-w-[12rem] truncate text-sm font-medium text-ink">
                {documents.selectedDocumentId ?? 'No document selected'}
              </div>
            </div>
          </header>

          <div className="panel-grid min-h-0 flex-1">
            <SummaryPanel
              documentId={documents.selectedDocumentId}
              documents={documents.documents}
              summaryType={summary.summaryType}
              summaryTypeOptions={summary.summaryTypeOptions}
              query={summary.query}
              result={summary.result}
              isGenerating={summary.isGenerating}
              error={summary.error}
              copied={summary.copied}
              onChangeSummaryType={summary.changeSummaryType}
              onChangeQuery={summary.setQuery}
              onGenerate={() => void summary.generateSummary(documents.selectedDocumentId)}
              onRegenerate={() => void summary.generateSummary(documents.selectedDocumentId)}
              onClear={summary.clearSummary}
              onCopy={() => void summary.copySummary()}
            />

            <div className="grid min-h-0 grid-rows-[minmax(0,1fr)_minmax(18rem,0.8fr)] border-t border-border/70 md:border-l md:border-t-0">
              <ChatPanel
                documentId={documents.selectedDocumentId}
                conversationId={chat.conversationId}
                messages={chat.messages}
                input={chat.input}
                isSending={chat.isSending}
                error={chat.error}
                scrollRef={chat.scrollRef}
                onInputChange={chat.setInput}
                onSend={() => void chat.sendMessage()}
              />

              <HistoryPanel
                conversationId={chat.conversationId}
                history={chat.history}
                isLoading={chat.isLoadingHistory}
                error={chat.error}
                historyMeta={chat.historyMeta}
                onRefresh={() => void chat.loadHistory()}
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
