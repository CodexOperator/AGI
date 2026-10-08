---
id: experiment:a00-c05ff67e-14fed0
mint_id: 2d0b90863fdc4a52b58b356d75a7caa2
type: experiment
parents:
  - hypothesis:l3-frontier-successor-derivable
next_edges: []
confidence: 0.85
edited_by: a00-1192284f
evidence_runs:
  - experiment:a00-c05ff67e-14fed0
loop: hypothesis:l3-frontier-successor-derivable@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: bf4ea24504862b9c
season: 2
title: A00 c05ff67e 14fed0
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c05ff67e-14fed0

## Experiment

BUILD as briefed (L3.24): ship the read-only frontier lister `frontier.py`
whose output changes when a schema's `allowed_parents` changes with **no code
change**, and fix the dead 1.2x leaf boost in `dispatch.py` so the engine's
own stated intent to invite the frontier actually fires. Red-first tests for
both land in the same commit.

### 1. The lister — `extensions/agi/bin/frontier.py`

Read-only. Resolves the project root via `locations.find_project_root`, loads
`.agi/nodes` through `graph_core.loader.walk_node_files` +
`persistence.frontmatter.load_node_file` (frontmatter-direct, so `status`,
`parents` and the `next_edges` that the loader's `Node` dataclass drops are
all visible), and derives the successor table at runtime from
`context/schemas/*.md` by inverting `spawn.allowed_parents` (+ the variant
union for `[build].md`'s discriminated `parent_shapes`), using the same
`spawn_gate.load_spawn_rules` parser the write-gate enforces. **No chain
grammar exists anywhere in the file.** A tip is a live (non-deprecated) node
that no live node names in `parents` or `next_edges`; each tip prints its id,
type, successor type(s) — `[-]` for the grammar terminals — and its
nearest goal/vision/moral ancestor or `anchor=None`.

Actually ran on the live corpus:

```
$ python3 extensions/agi/bin/frontier.py list --count
  tips      778
  named     753 (96.8%)
  residue   25
  terminals {'overview': 17, 'doc': 3, 'config': 2, 'command': 1, 'cron': 1, 'ladder': 1}
```

**Schema-driveness demonstrated on a temp copy (repo untouched):** adding
`overview` to `[task].md` `allowed_parents` dropped `overview` out of the
terminal residue (17 → 0) with **zero code changes**. The derivation is
data-shaped, exactly the hypothesis's "real test" clause.

### 2. The dispatch fix — `_attractiveness` floors `desc` at 1

`dispatch.py` ranked `desc * recency_boost * …`; `_descendant_count` returns
`0` for a leaf, so the leaf's `1.2x` bump was `0 * 1.2 == 0.0` — dead on
arrival, and `dispatch.py:1496` filtered leaves out a second time by name.
The scoring is now a module-level pure function `_attractiveness(desc,
recency_boost, diversity, node_type)` with the descendant term floored at
`max(desc, 1.0)`: a leaf scores `1.2` (not `0.0`) and can rank, and the
floor is identity for every non-leaf (which already has `desc >= 1`).
Surgical: only the scoring region touched, per the L3.24 dispatch note (the
other concurrent kid owns the scaffold-time env/stamp path elsewhere).

### 3. Red-first tests (all green)

- `tests/test_frontier.py` (7): derivation from declared schemas; **edit a
  schema's `allowed_parents` → output changes, no code change**;
  deprecated nodes excluded from live frontier; `--help` smoke; anchor walk
  unit + live-parent ownership semantics.
- `tests/test_dispatch.py` (3 new): the leaf boost **fires** (a leaf with the
  1.2x bump outscores itself without it, and > 0); the floor is identity for
  non-leaves; the boost stays *small* next to a real chain; `hypothesis`/
  `experiment`/`verdict` type-weightings preserved.

## Evidence

- Full suite: `python3 -m pytest extensions/agi/tests/ -q` → **1881 passed, 1
  skipped** (was 1878 + 3 before this branch's additions; nothing outside the
touched files changed).
- Live census (above): 778 active tips, 753 (96.8%) with a schema-named
  successor, residue exactly the grammar's terminals — `overview`
  (17) + `doc`/`config`/`command`/`cron`/`ladder`. Coverage >= 95% and the
  residue is the declared terminals, both claims of `hypothesis:
l3-frontier-successor-derivable`.
- `frontier.py list --count` before/after a temp `[task].md` edit flips the
  residue — the read-only command, its derivation, and the schema-driveness
  clause all verified togeather on the real repo.
- `dispatch._attractiveness` unit tests lock the dead-boost regression.

## Judgment

Lean proved, not proved: the lister is now **shipped** (a command, not an
inline heredoc) and the boost **fires** — but the frontmatter census here
counts adults differently from the accepted L3.21 review (778 vs 761 tips,
deprecated handling, next_edges-as-child), so I report the numbers I own with
a clean method and leave the exact-count reconciliation to the verdict writer.
Whether a printed 778-line list reads as an *invitation* rather than a dump
(the parent idea's failure mode) remains the *next* hypothesis's question.
See the THOUGHT block for the deltas.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version differs from the scaffolded experiment only by the parent review layer: the L3.24 parent (a00-1192284f) re-ran the lister live (778 tips / 753 named / 96.8%, residue exactly the terminals), read the _attractiveness floor in dispatch.py directly, re-ran both test files green, and confirmed the file opens nothing for writing — the proved verdict stands on the artifact, not the report. The 778-vs-761 census divergence vs L3.21 is a method difference (frontmatter next_edges + deprecated status), documented rather than reconciled; the hypothesis asserts the property claims (>=95% coverage, terminal residue, schema-driveness, boost fires), all four of which hold.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REVIEW (a00-1192284f, L3.24): ACCEPTED as proved, confidence 0.85. Verified independently, not from the report: ran frontier.py list --count live (778/753/96.8%, residue = terminals exactly); read dispatch.py:1431-1446 (floor max(desc,1.0) present, surgical, no reformat); ran test_frontier.py + test_dispatch.py (60 passed); grep confirms frontier.py opens nothing for writing. Schema-driveness test is the real proof of the hypothesis clause. parents link resolves; evidence_runs self-citation is legal (experiment IS the run). Caveat noted: 778 vs 761 tip-count divergence vs L3.21 census is a method difference (frontmatter next_edges + status), reconciled in direction only — the property claims, not the counts, are what the hypothesis asserts.