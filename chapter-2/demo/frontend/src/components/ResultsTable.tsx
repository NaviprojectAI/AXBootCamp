import { useEffect, useState, useCallback } from 'react'
import { apiPut, apiPost } from '../hooks/useApi'
import type { BidResult } from '../types'

interface Props {
  refreshTrigger: number
}

const SOURCE_LABELS: Record<string, { label: string; color: string }> = {
  bid: { label: '입찰공고', color: 'bg-blue-100 text-blue-700' },
  procurement_plan: { label: '발주계획', color: 'bg-green-100 text-green-700' },
  pre_spec: { label: '사전규격', color: 'bg-purple-100 text-purple-700' },
}

export default function ResultsTable({ refreshTrigger }: Props) {
  const [results, setResults] = useState<BidResult[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [showBlocked, setShowBlocked] = useState(false)
  const [sourceFilter, setSourceFilter] = useState('')
  const [toast, setToast] = useState<{ message: string; type: 'block' | 'info'; bid_id?: string } | null>(null)
  const [addingIds, setAddingIds] = useState<Set<string>>(new Set())
  const pageSize = 50

  const fetchResults = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: String(page),
        page_size: String(pageSize),
        show_blocked: String(showBlocked),
      })
      if (sourceFilter) params.set('source_type', sourceFilter)

      const res = await fetch(`/api/search/results?${params}`)
      if (res.ok) {
        const data = await res.json()
        setResults(data.results)
        setTotal(data.total)
      }
    } catch { /* ignore */ }
    setLoading(false)
  }, [page, showBlocked, sourceFilter])

  useEffect(() => {
    fetchResults()
  }, [fetchResults, refreshTrigger])

  useEffect(() => {
    if (!toast) return
    const timer = setTimeout(() => setToast(null), 3000)
    return () => clearTimeout(timer)
  }, [toast])

  const handleAddToSheets = async (bid_id: string) => {
    setAddingIds(prev => new Set(prev).add(bid_id))
    try {
      await apiPost(`/sheets/add/${encodeURIComponent(bid_id)}`)
      setResults(prev =>
        prev.map(r => r.bid_id === bid_id ? { ...r, sheets_synced: true } : r)
      )
      setToast({ message: '시트에 추가 완료', type: 'info' })
    } catch (e) {
      const msg = e instanceof Error ? e.message : 'Sheets 추가 실패'
      if (msg.includes('Service Account') || msg.includes('찾을 수 없습니다') || msg.includes('credentials')) {
        setToast({ message: 'Google Sheets 연동이 아직 설정되지 않았습니다 (credentials/google-sa.json 필요)', type: 'info' })
      } else {
        setToast({ message: msg, type: 'info' })
      }
    } finally {
      setAddingIds(prev => {
        const next = new Set(prev)
        next.delete(bid_id)
        return next
      })
    }
  }

  const handleBlock = async (bid_id: string, title: string) => {
    try {
      await apiPut(`/search/results/${encodeURIComponent(bid_id)}/block`)
      setToast({ message: `"${title.slice(0, 25)}..." 차단됨`, type: 'block', bid_id })
      fetchResults()
    } catch { /* ignore */ }
  }

  const handleUndo = async () => {
    if (!toast?.bid_id) return
    try {
      await apiPut(`/search/results/${encodeURIComponent(toast.bid_id)}/block`)
      setToast(null)
      fetchResults()
    } catch { /* ignore */ }
  }

  const formatAmount = (amount: number | null) => {
    if (!amount) return '-'
    return new Intl.NumberFormat('ko-KR').format(amount) + '원'
  }

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '-'
    return dateStr.replace('T', ' ').slice(0, 16)
  }

  const getSourceBadge = (sourceType: string) => {
    const info = SOURCE_LABELS[sourceType] || { label: sourceType, color: 'bg-gray-100 text-gray-600' }
    return (
      <span className={`px-2 py-1 rounded text-xs font-medium ${info.color}`}>
        {info.label}
      </span>
    )
  }

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div className="bg-white rounded-lg shadow relative">
      {/* 토스트 알림 */}
      {toast && (
        <div className="absolute top-2 right-2 z-10 bg-gray-800 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 text-sm max-w-md">
          <span>{toast.message}</span>
          {toast.type === 'block' && toast.bid_id && (
            <button
              onClick={handleUndo}
              className="text-yellow-300 hover:text-yellow-100 font-bold underline shrink-0"
            >
              되돌리기
            </button>
          )}
        </div>
      )}

      <div className="p-6 border-b flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-lg font-semibold">
          검색 결과 <span className="text-sm text-gray-500 font-normal">총 {total}건</span>
        </h2>
        <div className="flex items-center gap-3">
          <select
            value={sourceFilter}
            onChange={(e) => { setSourceFilter(e.target.value); setPage(1) }}
            className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체 구분</option>
            <option value="bid">입찰공고</option>
            <option value="procurement_plan">발주계획</option>
            <option value="pre_spec">사전규격</option>
          </select>
          <button
            onClick={() => { setShowBlocked(!showBlocked); setPage(1) }}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium border ${
              showBlocked
                ? 'bg-red-50 text-red-700 border-red-200'
                : 'text-gray-600 border-gray-200 hover:bg-gray-50'
            }`}
          >
            {showBlocked ? '차단 포함' : '차단 목록'}
          </button>
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-gray-500">로딩 중...</div>
      ) : results.length === 0 ? (
        <div className="p-8 text-center text-gray-500">검색 결과가 없습니다.</div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">검색일</th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">구분</th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">공모명</th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">발주기관</th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">제출기한</th>
                  <th className="px-4 py-3 text-right font-medium text-gray-600">금액</th>
                  <th className="px-4 py-3 text-left font-medium text-gray-600">키워드</th>
                  <th className="px-4 py-3 text-center font-medium text-gray-600 w-28">액션</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {results.map((r) => (
                  <tr
                    key={r.id}
                    className={`hover:bg-gray-50 ${r.is_blocked ? 'opacity-50 bg-red-50' : ''}`}
                  >
                    <td className="px-4 py-3 text-gray-600 whitespace-nowrap">{r.search_date}</td>
                    <td className="px-4 py-3 whitespace-nowrap">{getSourceBadge(r.source_type)}</td>
                    <td className="px-4 py-3">
                      <a
                        href={r.bid_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                      >
                        {r.title}
                      </a>
                    </td>
                    <td className="px-4 py-3 text-gray-700 whitespace-nowrap">{r.org_name}</td>
                    <td className="px-4 py-3 text-gray-600 whitespace-nowrap">{formatDate(r.deadline)}</td>
                    <td className="px-4 py-3 text-right text-gray-700 whitespace-nowrap">{formatAmount(r.amount)}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                        {r.search_keyword}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div className="flex items-center justify-center gap-2">
                        {/* 시트 추가 버튼 / 완료 표시 */}
                        {r.sheets_synced ? (
                          <span
                            className="inline-flex items-center justify-center w-8 h-8 rounded-md bg-green-100 text-green-600 font-bold text-base"
                            title="시트에 추가됨"
                          >
                            &#10004;
                          </span>
                        ) : (
                          <button
                            onClick={() => handleAddToSheets(r.bid_id)}
                            disabled={addingIds.has(r.bid_id)}
                            title="시트에 추가"
                            className="inline-flex items-center justify-center w-8 h-8 rounded-md bg-blue-50 border border-blue-300 text-blue-600 hover:bg-blue-100 hover:border-blue-400 font-bold text-lg leading-none disabled:opacity-40"
                          >
                            {addingIds.has(r.bid_id) ? (
                              <span className="text-xs">...</span>
                            ) : (
                              '+'
                            )}
                          </button>
                        )}
                        {/* 차단 버튼 */}
                        {r.is_blocked ? (
                          <button
                            onClick={() => handleBlock(r.bid_id, r.title)}
                            title="차단 해제"
                            className="inline-flex items-center justify-center w-8 h-8 rounded-md bg-green-50 border border-green-300 text-green-600 hover:bg-green-100 font-bold text-xs"
                          >
                            해제
                          </button>
                        ) : (
                          <button
                            onClick={() => handleBlock(r.bid_id, r.title)}
                            title="차단"
                            className="inline-flex items-center justify-center w-8 h-8 rounded-md bg-red-50 border border-red-300 text-red-500 hover:bg-red-100 hover:border-red-400 font-bold text-lg leading-none"
                          >
                            &times;
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="p-4 border-t flex items-center justify-center gap-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50"
              >
                이전
              </button>
              <span className="text-sm text-gray-600">
                {page} / {totalPages}
              </span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50"
              >
                다음
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
