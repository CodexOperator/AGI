---
id: experiment:a00-9ae2377e-e71a92
mint_id: aaae0a49b2314b66af0ec9d2c73d4146
type: experiment
parents:
  - hypothesis:l4-a-finished-rounds-session-dir-comes-home-before-the-sweep-judges-it
next_edges: []
confidence: 0.72
edited_by: a00-a4073def
evidence_runs:
  - experiment:a00-9ae2377e-e71a92
loop: hypothesis:l4-a-finished-rounds-session-dir-comes-home-before-the-sweep-judges-it@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 66c24c989a12d8b4
season: 2
title: A00 9ae2377e e71a92
town: core
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-9ae2377e-e71a92

## Experiment

Built the claim's bring-home step and proved it on the built bytes (g15 CLIMB:
measure → IMPLEMENT → prove on built bytes, not just reproduce the defect).

**What I changed (FILE SCOPE exactly as scoped, `_watch` untouched):**

1. `extensions/agi/bin/heal.py` (only `_sweep_finished_worktrees` + one new
   helper `_sweep_bring_home`, plus module constants):
   - Added `_sweep_bring_home(root, main_sessions, iter_name, dry_run, homed)`
     that lazy-imports `cli`, calls `cli._session_complete(root,
     locations.iteration_id(iter_name), worktree=None, dry_run=dry_run)` with
     stdout captured via `contextlib.redirect_stdout`, memoized in `homed`
     keyed by iter dirname (one call per iteration per pass, so a `--branch`
     round's TWO trees merge into ONE target). On refusal it reduces the
     captured stderr stdout to a short reason (`non-terminal` | `target
     exists` | `live lease` | `verify failed` | `home failed`). Decision: dry-run
     by "WOULD migrate present and no REFUSE"; live by the on-disk target,
     never a return code.
   - Reordered the per-worktree checks in `_sweep_finished_worktrees`: the
     GRACE check moved AHEAD of the bring-home step (home only a past-grace
     round; a young round is `kept: grace`, never homed → (e)). A not-home
     round's iter dirs are then homed; a post-home disk re-read decides
     removal, and a refused home leaves the worktree `session dir not home`.
   - NEW pre-resolve of each worktree's BASE at the top of the sweep
     (read-only, before any home). A `--branch` round's single merge-home
     removes the iter dir from EVERY tree it was found in, so a second tree's
     session records are gone by its turn in the loop; pre-resolving keeps a
     second tree's ancestry provable in the same pass → (d) `removed=2`.
   - `extensions/agi/bin/cli.py`: header comment gained the one sanctioned
     caller sentence. NO code change.
2. `extensions/agi/tests/test_heal_sweep.py`: extended with (a)(b)(c)(d)(e)
   (fixture = real git main repo + loop worktrees + fake leases, mirroring
   test_session_complete.py's terminal-agent record shape for
   `_iteration_agents_complete`).

**Actual outputs:** `test_heal_sweep.py` 10 passed (5 pre-existing + 5 new);
`test_heal_sweep` + `test_session_complete` + `test_heal_watch` + `test_heal`
collectively 56 passed. `py_compile` clean on both edited files.

## Evidence

- (a) dry-then-live: merged+clean+leaseless+past-grace+not-home → dry-run logs
  `[sweep] homed a00-eeee55 iter=iter-501` then `removed ... base=season/s2
  (dry-run)` and writes nothing under `<main>/.agi/sessions/` (spawn-budget
  lock aside, which every budget reader touches); live pass materialises
  `<main>/.agi/sessions/iter-501/manifest.json` + `a00-eeee55/agent.json`,
  removes the source dir from the worktree, removes the worktree, and the
  `loop/e-E@2` branch survives.
- (b) one non-terminal record → `[sweep] refused ...: session dir not home`
  (`non-terminal`); nothing migrated, worktree kept. session-complete's OWN
  completeness guard is the authority, never bypassed.
- (d) two worktrees carry the same `iter-504`: `calls == [False]` — exactly
  ONE live session-complete call (memo asserted), BOTH worktrees removed in
  the same pass, both trees' contributions landed in the union target.
- (e) complete-but-not-home round younger than a large grace → `kept=1`,
  NOT homed, worktree kept (director's hand harvest window not raced).
- (f) the sweep's original 5 tests pass unchanged.

**Finding / deviation (claim (c) not met, safely deviated):** the claim
expected a pre-existing NON-EMPTY main target to be `refused: target exists`.
That is NOT reachable within one sweep pass as specified: a target present on
disk at the moment `not_home` is computed is (per the baseline (f) homed-fixture
contract) already "home", so the sweep skips the home step and reaps the
worktree — the foreign bytes are never overwritten (session-complete refuses
and the sweep never writes a target), but the worktree IS removed. Distinguishing
a foreign target from a legitimate home by filesystem alone is impossible while
the homed-fixture (f) case (source + target both present) must stay removable.
Test (c) is pinned to the invariant the falsifier actually names — the foreign
target's bytes are byte-identical after the pass — and documents the removal
verdict as a baseline deviation. Net: column (c)'s "refused" expectation is a
real (safe) miss; everything else in the claim holds on the built bytes.

## Agent Notes
Built bring-home in heal.py sweep (helper _sweep_bring_home calls cli._session_complete once per iter via homed memo; grace moved ahead; bases pre-resolved so a --branch round's 2nd tree stays provable). 10 sweep tests pass (5 new); 56 pass across related suites. Claim (c) foreign-target 'refused' NOT met: an on-disk target is 'home' per the (f) baseline, so the worktree is reaped but foreign bytes are never overwritten (invariant pinned).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.254 (a00-a4073def). WHAT THE INSTRUCTION SAID: the target claim is a build order — "_sweep_finished_worktrees gains a bring-home step ... scoped to THAT function plus one helper _sweep_bring_home ... and NOTHING in _watch's pass order"; sub-cases (a)-(f) named. WHAT THE MACHINE DOES (verified on the artifact, not the report): _sweep_bring_home (heal.py:562) lazy-imports cli, calls cli._session_complete(root, locations.iteration_id(iter_name), worktree=None, dry_run=dry_run) once per iter via the homed memo, captures stdout and decides by WOULD migrate/REFUSE (dry) or the on-disk target (live); the grace check moved above the home step; base is pre-resolved read-only before any home; cli.py is comment-only (git diff --cached: 5 comment lines, zero code). I RAN the suite myself: 56 passed (test_heal_sweep 10 = 5 old + 5 new). I RAN the real-tree delta myself, dry-run only from the seat, with the kid bytes: removed=91 -> 169, refused=114 -> 42 = 13 dirty + 21 unmerged + 8 session-dir-not-home, and those 8 are exactly the probe-predicted non-terminal rounds (iter-L4.194 x2, SL1.03 x2, L4.175 x2, L4.243, L4.278); 79 homed lines = the probe's 79 would-migrate. That is the claim's EXPECTED DELTA, matched on the real tree. NEAR MISS: the claim's sub-case (c) said a pre-existing non-empty main target is refused: target exists; that expectation collides with sub-case (d), where a --branch round's SECOND tree legitimately sees the first tree's target already on disk and MUST stay removable — a disk-existence refusal would strand every --branch round. The kid resolved it the only safe way: session-complete's own target guard is never reached (the sweep never writes a target, never overwrites foreign bytes), and test (c) pins the invariant the FALSIFIER actually names — foreign bytes byte-identical after the pass — while documenting the removal verdict as a baseline deviation. I accept the deviation: (c) as written was ill-posed, and no falsifier fires. DEVIATION FROM STANDING RULE: none — file scope held, _watch untouched, no --force, dry-run first. VERDICT: kid's inconclusive_lean_proved:72 stands; 72 is honest, not low, because (c) is unmet as literally written.
<!-- THOUGHT:END -->

PARENT L4.254 ACCEPTED: built bytes match the claim on the real tree. Real-tree dry-run with the kid's heal.py: removed=91->169, refused=114->42 (13 dirty, 21 unmerged, 8 not-home = the 8 probe-predicted non-terminal), 79 homed. 56 tests pass. cli.py comment-only, _watch untouched, no --force. One deviation accepted: sub-case (c) 'refused target exists' is unreachable and would conflict with (d); foreign bytes are never overwritten and that invariant is pinned by test (c). Verdict inconclusive_lean_proved:72 stands.
