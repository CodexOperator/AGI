#!/usr/bin/env python3
"""SD.06 experiment a00-e6925346-673328 part 2: scaling regime.
Test the hypothesis's claim in the regime where it bites -- a wide
column-aligned box table (the node's own command-table shape, ~9 rows)
vs the same 9 commands as an indented list. Big tables = many border glyphs.
"""
import tiktoken
enc = tiktoken.get_encoding("o200k_base")

CMDS = [
    ("smoke", "snapshot+render+metrics, no dispatch"),
    ("pytest", "engine's test suite"),
    ("goals --check", "GOALS.md and goal nodes byte-identical"),
    ("viewport --verify", "one render, two readers"),
    ("grid commit --all", "version every changed node+payload"),
    ("links links", "every link resolves; 0 broken"),
    ("links schema", "nodes violating type required list"),
    ("spawn_budget status", "live agents vs tree-wide bound"),
    ("envfile --check", "required keys present, forbidden absent"),
]

BOX = "  +----------------+---------------------------------+\n"
BOX += "  | cmd            | does                            |\n"
BOX += "  +----------------+---------------------------------+\n"
for c, d in CMDS:
    BOX += f"  | {c:<14} | {d:<31} |\n"
BOX += "  +----------------+---------------------------------+"

INDENT = "commands\n"
for c, d in CMDS:
    INDENT += f"  {c}  {d}\n"

for name, text in [("BOX_TABLE", BOX), ("INDENT_LIST", INDENT)]:
    n = len(enc.encode(text))
    glyphs = sum(1 for ch in text if ch in "+-|")
    print(f"{name:11s} {n:5d} tok  ({len(text):5d} B)  border-glyphs={glyphs}")