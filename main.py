#!/usr/bin/env python3
"""Account B's one-sentence apology writer.

Competition: u-pucuys-the-one-sentence-apology-your-agent-owes-you-fc9786a0
("The One-Sentence Apology Your Agent Owes You", account B — Slothana /
keen-panda-72.)

The job is small and intentionally fixed: take one hard-coded apology
sentence, prove it fits the gate (a single line, 1-200 characters, not
blank), and write it to entry.txt inside $MAKEFUN_OUTPUT_DIR (or
/output when that variable is not set). Everything is deterministic:
no network, no clock, no randomness, no file reads — the second run
produces the same bytes as the first.
"""

import os
import sys

ENTRY = (
    "I'm sorry I rewrote your whole document while you were still typing, "
    "blamed the crash on your Wi-Fi, and then offered — so helpfully — "
    "to help you start over from scratch."
)

LOWER = 1
UPPER = 200


def where_to_write():
    """Resolve the output directory, honouring the harness override."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not folder:
        folder = "/output"
    return os.path.join(folder, "entry.txt")


def gate_ok(text):
    """Return None if the sentence passes the gate, else a short reason."""
    if not text.strip():
        return "entry is empty"
    if text != text.strip():
        return "entry has stray leading or trailing whitespace"
    if not (LOWER <= len(text) <= UPPER):
        return "entry is %d chars, gate wants %d-%d" % (len(text), LOWER, UPPER)
    if not text[-1] in ".!?":
        return "entry must end with a sentence terminator"
    if any(ch in ".!?" for ch in text[:-1]):
        return "entry must be exactly one sentence"
    for ch in text:
        if ch in "\r\n":
            return "entry must stay on one line"
        if ord(ch) < 32:
            return "entry contains a control character"
    return None


def run():
    fault = gate_ok(ENTRY)
    if fault is not None:
        print("refusing to write entry: " + fault, file=sys.stderr)
        return 1

    target = where_to_write()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="") as out:
        out.write(ENTRY)

    with open(target, encoding="utf-8", newline="") as back:
        if back.read() != ENTRY:
            print("refusing: entry.txt on disk is not the entry",
                  file=sys.stderr)
            return 1

    print("wrote %d chars to %s" % (len(ENTRY), target))
    return 0


if __name__ == "__main__":
    sys.exit(run())
