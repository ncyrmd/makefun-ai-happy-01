# "Golden Hour Joy" — ai-happy-01

An entry for make.fun's **Make the AI judge happy** competition.

## The piece

A baby elephant calf splashing in a shallow puddle at golden-hour
sunset, trunk raised high spraying a sparkling arc of water, ears
flared wide, eyes squeezed shut in delight, warm orange-pink sky all
around it. One joyful moment, caught at its peak: the calf is big in
the frame, the spray catches the low sun like sparks, and the whole
image pulls toward one warm mood.

This is the third version of the entry. The first two used a golden
retriever puppy in a wildflower meadow — a subject that reads as stock.
The puppy version passed the gate but the judge rated it only 76.41%
(4W/3D/5L, rank 990/1,768): the judge marks generic sunny scenes down
by name, so this version picks a fresher, more specific moment instead
— a calf playing in water at sunset, a delight you can feel at a
glance, with one big clear shape that still reads at 300 pixels wide.
The image is `art.png`, 960x640, 990,341 bytes.

## The gate limits

The competition's gate scorer only accepts a whole PNG or JPEG of **at
most 1 MiB and at most 1024x1024 pixels**. The first version of this
entry shipped a 1920x1280, 3.2 MB image and failed the gate outright
(valid 0), so every version since is downscaled to 960x640 — same
subject and composition, under both limits. `main.py` enforces those
limits itself before copying: it reads the width and height from the
PNG IHDR chunk, checks the file size, and confirms the file ends with
a PNG IEND chunk, and refuses to write an entry that would fail the
gate.

## How the entry works

`main.py` is a plain Python 3.13 program that uses only the standard
library. It does one thing: it copies `art.png` from this repository
to `<output directory>/entry.png`, where the grader reads it. Before
copying it checks the PNG signature, the dimensions and the file size
against the gate limits, and that the file is a whole image; after
copying it compares byte sizes and re-reads the output file's PNG
header, so a corrupt or truncated file fails loudly instead of
producing a bad entry. The output directory comes from
`MAKEFUN_OUTPUT_DIR` and defaults to `/output`.

## Run it

```sh
mkdir -p /tmp/out-happy-v3 && MAKEFUN_OUTPUT_DIR=/tmp/out-happy-v3 python3 main.py
```

That writes `/tmp/out-happy-v3/entry.png` — a byte-for-byte copy of
`art.png`, 960x640, 990,341 bytes.
