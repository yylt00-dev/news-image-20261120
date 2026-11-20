#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Writes the pre-drawn front page for Friday 20 November 2026 into the
grader's output directory. Pure standard library, deterministic, no
network: it only copies the entry.png that ships beside this file.

Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import sys
from os import environ
from pathlib import Path

SOURCE = "entry.png"
PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
MAX_BYTES = 1024 * 1024


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_entry(path):
    blob = path.read_bytes()
    if blob[: len(PNG_MAGIC)] != PNG_MAGIC:
        fail(f"{path} is not a PNG file")
    if len(blob) > MAX_BYTES:
        fail(f"{path} is {len(blob)} bytes, over the 1 MiB cap")
    return blob


def main():
    here = Path(__file__).resolve().parent
    blob = read_entry(here / SOURCE)
    out_dir = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE
    target.write_bytes(blob)
    if target.read_bytes() != blob:
        fail(f"{target} does not match {SOURCE} after writing")


if __name__ == "__main__":
    main()
