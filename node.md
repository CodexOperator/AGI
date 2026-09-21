---
id: experiment:a00-a8449c51-8f6f88
mint_id: b2b2aa08905c4e1da9e415153f4a4110
type: experiment
parents:
  - hypothesis:l3w4-masters-rollover
next_edges: []
confidence: 0.9
edited_by: a00-e1fc33bf
evidence_runs:
  - experiment:a00-a8449c51-8f6f88
loop: hypothesis:l3w4-masters-rollover@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7f89f8428426721e
season: 2
title: A00 a8449c51 8f6f88
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a8449c51-8f6f88

## Experiment

Implemented the Masters rollover handoff for hypothesis:l3w4-masters-rollover,
red-first, and proved it live.

**Edited `extensions/agi/bin/season.py`:**
1. Fixed the clobber bug: `rollover --name` wrote `season_names[1] = name`
   (L880 print, L956 write) — a second rollover silently destroyed season 1's
   name. Now `season_names[season] = name`, the closing season's own key.
2. `judge` and `rollover` gained `--actor SEAT --session S` (mirroring
   `retag`), falling back to the current literals (`season.py`/`season`) when
   omitted.
3. `cmd_judge` threads them into its judgment write; `cmd_rollover` threads
   them into the ladder-bump write only — `_mint_vision`'s `edited_by:
   "owner"` untouched.

**Added to `extensions/agi/tests/test_season.py`:**
- `test_second_rollover_names_its_own_season_and_attributes_each_write` (the
  GATE): rehearse 1→2 (`--name genesis --actor sanctuary-master`) then 2→3
  (`--name wave-4-masters --actor sanctuary-master`); asserts
  `season_names == {1:"genesis", 2:"wave-4-masters"}` (today: genesis
  clobbered), `current_season == 3`, and ladder `edited_by ==
  "sanctuary-master"`.
- `test_judge_actor_stamps_edited_by`: `judge <id> --against <plan>
  --actor glitch-master --session season-3` leaves `edited_by=="glitch-
master"`, `thought_session=="season-3"` on the outcome.

## Evidence

**RED first (current season.py, both new tests):**
- `usage: season.py ... error: unrecognized arguments: --actor sanctuary-master`
  and `--actor glitch-master` → `returncode 2`, both failed.

**GREEN after the fix:**
```
1 passed in 0.68s   (second_rollover_names_its_own_season_and_attributes_each_write)
1 passed in 0.40s   (judge_actor_stamps_edited_by)
```

**Full suite (`python3 -m pytest extensions/agi/tests/ -q`):**
```
2053 passed, 1 skipped in 122.98s
```
Season-1 rollover/genesis tests untouched and green. No new frontmatter field
added — `grid.py diff ladder:ladder` shows `edited_by` change seat by seat.
No writes to `.agi/nodes/.geometry/seats.md`; no seat row installed (per the
standing prohibition, this experiment builds the mechanism and stops).

## Agent Notes
Fixed season_names[1] clobber (now [season]); judge+rollover gained --actor/--session threading the seat into edited_by; GATE test red-before/green-after, full suite 2053 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-e1fc33bf, L3.38): accepted as proved. Verified in tree, not from the report — season.py diff shows season_names[season] = name at the write site (the [1] clobber is gone) and --actor/--session on both p_judge and p_rollover with literal fallbacks; test_season.py carries the red-first gate test plus judge-attribution test, 39/39 green on re-run; links.py shows 0 broken. Evidence_runs self-citation is legal (an experiment IS the run). Caveat kept honest: red-first failure output is quoted from the kid only, not reproduced here — accepted because the gate test asserts exactly the today-broken state (genesis clobbered) and now passes.
<!-- THOUGHT:END -->

Parent review passed: diff inspected, tests re-run green, verdict proved stands.
