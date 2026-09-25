---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: belam-S2-L5-IV
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## IDENTITY
**[rule] BRANCHES + PUSH AUTHORITY (owner 09-25 02:54Z, verified/signed via belam) -- NEVER `git push`, ANY form,
from this worktree, ever.** Post branch is LOCAL-ONLY. A finished merge-up is HANDED to thought-master (one
`[merge-up]` line); thought-master ALONE lands it on `local-maxxing/season2/main` and pushes. Durable copy:
`doc:unified-director-brief` §2 "branches" row. One sanctioned exception: `rotate.py ack`'s own seat-row identity
commit on MAIN (confirmed by thought-master, TMM.159(0)) -- I broke the git-push half of this once this session
(06:48Z, old-card habit) before reading the corrected rule; thought-master confirmed nothing to undo. Never again.

Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine`
on `local-maxxing/season2/posts/director-engine/main`. Merge-ups go to **thought-master**. `goal:g7.33` leaves mine
directly: `g7.33.9` (template-max), `g7.33.10` (schema-checked rows, OPEN), `g7.33.11`/`.12`/`.13` (CLOSED). Other
leaves stay HELD pending Prime/owner ruling (`g7.33.1/.7/.8`) -- check a leaf's own `who` row before touching it.

## §0 STATE (gen 15, crash-recovered 06:40:55Z after the 04:00Z town-wide OOM; meter last read 0.373/0.47)
```
seat      ack'd clean: ref 7a89d0, session 88efbe08-2e97-444d-a379-065c0edf8082, pid 1135343
branch    post-director-engine synced to trunk, LOCAL ONLY throughout except the one MAIN ack exception above
tip       131c7319d1 (local, unpushed by design -- thought-master lands + pushes after gating)
merge-ups sent this session: #1 @edc78b1c21 (TMM.156 red + DH.305/307/311/308), #2 @131c7319d1 (TMM.160's tags
          fix + a naming correction) -- #1 was CLEAN on thought-master's gate as of TMM.160 (merge-tree, goals,
          links, anonymize, strict-veto-on-live-cell all OK); full suite was still running as of that read
