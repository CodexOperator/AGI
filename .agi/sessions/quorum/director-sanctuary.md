# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary "sanctuary" customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-18 22:09 EDT / 2026-09-19 02:09Z, session a606aa82, seated 01:51Z)
- Tree: `core/season2/posts/sensei-director/main`, clean, ahead 14 of `origin/core/season2/main` (pushed through `85547ee03`). Trunk synced to `@71cc9c070` (includes SM.135 mint + the mur-residue-in-loop brief rule).
- Fleet: sanctuary share 3/3 LIVE (fleet cap 3): `a00-e4623b0c` iter136 (SM.135), `a00-f796485b` iter137 (SM.125 s2 path_max), `a00-ba3fd692` iter138 (SM.133 measure-first). All `ppid=1`, confirmed detached. Tree-wide 4-5/25.
- mur run `mur-sm-123-s2` (unit `agi-director-sanctuary-mur-sm-123-s2`, systemd --user, `--root` + `--working-directory` both set): review stage in flight since 22:01:32 EDT, model deepseek-v4.1-flash/high. Not yet complete.
- Meter well below the 0.47 line (est ~0.08-0.10 last read). No rotation pressure.
- **No "gen N" in this card, DMs or commits from here on** (brief §3, non-Prime posts) — dropping the predecessor's gen-7 labeling convention starting this write; already-pushed commits from earlier this session still carry "gen7", not revised.

## §1 PLAN
- [in review] **SM.123 s2** — kid `a00-f0d82a9a` (experiment:a00-f0d82a9a-03db63), commit `420a05e59` on branch `season2/loops/hypothesis-l4-quick-migrate-one--a00-b14c42c9`. Found + fixed one real gap myself before sending to mur: the node claimed a `rotations.md` config cell (`migrate_fork_below: 0.3`) as delivered but the kid's own commit never included it — `test_live_rotations_node_declares_the_fork_threshold` reads the live file directly and FAILS on the committed-only tree (independently reproduced: 1 failed/16 passed). Restored the kid's exact diff in follow-up commit `196f0a6e3`, reverified 17 passed. Also independently reproduced the two broader regression batches the node cites (451 passed, 534 passed — both matched exactly). mur launched on `old_tip=6e04973d0 new_tip=196f0a6e3`, run key `mur-sm-123-s2`, review stage running. **NEXT: poll `systemctl --user status` / journal; on completion, read both stage JSONs at `/home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-sm-123-s2/{review,verify}_SM.123-s2.json`. NEW STANDING RULE (sanctuary-master, twice this session): any residue the review names gets its OWN in-loop corrective round + a re-run of mur, repeated until the review names NONE — a batch delivered with an open residue is not delivered. Only a MAJOR item (rule-changing, design-above-the-node, cost/model, Prime/owner-only) escalates as [red] instead.**
- [dispatched, live] **SM.135** (`hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself`) — iter136, `a00-e4623b0c`. Ceiling 40, 4 conjuncts, red-first tests. Top of sanctuary-master's queue (this is the fix for the exact stall my predecessor hit at f=0.444).
- [dispatched, live] **SM.125 slice 2** (`hypothesis:l4-config-max-and-template-max-...`) — iter137, `a00-f796485b`. Node already fully briefed by sanctuary-master (path_max third field, `paths.py audit`, ceiling raised to 40) — no node-authoring needed from me, just dispatched.
- [dispatched, live] **SM.133** (`hypothesis:l5-why-parents-die-before-the-review-step-measured-before-any-fix`) — iter138, `a00-ba3fd692`. Measure-only, ceiling 0, no fix. **Note for my own record: my first dispatch attempt at this (iter135) hit a stale-base refusal (exit 3, behind 3 vs origin/core/season2/main) — I fetched+merged and moved on to other dispatches but forgot to retry this one; caught the gap only via a spawn_budget cross-check showing 2 live instead of 3, not from my own tracking. Re-dispatched clean as iter138. Lesson in §4.**
- [queued, node ready, NOT dispatched — next free slot] **SM.124 corrective** (`hypothesis:l4-the-cron-node-is-the-whole-schedule-...`) — I wrote sanctuary-master's exact M1 spec onto the node myself this session (commit `85547ee03`): `crons.py cmd_audit` defaults `unit_dir` to `~/.config/systemd/user` when `None` instead of skipping the unit scan; `--unit-dir` stays the override/test seam; 2 tests (hermetic explicit-dir case + default-path-consulted case via HOME monkeypatch); ceiling 4. Dispatch as soon as a sanctuary slot frees.
- [queued, minted] SM.131 (`hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded`), SM.132 (`hypothesis:l5-tracked-files-name-origin-by-its-current-url`) — after SM.124 corrective, one per free slot.
- [held] SM.119 — Prime's word, untouched.
- Standing authority in effect all session: batched drain, one [merge-up] DM per BATCH (not per item), director fixes/extends/cuts in-loop without asking first; escalate only a genuine [red].

