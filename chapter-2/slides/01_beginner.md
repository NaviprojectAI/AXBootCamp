[슬라이드 8] [제목]
# Chapter 1. 입문
## 클로드 코드, 첫 만남

> 이 챕터가 끝나면: 클로드 코드를 설치하고 첫 대화를 나눌 수 있습니다

---

[슬라이드 9] [내용]
# Step 1: Git 설치 (Windows 필수)

1. https://git-scm.com 접속
2. **"Download for Windows"** 클릭
3. 설치 진행 — 대부분 기본값 "Next"로 진행
4. 설치 완료 확인:

```
git --version
```

> Mac은 Git이 기본 내장되어 있어 별도 설치 불필요

---

[슬라이드 10] [코드]
# Step 2: Claude Code 설치

**방법 1: PowerShell에서 설치** (추천)

```
irm https://claude.ai/install.ps1 | iex
```

**방법 2: WinGet으로 설치** (Windows 11 기본 내장, Windows 10은 미설치일 수 있음)

```
winget install Anthropic.ClaudeCode
```

⚠️ **PATH 경고 발생 시**
- 시스템 속성 → 환경 변수 → 사용자 PATH에 `C:\Users\{사용자이름}\.local\bin` 추가 → 터미널 재시작

- 설치 후 자동 업데이트 지원 (PowerShell 방식)

> Mac/Linux: `curl -fsSL https://claude.ai/install.sh | bash`

---

[슬라이드 11] [내용]
# Step 3: VSCode 설치 + Claude Code 확장

**VSCode 설치**
1. https://code.visualstudio.com 접속
2. **"Download for Windows"** 클릭 → 설치 진행
3. 설치 완료 후 실행

**Claude Code 확장 설치**
1. VSCode 좌측 **확장(Extensions)** 아이콘 클릭 (또는 `Ctrl+Shift+X`)
2. **"Claude Code"** 검색 → Anthropic 공식 확장 설치
3. 설치 완료 → 좌측 사이드바에 Claude 아이콘 등장

**왜 VSCode 확장을 쓰나요?**
- 파일 수정 내역을 **에디터에서 바로 확인**
- **diff 미리보기** — 수정한 부분을 색상으로 한눈에 비교
- 파일 탐색기, 터미널, 에디터가 **한 화면에**

> CLI가 모든 기능을 지원하지만, 이 강의에서는 **VSCode 확장 기준**으로 진행합니다 (일부 명령어는 CLI에서만 동작)

---

[슬라이드 12] [내용]
# Step 4: 인증 설정

**방법 1: Claude Pro/Max 구독** (추천)
- claude.ai에서 Pro 또는 Max 플랜 구독
- 터미널에서 `claude` 입력 → 브라우저 인증 창이 열림
- 로그인하면 자동 연결

**방법 2: API 키**
- console.anthropic.com에서 API 키 발급
- 사용한 만큼 비용 청구 (종량제)

---

[슬라이드 13] [코드]
# Step 5: 사용량 확인 — /usage

설치 후 가장 먼저 해볼 것:

```
/usage
```

- 현재 사용량과 남은 한도 확인
- **토큰 = 돈** — 클로드가 읽고 쓰는 모든 텍스트는 토큰으로 측정
- Pro/Max: 월 정해진 한도 내 사용
- API: 사용한 토큰만큼 과금

> 습관: 작업 시작 전, 끝난 후 `/usage` 확인하기

---

[슬라이드 14] [내용]
# 작업 폴더 구성과 첫 실행

**1. 새 폴더 생성** — 예: `D:\MyFirstProject`

**2. VSCode에서 폴더 열기** — 파일 > 폴더 열기

**3. 터미널 열기** — `Ctrl + `` (백틱)

---

[슬라이드 15] [코드]
# 클로드 코드 첫 실행!

터미널에서:

```
claude
```

**처음 실행하면:**
1. 인증 확인 (브라우저 로그인 또는 API 키)
2. 작업 폴더 신뢰 여부 → "Yes" 선택
3. 대화 입력창 등장!

```
╭────────────────────────────────────╮
│ Welcome to Claude Code!            │
│                                    │
│ /help for available commands       │
╰────────────────────────────────────╯

>
```

> 이 화면이 나오면 성공!

---

[슬라이드 16] [코드]
# 해보기: 첫 요청

**요청 1: 아무 질문이나 해보기**
```
최근 사회적경제 정책 동향 알려줘
```

- 답변이 바로 돌아오면 성공!
- 채팅형 AI처럼 대화가 되는지 확인

