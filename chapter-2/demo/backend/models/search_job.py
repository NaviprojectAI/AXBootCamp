from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class SearchJob(SQLModel, table=True):
    __tablename__ = "search_jobs"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True, unique=True)
    status: str = "pending"  # 'pending' | 'running' | 'completed' | 'failed'
    total_keywords: int = 0
    processed_keywords: int = 0
    current_keyword: str = ""
    new_results: int = 0
    duplicate_results: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
