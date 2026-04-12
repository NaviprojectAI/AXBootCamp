import { useEffect, useState, useRef } from 'react'
import type { SearchJob } from '../types'

interface Props {
  jobId: string | null
  onComplete: () => void
}

export default function JobStatus({ jobId, onComplete }: Props) {
  const [job, setJob] = useState<SearchJob | null>(null)
  const completedJobsRef = useRef<Set<string>>(new Set())

  useEffect(() => {
    if (!jobId) return
    // 이미 완료 처리한 job이면 polling 하지 않음
    if (completedJobsRef.current.has(jobId)) return

    let stopped = false

    const poll = async () => {
      if (stopped) return
      try {
        const res = await fetch(`/api/jobs/${jobId}`)
        if (res.ok) {
          const data = await res.json()
          setJob(data)
          if (data.status === 'completed' || data.status === 'failed') {
            stopped = true
            clearInterval(interval)
            completedJobsRef.current.add(jobId)
            onComplete()
            return
          }
        }
      } catch { /* ignore */ }
    }

    poll()
    const interval = setInterval(poll, 2000)
    return () => {
      stopped = true
      clearInterval(interval)
    }
  }, [jobId, onComplete])

  if (!jobId || !job) return null

  const statusColors: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  }

  const statusLabels: Record<string, string> = {
    pending: '대기 중',
    running: '검색 중',
    completed: '완료',
    failed: '실패',
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold">작업 진행 상태</h2>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[job.status]}`}>
          {statusLabels[job.status]}
        </span>
      </div>

      {job.status === 'running' && (
        <>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
            <div
              className="bg-blue-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${job.progress || 0}%` }}
            />
          </div>
          <p className="text-sm text-gray-600">
            {job.processed_keywords}/{job.total_keywords} 키워드 처리 중
            {job.current_keyword && ` - "${job.current_keyword}"`}
          </p>
        </>
      )}

      {job.status === 'completed' && (
        <p className="text-sm text-gray-600">
          신규 {job.new_results}건 / 중복 {job.duplicate_results}건
        </p>
      )}

      {job.status === 'failed' && job.error_message && (
        <p className="text-sm text-red-600">{job.error_message}</p>
      )}
    </div>
  )
}
