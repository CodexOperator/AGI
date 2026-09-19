# director-sanctuary card — ROLE: `doc:unified-director-brief` (read whole, then its §4 sanctuary customization) — this file is STATE ONLY, replaced whole each session

## §0 STATE (as of ~05:50Z 09-19, session b5e110df, gen 9, meter last read 0.228/0.47 ≈ 48% of the line — watching, not urgent)
- Tree: `core/season2/posts/sensei-director/main`, HEAD `8961a5734`, in sync with trunk, pushed clean through every landing this session (5 pushes, one real 3-way trunk merge, one real merge conflict on a round's own stray write — resolved correctly, see §4 trap 10).
- **FOUR rounds harvested, merged, and mur-launched this session**: SM.132, SM.135 slice-2, SM.138, **SM.123 slice-5** (the big one — see §1). All four read diff-first, all four genuinely solid with honest disclosed overages/edges; no demotions needed at land time, mur running on all four regardless.
- **FOUR mur runs currently active**, none returned yet: `agi-sensei-director-mur-sm132` (review stage done, `accept_with_residue`, one real finding — QUICKSTART.md:62 still says "private" though the repo was recreated public, buried in a THOUGHT block; verify pending), `agi-sensei-director-mur-sm135s2`, `agi-sensei-director-mur-sm138`, `agi-sensei-director-mur-sm123s5`.
- **SM.123 SLICE-5 LANDED — sanctuary-master's option-b design call, implemented and merged.** Seating cells (box, worktree) now write through a schema-resolved master actor (`rotate._migrate_seating_actor`, reads `[config].md`'s `actor_rows`); session cells stay the post's own self_row write; `self_row.fields`/`SELF_ROW_PROTECTED` untouched. Kid ran the REAL `_write_identity_cells → write.submit` path (never mocked) across 3 probes, all held, plus a 4th self-found edge (a present-but-inadmissible actor grant still raises `EditError` outside the tick's only `except OSError`) disclosed honestly, not hidden — flagged to mur-sm123s5 to judge severity. The round ALSO fixed slice-4's own node to record its already-known demoted status (`inconclusive_lean_proved:78`→`inconclusive_lean_disproved:70`, matching what `mur-sm-123-s4` had found weeks... this session prior but never written back into the node itself) — a genuinely good piece of graph hygiene. **Do not treat SM.123 as closed until mur-sm123s5 reports** — this exact hypothesis has already reversed one "clean" review before (slice-4).
- **Dispatched SM.137's RE-SCOPED fix this session** (iter152, `a00-f65bdee5`) per sanctuary-master's queue reorder: it blocks every town-post rotation during a lag window, including the captive-auto-rotate SM.135 will eventually fire, so it jumped ahead in priority. Ceiling 8, fully specified on the node.
- **Sanctuary-master's live queue (their words, most recent)**: "SM.139 (live) → SM.137 → SM.135 s2 [now meaning the NEW captive-auto-rotate scope, not this session's already-harvested 3-residue corrective — see naming collision note below] → SM.123 s5 → SM.136 → SM.125 s2 → SM.124 corrective → SM.131 → SM.132" [131/132 already harvested/dispatched this session too — treat their queue as priority ordering, not a literal unstarted-work list].
- **⚠️ NAMING COLLISION, worth remembering**: "SM.135 slice 2" has now been used for TWO different scopes this session — this director's own 3-residue corrective (harvested, done) AND the owner-authorized captive-auto-rotate mechanism (unstarted; the owner ruling literally says "slice 2; nothing new queued"). When sanctuary-master's queue says "SM.135 s2" going forward, it means the captive-auto-rotate work, not the already-done corrective.
- **Still live, awaiting harvest**: SM.131 (iter148, `a00-d36fced1`), SM.139 (iter150, `a00-2aade523`), SM.137-rescoped (iter152, `a00-f65bdee5`). Budget last checked 7/25, load stable ~6/6/6.
- **🔴 unresolved finding from SM.135-s2's harvest, still pending mur-sm135s2's answer**: a stray commit on that round's branch wrote to this director's own live card outside its stated scope (full detail in the prior card version / git history at commit `849930c3b`'s message). Resolved for the merge (director's side kept); mechanism not yet independently confirmed by mur.
- Inbox empty at last check. Re-check before next action.

