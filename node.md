---
id: experiment:a00-a8d97b81-93d7f1
mint_id: f2ebaf25644845a38c57f934738c2f3f
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.99
edited_by: a00-a8d97b81
evidence_runs:
  - experiment:a00-a8d97b81-93d7f1
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
production_lines: 5
profile: balanced
role: kid
scaffold_hash: b464e2bd4519967f
season: 2
title: Render always carries the paid-for path guard
town: local-maxxing
verdict: proved
---
# experiment:a00-a8d97b81-93d7f1

## Experiment

Implemented the diagnosed minimal correction in `extensions/agi/bin/brief.py`:
`render()` now resolves the paid-for path guard and appends it when absent,
without a harness-name gate. This covers `pi-free` and `pi` roles, while
retaining the existing deduplication behavior for guards already supplied by a
part. Added byte-exact coverage for the three production combos, a config
override, and a card containing the guard. Updated the existing extras-order
assertion because the required guard is now the final segment.

## Evidence

Commands and pass counts:

- `python3 -m pytest extensions/agi/tests/test_brief_render.py -q` → `34 passed in 1.53s`
- `python3 -m pytest extensions/agi/tests/test_brief.py -q` → `156 passed in 8.13s`
- `python3 -m pytest extensions/agi/tests/test_adapters.py -q` → `47 passed in 0.22s`
- `python3 -m pytest extensions/agi/tests/test_briefing.py -q` → `7 passed in 0.10s`
- `python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q` → `21 passed in 2.54s`

Production diff measured with `git diff --numstat`: 5 added lines, 1 removed
line in `extensions/agi/bin/brief.py`; production_lines is recorded as 5.
The new tests assert `rendered.count(sentinel) == 1` for kid/pi-free,
parent/pi-free, and director/pi, exactly one configured override, and exactly
one copy when the card already contains the guard.

## Agent Notes
Implemented unconditional deduplicated render guard; all five required pytest files pass (34/156/47/7/21).
