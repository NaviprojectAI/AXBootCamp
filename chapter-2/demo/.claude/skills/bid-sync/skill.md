---
name: bid-sync
description: "시트 동기화, 구글시트 기록, sheets sync, 시트에 기록, 구글시트 동기화"
---

# Google Sheets 동기화

미동기화된 입찰공고 검색 결과를 Google Sheets에 일괄 기록합니다.

## 실행 방법

1. Google Sheets 연결 상태를 확인합니다:
   - `GET http://localhost:8000/api/sheets/status`
   - 연결 실패 시 사용자에게 알림

2. 미동기화 결과를 일괄 동기화합니다:
   - `POST http://localhost:8000/api/sheets/sync`

3. 결과를 보고합니다:
   - 동기화된 건수
   - Google Sheets 링크 제공
   - 실패한 건이 있으면 원인 안내
