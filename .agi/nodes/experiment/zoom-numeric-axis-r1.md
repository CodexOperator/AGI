---
id: exp:zoom-numeric-axis-r1
mint_id: e8c3b74bbe4c46e385670d1f3ab9f92c
type: experiment
parents:
  - goal:g2
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - zoom
  - g2
thought_session: season
title: Numeric zoom axis, first implementation
---
Generalized `extensions/agi/bin/zoom.py` from `--level big|small` to
`--level 1..5`. `big`/`small` still work — required by `dispatch.py`'s live
research pipeline — but as labeled legacy aliases with unchanged content, not
as thin wrappers over the new numeric levels. Added
`extensions/agi/tests/test_zoom.py` (22 tests, new file).

**Levels 1-3 (real data, filtered from the same loaded graph):**
- L1 = `type: goal` (`nodes/goal/*.md`, 21 nodes total)
- L2 = `type: idea` **and** has `unit_path` in frontmatter (`nodes/idea/
  engine-*.md`, 26 of the 27 `engine-*` files — `engine-self-decomposition`
  is the one census-shaped file without `unit_path` and is correctly
  excluded)
- L3 = `type: level3` (`nodes/level3/*.md`, 73 nodes total)

All three share one graph load (`_load_wired_graph`) and one BFS
(`_bfs_neighbors`, unchanged 2-hop `parents|children` traversal lifted
verbatim out of the old `_compose_small`) — the only thing that differs
per level is a type predicate applied after the BFS. `--target` is optional
at levels 1-3: given, it bounds to the 2-hop neighborhood filtered to that
level's type; omitted, it shows the whole census at that grain. Titles and
`unit_path`/`payload_ref` are pulled in for display via a second, header-only
frontmatter read (`_frontmatter_for`, `load_node_file(..., body=False)`) —
kept deliberately separate from graph *structure*, which stays entirely
`graph_core`'s responsibility (identity/duplicate handling in one place).

**Levels 4-5: explicit refusal, not built.** `--level 4`/`5` print a message
naming exactly what's missing (no `nodes/level4/` or `nodes/level5/`, no
generator, no contract shape for call edges or built-in resolution) and exit
1, without touching the graph at all. Level 4 would need a `level4.py`
analogous to `level3.py`, walking each level3 `payload_ref` and mining one
node per function — GitNexus's own call-graph index is a legitimate *seed*
for that per `goal:g2.1`, but nothing wires it in today. Level 5 needs level
4 first, plus resolution into third-party source that nothing in this repo
(GitNexus included) currently attempts across package boundaries.

**A fourth silent-whole-graph path, found and fixed.** `TODO.md`/prior
commits already fixed three `except` branches that fell back to
`_compose_big`. Reading the file to generalize it turned up a fourth: the
target-not-found branch in `_compose_small` did
`return _compose_big(inject_text, args).replace("## Zoom Level: BIG", "...
falling back to big")` — clearly labeled in the text, but still the entire
617-node graph handed to a kid who asked for a bounded 2-hop view. Now raises
`ZoomUnavailable` like every other failure path. `test_zoom.py` has a static
guard for exactly this defect class: `"return _compose_big" not in SOURCE`,
plus asserting there is exactly one non-`def` call site of `_compose_big(`
in the whole file (the one legitimate `--level big` branch in `main()`).

**big -> 1, small -> 3: mapping decided, then deliberately NOT wired
through.** The stderr deprecation note documents `big` as closest in spirit
to level 1 (broadest, unbounded, "pick a fresh high-level direction") and
`small` as closest to level 3 (bounded, targeted, concrete — and the level
`goal:g2.1` says to build first). But their rendered *content* is left
exactly as it was: `big` still embeds the full `INJECTION.md` (all ~617
nodes, every type), `small` still returns the full any-type 2-hop subtree.
I evaluated literally routing `small` through the level-3 filter and
rejected it: `dispatch.py`'s `_research_pipeline_targets` calls `small` with
a `hypothesis` node as `--target` on every research-pipeline iteration
(`bin/dispatch.py:277-281`) and `_pick_targets` does the same with
idea/hypothesis/experiment targets. Forcing those through a level-3
(code-file-only) filter would show a research kid an empty or near-empty
subtree around its actual target — precisely the "silently wrong grain"
failure mode this whole file exists to prevent, just moved from an
exception handler into a well-intentioned aliasing decision. Documented,
not escalated — reversible, no forbidden file, no irreversible op.

**Measured, real corpus (`/home/ubuntu/work/agi-tree`), same target
(`goal:g2`) at every level, `wc -l` on the written `context.md`:**

