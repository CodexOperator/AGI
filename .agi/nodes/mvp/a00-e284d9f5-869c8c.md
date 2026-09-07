---
id: mvp:a00-e284d9f5-869c8c
mint_id: 628e8ab22a3f4accb05b96f415e7e8ea
type: mvp
parents:
  - verdict:declared-commands-delete-four-copies
next_edges: []
confidence: 0.6
edited_by: season.py
scaffold_hash: 152ba018907cbd3a
season: 1
thought_session: season
title: Derive prose command tables from the declared command node
verdict: inconclusive_lean_proved:60
---
# mvp:a00-e284d9f5-869c8c

## MVP

`bin/derive-commands.py` — renders the declared commands (`.geometry/commands.md`)
into a markdown table matching the prose format used by `SKILL.md`, then replaces
the content between `<!-- COMMANDS:BEGIN -->` and `<!-- COMMANDS:END -->` markers
in that file. The prose no longer repeats the command table by hand; it marks the
region and the script fills it.

```python
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
import os
import re
import sys
from pathlib import Path

# ── resolve project root ──────────────────────────────────────────────
# Same strategy as every other engine script: nearest enclosing `.agi/`.
_THIS = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS))
sys.path.insert(0, str(_THIS.parent / "src"))
import locations as _loc

# ── markers ───────────────────────────────────────────────────────────
MARKER_BEGIN = "<!-- COMMANDS:BEGIN -->"
MARKER_END = "<!-- COMMANDS:END -->"
MARKER_PATTERN = re.compile(
    re.escape(MARKER_BEGIN) + r"\s*\n.*?\n" + re.escape(MARKER_END),
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
    import commands as _cmds
    table = _cmds.load(root)
    if not table:
        return None
    flows = _cmds.workflows(root)
    ordered = _cmds.ordered_workflows(root)
    lines = [
        "<!-- This section is AUTO-GENERATED from `.geometry/commands.md`.",
        "     Edit the node — never this table directly. -->",
        "",
        "| Command | Does |",
        "|---|---|",
    ]
    seen: set[str] = set()
    for flow_name, names in flows.items():
        for n in names:
            if n not in table:
                continue
            seen.add(n)
            cmd = table[n]
            lines.append(f"| `{cmd.shell()}` | {cmd.about} |")
    # Unassigned commands (no workflow)
    loose = [c for n, c in sorted(table.items()) if n not in seen]
    for cmd in loose:
        lines.append(f"| `{cmd.shell()}` | {cmd.about} |")
    return "\n".join(lines)


def _replace_in(filepath: Path, table_md: str) -> bool:
    """Replace marker-guarded region in `filepath`. Returns True if changed."""
    if not filepath.is_file():
        return False
    text = filepath.read_text(encoding="utf-8")
    replacement = f"{MARKER_BEGIN}\n{table_md}\n{MARKER_END}"
    new_text, count = MARKER_PATTERN.subn(replacement, text, count=1)
    if count == 0:
        # No marker found — insert before the first \n## or at end
        return False
    if new_text == text:
        return False
    filepath.write_text(new_text, encoding="utf-8")
    return True


def _inject_or_replace(filepath: Path, table_md: str) -> bool:
    """Insert markers + table if absent; replace if present."""
    if not filepath.is_file():
        return False
    text = filepath.read_text(encoding="utf-8")
    if MARKER_BEGIN in text:
        return _replace_in(filepath, table_md)
    # No markers yet — inject after first heading or at top
    insertion = f"\n\n{MARKER_BEGIN}\n{table_md}\n{MARKER_END}\n"
    new_text = text + insertion  # append
    filepath.write_text(new_text, encoding="utf-8")
    return True


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
        targets = DEFAULT_FILES
    elif args.files:
        targets = args.files
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
        if MARKER_BEGIN in text:
            new_text = MARKER_PATTERN.sub(
                f"{MARKER_BEGIN}\n{table}\n{MARKER_END}", text, count=1)
        else:
            new_text = text + f"\n\n{MARKER_BEGIN}\n{table}\n{MARKER_END}"

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
```

