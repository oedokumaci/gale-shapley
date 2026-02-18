import type { MatchingRequest, MatchingResponse, StepsResponse } from '@/types';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export function runMatching(req: MatchingRequest): Promise<MatchingResponse> {
  return request('/api/matching', { method: 'POST', body: JSON.stringify(req) });
}

export function runMatchingSteps(req: MatchingRequest): Promise<StepsResponse> {
  return request('/api/matching/steps', { method: 'POST', body: JSON.stringify(req) });
}

export function healthCheck(): Promise<{ status: string }> {
  return request('/api/health');
}
