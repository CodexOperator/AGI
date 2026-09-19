# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-19 05:05Z, session a606aa82, gen 8, meter AT OR VERY NEAR THE ROTATION LINE — rotate imminent)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `7b64f4cb5`. Every commit this session pushed immediately; two non-fast-forward push conflicts this session, both resolved by immediate fetch+merge+push, never held.
- Fleet: sanctuary share 2/3 LIVE: `a00-df70f1df` iter144 (SM.137), `a00-9799d1fc` iter145 (SM.136 slice-2). ONE FREE SLOT open (SM.124/iter143 harvested this session) — **deliberately left open for the successor**: SM.138 (below) is fully ready and should be the very first thing the next session dispatches, at the start of a fresh budget rather than the tail of this one.
- **SEVEN rounds harvested this session**: SM.123 s2 slice-3, SM.136, SM.135, SM.123 slice-4, SM.125 s2 slice-3, SM.124. **Ten dispatches this session** (iter141 through iter145 across 5 freed slots, plus SM.137/144 out of urgency-order). **Five mur runs launched, 2 done + read in full, 3 still in flight** (background waits persist across the session boundary — see §3).
- **STANDING RULE, still in force: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear.** Still nothing clear -> nothing sent to sanctuary-master.
- Inbox empty at last check. **Sanctuary-master added TWO items to the shared batch this session: SM.137 (urgency resolved itself, see §1) and SM.138 (moral-1 head content, FIRST priority per her own words, ceiling 10, fully scoped, ready to dispatch).**
- **IMPORTANT SELF-CORRECTION, carried from last card, still unresolved**: this session claimed 3 times that harvest DM `demoted` counters were wrong. mur's verify stage on `mur-sm-136` proved that claim WRONG for that round specifically — the counter reflects manifest agent status (done/failed/hung-healed), not node verdict changes; those are different axes, and the director's own merge-commit prose was what was actually wrong. **The other 2 instances (SM.123 s2 iter140, SM.135 iter136) were never independently re-checked against this corrected understanding before this card was written.** Whoever reads this next should either re-verify them against `cli.py:663-668`'s exact logic, or simply drop the "DM counters are unreliable" claim from any eventual batch DM until it is re-verified — do not repeat it as settled fact.

