"""Google Sheets 동기화 API"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.database import get_session
from backend.models.bid import BidAnnouncement
from backend.services.google_sheets import GoogleSheetsService

router = APIRouter()
sheets_service = GoogleSheetsService()


@router.post("/sync")
async def sync_to_sheets(session: Session = Depends(get_session)):
    """미동기화 결과를 Google Sheets에 기록"""
    unsynced = session.exec(
        select(BidAnnouncement).where(BidAnnouncement.sheets_synced == False)
    ).all()

    if not unsynced:
        return {"message": "동기화할 새 결과가 없습니다.", "synced": 0}

    try:
        count = sheets_service.append_results(unsynced)

        # 동기화 완료 표시
        for bid in unsynced:
            bid.sheets_synced = True
            session.add(bid)
        session.commit()

        return {"message": f"{count}건이 Google Sheets에 기록되었습니다.", "synced": count}
    except Exception as e:
        return {"error": str(e), "synced": 0}


@router.post("/add/{bid_id}")
async def add_single_to_sheets(bid_id: str, session: Session = Depends(get_session)):
    """개별 공고를 Google Sheets에 추가"""
    bid = session.exec(
        select(BidAnnouncement).where(BidAnnouncement.bid_id == bid_id)
    ).first()

    if not bid:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다")

    if bid.sheets_synced:
        return {"bid_id": bid_id, "sheets_synced": True, "message": "이미 추가됨"}

    try:
        sheets_service.append_results([bid])
        bid.sheets_synced = True
        session.add(bid)
        session.commit()
        return {"bid_id": bid_id, "sheets_synced": True, "message": "추가 완료"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def sheets_status():
    """Google Sheets 연동 상태"""
    return sheets_service.get_status()
