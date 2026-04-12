"""검색 오케스트레이션 - 키워드 루프, 중복 제거, 작업 관리"""

import uuid
from datetime import datetime

from sqlmodel import Session, select

from backend.database import engine
from backend.models.bid import BidAnnouncement
from backend.models.search_job import SearchJob
from backend.models.keyword import Keyword
from backend.services.koneps_api import KonepsApiClient


class SearchEngine:
    def __init__(self):
        self.api_client = KonepsApiClient()

    async def run_full_search(self, job_id: str | None = None) -> str:
        """전체 키워드 검색 실행"""
        if not job_id:
            job_id = str(uuid.uuid4())[:8]

        # 활성 키워드 목록 조회
        with Session(engine) as session:
            keywords = session.exec(
                select(Keyword).where(Keyword.is_active == True)
            ).all()

        if not keywords:
            return job_id

        # 작업 생성
        with Session(engine) as session:
            job = SearchJob(
                job_id=job_id,
                status="running",
                total_keywords=len(keywords),
                started_at=datetime.now(),
            )
            session.add(job)
            session.commit()

        total_new = 0
        total_dup = 0

        try:
            for i, kw in enumerate(keywords):
                # 진행 상태 업데이트
                with Session(engine) as session:
                    job = session.exec(
                        select(SearchJob).where(SearchJob.job_id == job_id)
                    ).one()
                    job.current_keyword = kw.word
                    job.processed_keywords = i
                    session.add(job)
                    session.commit()

                # 1) 입찰공고 검색 (용역)
                bids = await self.api_client.search_bids(kw.word)
                new, dup = self._save_results(bids)
                total_new += new
                total_dup += dup
                await self.api_client.wait_delay()

                # 2) 발주계획 검색
                plans = await self.api_client.search_order_plans(kw.word)
                new, dup = self._save_results(plans)
                total_new += new
                total_dup += dup
                await self.api_client.wait_delay()

                # 3) 사전규격 검색
                specs = await self.api_client.search_pre_specs(kw.word)
                new, dup = self._save_results(specs)
                total_new += new
                total_dup += dup
                await self.api_client.wait_delay()

            # 작업 완료
            with Session(engine) as session:
                job = session.exec(
                    select(SearchJob).where(SearchJob.job_id == job_id)
                ).one()
                job.status = "completed"
                job.processed_keywords = len(keywords)
                job.current_keyword = ""
                job.new_results = total_new
                job.duplicate_results = total_dup
                job.completed_at = datetime.now()
                session.add(job)
                session.commit()

        except Exception as e:
            with Session(engine) as session:
                job = session.exec(
                    select(SearchJob).where(SearchJob.job_id == job_id)
                ).one()
                job.status = "failed"
                job.error_message = str(e)
                job.completed_at = datetime.now()
                session.add(job)
                session.commit()

        return job_id

    async def run_single_keyword_search(self, keyword: str) -> dict:
        """단일 키워드 검색 (입찰공고 + 발주계획 + 사전규격)"""
        total_new = 0
        total_dup = 0
        total_count = 0

        # 입찰공고
        bids = await self.api_client.search_bids(keyword)
        new, dup = self._save_results(bids)
        total_new += new
        total_dup += dup
        total_count += len(bids)

        await self.api_client.wait_delay()

        # 발주계획
        plans = await self.api_client.search_order_plans(keyword)
        new, dup = self._save_results(plans)
        total_new += new
        total_dup += dup
        total_count += len(plans)

        await self.api_client.wait_delay()

        # 사전규격
        specs = await self.api_client.search_pre_specs(keyword)
        new, dup = self._save_results(specs)
        total_new += new
        total_dup += dup
        total_count += len(specs)

        return {"keyword": keyword, "new": total_new, "duplicates": total_dup, "total": total_count}

    def _save_results(self, bids: list[BidAnnouncement]) -> tuple[int, int]:
        """결과 저장 (중복 제거). (new_count, dup_count) 반환"""
        new_count = 0
        dup_count = 0

        with Session(engine) as session:
            for bid in bids:
                existing = session.exec(
                    select(BidAnnouncement).where(
                        BidAnnouncement.bid_id == bid.bid_id
                    )
                ).first()

                if existing:
                    dup_count += 1
                else:
                    session.add(bid)
                    new_count += 1

            session.commit()

        return new_count, dup_count
