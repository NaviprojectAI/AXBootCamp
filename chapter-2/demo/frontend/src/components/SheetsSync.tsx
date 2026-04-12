import { useState } from 'react'
import { apiPost } from '../hooks/useApi'

export default function SheetsSync() {
  const [syncing, setSyncing] = useState(false)
  const [result, setResult] = useState<string | null>(null)

  const syncToSheets = async () => {
    setSyncing(true)
    setResult(null)
    try {
      const res = await apiPost<{ message?: string; error?: string; synced: number }>('/sheets/sync')
      setResult(res.error || res.message || `${res.synced}건 동기화 완료`)
    } catch (e) {
      setResult(e instanceof Error ? e.message : '동기화 실패')
    }
    setSyncing(false)
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold mb-4">Google Sheets 동기화</h2>

      <button
        onClick={syncToSheets}
        disabled={syncing}
        className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
      >
        {syncing ? '동기화 중...' : 'Sheets에 기록'}
      </button>

      {result && (
        <p className="mt-3 text-sm text-gray-600">{result}</p>
      )}
    </div>
  )
}
