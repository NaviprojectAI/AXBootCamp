import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabase'

const KEYWORDS = [
  '조직', '조직문화', '인사', '리더십', '사회복지', '사회적기업',
  '협동조합', '조직진단', '청렴도', '녹지', '인사조직',
  '인사제도', 'SVI', '사회적가치', '일 생활', '양성평등', '성희롱',
  '소셜벤처', '마을기업', '출연',
]

interface Stats {
  total: number
  bid: number
  prePlan: number
  preSpec: number
  deadlineSoon: number
}

export default function StatsCards() {
  const [stats, setStats] = useState<Stats>({ total: 0, bid: 0, prePlan: 0, preSpec: 0, deadlineSoon: 0 })

  useEffect(() => {
    async function fetchStats() {
      const { count: total } = await supabase
        .from('bid_announcements')
        .select('*', { count: 'exact', head: true })
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)

      const { count: bid } = await supabase
        .from('bid_announcements')
        .select('*', { count: 'exact', head: true })
        .eq('source_type', 'bid')
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)

      const { count: prePlan } = await supabase
        .from('bid_announcements')
        .select('*', { count: 'exact', head: true })
        .eq('source_type', 'procurement_plan')
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)

      const { count: preSpec } = await supabase
        .from('bid_announcements')
        .select('*', { count: 'exact', head: true })
        .eq('source_type', 'pre_spec')
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)

      const threeDaysLater = new Date()
      threeDaysLater.setDate(threeDaysLater.getDate() + 3)
      const { count: deadlineSoon } = await supabase
        .from('bid_announcements')
        .select('*', { count: 'exact', head: true })
        .eq('is_blocked', false)
        .in('search_keyword', KEYWORDS)
        .gte('deadline', new Date().toISOString())
        .lte('deadline', threeDaysLater.toISOString())

      setStats({
        total: total || 0,
        bid: bid || 0,
        prePlan: prePlan || 0,
        preSpec: preSpec || 0,
        deadlineSoon: deadlineSoon || 0,
      })
    }
    fetchStats()
  }, [])

  const cards = [
    { label: '전체 공고', value: stats.total, color: 'bg-blue-500' },
    { label: '입찰공고', value: stats.bid, color: 'bg-indigo-500' },
    { label: '발주계획', value: stats.prePlan, color: 'bg-green-500' },
    { label: '사전규격', value: stats.preSpec, color: 'bg-purple-500' },
    { label: '마감 임박 (3일)', value: stats.deadlineSoon, color: 'bg-red-500' },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      {cards.map((c) => (
        <div key={c.label} className="bg-white rounded-xl shadow p-4">
          <div className={`text-xs font-semibold text-white ${c.color} inline-block px-2 py-0.5 rounded mb-2`}>
            {c.label}
          </div>
          <div className="text-2xl font-bold text-gray-800">{c.value.toLocaleString()}</div>
        </div>
      ))}
    </div>
  )
}
