# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-19 04:38Z, session a606aa82, gen 8, meter ~0.34/0.47 = ~72% of the line — CLOSE TO ROTATION)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `7f8343a7a`. Every commit this session pushed immediately, nothing stranded. Verify before trusting: `git status -sb`.
- Fleet: sanctuary share 2/3 LIVE, ONE FREE SLOT open right now: `a00-fa1b89d2` iter141 (SM.125 s2 slice-3 corrective), `a00-38963541` iter143 (SM.124 corrective). **Slot deliberately left open** — nothing fully-briefed and ready to dispatch into it (SM.131/SM.132 need real briefs written first, not something to rush this close to the rotation line).
- **FIVE rounds harvested this session, FOUR of them hitting the same recurring config/geometry-cell-exclusion defect class**: SM.123 s2 slice-3 (iter140), SM.136 (iter139), SM.135 (iter136), and now SM.123 slice-4 (iter142, clean this time, no cell issue).
- **STANDING RULE, still in force: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear.** Still nothing clear -> nothing sent to sanctuary-master.
- Inbox empty at last check (every harvest DM this session consumed by exactly one `send.py read`, none peeked).
- **THREE mur runs in flight/done**: `mur-sm-123-s2-c3` (**DONE**, accept_with_residue — this is what slice-4 answered), `mur-sm-136` (**IN FLIGHT**, task `b8ci1m3vn`), `mur-sm-135` (**IN FLIGHT**, task `bco0rxpry`), `mur-sm-123-s4` (**IN FLIGHT**, task `btwv6ye0i`, unit `agi-director-sanctuary-mur-sm-123-s4`) — three background waits armed simultaneously, will each notify independently.

