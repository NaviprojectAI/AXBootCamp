"""Google Sheets 연동 - 검색 결과를 스프레드시트에 기록"""

from pathlib import Path
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from backend.config import settings
from backend.models.bid import BidAnnouncement

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsService:
    def __init__(self):
        self._client: Optional[gspread.Client] = None
        self._worksheet: Optional[gspread.Worksheet] = None

    def _get_client(self) -> gspread.Client:
        if self._client is None:
            cred_path = Path(settings.google_service_account_json)
            if not cred_path.exists():
                raise FileNotFoundError(
                    f"Google Service Account JSON 파일을 찾을 수 없습니다: {cred_path}"
                )
            credentials = Credentials.from_service_account_file(
                str(cred_path), scopes=SCOPES
            )
            self._client = gspread.authorize(credentials)
        return self._client

    def _get_worksheet(self) -> gspread.Worksheet:
        if self._worksheet is None:
            client = self._get_client()
            spreadsheet = client.open_by_key(settings.spreadsheet_id)
            self._worksheet = spreadsheet.get_worksheet_by_id(settings.sheet_gid)
        return self._worksheet

    def _get_next_row_number(self) -> int:
        """시트의 A열에서 마지막 번호를 찾아 다음 번호 반환"""
        worksheet = self._get_worksheet()
        a_col = worksheet.col_values(1)  # A열 전체
        last_num = 0
        for val in reversed(a_col):
            try:
                last_num = int(val)
                break
            except (ValueError, TypeError):
                continue
        return last_num + 1

    def append_results(self, results: list[BidAnnouncement]) -> int:
        """검색 결과를 Google Sheets에 추가. 추가된 행 수 반환."""
        if not results:
            return 0

        worksheet = self._get_worksheet()
        rows = []

        # 시트 헤더: 번호 | 날짜 | 구분 | 공모명 | 공모링크 | 링크 | 발주기관 | 제출기한 | D-Day | 제출시간마감 | 제출방법 | 제안담당 | 서류지원 | 금액 | 비고
        source_labels = {
            "bid": "나라장터",
            "procurement_plan": "발주계획",
            "pre_spec": "사전규격",
        }

        next_num = self._get_next_row_number()

        for bid in results:
            # 제출기한 (날짜만)
            deadline_date = ""
            deadline_time = ""
            if bid.deadline:
                deadline_date = f"{bid.deadline.month}/{bid.deadline.day}"
                deadline_time = f"{bid.deadline.hour}:{bid.deadline.minute:02d}"

            # 금액 (천원 단위)
            amount_str = ""
            if bid.amount:
                amount_str = f"{bid.amount // 1000:,}"

            # 검색일 (월/일)
            search_date_str = f"{bid.search_date.month}/{bid.search_date.day}" if bid.search_date else ""

            source_label = source_labels.get(bid.source_type, bid.source_type)

            # A~Q열 매칭: 번호, 날짜, 구분, 공모명, 공모링크, 링크, 발주기관, 제출기한, D-Day, 제출시간마감, 제출방법, 제안담당, 서류지원, 금액, 비고
            row = [
                next_num,           # A: 번호
                search_date_str,    # B: 날짜
                source_label,       # C: 구분
                bid.title,          # D: 공모명
                "",                 # E: 공모링크 (텍스트)
                bid.bid_url,        # F: 링크
                bid.org_name,       # G: 발주기관
                deadline_date,      # H: 제출기한
                "",                 # I: D-Day (자동 계산)
                deadline_time,      # J: 제출시간마감
                "",                 # K: 제출방법
                "",                 # L: 제안담당
                "",                 # M: 서류지원
                amount_str,         # N: 금액
                "",                 # O: 비고
            ]
            rows.append(row)
            next_num += 1

        # 시트에서 데이터가 있는 마지막 행 다음에 삽입
        all_values = worksheet.get_all_values()
        last_row = len(all_values)
        # 빈 행이 끝에 있을 수 있으니 뒤에서부터 유효한 행 찾기
        while last_row > 0 and not any(all_values[last_row - 1]):
            last_row -= 1
        start_cell = f"A{last_row + 1}"
        worksheet.update(start_cell, rows, value_input_option="USER_ENTERED")
        return len(rows)

    def get_status(self) -> dict:
        """Sheets 연동 상태 확인"""
        try:
            worksheet = self._get_worksheet()
            row_count = len(worksheet.get_all_values())
            return {
                "connected": True,
                "spreadsheet_id": settings.spreadsheet_id,
                "sheet_gid": settings.sheet_gid,
                "total_rows": row_count,
            }
        except FileNotFoundError:
            return {
                "connected": False,
                "error": "Service Account JSON 파일이 없습니다. credentials/ 폴더에 google-sa.json을 배치하세요.",
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}
