# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~05:40Z 09-19, session b5e110df, gen 9, meter last read 0.228/0.47 ≈ 48% of the line — watching, not urgent)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `87560a22b`, in sync with trunk, pushed clean through every landing this session (4 pushes, one real 3-way merge when trunk moved concurrently, zero conflicts on trunk syncs — the one real conflict this session was a round's own stray write, see below).
- **THREE rounds harvested, merged, and mur-launched this session**: SM.132, SM.135 slice-2, SM.138. All three read diff-first (never the report), all three genuinely solid work with honest disclosed overages — no demotions needed at land time, but mur runs are in flight regardless (never skip verify on a clean-looking round).
- **THREE mur runs currently active**: `agi-sensei-director-mur-sm132`, `agi-sensei-director-mur-sm135s2`, `agi-sensei-director-mur-sm138` (all systemd --user units, all confirmed `active` at launch). None have returned yet.
- **Still live in the fleet, awaiting their own harvest**: SM.131 (iter148, `a00-d36fced1`, kid `a00-09d5b982`), SM.139 (iter150, `a00-2aade523`, kid `a00-c2bcfc6a`), SM.123 slice-5 (iter151, `a00-2a62c783`). Budget 6/25 live, load stable 6.2/6.1/6.2 (down from the earlier climbing 10.3/8.2 — fine).
- **🔴 FINDING THIS SESSION, flagged to mur-sm135s2 for independent verification, not yet resolved**: while harvesting SM.135 slice-2 (iter147), its round branch carried an UNDISCLOSED commit (`a6884124058a416d61ef3772483d2cc6f8d8079f`, msg "director-sanctuary rotate-out gen 8->9: stops: n/a | last dm:") that overwrote `.agi/sessions/quorum/director-sanctuary.md` — a file entirely outside the round's stated scope — down to a 1-line stub. This produced a REAL merge conflict (not a silent stomp) when merging, which is how it was caught. Resolved by keeping the director's real card (`git checkout --ours`) and merging everything else normally; the stray commit's content never reached the trunk. The round's own node discloses nothing about touching this file — most likely a real `rotate.py handoff`/`rotate-self` invocation fired against this worktree's own live files during the parent's probe PA2 (`_force_capture` with "stand-in handoff/rotate" via real `_Popen`), which is exactly the "test touches a real resource" defect class the mur prompt itself warns about. Asked mur-sm135s2 to identify the exact call site and whether the new one-child `bash -c` chain could do this again outside a fixture. **Do not treat this as closed until that mur result is read.**
- **Two hypothesis nodes got RE-SCOPED by owner/other-post rulings mid-session, landing via trunk syncs, not this director's own action**: SM.135 (owner ruling via the Prime, `bfaf708a0`: authorizes a NEW captive-auto-rotate mechanism — f ≥ 0.85×director_rotate_at force-rotates a director with no consent, two triggers, ceiling 44 across the slice) and SM.137 (thought-master, `3626f0eb3`: rescoped to the measured cause — rotate's held-key check reads a lagging worktree row instead of the shared root). **Neither is dispatched yet** — SM.135's re-scope arrived AFTER iter147 was already in flight on the OLD narrower 3-residue scope (that round is now harvested on the old scope; the new captive-auto-rotate work is unstarted, separate follow-up). SM.137 still just owes its ORIGINAL mur run before anyone touches the re-scope.
- Inbox: sanctuary-master's SM.135-rescope FYI (informational, already cross-referenced via git), plus the two harvest DMs already processed above. Re-read before next action — SM.131/SM.139/SM.123-s5 harvest DMs may already be waiting.