| level | target | nodes shown | lines |
|---|---|---|---|
| 1 | goal:g2 | 3 (goal:g2, g2.1, g2.2) | 29 |
| 2 | goal:g2 | 4 (engine-embeddings, engine-zoom, engine-agi-algos, engine-level3) | 38 |
| 3 | goal:g2 | 5 (bin-zoom + 4 embeddings/*.py files) | 37 |
| small (legacy) | goal:g2 | 7, any type | 52 |
| big (legacy) | — | whole graph | 278 |

**Negative result, reported as found rather than tuned away:** node count is
monotonic (3 < 4 < 5) but *line count is not materially larger from L2 to
L3 at a single target* (38 -> 37, i.e. flat/slightly down) — level-3 entries
render with fewer lines each (leaf nodes, no `children:` line) than level-2
entries (each idea lists 1-3 level3 `children:`). The "level N materially
smaller than N+1" property the brief predicts **does hold, cleanly, in the
unbounded case** (whole census per level, no `--target`):

| level | nodes | lines |
|---|---|---|
| 1 (no target) | 21 | 66 |
| 2 (no target) | 26 | 120 |
| 3 (no target) | 73 | 239 |

So the axis property is real at the corpus-wide grain but not guaranteed at
a single narrow target with a fixed 2-hop BFS — worth knowing before anyone
wires kid dispatch to expect it locally. A second, related asymmetry found
while measuring: depth-2 BFS reaches level-3 nodes hanging off a 1-hop idea
(`goal:g2` -> `idea:engine-zoom` -> `build:bin-zoom`, 2 hops, included) but
NOT level-3 nodes hanging off a 2-hop idea reached via a subgoal
(`goal:g2` -> `goal:g2.1` -> `idea:engine-agi-algos` -> `level3:src-agi-
algos-*`, 3 hops, excluded) — confirmed in the real L2 output above, which
shows `engine-agi-algos`/`engine-level3` at `layer=2` with their own level3
children never surfacing in the matching L3 run. Fixed-depth BFS and a
variable-length goal-chain don't compose cleanly; flagging rather than
quietly bumping the hop count to paper over it.

**Tests (`extensions/agi/tests/test_zoom.py`, 22 new):** project-root
validation, output path convention, per-level type filtering (including the
census-vs-non-census idea distinction at L2, proven with a fixture idea that
has no `unit_path`), each level's blurb text present in its own output,
unbounded whole-census listings, L4/L5 refusal (exit 1, message names the
missing pieces, graph never touched, no `context.md` written), target-not-
found refusal parametrized across L1/L2/L3/legacy-small (all four assert
`"Refusing to fall back to the whole graph"` in stderr and no `context.md`
written), a broken-sqlite-backend refusal (parent dir replaced by a file, so
`SQLiteBackend._ensure_db`'s `mkdir` raises `FileExistsError`, caught into
`ZoomUnavailable`), the static `_compose_big` call-site guard, and two tests
proving legacy `small` and numeric `1` diverge in scope on the identical
target (the actual behavior change this file makes, asserted directly
rather than assumed).

**Suite: 473 passed, 0 failed**
(`cd /home/ubuntu/work/agi && python3 -m pytest extensions/agi/tests -q`) —
the 420-passing baseline, my 22, and 31 more from a sibling KID's
`extensions/agi/bin/stitch.py` / `tests/test_stitch.py` (untracked, not
touched here; both files stayed untouched and green across every run in
this session). Also untouched: the sibling's
`agi-tree/nodes/experiment/stitch-roundtrip-r1.md` (untracked). Real-corpus
measurement runs left session artifacts at
`agi-tree/sessions/iter-9001` through `iter-9005` (agent ids prefixed
`zoom-r1-`) as evidence for the numbers above — ordinary `zoom.py` output,
not a special code path, left in place rather than cleaned up since
`sessions/` is already tracked and this is exactly what the tool is for.

**What I'd flag for a follow-up, not done here:** `skills/agi/SKILL.md`
(lines 39-40) still documents only `--level big|small` — out of scope
(not an owned file) but now stale; whoever wires L1-3 into `dispatch.py`'s
actual target-picking (`_pick_targets`/`_research_pipeline_targets`, both
currently hardcode `"big"`/`"small"`/`"auto"`) should update it in the same
pass. GitNexus's `impact`/`detect_changes` were both run before/after this
edit (repo `agi`): `impact` couldn't resolve `zoom.py` as a symbol at all
(bin/*.py has zero GitNexus symbol coverage — the exact gap `goal:g2.1`
already names), `detect_changes` reported `risk_level: low`, 0 recognized
changed symbols — consistent with that same coverage gap, not a real
all-clear signal on its own; the 473/473 suite is the actual evidence used
here.