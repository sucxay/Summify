import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  deleteDocument,
  generateSummary,
  getConversationHistory,
  listDocuments,
  sendChatMessage,
  uploadDocument,
} from './lib/api';
import type {
  ChatHistoryResponse,
  ChatMessage,
  ChatRequest,
  ChatResponse,
  DocumentUploadResponse,
  SummaryRequest,
  SummaryResponse,
  SummaryType,
} from './types/api';

const summaryTypeOptions: Array<{ value: SummaryType; label: string }> = [
  { value: 'general', label: 'General' },
  { value: 'executive', label: 'Executive' },
  { value: 'bullet_points', label: 'Bullet Points' },
  { value: 'key_findings', label: 'Key Findings' },
  { value: 'action_items', label: 'Action Items' },
];

const defaultSummaryQuery = (type: SummaryType) => {
  const map: Record<SummaryType, string> = {
    general: 'Summarize this document in a concise and complete way.',
    executive: 'Provide an executive summary of this document.',
    bullet_points: 'Extract all the key points from this document as bullet points.',
    key_findings: 'What are the key findings and conclusions in this document?',
    action_items: 'Extract the action items and next steps from this document.',
  };

  return map[type];
};

export default function App() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(null);
  const [isLoadingDocuments, setIsLoadingDocuments] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [dragging, setDragging] = useState(false);
  const [summaryType, setSummaryType] = useState<SummaryType>('executive');
  const [summaryQuery, setSummaryQuery] = useState(defaultSummaryQuery('executive'));
  const [summaryResult, setSummaryResult] = useState<SummaryResponse | null>(null);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [chatInput, setChatInput] = useState('');
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [chatError, setChatError] = useState<string | null>(null);
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const loadDocuments = useCallback(async () => {
    setIsLoadingDocuments(true);
    try {
      const data = await listDocuments();
      setDocuments(data.documents || []);
      if (!selectedDocumentId && (data.documents || []).length > 0) {
        setSelectedDocumentId(data.documents[0]);
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to load documents.';
      setUploadError(message);
    } finally {
      setIsLoadingDocuments(false);
    }
  }, [selectedDocumentId]);

  useEffect(() => {
    void loadDocuments();
  }, [loadDocuments]);

  useEffect(() => {
    if (selectedDocumentId) {
      setSummaryQuery((value) => value || defaultSummaryQuery(summaryType));
      setChatError(null);
      setSummaryError(null);
    }
  }, [selectedDocumentId, summaryType]);

  const selectedDocument = useMemo(() => (selectedDocumentId ? selectedDocumentId : null), [selectedDocumentId]);

  const handleDocumentSelection = (documentId: string) => {
    setSelectedDocumentId(documentId);
    setIsSidebarOpen(false);
    setChatError(null);
    setSummaryError(null);
  };

  const validateFile = (file: File) => {
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ];
    const isAllowedMime = allowedTypes.includes(file.type);
    const isAllowedExt = /\.(pdf|doc|docx)$/i.test(file.name);
    if (!isAllowedMime && !isAllowedExt) {
      throw new Error('Only PDF, DOC, or DOCX files are supported.');
    }
  };

  const handleUploadFile = async (file: File) => {
    validateFile(file);
    setIsUploading(true);
    setUploadError(null);

    try {
      const response: DocumentUploadResponse = await uploadDocument(file);
      setDocuments((current) => {
        if (current.includes(response.document_id)) return current;
        return [response.document_id, ...current];
      });
      setSelectedDocumentId(response.document_id);
      setSummaryResult(null);
      setChatMessages([]);
      setConversationId(null);
      setHistory([]);
      setSummaryQuery(defaultSummaryQuery(summaryType));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Upload failed.';
      setUploadError(message);
    } finally {
      setIsUploading(false);
    }
  };

  const onInputFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      await handleUploadFile(file);
    }
    event.target.value = '';
  };

  const onDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files?.[0];
    if (file) {
      await handleUploadFile(file);
    }
  };

  const handleGenerateSummary = async () => {
    if (!selectedDocumentId) {
      setSummaryError('Select a document before generating a summary.');
      return;
    }

    const query = summaryQuery.trim() || defaultSummaryQuery(summaryType);

    setIsGeneratingSummary(true);
    setSummaryError(null);

    try {
      const payload: SummaryRequest = {
        query,
        document_id: selectedDocumentId,
        summary_type: summaryType,
        top_k: 5,
      };
      const response = await generateSummary(payload);
      setSummaryResult(response);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Summary generation failed.';
      setSummaryError(message);
    } finally {
      setIsGeneratingSummary(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      const nextDocuments = documents.filter((item) => item !== documentId);
      setDocuments(nextDocuments);
      if (selectedDocumentId === documentId) {
        setSelectedDocumentId(nextDocuments[0] ?? null);
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to delete the selected document.';
      setUploadError(message);
    }
  };

  const fetchHistory = useCallback(async (id: string) => {
    setIsLoadingHistory(true);
    try {
      const response: ChatHistoryResponse = await getConversationHistory(id);
      setHistory(response.history || []);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to load conversation history.';
      setChatError(message);
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  const handleSendMessage = async () => {
    const trimmed = chatInput.trim();
    if (!trimmed || !selectedDocumentId) {
      if (!trimmed) setChatError('Message cannot be empty.');
      if (!selectedDocumentId) setChatError('Select a document before chatting.');
      return;
    }

    setIsSendingMessage(true);
    setChatError(null);

    try {
      const payload: ChatRequest = {
        message: trimmed,
        conversation_id: conversationId ?? undefined,
        document_id: selectedDocumentId,
      };
      const response: ChatResponse = await sendChatMessage(payload);
      const nextMessages: ChatMessage[] = [
        ...chatMessages,
        { role: 'user', content: trimmed },
        { role: 'assistant', content: response.message },
      ];
      setChatMessages(nextMessages);
      setConversationId(response.conversation_id);
      setHistory(nextMessages);
      setChatInput('');
      await fetchHistory(response.conversation_id);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Chat message failed.';
      setChatError(message);
    } finally {
      setIsSendingMessage(false);
    }
  };

  const handleCopySummary = async () => {
    if (!summaryResult?.summary) return;
    try {
      await navigator.clipboard.writeText(summaryResult.summary);
    } catch {
      setSummaryError('Unable to copy the summary to the clipboard.');
    }
  };

  return (
    <main style={styles.page}>
      <div style={styles.shell}>
        <aside style={{ ...styles.sidebar, transform: isSidebarOpen ? 'translateX(0)' : 'translateX(-110%)' }}>
          <div style={styles.sidebarHeader}>
            <div>
              <p style={styles.kicker}>Workspace</p>
              <h1 style={styles.logo}>SUMMIFY</h1>
            </div>
            <button type="button" onClick={() => fileInputRef.current?.click()} style={styles.primaryButton}>
              + New Document
            </button>
          </div>

          <div style={styles.uploadCardWrap}>
            <div
              onDragOver={(event) => {
                event.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                ...styles.uploadCard,
                borderColor: dragging ? '#3b82f6' : '#dbe1ea',
                background: dragging ? '#eff6ff' : '#f8fafc',
              }}
            >
              <input ref={fileInputRef} type="file" accept="application/pdf" style={{ display: 'none' }} onChange={onInputFileChange} />
              <div style={{ fontSize: 28, marginBottom: 8 }}>{dragging ? '↑' : '↓'}</div>
              <p style={{ fontSize: 18, fontWeight: 700, margin: 0 }}>{dragging ? 'Release to upload' : 'Upload your PDF'}</p>
              <p style={{ fontSize: 13, color: '#64748b', margin: '8px 0 0' }}>{dragging ? 'Drop the file to begin processing' : 'or click to browse'}</p>
            </div>
          </div>

          <div style={styles.listSection}>
            <div style={styles.listHeaderRow}>
              <h2 style={styles.sectionTitle}>Documents</h2>
              {isUploading && <span style={styles.smallBadge}>Uploading…</span>}
            </div>

            {isLoadingDocuments ? (
              <div style={{ display: 'grid', gap: 10 }}>
                {[1, 2, 3].map((item) => (
                  <div key={item} style={{ ...styles.skeleton, height: 46 }} />
                ))}
              </div>
            ) : documents.length === 0 ? (
              <div style={styles.emptyBox}>No documents uploaded yet.</div>
            ) : (
              <div style={{ display: 'grid', gap: 10 }}>
                {documents.map((documentId) => (
                  <button key={documentId} type="button" onClick={() => handleDocumentSelection(documentId)} style={{
                    ...styles.docItem,
                    borderColor: selectedDocumentId === documentId ? '#bfdbfe' : '#e2e8f0',
                    background: selectedDocumentId === documentId ? '#eff6ff' : '#ffffff',
                  }}>
                    <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: 14, fontWeight: 600 }}>{documentId}</span>
                    <span onClick={(event) => { event.stopPropagation(); void handleDeleteDocument(documentId); }} style={styles.deletePill}>Delete</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {uploadError && <div style={styles.errorBox}>{uploadError}</div>}
        </aside>

        <div style={styles.contentWrap}>
          <header style={styles.mobileHeader}>
            <button type="button" onClick={() => setIsSidebarOpen((value) => !value)} style={styles.secondaryButton}>Menu</button>
            <div style={styles.currentDocLabel}>Current Document</div>
          </header>

          <div style={styles.mainGrid}>
            <section style={styles.panelLeft}>
              <div style={styles.panelHeader}>
                <div>
                  <p style={styles.kicker}>Summary</p>
                  <h2 style={styles.panelTitle}>Current Document</h2>
                </div>
                <div style={styles.docBadge}>{selectedDocument ? selectedDocument.slice(0, 12) : 'No document selected'}</div>
              </div>

              <div style={{ display: 'grid', gap: 18, padding: 18 }}>
                <div style={styles.card}>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12 }}>
                    {summaryTypeOptions.map((option) => (
                      <button
                        key={option.value}
                        type="button"
                        onClick={() => {
                          setSummaryType(option.value);
                          setSummaryQuery(defaultSummaryQuery(option.value));
                        }}
                        style={{
                          ...styles.summaryChip,
                          background: summaryType === option.value ? '#dbeafe' : '#ffffff',
                          borderColor: summaryType === option.value ? '#bfdbfe' : '#dfe7ef',
                          color: summaryType === option.value ? '#1d4ed8' : '#334155',
                        }}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>

                  <label style={styles.label}>Prompt</label>
                  <textarea value={summaryQuery} onChange={(event) => setSummaryQuery(event.target.value)} rows={4} style={styles.textArea} placeholder="Describe what you want the summary to focus on." />

                  <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginTop: 16 }}>
                    <button type="button" onClick={handleGenerateSummary} disabled={!selectedDocumentId || isGeneratingSummary} style={{ ...styles.primaryButton, opacity: !selectedDocumentId || isGeneratingSummary ? 0.6 : 1 }}>
                      {isGeneratingSummary ? 'Generating…' : 'Generate Summary'}
                    </button>
                    <button type="button" onClick={() => setSummaryResult(null)} style={styles.secondaryButton}>Clear</button>
                  </div>

                  {summaryError && <div style={styles.errorBox}>{summaryError}</div>}
                </div>

                <div style={styles.card}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <h3 style={{ margin: 0, fontSize: 18 }}>Summary Result</h3>
                    {summaryResult && (
                      <div style={{ display: 'flex', gap: 8 }}>
                        <button type="button" onClick={handleCopySummary} style={styles.inlineButton}>Copy</button>
                        <button type="button" onClick={handleGenerateSummary} style={styles.inlineButton}>Regenerate</button>
                      </div>
                    )}
                  </div>

                  {!selectedDocumentId ? (
                    <div style={styles.emptyBox}>Select or upload a document to generate a summary.</div>
                  ) : summaryResult ? (
                    <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8, color: '#334155' }}>
                      <div style={styles.summaryTag}>{summaryResult.summary_type}</div>
                      {summaryResult.summary}
                    </div>
                  ) : (
                    <div style={styles.emptyBox}>No summary generated yet.</div>
                  )}
                </div>
              </div>
            </section>

            <section style={styles.panelRight}>
              <div style={styles.panelHeader}>
                <div>
                  <p style={styles.kicker}>Chat</p>
                  <h2 style={styles.panelTitle}>Ask about this document</h2>
                </div>
              </div>

              <div style={{ padding: 16, display: 'flex', flexDirection: 'column', height: '100%' }}>
                <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 12, flexWrap: 'wrap' }}>
                  <button type="button" onClick={() => { if (conversationId) void fetchHistory(conversationId); }} disabled={!conversationId || isLoadingHistory} style={{ ...styles.inlineButton, opacity: !conversationId || isLoadingHistory ? 0.5 : 1 }}>
                    {isLoadingHistory ? 'Loading…' : 'Load History'}
                  </button>
                  {conversationId && <span style={styles.conversationBadge}>{conversationId}</span>}
                </div>

                <div style={styles.chatArea}>
                  {!selectedDocumentId ? (
                    <div style={styles.emptyBox}>Choose or upload a document to start chatting.</div>
                  ) : chatMessages.length === 0 ? (
                    <div style={styles.emptyBox}>Ask about the document to begin the conversation.</div>
                  ) : (
                    chatMessages.map((message, index) => (
                      <div key={`${message.role}-${index}`} style={{
                        ...styles.messageBubble,
                        background: message.role === 'user' ? '#111827' : '#ffffff',
                        color: message.role === 'user' ? '#ffffff' : '#0f172a',
                        marginLeft: message.role === 'user' ? 'auto' : 0,
                        border: message.role === 'user' ? 'none' : '1px solid #e2e8f0',
                      }}>
                        <div style={{ fontSize: 10, letterSpacing: '0.18em', textTransform: 'uppercase', opacity: 0.8, marginBottom: 4 }}>{message.role === 'user' ? 'You' : 'AI'}</div>
                        <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                      </div>
                    ))
                  )}

                  {history.length > 0 && chatMessages.length === 0 && (
                    <div style={{ display: 'grid', gap: 10 }}>
                      {history.map((message, index) => (
                        <div key={`${message.role}-${index}`} style={{
                          ...styles.messageBubble,
                          background: message.role === 'user' ? '#111827' : '#ffffff',
                          color: message.role === 'user' ? '#ffffff' : '#0f172a',
                          marginLeft: message.role === 'user' ? 'auto' : 0,
                          border: message.role === 'user' ? 'none' : '1px solid #e2e8f0',
                        }}>
                          <div style={{ fontSize: 10, letterSpacing: '0.18em', textTransform: 'uppercase', opacity: 0.8, marginBottom: 4 }}>{message.role === 'user' ? 'You' : 'AI'}</div>
                          <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {chatError && <div style={styles.errorBox}>{chatError}</div>}

                <div style={{ display: 'flex', gap: 10, marginTop: 14 }}>
                  <textarea value={chatInput} onChange={(event) => setChatInput(event.target.value)} rows={3} style={{ ...styles.textArea, flex: 1, minHeight: 84 }} placeholder="What is the main conclusion?" />
                  <button type="button" onClick={() => void handleSendMessage()} disabled={isSendingMessage || !selectedDocumentId} style={{ ...styles.primaryButton, background: '#2563eb', opacity: isSendingMessage || !selectedDocumentId ? 0.6 : 1 }}>
                    {isSendingMessage ? 'Sending…' : 'Send'}
                  </button>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: { minHeight: '100vh', background: '#f8fafc', color: '#0f172a', fontFamily: 'Arial, Helvetica, sans-serif' },
  shell: { maxWidth: 1600, margin: '0 auto', display: 'flex', minHeight: '100vh', borderLeft: '1px solid #e2e8f0', borderRight: '1px solid #e2e8f0', background: '#fff' },
  sidebar: { width: 290, borderRight: '1px solid #e2e8f0', background: '#fff', position: 'fixed', left: 0, top: 0, bottom: 0, zIndex: 20, transition: 'transform 0.2s ease', boxShadow: '0 12px 28px rgba(15,23,42,0.12)' },
  sidebarHeader: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '18px 18px 16px', borderBottom: '1px solid #e2e8f0' },
  kicker: { margin: 0, fontSize: 10, letterSpacing: '0.22em', textTransform: 'uppercase', color: '#64748b', fontWeight: 700 },
  logo: { margin: '8px 0 0', fontSize: 30, letterSpacing: '-0.04em' },
  primaryButton: { background: '#0f172a', color: '#fff', border: '1px solid #0f172a', borderRadius: 12, padding: '10px 14px', fontSize: 13, fontWeight: 600, cursor: 'pointer' },
  secondaryButton: { background: '#fff', color: '#334155', border: '1px solid #d9e0ea', borderRadius: 10, padding: '9px 12px', fontSize: 13, fontWeight: 600, cursor: 'pointer' },
  uploadCardWrap: { padding: 16 },
  uploadCard: { cursor: 'pointer', borderRadius: 18, border: '2px dashed #dfe7ef', padding: 18, textAlign: 'center', transition: 'all 0.2s ease' },
  listSection: { borderTop: '1px solid #e2e8f0', padding: '14px 16px 18px' },
  listHeaderRow: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  sectionTitle: { margin: 0, fontSize: 12, letterSpacing: '0.18em', color: '#64748b', textTransform: 'uppercase' },
  smallBadge: { fontSize: 11, color: '#2563eb', fontWeight: 700 },
  emptyBox: { border: '1px dashed #d9e0ea', borderRadius: 14, background: '#f8fafc', color: '#64748b', padding: '14px 12px', fontSize: 13 },
  skeleton: { background: '#e2e8f0', borderRadius: 12, animation: 'pulse 1.5s ease-in-out infinite' },
  docItem: { display: 'flex', alignItems: 'center', width: '100%', border: '1px solid #e2e8f0', borderRadius: 12, background: '#fff', padding: '12px 10px', cursor: 'pointer', textAlign: 'left' },
  deletePill: { border: '1px solid #d9e0ea', borderRadius: 8, padding: '4px 6px', fontSize: 10, letterSpacing: '0.12em', textTransform: 'uppercase', color: '#64748b', background: '#fff' },
  errorBox: { marginTop: 10, border: '1px solid #fecaca', background: '#fef2f2', color: '#b91c1c', borderRadius: 10, padding: '10px 12px', fontSize: 13 },
  contentWrap: { flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 },
  mobileHeader: { display: 'none', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #e2e8f0', padding: '12px 14px' },
  currentDocLabel: { fontSize: 12, letterSpacing: '0.18em', textTransform: 'uppercase', color: '#64748b', fontWeight: 700 },
  mainGrid: { display: 'grid', flex: 1, gridTemplateColumns: '1.15fr 0.85fr', minHeight: 0 },
  panelLeft: { minWidth: 0, background: '#f8fafc', borderRight: '1px solid #e2e8f0' },
  panelRight: { background: '#ffffff', display: 'flex', flexDirection: 'column', minHeight: 0 },
  panelHeader: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #e2e8f0', background: '#fff', padding: '18px 20px' },
  panelTitle: { margin: '6px 0 0', fontSize: 26, letterSpacing: '-0.03em' },
  docBadge: { borderRadius: 999, border: '1px solid #e2e8f0', background: '#f1f5f9', color: '#475569', padding: '6px 10px', fontSize: 12, fontWeight: 600 },
  card: { border: '1px solid #e2e8f0', borderRadius: 18, background: '#fff', padding: 18, boxShadow: '0 10px 25px rgba(15,23,42,0.04)' },
  label: { display: 'block', marginBottom: 8, fontSize: 13, fontWeight: 600, color: '#475569' },
  textArea: { width: '100%', border: '1px solid #d7dfeb', borderRadius: 12, background: '#fff', color: '#0f172a', padding: '12px 14px', fontSize: 14, resize: 'vertical', outline: 'none' },
  summaryChip: { border: '1px solid #dfe7ef', borderRadius: 999, padding: '7px 12px', fontSize: 13, cursor: 'pointer' },
  inlineButton: { border: '1px solid #dfe7ef', background: '#f8fafc', color: '#334155', borderRadius: 10, padding: '7px 9px', cursor: 'pointer', fontSize: 12, fontWeight: 600 },
  summaryTag: { display: 'inline-flex', borderRadius: 999, border: '1px solid #bfdbfe', background: '#eff6ff', color: '#1d4ed8', fontSize: 10, letterSpacing: '0.18em', textTransform: 'uppercase', padding: '5px 8px', fontWeight: 700, marginBottom: 12 },
  conversationBadge: { borderRadius: 999, border: '1px solid #e2e8f0', background: '#f1f5f9', color: '#475569', padding: '6px 10px', fontSize: 10, letterSpacing: '0.14em', textTransform: 'uppercase', fontWeight: 700 },
  chatArea: { flex: 1, display: 'grid', gap: 10, overflowY: 'auto', borderRadius: 16, border: '1px solid #e2e8f0', background: '#f8fafc', padding: 12 },
  messageBubble: { maxWidth: '90%', borderRadius: 18, padding: '10px 12px', fontSize: 14, lineHeight: 1.6 },
};

