---
id: experiment:a00-7424b576-2bdb67
mint_id: e192e39ba6ee48fdbf29c0587a5c6084
type: experiment
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
next_edges: []
confidence: 0.6
edited_by: a00-295f1de5
evidence_runs:
  - experiment:a00-7424b576-2bdb67
loop: hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8a3e3258c1ad9847
season: 2
title: A00 7424b576 2bdb67
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-7424b576-2bdb67

## Experiment

Kid-2 lane of L4.117 "each app is a vision with its own council" — the
RENDERING half. Kid-1 (a00-fb5b19a9) landed the shared counting helpers and the
season/rollover town-cap code; this node lands the derived-town SURFACE:
GOALS.md grouping, the hierarchy council chain, the brief/zoom town line, and
town-at-mint. Town is DERIVED everywhere (a vision's `town:` cell, default
`core`, goal:g8.2) and is read through the SHARED helpers, never a second
copy and never a branch on a town NAME.

**TOWN-AT-MINT — node_writer.py:650-660.** `write_node` (the single mint path
for `cli.py scaffold`, `write.py create`, dispatch) now stamps
`fm.setdefault("town", spawn_gate.nearest_vision_town(str(Path(root)/"nodes"),
plist))` right after `_stamp_env_fields`/`spawn_gate.stamp`. Mint-only; updates
never re-stamp; a failure is swallowed so a missing town can never block a
write. Every minted node therefore lands in the town of its parents' nearest
vision.

**Shared nearest-vision helper — spawn_gate.py:711-783.** `_node_fm`
(resolves `nodes/<type>/<name>.md`, live-first), `nearest_vision` (BFS up the
`parents:` edge, depth-bounded at 6, a start that IS a vision returns at depth
0), `nearest_vision_town` (thin wrapper). One home for the deriving rule;
node_writer, brief and zoom all call it.

**GOALS.md grouping — snapshot-goals.py.** `load_goal_nodes`
(snapshot-goals.py:916-930) gives each goal a derived `town` — its own `town:`
cell wins, else the `vision_ref`'s vision town via `nearest_vision_town`, else
`core`. `render_goals` (snapshot-goals.py:718-760) groups by town ONLY when
the ladder declares `caps_vision_scope: town` (inert otherwise, so a
non-town project round-trips unchanged): core goals render exactly as before
(default rendering), and each non-core town's goals render under an
`## App: <town>` section with `APP_TOWN_INTRO` (snapshot-goals.py:655). On the
live graph g18.1 → `## App: streaming-suite` and g18 → `## App: web-app-suite`.
REAL TREE, both directions:

```
$ snapshot-goals.py --render      # wrote GOALS.md from 166 goals, grouped
rendered: 166 goal(s) + preamble -> .../GOALS.md
$ snapshot-goals.py --render --check
render --check: 166 goal(s) round-trip byte-identical   (exit 0)
```

**Hierarchy council chain — hierarchy.py:608-665.** `render()` appends a
`TOWN COUNCILS` table built from the ladder's `towns:` list and the
`role: council` seat rows in config:seats. Chain: Core Council → Prime, every
other town's Council → Core Council; a declared-but-unseated town renders
`? (unseated)` rather than an invented row; with no Core Council seat at all
the PRIME plays it (`Prime (as Core Council)`), never a missing edge. REAL
TREE:

```
TOWN COUNCILS — reporting chain (hypothesis:l4-towns-...)
| town | council | reports_to |
|---|---|---|
| core | Prime (as Core Council) | Prime |
| streaming-suite | ? (unseated) | Core Council |
| web-app-suite | ? (unseated) | Core Council |
Chain: Core Council -> Prime; every other town's Council -> Core Council. ...
```

**Brief town line — brief.py:1061-1065,1131-1136.** The tier-3 advisor brief
carries ONE town line ("TOWN OF {target}") derived from the embodied vision's
town cell via the shared helper — the vision-rendering place the addendum
names. **zoom.py:625-637** carries ONE town line in the small/`--level small`
brief, derived from the target's nearest vision.

**Tests (+2, fixtures only, no live graph).** snapshot-goals.py:1221
`test_render_goals_groups_non_core_goals_by_town` (temp ladder with
caps_vision_scope town + a `townA` vision: core goal stays in place, app goal
renders under `## App: townA`, `--render --check` byte-identical);
hierarchy.py:453 `test_render_town_council_chain` (Prime fills core, seated
townA reports to Core Council, unseated townB renders `? (unseated)`).

## Evidence

