"""
디자인 시스템 — 색상, 폰트, 레이아웃 상수 중앙 관리
"""
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


# ═══════════════════════════════════════
# 색상 팔레트
# ═══════════════════════════════════════

# 배경
BG_DARK = RGBColor(0x1A, 0x1A, 0x2E)
BG_LIGHT = RGBColor(0xF5, 0xF0, 0xEB)

# 포인트 컬러
ACCENT = RGBColor(0xD4, 0x7B, 0x2A)       # 오렌지
ACCENT_BLUE = RGBColor(0x4A, 0x90, 0xD9)  # 블루

# 텍스트
TEXT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT_DARK = RGBColor(0x2D, 0x2D, 0x2D)
TEXT_GRAY = RGBColor(0x88, 0x88, 0x88)
TEXT_LIGHT_GRAY = RGBColor(0xAA, 0xAA, 0xAA)
TEXT_CODE = RGBColor(0xE0, 0xE0, 0xE0)

# 컴포넌트
CODE_BG = RGBColor(0x2B, 0x2B, 0x3D)
TABLE_HEADER_BG = RGBColor(0x2D, 0x2D, 0x4E)
TABLE_ROW_LIGHT = RGBColor(0xF8, 0xF6, 0xF3)
TABLE_ROW_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
QUOTE_BG = RGBColor(0xED, 0xE7, 0xDF)

# 비교 패널
PANEL_WARM = RGBColor(0xFD, 0xF0, 0xE0)   # AS-IS / Claude.ai 쪽
PANEL_COOL = RGBColor(0xE0, 0xED, 0xFD)   # TO-BE / Claude Code 쪽


# ═══════════════════════════════════════
# 폰트
# ═══════════════════════════════════════

FONT_TITLE = "Pretendard"
FONT_BODY = "Pretendard"
FONT_CODE = "Consolas"
FONT_EMOJI = "Segoe UI Emoji"


# ═══════════════════════════════════════
# 슬라이드 크기
# ═══════════════════════════════════════

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


# ═══════════════════════════════════════
# 레이아웃 상수
# ═══════════════════════════════════════

# 여백
MARGIN_LEFT = Inches(1.0)
MARGIN_TOP = Inches(0.5)
CONTENT_WIDTH = Inches(11.333)       # 슬라이드폭 - 좌우여백

# 악센트 라인
ACCENT_LINE_WIDTH = Inches(4.0)
ACCENT_LINE_HEIGHT = Pt(5)

# 제목 영역 (일반 슬라이드: content, code, compare, practice)
TITLE_TOP = Inches(0.5)
TITLE_HEIGHT = Inches(0.55)
TITLE_FONT_SIZE = 36
ACCENT_LINE_TOP = Inches(1.3)       # 제목 bottom(1.05)에서 0.25 간격
CONTENT_START_Y = Inches(1.65)       # 악센트 라인 아래 0.35 간격

# 제목 슬라이드 (title type)
TITLE_SLIDE_MAIN_TOP = Inches(2.2)
TITLE_SLIDE_MAIN_SIZE = 48
TITLE_SLIDE_SUB_SIZE = 28
TITLE_SLIDE_DESC_SIZE = 20

# 본문 텍스트
BODY_FONT_SIZE = 18
BODY_LINE_SPACING = 1.6
BULLET_FONT_SIZE = 18
SUB_HEADING_FONT_SIZE = 20

# 코드 블록
CODE_FONT_SIZE = 14
CODE_LINE_SPACING = 1.4
CODE_PADDING = Inches(0.3)

# 테이블
TABLE_HEADER_FONT_SIZE = 14
TABLE_BODY_FONT_SIZE = 13
TABLE_ROW_HEIGHT = Inches(0.52)

# 인용문
QUOTE_FONT_SIZE = 16
QUOTE_HEIGHT = Inches(0.6)
QUOTE_BAR_WIDTH = Pt(6)
QUOTE_BOTTOM_Y = Inches(6.5)        # 인용문 하단 고정 위치

# 간격
ELEMENT_GAP = Inches(0.25)           # 요소 간 기본 간격
SECTION_GAP = Inches(0.35)          # 섹션 간 간격

# 장식 요소
SIDE_BAR_WIDTH = Pt(6)               # 타이틀 슬라이드 좌측 세로 바
