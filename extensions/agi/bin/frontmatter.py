"""One line-anchored frontmatter reader.

THE single place the frontmatter boundary of a node file is defined. Every
other module that splits a node file on `---` calls this; it is the only
boundary that survives a `---` run INSIDE a quoted YAML value or in the body
(hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-
refuses-a-held-lock-before-spawning).

node_writer.py is NOT usable as the home: node_writer imports spawn_gate,
and spawn_gate is one of the seventeen call sites, so putting the reader in
node_writer creates an import cycle. This module is that cycle's resolution —
it imports nothing but the stdlib, so every caller can import it freely.
"""

from __future__ import annotations

import re

#: A line that is exactly three dashes with optional trailing whitespace
#: (and a Windows carriage return). This is the ONLY thing that bounds the
#: frontmatter; a `---` anywhere else never splits.
_FM_LINE = re.compile(r"^---[ \t]*\r?$")


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Split `text` into `(frontmatter_text, body)`, or None when absent.

    The boundary is the LINE `---` — a line that is exactly three dashes with
    optional trailing whitespace. The first such line MUST be line 1 (the
    very first line of the file); the second such line bounds the
    frontmatter; a `---` inside a quoted scalar or later in the body never
    splits. Returns None when the shape is absent (no opening marker on line
    1, or an opening marker with no closing marker).

    `frontmatter_text` is the content between the two marker lines, safe to
    hand straight to `yaml.safe_load`; `body` is everything after the closing
    marker line. Both are newline-joined without surplus leading/trailing
    newlines.
    """
    lines = text.split("\n")
    if not lines or _FM_LINE.match(lines[0]) is None:
        return None
    close = None
    for i in range(1, len(lines)):
        if _FM_LINE.match(lines[i]) is not None:
            close = i
            break
    if close is None:
        return None
    fm_text = "\n".join(lines[1:close])
    body = "\n".join(lines[close + 1:])
    return fm_text, body


def read_frontmatter(text: str) -> dict | None:
    """`yaml.safe_load` of the frontmatter text, or None when unreadable.

    None covers both "no frontmatter" and "will not parse" — a caller that
    must NOT rewrite what it cannot read should treat None as a refusal.
    """
    import yaml

    parts = split_frontmatter(text)
    if parts is None:
        return None
    try:
        fm = yaml.safe_load(parts[0]) or {}
    except Exception:
        return None
    return fm if isinstance(fm, dict) else None
