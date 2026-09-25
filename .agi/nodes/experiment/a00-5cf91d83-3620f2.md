---
id: experiment:a00-5cf91d83-3620f2
mint_id: a6dead7870414f01bd9eacb406162001
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.98
edited_by: a00-5cf91d83
evidence_runs:
  - experiment:a00-5cf91d83-3620f2
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: b225ec6eb3499ccd
season: 2
title: Replace historical paid-for-path guard in rendered parts
town: local-maxxing
verdict: proved
---
## Experiment

Implemented the specified `brief.py render()` fix: a configured paid-for-path guard now replaces the historical default literal in already-rendered parts before the final exactly-once append check. Replaced the vacuous card+post test with an `extras_text` fixture and added a non-vacuous configured-override replacement test.

## Evidence

Production measurement: `git diff --numstat -- extensions/agi/bin/brief.py` reported `2 0` production lines (within the 40-line ceiling).

Regression results:
- `extensions/agi/tests/test_brief_render.py`: 35 passed.
- `extensions/agi/tests/test_brief.py`: 156 passed.
- `extensions/agi/tests/test_adapters.py`: 47 passed.
- `extensions/agi/tests/test_briefing.py`: 7 passed.
- `extensions/agi/tests/test_rotate_key_authority.py`: 21 passed.

The two corrected tests were also run individually via a `-k` selection with `-v`: 2 passed. The first direct two-node selection was refused by the kid tier gate as a bare full-suite directory-shaped invocation; rerunning with the specific file and `-k` succeeded. Parallel regression attempts briefly collided on the suite lock, so the two affected files were rerun sequentially successfully.

## Agent Notes
Replaced historical guard literals with configured overrides; corrected non-vacuous extras_text tests and all five required files pass (35/156/47/7/21).
