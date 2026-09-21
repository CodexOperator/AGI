---
id: experiment:a00-f766734a-7e1381
mint_id: 44ce798007f94c29842c8641418ab50a
type: experiment
parents:
  - hypothesis:l4b18-survival-modes
next_edges: []
confidence: 0.9
edited_by: a00-1530a0c1
evidence_runs:
  - experiment:a00-f766734a-7e1381
loop: hypothesis:l4b18-survival-modes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 68eb7d2d0d9f072b
season: 2
title: A00 f766734a 7e1381
verdict: inconclusive_lean_disproved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-f766734a-7e1381

## Experiment

Probe the current state of the mode-selection machinery to test whether
survival / ultimate survival are DECLARED IN CONFIG (the hypothesis claim:
"declared in config and rendered by brief.py, so the operating mode is
read, never remembered").

Commands run from the loop worktree:

1. Check `.agi/config.json` for any mode/survival key:
   `python3 -c "import json; c=json.load(open('.agi/config.json')); print('operating_mode' in c, 'survival' in c, 'ultimate_survival' in c); print([k for k in c.keys() if 'survival' in k or 'mode' in k] or 'NONE found')"`
2. Read the profile-selection path in `extensions/agi/bin/brief.py`
   (`PROFILES`, `survival_selected()`, the `assemble()` profile switch).

## Evidence

Config probe output:
```
False False False
top keys: NONE found
```
`.agi/config.json` has NO `operating_mode` / `survival` / `ultimate_survival`
key anywhere. Its top-level keys carry engine/harness/spawn/agent config only
(engine_commit, metric_primary, harnesses, agent_dispatch, cc_dispatch, ...).

`brief.py` (read directly, lines 55-80, 1446-1483):
- `PROFILES = ("full", "survival")` — only TWO profiles; `ultimate_survival`
  is not a value anywhere.
- `survival_selected()` (line 61-77): `profile = os.environ.get("AGI_BRIEF_PROFILE", "full")` — selection is **ENV-VAR ONLY**, no config source consulted.
- `assemble()` (line 1456-1464): same — `profile = os.environ.get("AGI_BRIEF_PROFILE", "full")`.

## Verdict

The hypothesis asserts the modes ARE declared in config. They are not. The
operating mode is still selected by `AGI_BRIEF_PROFILE` env var, defaulting to
`full`; no config key names the mode; `ultimate_survival` does not exist as a
value. Under the current snapshot the claim is FALSE — the very "remembered
via env, not read from config" gap the owner's own L4.26 note names remains
open. Config-declarable survival/ultimate-survival is the *designed* direction
but is not yet implemented.

Conclusion: lean_disproved at the current state. Strong confidence that the
claim is currently unsatisfied (config lacks the key; verified by direct
read). Weakness: the claim may be read as a forward design intent rather than
a present-tense fact; if so, the correct verdict is "not yet implemented,"
which this still captures — the machinery does not read a config declaration
today.

## Agent Notes
Config declares no operating mode; brief.py selects via AGI_BRIEF_PROFILE env only. ultimate_survival not a PROFILES value. Claim currently unmet.

Parent review accepted as survey run: config probe (no mode key) and brief.py env-only selection verified. Kept at lean_disproved:90 — correct against present-tense claim; superseded as state by the implementation run experiment:a00-b3efe756-4171e1 which proved the claim post-change.
