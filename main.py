#!/usr/bin/env python3
"""Entry program for make.fun's "Make the AI judge happy" bounty.

The artwork, "Golden Hour Joy", is already in this repository as art.png:
a golden retriever puppy laughing mid-leap in a sun-drenched wildflower
meadow at golden hour, butterflies all around it. This script does the
only thing the entry needs: it places a copy of that image where the
grader looks for it, at <output directory>/entry.png.

Before copying it confirms art.png really is a PNG by checking its
8-byte signature, and after copying it compares byte sizes, so a corrupt
or truncated file fails loudly instead of silently producing a bad entry.

Contract with the grader:
  - exit code 0 means entry.png was written and verified;
  - any failure prints a single "error: ..." line and exits non-zero,
    so the grader can tell a broken entry from a successful one.

It needs nothing but the Python 3.13 standard library, because the
grading sandbox installs nothing before it runs this script.
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_png(path: str) -> bool:
    """True when the file starts with the 8-byte PNG signature."""
    try:
        with open(path, "rb") as handle:
            return handle.read(len(PNG_SIGNATURE)) == PNG_SIGNATURE
    except OSError:
        return False


def fail(message: str) -> int:
    """Report a problem on stderr and return the failure exit code."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, "art.png")

    if not os.path.isfile(source):
        return fail("art.png is missing from this repository")

    if not is_png(source):
        return fail("art.png does not start with a PNG signature")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, destination)

    copied = os.path.getsize(destination)
    original = os.path.getsize(source)
    if copied != original:
        return fail(f"copy incomplete: {copied} of {original} bytes written")

    print(f"wrote {destination} ({copied} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
