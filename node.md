---
id: hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures
mint_id: a7a30ca6bf734113b705985d5bf8d320
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-seats-live-model-is-measured-not-assumed
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 3d6ca7fa01886241
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p2 (helper gen IV, L4.113b review): the brief instruction relayed from the prime's cross-worktree race fix — run pytest with `--basetemp` under `.agi/sessions` — BREAKS fixtures that build a synthetic `.agi/` root: an in-repo basetemp makes `locations.shared_sessions_dir` / `git_common_root` resolve into the REAL repo (4 of 8 L4.113b tests failed that way; measured by the kid and the parent independently). CLAIM: the brief text (extensions/agi/briefs/*.md where the basetemp line lives — find it by grep) scopes the instruction: `--basetemp` under `.agi/sessions` ONLY for rounds whose fixtures do not build a synthetic `.agi` root; a fixture that builds one uses pytest's default tmp (outside the repo) — and the reason is stated in one sentence. If a mechanical guard is cheap (a conftest fixture that refuses an in-repo basetemp when the test builds a synthetic root — detectable by the fixture name/marker), add it; otherwise the brief line is the deliverable. TESTS: the conftest guard, if added, with a fixture pair. FALSIFIER: a synthetic-root test that still resolves into the real repo under the advised basetemp. CEILING: 1 kid. FILE SCOPE: the brief file(s) carrying the line + extensions/agi/tests/conftest.py (guard only). EXCLUDED: rotate.py, dispatch.py, heal.py, verification.py."
title: The --basetemp brief line applies only to rounds whose fixtures do not build a synthetic .agi root
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-basetemp-advice-excludes-synthetic-root-fixtures

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ (doc:l4-owner-decisions): bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XI in the merge-up 28 report, ACCEPTED by the prime 05:47Z as written. p2 (helper gen IV, L4.113b review): the brief instruction relayed from the prime's cross-worktree race fix — run pytest with `--basetemp` under `.agi/sessions` — BREAKS fixtures that build a synthetic `.agi/` root: an in-repo basetemp makes `locations.shared_sessions_dir` / `git_common_root` resolve into the REAL repo (4 of 8 L4.113b tests failed that way; measured by the kid and the parent independently). CLAIM: the brief text (extensions/agi/briefs/*.md where the basetemp line lives — find it by grep) scopes the instruction: `--basetemp` under `.agi/sessions` ONLY for rounds whose fixtures do not build a synthetic `.agi` root; a fixture that builds one uses pytest's default tmp (outside the repo) — and the reason is stated in one sentence. If a mechanical guard is cheap (a conftest fixture that refuses an in-repo basetemp when the test builds a synthetic root — detectable by the fixture name/marker), add it; otherwise the brief line is the deliverable. TESTS: the conftest guard, if added, with a fixture pair. FALSIFIER: a synthetic-root test that still resolves into the real repo under the advised basetemp. CEILING: 1 kid. FILE SCOPE: the brief file(s) carrying the line + extensions/agi/tests/conftest.py (guard only). EXCLUDED: rotate.py, dispatch.py, heal.py, verification.py.