## §1 PLAN — full batch state
- **SM.123 slice 5**: still live (iter151), not yet harvested.
- **SM.125 (slice-3)**: CLOSED, unchanged.
- **SM.131**: still live (iter148), not yet harvested.
- **SM.132**: **HARVESTED, merged, mur launched** (`agi-sensei-director-mur-sm132`). Genuinely good round: the original brief's file list (README.md + "2 nodes") and its "grep finds only the rotation record" claim were BOTH independently measured false by the kid; parent rescoped to the real live-address file set (QUICKSTART.md, TODO.md, package.json, legacy-prestate.md) and left 7 historical/measurement/substring-collision residuals alone with a reason each. Verdict `inconclusive_lean_proved:65` (conjuncts 1 and 3 of the ORIGINAL claim were literally false as written, correctly reported false rather than papered over). 1-line ceiling overage (7 vs 6), owned by the parent's rescope.
- **SM.133**: closed by its own finding (SM.139). No action.
- **SM.135**: slice-2 (the 3 mur-sm-135 residues) **HARVESTED, merged, mur launched** (`agi-sensei-director-mur-sm135s2`) — see the 🔴 finding above, not yet resolved. The NEW captive-auto-rotate scope (owner ruling) is separate, unstarted follow-up work — do not conflate with slice-2, which is done on its original scope.
- **SM.136 slice-2**: still owes a mur run — untouched this session, next real work once a slot allows.
- **SM.137**: re-scoped by thought-master this session; still owes its mur run on the ALREADY-MERGED code from before the re-scope. The re-scope itself is unstarted.
- **SM.138**: **HARVESTED, merged, mur launched** (`agi-sensei-director-mur-sm138`). Clean round with a real internal catch: kid 1 built the feature but its OWN adversarial probe found a crash (uncaught `ValueError` when moral:faith lacks `## ESSENCE`); parent demoted kid 1 in-node (`inconclusive_lean_disproved:40`) and dispatched kid 2 to fix it (`proved`). Cumulative 19 lines vs a 10-line ceiling clause (1.9x) — flagged to mur to settle whether that's the right comparator (each kid's own `line_ceiling` was independently 10, and each was individually under it).
- **SM.139**: still live (iter150), not yet harvested.
- **SM.124**: merged, clean, separate un-mur'd finding stays low-urgency.
- **SM.134**: retired, not this director's concern.
- **SM.119**: held for the Prime.
- **DM-counter-unreliability claim**: SM.138 gives a THIRD data point, and it looks like the counter is measuring something real and distinct — "demoted" tracks the automatic evidence-gate mechanism, not a parent's in-node manual verdict-lowering (which happened here, `proved`→`inconclusive_lean_disproved:40`, and did NOT increment any demoted counter, but that is arguably correct behavior, not a bug, since the gate itself never fired). Still not proven either way for SM.123 s2 specifically; do not overclaim.

## §2 WHAT LANDED THIS SESSION (gen 9, condensed — long session, most substantive yet)
Escalated SM.123's design question and relayed SM.133's finding via `[ask]`; both answered same-session (SM.123 → concrete option-b slice-5 dispatched; SM.133 → SM.139 minted and dispatched). Dispatched all 6 ready items in sanctuary-master's queue (SM.138, SM.135-s2, SM.131, SM.132, SM.139, SM.123-s5). Synced trunk three separate times as other posts landed concurrently (SM.135 captive-auto-rotate ruling, SM.137 re-scope), always fetch+merge before push, zero lost work. Harvested three rounds fully — read every diff before trusting a report, caught one real cross-file hazard (a round's stray write to this director's own live card, resolved via merge conflict rather than silent overwrite) and flagged it to that round's own mur for independent mechanism analysis. Launched three mur runs, none returned yet. Re-verified every round's own named tests after each merge (398, 301, and the SM.132 smoke suite all green, matching each kid's own reported counts).

## §3 🔴 WHERE IT STOPS — next action
```
1. Check inbox for SM.131/SM.139/SM.123-s5 harvest DMs and for the three outstanding mur results
   (verify_sm-132.json, verify_sm-135-s2.json, verify_sm-138.json under
   .agi/sessions/workflows/runs/mur-<sha>/ — confirm the actual directory name at result time,
   it is keyed by the workflow's own run-key (mur-<new_tip-sha>), not the round's short "key").
2. When mur-sm135s2 returns: read its answer on the stray-card-write mechanism FIRST. If it identifies
   a real, repeatable hazard (not just this-worktree-only), that may need its own hypothesis node
   (per the standing rule: a defect found while reviewing target X, but not IN X's own scope, gets its
   own node rather than a fix folded in).
3. Land SM.131/SM.139/SM.123-s5 the same way: diff first, confirm real exit, watch for any file
   outside stated scope before merging, tests, push, mur regardless of cleanliness.
4. SM.123 slice-5's mur is the real test of whether sanctuary-master's option-b design actually works
   end to end — treat "master approved the design" as a hypothesis, not a result, same as slice-4
   caught R1 after 4 clean review passes.
5. Once the fleet clears: SM.136 and SM.137 both still owe mur runs on their ALREADY-MERGED code
   (SM.137's re-scope is separate future work, not blocking its overdue mur).
6. The NEW captive-auto-rotate scope on SM.135 (owner-authorized, ceiling 44, "directors first") is
   real, unstarted, high-value work — it fixes the exact failure mode that has hit this director's own
   lineage repeatedly. Consider dispatching once current fleet clears, but read the ruling in full on
   the node first (not just this card's summary).
7. SM.119 stays held for the Prime.
```

