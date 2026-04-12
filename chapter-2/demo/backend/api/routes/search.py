"""검색 실행 및 결과 조회 API"""

import uuid
from datetime import date, datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlmodel import Session, select, col

from backend.database import get_session
from backend.models.bid import BidAnnouncement
from backend.models.search_job import SearchJob
from backend.services.search_engine import SearchEngine

router = APIRouter()
search_engine = SearchEngine()


@router.post("/run")
async def run_full_search(background_tasks: BackgroundTasks):
    """전체 키워드 검색 실행 (백그라운드)"""
    job_id = str(uuid.uuid4())[:8]
    background_tasks.add_task(search_engine.run_full_search, job_id)
    return {"job_id": job_id, "message": "검색이 시작되었습니다."}


@router.post("/run-single")
async def run_single_search(keyword: str):
    """단일 키워드 검색"""
    result = await search_engine.run_single_keyword_search(keyword)
    return result


@router.put("/results/{bid_id}/block")
async def toggle_block(bid_id: str, session: Session = Depends(get_session)):
    """공고 차단/차단해제 토글"""
    bid = session.exec(
        select(BidAnnouncement).where(BidAnnouncement.bid_id == bid_id)
    ).first()
    if not bid:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다")
    bid.is_blocked = not bid.is_blocked
    session.add(bid)
    session.commit()
    session.refresh(bid)
    return {"bid_id": bid_id, "is_blocked": bid.is_blocked}


@router.get("/results")
async def get_results(
    session: Session = Depends(get_session),
    search_date: Optional[str] = Query(None, description="검색일 (YYYY-MM-DD)"),
    keyword: Optional[str] = Query(None, description="키워드 필터"),
    source_type: Optional[str] = Query(None, description="소스 타입"),
    show_blocked: bool = Query(False, description="차단된 항목 포함 여부"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
):
    """검색 결과 조회 (필터링, 페이징)"""
    query = select(BidAnnouncement).order_by(col(BidAnnouncement.created_at).desc())

    if not show_blocked:
        query = query.where(BidAnnouncement.is_blocked == False)

    if search_date:
        target_date = date.fromisoformat(search_date)
        query = query.where(BidAnnouncement.search_date == target_date)

    if keyword:
        query = query.where(BidAnnouncement.search_keyword == keyword)

    if source_type:
        query = query.where(BidAnnouncement.source_type == source_type)

    # 페이징
    offset = (page - 1) * page_size
    results = session.exec(query.offset(offset).limit(page_size)).all()

    # 전체 건수 (동일 필터 적용)
    count_query = select(BidAnnouncement)
    if not show_blocked:
        count_query = count_query.where(BidAnnouncement.is_blocked == False)
    if search_date:
        count_query = count_query.where(
            BidAnnouncement.search_date == date.fromisoformat(search_date)
        )
    if keyword:
        count_query = count_query.where(BidAnnouncement.search_keyword == keyword)
    if source_type:
        count_query = count_query.where(BidAnnouncement.source_type == source_type)
    total = len(session.exec(count_query).all())

    return {
        "results": [
            {
                "id": r.id,
                "bid_id": r.bid_id,
                "title": r.title,
                "org_name": r.org_name,
                "deadline": r.deadline.isoformat() if r.deadline else None,
                "amount": r.amount,
                "bid_url": r.bid_url,
                "source_type": r.source_type,
                "search_keyword": r.search_keyword,
                "search_date": r.search_date.isoformat(),
                "is_interested": r.is_interested,
                "is_blocked": r.is_blocked,
                "sheets_synced": r.sheets_synced,
            }
            for r in results
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/results/today")
async def get_today_results(session: Session = Depends(get_session)):
    """오늘 검색 결과 (차단 제외)"""
    today = date.today()
    results = session.exec(
        select(BidAnnouncement)
        .where(BidAnnouncement.search_date == today)
        .where(BidAnnouncement.is_blocked == False)
        .order_by(col(BidAnnouncement.created_at).desc())
    ).all()

    return {
        "date": today.isoformat(),
        "count": len(results),
        "results": [
            {
                "id": r.id,
                "bid_id": r.bid_id,
                "title": r.title,
                "org_name": r.org_name,
                "deadline": r.deadline.isoformat() if r.deadline else None,
                "amount": r.amount,
                "bid_url": r.bid_url,
                "source_type": r.source_type,
                "search_keyword": r.search_keyword,
                "is_blocked": r.is_blocked,
            }
            for r in results
        ],
    }
