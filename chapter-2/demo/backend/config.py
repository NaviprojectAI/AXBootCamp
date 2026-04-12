from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # 나라장터 로그인
    g2b_user_id: str = ""
    g2b_password: str = ""

    # 공공데이터포털 API
    data_go_kr_api_key: str = ""

    # Google Sheets
    google_service_account_json: str = "./credentials/google-sa.json"
    spreadsheet_id: str = "1UsyNSNMNjlGBIOIodwQGgJPAMzFIjfts4hF7X0VJlSQ"
    sheet_gid: int = 593929283

    # 앱 설정
    search_days_range: int = 7
    api_call_delay_seconds: float = 1.0
    database_url: str = "sqlite:///./data/koneps.db"

    # CORS 허용 오리진
    cors_origins: list[str] = ["http://localhost:5173"]

    # 기본 키워드 목록
    default_keywords: list[str] = [
        "조직", "조직문화", "인사", "리더십", "사회복지", "사회적기업",
        "가치", "컨설팅", "연구", "협동조합", "사회", "조직진단",
        "청렴도", "평가", "지표", "복지", "성과", "인사조직",
        "인사제도", "모니터링", "개발", "육성", "창업", "SVI",
        "사회적가치", "일 생활", "양성평등", "성희롱", "소셜벤더",
        "마을기업", "과학기술", "출연",
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
