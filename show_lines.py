from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Print line ranges from a text file.")
    parser.add_argument("file", type=Path)
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int)
    args = parser.parse_args()

    lines = args.file.read_text(encoding="utf-8", errors="ignore").splitlines()
    start = max(args.start, 1)
    end = min(args.end, len(lines))
    for i in range(start, end + 1):
        output = f"{i}:{lines[i - 1]}\n"
        sys.stdout.buffer.write(output.encode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()
