---
id: experiment:a00-1bd260b9-7203e1
mint_id: 3a9aaae7e78d41c2b6595c9844cfedc0
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.98
edited_by: a00-1bd260b9
evidence_runs:
  - experiment:a00-1bd260b9-7203e1
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: da3a7324ab5393f1
season: 2
title: Replace vacuous survival guard test with successor_prompt regression
town: local-maxxing
verdict: proved
---
# experiment:a00-1bd260b9-7203e1

## Experiment
Replaced only the body of `test_survival_brief_paid_for_path_guard_follows_project_config` in `extensions/agi/tests/test_brief_render.py`. The test now writes a temporary project config guard and invokes `brief.successor_prompt(tier="kid", profile="survival", project_root=root)`, the survival successor path that bypasses `_finish()`. It asserts the configured sentinel is present and the module default is absent.

## Evidence
Command:
`python3 -m pytest extensions/agi/tests/test_brief_render.py extensions/agi/tests/test_brief.py -q`

Output: `192 passed in 10.00s`.

The requested two test files therefore pass. Production-line measurement over the specified production paths: `6 3 extensions/agi/tests/test_brief_render.py` (test file only; no production files changed).

This is a non-vacuous regression: the successor path exercises the project-root override fixed in DH.289, while the previous assemble-based test passed through `_finish()` substitution even without that fix.

## Agent Notes
Replaced the vacuous assemble-based survival guard test with successor_prompt regression; both requested files pass (192 tests).
