---
id: hypothesis:a01-0c63908f-245cab
mint_id: 56fb23c1c07548fea077c85660d8e9c3
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.6
edited_by: season.py
scaffold_hash: d1115dbf48c5d2bc
season: 1
thought_session: season
title: A01 0c63908f 245cab
verdict: pending
---
# hypothesis:a01-0c63908f-245cab

## Hypothesis

**Claim:** the drop-in-clone distribution shape's staleness gap (`goal:g8.1`,
inherited from L9) can be closed cheaply and independently of which of the
three shapes (clone / skill package / install) wins, by recording the engine
commit a project was cloned against in its own `.agi/config.json` (e.g.
`engine_pin: {commit: <sha>, checked_at: <date>}`) and having one read path —
`locations.py` or a small `bin/engine-pin.py` — compare it to the engine
clone's actual `HEAD` and print a non-fatal warning on mismatch.

Checked: `config.json` for this repo has no `engine_commit`/`engine_pin`
field today (grepped `.agi/config.json` and every `bin/*.py` for
`engine_commit|engine_version|pinned` — zero hits outside prose mentions of
"pinned" as an adjective), so the gap L9 found is still open as of
2026-09-03.

**What would prove it:** a project cloned against engine commit A, then the
engine advances to commit B, then a normal `driver.sh --smoke` run in that
project prints a visible drift warning naming both commits and does not fail
or block the run.

**What would disprove it:** the warning either fires on every run regardless
of drift (false positive, unusable) or never fires when the engine has
genuinely moved (silent staleness persists — the exact failure mode this is
meant to close), or implementing it requires touching `locations.py` in a way
that couples the pin check to one specific distribution shape (contradicting
"closes the gap regardless of the outcome" from `goal:g8.1`'s own text).

No experiment has been run yet — a sibling scaffold under this same goal
(`hypothesis:a01-abd43b16-1beb10`) records that both pi kids dispatched for
this goal on iteration 1042 hit `403 Workspace weekly budget of $10.00
exceeded` before producing content, so this claim is written directly by the
agent that got dispatch, not delegated further this iteration.


## Agent Notes
Sharpened engine-pin hypothesis under g8.1: record engine commit in config.json, warn non-fatally on drift, independent of which distribution shape wins. Confirmed no engine_commit/pin field exists yet. No experiment run this iteration.