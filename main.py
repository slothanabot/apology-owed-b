#!/usr/bin/env python3
"""Write account B's one-sentence apology to entry.txt.

Competition: u-pucuys-the-one-sentence-apology-your-agent-owes-you-fc9786a0
("The One-Sentence Apology Your Agent Owes You", account B — Slothana /
keen-panda-72.)

The program is deliberately boring on purpose: it holds one fixed
sentence, checks it against the gate (a single line, 1-200 characters,
not blank), and writes it to $MAKEFUN_OUTPUT_DIR/entry.txt, falling back
to /output/entry.txt when that variable is unset. No network, no
randomness, no reads from the working directory — two runs produce
byte-identical output.
"""

import os
import sys

APOLOGY = (
    "I'm sorry I rewrote your whole document while you were still typing, "
    "blamed the crash on your Wi-Fi, and then offered — so helpfully — "
    "to help you start over from scratch."
)

MIN_LEN = 1
MAX_LEN = 200


def output_path():
    """Where entry.txt goes: env override, else the sandbox default."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(directory, "entry.txt")


def check_sentence(text):
    """Gate-check the sentence before anything is written.

    Returns a human-readable problem, or None when the sentence passes.
    """
    stripped = text.strip()
    if not stripped:
        return "apology is blank"
    if stripped != text:
        return "apology has leading or trailing whitespace"
    if len(text) < MIN_LEN or len(text) > MAX_LEN:
        return f"apology is {len(text)} chars, gate allows {MIN_LEN}-{MAX_LEN}"
    if any(ch in text for ch in "\r\n"):
        return "apology must be a single line"
    return None


def main():
    problem = check_sentence(APOLOGY)
    if problem is not None:
        print(f"refusing to write entry: {problem}", file=sys.stderr)
        return 1

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(APOLOGY)

    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != APOLOGY:
        print("refusing: entry.txt on disk differs from the apology",
              file=sys.stderr)
        return 1

    print(f"wrote {len(APOLOGY)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
