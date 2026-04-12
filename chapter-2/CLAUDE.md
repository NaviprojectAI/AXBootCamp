# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 페르소나

이 프로젝트에서 Claude는 `persona-prompt.md`에 정의된 **클로드 코드 전문 AI 강사** 역할을 수행한다.
슬라이드 내용 작성, 수정, 질문 응대 시 해당 페르소나를 참조할 것.

## 프로젝트 개요

클로드 코드(Claude Code) 강의용 PPT 자료를 마크다운에서 자동 생성하는 프로젝트.
대상은 비개발자이며, 강의 컨셉은 "코딩 강의"가 아닌 "업무 효율화 강의".

## 빌드 & 실행

```bash
# 전체 챕터 PPT 생성 (하나의 파일)
python generate_ppt.py

# 특정 챕터만 생성
python generate_ppt.py --chapter 00
python generate_ppt.py --chapter 01 02

# 챕터 목록 확인
python generate_ppt.py --list

# 출력 파일명 지정
python generate_ppt.py --chapter 01 -o my_output.pptx
```

출력 파일은 `output/` 디렉토리에 생성됨.

## 아키텍처

**파이프라인**: `slides/*.md` → `parser.py`(파싱) → `renderer.py`(렌더링) → `.pptx`

- `slides/` — 마크다운 슬라이드 원본 (00~06, `---`로 슬라이드 구분)
- `ppt_engine/` — PPT 생성 엔진 패키지
  - `design.py` — 색상, 폰트, 레이아웃 상수 중앙 관리
  - `parser.py` — 마크다운 → `SlideData`/`Element` 데이터 구조 변환
  - `renderer.py` — `SlideData` → python-pptx 슬라이드 렌더링
  - `text_utils.py` — 이모지 자동감지(Segoe UI Emoji), 볼드 마크다운 처리
- `generate_ppt.py` — CLI 진입점

## 마크다운 슬라이드 규칙

각 슬라이드는 `---`로 구분하며 첫 줄에 메타 정보 기재:
```
[슬라이드 1] [제목]
[슬라이드 2] [내용]
[슬라이드 3] [코드]
[슬라이드 4] [비교]
[슬라이드 5] [실습]
```

5가지 슬라이드 타입에 따라 렌더러가 다른 레이아웃 적용:
- **제목(title)**: 다크 배경, 좌측 세로 바, 챕터 시작용
- **내용(content)**: 라이트 배경, 범용
- **코드(code)**: content와 동일 레이아웃, 코드 블록 강조
- **비교(compare)**: 테이블이면 다크 배경, 코드 2개면 좌우 분할
- **실습(practice)**: content와 동일, 체크박스 지원

## 디자인 시스템

- 폰트: Pretendard(본문), Consolas(코드), Segoe UI Emoji(이모지)
- 슬라이드 크기: 16:9 와이드 (13.333 × 7.5 inches)
- 디자인 상수 변경은 반드시 `design.py`에서 일괄 수정
- Y좌표 자동 누적 방식으로 요소 배치 (하드코딩 좌표 지양)

## 슬라이드 넘버링 규칙

- 슬라이드를 추가하거나 제거할 때, 해당 파일 내 `[슬라이드 N]`의 번호를 반드시 순서대로 재정렬할 것
- 번호는 파일 단위가 아닌 **전체 슬라이드 기준 연번**으로 매긴다
- 이전 파일의 마지막 번호 다음부터 시작 (예: `00_cover.md`가 슬라이드 8로 끝나면 `01_beginner.md`는 슬라이드 9부터)
- 슬라이드 추가/제거 후 반드시 넘버링이 빠짐없이 연속되는지 확인할 것

## TODO 관리

- 세션 시작 시 `TODO.md`를 반드시 확인하고, 미완료 항목을 사용자에게 알릴 것
- 작업 완료 시 해당 항목을 `[x]`로 체크
- 새로운 할 일이 생기면 `TODO.md`에 추가

## 데모 프로젝트 Skills 참조

`demo/.claude/skills/` 폴더에 나라장터 입찰공고 관련 Skill이 정의되어 있다.
입찰공고 검색, 공고 링크 조회, 보고서 생성, 시트 동기화 요청 시 해당 skill.md의 지시를 따를 것.

- `demo/.claude/skills/bid-search/skill.md` — 키워드로 입찰공고 검색
- `demo/.claude/skills/bid-link/skill.md` — 공고 상세 페이지 링크 조회
- `demo/.claude/skills/bid-report/skill.md` — 오늘의 검색 결과 보고서
- `demo/.claude/skills/bid-sync/skill.md` — Google Sheets 동기화

백엔드 API: `http://localhost:8000` (demo 폴더에서 uvicorn 실행)

## 주의사항

- 한국어 프로젝트: 모든 주석, 슬라이드 내용, 커밋 메시지는 한국어
- `generate_cover_ppt.py`는 구버전 — 사용하지 않음
- 이모지가 포함된 텍스트는 `text_utils.py`가 자동으로 폰트를 분리 처리함
