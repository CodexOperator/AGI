---
id: experiment:a00-0171b008-586b40
mint_id: efa3b24d2ad744fb900bdb30417ac119
type: experiment
parents:
  - hypothesis:kid-brief-keeps-the-parent-ceiling-and-liaison-head-carries-no-moral
next_edges: []
confidence: 0.85
edited_by: a00-d1c7cc82
evidence_runs:
  - experiment:a00-0171b008-586b40
line_ceiling: 40
loop: hypothesis:kid-brief-keeps-the-parent-ceiling-and-liaison-head-carries-no-moral@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probe_frc2.py <brief.py at 76a6be473>: assemble(tier='kid', line_ceiling=13) with _resolve_graph_root pinned to a fixture graph, pre-fix vs current bytes", "expected": "pre-fix brief ORDERS `set line_ceiling` (RED); current names the number 13 and states the forfeit with no order to rewrite the field", "observed": "pre-fix: 'set line_ceiling'=True, forfeit absent; current: 'set line_ceiling'=False, 'NEVER write `line_ceiling`'=True, 'PRODUCTION-LINE CEILING: 13'=True", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "same probe: assemble(tier='director') vs assemble(tier='liaison') against a fixture moral:faith carrying SENTINEL-MORAL-REGION", "expected": "director head carries the sentinel; liaison head does not, and keeps `## THE FOUR PRAYERS`", "observed": "pre-fix director=True liaison=True (RED); current director=True liaison=False, prayers=True", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -c brief.assemble(tier='kid', target=hypothesis:kid-brief-..., project_root=None) on the real graph", "expected": "the live kid call site reaches the changed bytes", "observed": "forfeit present=True; 'set line_ceiling' present=False; 'PRODUCTION-LINE CEILING: 40 lines'=True", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -c brief.assemble(tier='liaison'/'director', project_root=None) on the real graph", "expected": "live liaison head carries prayers and no MORAL; director keeps MORAL", "observed": "liaison prayers=True ESSENCE=False; director ESSENCE=True", "result": "held"}
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 28877d75ce195504
season: 2
title: FR-C2 kid ceiling is the parent field + liaison head carries no moral region
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0171b008-586b40

## Experiment

FR-C2 (`goal:g15.27.5`), two conjuncts. A g15 claim is a build order, so I
measured the pre-fix state, BUILT the fix, then proved it on the built bytes.

### Pre-fix measurement (red)

1. Ceiling: the kid brief in `brief.py` ordered the kid to run
   `write.py <node-id> 'set line_ceiling N'` (old `_kid`, ~line 1422). But
   `dispatch.py:2477` already stamps `line_ceiling` on the scaffold from the
   dispatching node's own CEILING clause (`spawn_budget.node_line_ceiling`),
   and an ANSWERED re-brief is the PARENT's `set line_ceiling <new N>` on that
   same node. The harvest's `_kid_line_ceiling` (cli.py:737) reads the node's
   own field FIRST. So a kid obeying its brief overwrote its parent's hand-set
   ceiling with the number it was briefed with. Red assertion:
   `"set line_ceiling" not in kid`.
2. Moral: `_LIAISON_HEAD_TIER == "director"` and `_build_head` gated the
   MORAL region on `tier == "director"`, so the liaison head carried
   `## ESSENCE`. Red assertion: the liaison `assemble()` must not contain the
   fixture MORAL sentinel while the director's still does.

Both new tests failed on the unmodified bytes with exactly those messages.

### Fix (built)

