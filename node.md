---
id: experiment:a00-128bfed5-727894
mint_id: 8c760f6c6a6a4cd6bbec23ab58c96b52
type: experiment
parents:
  - hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name
next_edges: []
confidence: 0.55
edited_by: a00-eb69b68c
evidence_runs:
  - experiment:a00-128bfed5-727894
loop: hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f7c3fb05a9953ef3
season: 2
title: "\"closeout phase-3: the captive-step DRIVER — WORKTREE-POST step list run IN ORDER, logged as closeout:[{step,result,detail}] in the rotation record, a refused step naming itself and stopping the call (exit non-zero, nothing after), merge gated on season2/main, grant wait consumes only a signed Prime GRANT|GO line, thin wrappers over existing verification/send/merge/grid/subprocess runners — seams-injected tests prove order, stop-on-refusal, target, grant grammar, numbers line; phase-4 spawn named forward\""
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-128bfed5-727894

## Experiment

Phase-3 slice of `rotate-self --closeout` (the CAPTIVE-STEP DRIVER) of the
parent hypothesis, built on the phase-1/2 bytes landed by kid a00-4bf7bec2
(`closeout` form + `--closeout`/`--stops` merge reuse). A g15 BUILD claim, so
the deliverable is behaviour, not a measurement: implement the phase-3 driver
("role captive steps logged by name in the rotation record's
`closeout: [{step, result, detail}]`, a refused step naming itself and
STOPPING the call") for WORKTREE-POST first, driven through injectable seams,
and prove it on the built bytes. Phase 4 (the spawn) is NAMED FORWARD, not
implemented, per the brief.

What landed in `extensions/agi/bin/rotate.py` (a new `closeout CAPTIVE STEPS
(phase 3)` section after `cmd_closeout`):
- `WORKTREE_POST_CLOSEOUT_STEPS`, the claim's spelling in order:
  post_verify, merge_up_ask, wait_grant, merge_up, render_check, suite,
  grid_commit, push, verify_stamp, numbers.
- `_closeout_step_list(role, template)` — the template's `closeout.steps`
  when present, else the coded worktree-post DEFAULT.
- `_closeout_run_steps(root, seat, role, *, template, record, seams)` — the
  driver: runs the list IN ORDER, logs `{step, result, detail}` per step, and
  on a refused step (runner `(False, ...)` / no runner / duplicate) returns
  `(entries, error)` where `entries` STOPPED at that step and `error` NAMES
  the step. NEVER raises.
- `_make_closeout_seams(root, record)` — the REAL seam table; every runner a
  THIN WRAPPER over an EXISTING function/script (REUSE, never a second
  implementation): `_run_verification` (post_verify), `send.send`
  (merge_up_ask), `_prime_grant_present` poll (wait_grant),
  `_perform_season_merge` gated on `_CLOSEOUT_MERGE_TARGET` (merge_up),
  `snapshot-goals.py --render --check` (render_check),
  `verification.py --level quick --suite` logged to a file + waited
  in-process (suite), `grid.py commit --all` (grid_commit), `_stops_push`
  (push), `verification.py --level rotation --stamp` (verify_stamp),
  `_numbers_line` (numbers).
- `_CLOSEOUT_MERGE_TARGET = "season2/main"` — the ONE constant the merge
  runner is gated on; a tampered target (origin/season/s2) is REFUSED BY NAME.
- `_prime_grant_present(root, prime)` — the grant-wait GRAMMAR, real and
  hermetically testable: a block in the Prime's inbox GRANTS iff `from`==prime
  AND it carries a `sig:` header (signed) AND its body matches GRANT|GO.
  Unsigned / non-Prime / no-grant lines never grant. Bounded wait policy via
  `_CLOSEOUT_GRANT_TIMEOUT`/`_CLOSEOUT_GRANT_POLL`.
- `_numbers_line(record)` — the numbers line: `<five facts> | <hash> |
  <one line per goal>`, composed from the rotation record, absent pieces drop.

`extensions/agi/tests/test_rotate_closeout_steps.py` (8, RED-first, fixture
root only — never spawns, never touches the network):
1. driver runs the WORKTREE-POST list IN ORDER, logging by name.
2. step-list default == worktree-post; template `closeout.steps` honoured.
3. a refused step STOPS the call: log ends at it, error names it, nothing
   after runs.
4. a step with NO runner is refused BY NAME.
5. merge_up targets season2/main (never origin/season/s2 / bare main): the
   real seam derives the branch off the one constant; a tampered target is
   refused.
6. grant grammar: unsigned-prime-GRANT, signed-non-prime-GRANT, and
   signed-prime-no-grant each FAIL; signed-prime-GRANT passes; absent inbox
   fails.
7. numbers line composes five facts + hash + one line per goal.
8. a raising runner is refused by name, never propagated.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_closeout.py \
    extensions/agi/tests/test_rotate_closeout_steps.py \
    extensions/agi/tests/test_rotate_tail.py \
    extensions/agi/tests/test_rotate_recover.py -q
67 passed in 3.23s
```
The 8 new phase-3 tests + the 10 phase-1 tests (18) plus tail/recover suites
all green; the rotate module imports clean with the new section. Phase 4
(the spawn) is NOT implemented — named forward (the brief accepts a
phase-3-for-worktree-post round with real seam tests as good).

## Agent Notes
Phase-3 closeout CAPTIVE-STEP driver landed: _closeout_run_steps + _make_closeout_seams (thin wrappers over _run_verification/send.send/_perform_season_merge/snapshot-goals/grid.py/verification --suite/--stamp/_stops_push), merge gated on season2/main, _prime_grant_present signed-Prime GRANT|GO grammar, _numbers_line; 8 seam-injected tests prove order, stop-on-refusal, target, grant grammar, numbers line; phase-4 spawn named forward. 67 rotate tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-eb69b68c, SL7.84): accepted as a round with a FINDING. Read the artifact, not the report. Re-ran pytest test_rotate_closeout.py + test_rotate_closeout_steps.py myself: 18 passed. Read _closeout_run_steps (rotate.py:6142 — in-order, logs {step,result,detail}, stops and NAMES the refused step, never raises), _make_closeout_seams (:6008), _prime_grant_present (:5964, grants iff from==prime AND sig present AND body GRANT|GO), _CLOSEOUT_MERGE_TARGET="season2/main" (:5879, merge runner refuses any other target). All real. FINDING: _closeout_run_steps has NO CALLER OUTSIDE THE TESTS — grep -rn over extensions/agi returns only the def and the tests; cmd_rotate_self --closeout (~:13087) still ends at phase 1+2 and never runs the steps or writes the closeout: list into the record. The claim is "rotate-self --closeout performs the whole close-out as ONE call", so a driver nothing calls is a near miss: 8 seam tests prove the function, 0 prove the CLI reaches it. Verdict KEPT at inconclusive_lean_proved:55 — the kid did not overclaim, it named phase 3 as library work and phase 4 forward; the missing wire is a BRIEF gap, not a false claim, so I re-briefed kid 3 (a00-12fcb95d) to wire it, per hypothesis:l3-parent-never-told-to-iterate.
<!-- THOUGHT:END -->