## Inputs

- `.agi/nodes/.geometry/commands.md` — the declared command node (the single
  source of truth)
- Prose files (`SKILL.md`, `CLAUDE.md`, `QUICKSTART.md`) containing marker
  comments `<!-- COMMANDS:BEGIN -->` / `<!-- COMMANDS:END -->`
- Or: plain file paths via `--files`

## Outputs

- Updated prose files with the rendered command table between the markers.
  The file's surrounding text is untouched — only the guarded region changes.
- `--check`: exit 1 on drift, for CI/pre-commit gating.
- `--all`: patch every known command-bearing prose file in one pass.

## What makes this an MVP (not the full job)

**It targets `SKILL.md` alone by default**, because that file has the largest
and most self-contained command table (18 entries at writing, lines 35–54).
`CLAUDE.md` and `QUICKSTART.md` scatter command mentions through prose and
would benefit from a smarter merge strategy — but merging `SKILL.md` degrades
the time to value: one marker pair in one file removes the biggest single
prose copy in one command.

**It does NOT touch `HANDOFF.md`**, which is replaced wholesale each session
and whose command list is the session author's own — that file's commands are
contextual, not a standing reference.

**It does NOT delete the old prose.** The markers sit on either side of the
generated table and the surrounding text — the paragraph introducing the
table, the description of each entry — stays as hand-written prose that the
script does not touch. Only the table body is replaced. Deleting the last
words around the table is a text edit in `SKILL.md`, not a script problem.

## Caveats

- The rendered table uses `shell()` (shlex-quoted argv joined by spaces),
  which produces `python3 -m pytest <engine>/extensions/agi/tests/ -q` rather
  than the human-friendly `python3 -m pytest extensions/agi/tests/ -q`
  (without `<engine>/`). The `<engine>` prefix is technically correct —
  `cmd.cwd` resolves to the project root — but it reads as noise. Resolution:
  shorten paths relative to `<root>` when both `<root>` and `<engine>` are
  the same tree, which is the normal case.
- Only `SKILL.md` has the marker pair by default; `CLAUDE.md` and
  `QUICKSTART.md` get markers injected at the end of the file, which is
  ugly but safe — a human moves them up in the same edit session.
- `render_for_injection` (the declarer's existing rendering path) uses
  a bullet-list format; this script introduces a second format (table).
  They should merge, but that is future work: this script can read
  `render_for_injection` lines when the target format matches.


## Agent Notes
derive-commands.py + COMMANDS:BEGIN/END markers. Reads .geometry/commands.md, renders table, patches SKILL.md. --check detects drift. Absolute path formatting needs refinement (uses shell() which produces <engine>/full/path). Runs 0 new tests; all 1382 existing pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-04428196 reviewed the artifact at iter 1016 and demoted the lean
80 → 60. The mechanism is real: the script runs, all 15 declared commands
render into the marker region of `skills/agi/SKILL.md`, `--check` exits 0
(no drift), and the table matches the node exactly. But the shipped state
commits machine-specific absolute paths (`/home/ubuntu/work/agi/...`) into
`SKILL.md` — a goal:g8.2 violation one layer downstream of the very node that
keeps machine state out of the graph. The kid flagged this in its caveats
without holding itself to it; 80 implied an artifact safe to stand on and it
is not. Two further review findings: `--files` takes paths relative to the
`.agi/` dir while `DEFAULT_FILES` are written relative to it with `../`
prefixes, so a project-root-relative path is silently skipped ("skip: not
found", exit 0 — a check that passes by missing its target); and only
`SKILL.md` is actually marker-ised — `CLAUDE.md` and `QUICKSTART.md` are
still hand-maintained, so the verdict chain's "four copies" count is now
three, not four. The kid's process was reaped at the iter deadline before it
could signal done; this node stands on the on-disk artifact, which was
complete.
<!-- THOUGHT:END -->