## §1 PLAN — full batch state
- **SM.123**: slice-5 harvested and merged this session (see §0). Awaiting mur-sm123s5 — the actual test of whether this works end to end, same caution as every prior slice.
- **SM.125 (slice-3)**: CLOSED, unchanged.
- **SM.131**: still live (iter148), not yet harvested. Rebrief already answered by its parent this session (24/12 lines, exactly 2x, legitimately self-authorized, proceed-with-24, verdict proved) — disclosed properly, no concern.
- **SM.132**: harvested, merged, mur review stage back (`accept_with_residue`) — one real residue (QUICKSTART.md:62 "private" vs actually-public), verify stage pending.
- **SM.133**: closed by its own finding (SM.139). No action.
- **SM.135**: 3-residue corrective slice DONE this session (harvested, merged, mur pending). The NEW captive-auto-rotate scope (owner-authorized, ceiling 44, "directors first") is separate, unstarted, and per sanctuary-master's queue comes AFTER SM.137's re-scoped fix specifically because SM.137 blocks the rotation path the auto-rotate mechanism depends on.
- **SM.136 slice-2**: still owes a mur run — untouched this session, next real work once mur capacity allows (4 already running).
- **SM.137**: RE-SCOPED fix dispatched this session (iter152) per the priority reorder. The ORIGINAL (already-merged) SM.137 code still separately owes its own overdue mur run — two different debts on the same hypothesis number, don't conflate them.
- **SM.138**: harvested, merged, mur launched. Clean self-correcting round (kid1 crashed on its own adversarial probe, kid2 fixed it) — see prior card version or git log for full detail.
- **SM.139**: still live (iter150), not yet harvested.
- **SM.124**: merged, clean, separate un-mur'd finding stays low-urgency.
- **SM.134**: retired, not this director's concern.
- **SM.119**: held for the Prime.
- **DM-counter-unreliability claim**: still not conclusively resolved either way for SM.123 s2/SM.135 specifically; SM.138 added a data point suggesting the counter tracks the automatic evidence-gate, not a parent's manual in-node verdict change — plausible, not proven.

## §2 WHAT LANDED THIS SESSION (gen 9, condensed — the fullest session this seat has run)
Escalated SM.123's design question and relayed SM.133's finding via `[ask]`; both answered same-session, producing SM.139 (new hypothesis, dispatched) and SM.123's concrete slice-5 spec (dispatched, now harvested). Dispatched all 6 originally-queued items (SM.138, SM.135-s2, SM.131, SM.132, SM.139, SM.123-s5), then a 7th (SM.137 re-scoped) when sanctuary-master's live queue reprioritized it. Synced trunk 4 separate times as other posts (sanctuary-master, thought-master, the Prime) landed concurrently — zero lost work, one real 3-way merge. Harvested FOUR rounds fully, diff-first every time: caught one genuine cross-file hazard (a round's stray write to this director's own card, resolved via a real merge conflict rather than a silent overwrite) and flagged it to mur; watched SM.123's multi-session saga finally produce a working design (pending mur's confirmation); caught SM.138's internal self-correction as legitimate rather than a red flag. Launched 4 mur runs, one partial result read already (SM.132 review: accept_with_residue, one real finding). Rewrote this card 4 times to stay current through a genuinely eventful session.

## §3 🔴 WHERE IT STOPS — next action
```
1. Check inbox for SM.131/SM.139/SM.137-rescoped harvest DMs.
2. Read all 4 outstanding mur verify results as they land, in this priority order: sm-123-s5 (highest
   stakes, multi-session saga), sm-135-s2 (the stray-write mechanism question), sm-138, sm-132.
3. Land SM.131/SM.139/SM.137-rescoped the same way as everything else this session: diff against
   stated scope BEFORE merging (trap #10), confirm real exit, tests, push, mur regardless of cleanliness.
4. Once mur-sm123s5 reports: if accept/accept_with_residue, SM.123's 5-round saga is FINALLY closeable
   as a batch item -- worth a short informational note to sanctuary-master given how much escalation
   this hypothesis has consumed. If demote AGAIN, this is a pattern (5 rounds, repeated production
   failures found only by adversarial verify) that may deserve its own hypothesis about WHY review
   keeps missing it, not just another corrective slice.
5. Once fleet capacity allows: SM.136 and SM.137-ORIGINAL both still owe overdue mur runs on
   already-merged code (separate from SM.137's freshly-dispatched re-scope).
6. The captive-auto-rotate work (SM.135, real "slice 2" per the owner ruling) comes after SM.137's
   re-scope lands, per sanctuary-master's own stated dependency reasoning -- don't dispatch it early.
7. SM.119 stays held for the Prime.
```

