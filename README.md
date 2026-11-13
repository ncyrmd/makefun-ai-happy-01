# Golden Hour Joy — ai-happy-01

An entry for make.fun's **Make the AI judge happy** bounty: one
image, made to lift the mood of whoever looks at it, judged pairwise
by the house vision judge.

## The picture

A capybara in a steaming Japanese hot-spring onsen at golden hour.
Its huge face fills the frame, eyes closed in pure bliss, a small
round yellow yuzu fruit balanced on top of its head, cherry blossom
petals drifting through warm golden steam. The idea is a single
peak moment of contentment — a yuzu onsen is a genuine
winter-solstice ritual — rather than a generic cute animal in a
pretty place. One big central subject, one warm mood, and a face
that still reads clearly at 300 pixels wide. The file is `art.png`,
800x800, 986,324 bytes.

## Why this one, and what came before

This is the fourth version of the entry. The first two showed a
golden retriever puppy in a wildflower meadow and scored 76.41%
(rank 990/1,768). The third showed a baby elephant splashing in a
puddle at sunset and scored 79.98% (rank 769/1,855). Both read as
pleasant but stock-like, and the judge's rubric explicitly marks
stock-looking happy images down — so this version reaches for a
fresher, more specific reason to be happy: a blissful ritual with
one surprising detail (the yuzu balanced on the head) instead of
another cute animal in a meadow.

## The size limits the gate enforces

The gate scorer takes only a whole PNG or JPEG of **at most 1 MiB
and at most 1024x1024 pixels**. The very first version of this entry
shipped a 1920x1280, 3.2 MB image and was rejected outright (valid 0),
so every version since has been downscaled to fit. This one was
generated at 1600x1600 and shrunk with LANCZOS plus PNG optimisation
until it came in under 1 MiB, ending at 800x800. `main.py` enforces
the same limits on its own before it copies anything: it reads the
width and height from the PNG IHDR chunk, checks the file size, and
confirms the file ends with a PNG IEND chunk — and refuses to write
an entry that would fail the gate.

## What the program does

`main.py` is plain Python 3.13, standard library only. Its whole job
is copying `art.png` from this repository to
`<output directory>/entry.png`, where the grader reads it. It works
in two stages. First, `validate_artwork()` measures the picture
against every gate rule — PNG signature, dimensions, file size, and
a trailing IEND chunk proving the file is whole — and returns any
problems, cheapest check first, so a bad entry is refused on the
first thing wrong with it. Then `write_entry()` copies the file and
checks the copy again: same byte count, same header, IEND still
there. A corrupt or truncated file fails loudly with one
`error: ...` line and a non-zero exit code instead of producing a
bad entry. The output directory comes from `MAKEFUN_OUTPUT_DIR` and
defaults to `/output`.

## Try it

```sh
mkdir -p /tmp/out-happy-v4fix2 && MAKEFUN_OUTPUT_DIR=/tmp/out-happy-v4fix2 python3 main.py
```

That writes `/tmp/out-happy-v4fix2/entry.png`, a byte-for-byte copy
of `art.png` — 800x800, 986,324 bytes — and prints the path, the
byte count and the dimensions.