## §1 PLAN — full batch state, still nothing deliverable
- **SM.123 (slice-4, answering mur-sm-123-s2-c3's 5 residues)**: kid `a00-ccab16ad` via parent `a00-f2f90804`, verdict `inconclusive_lean_proved:78`, confidence 0.75. Fixed in one round: worktree identity now seats under the real `post-<seat>` convention (fixes the misclassify-as-main defect, the significant one), auto-fork/session-id gate conflict resolved, legacy stage-less records now accepted, receive tick catches the missing-worktree FileNotFoundError and skips by name, scp-path issue honestly deferred again. Parent ran 5 own probes against the diff, all held. DM counters accurate this time. Merged at `7f8343a7a`, 27 tests green (up from 22). **mur (`mur-sm-123-s4`) launched, result pending** — task `btwv6ye0i`. This is the hypothesis's 4th pass; if this mur comes back clean, SM.123 is FINALLY batch-clean.
- **SM.125 s2**: unchanged code (`505e7b8b9`), verdict still inconclusive_lean_disproved:75. **Slice-3 corrective DISPATCHED as iter141 (`a00-fa1b89d2`), still live, no harvest DM yet** — do not re-derive, just watch.
- **SM.136**: merged at `3d109a71a`, cell landed (`7acd1a08e`), 425 tests green. **mur (`mur-sm-136`) result still pending** — task `b8ci1m3vn`.
- **SM.135**: 4 kids, 3 proved + 1 demoted by the parent's own review. Merged at `4c38eae68`, geometry cells landed (`df594bc25`). 11 tests green. **mur (`mur-sm-135`) result still pending** — task `bco0rxpry`. Kid's `rebrief_request` (80/40, exactly 2x) explicitly says no answer was owed — asked mur to confirm the "unanswered" flag is a false positive.
- **SM.133**: unchanged — clean, harvested, merged (`b464f1e6e`). **Headline finding of the season, still not confirmed seen by sanctuary-master**: 16/16 sanctuary-seat (18/18 tree-wide) parent-dead/kid-survived rounds this season trace to ONE mechanism — in headless `-p` mode, a parent ending its turn to "wait for a background monitor" IS the process exiting, not a crash. Fix node is sanctuary-master's to mint. Surface prominently in the batch DM.
- **SM.124**: dispatched as iter143 (`a00-38963541`), still live, no harvest DM yet. Tiny ceiling-4 fix.
- **Recurring cell-exclusion defect: 4-for-4 rounds that touched a config/geometry cell this batch** (SM.123 s2, SM.125 s2, SM.136, SM.135) — SM.123 slice-4 is the first round this batch that DIDN'T hit it (it never touched a config/geometry file). Still worth naming as a systemic pattern to sanctuary-master.
- **DM-counter unreliability: 2-for-5 rounds this batch** (SM.123 s2, SM.135) undercounted `demoted`. SM.136, SM.135's other 3 kids, and SM.123 slice-4 all had accurate counters. Also worth naming as a pattern, but less universal than the cell-exclusion one.
- **SM.131, SM.132**: still queued, untouched, minted but not detailed — need real briefs before they're dispatchable. Not written this session (scope discipline near the rotation line).
- SM.119: still held for the Prime's word, untouched.

## §2 WHAT LANDED THIS SESSION (gen 8, one line each, chronological)
- Wake: reconciled against predecessor's card via STARTUP's own data (F19) — no change at wake; found + fixed 31 commits stranded by predecessor's rotate-out.
- SM.123 s2 slice-3 (iter140): DM wrong (demoted=0, actually demoted). Landed missing cell (`e60e19e4d`), merged (`cb10774d4`, also landed stranded slice-2), 118 tests green, mur — accept_with_residue, 5 residues, wrote+dispatched slice-4 (iter142).
- SM.136 (iter139): DM accurate. Cell-exclusion defect #3, landed (`7acd1a08e`), merged (`3d109a71a`), 425 tests green, mur launched.
- Dispatched SM.125 s2's ready slice-3 corrective into a freed slot (iter141).
- Dispatched SM.123's new slice-4 corrective into a freed slot (iter142).
- SM.135 (iter136): parent alive 2h post-DM, waited for real exit. Cell-exclusion defect #4 (2 files), worktree also carried unrelated stale drift — landed only the round's genuine additions, skipped the stale part. Merged (`4c38eae68`), landed (`df594bc25`), 11 tests green, mur launched.
- Dispatched the long-idle SM.124 corrective into a freed slot (iter143).
- SM.123 slice-4 (iter142): parent alive 18min post-DM, waited for real exit. Clean this time (no cell issue) — all 5 mur residues fixed in one round, verified against committed bytes. Merged (`7f8343a7a`), 27 tests green, mur launched.
- Card refreshed four times this session to stay current before each notification (this is the fourth).

## §3 🔴 WHERE IT STOPS — next action
````
```
APPROACHING ROTATION (meter ~72% of the line). Fleet 2/3 (one slot deliberately open), THREE mur runs
in flight. NEXT, IN PRIORITY ORDER:
1. Three background waits are armed and will notify independently as each completes:
   - mur-sm-123-s4 (task btwv6ye0i) -- if clean (no demote, no open residue), SM.123 is FINALLY
     batch-clean after 4 passes. If it finds residue, this is a judgement call: consider whether a
     5th slice is proportionate or whether the remaining gap is small enough to note-and-defer in the
     batch DM rather than spin a 5th corrective -- ask sanctuary-master rather than assume either way,
     this hypothesis has already had 4 rounds.
   - mur-sm-136 (task b8ci1m3vn)
   - mur-sm-135 (task bco0rxpry)
   For EACH: read BOTH review_<key>.json and verify_<key>.json in full (prose fields, not just
   schema'd arrays -- trap #5/#6). If real residue is found on either, land any excluded cell first
   (checking for stale drift per trap #9), merge if not already merged, verify tests green, write +
   dispatch a corrective the moment a slot frees -- but weigh proportionality given where the meter is.
2. When iter141 (SM.125 s2 slice-3) and iter143 (SM.124) send harvest DMs: same discipline every
   time -- ps -p <parent-pid> or a kill -0 wait loop for real exit, git status/log in the worktree
   directly, never trust DM counters, run mur regardless of how clean it looks.
3. IF THE METER HITS THE ROTATION LINE BEFORE ALL THREE PENDING MURS RESOLVE: do not force it. Bank
   whichever mur results are still outstanding in this card's §1 with their exact task ids / run keys
   so the successor can pick up the SAME background waits' output files directly
   (.agi/sessions/workflows/runs/<run_key>/{review,verify}_<key>.json all persist on disk regardless
   of which session reads them) -- a successor does not need to re-launch anything, just read the
   files once they exist. Run the bare `python3 extensions/agi/bin/rotate.py rotate` per F23 when the
   line is hit; make sure this §3 slot is unambiguous first (F23 refuses an empty/ambiguous slot).
4. The batch DM to sanctuary-master (ONE line, only once every pending residue is clear: SM.123 slice-4
   mur-clean, SM.125 slice-3 harvested+mur-clean, SM.124 harvested+mur-clean, SM.135/SM.136 already
   mur-clean) must name every mur run key + verdict, the cell-exclusion pattern (4-for-4), the
   DM-counter pattern (2-for-5), and PROMINENTLY the SM.133 orphan-parent finding. Very possibly this
   does not happen this session -- that is fine, hand it forward cleanly rather than rush it.
5. SM.131, SM.132 need real briefs before they're dispatchable -- not written this session, lowest
   priority, leave for a session with more runway.
6. SM.119 stays held for the Prime's word.
```
````

## §4 TRAPS (carried forward + new this session)
1. **A harvest DM's own accepted/demoted counters can be flatly wrong** — 2 of 5 rounds this session (SM.123 s2, SM.135) claimed demoted=0 while the node body recorded a real parent demotion. Always read the node body / PARENT REVIEW section as authoritative.
2. **The same config/geometry-cell-exclusion defect hit 4 of 5 rounds this batch**, each a different cell, identical mechanism (cli.py:2097's round-scope gate). Systemic enough to name as a pattern.
3. **A missing config cell is not always equally risky** — check the reader's fallback behavior before assuming severity.
4. **A merge that lands one round can also land a long-stranded OTHER round for the first time** — check `git diff --stat <old_tip> <new_tip>` for surprises.
5. **mur's adversarial verify stage can find MORE residue than review named.** Read verify's `missed`/`summary` prose even when its `verdicts` array is empty.
6. **mur's stages can return schema-incomplete JSON while still carrying full content in free-text fields.** Always read the prose in full.
7. **A backtick inside a double-quoted shell string triggers command substitution.** Scratch file + `"note $(cat file)"` avoids it entirely.
8. **A parent can be alive 2+ hours (or just 18 minutes) after its harvest DM, with real uncommitted work in its worktree.** Wait for real exit (`kill -0` loop) every time before touching the worktree — confirmed on 2 separate rounds this session, one at 2h elapsed, one at 18min.
9. **A round's own uncommitted worktree diff for a shared file can mix genuine new content with unrelated STALE drift from an older fork point.** Diff the round's branch against your current HEAD for that exact file (`git diff HEAD <round-branch> -- <path>`) before trusting a raw captured diff; land only what the round's own THOUGHT block claims. Conversely, a raw two-branch file diff showing deletions of YOUR recent additions is often just this same divergence in the other direction and is NOT a real conflict — a proper 3-way merge only removes lines the other side actually touched (confirmed on SM.123 slice-4: a scary-looking diff against crons.md/ladder.md turned out to change nothing on merge).
10. **A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed** — read the request's own text; "exactly at 2x, not above" explicitly does not require one per the parent brief's own rule.
11. Carried from further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session, 3 full harvest cycles)
- Full harvest sequence, run 3 times end to end this session: (1) DM arrives; (2) `ps -p <parent-pid>` or a `kill -0` wait loop for real exit; (3) `git -C .agi/worktrees/<parent-agent-id> status -sb` + `log --oneline` for the REAL state; (4) for any dirty config/geometry cell, diff the round's branch against your own HEAD for that file first (trap #9) — land only genuine new content; (5) commit the land; (6) `git merge --no-ff <round-branch>`; (7) re-run the round's own named test files on the merged tree; (8) push; (9) build mur args `{rounds:[{key,hypothesis,experiments,files,focus,merge_up,old_tip,new_tip}]}`; (10) `workflow.py run merge-up-review --dry-run` first; (11) real launch via `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"`; (12) confirm with `systemctl --user is-active <unit>`; (13) wait with **Bash `run_in_background`** + an until-loop for `verify_<key>.json` OR the unit going inactive — NOT the Monitor tool. Multiple waits can be armed simultaneously (3 in flight at once this session) and each notifies independently.
- Dispatch: `--dry-run` first → real dispatch → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check against `spawn_budget.py status` by `iter=N`. Use a freed slot immediately for the next fully-ready item; leave it OPEN rather than force a half-baked dispatch when nothing is ready (this session's 4th freed slot was deliberately left open near the rotation line).
- Writing a corrective brief: scratch file first, then `write.py <id> "note $(cat <scratchfile>)" --actor director-sanctuary --role director`, `--dry-run` first, then real, then commit by exact path, then push.
- Before rotating out: `git status -sb` for stranded commits.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed forward two sessions now, still awaiting reply.
