import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'
import type { BidAnnouncement } from '../types'

const SOURCE_LABELS: Record<string, { label: string; color: string }> = {
  bid: { label: '입찰공고', color: 'bg-blue-100 text-blue-700' },
  procurement_plan: { label: '발주', color: 'bg-green-100 text-green-700' },
  pre_spec: { label: '사전규격', color: 'bg-purple-100 text-purple-700' },
}

const KEYWORDS = [
  '조직', '조직문화', '인사', '리더십', '사회복지', '사회적기업',
  '협동조합', '조직진단', '청렴도', '녹지', '인사조직',
  '인사제도', 'SVI', '사회적가치', '일 생활', '양성평등', '성희롱',
  '소셜벤처', '마을기업', '출연',
]

export default function RecentBids() {
  const [bids, setBids] = useState<BidAnnouncement[]>([])
  const [filter, setFilter] = useState('')
  const [keyword, setKeyword] = useState('')
  const [page, setPage] = useState(0)
  const [total, setTotal] = useState(0)
  const pageSize = 20

  useEffect(() => {
    async function fetch() {
      let query = supabase
        .from('bid_announcements')
        .select('*', { count: 'exact' })
        .eq('is_blocked', false)
        .order('created_at', { ascending: false })
        .range(page * pageSize, (page + 1) * pageSize - 1)

      if (filter) query = query.eq('source_type', filter)
      if (keyword) {
        query = query.eq('search_keyword', keyword)
      } else {
        query = query.in('search_keyword', KEYWORDS)
      }

      const { data, count } = await query
      setBids(data || [])
      setTotal(count || 0)
    }
    fetch()
  }, [filter, keyword, page])

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div className="bg-white rounded-xl shadow">
      <div className="p-6 border-b flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-lg font-bold text-gray-800">
          최근 공고 <span className="text-sm font-normal text-gray-500">{total.toLocaleString()}건</span>
        </h2>
        <div className="flex items-center gap-2">
          <select
            value={keyword}
            onChange={(e) => { setKeyword(e.target.value); setPage(0) }}
            className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체 키워드</option>
            {KEYWORDS.map((kw) => (
              <option key={kw} value={kw}>{kw}</option>
            ))}
          </select>
          <select
            value={filter}
            onChange={(e) => { setFilter(e.target.value); setPage(0) }}
            className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체 구분</option>
            <option value="bid">입찰공고</option>
            <option value="procurement_plan">발주계획</option>
            <option value="pre_spec">사전규격</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left font-medium text-gray-600 w-20">구분</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">공고명</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">발주기관</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">마감일</th>
              <th className="px-4 py-3 text-left font-medium text-gray-600">키워드</th>
              <th className="px-4 py-3 text-right font-medium text-gray-600">금액</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {bids.map((bid) => {
              const src = SOURCE_LABELS[bid.source_type] || { label: bid.source_type, color: 'bg-gray-100 text-gray-600' }
              return (
                <tr key={bid.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium whitespace-nowrap ${src.color}`}>{src.label}</span>
                  </td>
                  <td className="px-4 py-3">
                    <a href={bid.bid_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline line-clamp-1">
                      {bid.title}
                    </a>
                  </td>
                  <td className="px-4 py-3 text-gray-700 whitespace-nowrap">{bid.org_name}</td>
                  <td className="px-4 py-3 text-gray-600 whitespace-nowrap">
                    {bid.deadline ? new Date(bid.deadline).toLocaleDateString('ko-KR') : '-'}
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 bg-gray-100 rounded text-xs text-gray-600">{bid.search_keyword}</span>
                  </td>
                  <td className="px-4 py-3 text-right text-gray-700 whitespace-nowrap">
                    {bid.amount ? `${bid.amount.toLocaleString()}원` : '-'}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div className="p-4 border-t flex items-center justify-center gap-2">
          <button
            onClick={() => setPage(p => Math.max(0, p - 1))}
            disabled={page === 0}
            className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50 text-sm"
          >
            이전
          </button>
          <span className="text-sm text-gray-600">{page + 1} / {totalPages}</span>
          <button
            onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50 text-sm"
          >
            다음
          </button>
        </div>
      )}
    </div>
  )
}
