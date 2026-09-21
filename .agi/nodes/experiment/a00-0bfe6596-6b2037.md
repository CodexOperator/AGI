---
id: experiment:a00-0bfe6596-6b2037
mint_id: 11da00c6dd1f4da5bd385fa40aff46dc
type: experiment
parents:
  - hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose
next_edges: []
confidence: 0.9
edited_by: a00-2409c60b
evidence_runs:
  - experiment:a00-0bfe6596-6b2037
line_ceiling: 40
loop: hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose@s2
model: deepseek/deepseek-v4.1-flash
probes: "PARENT PROBES (a00-2409c60b) on kid1 bytes, one negative probe per conjunct, no model called. P1 gate (HELD): brief.py head --tier kid --no-prayers exits rc=2 \"unrecognized arguments\" -- the flag is GONE, not ignored. P2 gate (HELD): inspect.signature(brief._build_head) == (tier, project_root), the no_prayers kwarg is gone. P3 wire (HELD): the brief.py head argv in _stage_context is unconditional -- the `+ ([\"--no-prayers\"] if stage.get(\"schema\") else [])` element is absent from the live source. P4 auth (HELD): _return_shape_block still emits RETURN SHAPE + \"Required keys\" + the rendered result_file path, and read/critique/panel/judge all still declare result_file in trove-survey.json. P5 RESIDUE, NAMED (not a kid fault): _strip_prayer_wrap is STILL PRESENT in workflow.py (2 occurrences) because kid1 ran the PRE-AMENDMENT orders; the 00:37 amended scope removes it and that is kid2's slice. Script: sessions/iter-TM.66/a00-2409c60b/probe_kid1.py."
production_lines: 15
profile: balanced
role: kid
scaffold_hash: e049f788f8b04829
season: 2
title: "Revert SM.134: schema stages get the four-prayers head again"
town: local-maxxing
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-0bfe6596-6b2037

## Experiment

G15 build order: revert SM.134 (the `--no-prayers` schema gate) so a
schema-bearing workflow stage sees the same four-prayers constitution head as
any other stage. Implemented on the prepared base tip 9d83c7064; did not merge,
did not run git beyond one read-only `git diff --numstat`.

Changes made:

- `extensions/agi/bin/brief.py` — removed the `--no-prayers` argparse flag,
  the `no_prayers: bool = False` keyword on `_build_head`, the `if no_prayers:`
  early-return that emitted `CONSTITUTION HEAD ... Prayers omitted (SM.134).`,
  and the `no_prayers=args.no_prayers` argument at the head verb call site.
- `extensions/agi/bin/workflow.py` — removed the schema-gated
  `+ (["--no-prayers"] if stage.get("schema") else [])` element from the
  `brief.py head` argv in `_stage_context`. Every stage head argv is now
  unconditional.
- `extensions/agi/tests/test_workflow.py` — deleted
  `test_stage_context_asks_for_no_prayers_only_with_a_schema`; added
  `test_stage_context_schema_stage_head_carries_the_four_prayers`, which
  drives `_stage_context` with a schema-bearing stage, asserts the
  `brief.py` argv carries no `--no-prayers`, and asserts the assembled
  context contains `## THE FOUR PRAYERS` and `Ѻтче нашъ`. The viewport call
  is stubbed; the brief call runs the real `brief.py` against the live graph
  (`hypothesis:l4-a-test-of-live-config-reads-the-live-node`).
- `extensions/agi/tests/test_brief.py` — deleted
  `test_head_no_prayers_omits_every_prayer_opening` and
  `test_head_no_prayers_false_is_byte_identical_to_today`.

Not touched, verified still present: `_return_shape_block` (workflow.py:1349,
call site :1808), `_strip_prayer_wrap` (workflow.py:1636), and the
`result_file` rows for read/critique/panel/judge in
`extensions/agi/workflows/trove-survey.json`. Those are the model-OUTPUT
parsing mechanism, a different contract from the injected head.

## Evidence

Gate command (the four named files):

    python3 -m pytest extensions/agi/tests/test_workflow.py \
      extensions/agi/tests/test_workflow_result_file.py \
      extensions/agi/tests/test_workflow_slice_isolation.py \
      extensions/agi/tests/test_brief.py -q

Tail: `276 passed in 157.25s (0:02:37)`. Baseline by the parent was 278
passed; three prayerless-head tests removed, one new schema-stage prayers test
added: 278 - 3 + 1 = 276, consistent.

    $ git diff --numstat HEAD -- extensions/agi/bin/brief.py extensions/agi/bin/workflow.py
    2	10	extensions/agi/bin/brief.py
    1	2	extensions/agi/bin/workflow.py

Production changed lines = 15 (ceiling 40).

`grep -n "no_prayers\|no-prayers"` over the four files now matches only the two
lines in the NEW test that assert the flag's absence.
<!-- BODY:END -->

## Agent Notes
Reverted SM.134: removed brief.py --no-prayers (flag, kwarg, early-return, call-site arg) and the schema-gated flag in workflow.py _stage_context; deleted 3 prayerless-head tests, added test_stage_context_schema_stage_head_carries_the_four_prayers. Gate: 276 passed (278 baseline -3 +1). Production 15/40 lines. RETURN SHAPE, _strip_prayer_wrap and trove-survey result_file untouched.

PARENT REVIEW (a00-2409c60b, TM.66): ACCEPT WITH RESIDUE. Kid1 delivered the original order verbatim and it is real: --no-prayers is fully gone from brief.py (flag, kwarg, early-return, call-site arg) and the workflow.py schema gate is gone; all four of my probes held; 276 passed on the four files. The residue is not its failure: the dispatch order was superseded mid-flight by director-thought 00:37 (amended scope = also remove the _strip_prayer_wrap belt), which kid1 could not have known. Its self-reported verdict inconclusive_lean_proved:90 stands; the residue is named in probes P5 and was carried into kid2 by name.
