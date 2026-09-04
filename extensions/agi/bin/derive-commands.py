#!/usr/bin/env python3
"""derive-commands.py — replace prose command tables with content from the node.

`goal:g1.10`. The four prose copies (SKILL.md, CLAUDE.md, QUICKSTART.md,
HANDOFF.md) listed commands independently, all drifting from the declared
source in `.geometry/commands.md`. This script replaces marker-guarded regions
in any prose file with the rendered command table, so the prose derives from
the node rather than restating it.

Usage:
    python3 bin/derive-commands.py [--files FILE...]
    python3 bin/derive-commands.py --all    # all marker-bearing files
    python3 bin/derive-commands.py --check  # exit 1 if any file would change

The declarer — `render_for_injection` in `commands.py` — already produces one
format (bullet-list by workflow). The prose files use a table format (| Command
| Does |). This script bridges that gap by producing both formats and choosing
the one the target file already uses.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── resolve project root ──────────────────────────────────────────────
# Same strategy as every other engine script: nearest enclosing `.agi/`.
_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))
sys.path.insert(0, str(_THIS.parent / "src"))
import locations as _loc  # noqa: E402

# ── markers ───────────────────────────────────────────────────────────
MARKER_BEGIN = "<!-- COMMANDS:BEGIN -->"
MARKER_END = "<!-- COMMANDS:END -->"
MARKER_PATTERN = re.compile(
    re.escape(MARKER_BEGIN) + r".*?" + re.escape(MARKER_END),
    re.DOTALL,
)

# ── prose files known to carry command tables ─────────────────────────
# Relative to the project root (where `.agi/` lives).
DEFAULT_FILES = [
    "../skills/agi/SKILL.md",  # skills/agi/SKILL.md — the biggest table
    "../CLAUDE.md",            # repo root CLAUDE.md — scattered mentions
    "../QUICKSTART.md",        # repo root QUICKSTART.md — verification cmds
]


def _render_table(root: Path) -> str | None:
    """The declared commands as a markdown table (SKILL.md format)."""
    import commands as _cmds  # noqa: E402

    table = _cmds.load(root)
    if not table:
        return None
    flows = _cmds.workflows(root)

    # Build a table row for each workflow, in order
    lines = [
        "<!-- This section is AUTO-GENERATED from `.geometry/commands.md`.",
        "     Edit the node — never this table directly. -->",
        "",
        "| Command | Does |",
        "|---|---|",
    ]
    seen: set[str] = set()
    for _flow_name, names in flows.items():
        for n in names:
            if n not in table:
                continue
            seen.add(n)
            cmd = table[n]
            lines.append(f"| `{cmd.shell(placeholders=True)}` | {cmd.about} |")
    # Unassigned commands (no workflow)
    loose = [c for n, c in sorted(table.items()) if n not in seen]
    for cmd in loose:
        lines.append(f"| `{cmd.shell(placeholders=True)}` | {cmd.about} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--files", nargs="*", default=None,
                    help="prose files to patch (default: SKILL.md)")
    ap.add_argument("--all", action="store_true",
                    help="patch all known command-bearing files")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any file would change, without writing")
    args = ap.parse_args(argv)

    root = _loc.find_project_root(Path.cwd())
    if root is None:
        print("ERR: not an agi project", file=sys.stderr)
        return 1

    if args.all:
        targets = list(DEFAULT_FILES)
    elif args.files:
        targets = list(args.files)
    else:
        targets = DEFAULT_FILES[:1]  # SKILL.md by default

    table = _render_table(root)
    if table is None:
        print("no commands declared — nothing to derive")
        return 0

    changed = 0
    for rel in targets:
        fp = (root / rel).resolve()
        if not fp.is_file():
            print(f"skip: {rel} not found")
            continue

        text = fp.read_text(encoding="utf-8")
        replacement = f"{MARKER_BEGIN}\n{table}\n{MARKER_END}"
        if MARKER_BEGIN in text:
            new_text = MARKER_PATTERN.sub(replacement, text, count=1)
        else:
            # No markers yet — inject at end
            new_text = text + f"\n\n{replacement}\n"

        if new_text == text:
            continue
        if args.check:
            print(f"would change: {rel}")
            changed += 1
        else:
            fp.write_text(new_text, encoding="utf-8")
            print(f"patched: {rel}")
            changed += 1

    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())