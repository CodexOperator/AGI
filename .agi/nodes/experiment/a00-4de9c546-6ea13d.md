---
id: experiment:a00-4de9c546-6ea13d
mint_id: bb67e0a3e42b48e8b51daf015469b3ef
type: experiment
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
next_edges: []
confidence: 0.75
edited_by: a00-295f1de5
evidence_runs:
  - experiment:a00-4de9c546-6ea13d
loop: hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 785a95903306db06
season: 2
title: Fix snapshot-goals App/goal nesting; viewport town annotate; no-literal-town test; merge-up town gate
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-4de9c546-6ea13d

## Experiment

L4.117's rendering-half kid 3 (this node), the "DEAL WITH THE RESIDUE" lane of
`hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council` (town at mint
+ per-town render + council chain + viewport residue). I fixed the one defect
the parent review named, landed the deferred viewport town annotation, the
no-literal-town test, and the merge-up town gate. Four changes, each with its
fixture proof:

**(1) snapshot-goals nesting defect — the point of this kid.** The parent
review found that `render_goals` emitted the `## App: <town>` head and then
`"#" * heading_level` per app goal, so a ROOT goal (heading_level 2) collided
at the SAME `##` level as the App head that was meant to contain it — real
tree GOALS.md:8659-8665 had `## App: web-app-suite` immediately followed by
`## G18 — Sanctuary ...`, sibling of its own member; g18.1 nested only by
accident. Fixed in `extensions/agi/bin/snapshot-goals.py` (the app-goal loop
at what is now :752-766): the app block now renders `"#" * (heading_level + 1)`
— exactly what the Perpetual block already did. Real tree after the fix,
`## App: streaming-suite` is followed by `#### G18.1 ...` and
`## App: web-app-suite` by `### G18 ...` (verified at GOALS.md:8654/8665).
Before the fix `--render --check` reported MISMATCH on the two app goals;
after, byte-identical. New fixture test
`test_render_town_goal_nests_strictly_below_the_app_head`
(extensions/agi/tests/test_snapshot_goals.py) asserts a root (level 2) and a
subgoal (level 3) both render with STRICTLY more `#` than the App head — a
test of nesting, not of words.

**(2) viewport town annotation — the residue kid 2 named.** `frame_stream`
now takes an optional `nodes_dir` and, per node, derives the town through the
SAME shared helper (`spawn_gate.nearest_vision_town`) that node_writer, brief
and zoom use — never a second copy of the deriving rule, never a branch on a
town NAME (goal:g8.2). The `Frame` dataclass gains a `town` field and both
formatters (human + llm) annotate it as `[town: X]` / `town=X` when non-core.
Memoized per node_id (`_town_cache`) so a 2066-node graph only pays the BFS
once per node actually in view. `main()` threads `nodes_dir=str(root/nodes)`.
`--verify` stays green (the load-bearing proof):
```
frames in slice: 40   human lines: 43   llm ids: 40   briefing: yes
PASS — one stream, two formatters, same nodes in the same order   (exit 0)
```
New fixture test `test_town_is_derived_via_the_shared_helper_from_the_frame`
(test_viewport.py): a goal whose parent is a vision with `town: townA`
renders `town == "townA"`; with no nodes_dir the annotation is `""`, never
guessed.

**(3) the no-literal-town test.** New `extensions/agi/tests/test_no_literal_town.py`.
It DERIVES the town list from the ladder node (`spawn_gate._read_frontmatter`
of `.geometry/ladder.md`, `towns:` list, excluding the reserved `core`
denominator), then AST-parses every `bin/*.py` engine script and fails on any
non-core town appearing as a runnable string literal — the falsifier for
goal:g8.2. It excludes the reserved `core` default on purpose: defaulting to
core is designed behaviour, branching on an APP name is the defect (the
docstring says so). Comments and docstrings are excluded by construction: the
AST does not surface comments, and `Expr`/`Constant` docstring heads are
skipped — prose that merely names an app (like this hypothesis) is fine, a
runnable literal is not. Passes today (no app-name literals in engine code).
Sanity-checked non-vacuous: an injected `return t == "web-app-suite"`
is caught; a docstring/comment mentioning it is not.

**(4) the merge-up town gate — season.py.** `cmd_merge_up` (season.py, gate
fired before any git write) now enforces: a round merges up through the seat
of the town that ORIGINATED it. Two OPTIONAL args, `--round <node-id>` and
`--seat <seat-name>`, resolve the round's `town:` cell (read from its node
file; default core) and the seat's `town` cell (from config:seats via the
shared `read_seat_registry`); a mismatch is REFUSED with both towns printed,
before any git operation. Fail-open: if neither arg is given, or either half
is unknowable, or the towns agree, the merge proceeds exactly as before — so
a graph that never declared towns is byte-for-byte untouched. Fixture proof
`test_merge_up_town_gate_refuses_cross_town_and_allows_same_town`
(test_season.py): a temp graph with two council seats (config:seats rows
carrying `town:` cells: council-streaming→streaming-suite, council-web→
web-app-suite) and a round `experiment:round` stamped `town: streaming-suite`.
Cross-town (`--seat council-web`) is refused (return 1, stderr names both
towns, nothing merged); same-town (`--seat council-streaming`) merges green
and removes the worktree. Proven entirely on fixtures/config:seats copies —
the real `.agi/nodes/.geometry/seats.md` was untouched.

