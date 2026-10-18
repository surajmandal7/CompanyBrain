export type Dashboard = {
  counts: Record<string, number>
  tasks: { open: number; blocked: number; done: number; byStatus: Record<string, number> }
  decisions: Array<Record<string, unknown>>
  meetings: Array<Record<string, unknown>>
}

export type ChatResult = { answer: string; citations: Array<{ id: string; label: string; type: string; kind?: string; sourceRef?: string; sourceType?: string; sourceRefs?: string[]; sourceLabels?: string[] }>; operation: string; contextRecordCount?: number }

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json', ...(options?.headers || {}) }, ...options })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${response.status})`)
  }
  return response.json()
}

export const api = {
  dashboard: () => request<Dashboard>('/api/dashboard'),
  projects: () => request<{ items: Array<Record<string, unknown>> }>('/api/projects'),
  employees: () => request<{ items: Array<Record<string, unknown>> }>('/api/employees'),
  tasks: (blocked = false) => request<{ items: Array<Record<string, unknown>> }>(`/api/tasks${blocked ? '?blocked=true' : ''}`),
  decisions: () => request<{ items: Array<Record<string, unknown>> }>('/api/decisions'),
  meetings: () => request<{ items: Array<Record<string, unknown>> }>('/api/meetings'),
  documents: (search = '') => request<{ items: Array<Record<string, unknown>> }>(`/api/documents${search ? `?search=${encodeURIComponent(search)}` : ''}`),
  graph: () => request<{ nodes: Array<Record<string, unknown>>; links: Array<Record<string, unknown>> }>('/api/knowledge-graph'),
  settings: () => request<Record<string, unknown>>('/api/settings'),
  health: () => request<Record<string, unknown>>('/api/health'),
  chat: (question: string) => request<ChatResult>('/api/chat', { method: 'POST', body: JSON.stringify({ question }) }),
  seed: (adminKey: string) => request<Record<string, unknown>>('/api/admin/seed', { method: 'POST', headers: { 'X-Admin-Key': adminKey }, body: JSON.stringify({ confirm: true }) }),
  uploadDocuments: async (adminKey: string, files: File[]) => {
    const form = new FormData(); files.forEach(file => form.append('files', file))
    const response = await fetch('/api/documents/upload', { method: 'POST', headers: { 'X-Admin-Key': adminKey }, body: form })
    const body = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(body.detail || `Upload failed (${response.status})`)
    return body as { status: string; documents: Array<Record<string, unknown>>; errors: Array<{ filename: string; error: string }>; storedCount: number; errorCount: number }
  },
}