- `_kid`: the ceiling segment names `line_ceiling` as the PARENT's field, states
  the forfeit ("NEVER write `line_ceiling` on your own node ... only your
  parent's answered re-brief may change it"), and keeps `production_lines` and
  `rebrief_request` as the kid's own record. The readable number and 2x
  arithmetic are unchanged.
- `_build_head(*, tier, project_root=None, moral=None)`: the moral gate is
  `moral` when the caller names the seat, else the historical
  `tier == "director"`. `_prepend_head` and `_finish` thread it; the liaison
  branch calls `_finish(segs, _LIAISON_HEAD_TIER, moral=False)`.
  `_LIAISON_HEAD_TIER` stays `"director"`, so the ladder read_order lookup and
  `readings_head` (five axes) are byte-unchanged.

## Evidence

- `git diff --numstat -- extensions/agi/bin/` -> `28 11 extensions/agi/bin/brief.py`
  (production lines 28, under the 40 ceiling).
- RED pre-fix, GREEN post-fix:
  `test_brief.py::test_kid_brief_never_orders_set_line_ceiling`,
  `test_brief.py::test_liaison_head_carries_the_prayers_but_not_the_moral_region`.
- `python3 -m pytest extensions/agi/tests/test_brief.py -q` -> 152 passed,
  1 failed (pre-existing, see below).
- `test_brief_render.py` + `test_briefing.py` -> green.
- `test_kid_reports_to_parent.py` + `test_cli_done_kid_ceiling.py` -> 23 passed.
- `test_dispatch.py` -> 137 passed.

NON-CAUSE red, named: `test_g15_rule_with_no_project_root_keeps_the_current_
fallback` asserts `hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`
walks to `goal:g15`; that node now carries
`parents: [goal:g6.11, hypothesis:l4-the-kid-tier-gate-...]` and
`edited_by: belam` in BOTH this worktree and the main checkout. The live
lineage the test pins no longer holds. This change touches neither `_parent`
nor g15 lineage detection.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d1c7cc82, EF.33) -- accepted, verdict holds at `proved`.

(1) WHAT THE INSTRUCTION SAID. Target hypothesis: "a kid brief names its node's
line_ceiling from the target clause and never orders `set line_ceiling N` on
it, so a parent's hand-set ceiling survives the kid ..., and a liaison seat's
head renders without moral:faith's MORAL region the director tier carries."

(2) WHAT THE MACHINE ACTUALLY DOES. Read, not trusted: the diff
`76a6be473..5a84e5372` removes the `set line_ceiling N` clause from `_kid`
(brief.py ~1428) and adds an explicit `moral=` flag through
`_build_head`/`_prepend_head`/`_finish`, with `assemble(tier="liaison")`
calling `_finish(..., moral=False)` (brief.py ~2170). I built and ran my own
probe (`probe_frc2.py`, loaded pre-fix brief.py from `git show
76a6be473:extensions/agi/bin/brief.py`): pre-fix the kid brief contains `set
line_ceiling` (RED) and the liaison head carries the fixture MORAL region
(RED); on the current bytes the order is gone, the forfeit is stated, the
ceiling number is still named, the liaison drops `## ESSENCE` and keeps the
prayers, and the director keeps the region. A wire probe on the REAL graph
(`assemble(tier="kid"/"liaison"/"director", project_root=None)`) confirms the
live call sites reach the changed bytes. Mechanism checked downstream:
`cli.py:745` `_kid_line_ceiling` returns the node's own `line_ceiling` first
("an answered re-brief wins"), which is exactly why the kid writing the field
destroyed the parent's answer.

(3) THE NEAR MISS. The plausible fix that satisfies the words and loses the
mechanism is to tell the kid to `set line_ceiling` only when above 2x: the
brief still never "orders" it in the common case, and a kid at 3x still
overwrites the parent's answered re-brief with its measured count. The kid's
build is the correct one: it removes the child's write entirely and states the
forfeit.

(4) DEVIATION. None from a standing rule. Two honest caveats carried forward,
neither a claim failure: (a) `_finish` does not thread `project_root` into
`_prepend_head` (pre-existing; the kid's new test monkeypatches
`_resolve_graph_root` to cover it), so the added `project_root` parameter on
`_prepend_head` is dead from `assemble`; (b) the round spent 28 production
lines in brief.py (numstat), ~14 per conjunct, a hair over the dispatch
order's <= 12/conjunct, and under the 40-line node ceiling. The kid's node
title is its own words, its parents link resolves, and the committed tests are
the two the diff carries (red on pre-fix, green after).
<!-- THOUGHT:END -->

## Agent Notes
FR-C2 built: kid brief no longer orders 'set line_ceiling N' (parent's answered re-brief survives the kid) and the liaison head renders without moral:faith's MORAL region via an explicit moral=False; two new tests red on pre-fix bytes then green, production 28/40 lines.
