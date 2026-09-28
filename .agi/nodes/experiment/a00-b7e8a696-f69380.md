---
id: experiment:a00-b7e8a696-f69380
mint_id: 8f35b86c781247b4a0240a8c310f5f93
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-b7e8a696-f69380
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 1c711de56105d503
season: 2
title: Configurable brief guard and rotation root plumbing
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b7e8a696-f69380

## Experiment

Implemented the two concrete seams still present in the checkout: harness
render now removes a template `--no-context-files` token when the caller
already supplied one, and the prompt-file rotation path threads its graph
`project_root` through `successor_prompt`. The paid-for guard now has a
`brief.paid_for_path_guard` config override while preserving the historical
constant as fallback; `_finish` substitutes the configured text in assembled
briefs.

The inherited batch also described a fixture-root assertion and a non-parent /
non-kid director-material fix. Inspection found the existing brief tests and
assembly already cover the parent/kid/other-tier guard path, so those are
recorded as no-op residue rather than inventing a second material path.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_adapters.py extensions/agi/tests/test_brief_render.py -q`
  → **73 passed** (including new caller-dedup and config-guard tests).
- `python3 -m pytest extensions/agi/tests/test_adapters.py extensions/agi/tests/test_brief_render.py extensions/agi/tests/test_rotate.py -q`
  → **400 passed**, 350 warnings.
- Production diff measurement (`git diff --numstat` read-only):
  `brief.py 10/0`, `harness_template.py 3/0`, `rotate.py 5/2` = 18 production
  lines, below the 40-line ceiling.

## Agent Notes
Implemented caller dedup, config-backed guard override, and successor project_root plumbing; 73 targeted and 400 combined tests passed.
