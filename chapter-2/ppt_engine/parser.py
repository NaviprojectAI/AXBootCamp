"""
마크다운 파서 — slides/*.md 파일을 슬라이드 데이터 구조로 변환
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional


# ═══════════════════════════════════════
# 데이터 구조
# ═══════════════════════════════════════

@dataclass
class Element:
    """슬라이드 내 개별 요소"""
    type: str           # heading, text, bold_text, bullets, code_block, table, quote, checkbox, image
    content: str = ""   # 단일 텍스트
    lines: List[str] = field(default_factory=list)    # 여러 줄
    level: int = 1      # heading level (1=H1, 2=H2, 3=H3)
    headers: List[str] = field(default_factory=list)  # 테이블 헤더
    rows: List[List[str]] = field(default_factory=list)  # 테이블 데이터


@dataclass
class SlideData:
    """파싱된 슬라이드 한 장의 데이터"""
    number: int = 0
    slide_type: str = "content"  # title, content, code, compare, practice
    elements: List[Element] = field(default_factory=list)


# ═══════════════════════════════════════
# 타입 매핑
# ═══════════════════════════════════════

_TYPE_MAP = {
    "제목": "title",
    "내용": "content",
    "코드": "code",
    "비교": "compare",
    "실습": "practice",
}

# 슬라이드 메타 패턴: [슬라이드 N] [타입]
_META_PATTERN = re.compile(r'\[슬라이드\s*(\d+)\]\s*\[(.+?)\]')


def _detect_type(meta_line):
    """메타 라인에서 슬라이드 번호와 타입 추출"""
    match = _META_PATTERN.search(meta_line)
    if match:
        num = int(match.group(1))
        raw_type = match.group(2).strip()
        slide_type = _TYPE_MAP.get(raw_type, "content")
        return num, slide_type
    return 0, "content"


def _parse_table(lines):
    """마크다운 테이블 파싱 → headers, rows"""
    if len(lines) < 2:
        return [], []

    def split_row(line):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # \n(리터럴 백슬래시+n)을 실제 줄바꿈으로 변환
        cells = [c.replace(r"\n", "\n") for c in cells]
        return cells

    headers = split_row(lines[0])

    # 구분선(---) 건너뛰기
    data_start = 1
    if len(lines) > 1 and re.match(r'^[\s|:-]+$', lines[1]):
        data_start = 2

    rows = []
    for line in lines[data_start:]:
        if line.strip():
            rows.append(split_row(line))
    return headers, rows


def _parse_slide_body(lines):
    """슬라이드 본문을 Element 리스트로 파싱"""
    elements = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 빈 줄 건너뛰기
        if not stripped:
            i += 1
            continue

        # 코드 블록 (```)
        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].rstrip())
                i += 1
            i += 1  # 닫는 ``` 건너뛰기
            elements.append(Element(type="code_block", lines=code_lines))
            continue

        # 이미지 (![alt](path))
        img_match = re.match(r'^!\[([^\]]*)\]\((.+?)\)', stripped)
        if img_match:
            elements.append(Element(type="image", content=img_match.group(2)))
            i += 1
            continue

        # 인용문 (>)
        if stripped.startswith(">"):
            quote_text = stripped.lstrip("> ").strip()
            elements.append(Element(type="quote", content=quote_text))
            i += 1
            continue

        # 헤딩 (#, ##, ###)
        heading_match = re.match(r'^(#{1,3})\s+(.+)', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            elements.append(Element(type="heading", content=text, level=level))
            i += 1
            continue

        # 테이블 (|로 시작)
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            headers, rows = _parse_table(table_lines)
            elements.append(Element(type="table", headers=headers, rows=rows))
            continue

        # 체크박스 (- [ ])
        if stripped.startswith("- [ ]") or stripped.startswith("- [x]"):
            checkbox_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith("- [ ]") or s.startswith("- [x]"):
                    checkbox_lines.append(s[2:].strip())  # "[ ] text" or "[x] text"
                    i += 1
                else:
                    break
            elements.append(Element(type="checkbox", lines=checkbox_lines))
            continue

        # 불릿 리스트 (-, •, 숫자.)
        if re.match(r'^[-•]\s', stripped) or re.match(r'^\d+\.\s', stripped):
            bullet_lines = []
            while i < len(lines):
                s = lines[i].strip()
                if re.match(r'^[-•]\s', s) or re.match(r'^\d+\.\s', s):
                    # 불릿 마커 제거
                    text = re.sub(r'^[-•]\s+', '', s)
                    text = re.sub(r'^\d+\.\s+', '', text)
                    bullet_lines.append(text)
                    i += 1
                elif s.startswith("  ") and bullet_lines:
                    # 들여쓰기된 연속 줄
                    bullet_lines[-1] += " " + s.strip()
                    i += 1
                else:
                    break
            elements.append(Element(type="bullets", lines=bullet_lines))
            continue

        # 볼드 텍스트 줄 (**으로 시작)
        if stripped.startswith("**") and stripped.endswith("**"):
            text = stripped.strip("*").strip()
            elements.append(Element(type="bold_text", content=text))
            i += 1
            continue

        # 일반 텍스트
        elements.append(Element(type="text", content=stripped))
        i += 1

    return elements


# ═══════════════════════════════════════
# 메인 파서
# ═══════════════════════════════════════

def parse_markdown(filepath):
    """마크다운 파일을 SlideData 리스트로 파싱

    Args:
        filepath: slides/*.md 파일 경로

    Returns:
        list[SlideData]
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 로 슬라이드 분리
    raw_slides = re.split(r'\n---\n', content)

    slides = []
    for raw in raw_slides:
        raw = raw.strip()
        if not raw:
            continue

        lines = raw.split("\n")

        # 첫 줄에서 메타 정보 추출
        slide = SlideData()
        first_line = lines[0].strip()

        if _META_PATTERN.search(first_line):
            slide.number, slide.slide_type = _detect_type(first_line)
            body_lines = lines[1:]  # 메타 줄 제외
        else:
            body_lines = lines

        # 본문 파싱
        slide.elements = _parse_slide_body(body_lines)
        slides.append(slide)

    return slides
