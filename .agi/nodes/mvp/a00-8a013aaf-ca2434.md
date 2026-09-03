---
id: mvp:a00-8a013aaf-ca2434
mint_id: bb79575ace534f4bb005bb8993e61dcd
type: mvp
parents:
  - verdict:a00-52a8f13a-a156b6
confidence: 0.7
evidence_runs: 2
scaffold_hash: fbb5f68c29d733aa
title: A00 8a013aaf ca2434
verdict: inconclusive_lean_proved:70
wired_at: 1788283900
wired_from: a00-8a013aaf
---
# mvp:a00-8a013aaf-ca2434

## MVP

A single-file, dependency-free unified node reader that implements the design
the parent verdict proved: exactly three `on_error` policies, no `empty_fm`
mode, P1's sorted-first-wins dupe rule, and the two-class-raise gap closed.
It is the shape a unified `parse_node` should take. Self-contained (no
`graph_core` import) so it can be run standalone: `python3 g13-unified-read.py`.

### What it embodies (each is a verdict correction, not a guess)

1. **Three `on_error` policies** — `raise` (default), `skip` (report +
   continue), `skip_quiet` (silent drop). No fourth `empty_fm` mode: no caller
   distinguishes `fm == {}`-because-malformed from `fm == {}`-because-no-markers.
2. **`raise` is ONE class.** `yaml.YAMLError` is wrapped in `FrontmatterError`
   inside the parser, so a caller's single `except FrontmatterError` catches
   malformed-YAML nodes too. Closes the two-class gap the verdict flagged on
   P1/P3, where a bare `ParserError` escaped every `except FrontmatterError`.
3. **Non-dict YAML rejected in the parser** (a list → `FrontmatterError`), not
   allowed to slip to the caller as an uncaught `AttributeError`. Closes P3's
   fourth, unmodeled branch.
4. **Dupe rule pinned to P1's** — sorted-walk first-wins with a visible `WARN`
   and a `duplicate_ids` trail. Not P5's silent last-wins.
5. **Default for write-adjacent callers is `skip`-with-report, not `{}`+raw.**
   `{}`+raw is read-neutral but corrupts on write-back (one pass re-headers the
   node with a fresh `mint_id` and demotes its original frontmatter into the
   body) — so the safe default reports and skips.
6. **Acceptance pinned to P1's rule** — opening `---` matched after `.strip()`,
   so one leading whitespace char is accepted (P9/P10 reject it today).

### Code

```python
"""Unified node reader MVP (goal:g13). Self-contained; no graph_core import."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import sys
import yaml


class FrontmatterError(Exception):
    """Raised when a node file cannot be parsed. The ONLY failure class."""


@dataclass
class ParsedNode:
    frontmatter: dict
    body: str
    path: Path


@dataclass
class LoadReport:
    nodes: dict = field(default_factory=dict)          # id -> ParsedNode
    errors: list = field(default_factory=list)         # (path, reason)
    duplicate_ids: list = field(default_factory=list)  # (id, kept, hidden)


def parse_node(text: str) -> ParsedNode:
    """Parse node text. Raises FrontmatterError on ANY malformed shape (one class)."""
    lines = text.splitlines(keepends=False)
    # acceptance pinned to P1: strip() before compare -> one leading space ok
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing opening '---'")
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None:
        raise FrontmatterError("missing closing '---'")
    yaml_text = "\n".join(lines[1:close_idx])
    try:
        fm = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as e:
        # THE wrap: malformed YAML between valid markers -> FrontmatterError,
        # not a bare ParserError that escapes every `except FrontmatterError`.
        raise FrontmatterError(f"malformed YAML frontmatter: {e}") from e
    if not isinstance(fm, dict):
        # valid YAML that is a list -> reject here, not AttributeError at caller
        raise FrontmatterError(f"frontmatter must be a mapping, got {type(fm).__name__}")
    body_lines = lines[close_idx + 1:]
    if body_lines and body_lines[0] == "":
        body_lines = body_lines[1:]
    return ParsedNode(frontmatter=fm, body="\n".join(body_lines), path=None)


def read_node(path: Path, on_error: str = "skip", _warn=None) -> ParsedNode | None:
    """Read one file. on_error in {raise, skip, skip_quiet}."""
    text = path.read_text(encoding="utf-8")
    try:
        nf = parse_node(text)
    except FrontmatterError as e:
        if on_error == "raise":
            raise
        if on_error == "skip":
            w = _warn or (lambda m: print(f"WARN: {m}", file=sys.stderr))
            w(f"{path.name}: {e}")
        return None
    nf.path = path
    return nf


def load_directory(directory: Path, on_error: str = "skip") -> LoadReport:
    """Walk *.md recursively, sorted (deterministic). Dupe: P1's first-wins."""
    d = Path(directory)
    report = LoadReport()
    for p in sorted(d.rglob("*.md")):
        if not p.is_file():
            continue
        nf = read_node(p, on_error=on_error)
        if nf is None:
            if on_error == "skip":
                report.errors.append((p, "dropped (see WARN)"))
            continue
        nid = nf.frontmatter.get("id")
        if nid is None:
            report.nodes[f"<no-id>:{p.name}"] = nf
            continue
        if nid in report.nodes:
            kept = report.nodes[nid].path
            report.duplicate_ids.append((nid, str(kept), str(p)))
            print(f"WARN: duplicate node id {nid!r}: kept {kept}, hidden {p}",
                  file=sys.stderr)
            continue  # first-wins: later file is hidden
        report.nodes[nid] = nf
    return report
```