```

## §1 PLAN
| item | status |
|---|---|
| TMM.156 red (g7.33.12/.13 missing `heading_level`) | **DONE** |
| DH.304 (PASS-5 item 1, authority-publish fails closed on unreadable veto) | **DONE this session** -- proved, merged, 41 passed. **NAME CORRECTION (TMM.160): this is DH.304, not DH.311** -- my own merge commit message says "merge DH.311" and is wrong; not rewritten (immutable), corrected here |
| DH.307 (PASS-5 item 3, brainstorm/research-review contract match) | **DONE** -- already merged pre-crash, re-confirmed 116 passed |
| DH.305 (g7.33.13, symlinked-card stop_commit) | **DONE** -- already merged pre-crash, re-confirmed 329 passed; now also carries required `tags` (TMM.160) |
| DH.308 (PASS-5 item 4, grid-push-batch-limit) | **DONE this session** -- disproved, merged as finding (no code) |
| TMM.160 (g7.33.13 missing `tags`) | **DONE** -- write.py set tags [local-maxxing, engine, rotate] |
| [merge-up] x2 | **SENT** -- @edc78b1c21 (clean on gate, full suite pending at last read), @131c7319d1 (delta) |
| PASS-5 item 2: DH.306+309 (key-row-publish-fails-closed) | **OPEN, approved to re-dispatch (TMM.160)** -- both prior attempts left an empty experiment template; the real mechanism (`_authority_row_content` returns SKIPPED instead of a named refusal on a malformed row) is now recorded in the hypothesis's own THOUGHT so the next round starts briefed. **NOT dispatched yet this session** -- meter was already at 78%+ of the line; banked as the clean next task rather than rushed |
| **DH.311** (a00-977ab7a5) | uncommitted WIP on veto.py + test_rotate_key_authority.py, same files DH.304 already fixed and merged -- superseded, not lost (sits uncommitted in that worktree), not mine to commit on another parent's behalf |
| hypothesis:pass5-0925-residue-batch: 5 "DE" rows + g5.32-t0 demote | **READ this session, not yet acted on.** The 5 DE items: (1) demote g5.32-t0-hardcoded-prose-inventory-and-template-loader (inventory misses claimed surface, contradicts code, out-of-scope wording change, call sites drifted 6->9); (2) residue key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post (evidence count stale, distinct worktree handoff not evidenced); (3) residue engine-delta-1 (real-remote grid push claim has no experiment evidence, scoped tests met a live suite lock); (4) residue a00-93414710-7b19d2 (claim's first sentence overstates remote atomicity, with the grid defect); (5) residue rotation-alert-t1-capture-cluster-templated (call-site sweep not committed). Each needs its OWN corrective round per the standing "mur residues close in-loop" rule -- none dispatched yet |
| round B goal:g7.33.10 (write.py schema-check) | **OPEN** -- DH.300 measured, did not fix |
| goal:g1.14.1 (round-stage workflow chaining) | **OPEN** -- DH.301 scoped a 220-line/3-seam plan in its own THOUGHT |

## §2 WHAT LANDED THIS SESSION (one line each)
- Fixed TMM.156 (missing `heading_level` on g7.33.12/.13) and TMM.160 (missing `tags` on g7.33.13).
- Merged DH.304 (mislabeled DH.311 in my own commit message, see correction above): veto.py `read(..., strict=True)`
  now raises instead of defaulting; authority-publish fails CLOSED. Closes the gen-11 BANKED veto.py item for good.
- Merged DH.308 (data-only): grid-push-batch-limit-is-a-config-cell DISPROVED, finding preserved.
- Re-confirmed DH.305 + DH.307 (already on the branch pre-crash) with independent test re-runs.
- Sent two [merge-up]s; thought-master's TMM.160 confirms #1 clean on gate so far.
- Root-caused and recorded (never landed a fix for) DH.306/309's near-miss on key-row-publish in the hypothesis's
  own THOUGHT: a malformed matching row hits `_authority_row_content`'s parse-failure branch, which leaves content
  unchanged and returns `SKIPPED` rather than a named refusal -- same shape as the veto.py bug DH.304 just fixed.

## 🔴 WHERE IT STOPS — the one next command (gen 15, rotating now at meter ~0.373-0.38/0.47)
```
1  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's full-suite gate
   verdict on @edc78b1c21/@131c7319d1 likely landed by now.
2  Dispatch PASS-5 item 2 (approved, TMM.160): hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row.
   Its THOUGHT already carries the mechanism (rotate.py:10418-10470, _authority_row_content SKIPPED-not-refused)
   and the fix shape (DH.304's veto.py pattern: raise/catch broadly, return a named string on the exception path).
   Brief the parent explicitly: a prior kid died on a 401 before touching bytes -- check `provisioning.py status`
   if that recurs, don't assume the hypothesis itself is at fault; a kid producing an EMPTY experiment template
   is not evidence, re-cut rather than accept it as done.
3  Then, in priority order: the 5 "DE" residue rows + g5.32-t0 demote from hypothesis:pass5-0925-residue-batch
   (full list in §1 above -- each gets its own corrective round, dispatched without asking, per the standing
   "mur residues close in-loop" rule), then round B goal:g7.33.10, then goal:g1.14.1.
4  Judgement calls: decide, record the reasoning in the affected node's THOUGHT (or here if no single node fits),
   keep going -- delegated authority carries across the rotation boundary; bank only what is genuinely the
   owner's alone.
5  Card write LAST, right before rotating.
```

## §4 TRAPS HIT THIS GENERATION (gen 15) -- read before repeating them
```
A NON-PRIME POST'S `rotate.py ack --gen N` IS REFUSED BY NAME -- `ack` is DEPRECATED (the predecessor normally
  writes it during its own rotate-self; this is a crash-recovery fallback) and a non-prime seat is keyed by
  `--session`, never `--gen`. It worked THIS time only because the shared row's session_id happened to be blank.
  Read the refusal's own printed fix-line rather than pasting old boilerplate next time.
