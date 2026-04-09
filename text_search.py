from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple case-insensitive text search by line.")
    parser.add_argument("file", type=Path)
    parser.add_argument("terms", nargs="+")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8", errors="ignore").splitlines()
    terms = [t.lower() for t in args.terms]

    for idx, line in enumerate(text, start=1):
        lower = line.lower()
        if any(term in lower for term in terms):
            output = f"{idx}:{line}\n"
            sys.stdout.buffer.write(output.encode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()
