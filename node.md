---
id: mvp:goal-order-retired
mint_id: 2673baa700ca454487400f03908a85d3
type: mvp
parents:
  - goal:s12
next_edges: []
confidence: 0.9
edited_by: season.py
season: 1
source_files:
  - extensions/agi/bin/snapshot-goals.py
  - extensions/agi/tests/test_snapshot_goals.py
status: implemented
tags:
  - goals
  - render
tests_pass: true
thought_session: season
title: "GOALS.md renders by natural goal_id sort; the order: field is retired"
---
# mvp:goal-order-retired

**Parent chosen: `goal:s12`, not `goal:g2.5`.** Both exist on this corpus
(`.agi/nodes/goal/s12-snapshot-goalspy-silently-truncates-goal-bodies.md` and
`.agi/nodes/goal/g2.5-node-ids-are-hierarchical-addresses-not.md`), so the
instruction to pick "whichever actually exists" needed a tiebreak: `goal:s12`
is the more specific parent — it is the goal that already lives in
`snapshot-goals.py`'s rendering path (the body-cap fix), the same file and
the same render function this change edits. `goal:g2.5` is about node-id
addressing generally, one level more removed from this specific mechanism.

## What changed

`order:` — a dense, contiguous `0..90` integer stamped on every goal node,
read only by `snapshot-goals.py` — is retired. `GOALS.md` now renders sorted
by a natural read of each node's own `goal_id`, via a new
`natural_sort_key()`:

- Splits `<letters><digits[.digits...]>` into a prefix and a tuple of
  integers, so `G2.10` sorts after `G2.9` (a lexicographic sort would put it
  between `G2.1` and `G2.2`) and `S11` sorts after `S2`.
- `G` sorts before `S` because the prefix compares first and `"G" < "S"`
  lexically, preserving the document's existing G-goals-then-S-goals
  grouping with no special case.

Three places in `extensions/agi/bin/snapshot-goals.py` changed:

1. `render_goals()` sorts by `natural_sort_key(x["gid"])` instead of
   `x["order"]`.
2. `load_goal_nodes()` no longer requires `order` — the hard error now names
   only a missing `heading_level`. The duplicate-`order` check is removed
   (nothing left to collide on).
3. `parse_goals()`/`_start()` and the `--from-doc` node-writer no longer
   assign or emit an `order` field at all, so a fresh import cannot
   reintroduce it.

`heading_level:` is untouched — still required, still read the same way.

## The one consequence: the S-block reshuffles once

Computed with the parser and renderer themselves, comparing heading order in
the committed `GOALS.md` against the freshly rendered one:

```
$ python3 -c "
import importlib.util, re
spec = importlib.util.spec_from_file_location('sg', 'extensions/agi/bin/snapshot-goals.py')
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)
existing = sg.load_existing_nodes()
preamble, goals = sg.load_goal_nodes(existing)
rendered = sg.render_goals(preamble, goals)
before = re.findall(r'^#{2,3} ([GS]\d+(?:\.\d+)?) ', open('GOALS.md').read(), re.M)
after  = re.findall(r'^#{2,3} ([GS]\d+(?:\.\d+)?) ', rendered, re.M)
print(len(before), len(after), set(before) == set(after))
"
91 91 True
```

**17 of 91 goals move; 74 do not.** Every G-goal (0 of them) stays put — the
long-term/sub-goal chain was already in natural order. `S11`..`S17` move
from *before* `S1` to *after* `S10`:

| goal | old position | new position | delta |
|---|---|---|---|
| S1 | 78 | 71 | −7 |
| S2 | 79 | 72 | −7 |
| S3 | 80 | 73 | −7 |
| S4 | 81 | 74 | −7 |
| S5 | 82 | 75 | −7 |
| S6 | 83 | 76 | −7 |
| S7 | 84 | 77 | −7 |
| S8 | 85 | 78 | −7 |
| S9 | 86 | 79 | −7 |
| S10 | 87 | 80 | −7 |
| S11 | 71 | 81 | +10 |
| S12 | 72 | 82 | +10 |
| S13 | 73 | 83 | +10 |
| S14 | 74 | 84 | +10 |
| S15 | 75 | 85 | +10 |
| S16 | 76 | 86 | +10 |
| S17 | 77 | 87 | +10 |

