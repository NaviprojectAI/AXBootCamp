import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'
import type { BidAnnouncement } from '../types'

const KEYWORDS = [
  '조직', '조직문화', '인사', '리더십', '사회복지', '사회적기업',
  '협동조합', '조직진단', '청렴도', '녹지', '인사조직',
  '인사제도', 'SVI', '사회적가치', '일 생활', '양성평등', '성희롱',
  '소셜벤처', '마을기업', '출연',
]

export default function DeadlineSoon() {
  const [bids, setBids] = useState<BidAnnouncement[]>([])

  useEffect(() => {
    async function fetch() {
      const now = new Date().toISOString()
      const threeDays = new Date()
      threeDays.setDate(threeDays.getDate() + 3)

      const { data } = await supabase
        .from('bid_announcements')
        .select('*')
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)
        .gte('deadline', now)
        .lte('deadline', threeDays.toISOString())
        .order('deadline', { ascending: true })
        .limit(10)

      setBids(data || [])
    }
    fetch()
  }, [])

  const getDDay = (deadline: string) => {
    const diff = Math.ceil((new Date(deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    return diff <= 0 ? 'D-Day' : `D-${diff}`
  }

  if (bids.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-bold text-gray-800 mb-4">마감 임박</h2>
        <p className="text-gray-500 text-sm">3일 이내 마감 공고가 없습니다.</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-lg font-bold text-gray-800 mb-4">마감 임박 (3일 이내)</h2>
      <div className="space-y-3">
        {bids.map((bid) => (
          <div key={bid.id} className="flex items-start gap-3 p-3 bg-red-50 rounded-lg border border-red-100">
            <span className="text-xs font-bold text-red-600 bg-red-100 px-2 py-1 rounded shrink-0">
              {getDDay(bid.deadline!)}
            </span>
            <div className="min-w-0 flex-1">
              <a
                href={bid.bid_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm font-medium text-gray-800 hover:text-blue-600 line-clamp-1"
              >
                {bid.title}
              </a>
              <div className="text-xs text-gray-500 mt-1">
                {bid.org_name} · {bid.amount ? `${(bid.amount / 1000).toLocaleString()}천원` : '금액 미정'}
                <span className="ml-2 px-1.5 py-0.5 bg-gray-100 rounded text-gray-500">{bid.search_keyword}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
