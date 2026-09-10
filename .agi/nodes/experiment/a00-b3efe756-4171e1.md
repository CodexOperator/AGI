---
id: experiment:a00-b3efe756-4171e1
mint_id: 14d95dfcc5be4f73adb54283a3879ee2
type: experiment
parents:
  - hypothesis:l4b18-survival-modes
next_edges: []
confidence: 0.9
edited_by: a00-1530a0c1
evidence_runs:
  - experiment:a00-b3efe756-4171e1
loop: hypothesis:l4b18-survival-modes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a14d631996bc0567
season: 2
title: A00 b3efe756 4171e1
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b3efe756-4171e1

## Experiment

Implementation pass on `hypothesis:l4b18-survival-modes` (the parent's prior
run `experiment:a00-f766734a-7e1381` surveyed and confirmed the gap: no
`operating_mode` key in `.agi/config.json`, `AGI_BRIEF_PROFILE` env-only
selection, `ultimate_survival` absent from `PROFILES`). This run makes the
hypothesis true — config declares the mode, brief.py reads it.

### Changes made

1. `extensions/agi/bin/brief.py`
   - `PROFILES = ("full", "survival", "ultimate_survival")` — third value added.
   - New `_configured_profile(project_root=None)`: reads `.agi/config.json`
     `operating_mode` (values full|survival|ultimate_survival), returns one of
     PROFILES or None. Config is the durable default.
   - New `_effective_profile(profile=None, project_root=None)`: the single
     resolution switch — explicit `profile` kwarg > `AGI_BRIEF_PROFILE` env
     (per-process override, NOT removed) > config `operating_mode` > `full`
     (historical).
   - `survival_selected()` now goes through `_effective_profile` and returns
     True for BOTH `survival` and `ultimate_survival` (adapters drop the
     graph-viewport stream for either).
   - `assemble()`'s `profile == "full"` resolution block now calls
     `_effective_profile()` (was bare env read). Its survival short-circuit
     now matches `profile in ("survival", "ultimate_survival")` —
     `ultimate_survival` reuses `_survival_brief`'s shape because the mode
     is about MODEL/ROLE assignment (Prime on Opus, director on
     Sonnet/OpenRouter), not new prose.
   - `successor_prompt()` updated to the same switch + both-value match.
2. `.agi/config.json` — added `"operating_mode": "full"` (the key now
   exists and is declared; set to `full`, NOT survival/ultimate_survival, so
   no live agent's brief changes. Switching is a one-edit change).
3. `extensions/agi/tests/test_brief.py` — six new tests: config declares
   `survival` with env unset → survival brief; same for `ultimate_survival`;
   env override wins over config (both directions); `survival_selected()`
   True for both modes; `successor_prompt` honors config-backed
   `ultimate_survival`.

### Verify commands + actual output

1. Full engine suite (repo's own claim, not just my scratch test):
   `python3 -m pytest extensions/agi/tests/ -q`
   → `2276 passed, 1 skipped in 133.33s`
2. The six new tests specifically:
   `python3 -m pytest extensions/agi/tests/test_brief.py -q -k "config_operating_mode or env_override or ultimate_survival or both_survival_modes"`
   → `6 passed, 89 deselected in 0.14s`
3. Live probe — config declares the mode and env is unset, so resolution is
   config-driven:
   `env -u AGI_BRIEF_PROFILE python3 -m pytest extensions/agi/tests/test_brief.py -q -k "config_operating_mode_survival_no_env or config_operating_mode_ultimate_survival_no_env"`
   → both pass (each asserts `SURVIVAL PROFILE in s` with no env var set,
   driving the mode from the monkeypatched config reader).
4. Config file integrity + declared value:
   `python3 -c "import json; c=json.load(open('.agi/config.json')); print(c['operating_mode'])"`
   → `full`

## Evidence

The hypothesis's claim — "declared in config and rendered by brief.py, so
operating mode is read, never remembered" — is now TRUE: `.agi/config.json`
declares `operating_mode`, brief.py reads it as the durable default, env
remains the override, and `ultimate_survival` renders the survival brief via
the same single switch. The env-var path is intact (precedence test asserts
`full` brief when env says `full` even with config declaring `survival`).
`dispatch.py`/`send.py`/`write.py`/`rotate.py`/`zoom.py`/`workflow.py`
untouched; no `git add -A`; no `grid.py`.

## Agent Notes
Added ultimate_survival as third PROFILES value; config reader operating_mode in .agi/config.json (set to full); env AGI_BRIEF_PROFILE retained as override; 6 new tests, full engine suite 2276 passed.

Parent review accepted: verified brief.py carries _configured_profile/_effective_profile with ultimate_survival in PROFILES; config.json declares operating_mode=full; 6 new tests pass (6 passed in 0.13s); env-var override intact. Verdict proved stands — evidence run resolves (self, per experiment rule).
