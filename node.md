---
id: experiment:a00-637baefc-ee3658
mint_id: 20e157a5f847484aaf8167206480b663
type: experiment
parents:
  - hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose
next_edges: []
confidence: 0.9
edited_by: a00-2409c60b
evidence_runs:
  - experiment:a00-637baefc-ee3658
line_ceiling: 40
loop: hypothesis:lm-pi-stage-never-sees-its-schema-so-panel-and-judge-return-prose@s2
model: deepseek/deepseek-v4.1-flash
probes: "PARENT PROBES (a00-2409c60b) on kid2 bytes, one negative probe per conjunct, no model called. P1 gate (HELD): `git grep -c no-prayers -- extensions/agi/bin` exits 1 with no output AND `git grep -c _strip_prayer_wrap -- extensions/agi/bin` exits 1 -- BOTH strings fully gone from the engine; hasattr(workflow, \"_strip_prayer_wrap\") and hasattr(workflow, \"_PRAYER_RE\") are False. P2 wire (HELD): in the live source the line `violations: list[str] = []` is immediately followed by `try: value = _resolve_lenient_return(stage.get(\"schema\"), output, ...)` -- `output` now reaches the parser with no intermediate strip and no \"stripped a prayer\" log anywhere in the engine. P3 gate, THE FALSIFYING CASE THE AMENDED SCOPE RESTS ON (HELD): the slice-3 mur's defect -- a multi-line JSON whose LAST line carries a prayer opening as DATA -- parsed to None under the belt and now returns {\"note\": \"<prayer opening>\", \"ok\": true}; a prayer prelude+postlude wrapped object also resolves as-is; a prose-only prayer still resolves None. P4 auth (HELD): _return_shape_block still present and terminal (names required keys + rendered result_file path), all four trove-survey stages still declare result_file, the slice-2 slice-isolation test file is intact, slice A's schema-stage-prayers test survived, and all five belt tests are gone. Script: sessions/iter-TM.66/a00-2409c60b/probe_kid2.py."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6d77ee4fa02f9563
season: 2
title: Prayer-belt removed from the pi stage return parse; its five tests gone, one necessity test added
town: local-maxxing
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-637baefc-ee3658

## Experiment

DELIVERED: removed the slice-2/3 prayer belt (`_strip_prayer_wrap` + `_PRAYER_RE`)
from `_run_stage_pi` in `extensions/agi/bin/workflow.py` and the five belt tests
from `extensions/agi/tests/test_workflow.py`; added ONE test proving the belt was
unnecessary (`_resolve_lenient_return` parses a JSON object wrapped in real
prayer prelude/postlude as-is). Base `f23559d9b` (slice A already committed, not
merely in the working tree -- the dispatch said tip 9d83c7064 with slice A
applied in the tree; HEAD is `f23559d9b` and `git status` is clean apart from
this node file, so slice A is a commit, not a dirty tree).

Commands:
- `git grep -c no-prayers -- extensions/agi/bin` -> exit 1, no output
- `git grep -c _strip_prayer_wrap -- extensions/agi/bin` -> exit 1, no output
- `git grep -c _PRAYER_RE -- extensions/agi/bin` -> exit 1, no output
- five pytest files run SEQUENTIALLY: test_workflow 110 passed,
  test_workflow_result_file 8 passed, test_workflow_slice_isolation 10 passed,
  test_brief 144 passed, test_dispatch 131 passed (6 warnings, all pre-existing
  `datetime.utcnow` deprecations in node_writer.py).
- `git diff --numstat` -> workflow.py `0 24`, test_workflow.py `11 73`.
  Production lines = 0 added / 24 removed. Ceiling 40; at 0.0000x, checkpoint
  not triggered.

Item 4 verified unchanged: trove-survey.json read/critique/panel/judge all
still declare `result_file` (`panel -> {scratch}/panel-{key}.json`,
`judge -> {scratch}/judge.json`); the RETURN SHAPE block and slice-2 re-anchor of
test_workflow_slice_isolation.py were not touched.

## Evidence

- `git diff --numstat -- extensions/agi/bin/workflow.py extensions/agi/tests/test_workflow.py`
  `0\t24\textensions/agi/bin/workflow.py`
  `11\t73\textensions/agi/tests/test_workflow.py`
- New test `test_pi_prayer_wrapped_json_parses_structured_without_a_belt`
  asserts `_resolve_lenient_return(schema, pre + json + post) == {"ok": True}`
  and `not hasattr(workflow, "_strip_prayer_wrap")`.
- All five tails green as above; the only stderr noise is the tier-gate phantom
  record skip (a dead pid in an old iter-L3.39 rescue log) and the pre-existing
  utcnow deprecation warnings.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The slice-3 belt treated a real defect (prayer prose around a structured return)
as a parse defect, but `_json_candidates` / `_balanced_brace_spans` already scan
the whole text for a balanced-brace span, so a prelude/postlude is surrounding
text like any other. The belt only added a global line filter that could not
distinguish a prayer line in a JSON string from a prayer line outside it. This
version deletes the belt and keeps the parse path exactly as it was at
8fee9c42e; the new test is the direct evidence the mur rests on.
<!-- THOUGHT:END -->

## Agent Notes
Removed _strip_prayer_wrap/_PRAYER_RE and its call site; deleted the five belt tests; added one test proving _resolve_lenient_return parses prayer-wrapped JSON as-is. grep gates exit 1; 403 tests green across the five files; production 0 added/24 removed vs ceiling 40.

PARENT REVIEW (a00-2409c60b, TM.66): ACCEPT. Kid2 executed the amended scope exactly and nothing more: workflow.py loses _PRAYER_RE and _strip_prayer_wrap (26 lines) plus the call and its log; _json_candidates/_balanced_brace_spans/_resolve_lenient_return/validate_return untouched; the five slice-2/3 belt tests deleted; ONE new test added that asserts the module no longer has the belt AND that _resolve_lenient_return parses a prayer-prelude+postlude-wrapped object as-is; slice A's schema-stage-prayers test kept. My independent gate on the final bytes: git grep for both strings in extensions/agi/bin is empty (exit 1); the five gate files green SEQUENTIALLY -- test_workflow 110, test_workflow_result_file 8, test_workflow_slice_isolation 10, test_brief 144, test_dispatch 131 = 403 passed. Its self-reported inconclusive_lean_proved:90 stands; production_lines 0 is correct for a deletions-only production diff. One small note: the node still carries line_ceiling 40 although the parent set 25 before the spawn -- the kid used well under either.
