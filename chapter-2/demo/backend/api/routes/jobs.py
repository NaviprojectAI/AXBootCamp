"""작업 상태 조회 API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, col

from backend.database import get_session
from backend.models.search_job import SearchJob

router = APIRouter()


@router.get("")
async def list_jobs(session: Session = Depends(get_session)):
    """최근 작업 목록"""
    jobs = session.exec(
        select(SearchJob).order_by(col(SearchJob.created_at).desc()).limit(20)
    ).all()

    return {
        "jobs": [
            {
                "job_id": j.job_id,
                "status": j.status,
                "total_keywords": j.total_keywords,
                "processed_keywords": j.processed_keywords,
                "current_keyword": j.current_keyword,
                "new_results": j.new_results,
                "duplicate_results": j.duplicate_results,
                "started_at": j.started_at.isoformat() if j.started_at else None,
                "completed_at": j.completed_at.isoformat() if j.completed_at else None,
                "error_message": j.error_message,
            }
            for j in jobs
        ]
    }


@router.get("/{job_id}")
async def get_job(job_id: str, session: Session = Depends(get_session)):
    """특정 작업 상태 조회"""
    job = session.exec(
        select(SearchJob).where(SearchJob.job_id == job_id)
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")

    progress = 0
    if job.total_keywords > 0:
        progress = round(job.processed_keywords / job.total_keywords * 100, 1)

    return {
        "job_id": job.job_id,
        "status": job.status,
        "progress": progress,
        "total_keywords": job.total_keywords,
        "processed_keywords": job.processed_keywords,
        "current_keyword": job.current_keyword,
        "new_results": job.new_results,
        "duplicate_results": job.duplicate_results,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "error_message": job.error_message,
    }
