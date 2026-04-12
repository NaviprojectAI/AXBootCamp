---
name: bid-run
description: "나라장터 실행, 프로그램 실행, 서버 실행, bid run, 나라장터 켜줘, 백엔드 실행"
---

# 나라장터 입찰공고 검색 시스템 실행

백엔드 서버를 시작하고 브라우저에서 프론트엔드를 엽니다.

## 실행 순서

1. 기존 python 프로세스 종료 (포트 충돌 방지)
2. 백엔드 서버 시작 (uvicorn, 포트 8080)
3. 서버 정상 동작 확인 (health check)
4. 브라우저에서 `http://localhost:8080` 열기

## 실행 방법

```bash
# 1. 기존 프로세스 종료
taskkill //F //IM "python.exe" 2>/dev/null

# 2. 백엔드 시작 (백그라운드)
cd d:/1.Seminar/ClaudeCode/ClaudeCode-Chapter2/demo
python -m uvicorn backend.main:app --port 8080 --reload 2>&1 &

# 3. 서버 확인 (3~5초 대기 후)
curl -s http://localhost:8080/api/health

# 4. 브라우저 열기
start http://localhost:8080
```

## 주의사항

- 반드시 health check로 서버 동작을 확인한 후 브라우저를 열 것
- 프론트엔드는 `frontend/dist/`에 빌드된 정적 파일을 FastAPI가 직접 서빙하므로 별도 실행 불필요
- DB는 Supabase(PostgreSQL)를 사용하므로 `.env` 파일에 `DATABASE_URL`이 설정되어 있어야 함
