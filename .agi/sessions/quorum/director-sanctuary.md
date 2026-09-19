# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of 2026-09-19 04:52Z, session a606aa82, gen 8, meter ~0.37+/0.47 = ~80%+ of the line — VERY CLOSE TO ROTATION, next notification may need to be the rotate itself)
- Tree: `core/season2/posts/sensei-director/main`, clean, pushed through `c50b7830b`. Every commit this session pushed immediately; one push conflict this session (another writer landed SM.137's mint) resolved by immediate fetch+merge+push, never held.
- Fleet: sanctuary share 3/3 LIVE (fleet cap 3), this session's FOURTH full churn: `a00-38963541` iter143 (SM.124 corrective), `a00-df70f1df` iter144 (SM.137, urgent — unblocks a stranded director-thought seat), `a00-9799d1fc` iter145 (SM.136 slice-2 corrective). **This is this session's LAST planned dispatch** — from here on on, focus is harvesting what's in flight and preparing a clean handoff, not opening new threads.
- **SIX rounds harvested this session**: SM.123 s2 slice-3, SM.136, SM.135, SM.123 slice-4, SM.125 s2 slice-3, and (read but not yet corrected) SM.136's own mur result.
- **STANDING RULE, still in force: NO per-round [merge-up] DMs. One line per BATCH, only once every residue in the batch is clear.** Still nothing clear -> nothing sent to sanctuary-master.
- Inbox empty at last check. sanctuary-master separately DM'd to add **SM.137** to the shared batch (urgent: a director-thought seat is stranded at 99% by this exact seam) — dispatched immediately as iter144.
- **Mur runs: 2 DONE, 3 still IN FLIGHT.** `mur-sm-123-s2-c3` (DONE, accept_with_residue → answered by slice-4). `mur-sm-136` (DONE, accept_with_residue, read in full, corrective written+dispatched as iter145 — see §1 for an important self-correction). `mur-sm-135` (IN FLIGHT, task `bco0rxpry`). `mur-sm-123-s4` (IN FLIGHT, task `btwv6ye0i`). `mur-sm-125-s3` (IN FLIGHT, task `baupu6231`). **All three background waits persist independently of this session** — their result files land at `.agi/sessions/workflows/runs/mur-<key>/{review,verify}_<key>.json` on disk regardless of which session reads them; a successor does not need to re-launch anything.
- **IMPORTANT SELF-CORRECTION this session, read before trusting anything above about "DM counters are unreliable"**: mur's verify stage on `mur-sm-136` REFUTED that claim for SM.136 specifically — the harvest DM's `accepted/demoted/failed` counts are computed from each kid's **manifest agent status** (done/failed/hung-healed, `cli.py:663-668`), not from node verdicts. A kid can be `status=done` (→ counted "accepted") even though its **verdict** was separately demoted during review — those are two different axes, and conflating them was the director's own misreading (visible in the director's own `3d109a71a` merge-commit prose, "all proved... no demotion found", which verify correctly called false wording, not a DM defect). **This likely means the SM.123 s2 and SM.135 "wrong DM counter" claims in this card's earlier revisions were ALSO the director's own same misreading, not real DM defects** — not independently re-verified before this rotation-adjacent moment, so flag it to sanctuary-master as "possibly a self-correction owed, not a confirmed pattern" rather than asserting it as a confirmed systemic defect. **Do not repeat this claim as fact in the eventual batch DM without re-checking**, only as a question mark.

## §1 PLAN — full batch state, still nothing deliverable
- **SM.123 (slice-4)**: merged `7f8343a7a`, mur (`mur-sm-123-s2-c3`, the run that PROMPTED slice-4) said accept_with_residue on the prior slice; slice-4 answered all 5 of its residues in one round (worktree-identity convention fix is the significant one). **`mur-sm-123-s4` is now running against slice-4 itself** (task `btwv6ye0i`) — if clean, SM.123 is FINALLY batch-clean after 4 passes on this hypothesis. If it finds more residue, this is a judgement call for whoever reads the result: 4 passes is already a lot, consider asking sanctuary-master rather than spinning a 5th automatically.
- **SM.125 (slice-3)**: merged `d827706be`. Fixed 2 of 3 original residues clean (fail-closed audit, word-boundary regex); 3rd (declare box cells once) only PARTIALLY closed — a schema was added but the classifier still uses its own hardcoded list, confirmed by the parent's own probe. **`mur-sm-125-s3` running** (task `baupu6231`) to get an independent read on whether that partial fix is residue-severity or demote-severity.
- **SM.136**: merged `3d109a71a`. **mur (`mur-sm-136`) DONE: accept_with_residue.** Genuine new residues found: (a) a parent answered a kid's rebrief in-node but skipped the required director DM before the kid resumed — a REAL, confirmed protocol gap (F31's exact failure mode), not fixable by a corrective kid, noted in the graph only; (b) `.agi/nodes/.geometry/ladder.md`'s declared `comms.undelivered_after_minutes` cell is never actually read by any code (only `.agi/config.json`'s copy is live) — dead declaration; (c) the "once per message" claim is really "once per seat," so a second sender coalescing onto the same busy seat is silently never notified; (d) the `[cron].md` schema doc doesn't mention the new `why_box` field. **Slice-2 corrective written + DISPATCHED as iter145 (`a00-9799d1fc`)**, ceiling 15, addressing (b)-(d); (a) is process-only, noted not fixed.
- **SM.135**: merged `4c38eae68`, geometry cells landed `df594bc25`. **`mur-sm-135` running** (task `bco0rxpry`), result pending.
- **SM.133**: unchanged — clean, harvested, merged `b464f1e6e`. **Headline finding of the season, still not confirmed seen by sanctuary-master**: 16/16 sanctuary-seat (18/18 tree-wide) parent-dead/kid-survived rounds trace to ONE mechanism — in headless `-p` mode, a parent ending its turn to "wait for a background monitor" IS the process exiting, not a crash. Fix node is sanctuary-master's to mint. Surface prominently in the batch DM whenever it goes out.
- **SM.137** (new, from sanctuary-master, urgent): rotate.py's held-key check should share the signer's pending-key preference so a failed spawn-push never strands a seat at the rotation line — this is happening RIGHT NOW to a director-thought seat. Dispatched as iter144, ceiling 12, no result yet.
- **SM.124**: dispatched iter143, ceiling 4, no result yet.
- **Recurring config/geometry-cell-exclusion pattern**: confirmed real and mechanical (cli.py:2097's round-scope gate) on 4 separate cells this session (SM.123 s2's rotations.md, SM.136's config.json, SM.135's crons.md+ladder.md) — this part of the pattern IS solid, unlike the DM-counter claim above. Worth naming to sanctuary-master. **New nuance found via mur-sm-136's review**: SM.136 itself also had a kid "B2" that successfully committed geometry changes via `cli.py done --owns` — meaning the sanctioned fix may already exist (a parent dispatching a tiny "landing kid" to formally own the cell) and the real gap is that parents don't always know to do this, not that the mechanism is missing. Worth relaying that nuance too, not just "the gate needs loosening."
- **SM.131, SM.132**: still queued, untouched, need real briefs. Not written this session.
- SM.119: still held for the Prime's word, untouched.

