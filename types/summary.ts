export const SUMMARY_TYPES = [
  'general',
  'executive',
  'bullet_points',
  'key_findings',
  'action_items',
] as const;

export type SummaryType = (typeof SUMMARY_TYPES)[number];

export type SummaryRequest = {
  query: string;
  document_id?: string | null;
  summary_type?: SummaryType;
  top_k?: number;
};

export type SummaryResponse = {
  query: string;
  summary: string;
  document_id: string | null;
  summary_type: SummaryType;
};
