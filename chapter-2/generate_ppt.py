"""
마크다운 → PPT 변환 메인 스크립트

사용법:
    python generate_ppt.py                    # 전체 챕터 생성 (하나의 PPT)
    python generate_ppt.py --chapter 00       # 특정 챕터만
    python generate_ppt.py --chapter 00 01    # 여러 챕터
    python generate_ppt.py --list             # 챕터 목록 확인
"""
import argparse
import glob
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt_engine.parser import parse_markdown
from ppt_engine.renderer import render_slides


SLIDES_DIR = os.path.join(os.path.dirname(__file__), "slides")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def find_chapters():
    """slides/ 폴더에서 마크다운 파일 목록"""
    pattern = os.path.join(SLIDES_DIR, "*.md")
    files = sorted(glob.glob(pattern))
    chapters = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        chapters.append((name, f))
    return chapters


def main():
    parser = argparse.ArgumentParser(description="Markdown to PPT converter")
    parser.add_argument("--chapter", nargs="*",
                        help="Chapter prefixes to include (e.g., 00 01 02)")
    parser.add_argument("--list", action="store_true",
                        help="List available chapters")
    parser.add_argument("--output", "-o", default=None,
                        help="Output filename (default: auto)")
    args = parser.parse_args()

    chapters = find_chapters()

    if args.list:
        print("Available chapters:")
        for name, path in chapters:
            print(f"  {name}")
        return

    # 챕터 필터링
    if args.chapter:
        selected = []
        for ch in args.chapter:
            for name, path in chapters:
                if name.startswith(ch):
                    selected.append((name, path))
                    break
        if not selected:
            print(f"No chapters found matching: {args.chapter}")
            return
        chapters = selected

    # 파싱
    all_slides = []
    for name, path in chapters:
        slides = parse_markdown(path)
        print(f"  Parsed {name}: {len(slides)} slides")
        all_slides.extend(slides)

    if not all_slides:
        print("No slides found.")
        return

    # 출력 파일명
    if args.output:
        output_path = os.path.join(OUTPUT_DIR, args.output)
    elif len(chapters) == 1:
        output_path = os.path.join(OUTPUT_DIR, f"{chapters[0][0]}.pptx")
    else:
        output_path = os.path.join(OUTPUT_DIR, "full_presentation.pptx")

    # 렌더링
    count = render_slides(all_slides, output_path)
    print(f"PPT created: {output_path}")
    print(f"Total slides: {count}")


if __name__ == "__main__":
    main()
