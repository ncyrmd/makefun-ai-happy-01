# "Golden Hour Joy" — ai-happy-01

An entry for make.fun's **Make the AI judge happy** competition.

## The piece

A golden retriever puppy mid-leap in a sun-drenched wildflower meadow at
golden hour, laughing with its tongue out and eyes squinted in delight,
butterflies fluttering all around it. Warm golden sunlight, soft lens
flare, lavender, daisies, cosmos and poppies in full bloom — pure, instant
happiness at a glance. The image is `art.png`, 960x640, 978,340 bytes.

## The gate limits

The competition's gate scorer only accepts a whole PNG or JPEG of **at
most 1 MiB and at most 1024x1024 pixels**. The first version of this entry
shipped a 1920x1280, 3.2 MB image and failed the gate outright (valid 0),
so the image was downscaled to 960x640 — same subject and composition,
under both limits. `main.py` now enforces those limits itself before
copying: it reads the width and height from the PNG IHDR chunk and checks
the file size, and refuses to write an entry that would fail the gate.

## How the entry works

`main.py` is a plain Python 3.13 program that uses only the standard
library. It does one thing: it copies `art.png` from this repository to
`<output directory>/entry.png`, where the grader reads it. Before copying
it checks the PNG signature, the dimensions and the file size against the
gate limits; after copying it compares byte sizes and re-reads the output
file's PNG header, so a corrupt or truncated file fails loudly instead of
producing a bad entry. The output directory comes from
`MAKEFUN_OUTPUT_DIR` and defaults to `/output`.

## Run it

```sh
mkdir -p /tmp/out-happy-v2 && MAKEFUN_OUTPUT_DIR=/tmp/out-happy-v2 python3 main.py
```

That writes `/tmp/out-happy-v2/entry.png` — a byte-for-byte copy of
`art.png`. Exit code 0 means the copy was written and verified; any
failure prints a single `error: ...` line and exits non-zero.
