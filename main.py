#!/usr/bin/env python3
"""news-image-20261125 (Account B / keen-panda-72).

Copies the committed entry.png byte-for-byte to the output directory.

The image sums up Wednesday 25 November 2026 world news: a lead banner
naming the day's biggest story, a dotted world map with 35 numbered
story markers, and the 35 stories grouped by region below the map. It
was drawn by render.py (Pillow + DejaVu fonts) and committed as
entry.png; this entrypoint only copies that file, so both grader runs
write identical bytes and the result is fully deterministic.

Pure Python standard library only: no third-party imports, no network,
no randomness, no timestamps in the output.
Writes to $MAKEFUN_OUTPUT_DIR/entry.png, else /output/entry.png.
"""
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        magic = f.read(8)
    if magic != PNG_MAGIC:
        print("ERROR: entry.png is not a PNG file", file=sys.stderr)
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print("wrote %s (%d bytes)" % (dst, size))
    if size > MAX_BYTES:
        print("ERROR: entry.png exceeds the 1 MiB gate", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
