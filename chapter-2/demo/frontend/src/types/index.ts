export interface BidResult {
  id: number
  bid_id: string
  title: string
  org_name: string
  deadline: string | null
  amount: number | null
  bid_url: string
  source_type: string
  search_keyword: string
  search_date: string
  is_interested: boolean
  is_blocked: boolean
  sheets_synced: boolean
}

export interface SearchJob {
  job_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress?: number
  total_keywords: number
  processed_keywords: number
  current_keyword: string
  new_results: number
  duplicate_results: number
  started_at: string | null
  completed_at: string | null
  error_message: string | null
}

export interface Keyword {
  id: number
  word: string
  is_active: boolean
  category: string
}
