from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, BigInteger
from sqlmodel import SQLModel, Field


class BidAnnouncement(SQLModel, table=True):
    __tablename__ = "bid_announcements"

    id: Optional[int] = Field(default=None, primary_key=True)
    bid_id: str = Field(index=True, unique=True)  # 공고번호 (중복 제거용)
    title: str  # 공모명
    org_name: str  # 발주기관
    deadline: Optional[datetime] = None  # 제출기한
    amount: Optional[int] = Field(default=None, sa_column=Column(BigInteger))  # 금액 (추정가격)
    bid_url: str = ""  # 공고 상세 페이지 URL
    source_type: str = "bid"  # 'bid' | 'procurement_plan' | 'pre_spec'
    search_keyword: str = ""  # 검색에 사용된 키워드
    search_date: date = Field(default_factory=date.today)  # 검색일
    created_at: datetime = Field(default_factory=datetime.now)

    # 차단 기능
    is_blocked: bool = False  # 차단된 공고 (다음 검색 시 미표시)

    # Stage 2 확장용
    is_interested: bool = False  # 관심 공고 표시
    is_participating: bool = False  # 입찰 참가 표시
    sheets_synced: bool = False  # Sheets 동기화 여부
