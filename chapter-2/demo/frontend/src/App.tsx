import { useState, useCallback } from 'react'
import SearchPanel from './components/SearchPanel'
import JobStatus from './components/JobStatus'
import ResultsTable from './components/ResultsTable'
import KeywordManager from './components/KeywordManager'

const SHEET_URL = 'https://docs.google.com/spreadsheets/d/1ZzsKabFjoVM3zDwvpL3lUMtn3ZCNOgGrSOO__qfFYSo/edit'

type Tab = 'dashboard' | 'keywords'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('dashboard')
  const [activeJobId, setActiveJobId] = useState<string | null>(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleSearchStarted = (jobId: string) => {
    setActiveJobId(jobId)
  }

  const handleJobComplete = useCallback(() => {
    setRefreshTrigger(prev => prev + 1)
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">
            나라장터 입찰공고 검색
          </h1>
          <nav className="flex gap-1">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                activeTab === 'dashboard'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              대시보드
            </button>
            <button
              onClick={() => setActiveTab('keywords')}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                activeTab === 'keywords'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              키워드 관리
            </button>
          </nav>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
        {activeTab === 'dashboard' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SearchPanel onSearchStarted={handleSearchStarted} />
              <div className="bg-white rounded-lg shadow p-6 flex flex-col justify-center items-center gap-3">
                <h2 className="text-lg font-semibold text-gray-800">Google Sheets</h2>
                <p className="text-sm text-gray-500">추가된 공고를 시트에서 확인하세요</p>
                <a
                  href={SHEET_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-green-600 text-white px-6 py-2.5 rounded-lg hover:bg-green-700 font-medium text-sm"
                >
                  시트 열기
                </a>
              </div>
            </div>

            <JobStatus jobId={activeJobId} onComplete={handleJobComplete} />

            <ResultsTable refreshTrigger={refreshTrigger} />
          </>
        )}

        {activeTab === 'keywords' && <KeywordManager />}
      </main>
    </div>
  )
}
