"""공공데이터포털 나라장터 API 클라이언트 (입찰공고 + 발주계획 + 사전규격)"""

import asyncio
from datetime import datetime, date, timedelta
from typing import Optional

import httpx

from backend.config import settings
from backend.models.bid import BidAnnouncement

# 엔드포인트
BID_BASE_URL = "http://apis.data.go.kr/1230000/ad/BidPublicInfoService"
ORDER_PLAN_BASE_URL = "https://apis.data.go.kr/1230000/ao/OrderPlanSttusService"
PRE_SPEC_BASE_URL = "https://apis.data.go.kr/1230000/ao/HrcspSsstndrdInfoService"


class KonepsApiClient:
    def __init__(self):
        self.api_key = settings.data_go_kr_api_key
        self.delay = settings.api_call_delay_seconds

    # ── 입찰공고 검색 ──

    async def search_bids(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        num_of_rows: int = 999,
    ) -> list[BidAnnouncement]:
        """입찰공고 검색 (용역) - PPSSrch로 키워드 검색"""
        if not end_date:
            end_date = date.today()
        if not start_date:
            # 입찰공고 API는 최대 7일 범위만 허용
            days = min(settings.search_days_range, 7)
            start_date = end_date - timedelta(days=days)

        params = {
            "ServiceKey": self.api_key,
            "numOfRows": str(num_of_rows),
            "pageNo": "1",
            "inqryDiv": "1",  # 1: 등록일시 기준
            "inqryBgnDt": start_date.strftime("%Y%m%d") + "0000",
            "inqryEndDt": end_date.strftime("%Y%m%d") + "2359",
            "bidNtceNm": keyword,
            "type": "json",
        }

        return await self._call_api(
            f"{BID_BASE_URL}/getBidPblancListInfoServcPPSSrch",
            params, keyword, "bid",
        )

    async def search_construction_bids(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[BidAnnouncement]:
        """입찰공고 검색 (공사)"""
        if not start_date:
            start_date = date.today() - timedelta(days=settings.search_days_range)
        if not end_date:
            end_date = date.today()

        params = {
            "ServiceKey": self.api_key,
            "numOfRows": "999",
            "pageNo": "1",
            "inqryDiv": "1",
            "inqryBgnDt": start_date.strftime("%Y%m%d") + "0000",
            "inqryEndDt": end_date.strftime("%Y%m%d") + "2359",
            "bidNtceNm": keyword,
            "type": "json",
        }

        return await self._call_api(
            f"{BID_BASE_URL}/getBidPblancListInfoCnstwkPPSSrch",
            params, keyword, "bid",
        )

    async def search_goods_bids(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[BidAnnouncement]:
        """입찰공고 검색 (물품)"""
        if not start_date:
            start_date = date.today() - timedelta(days=settings.search_days_range)
        if not end_date:
            end_date = date.today()

        params = {
            "ServiceKey": self.api_key,
            "numOfRows": "999",
            "pageNo": "1",
            "inqryDiv": "1",
            "inqryBgnDt": start_date.strftime("%Y%m%d") + "0000",
            "inqryEndDt": end_date.strftime("%Y%m%d") + "2359",
            "bidNtceNm": keyword,
            "type": "json",
        }

        return await self._call_api(
            f"{BID_BASE_URL}/getBidPblancListInfoThngPPSSrch",
            params, keyword, "bid",
        )

    # ── 발주계획 검색 ──

    async def search_order_plans(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[BidAnnouncement]:
        """발주계획 검색 (용역) - PPSSrch"""
        if not start_date:
            start_date = date.today() - timedelta(days=settings.search_days_range)
        if not end_date:
            end_date = date.today()

        params = {
            "ServiceKey": self.api_key,
            "numOfRows": "999",
            "pageNo": "1",
            "inqryDiv": "1",
            "inqryBgnDt": start_date.strftime("%Y%m%d") + "0000",
            "inqryEndDt": end_date.strftime("%Y%m%d") + "2359",
            "type": "json",
            "bizNm": keyword,
        }

        return await self._call_api(
            f"{ORDER_PLAN_BASE_URL}/getOrderPlanSttusListServcPPSSrch",
            params, keyword, "procurement_plan",
            parse_fn=self._parse_order_plan_item,
        )

    # ── 사전규격 검색 ──

    async def search_pre_specs(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[BidAnnouncement]:
        """사전규격 검색 (용역) - PPSSrch"""
        if not start_date:
            start_date = date.today() - timedelta(days=settings.search_days_range)
        if not end_date:
            end_date = date.today()

        params = {
            "ServiceKey": self.api_key,
            "numOfRows": "999",
            "pageNo": "1",
            "inqryDiv": "1",
            "inqryBgnDt": start_date.strftime("%Y%m%d") + "0000",
            "inqryEndDt": end_date.strftime("%Y%m%d") + "2359",
            "type": "json",
            "prdctClsfcNoNm": keyword,
        }

        return await self._call_api(
            f"{PRE_SPEC_BASE_URL}/getPublicPrcureThngInfoServcPPSSrch",
            params, keyword, "pre_spec",
            parse_fn=self._parse_pre_spec_item,
        )

    # ── 공통 ──

    async def _call_api(
        self,
        url: str,
        params: dict,
        keyword: str,
        source_type: str = "bid",
        parse_fn=None,
    ) -> list[BidAnnouncement]:
        """API 호출 및 결과 파싱"""
        if parse_fn is None:
            parse_fn = self._parse_bid_item
        results = []

        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # 응답 구조 파싱
                body = data.get("response", {}).get("body", {})
                items = body.get("items", [])

                if not items:
                    return results

                # items가 단일 객체일 수 있음
                if isinstance(items, dict):
                    items = [items]

                for item in items:
                    bid = parse_fn(item, keyword, source_type)
                    if bid:
                        results.append(bid)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    print(f"API 권한 없음 ({source_type}/{keyword}): 해당 서비스 활용 신청 필요")
                else:
                    print(f"API HTTP 에러 ({keyword}): {e.response.status_code}")
            except httpx.RequestError as e:
                print(f"API 요청 에러 ({keyword}): {e}")
            except Exception as e:
                print(f"API 파싱 에러 ({keyword}): {e}")

        return results

    def _parse_bid_item(
        self, item: dict, keyword: str, source_type: str = "bid"
    ) -> Optional[BidAnnouncement]:
        """입찰공고 API 응답 파싱"""
        try:
            bid_ntce_no = item.get("bidNtceNo", "")
            bid_ntce_ord = item.get("bidNtceOrd", "000")
            bid_id = f"{bid_ntce_no}-{bid_ntce_ord}"

            title = item.get("bidNtceNm", "").strip()
            org_name = item.get("ntceInsttNm", "").strip()

            deadline = None
            deadline_str = item.get("bidClseDt", "")
            if deadline_str:
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"]:
                    try:
                        deadline = datetime.strptime(deadline_str, fmt)
                        break
                    except ValueError:
                        continue

            amount = None
            for key in ["presmptPrce", "asignBdgtAmt"]:
                amount_str = item.get(key, "")
                if amount_str:
                    try:
                        amount = int(float(str(amount_str).replace(",", "")))
                        break
                    except (ValueError, TypeError):
                        continue

            bid_url = item.get("bidNtceDtlUrl", "") or item.get("bidNtceUrl", "")
            if not bid_url:
                bid_url = (
                    f"https://www.g2b.go.kr/link/PNPE027_01/single/"
                    f"?bidPbancNo={bid_ntce_no}&bidPbancOrd={bid_ntce_ord}"
                )

            return BidAnnouncement(
                bid_id=bid_id,
                title=title,
                org_name=org_name,
                deadline=deadline,
                amount=amount,
                bid_url=bid_url,
                source_type=source_type,
                search_keyword=keyword,
                search_date=date.today(),
            )
        except Exception as e:
            print(f"입찰공고 파싱 실패: {e}")
            return None

    def _parse_order_plan_item(
        self, item: dict, keyword: str, source_type: str = "procurement_plan"
    ) -> Optional[BidAnnouncement]:
        """발주계획 API 응답 파싱"""
        try:
            plan_no = item.get("orderPlanNo", "") or item.get("refNo", "")
            bid_id = f"PLAN-{plan_no}" if plan_no else f"PLAN-{hash(str(item))}"

            title = (item.get("bizNm", "") or item.get("prdctClsfcNoNm", "")).strip()
            org_name = (item.get("orderInsttNm", "") or item.get("rlDminsttNm", "")).strip()

            amount = None
            for key in ["orderPlanAmnt", "asignBdgtAmt"]:
                amount_str = item.get(key, "")
                if amount_str:
                    try:
                        amount = int(float(str(amount_str).replace(",", "")))
                        break
                    except (ValueError, TypeError):
                        continue

            # 발주계획은 마감일 대신 발주예정시기 사용
            deadline = None
            for key in ["orderPlanSchdulDt", "orderPlanYm"]:
                dt_str = item.get(key, "")
                if dt_str:
                    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y%m"]:
                        try:
                            deadline = datetime.strptime(dt_str, fmt)
                            break
                        except ValueError:
                            continue
                    if deadline:
                        break

            bid_url = item.get("dtlPageUrl", "")
            if not bid_url:
                bid_url = f"https://www.g2b.go.kr"

            return BidAnnouncement(
                bid_id=bid_id,
                title=title,
                org_name=org_name,
                deadline=deadline,
                amount=amount,
                bid_url=bid_url,
                source_type=source_type,
                search_keyword=keyword,
                search_date=date.today(),
            )
        except Exception as e:
            print(f"발주계획 파싱 실패: {e}")
            return None

    def _parse_pre_spec_item(
        self, item: dict, keyword: str, source_type: str = "pre_spec"
    ) -> Optional[BidAnnouncement]:
        """사전규격 API 응답 파싱"""
        try:
            spec_no = item.get("bfSpecRgstNo", "")
            bid_id = f"SPEC-{spec_no}" if spec_no else f"SPEC-{hash(str(item))}"

            title = (item.get("prdctClsfcNoNm", "") or item.get("bidNtceNm", "")).strip()
            org_name = (item.get("orderInsttNm", "") or item.get("rlDminsttNm", "")).strip()

            amount = None
            amount_str = item.get("asignBdgtAmt", "")
            if amount_str:
                try:
                    amount = int(float(str(amount_str).replace(",", "")))
                except (ValueError, TypeError):
                    pass

            deadline = None
            for key in ["opinionRgstClseDt", "rgstDt"]:
                dt_str = item.get(key, "")
                if dt_str:
                    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
                        try:
                            deadline = datetime.strptime(dt_str, fmt)
                            break
                        except ValueError:
                            continue
                    if deadline:
                        break

            bid_url = item.get("dtlPageUrl", "")
            if not bid_url:
                bid_url = f"https://www.g2b.go.kr"

            return BidAnnouncement(
                bid_id=bid_id,
                title=title,
                org_name=org_name,
                deadline=deadline,
                amount=amount,
                bid_url=bid_url,
                source_type=source_type,
                search_keyword=keyword,
                search_date=date.today(),
            )
        except Exception as e:
            print(f"사전규격 파싱 실패: {e}")
            return None

    async def wait_delay(self):
        """API rate limit 준수용 딜레이"""
        await asyncio.sleep(self.delay)