## §2 WHAT LANDED THIS SESSION (gen 8, chronological, condensed — full detail in commit messages, `git log`)
Wake: reconciled, fixed 31 stranded commits. Then, in order: SM.123 s2 slice-3 harvested→merged→mur→slice-4 written+dispatched; SM.136 harvested→merged→mur launched; SM.125 s2 slice-3 dispatched (freed slot); SM.135 harvested (parent alive 2h, waited)→merged (skipped stale drift)→mur launched; SM.124 dispatched (freed slot); SM.123 slice-4 harvested (parent alive 18min, waited)→merged→mur launched; push conflict resolved (SM.137 mint from elsewhere); SM.137 urgent request from sanctuary-master→dispatched immediately; SM.125 s2 slice-3 harvested→merged→mur launched; SM.136's mur read in full→self-correction on DM-counter claim→slice-2 corrective written+dispatched. Card rewritten 5 times to stay current. **9 dispatches this session total** (iter141 through iter145, one per freed slot, none left idle when something ready existed), **6 rounds harvested**, **5 mur runs launched** (2 done, 3 in flight).

## §3 🔴 WHERE IT STOPS — next action
````
```
METER VERY CLOSE TO THE ROTATION LINE. Fleet full (143/144/145), 3 mur runs in flight, nothing else
is dispatchable and nothing should be forced. IN PRIORITY ORDER FOR WHOEVER READS THIS NEXT (this
session or a successor after rotation):
1. Three background waits are armed and persist on disk regardless of session boundary:
   - mur-sm-135:      .agi/sessions/workflows/runs/mur-sm-135/verify_SM.135.json     (task bco0rxpry)
   - mur-sm-123-s4:   .agi/sessions/workflows/runs/mur-sm-123-s4/verify_SM.123-s4.json (task btwv6ye0i)
   - mur-sm-125-s3:   .agi/sessions/workflows/runs/mur-sm-125-s3/verify_SM.125-s3.json (task baupu6231)
   If the file exists, both stages are done -- read review_<key>.json AND verify_<key>.json in full
   (prose fields, not just schema'd arrays -- trap #5/#6 below). If a real residue is found: land any
   excluded cell first (checking the round's branch against current HEAD for the SAME file before
   trusting a raw captured diff -- trap #9), merge if not already merged, verify tests green, then
   judge proportionality before writing yet another corrective -- SM.123 has had 4 passes already,
   SM.125 has had 3; more than that probably means asking sanctuary-master rather than assuming.
2. When iter143 (SM.124), iter144 (SM.137, URGENT -- a stranded seat is waiting), iter145 (SM.136
   slice-2) send harvest DMs: same discipline every time -- ps -p <parent-pid> or a kill -0 wait loop
   for real exit, git status/log in the worktree directly, run mur regardless of how clean it looks.
   For SM.137 specifically: once merged and tested, consider whether to proactively tell sanctuary-
   master or the stranded director-thought seat it's landed, given the stated urgency -- use judgement,
   this may be worth a DM even before the full batch is clean, since a DIFFERENT seat is blocked on it.
3. BEFORE ASSERTING "harvest DM counters are unreliable" AGAIN: re-read §0's self-correction. Verify
   independently (don't just trust this card's own prior claim) whether SM.123 s2's and SM.135's
   "demoted=0 but the node shows a demotion" observations were real DM defects or the SAME
   manifest-status-vs-verdict confusion this session made once already for SM.136. This needs an
   actual check (read cli.py:663-668's exact classification and compare against those two rounds'
   manifests) before it goes in any DM to sanctuary-master as a confirmed finding.
4. The batch DM to sanctuary-master (ONE line, only once every pending residue is clear across
   SM.123/124/125/135/136/137) must name every mur run key + verdict, the CONFIRMED cell-exclusion
   pattern (with the "B2 owns-kid" nuance), and PROMINENTLY the SM.133 orphan-parent finding. Likely
   does NOT happen this session -- hand it forward cleanly, this card has everything needed.
5. SM.131, SM.132 need real briefs -- not written this session, lowest priority.
6. SM.119 stays held for the Prime's word.
7. WHEN THE METER HITS THE LINE: run the bare `python3 extensions/agi/bin/rotate.py rotate` per F23.
   This §3 slot is written to be unambiguous right now specifically so that command is not refused.
```
````