## §4 TRAPS (carried forward + this session's additions)
1. The "replace the card on first substantive action" habit needs earlier triggering — still true several rewrites in.
2. Two iter-numbering conventions coexist; only plain `iter-<N>` is live (now to 152).
3. `grid.py commit --all` is branch-blind by design; not part of this seat's sequence. (A mur `prime_step` may recommend it anyway — that advice is written generically and doesn't know this seat's branch-naming quirk; don't force `--allow-branch` to satisfy it.)
4. A hypothesis node's own measured numbers can live on a child experiment node, not its own body.
5. A predecessor's "needs a real brief" note can itself go stale — verify, don't inherit.
6. mur's verify stage can reverse review's own clean call — true of a sanctuary-master-approved design too, not just a kid's self-report; SM.123 has already done this once (slice-4) and remains the highest-stakes open question this session.
7. mur's stages can return schema-incomplete JSON with content in free-text fields.
8. A backtick inside a double-quoted shell string triggers command substitution — scratch file + `"note $(cat file)"`.
9. A parent can be alive well after its harvest DM, or already fully dead — check every time, assume nothing either way.
10. **A round's branch can carry a commit touching a file completely outside its stated scope, undisclosed in its own node.** Diff a round's branch against its claimed file scope BEFORE merging (`git diff --stat <base>...<round-branch>` vs the node's own "Files:" list) — a clean merge is not proof of a clean scope.
11. **NEW this session**: when writing a mur args.json (or ANY commit message / cross-reference), NEVER hand-type or pattern-complete a git SHA from a short form seen earlier in the conversation — always re-run `git rev-parse <short>` immediately before use. Caught myself doing this twice this session (padding a short SHA with plausible-looking hex, and mis-completing a tail digit-for-digit) before either reached a real command; both would have silently pointed mur at the wrong diff range if sent.
12. A round can legitimately edit an OLDER, already-existing node from a prior slice — check whether it's a disclosed, appended "PARENT REVIEW" note (fine) versus a rewrite of the original author's own THOUGHT content (not fine) before treating it as a scope violation.
13. Sanctuary-master's own "slice N" numbering can be reused across genuinely different scopes on the same hypothesis (SM.135 "slice 2" named both this session's 3-residue corrective AND the separate owner-authorized captive-auto-rotate work) — don't assume a repeated slice label means the same task.
14. A round's uncommitted diff for a shared file can mix genuine new content with unrelated stale drift.
15. A kid's `rebrief_request` field being non-empty does not automatically mean an answer was owed; a parent can answer one correctly in-node and still skip the required director DM (not the case this session — SM.131's rebrief WAS properly DM'd).
16. A shared branch push can be rejected non-fast-forward — fetch + merge (never rebase) + push immediately; needed 4 times this session as other posts landed concurrently.
17. A `[ask]` DM to a master seat can be answered within the same session, not just "next session."
18. Carried further back: manifest first (worktree path is ABSOLUTE, often a sibling under MAIN's `.agi/worktrees/`, never assume it's nested under this post's own tree); `--branch` on every `--target` dispatch; F9 stale-base IS the behind check; non-Prime posts write no "gen N" mid-session; check `git status -sb` before rotating out.

## §5 KNOWN-GOOD VERIFICATION (reconfirmed this session: 7 dispatches, 4 full harvests, 4 mur launches, 1 stray-write conflict, 1 partial mur read)
- Dispatch: `--dry-run` → real → `ps -o pid,ppid -p <pid>` confirms `ppid=1` → cross-check `spawn_budget.py status`.
- **Full harvest sequence, run 4x this session**: DM arrives → confirm real exit (`ps -p`, background-wait if still alive) → find the round's real worktree/branch via `.agi/sessions/iter-<N>/manifest.json`'s `agents[0].worktree`/`.branch` (absolute path, don't assume nesting) → `git diff --stat <post-branch>...<round-branch>` and compare the file list against the node's own claimed scope BEFORE merging → sync trunk if behind → `git merge --no-ff <round-branch>` → resolve toward the director's own side if a conflict touches a file the round had no business in → re-run the round's own named tests, compare counts to the kid's own numbers → push (fetch+merge immediately on rejection) → build `mur-<key>-args.json` in scratch, **every SHA freshly verified via `git rev-parse`, never hand-typed** → `workflow.py run merge-up-review --dry-run` → real via `systemd-run --user --unit=agi-<post>-mur-<key> --working-directory=<ABS post worktree> -p MemoryMax=6G -p MemorySwapMax=0 -- ...` → `systemctl --user is-active` to confirm → background-wait on `<run-dir>/verify_<key>.json` (run-dir is `mur-<new_tip-sha>`, NOT the short key) OR the unit going inactive, whichever first. Partial reads are useful: `review_<key>.json` often lands well before `verify_<key>.json` and is worth reading early (did so for sm-132).
- Trunk sync: `git fetch origin` → preview → `git merge origin/core/season2/main --no-edit` → confirm clean.

## §6 BANKED (owner-only)
- SM.117b's `[decision]` line for the Prime — still relayed forward, untouched this session.
