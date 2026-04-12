"""Playwright 기반 나라장터 스크래퍼 - 발주계획/사전규격 검색용"""

import asyncio
from datetime import date, datetime
from typing import Optional

from playwright.async_api import async_playwright, Browser, Page

from backend.config import settings
from backend.models.bid import BidAnnouncement


class KonepsScraper:
    def __init__(self):
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
        self._logged_in = False

    async def _ensure_browser(self):
        if self._browser is None:
            pw = await async_playwright().start()
            self._browser = await pw.chromium.launch(headless=True)
            self._page = await self._browser.new_page()

    async def login(self) -> bool:
        """나라장터 ID/PW 로그인"""
        await self._ensure_browser()

        try:
            await self._page.goto("https://www.g2b.go.kr", wait_until="networkidle")

            # 로그인 페이지로 이동
            # NOTE: 나라장터 신규 시스템은 OIDC SSO를 사용하므로
            # 실제 로그인 플로우는 사이트 구조에 맞게 조정 필요
            await self._page.click('a:has-text("로그인")')
            await self._page.wait_for_load_state("networkidle")

            # ID/PW 입력
            await self._page.fill('input[name="userId"], input[id="userId"]', settings.g2b_user_id)
            await self._page.fill('input[name="userPw"], input[id="userPw"]', settings.g2b_password)
            await self._page.click('button:has-text("로그인"), input[type="submit"]')
            await self._page.wait_for_load_state("networkidle")

            self._logged_in = True
            return True

        except Exception as e:
            print(f"로그인 실패: {e}")
            self._logged_in = False
            return False

    async def search_procurement_plans(self, keyword: str) -> list[BidAnnouncement]:
        """발주계획 검색"""
        if not self._logged_in:
            await self.login()

        results = []
        try:
            # 발주계획 목록 페이지로 이동
            # NOTE: 실제 URL과 셀렉터는 나라장터 사이트 구조에 맞게 조정 필요
            await self._page.goto(
                "https://www.g2b.go.kr/pt/menu/selectSubFrame.do?framesrc=/pt/menu/frameTgong.do",
                wait_until="networkidle",
            )

            # 검색유형: 발주계획 선택
            # 키워드 입력 및 검색
            # 결과 파싱

            # TODO: 나라장터 신규 시스템의 정확한 셀렉터 확인 후 구현
            # 현재는 placeholder - 실제 사이트 분석 후 완성

        except Exception as e:
            print(f"발주계획 검색 에러 ({keyword}): {e}")

        return results

    async def search_pre_specifications(self, keyword: str) -> list[BidAnnouncement]:
        """사전규격 공개 검색"""
        if not self._logged_in:
            await self.login()

        results = []
        try:
            # TODO: 사전규격 공개 페이지 셀렉터 확인 후 구현
            pass
        except Exception as e:
            print(f"사전규격 검색 에러 ({keyword}): {e}")

        return results

    async def close(self):
        """브라우저 종료"""
        if self._browser:
            await self._browser.close()
            self._browser = None
            self._page = None
            self._logged_in = False
