'use client';

import { useMemo, useState } from 'react';

import * as summaryApi from '@/lib/api/summary';
import { SUMMARY_TYPES, type SummaryResponse, type SummaryType } from '@/types/summary';

const SUMMARY_PROMPTS: Record<SummaryType, string> = {
  general: 'Summarize this document in a clear, balanced way.',
  executive: 'Provide an executive summary of this document.',
  bullet_points: 'Extract the key points from this document as bullet points.',
  key_findings: 'What are the key findings and conclusions in this document?',
  action_items: 'Extract the action items and next steps from this document.',
};

export function useSummary() {
  const [summaryType, setSummaryType] = useState<SummaryType>('executive');
  const [query, setQuery] = useState(SUMMARY_PROMPTS.executive);
  const [result, setResult] = useState<SummaryResponse | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const summaryTypeOptions = useMemo(
    () => SUMMARY_TYPES.map((value) => ({ value, label: value.replace('_', ' ') })),
    [],
  );

  const changeSummaryType = (nextType: SummaryType) => {
    setSummaryType(nextType);
    setQuery(SUMMARY_PROMPTS[nextType]);
  };

  const clearSummary = () => {
    setResult(null);
    setError(null);
  };

  const generateSummary = async (documentId: string | null) => {
    if (!documentId) {
      setError('Select a document before generating a summary.');
      return;
    }

    setIsGenerating(true);
    setError(null);

    try {
      const response = await summaryApi.generateSummary({
        query: query.trim() || SUMMARY_PROMPTS[summaryType],
        document_id: documentId,
        summary_type: summaryType,
        top_k: 5,
      });
      setResult(response);
    } catch (cause) {
      const message = cause instanceof Error ? cause.message : 'Summary generation failed.';
      setError(message);
    } finally {
      setIsGenerating(false);
    }
  };

  const copySummary = async () => {
    if (!result?.summary) {
      return;
    }

    try {
      await navigator.clipboard.writeText(result.summary);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError('Unable to copy the summary to the clipboard.');
    }
  };

  return {
    summaryType,
    summaryTypeOptions,
    query,
    setQuery,
    result,
    isGenerating,
    error,
    copied,
    setError,
    changeSummaryType,
    clearSummary,
    generateSummary,
    copySummary,
  };
}