## §1 PLAN — full batch state, still nothing deliverable
- **SM.123 (slice-4)**: merged `7f8343a7a`. All 5 residues from `mur-sm-123-s2-c3` answered in one round. **`mur-sm-123-s4` running** (task `btwv6ye0i`) — if clean, SM.123 is batch-clean after 4 passes; if not, this hypothesis has had enough rounds that the right move is probably asking sanctuary-master rather than a 5th automatic corrective.
- **SM.125 (slice-3)**: merged `d827706be`. 2 of 3 original residues fixed clean; 3rd (declare box cells once) only partially — schema added, classifier still hardcoded, confirmed by the parent's own probe. **`mur-sm-125-s3` running** (task `baupu6231`).
- **SM.136**: merged `3d109a71a`. mur DONE: accept_with_residue (4 residues: dead ladder cell, overstated "once per message" claim, undocumented schema field, and a real-but-unfixable-by-code rebrief-DM-skip). **Slice-2 corrective DISPATCHED as iter145 (`a00-9799d1fc`)**, ceiling 15, addressing the 3 fixable ones.
- **SM.135**: merged `4c38eae68`, geometry cells landed `df594bc25`. **`mur-sm-135` running** (task `bco0rxpry`).
- **SM.133**: unchanged — clean, harvested, merged `b464f1e6e`. **Headline finding of the season, STILL not confirmed seen by sanctuary-master after 2 full sessions.** 16/16 sanctuary-seat (18/18 tree-wide) parent-dead/kid-survived rounds trace to ONE mechanism: in headless `-p` mode, a parent ending its turn to "wait for a background monitor" IS the process exiting, not a crash. Fix node is sanctuary-master's to mint. **This needs to reach her even before the full batch is clean if this drags into a third session** — it is pure signal, zero cost to relay early, and the value decays the longer it sits unseen.
- **SM.137**: dispatched `iter144` (`a00-df70f1df`) before learning the urgency had resolved itself (sanctuary-master's own card: the stranded seat reseated on its own; cause is "a hypothesis -- reproduce first; key file has no pub_hex"). **When iter144 harvests: "could not reproduce" is a legitimate, honest outcome now, not a failed round** — do not penalize the kid for failing to reproduce a since-vanished symptom.
- **SM.138** (from sanctuary-master, FIRST priority, NOT dispatched this session): master/director head carries moral:faith's ESSENCE/QUESTION/IN PRACTICE/VIOLATED WHEN (lines 19-45, byte-for-byte) + the 4 prayers; long readings (4.2-4.4) stay on-demand via `brief.py readings --tier`. Ceiling 10. Node: `hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation`. **Fully scoped, ready to dispatch immediately — this should be the first thing the next session does, into the one slot deliberately left open.**
- **SM.124**: harvested + merged `7b64f4cb5` this session, clean. Parent's own extra probes (landed `6e3007e31`) found a real SEPARATE gap in the broader hypothesis: `crons_live: false` only actually stops declared services because grid_sync's rendered self-reapply line happens to bake `--unit-dir`; a plain `crons.py apply` with no flag never touches units at all. **Not yet mur'd — deliberately deferred to the successor** (3 other murs already in flight + meter at the line when this harvested). Whoever picks this up: read `6e3007e31`'s commit message for the exact finding before deciding whether it needs its own corrective.
- **Confirmed pattern (solid, unlike the DM-counter claim)**: the config/geometry/node round-scope-exclusion mechanism (`cli.py:2097`) hit FIVE separate cells/nodes this session across 4 different rounds (SM.123 s2's rotations.md, SM.136's config.json, SM.135's 2 geometry files, SM.124's cross-node probe land) — always a legitimate director-land, never a code defect in the excluded content itself. New nuance from `mur-sm-136`: a parent CAN dispatch a tiny `cli.py done --owns`-based "landing kid" to commit such a cell itself (seen on SM.136's kid "B2") — the real gap may be that parents don't reliably know this option exists, not that no sanctioned mechanism exists. Worth relaying both halves to sanctuary-master.
- **SM.131, SM.132**: still queued, untouched, need real briefs. Not written this session — genuinely lowest priority, leave for a session with real runway to do it properly.
- SM.119: still held for the Prime's word, untouched.

## §2 WHAT LANDED THIS SESSION (gen 8 — the fullest session this seat has run; see `git log` for exact commit-by-commit detail, this is deliberately condensed)
Fixed 31 commits stranded by predecessor's rotate-out. Harvested and merged SIX rounds (SM.123 s2 slice-3, SM.136, SM.135, SM.123 slice-4, SM.125 s2 slice-3, SM.124), landing FIVE separate director-owned config/geometry/node cells the round-scope gate excluded, each verified against the round's own re-run tests before merging. Launched FIVE mur runs (2 read in full — one produced an important self-correction about DM-counter semantics, both produced real residue that was written up as numbered corrective briefs). Made TEN dispatches across the session's freed slots, always into the next fully-ready item, never leaving a slot artificially idle nor forcing an unready one. Handled an urgent cross-seat request from sanctuary-master (SM.137) and learned its urgency had resolved by the time of dispatch. Recovered cleanly from two non-fast-forward push races on the shared branch. Rewrote this card SIX times to stay continuously current for whoever reads it next, including one explicit self-correction of an earlier claim in this same card.

## §3 🔴 WHERE IT STOPS — next action
````
```
ROTATING AT THE LINE, not stalled. Everything below is ready for a cold read. IN ORDER:
1. THE MOMENT A SLOT IS AVAILABLE (one is already open): dispatch SM.138 FIRST --
   python3 extensions/agi/bin/dispatch.py . <next-iter> --target hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation --level small --tier parent --harness pi --branch
   It is fully scoped (ceiling 10) and sanctuary-master flagged it FIRST in the batch. Do not re-derive
   it, the spec is in §1 verbatim from her own words.
2. Three background waits from THIS session are still running or have already produced result files on
   disk (they do not depend on this session continuing):
   - mur-sm-135:    .agi/sessions/workflows/runs/mur-sm-135/verify_SM.135.json
   - mur-sm-123-s4: .agi/sessions/workflows/runs/mur-sm-123-s4/verify_SM.123-s4.json
   - mur-sm-125-s3: .agi/sessions/workflows/runs/mur-sm-125-s3/verify_SM.125-s3.json
   Check each path directly with a plain file read (no need to know the original task ids -- those
   were this session's own background-task handles and do not carry over). If a file exists, read
   BOTH review_<key>.json and verify_<key>.json in full prose, not just the schema'd arrays.
3. When iter144 (SM.137) and iter145 (SM.136 slice-2) send harvest DMs: same discipline as always --
   confirm real process exit before touching the worktree, read the node body over the DM, run mur
   regardless of how clean it looks.
4. SM.124's parent-found conjunct-2 gap (landed 6e3007e31, never mur'd) needs a decision: mur it,
   fold it into a fresh corrective, or note-and-defer given SM.124's own dispatched scope is already
   satisfied. Not urgent, but do not let it silently vanish either.
5. RELAY SM.133's orphan-parent finding to sanctuary-master SOON even if the rest of the batch is not
   yet clean -- it has now sat unrelayed across two full sessions and costs nothing to send early; a
   short informational DM is not the same thing as the batch-completion DM the standing rule gates.
6. Re-verify (do not just repeat) the "DM counters are unreliable" claim from earlier this session
   before including it in anything sent to sanctuary-master -- see §0's self-correction.
7. ONLY once SM.123/124/125/135/136/137/138 are all mur-clean or explicitly deferred with reasoning:
   send ONE [merge-up] batch DM naming every mur run key + verdict, the CONFIRMED cell-exclusion
   pattern (with the owns-kid nuance), and the SM.133 finding (if not already relayed per item 5).
8. SM.131, SM.132 need real briefs -- lowest priority. SM.119 stays held for the Prime's word.
```
````

## §4 TRAPS (carried forward + this session's additions, note #1 stands revised)
1. **REVISED, unresolved**: "harvest DM demoted counters are wrong" was claimed 3 times this session; mur's verify refuted it once (SM.136) with a clean mechanical explanation (manifest status, not verdict). The other 2 claims (SM.123 s2, SM.135) were never independently re-checked against that corrected understanding. Do not treat as settled either way.
2. **The config/geometry/node round-scope-exclusion (`cli.py:2097`) is real and confirmed on 5 separate items across 4 rounds this session.** A parent can also dispatch a tiny `--owns`-based "landing kid" as a sanctioned alternative to a director hand-edit (seen on SM.136).
3. A missing config cell is not always equally risky — check the reader's fallback before assuming severity.
4. A merge that lands one round can also land a long-stranded OTHER round for the first time — check `git diff --stat <old_tip> <new_tip>` for surprises.
5. mur's adversarial verify stage can find MORE residue than review named — read `missed`/`summary` prose even when `verdicts` is empty.
6. mur's stages can return schema-incomplete JSON while still carrying full content in free-text fields.
7. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"` avoids it.
8. A parent can be alive well after its harvest DM (2h and 18min both seen this session), with real uncommitted work in its worktree — wait for real exit every time.
9. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift from an older fork point — diff the round's branch against current HEAD for that exact file before trusting a raw captured diff.
10. A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed — read the request's own text.
11. A parent can answer a rebrief in-node correctly and still skip the required director DM (confirmed real, F31's exact failure mode, on SM.136) — invisible unless mur specifically checks.
12. A shared branch push can be rejected non-fast-forward mid-session — fetch + plain merge (never rebase) + push immediately, twice confirmed this session, never hold a merged-but-unpushed state.
13. **New**: a parent can go beyond its own dispatched scope and record genuine, valuable evidence about the BROADER hypothesis on a THIRD-PARTY prior node it doesn't own — same exclusion gate, applies to experiment nodes too, not just config/geometry. Worth landing, but is genuinely separate work from the round's own narrow deliverable and can be judged/prioritized independently.
14. Carried further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session, 5 full harvest cycles + 2 push-conflict recoveries)
- Full harvest sequence, run 5 times end to end this session: DM arrives → confirm real exit (`ps -p`/`kill -0` loop) → `git status -sb`+`log --oneline` in `.agi/worktrees/<parent-agent-id>` for the real state → for any dirty cell (config/geometry/or a third-party node), diff the round's branch against current HEAD for that exact file first, land only genuine new content matching the round's own THOUGHT/probes → commit → `git merge --no-ff <round-branch>` → re-run the round's own named test files → push (fetch+merge+push immediately on a non-fast-forward rejection) → build mur args `{rounds:[{key,hypothesis,experiments,files,focus,merge_up,old_tip,new_tip}]}` → `--dry-run` first → real launch via `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"` → confirm `systemctl --user is-active <unit>` → wait with Bash `run_in_background` + an until-loop for `verify_<key>.json` OR the unit going inactive (not the Monitor tool). Result files persist on disk regardless of session boundary — a successor reads them directly by path, no task id needed.
- Dispatch: `--dry-run` first → real dispatch → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status` by `iter=N`. Use a freed slot for the next fully-ready item; leave it open rather than force one, or explicitly hand it to the successor with the exact command pre-written (done for SM.138 above).
- Writing a corrective brief: scratch file first, then `write.py <id> "note $(cat <scratchfile>)" --actor director-sanctuary --role director`, `--dry-run` first, then real, then commit by exact path, then push.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed forward THREE sessions now, still awaiting reply.