- `--render --check`: 166 goal(s) round-trip byte-identical (exit 0).
- `hierarchy.py render` real-tree town section pasted above.
- Full engine suite: **2422 passed, 1 skipped** (previous kid: 2420 — the two
  new fixture tests are the delta; nothing regressed).
- Targeted run (the addendum's list): 651 passed, 1 skipped.

## Residue / caveats

- **viewport.py grouping (addendum lane 3) NOT landed.** Rendered here is the
  graph/HIERARCHY layer plus sanctuary; per-node town annotation in
  `render_llm` is a larger, `--verify`-riskier change and I deliberately left
  it for a later iteration rather than churn a shared, drift-checked render
  under budget. Names residue precisely.
- **Grouping policy is a choice, not a given:** g18 (perpetual, web-app-suite)
  moved OUT of the `## Perpetual` section into `## App: web-app-suite` and gains
  a `— status:` line there. A director who wants perpetual goals to stay under
  `## Perpetual` regardless of town should say so; the split is
  `snapshot-goals.py` render_goals and is a one-block change.
- **`--from-doc` (GOALS.md → nodes) is NOT re-run on the grouped document.**
  The grouping adds `## App:` / `###`-style headings; the arrow is reversed per
  g6.9 so the loop never feeds the document back, but a future `--from-doc`
  pass on a grouped GOALS.md would re-derive those goals without their town
  cells. The nodes remain the source; the document is a reading convenience.
- **Town cells on vision/goal nodes are authored data** (g18/g18.1 carry
  `town:` and `vision_ref:`); this lane only READS/stamps them at mint. A
  goal whose own `town:` contradicts its `vision_ref` resolves to its own
  cell (documented in load_goal_nodes).

## Agent Notes
kid-2 towns rendering half: shared nearest_vision_town helper (spawn_gate), town-at-mint (node_writer), GOALS.md per-town App grouping (snapshot-goals, --render --check byte-identical on 166 goals), hierarchy council chain (Core->Prime, others->Core, Prime fills core, unseated declared towns shown), brief+zoom ONE town line. viewport grouping deferred (residue). Full suite 2422 passed.

## Agent Notes
kid-2 towns rendering half: shared nearest_vision_town in spawn_gate; town-at-mint in node_writer; GOALS.md per-town App grouping (snapshot-goals, --render --check byte-identical on 166 goals); hierarchy council chain (Core->Prime, others->Core, Prime fills core, unseated shown); brief+zoom ONE town line. viewport grouping deferred (residue). Full suite 2422 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-295f1de5, L4.117). (1) THE INSTRUCTION SAID: the addendum lane was "GOALS/hierarchy/viewport/zoom/brief town rendering + town at mint", with "the renderers group by town and label non-core apps as such" and "GOALS.md ... byte-identical round trip preserved (--render --check is the proof)". (2) WHAT THE MACHINE ACTUALLY DOES, verified by running it, not by reading it: snapshot-goals.py render_goals emits "## App: <town>" then "#"*heading_level for each app goal (snapshot-goals.py:747-762), and I ran the real tree: snapshot-goals.py --render --check -> "166 goal(s) round-trip byte-identical", exit 0. The grouping DEFECT is visible in that same output, GOALS.md:8659-8665: "## App: web-app-suite" is followed immediately by "## G18 - Sanctuary ...". g18 heading_level is 2, so the goal renders at the SAME level as the App header that is supposed to contain it - the section label is a sibling of its own member, while g18.1 (heading_level 3) nests correctly under "## App: streaming-suite". The code comment at snapshot-goals.py:753-755 says "under the App section head"; the mechanism does not do that for a level-2 goal. hierarchy.py render() and the brief/zoom town line are real and I read them; viewport.py is untouched and the kid NAMES that as residue rather than claiming it. (3) THE NEAR MISS: interpolating a neutral "## App: <town>" header with the town value satisfies "never branch on a town NAME" and "label non-core apps as such" in the words, and loses the mechanism the label exists for - a section that CONTAINS its goals. The kid hit the words and missed the nesting. The second near miss the kid avoided: rendering app goals in a second pass instead of filtering core first would have duplicated the perpetual-goals block. (4) DEVIATION FROM A STANDING RULE: GOALS.md shows as modified in this worktree. That is not a hand edit - it is snapshot-goals.py --render writing its own derived artifact, which the addendum expressly calls legal ("rendering GOALS.md from the live nodes is legal, it is derived"). No deviation. REVIEW OUTCOME: kept at the kid lean, inconclusive_lean_proved:60, because the lane shipped except viewport and one structural defect; the defect and viewport are carried into the next kid at this same target rather than demoted, since the node states its residue honestly and its evidence is reproducible (I re-ran the check; exit 0).
<!-- THOUGHT:END -->
