"""키워드 관리 API"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from backend.database import get_session
from backend.models.keyword import Keyword

router = APIRouter()


class KeywordCreate(BaseModel):
    word: str
    category: str = ""


class KeywordUpdate(BaseModel):
    is_active: bool | None = None
    category: str | None = None


@router.get("")
async def list_keywords(session: Session = Depends(get_session)):
    """키워드 목록 조회"""
    keywords = session.exec(select(Keyword).order_by(Keyword.id)).all()
    return {
        "keywords": [
            {
                "id": kw.id,
                "word": kw.word,
                "is_active": kw.is_active,
                "category": kw.category,
            }
            for kw in keywords
        ],
        "total": len(keywords),
        "active": sum(1 for kw in keywords if kw.is_active),
    }


@router.post("")
async def create_keyword(data: KeywordCreate, session: Session = Depends(get_session)):
    """키워드 추가"""
    existing = session.exec(
        select(Keyword).where(Keyword.word == data.word)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="이미 존재하는 키워드입니다.")

    keyword = Keyword(word=data.word, category=data.category)
    session.add(keyword)
    session.commit()
    session.refresh(keyword)
    return {"id": keyword.id, "word": keyword.word}


@router.put("/{keyword_id}")
async def update_keyword(
    keyword_id: int, data: KeywordUpdate, session: Session = Depends(get_session)
):
    """키워드 수정 (활성/비활성, 카테고리)"""
    keyword = session.get(Keyword, keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")

    if data.is_active is not None:
        keyword.is_active = data.is_active
    if data.category is not None:
        keyword.category = data.category

    session.add(keyword)
    session.commit()
    return {"id": keyword.id, "word": keyword.word, "is_active": keyword.is_active}


@router.delete("/{keyword_id}")
async def delete_keyword(keyword_id: int, session: Session = Depends(get_session)):
    """키워드 삭제"""
    keyword = session.get(Keyword, keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")

    session.delete(keyword)
    session.commit()
    return {"message": f"키워드 '{keyword.word}'가 삭제되었습니다."}
