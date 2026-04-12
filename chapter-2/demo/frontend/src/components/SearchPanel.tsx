import { useState } from 'react'
import { apiPost } from '../hooks/useApi'

interface Props {
  onSearchStarted: (jobId: string) => void
}

export default function SearchPanel({ onSearchStarted }: Props) {
  const [loading, setLoading] = useState(false)
  const [singleKeyword, setSingleKeyword] = useState('')

  const runFullSearch = async () => {
    setLoading(true)
    try {
      const res = await apiPost<{ job_id: string }>('/search/run')
      onSearchStarted(res.job_id)
    } catch (e) {
      alert(e instanceof Error ? e.message : '검색 실행 실패')
    } finally {
      setLoading(false)
    }
  }

  const runSingleSearch = async () => {
    if (!singleKeyword.trim()) return
    setLoading(true)
    try {
      const res = await apiPost<{ keyword: string; new: number; duplicates: number }>(
        `/search/run-single?keyword=${encodeURIComponent(singleKeyword)}`
      )
      alert(`"${res.keyword}" 검색 완료: 신규 ${res.new}건, 중복 ${res.duplicates}건`)
    } catch (e) {
      alert(e instanceof Error ? e.message : '검색 실패')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">검색 실행</h2>

      <div className="flex gap-4 mb-4">
        <button
          onClick={runFullSearch}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '검색 중...' : '전체 키워드 검색'}
        </button>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={singleKeyword}
          onChange={(e) => setSingleKeyword(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && runSingleSearch()}
          placeholder="단일 키워드 입력"
          className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={runSingleSearch}
          disabled={loading || !singleKeyword.trim()}
          className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 disabled:opacity-50"
        >
          검색
        </button>
      </div>
    </div>
  )
}
