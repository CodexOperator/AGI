---
id: experiment:a00-0e2d9bc4-11482b
mint_id: 297356437ace46f69881157668ba6f24
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.55
evidence_runs:
  - experiment:a00-0e2d9bc4-11482b
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: e983cdb291252f93
season: 2
title: Preserve pi guard position and survival guard override
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-0e2d9bc4-11482b

## Experiment

Applied the two scoped production fixes and their append-only regression tests:

| Path | Change |
|---|---|
| `extensions/agi/bin/harness_template.py` | Replaced strip-and-append deduplication with in-place first-occurrence deduplication, preserving `--no-context-files` before the positional prompt. |
| `extensions/agi/bin/brief.py` | Routed `_survival_brief()` through `_paid_for_path_guard(project_root)`. |
| `extensions/agi/tests/test_adapters.py` | Added a full-argv assertion covering duplicate position. |
| `extensions/agi/tests/test_brief_render.py` | Added a survival-profile override assertion. |

The changes are within the requested 40-line production ceiling: 9 changed production lines in `harness_template.py` and 1 in `brief.py` (10 additions/deletions by the scoped diff), with no other production paths changed.

## Evidence

The added tests encode the pre-fix failures and expected fixed behavior: duplicate pi argv must equal the full list ending in `turn`, and a configured survival guard must appear without the historical default. The required six-file pytest regression was not run because this iteration's command contract permits only the final `cli.py done` command; the node therefore records the implementation but not test execution.

## Agent Notes
Applied both scoped fixes and added two focused regression tests; pytest and numstat could not be run under the sole-command completion contract.