(positions are 0-indexed in the script above; +1 for a 1-indexed reading of
`GOALS.md`.) All 91 `goal_id`s are present in both — none dropped, none
duplicated. This is the expected, one-time correction the task called out in
advance: `S11..S17` were only ever ahead of `S1..S10` because ids are never
renumbered and the document grew that way, not because of any intended
priority. `GOALS.md` was regenerated with `--render` (never hand-edited) and
committed as the render's own output; `git diff --stat GOALS.md` shows
`680 insertions(+), 680 deletions(-)` against the 91-goal reshuffle.

## Gates run

```
$ python3 -m pytest extensions/agi/tests/ --ignore=extensions/agi/tests/test_publish_alarm.py -q
975 passed in 44.11s

$ grep -c '^order:' .agi/nodes/goal/*.md | grep -v ':0' | wc -l
0

$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 91 goal(s) round-trip byte-identical

$ python3 extensions/agi/bin/snapshot-goals.py --render --strict-goals
rendered: 91 goal(s) + preamble -> GOALS.md   (exit 0)

$ find .agi/nodes -name '*.md' | wc -l
814 before this node, 815 after (this file)

$ grep -c '^#\{2,\} ' GOALS.md
180 before and after (91 goal headings + doc-internal headings, unchanged)
```

`test_publish_alarm.py` (26 tests) is excluded from the pytest count above,
not fixed here: `extensions/agi/bin/metrics.py` is mid-edit by a second kid
working the same tree this iteration (git shows it modified, 243 lines
changed, currently missing a `publish_stats` definition its own call site
needs — `NameError: name 'publish_stats' is not defined` at line 614). That
file and `.agi/nodes/.geometry/crons.md` are explicitly not mine to touch.
Running the full suite including that file is flaky by the run (23–54 failed
depending on the concurrent edit's state at that instant); every failure is
confined to `test_publish_alarm.py`/`test_locations.py`'s `metrics` import,
none in `test_snapshot_goals.py` or anywhere else this change touches.

## Regression tests added

`extensions/agi/tests/test_snapshot_goals.py`:
- `test_natural_sort_orders_dotted_subgoals_numerically` — `G2.9 < G2.10 <
  G2.11`.
- `test_natural_sort_orders_short_term_goals_numerically` — `S2 < S11`.
- `test_natural_sort_puts_g_goals_before_s_goals`.
- `test_natural_sort_full_worked_example` — the exact ordering from the
  task's spec, shuffled and re-sorted.
- `test_a_goal_node_missing_order_renders_without_error` — a goal node
  carrying no `order` field at all still renders.
- `test_a_goal_node_missing_heading_level_is_a_hard_error` — replaces the
  retired `test_a_goal_node_missing_order_is_a_hard_error`; `heading_level`
  is still required, `order` no longer is.
- `test_document_order_is_naturally_sorted_by_goal_id_on_render` — replaces
  `test_unsorted_document_order_survives_the_round_trip`, which pinned the
  exact behaviour this change deliberately reverses.
- `test_duplicate_order_across_nodes_is_a_hard_error` removed outright: there
  is no `order` value left for two nodes to collide on.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Chose goal:s12 over goal:g2.5 as parent because both existed and the task
asked for a judgment call, not an escalation — s12 already lives in the exact
function (`render_goals`/body-cap logic) this change modifies, making it the
tighter fit. Did not attempt to fix metrics.py's NameError even though it
inflates the "tests passing" number of a naive full-suite run to a scary
54-failed: it is not a file this task owns, another kid is actively mid-edit
on it, and the hard rules are explicit that I only report what I see there,
never touch it. Removed the duplicate-order hard-error test rather than
inventing a duplicate-goal_id check to replace it, since introducing a new
integrity check was out of the bounded scope this task defined (remove
order:, sort by goal_id, keep both directions working) — flagging it here
instead of quietly expanding scope.
<!-- THOUGHT:END -->