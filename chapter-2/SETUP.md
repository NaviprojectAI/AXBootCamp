# 프로젝트 셋업 가이드

다른 PC에서 이 프로젝트를 처음 설정할 때 따라야 할 순서입니다.

---

## 1. PPT 엔진 (슬라이드 생성)

```bash
# Python 패키지 설치
pip install -r requirements.txt

# Pretendard 폰트 설치 (Windows)
powershell -ExecutionPolicy Bypass -File scripts/install-fonts.ps1

# Mac은 brew로 설치
# brew install --cask font-pretendard

# PPT 생성 테스트
python generate_ppt.py --chapter 00
```

## 2. 데모 백엔드 (나라장터 검색)

```bash
cd demo

# Python 패키지 설치
pip install -r requirements.txt

# .env 설정 (.env.example 복사 후 실제 값 입력)
cp .env.example .env
# 필수 항목:
#   DATA_GO_KR_API_KEY  — 공공데이터포털 API 키 (data.go.kr에서 발급)
#   SPREADSHEET_ID      — Google Sheets 스프레드시트 ID
#   SHEET_GID           — 시트 GID

# Google 서비스 계정 키 배치
mkdir -p credentials
# credentials/google-sa.json 파일을 직접 복사해야 합니다

# 백엔드 실행
uvicorn backend.main:app --reload --port 8000
```

## 3. Claude Code 설정

### 자동 포함 (git에 커밋됨)
- `.claude/settings.local.json` — MCP(Google Drive), 훅, 권한
- `.claude/skills/` — 입찰공고 검색/동기화 스킬
- `.claude/hooks/` — 시트 기록 후 메일 알림 훅

### 수동 설정 필요
글로벌 설정(`~/.claude/settings.json`)에 아래를 추가해야 합니다:

```json
{
  "mcpServers": {
    "google-drive": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@piotr-agier/google-drive-mcp"],
      "env": {}
    }
  }
}
```

> 참고: 프로젝트 `.claude/settings.local.json`에도 동일 설정이 있으므로,
> 글로벌에 없어도 이 프로젝트에서는 동작합니다.

### MCP 패키지 사전 설치 (선택)
```bash
npx -y @piotr-agier/google-drive-mcp
```

## 4. 민감 파일 체크리스트

| 파일 | 설명 | git 포함 |
|------|------|----------|
| `demo/.env` | API 키, DB 접속정보 | ❌ (.env.example 참고) |
| `demo/credentials/google-sa.json` | Google 서비스 계정 키 | ❌ (별도 전달) |
| `.claude/settings.local.json` | MCP, 훅 설정 | ✅ |
| `.claude/skills/` | Claude Code 스킬 | ✅ |
| `.claude/hooks/` | Claude Code 훅 스크립트 | ✅ |

## 5. 필수 외부 서비스

| 서비스 | 용도 | 키 발급처 |
|--------|------|----------|
| 공공데이터포털 | 나라장터 입찰공고 API | data.go.kr |
| Google Cloud | 서비스 계정 (Sheets 접근) | console.cloud.google.com |
| Supabase | PostgreSQL DB (선택) | supabase.com |
