#!/usr/bin/env python3
"""Put "Golden Hour Joy" where the grader can find it.

The picture is finished and already lives in this repository as
art.png: a capybara soaking in a steaming Japanese onsen at golden
hour, eyes shut in total bliss, a round yellow yuzu fruit perched on
top of its head, cherry-blossom petals floating through the warm
steam. Its charm is one very specific, very contented moment — a
winter-solstice yuzu bath, not a generic cute animal — and the
animal's huge face stays legible even shrunk to a thumbnail.

This program has exactly one job: copy that picture to
<output directory>/entry.png and prove the copy is good. It needs
nothing beyond the Python 3.13 standard library, because the grading
sandbox installs nothing before it runs.

The gate is strict about what it accepts: a complete PNG or JPEG no
bigger than 1 MiB and no wider or taller than 1024 pixels. So before
anything is copied, the artwork is measured against every one of
those rules — the 8-byte signature, the width and height read
straight out of the IHDR chunk, the file size, and a trailing IEND
chunk proving the file is whole. A picture that breaks a rule is
refused with a plain error message instead of quietly producing an
entry the gate would throw out. After the copy, the result is checked
again (same byte count, same header, IEND still present), so a
truncated or corrupted write cannot slip through either.

How the outcome is reported:
  - exit code 0 means entry.png was written and double-checked;
  - anything else prints one "error: ..." line to stderr and exits
    non-zero, so the grader can tell a broken entry from a good one.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
BYTE_CEILING = 1_048_576          # gate limit: at most 1 MiB
EDGE_LIMIT = 1024                # gate limit: at most 1024x1024 pixels


def die(message: str) -> int:
    """Print one error line and hand back the failure exit code."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def read_png_size(path: str):
    """Pull (width, height) out of the PNG IHDR chunk, or None if unreadable."""
    try:
        with open(path, "rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) < 24 or header[:8] != PNG_MAGIC:
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def has_iend_tail(path: str) -> bool:
    """True when the file ends with a PNG IEND chunk, i.e. it is whole."""
    try:
        with open(path, "rb") as handle:
            handle.seek(-12, os.SEEK_END)
            tail = handle.read(12)
    except OSError:
        return False
    return len(tail) == 12 and tail[4:8] == b"IEND"


def validate_artwork(path: str) -> list:
    """Check the artwork against every gate rule.

    Returns a list of problems, in the order they should be reported;
    an empty list means the picture is fine to submit. The cheapest
    checks run first, so a bad entry is refused on the first thing
    wrong with it instead of failing later with a vaguer message.
    """
    if not os.path.isfile(path):
        return [f"art.png is missing: expected it at {path}"]

    problems = []
    size = read_png_size(path)
    if size is None:
        problems.append("art.png does not start with a valid PNG header")
        return problems
    width, height = size
    if width > EDGE_LIMIT or height > EDGE_LIMIT:
        problems.append(
            f"art.png is {width}x{height}, over the {EDGE_LIMIT}x{EDGE_LIMIT} limit"
        )

    nbytes = os.path.getsize(path)
    if nbytes > BYTE_CEILING:
        problems.append(f"art.png is {nbytes} bytes, over the {BYTE_CEILING} byte limit")

    if not has_iend_tail(path):
        problems.append("art.png does not end with a PNG IEND chunk (not a whole image)")

    return problems


def write_entry(artwork: str, entry_path: str):
    """Copy the artwork to entry_path and check the copy.

    Returns (error, bytes, width, height): error is None on success,
    otherwise a message describing what went wrong with the copy.
    The copy is only trusted once its byte count, its header and its
    IEND tail all match the original.
    """
    shutil.copyfile(artwork, entry_path)

    copied = os.path.getsize(entry_path)
    original = os.path.getsize(artwork)
    if copied != original:
        return f"copy incomplete: {copied} of {original} bytes written", 0, 0, 0

    if read_png_size(entry_path) != read_png_size(artwork):
        return "entry.png header does not match art.png after copying", 0, 0, 0

    if not has_iend_tail(entry_path):
        return "entry.png is not a whole PNG after copying (no IEND chunk)", 0, 0, 0

    width, height = read_png_size(entry_path)
    return None, copied, width, height


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    artwork = os.path.join(here, "art.png")

    problems = validate_artwork(artwork)
    if problems:
        return die(problems[0])

    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError as exc:
        return die(f"cannot create output directory {target_dir}: {exc}")
    entry_path = os.path.join(target_dir, "entry.png")

    error, copied, width, height = write_entry(artwork, entry_path)
    if error is not None:
        return die(error)

    print(f"wrote {entry_path} ({copied} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