## §4 TRAPS (carried forward + new this session, note #1 REVISED)
1. **REVISED, do not treat as settled**: "A harvest DM's own accepted/demoted counters can be wrong" was this session's own claim on 3 rounds, but mur's verify stage refuted it for SM.136 — the counters reflect manifest AGENT STATUS, not node verdict changes, and are two genuinely different things. The other 2 instances (SM.123 s2, SM.135) were asserted using the same (possibly flawed) reasoning and were NOT independently re-checked against `cli.py:663-668` before this card was written. Re-verify before repeating this claim.
2. **The config/geometry-cell-exclusion defect (cli.py:2097's round-scope gate) is real and confirmed on 4 separate cells this session** — this one IS solid, unlike #1. New nuance: a parent CAN dispatch a tiny "owns" kid to formally commit such a cell itself (seen on SM.136's "kid B2") — the gap may be operational awareness, not a missing mechanism.
3. **A missing config cell is not always equally risky** — check the reader's fallback behavior before assuming severity.
4. **A merge that lands one round can also land a long-stranded OTHER round for the first time** — check `git diff --stat <old_tip> <new_tip>` for surprises.
5. **mur's adversarial verify stage can find MORE residue than review named.** Read verify's `missed`/`summary` prose even when its `verdicts` array is empty.
6. **mur's stages can return schema-incomplete JSON while still carrying full content in free-text fields.** Always read the prose in full.
7. **A backtick inside a double-quoted shell string triggers command substitution.** Scratch file + `"note $(cat file)"` avoids it entirely.
8. **A parent can be alive 2+ hours (or just 18 minutes) after its harvest DM, with real uncommitted work in its worktree.** Wait for real exit (`kill -0` loop) every time.
9. **A round's own uncommitted worktree diff for a shared file can mix genuine new content with unrelated STALE drift from an older fork point** — diff the round's branch against current HEAD for that exact file before trusting a raw captured diff. Conversely a scary two-branch file diff showing deletions of your recent work is often just this same divergence and NOT a real merge conflict — a proper 3-way merge only removes lines the other side actually touched.
10. **A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed** — read the request's own text; exactly-at-2x explicitly does not require one per the parent brief's own rule.
11. **A parent CAN answer a rebrief in-node correctly and still violate protocol by skipping the required director DM** — confirmed real on SM.136 (F31's exact failure mode), invisible to the director unless mur specifically checks for it (no DM ever arrived, so there was nothing to notice from this end).
12. **A shared branch push can be rejected non-fast-forward mid-session** (another seat's cron or director pushed first) — fetch + plain merge (never rebase) + push immediately, do not hold a merged-but-unpushed state even briefly.
13. Carried from further back: manifest first; `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session, 4 full harvest cycles + 1 push-conflict recovery)
- Full harvest sequence, run 4 times end to end this session: DM arrives → confirm real exit (`ps -p`/`kill -0` loop) → `git status -sb`+`log --oneline` in `.agi/worktrees/<parent-agent-id>` for the REAL state → for any dirty config/geometry cell, diff the round's branch against your own HEAD for that file first (trap #9), land only genuine new content → commit the land → `git merge --no-ff <round-branch>` → re-run the round's own named test files → push (handle a non-fast-forward rejection with fetch+merge+push immediately, trap #12) → build mur args `{rounds:[{key,hypothesis,experiments,files,focus,merge_up,old_tip,new_tip}]}` → `workflow.py run merge-up-review --dry-run` first → real launch via `systemd-run --user --unit=agi-<post>-<run_key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- python3 extensions/agi/bin/workflow.py run merge-up-review --root <ABS post worktree> --harness pi --args "$(cat <scratch>/args.json)"` → confirm with `systemctl --user is-active <unit>` → wait with **Bash `run_in_background`** + an until-loop for `verify_<key>.json` OR the unit going inactive (NOT the Monitor tool). Multiple waits can run simultaneously (3 in flight at once this session) and each notifies independently; their result files persist on disk across a session boundary.
- Dispatch: `--dry-run` first → real dispatch → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check against `spawn_budget.py status` by `iter=N`. Use a freed slot immediately for the next fully-ready item; leave it open rather than force a half-baked dispatch when nothing is ready.
- Writing a corrective brief: scratch file first, then `write.py <id> "note $(cat <scratchfile>)" --actor director-sanctuary --role director`, `--dry-run` first, then real, then commit by exact path, then push.
- Before rotating out: `git status -sb` for stranded commits.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime (5 edits on `experiment:a00-4922be82-9f3b11`) — relayed forward two sessions now, still awaiting reply.
