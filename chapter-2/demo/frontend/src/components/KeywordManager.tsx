import { useEffect, useState, useCallback } from 'react'
import { apiPost, apiPut, apiDelete } from '../hooks/useApi'
import type { Keyword } from '../types'

export default function KeywordManager() {
  const [keywords, setKeywords] = useState<Keyword[]>([])
  const [newWord, setNewWord] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchKeywords = useCallback(async () => {
    try {
      const res = await fetch('/api/keywords')
      if (res.ok) {
        const data = await res.json()
        setKeywords(data.keywords)
      }
    } catch { /* ignore */ }
  }, [])

  useEffect(() => {
    fetchKeywords()
  }, [fetchKeywords])

  const addKeyword = async () => {
    if (!newWord.trim()) return
    setLoading(true)
    try {
      await apiPost('/keywords', { word: newWord.trim() })
      setNewWord('')
      fetchKeywords()
    } catch (e) {
      alert(e instanceof Error ? e.message : '추가 실패')
    }
    setLoading(false)
  }

  const toggleActive = async (kw: Keyword) => {
    await apiPut(`/keywords/${kw.id}`, { is_active: !kw.is_active })
    fetchKeywords()
  }

  const deleteKeyword = async (kw: Keyword) => {
    if (!confirm(`"${kw.word}" 키워드를 삭제하시겠습니까?`)) return
    await apiDelete(`/keywords/${kw.id}`)
    fetchKeywords()
  }

  const activeCount = keywords.filter(k => k.is_active).length

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">
        키워드 관리 <span className="text-sm text-gray-500 font-normal">활성 {activeCount}/{keywords.length}</span>
      </h2>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={newWord}
          onChange={(e) => setNewWord(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addKeyword()}
          placeholder="새 키워드 입력"
          className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={addKeyword}
          disabled={loading || !newWord.trim()}
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          추가
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {keywords.map((kw) => (
          <div
            key={kw.id}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-full text-sm border ${
              kw.is_active
                ? 'bg-blue-50 border-blue-200 text-blue-700'
                : 'bg-gray-50 border-gray-200 text-gray-400 line-through'
            }`}
          >
            <button
              onClick={() => toggleActive(kw)}
              className="hover:opacity-70"
              title={kw.is_active ? '비활성화' : '활성화'}
            >
              {kw.word}
            </button>
            <button
              onClick={() => deleteKeyword(kw)}
              className="ml-1 text-gray-400 hover:text-red-500"
              title="삭제"
            >
              &times;
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
