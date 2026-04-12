from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Keyword(SQLModel, table=True):
    __tablename__ = "keywords"

    id: Optional[int] = Field(default=None, primary_key=True)
    word: str = Field(index=True, unique=True)
    is_active: bool = True
    category: str = ""  # 선택적 카테고리 분류
    created_at: datetime = Field(default_factory=datetime.now)
