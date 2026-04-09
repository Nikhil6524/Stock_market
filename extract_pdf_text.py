from __future__ import annotations

import argparse
from pathlib import Path

from PyPDF2 import PdfReader


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for idx, page in enumerate(reader.pages, start=1):
        parts.append(f"\n\n===== PAGE {idx} =====\n")
        parts.append(page.extract_text() or "")
    return "".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract PDF text by page.")
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_txt", type=Path)
    args = parser.parse_args()

    input_pdf = args.input_pdf
    if any(ch in str(input_pdf) for ch in "*?[]"):
        matches = sorted(Path(".").glob(str(input_pdf)))
        if not matches:
            raise FileNotFoundError(f"No PDF found for pattern: {input_pdf}")
        input_pdf = matches[0]

    text = extract_text(input_pdf)
    args.output_txt.write_text(text, encoding="utf-8")
    print(f"Extracted text from: {input_pdf}")
    print(f"Extracted text to: {args.output_txt}")


if __name__ == "__main__":
    main()
