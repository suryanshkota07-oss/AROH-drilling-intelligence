import type { DrillingEvent, Risk, Well } from '../types/domain'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? '/api'
/** Contract-aligned boundary; intentionally unused until backend endpoints exist. */
export const arohApi = { wells: { list: () => request<Well[]>('/wells'), detail: (wellId: string) => request<Well>(`/wells/${wellId}`), events: (wellId: string) => request<DrillingEvent[]>(`/wells/${wellId}/events`) }, risk: (wellId: string) => request<Risk>(`/risk/${wellId}`) }
async function request<T>(path: string): Promise<T> { const response = await fetch(`${apiBaseUrl}${path}`); if (!response.ok) throw new Error(`AROH API request failed: ${response.status}`); return response.json() as Promise<T> }