### Verified run (2026-09-01, corpus untouched, writes to a `tempfile` dir)

Drove the same five failure shapes the experiment used (`W` well-formed, `M1`
one marker, `M2` no markers, `M3` bad YAML, `M4` YAML-list, `M5` leading
space) plus a synthetic dupe pair. Output, abridged:

```
== T1: single-file on_error=raise is ONE class ==
  W:  parsed fm={'id': 't:ok', 'name': 'w'}
  M1: FrontmatterError: missing closing '---'
  M2: FrontmatterError: missing opening '---'
  M3: FrontmatterError: malformed YAML frontmatter: while parsing a flow sequence   <- was a bare ParserError on P1/P3
  M4: FrontmatterError: frontmatter must be a mapping, got list                   <- was uncaught AttributeError on P3
  M5: parsed fm={'id': 't5'}                                                     <- leading space accepted (P1's rule)

== T2: skip (report) vs skip_quiet (silent) vs raise ==
  M1: raise->FrontmatterError  skip->None  skip_quiet->None
  M3: raise->FrontmatterError  skip->None  skip_quiet->None

== T4: dupe rule pinned to P1 (sorted first-wins + WARN + trail) ==
  winner=aa.md pick=aa
  duplicate_ids=[('t:dup', 'aa.md', 'zz.md')]
```

Every malformed shape now raises `FrontmatterError` (one class), the dupe
winner is the sorted-first file with a warning and a `duplicate_ids` trail, and
the write-adjacent default is `skip`-with-report rather than the corrupting
`{}`+raw. The reader is the concrete target the verdict's "unified `parse_node`
needs exactly three `on_error` policies" conclusion points at.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First MVP in the g13 read-side chain. Did not design a reader from scratch;
implemented exactly the design the parent verdict proved, so every design
decision in the code is a verdict line, not a new choice: three policies (no
empty_fm), the yaml.YAMLError->FrontmatterError wrap that closes the two-class
raise gap, the in-parser non-dict check that closes P3's 4th branch, P1's
sorted-first-wins dupe rule, and skip-with-report (not {}+raw) as the
write-adjacent default. Kept it dependency-free and self-contained so the
proof runs without touching the tree. This is the node a unified parse_node
would land as once it is adopted; it does not yet replace any caller.
<!-- THOUGHT:END -->

## Inputs

- `parse_node(text)` — raw node file text (the `---\nYAML\n---\nbody` shape).
- `read_node(path, on_error="skip")` — one `.md` file path and a policy in
  `{raise, skip, skip_quiet}`.
- `load_directory(directory, on_error="skip")` — a directory tree to walk
  (sorted, recursive `*.md`).

## Outputs

- `ParsedNode(frontmatter, body, path)` for a well-formed file.
- `None` under `skip`/`skip_quiet` for a malformed file (with a `WARN` under
  `skip`); a raised `FrontmatterError` under `raise`.
- `LoadReport` from `load_directory`: `nodes` (id -> ParsedNode, first-wins on
  dupe), `errors` (dropped files under `skip`), and `duplicate_ids`
  (`(id, kept_path, hidden_path)` per collision).

## Caveat

Prototype, not yet wired to any caller. It hard-codes the `.md`/`---` shape and
the `id` key for dupe detection; the real `parse_node` must also cover the
`.json` shape `graph_core` already accepts, and must be adopted at the bulk
readers (P1/P5) before the ten-parser divergence actually collapses. The MVP
proves the reader's semantics, not its integration.



## Agent Notes
Unified parse_node MVP: 3 on_error policies, yaml->FrontmatterError wrap (closes 2-class raise), in-parser non-dict check (closes P3 4th branch), P1 sorted-first-wins dupe rule, skip-with-report default. Ran clean over 5 shapes + dupe.