"""
텍스트 유틸리티 — 이모지 감지, Rich Text 처리
"""
import re
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from . import design as D

# 이모지 감지용 정규식 (Unicode emoji ranges)
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F9FF"  # Misc Symbols, Emoticons, Symbols & Pictographs, Transport
    "\U00002702-\U000027B0"  # Dingbats
    "\U0000FE00-\U0000FE0F"  # Variation Selectors
    "\U0000200D"             # Zero Width Joiner
    "\U00002600-\U000026FF"  # Misc Symbols
    "\U0000231A-\U0000231B"  # Watch, Hourglass
    "\U00002934-\U00002935"  # Arrows
    "\U000025AA-\U000025FE"  # Geometric shapes
    "\U00002B05-\U00002B55"  # Arrows, circles
    "\U0000203C-\U00003299"  # CJK symbols, enclosed
    "\U0001FA00-\U0001FA6F"  # Chess, extended-A
    "\U0001FA70-\U0001FAFF"  # Symbols extended-A
    "]+",
    flags=re.UNICODE
)

# 볼드 마크다운 패턴
_BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')


def _has_emoji(text):
    """텍스트에 이모지가 포함되어 있는지 확인"""
    return bool(_EMOJI_PATTERN.search(text))


def _split_emoji_segments(text):
    """텍스트를 (일반, 이모지) 세그먼트로 분리
    Returns: list of (text, is_emoji) tuples
    """
    segments = []
    last_end = 0
    for match in _EMOJI_PATTERN.finditer(text):
        start, end = match.span()
        if start > last_end:
            segments.append((text[last_end:start], False))
        segments.append((match.group(), True))
        last_end = end
    if last_end < len(text):
        segments.append((text[last_end:], False))
    return segments if segments else [(text, False)]


def _split_bold_segments(text):
    """텍스트를 (일반, 볼드) 세그먼트로 분리
    Returns: list of (text, is_bold) tuples
    """
    segments = []
    last_end = 0
    for match in _BOLD_PATTERN.finditer(text):
        start, end = match.span()
        if start > last_end:
            segments.append((text[last_end:start], False))
        segments.append((match.group(1), True))
        last_end = end
    if last_end < len(text):
        segments.append((text[last_end:], False))
    return segments if segments else [(text, False)]


def add_rich_text(paragraph, text, font_size=None, color=None, bold=None,
                  font_name=None):
    """이모지와 볼드를 자동 처리하는 Rich Text 렌더링

    이모지는 Segoe UI Emoji 폰트로, **볼드**는 bold 처리,
    나머지는 지정된 폰트로 렌더링.
    """
    _font_name = font_name or D.FONT_BODY
    _font_size = font_size or D.BODY_FONT_SIZE
    _color = color or D.TEXT_DARK
    _bold = bold or False

    # 먼저 볼드 세그먼트로 분리
    bold_segments = _split_bold_segments(text)

    for bold_text, is_bold in bold_segments:
        # 각 볼드 세그먼트를 다시 이모지로 분리
        emoji_segments = _split_emoji_segments(bold_text)

        for seg_text, is_emoji in emoji_segments:
            if not seg_text:
                continue
            run = paragraph.add_run()
            run.text = seg_text
            run.font.size = Pt(_font_size)
            run.font.color.rgb = _color
            run.font.bold = _bold or is_bold

            if is_emoji:
                run.font.name = D.FONT_EMOJI
            else:
                run.font.name = _font_name


def set_paragraph_format(paragraph, font_size=None, color=None, bold=False,
                         alignment=PP_ALIGN.LEFT, font_name=None,
                         space_after=None):
    """단락 기본 포맷 설정 (텍스트 없이 포맷만)"""
    paragraph.alignment = alignment
    if space_after is not None:
        paragraph.space_after = space_after