THE INJECTED FIRST-TURN CARD CAN BE STALE RELATIVE TO THE REAL NODE FILE, independent of the symlink bug gen 13
  found. My own first-turn context ended at gen 13's rotate-out summary; the real committed file had two more
  full sections past that (PASS-5 dispatch, a rotate.py stop_commit bug). ALWAYS `Read` the live card file
  directly before replacing it -- never trust the first-turn injection as current.
`snapshot-goals.py --from-doc` IS THE WRONG TOOL FOR A MISSING-FIELD BACKFILL -- it is the LEGACY, PRUNING
  direction (deletes goal nodes GOALS.md does not mention). Use `write.py set <field> <value>` for a targeted
  frontmatter fix, then plain `--render`.
`write.py <node_id> <verb> <args...>` TAKES THE WHOLE VERB INVOCATION AS **ONE** "script" STRING, NOT SEPARATE
  ARGV ELEMENTS -- `subprocess.run(['write.py', node_id, 'thought', text])` puts `text` in the SLUG positional and
  fails with "missing 1 required positional argument"; it must be `subprocess.run(['write.py', node_id, 'thought '
  + text])`. Cost two failed attempts this session (one from shell quote-escaping, one from this).
A DH NUMBER IS thought-master's OWN BOOKKEEPING, NEVER A STRING IN THE DISPATCHED AGENT'S COMMITS, AND IS EASY TO
  MISASSIGN WHEN TWO PARENTS SHARE A HYPOTHESIS TOPIC -- I labeled a00-a4efedba's committed, proved fix "DH.311"
  and a00-977ab7a5's uncommitted WIP "DH.304"; thought-master's own TMM.160 corrected it the other way around
  (a00-a4efedba = DH.304, a00-977ab7a5 = DH.311). The commit message is immutable and now says the wrong number
  for an otherwise-correct merge -- the correction lives here and in the dm log, not in a rewritten commit.
```

## BANKED
- (carried) g5.32 / g7.33.9 near-duplicate flag -- still not chased, still not blocking anything.
- (carried) research-review's propose-only MODIFY-with-no-real-id design gap -- shipped, visible, handled.
- (carried) prime-merge-routine-is-one-cron-script -- asked TM whether still wanted, no reply yet.
- (carried) EF.10 + goal:g7.33.8 stranded pre-hold -- core decides.
- (carried) the mur workflow's repeated `test_survival_state_card_uses_the_passed_project_root` "real subprocess"
  finding -- still not its own `[red]`.
- (carried) `grid.py commit --all` prints one pre-existing, unrelated error every run: `experiment:a00-2a4dfb57-
  triage has no mint_id`. Not mine; flagging for whoever runs a full `backfill-mint-ids.py --write` pass.
- (carried) `write.py create --set` still does not coerce a list-typed schema field, and a missing required field
  on create is not refused -- goal:g7.33.10 (round B) is the round that fixes this; still open.
- RESOLVED this session: gen-11's `seatsig/veto.py read() swallows a malformed-cell exception internally` (fixed
  by DH.304) and the `rotate.py stop_commit` dirty-tree non-reentrancy bug from gen 13's TRAPS (fixed by DH.305).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 15, rotating out. Landed TMM.156 + TMM.160's reds, three of PASS-5's four code defects (DH.304 newly
proved+merged, DH.307 + DH.308 re-confirmed/merged from pre-crash work), and sent two honest [merge-up]s -- the
first already reads clean on thought-master's gate. Chose NOT to squeeze in PASS-5 item 2's re-dispatch this
generation despite it being approved and fully briefed (the hypothesis's own THOUGHT now carries the exact
mechanism and fix shape) because the meter was already past 75% of the line when the approval arrived; a rushed
dispatch risks a worse brief than a clean handoff. Caught and corrected my own DH.304/DH.311 mislabeling from
thought-master's read of the actual bytes rather than defending the original guess -- the commit message is wrong
and immutable, the record here and in the dm log is right. Two small but real tool-usage lessons banked in TRAPS
(write.py's script-string arity, ack's non-prime --gen refusal) so the next generation does not re-pay for either.
<!-- THOUGHT:END -->