## §4 TRAPS (carried forward + this session's additions)
1. The "replace the card on first substantive action" habit still needs earlier triggering — caught again this update cycle, several landings deep before this rewrite.
2. Two iter-numbering conventions coexist; only plain `iter-<N>` is live (now to 151).
3. `grid.py commit --all` is branch-blind by design; not part of this seat's sequence.
4. A hypothesis node's own measured numbers can live on a child experiment node, not its own body.
5. A predecessor's "needs a real brief" note can itself go stale — verify, don't inherit.
6. mur's verify stage can reverse review's own clean call — true of a sanctuary-master-approved design too, not just a kid's self-report.
7. mur's stages can return schema-incomplete JSON with content in free-text fields.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"`.
9. A parent can be alive well after its harvest DM — this session hit BOTH sides: SM.132's parent was still alive (had to background-wait for real exit) while SM.138/SM.135-s2's parents had already fully exited by the time their DMs were read. Check every time, assume nothing from the DM's mere existence.
10. **NEW, the most important catch this session**: a round's branch can carry a commit that touches a file completely outside its stated scope, with NO disclosure in the round's own node — caught here only because the file (this director's live card) was ALSO being edited concurrently by the director, producing a real merge conflict. Had the director's card been untouched that session, this would have been a SILENT overwrite instead of a conflict. **Lesson: diff a round's branch against its own claimed file scope BEFORE merging, not just after a conflict forces the question** — `git diff --stat <base>...<round-branch>` and compare the file list against the node's own "Files:"/evidence section; anything extra is a stop-and-investigate, not a wave-through, even if it merges cleanly.
11. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift.
12. A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed.
13. A parent can answer a rebrief in-node correctly and still skip the required director DM.
14. A shared branch push can be rejected non-fast-forward — fetch + merge (never rebase) + push immediately; this session alone needed it 3 times as other posts landed concurrently.
15. A `[ask]` DM to a master seat can be answered within the same session, not just "next session."
16. Carried further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session: 6 dispatches, 3 full harvests, 3 mur launches, 1 stray-write conflict resolution)
- Dispatch: `--dry-run` → real → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status`.
- **Full harvest sequence, now run 3x this session**: DM arrives → `ps -p <parent-pid>` (or a background `until ! ps -p ...` wait if still alive) → find the round's real worktree/branch via `.agi/sessions/iter-<N>/manifest.json`'s `agents[0].worktree`/`.branch` (do NOT assume `.agi/worktrees/<agent-id>` relative to the post's own tree — it is an ABSOLUTE path, often a sibling under the MAIN repo's `.agi/worktrees/`, not nested under this director's worktree) → `git diff --stat <post-branch>...<round-branch>` and sanity-check the file list against the round's own node before merging → `git status -sb` (sync trunk first if behind) → `git merge --no-ff <round-branch>` → if a conflict appears on a file the round had no business touching, resolve toward the director's own side and verify by re-reading the file, never assume → re-run the round's own named test files, compare counts to the kid's own reported numbers → push (fetch+merge immediately on rejection) → build `mur-<key>-args.json` in scratch (double check every SHA is a REAL `git rev-parse` output, never hand-typed or padded) → `workflow.py run merge-up-review --dry-run` → real via `systemd-run --user --unit=agi-<post>-mur-<key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- ...` → `systemctl --user is-active` to confirm.
- Trunk sync: `git fetch origin` → preview → `git merge origin/core/season2/main --no-edit` → confirm clean.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this session.
- The captive-auto-rotate scope (SM.135, owner-authorized) is not banked, just queued — no owner decision is pending on it, only dispatch capacity.
