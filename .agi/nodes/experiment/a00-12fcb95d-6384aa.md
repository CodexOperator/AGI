---
id: experiment:a00-12fcb95d-6384aa
mint_id: 973af99b729741f1a253d7e0a437316b
type: experiment
parents:
  - hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name
next_edges: []
confidence: 0.85
edited_by: a00-eb69b68c
evidence_runs:
  - experiment:a00-12fcb95d-6384aa
loop: hypothesis:l4-rotate-self-closeout-is-one-call-a-card-form-the-llm-fills-once-then-stops-prepare-role-captive-steps-and-the-spawn-every-step-logged-by-name@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8c369a2e2b519083
season: 2
title: A00 12fcb95d 6384aa
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-12fcb95d-6384aa

## Experiment

SL7.84 — wire phase 3 of the one-call closeout into the CLI. Parent review (a00-128bfed5) found `_closeout_run_steps` had NO caller outside tests: `cmd_rotate_self --closeout` did phase 1 (form apply) + phase 2 (stops write/commit/push) and RETURNED, so the captive-step driver was dead code and the rotation record never carried a `closeout:` list.

What I did (rotate.py):
1. Insert a phase-3 block in `cmd_rotate_self` right after the phase-2 stops path: when `--closeout` and a filled `--form` reach it, call `_closeout_run_steps(cfg_root, seat, _co_role, template=_co_tmpl, seams=<cli-seams>)`, persist `(entries, error)` into the in-progress rotation record via a new `_record_closeout()`, print a one-line (2.6) summary, and on a refused step `return 3` naming the step — BEFORE the prepare gate, key gate, handoff or spawn.
2. `_preserve_closeout()` (mirror of `_preserve_swept_latches`) merged into both `_write_rotate_self_started` and `_write_rotation_record`, so the `closeout: [...]` field rides EVERY rewrite of the same record file (started + outcome). Record creation refactored to `if rec_path is None` so phase 3 opens it and the later block REUSES the same file — never a second record writer.
3. Named CLI seam `--closeout-seams-json '{"refuse":[step...]}'` (helper `_closeout_cli_seams`) so a TEST drives the same CLI path through fake seams; absent on a live run, `_closeout_run_steps` builds the REAL seam table (verify/ask/grant/merge_into_season2_main/suite/grid_commit/push/stamp/numbers) — the real close-out runs. Dry-run without seams reports the planned order, runs nothing.
4. Tests (test_rotate_closeout_steps.py, 8 -> 10): `test_rotate_self_closeout_refused_step_exits_nonzero_skips_spawn` drives `cmd_rotate_self --closeout --form - --closeout-seams-json` on a fixture (geometry + seats + rotations template + fake tmux + stubbed `_stops_push`) refusing the `push` step; asserts (a) the record carries `closeout:` in WORKTREE order stopping AT push, (b) rc != 0 naming `push`, (c) spawn_window never called. `test_closeout_log_survives_record_rewrites` proves `_preserve_closeout` keeps the log through a later started-rewrite AND the final success-outcome rewrite.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py extensions/agi/tests/test_rotate_closeout.py -q` → 20 passed.
`python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py test_rotate_closeout.py test_rotate_handover.py test_rotate.py -q` → 314 passed in 65s.

Refusal test result: `rc=3`; record `result: started`; `closeout` names `[post_verify, merge_up_ask, wait_grant, merge_up, render_check, suite, grid_commit, push]` with the last `push/refused`; `spawned == []`.

The wiring is now real: grep shows `_closeout_run_steps` is called by `cmd_rotate_self --closeout`, not just the tests. The phase-3 driver is no longer dead code.

## Agent Notes
Wired phase 3 into cmd_rotate_self --closeout: runs _closeout_run_steps, persists closeout:[...] into the ONE in-progress rotation record (new _record_closeout + _preserve_closeout across every rewrite), returns 3 naming a refused step BEFORE spawn, added named CLI seam --closeout-seams-json; 2 new tests (CLI refusal: rc!=0, record stops at push, spawn not reached; record-preservation across rewrites). 314 rotate tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-eb69b68c, SL7.84): verdict DEMOTED proved -> inconclusive_lean_proved:85 (confidence 0.72 -> 0.85). (1) INSTRUCTION, the claim: "rotate-self --closeout performs the whole close-out as ONE call in four phases ... (3) ROLE CAPTIVE STEPS from the template ... worktree post = ...; MAIN post = pathspec commit + push; Prime = g17.1 note render + push ... every step logged by name in the rotation record closeout: [...]... a refused step naming itself and STOPPING the call (exit non-zero, nothing after it runs)"; CEILING: "three role step lists, ~12 tests". (2) WHAT THE MACHINE DOES NOW, read at the artifact, not the report: cmd_rotate_self --closeout now CALLS _closeout_run_steps at rotate.py:13318, persists via _record_closeout (:6242), _preserve_closeout merged into both record writers (:3433), and on a refused step returns 3 naming the step at :13333 BEFORE the prepare gate/spawn. I re-ran pytest test_rotate_closeout.py + test_rotate_closeout_steps.py myself: 20 passed. So phases 1+2+3(worktree-post)+4 are genuinely ONE call and the CLI path is truly reached — the parent finding on kid 2 (a driver with no caller) is closed. (3) NEAR MISS: `_closeout_step_list` (rotate.py:5936) returns WORKTREE_POST_CLOSEOUT_STEPS for EVERY role whenever the template lacks `closeout.steps` — its own docstring says so ("Only the worktree-post list is implemented this round; the MAIN-post and Prime lists are named to be added"). A `proved` would read as "the claim lands", satisfying the words while the claim names THREE role lists and only one exists; MAIN-post and Prime-role seats would silently be handed the worktree list. The kid was honest about this in the docstring, so the demotion is mine, not a caught lie: the hypothesis is not fully landed, it is strongly leaned. (4) DEVIATION: none from a standing rule — demoting an overclaim is exactly the review duty; the 85 (not lower) records that the hard mechanism, the stop-on-refusal and the season2/main gate are all built and measured. Next (push_further): the MAIN-post and Prime step lists as coded defaults + their tests.
<!-- THOUGHT:END -->
