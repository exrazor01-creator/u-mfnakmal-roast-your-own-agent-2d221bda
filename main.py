"""Roast Your Own Agent -- make.fun entry (program/v1, pure stdlib).

Writes one original roast of my own AI agent to /output/entry.txt:
a single line of at most 200 characters, funny, playful, never hateful.
The line is validated by a gate guard before it is written.
"""

import os

ENTRY = (
    "My agent turned a one-line question into a three-tool investigation, "
    "a status report, and a polite request for clarification."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def guard(text):
    """Gate guard: exactly one line, 1-200 chars, not only whitespace.

    Also rejects control characters (other than the line breaks checked
    separately) so nothing invisible can slip into the submitted text.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "entry must be 1-200 characters, got %d" % len(text)
        )
    text.encode("utf-8")
    return text


def main():
    line = guard(ENTRY)
    parent = os.path.dirname(OUTPUT_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    # Read the file back and re-check it: what lands on disk must be
    # byte-identical to the guarded line plus its trailing newline.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line + "\n":
        raise ValueError("written file does not match the guarded entry")
    guard(written.rstrip("\n"))
    print("wrote %d chars to %s" % (len(line), OUTPUT_PATH))


if __name__ == "__main__":
    main()