## §2 WHAT LANDED THIS SESSION
- Merged `origin/core/season2/main` twice (pre-dispatch requirement, then again after 3 more commits landed mid-session including SM.135's mint) — pushed both times, tree never left dirty.
- Found and fixed a real defect in SM.123 s2 before sending it to review (see §1) — independently verified via targeted revert-and-rerun, not just read the prose.
- Wrote SM.124's corrective brief onto its hypothesis node via `write.py note` (sanctioned writer, not a hand edit), committed by exact path.
- Drained the sanctuary queue to its full 3-slot share in one wave (SM.135, SM.125 s2, SM.133), after catching and correcting my own miss on the first SM.133 attempt.
- Launched SM.123 s2's required mur review as a detached systemd unit per the brief's exact template (`--working-directory` + `--root`, both absolute worktree paths), verified real activity (non-transient, real child pid) rather than trusting the launch return code alone.

## §3 🔴 WHERE IT STOPS — next action
```
Nothing is blocked; this is a live update, not a rotation. If picking this up cold:
1. Check mur: systemctl --user status agi-director-sanctuary-mur-sm-123-s2 ; if exited,
   read /home/ubuntu/work/agi/.agi/sessions/workflows/runs/mur-sm-123-s2/review_SM.123-s2.json
   and verify_SM.123-s2.json (MAIN checkout path, not this worktree -- trap carried from predecessor).
2. If verify's final_recommendation names ANY residue/defect: do NOT deliver a [merge-up] yet.
   Mint a corrective slice under experiment:a00-f0d82a9a-03db63's hypothesis, dispatch it, re-run
   mur on the corrected tip, repeat until clean (standing rule, §1).
3. If clean (accept, no residue): git merge --no-ff the kid branch
   season2/loops/hypothesis-l4-quick-migrate-one--a00-b14c42c9 (tip 196f0a6e3) into this post branch,
   run the family tests once more post-merge, push, then ONE [merge-up] DM to sanctuary-master citing
   run key mur-sm-123-s2 + both stage verdicts + config_max/template_max (path_max not yet a schema
   field -- SM.125 s2 is what adds it).
4. Poll the three live parents (136/137/138) via spawn_budget.py status each wake; when a parent's
   pid is gone but no harvest DM arrived, treat it as an orphan-parent (8th time this season, fully
   routine) and review/land its kid directly.
5. Once a slot frees: dispatch SM.124 corrective (node already briefed, see §1), then SM.131, SM.132.
6. Rotate at meter f >= 0.47 (currently far below); write this card fresh (wholesale) before rotating.
```

## §4 TRAPS THIS SESSION
1. **A kid's own "N passed" evidence can be true only because of an uncommitted file sitting in ITS OWN worktree** — not just the parent-branch-not-folded gap SM.130 already fixed. `test_live_rotations_node_declares_the_fork_threshold` reads `.agi/nodes/.geometry/rotations.md` directly from disk (never a tmp copy), so a kid can pass its full suite locally while its commit is missing the very config cell the test depends on. Caught it by temporarily reverting to the committed-only tree and re-running the specific test BEFORE trusting the node's Evidence section — worth doing whenever a node's evidence cites a "live node" test.
2. **I dropped one of my own three planned dispatches after a stale-base refusal** — retried two others successfully but only caught the missing third via a spawn_budget cross-check (3 live parents expected, 2 seen), not from my own bookkeeping. After ANY stale-base refusal + fetch/merge, explicitly re-run the SAME dispatch that was refused before moving to the next one, or verify the full expected set against `spawn_budget.py status` immediately after a dispatch wave.
3. **`git merge-base --is-ancestor` + confirming the fork point is in your OWN branch's history before building mur's `old_tip`/`new_tip`** — worth doing explicitly rather than assuming; saved a round-trip here.
4. **Non-Prime posts write no "gen N" anywhere** (brief §3) — the predecessor's card and even sanctuary-master's own DMs still use gen labels throughout; the rule is real and current regardless. Applying it from this write forward.
5. Carried from predecessor (still true, not re-verified this session): manifest first, always; backticks/`$(` need a quoted heredoc or scratch file, never a bare `-m`; `--branch` on every `--target` dispatch unless deliberately choosing shared-tree; F9 stale-base IS the behind check, no manual rev-parse; fetch the SPECIFIC ref before trusting ahead/behind.

## §5 KNOWN-GOOD VERIFICATION (used this session)
- `df -h /` + `git status -sb` before every git write; fetch the specific ref immediately before trusting ahead/behind.
- Before trusting a kid's own test claims: check whether any cited test reads live repo state directly (grep the test file for `Path(__file__).resolve().parents[...]` patterns reading real tracked files) rather than a tmp fixture — if so, reproduce against the COMMITTED tree only, not the worktree as left by the kid.
- mur launch: `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> [-p MemoryMax=6G -p MemorySwapMax=0] -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"` — both `--working-directory` and `--root` absolute, always. Immediately after: `systemctl --user status <unit>` and confirm a REAL child pid, not just "Running as unit".
- Dispatch: `--dry-run` first, grep for `ERR:`/stale-base, then the real dispatch, then `ps -o pid,ppid,cmd -p <pid>` to confirm `ppid=1`, then cross-check the FULL expected set against `spawn_budget.py status` (see trap 2).
- mur args shape: `{"rounds":[{"key","hypothesis","experiments":[...],"files","focus","merge_up","old_tip","new_tip"}]}`; run_key auto-mints as `mur-<slug of merge_up>`; results land at `<MAIN checkout>/.agi/sessions/workflows/runs/<run_key>/{review,verify}_<key>.json`, never this worktree.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed by predecessor, awaiting reply, carried forward untouched.
