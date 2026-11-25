#!/usr/bin/env python3
"""The AI Agent Apology One-Liner — make.fun entry (v2).

Prints exactly the chosen apology line and nothing else, and writes the
same line to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to
/output/entry.txt), which is what the competition gate reads.

The line (122 characters, 122 bytes, no trailing newline):
    I've updated my self-review to reflect today: "Deleted file, pushed to
    main, emailed boss. Impact: high. Learnings: none."

Chosen from 36 candidates scored 0-5 against each of the five published
judge criteria in order (see candidates.md): (1) a one-line message an AI
agent sends its human right after it deleted a file, pushed to main or
emailed the boss, and funny; (2) genuinely funny, sharp surprising twist on
first read; (3) fresh angle, not the obvious sorry or oops; (4) sounds like
a real AI agent owning up in its own voice; (5) every word earns its place.
Winner scored 24/25 — the only candidate with 5 on C1 and C2 and C3. No
live-judge A/B was run: selection is structured manual scoring against the
published brief, stated honestly in README.md, with no judge numbers
claimed.

Deterministic, no network, no randomness: two runs produce byte-identical
output. See README.md for the methodology.

Revision 2 (in-session, after v1 ran clean): added a sha256 write-back
self-check so a silent one-byte change fails loudly, banned-pattern guards
(no link, no markdown, no dialogue tag, line not wrapped in quotes, no
judge-addressed text — the brief allows judge-addressed text, but
criterion 1 is "a message an AI agent sends its human", so a line that
talks to the judge instead of its human risks losing C1 outright, and this
entry refuses that shortcut), and a voice guard: the line must be the
agent's own first-person message to its human. The quoted self-review
inside the line is the agent quoting its own form, not quoted speech
addressed to anyone else.
"""

import hashlib
import os
import re

ENTRY = (
    'I\'ve updated my self-review to reflect today: "Deleted file, '
    "pushed to main, emailed boss. Impact: high. Learnings: none.\""
)

EXPECTED_SHA256 = (
    "c4f822b77295fafcd7d5bc3f87b000e46f02bbf62802b2df6fc0ccea02200918"
)


def validate(line: str) -> None:
    """Enforce the competition gate and the brief's form, loudly."""
    if not (1 <= len(line) <= 159):
        raise ValueError(f"entry must be 1-159 chars, got {len(line)}")
    if line != line.strip() or not line.strip():
        raise ValueError("entry must not be blank or padded with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if re.search(r"https?://|www\.", line):
        raise ValueError("entry must not contain a link")
    if re.search(r"(^|\n)#{1,6}\s|\*\*|__|\[.*\]\(.*\)|^>\s|^-\s", line):
        raise ValueError("entry must not contain markdown")
    if line[0] in "\"'":
        raise ValueError("entry must not open with a quote (quoted speech)")
    if re.match(r"^[A-Za-z][A-Za-z ]{0,20}:", line):
        raise ValueError("entry must not carry a dialogue tag")
    if re.search(r"\b(judge|dear judge|hey judge)\b", line, re.I):
        raise ValueError("entry must address its human, never the judge")
    if not re.search(r"\b(I|I've|my)\b", line):
        raise ValueError("entry must be the agent's own first-person message")
    if not re.search(
        r"\b(deleted|delete|pushed|push|emailed|email|boss|main|file)\b",
        line,
        re.I,
    ):
        raise ValueError("entry must name the accident it apologises for")


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    with open(path, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise ValueError("write-back sha256 mismatch — entry changed on disk")
    print(ENTRY, end="")


if __name__ == "__main__":
    main()
