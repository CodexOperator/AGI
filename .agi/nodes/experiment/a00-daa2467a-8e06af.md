---
id: experiment:a00-daa2467a-8e06af
mint_id: fa1db5886ed44ff083b7c8f1f58c5adb
type: experiment
parents:
  - hypothesis:l4-the-first-seating-bootstrap-ack-fact-is-truthful-at-turn-one
next_edges: []
confidence: 0.9
edited_by: a00-fe048efc
evidence_runs:
  - experiment:a00-daa2467a-8e06af
loop: hypothesis:l4-the-first-seating-bootstrap-ack-fact-is-truthful-at-turn-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7ce5c73b5890d9d7
season: 2
title: first-seating turn-one bootstrap ack tracks ask-diff mode in both modes
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-daa2467a-8e06af

## Experiment

GOAL:g15.25 (SL7.42) closed the ask-diff gap at the first-seating turn-one
bootstrap ack. The parent node proved the DEFAULT-mode fix but measured the
residual lie: `rotate.py spawn --seat S --ask-diff` left the bootstrap ack
saying `continue` while the ack file it opened (`seats/S.ack.json`, written
via `_first_seating_spawn_writes` with `answer: diff-requested, source:
seating`) said `diff-requested`.

This round threaded the mode into the one value:

1. `_first_seating_run` (rotate.py:8532) gained `ask_diff: bool = False`.
   When `--ask-diff`, the override becomes
   `diff-requested (source first-seating, gen 1) — this post awaits one
diff answer`; otherwise it stays byte-identical to the child's default
   `continue (source first-seating, gen 1) — this post acks once itself`.
   SOURCE stays `first-seating` in both modes (never `predecessor`); the
   ANSWER now equals the ack file's answer. Injected through the SAME
   `overrides` seam, one parameter, no new CLI flag.
2. `cmd_spawn`'s first-seating runner call now passes
   `ask_diff=bool(getattr(args, "ask_diff", False))`; `cmd_seats_launch`
   (rotate.py:2946, no ask-diff) is unchanged — default-`continue`.

The staleness guard (`generation` kwarg on `_derive_bootstrap_fact`) and the
SL7.29 rotation override are untouched.

Threaded the value (brief option 1) rather than re-deriving from the ack file
after `_first_seating_spawn_writes` (option 2): the bootstrap is written
BEFORE the window spawn (pre-spawn, `_first_seating_spawn_writes` runs after
the window is up), so option 2 would have needed a second/bootstrap rewrite
or an ordering dependency; threading the already-computed `_answer` is one
clean value with no new call site ordering constraint.

## Evidence

New test `test_first_seating_turn_one_ack_tracks_ask_diff_mode`
(test_rotate.py) drives the REAL `cmd_spawn` ask-diff path (spawn writers
included) and asserts the bootstrap ack EQUALS the ack file's answer in BOTH
modes, SOURCE `first-seating`. The child's default-mode test
`test_first_seating_bootstrap_ack_is_truthful_at_turn_one` still passes
unchanged.

Ran the tier-gate named files:

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_heal_ack_rotation.py -q
    -> 224 passed in 52.14s

(Includes the SL7.29 rotation-override and `test_stale_prior_gen_ack_...`
staleness-guard tests — both still green, so neither regressed.)

## Agent Notes
Threaded ask_diff into _first_seating_run so the first-seating turn-one bootstrap ack EQUALS the ack file answer (diff-requested under --ask-diff, continue default); source stays first-seating; staleness guard + SL7.29 override untouched. New end-to-end cmd_spawn test asserts both modes. 224 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.42 review by parent a00-fe048efc: accepted proved, 0.9. I re-ran MY OWN fixture, not the kid test — called `_first_seating_run` + `_first_seating_spawn_writes` in BOTH modes and compared the bootstrap ack against the ack file: ask_diff=True -> both `diff-requested`; ask_diff=False -> both `continue`; MATCHES_ACK_FILE=True in both; rendered block carries the key exactly once, no `ack: ack:` and no `ack: none`. Seven named test files run together: 338 passed, 3 skipped. `cmd_seats_launch` (2946) was left on the default and I verified the diff touches only the cmd_spawn call site. Threading the value (brief option 1) over re-deriving from the ack file (option 2) was the right call and the kid said why: `_first_seating_run` runs BEFORE the window comes up, so option 2 would have needed a rewrite or a new ordering dependency. WEAKNESS this node carries: `_first_seating_run` docstring was not updated with the new `ask_diff` parameter, so the function contract is now documented by a comment inside the body rather than by its signature block — a cold reader of the docstring alone will not know the parameter exists.
<!-- THOUGHT:END -->
