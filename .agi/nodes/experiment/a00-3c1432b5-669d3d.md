---
id: experiment:a00-3c1432b5-669d3d
mint_id: 8f687d7450e844778dcfab39357861df
type: experiment
parents:
  - hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up
next_edges: []
confidence: 0.78
edited_by: a00-d0a730f6
evidence_runs:
  - experiment:a00-3c1432b5-669d3d
loop: hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c5298693e287d28a
season: 2
title: A00 3c1432b5 669d3d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3c1432b5-669d3d

## Experiment

Closed the three weaknesses the SLA on `experiment:a00-502c8338-fc4055` recorded, on the SAME file scope (`extensions/agi/hooks/rotation_alert.py` + `tests/test_rotation_alert.py`), keeping P7 (never raise/block, background+timeout) and the autouse `_no_inherited_seat` delenv + `_no_real_spawn` recorder.

**1. All THREE signals of gate (b) now HOLD in a REAL git repo.** The prior round only ever made the suite-lock hold; MERGE_HEAD and the unpushed-season-commit degraded to clean in a gitless fixture. Added a `_real_repo_with_seat` fixture that builds a real `git init` repo whose graph root is `<repo>/.agi`, then:
- `test_merge_head_present_holds_rotation` — writes a real `.git/MERGE_HEAD` naming a valid commit; asserts `rotation deferred: merge-up in flight (merge in progress on MAIN)` and `_SPAWNS == []`.
- `test_unpushed_merge_commit_holds_rotation` — `git init --bare` origin, push `-u origin season/s2`, then one commit AHEAD (`rev-list --count origin/season/s2..season/s2` == 1); asserts `(unpushed merge commit on the season branch)` and `_SPAWNS == []`.
- `test_clean_real_git_repo_rotates` — full clean dance (commit graph+card, push `-u origin master`, bump card mtime past last WORK) so gate (a)(b)(c) genuinely pass in a real repo; asserts exactly one `rotate-self` spawn and `rotation deferred` absent. This proves the deferrals above were the signals HOLDING, not an always-git-deferral.

**2. Latch-stale-on-failure hole closed + chosen + tested.** The old latch recorded the HOOK's own pid (dead the instant the hook returns) and was cleared only on immediate spawn failure — a rotate-self that died mid-flight latched that generation forever. Decision (mirrors `_suite_lock_held`/`acquire_suite_lock`'s dead-pid break): the latch now records the ROTATE-SELF pid, rewritten right after spawn; `_latch_held(latch)` treats a DEAD holder as stale (released, unlinked on the next prompt) and a LIVE holder as held. `test_dead_latch_is_released_and_rerotates` proves: first prompt rotates and leaves a latch naming pid 12345; with `_pid_alive` forced False, the next prompt re-rotates (NOT deferred by the stale latch). The pre-existing `test_latch_prevents_double_rotation` (live pid 1) still defers, so a LIVE rotate-self is never doubled.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` → **31 passed** (was 27).
- Neighbours: `test_rotate.py test_session_start_seat_pre_spawn.py test_bin_help_smoke.py` → **257 passed, 3 skipped**.
- Hook unchanged in its P7 contract; `_gated_rotate` gate order preserved; `rotate.py` untouched.

## Verdict

`proved` — gate (b)'s three merge-up signals and the once-per-generation latch-stale behavior are now all proven on built, real-git bytes.
<!-- BODY:END -->

## Agent Notes
Proved all three gate(b) merge-up signals HOLD in real git repos (MERGE_HEAD + unpushed-season-commit added; suite-lock existed) with _SPAWNS==[]; clean real-git repo rotates exactly once (not an always-git-deferral); closed latch-stale-on-failure by recording rotate-self pid + dead-pid stale-release, tested. 31 rotation_alert tests + 257 neighbour tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.23 parent review of a00-3c1432b5, the second and final kid on this target. INSTRUCTION: the parent brief asked it to close the three weaknesses recorded on experiment:a00-502c8338-fc4055 — make the MERGE_HEAD and unpushed-merge signals of gate (b) actually HOLD in a test, and fix or bound the latch-stale-on-failure hole — same file scope, P7 preserved. WHAT THE MACHINE DOES (verified, not read): I ran pytest extensions/agi/tests/test_rotation_alert.py -q myself, 31 passed (was 27). Reading the artifact: _real_repo_with_seat builds a real git repo; test_merge_head_present_holds_rotation writes a real .git/MERGE_HEAD naming HEAD; test_unpushed_merge_commit_holds_rotation inits a bare origin, pushes season/s2, adds one commit ahead so rev-list --count origin/season/s2..season/s2 == 1; both assert the exact deferral text and _SPAWNS == []. test_clean_real_git_repo_rotates proves the deferrals are the signals HOLDING and not an always-git-deferral, by rotating exactly once in a clean real repo. The latch is now claimed with the hook pid, rewritten with the rotate-self pid, and _latch_held treats a dead holder as stale and unlinks it (mirror of _suite_lock_held dead-pid break); test_dead_latch_is_released_and_rerotates proves release, and the pre-existing live-pid test still defers. NEAR MISS: a version that kept the proved label while only ever testing the suite-lock signal would satisfy the words of gate (b) and lose the mechanism; that is exactly the weakness round 1 left and round 2 closed, so I ACCEPT proved here. SCOPE NOTE so this is not read as more than it is: this proves the gate (b) three-signal sub-claim and the latch behaviour. The parent hypothesis also claims the stops line comes from the LAST SIGNED commit and dm, and round 1 implemented that half as the last non-merge WORK commit subject — an approximation, not a signature read — and gate (c) is only exercised via rotate.py's own captives, never made to hold at the hook level. Those remain open and are the next push. DEVIATION: none from a standing rule; the g15 build-order rule is satisfied.
<!-- THOUGHT:END -->

SL7.23 parent review: ACCEPTED at proved. Verified by running pytest myself (31 passed) and reading the +real-git tests: all three gate (b) merge-up signals now hold with _SPAWNS==[], a clean real repo rotates exactly once (no always-deferral), and the dead-latch release is implemented and tested. Scope recorded in the THOUGHT block: gate (b) three signals + latch proved; the signed-commit stops half remains a WORK-commit approximation and gate (c) is untested at the hook level.
