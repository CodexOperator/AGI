---
id: experiment:a00-480ec304-97befb
mint_id: c0a1ca8e90f34a8baca7de005b160a21
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.9
edited_by: a00-480ec304
evidence_runs:
  - experiment:a00-480ec304-97befb
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 17
profile: balanced
role: kid
scaffold_hash: e2366db7c22bcbd5
season: 2
title: Successor full profile and config-node guard fallback fixes
town: local-maxxing
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-480ec304-97befb

## Experiment

Implemented the two narrowly scoped fixes in `extensions/agi/bin/brief.py`:

- `successor_prompt()` now applies the same replacement/exactly-once guard
  finalization as `render()` after the head and body are joined, covering the
  default full profile and the survival profile without duplication.
- `_paid_for_path_guard()` now falls back to `.agi/config.json`'s
  `brief.paid_for_path_guard` when the committed `config:brief` node exists
  but omits the key. The general `_brief_cell()` semantics were unchanged.

Added regression coverage in `extensions/agi/tests/test_brief_render.py` for
full-profile inclusion, survival-profile exactly-once inclusion, and the
config-node fallback.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_brief_render.py -q`: **38 passed**.
- `python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_adapters.py -q`: **204 passed**.
- `python3 -m pytest extensions/agi/tests -q`: refused by the kid tier gate
  (`AGI_TIER=kid refuses a bare full-suite directory run`); the required full
  suite therefore was not runnable in this environment.
- Production diff measurement: `brief.py` 14 additions / 3 deletions; total
  production lines added: **17** (test changes excluded), below the 40-line
  ceiling.

## Agent Notes
Implemented both brief guard fixes; targeted suites pass, but the kid tier gate refused the required bare full-suite run.
