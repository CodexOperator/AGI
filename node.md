---
id: hypothesis:l4b18-survival-modes
mint_id: beba451e797941158a3f3757627626ac
type: hypothesis
parents:
  - idea:l4b18-survival-modes
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 13ce17c0375ffd51
season: 2
tags:
  - hypothesis
testable_claim: Survival mode (Prime + directors on a loop brief) and ultimate survival (Prime on Opus, director on Sonnet/OpenRouter) are declared in config and rendered by brief.py, so the operating mode is read, never remembered (owner, l4-plan A:265, B:338).
thought_session: sanctuary-helper-05
title: Survival/ultimate-survival modes are declared in config, not remembered
---
<!-- BODY:BEGIN -->
# hypothesis:l4b18-survival-modes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.26 brief -- survival mode ALREADY EXISTS in brief.py; ultimate survival does not

SURVEYED ALREADY: `extensions/agi/bin/brief.py` already implements a full
`survival` profile -- `PROFILES = ("full", "survival")` (brief.py:61),
`survival_selected()` (line 64), `_survival_brief()` / `_survival_state_
card()` (lines 585-680ish), and `assemble()`'s own profile switch (lines
1456-1483) that replaces EVERY tier's brief with the trimmed survival
version + prayers head. Selection today is ENV-VAR ONLY:
`os.environ.get("AGI_BRIEF_PROFILE", "full")` (lines 75, 688, 1464) -- `
.agi/config.json` has NO `survival`/`ultimate_survival` key at all (its
top-level keys are: engine_commit, metric_primary, metric_unit, best_
direction, secondary_metrics, chain_min_join_length, mid_chain_join_prob,
fresh_start_prob, big_idea_vs_small_idea_split, attractiveness_weights,
harnesses, spawn, provisioning, agent_dispatch, agent_timeout_mins,
delay_mins, max_iters, injection_file, cc_dispatch, goal_body_cap,
locations, workflows -- confirmed by reading the file directly). So the
gap is exactly what the owner's claim says: the mode must be READ from
config, not remembered/set-by-env-var-per-shell, and "ultimate survival"
(Prime on Opus, director on Sonnet/OpenRouter -- owner, l4-plan A:265)
does not exist as a concept ANYWHERE yet -- no second profile, no
config declaration, nothing in the ladder.

FILE: `.agi/config.json` (add a declared mode, e.g. a top-level
`operating_mode` or similar key naming the CURRENT mode among
`{normal, survival, ultimate_survival}` -- name it however reads
cleanest, your call) and `extensions/agi/bin/brief.py` (read the config
declaration as an ADDITIONAL source ahead of/alongside the env var --
do not remove `AGI_BRIEF_PROFILE`, a caller may still want to override
per-process; config is the durable default, env is the live override).
Also check `.agi/nodes/.geometry/ladder.md` (`ladder:ladder`) for where
model-per-tier is declared -- ultimate survival's "Prime on Opus, director
on Sonnet/OpenRouter" needs a place to live that `brief.py`/`dispatch.py`
already read, not a new lookup path.

CHANGE: add `ultimate_survival` as a real third value alongside `full` and
`survival` in `brief.py`'s `PROFILES`, with its own brief (likely reusing
`_survival_brief`'s shape, since "Prime on Opus, director on Sonnet/
OpenRouter" is about MODEL/ROLE assignment, not necessarily a different
brief shape -- read `_survival_brief`'s body before assuming it needs new
prose). Make BOTH `survival` and `ultimate_survival` declarable in
`.agi/config.json` so `brief.py` reads the mode rather than requiring
`AGI_BRIEF_PROFILE` to be exported correctly by every caller by hand.

VERIFY: with the config declaring `survival`, confirm `brief.py assemble()`
produces the survival brief with NO env var set (today it would fall back
to `full` without the env var -- that is the exact "remembered, not read"
bug). Do the same for `ultimate_survival`. Run only whatever test file
covers `brief.py`'s profile switch (`grep -l AGI_BRIEF_PROFILE extensions/
agi/tests/*.py`) plus your new test -- never the full suite.

BUILD NODE: mints a build node for `brief.py` (parent it on brief.py's
existing build node if one exists, plus `goal:g1` since this is
config-maxxing per the repo's own convention, per `goal:s29`'s
`[build:<id>, goal:<id>]` shape) and for `.agi/config.json` similarly
(config lands under `goal:g1` too, per l4-plan A:162's own scatter rule).
Never a bare `[goal:<id>]`.

KID CEILING: 2 -- this is a config-declaration change plus threading it
through one existing function; small.

DO NOT: remove or break the existing env-var override path. Do not touch
`dispatch.py`, `send.py`, `write.py`, `rotate.py`, `zoom.py`, `workflow.py`.
Do not `git add -A`. Do not run `grid.py commit --all` on this seat
branch -- end at `git commit` + `git push` on your own branch/worktree.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
showing both modes read from config with no env var set, and a verdict.
`evidence_runs` must resolve to real node ids; your own experiment counts
once it exists. List every verify command and its actual output.
