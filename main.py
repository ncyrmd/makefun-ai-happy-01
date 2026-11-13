#!/usr/bin/env python3
"""Entry program for make.fun's "Make the AI judge happy" bounty.

The artwork, "Golden Hour Joy", is already in this repository as art.png:
a golden retriever puppy laughing mid-leap in a sun-drenched wildflower
meadow at golden hour, butterflies all around it. This script does the
only thing the entry needs: it places a copy of that image where the
grader looks for it, at <output directory>/entry.png.

The gate scorer only accepts a whole PNG or JPEG of at most 1 MiB and at
most 1024x1024 pixels, so before copying this script enforces exactly
those limits on art.png: it checks the 8-byte PNG signature, reads the
width and height straight out of the IHDR chunk, and checks the file size.
Anything over the limits fails loudly instead of silently producing an
entry the grader rejects. After copying it compares byte sizes, so a
corrupt or truncated file fails loudly too.

Contract with the grader:
  - exit code 0 means entry.png was written and verified;
  - any failure prints a single "error: ..." line and exits non-zero,
    so the grader can tell a broken entry from a successful one.

It needs nothing but the Python 3.13 standard library, because the
grading sandbox installs nothing before it runs this script.
"""

import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576          # gate limit: at most 1 MiB
MAX_DIMENSION = 1024           # gate limit: at most 1024x1024 pixels


def png_dimensions(path: str):
    """Return (width, height) from the PNG IHDR chunk, or None if unreadable."""
    try:
        with open(path, "rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != PNG_SIGNATURE:
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def fail(message: str) -> int:
    """Report a problem on stderr and return the failure exit code."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, "art.png")

    if not os.path.isfile(source):
        return fail("art.png is missing from this repository")

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        return fail(f"art.png is {size} bytes, over the {MAX_BYTES} byte limit")

    dimensions = png_dimensions(source)
    if dimensions is None:
        return fail("art.png does not start with a valid PNG header")
    width, height = dimensions
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return fail(
            f"art.png is {width}x{height}, over the "
            f"{MAX_DIMENSION}x{MAX_DIMENSION} limit"
        )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, destination)

    copied = os.path.getsize(destination)
    if copied != size:
        return fail(f"copy incomplete: {copied} of {size} bytes written")

    out_dimensions = png_dimensions(destination)
    if out_dimensions != dimensions:
        return fail(
            f"output header mismatch: {out_dimensions} instead of {dimensions}"
        )

    print(f"wrote {destination} ({copied} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