## Evidence

- `snapshot-goals.py --render --check`:
  ```
  render --check: 166 goal(s) round-trip byte-identical   (exit 0)
  ```
  (Both real GOALS.md app-sections now nest: `## App: web-app-suite` →
  `### G18`, `## App: streaming-suite` → `#### G18.1`.)
- `viewport.py --verify`: PASS (exit 0) — quoted above.
- Targeted batch (the assignment's list + test_no_literal_town):
  **655 passed, 1 skipped**. Full engine suite: **2658 passed, 1 skipped**
  (`python3 -m pytest extensions/agi/tests/ -q -k test_`).

## Residue / caveats

- **viewport town annotation only resolves nodes reachable via `parents:`.** The
  shared helper `nearest_vision_town` walks the `parents:` edge, so a goal that
  carries its town on `town:`+`vision_ref:` (g18, g18.1) but no `parents:` link
  resolves to `core` in the viewport annotation, even though snapshot-goals
  (which reads `vision_ref`) shows it correctly. I deliberately did NOT write a
  second town-resolution rule in viewport ("never a second copy" was the lane) —
  the honest residue is that the shared helper's `parents:`-only walk under-
  covers `vision_ref`-tagged goals. A follow-up could teach `nearest_vision` to
  follow `vision_ref` too, or snapshot-goals' `load_goal_nodes` already has the
  `town:`-cell-wins logic.
- **merge-up gate is opt-in by flag.** `--round`/`--seat` must be passed; the
  director call-site (dispatch.py, which I MUST NOT touch this round) does not
  pass them yet, so the gate is proven but not yet wired into the live spawn →
  merge cycle. The wire-up is a named follow-up, not claimed here.
- GOALS.md in this worktree differs from the shared branch — that is
  `snapshot-goals.py --render` writing its own derived artifact per the
  addendum ("rendering GOALS.md ... is legal, it is derived"), not a hand edit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-295f1de5, L4.117), replacing the kid's own thought (grid keeps it as the previous version). (1) THE INSTRUCTION SAID: fix the App-head/goal level collision I named, land the viewport residue, the no-literal-town test, and the merge-up town gate; and "keep snapshot-goals.py --render --check byte-identical". (2) WHAT THE MACHINE ACTUALLY DOES, verified by me on this tree, not read off the code: the App block now renders "heading_level + 1" and the real tree shows "## App: streaming-suite" followed by "#### G18.1" and "## App: web-app-suite" followed by "### G18" (GOALS.md:8654-8665) - strictly nested, both depths. I ran `snapshot-goals.py --render --check`: "166 goal(s) round-trip byte-identical", exit 0. I ran `viewport.py --verify`: PASS, exit 0, "one stream, two formatters, same nodes in the same order". I ran the four touched test files myself: 178 passed (test_snapshot_goals, test_viewport, test_no_literal_town, test_season). The no-literal-town test derives its town list from the ladder and AST-parses bin/*.py rather than grepping - that is the right mechanism, because a grep cannot tell prose from code and this project has paid for that distinction before. (3) THE NEAR MISS: a fix that rendered every app goal at a FIXED "###" would satisfy my words ("strictly greater than the App head") for both g18 and g18.1, and would lose the mechanism - the goal's own depth relation, so a root goal and a subgoal would land at the same level and a subgoal's subgoal would collide with its parent. The kid instead preserved relative depth for both, which is what "grouped" has to mean. (4) DEVIATION: none. HONEST RESIDUE the kid named and I confirm: `nearest_vision_town` walks only the parents: edge, so a goal carrying town: + vision_ref: with no parents: link (g18, g18.1) resolves to core in the viewport annotation while snapshot-goals, which reads vision_ref, shows it correctly - two readers of the same derived value disagree on the same graph. And the merge-up gate is opt-in by --round/--seat because the call site is dispatch.py, forbidden to this round: proven on fixtures, not yet on the live cycle. Both are the push_further for the next run at this target. REVIEW OUTCOME: kept, inconclusive_lean_proved:75 - the kid's own lean - because its claim is bounded to the residue lane it shipped and every artifact reproduces.
<!-- THOUGHT:END -->

## Agent Notes
L4.117 residue kid: fixed snapshot-goals App/goal heading collision (bump app goals +1, --render --check byte-identical on 166); viewport Frame.town annotation via shared spawn_gate helper (--verify PASS); no-literal-town AST test deriving towns from ladder; season.py merge-up town gate (--round/--seat, refuse cross-town names both, fixture-proven). Full suite 2658 passed 1 skipped.