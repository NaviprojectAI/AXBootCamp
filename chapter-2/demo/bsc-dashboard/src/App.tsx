import StatsCards from './components/StatsCards'
import DeadlineSoon from './components/DeadlineSoon'
import RecentBids from './components/RecentBids'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">나라장터 입찰공고 대시보드</h1>
          <span className="text-xs text-gray-400">읽기 전용 · Supabase 연동</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
        <StatsCards />
        <DeadlineSoon />
        <RecentBids />
      </main>
    </div>
  )
}
