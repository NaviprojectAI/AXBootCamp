export interface BidAnnouncement {
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
  is_blocked: boolean
}
