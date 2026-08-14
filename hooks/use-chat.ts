'use client';

import { useEffect, useMemo, useRef, useState } from 'react';

import * as chatApi from '@/lib/api/chat';
import type { ChatMessage } from '@/types/chat';

export function useChat(selectedDocumentId: string | null) {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setConversationId(null);
    setMessages([]);
    setHistory([]);
    setInput('');
    setError(null);
  }, [selectedDocumentId]);

  useEffect(() => {
    if (!scrollRef.current) {
      return;
    }
    scrollRef.current.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages, isSending]);

  const historyMeta = useMemo(() => {
    if (!conversationId) {
      return 'No active conversation';
    }
    return `Conversation ${conversationId}`;
  }, [conversationId]);

  const loadHistory = async (id = conversationId) => {
    if (!id) {
      return;
    }

    setIsLoadingHistory(true);
    setError(null);

    try {
      const response = await chatApi.getConversationHistory(id);
      setHistory(response.history ?? []);
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Unable to load conversation history.';
      setError(message);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const sendMessage = async () => {
    const trimmed = input.trim();

    if (!selectedDocumentId) {
      setError('Select a document before chatting.');
      return;
    }

    if (!trimmed) {
      setError('Message cannot be empty.');
      return;
    }

    setIsSending(true);
    setError(null);

    try {
      const response = await chatApi.sendMessage({
        message: trimmed,
        conversation_id: conversationId,
        document_id: selectedDocumentId,
      });

      const nextMessages = [
        ...messages,
        { role: 'user', content: trimmed },
        { role: 'assistant', content: response.message },
      ];

      setConversationId(response.conversation_id);
      setMessages(nextMessages);
      setHistory(nextMessages);
      setInput('');
      await loadHistory(response.conversation_id);
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Chat request failed.';
      setError(message);
    } finally {
      setIsSending(false);
    }
  };

  return {
    conversationId,
    messages,
    history,
    input,
    setInput,
    isSending,
    isLoadingHistory,
    error,
    setError,
    historyMeta,
    scrollRef,
    loadHistory,
    sendMessage,
  };
}
