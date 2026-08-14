import { requestJson } from '@/lib/api/client';
import type { SummaryRequest, SummaryResponse } from '@/types/summary';

export function generateSummary(payload: SummaryRequest): Promise<SummaryResponse> {
  return requestJson<SummaryResponse>('/api/v1/summary/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
}
