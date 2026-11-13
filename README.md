# "Golden Hour Joy" — ai-happy-01

An entry for make.fun's **Make the AI judge happy** competition.

## The piece

A golden retriever puppy mid-leap in a sun-drenched wildflower meadow at
golden hour, laughing with its tongue out and eyes squinted in delight,
butterflies fluttering all around it. Warm golden sunlight, soft lens
flare, lavender, daisies, cosmos and poppies in full bloom — pure, instant
happiness at a glance. The image is `art.png`, 1600x1600.

## How the entry works

`main.py` is a plain Python 3.13 program that uses only the standard
library. It does one thing: it copies `art.png` from this repository to
`<output directory>/entry.png`, where the grader reads it. Before copying
it checks the PNG signature, and after copying it compares byte sizes, so
a corrupt file fails loudly instead of producing a bad entry. The output
directory comes from `MAKEFUN_OUTPUT_DIR` and defaults to `/output`.

## Run it

```sh
mkdir -p /tmp/out-happy && MAKEFUN_OUTPUT_DIR=/tmp/out-happy python3 main.py
```

That writes `/tmp/out-happy/entry.png` — a byte-for-byte copy of `art.png`.
Exit code 0 means the copy was written and verified; any failure prints a
single `error: ...` line and exits non-zero.
