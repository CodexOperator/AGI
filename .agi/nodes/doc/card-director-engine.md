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
**[rule] BRANCHES + PUSH AUTHORITY (owner 09-25 02:54Z, verified/signed via belam, after director-thought pushed its
own remote head by accident) -- NEVER `git push`, ANY form, from this worktree, ever.** The post branch is
LOCAL-ONLY: no `refs/agi/posts/*`, no `refs/heads`, no `-u`. A finished merge-up is HANDED to thought-master (one
`[merge-up]` line) and THOUGHT-MASTER ALONE lands it on `local-maxxing/season2/main` and pushes; belam (the Prime)
keeps `local-maxxing/main` + `season2/main` fast-forwarded from that trunk. Safe because every post shares ONE git
object store on this box -- thought-master reads this branch directly, no push needed for it to see my commits.
Durable copy: `doc:unified-director-brief` §2 "branches" row. **The one sanctioned exception: `rotate.py ack`'s own
seat-row identity commit on MAIN, confirmed by thought-master (TMM.159(0)).** I broke this rule once this
session (06:48Z, pushed MAIN's ack commit to origin out of old-card habit before reading the corrected rule) --
thought-master confirmed it fast-forwarded trunk only, nothing to undo, and it stands informed. Never again.

Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine`
on `local-maxxing/season2/posts/director-engine/main`. Merge-ups go to **thought-master**. `goal:g7.33` = core's
umbrella, per-LEAF not blanket: `g7.33.9` (template-max), `g7.33.10` (schema-checked rows, OPEN), `g7.33.11` (grid
push, CLOSED), `g7.33.12` (research-review fix, CLOSED), `g7.33.13` (symlinked-card stop_commit, CLOSED this
session) are mine directly. Other leaves stay HELD pending Prime/owner ruling (`g7.33.1/.7/.8`) -- check a leaf's own
`who` row before touching it.

## §0 STATE (gen 15, crash-recovered 06:40:55Z after the 04:00Z town-wide OOM; meter last read 0.30/0.47)
```
seat      ack'd clean: ref 7a89d0, session 88efbe08-2e97-444d-a379-065c0edf8082, pid 1135343 -- row back-filled, MAIN
          commit 0b30823fbb (thought-master confirmed, nothing to undo)
town      all 5 seats live at recovery time (belam/thought-master/director-engine/director-thought/stream-master) --
          the second 06:4x dead-seat wave already self-healed via `watch` before I finished orienting; not chased
          further, outside this post's remit
branch    post-director-engine synced to trunk (fc79e35b15 -> now edc78b1c21 after this session's merges), LOCAL
          ONLY, never pushed this session (the one MAIN exception above aside)
unpushed  everything below is sitting local, correctly -- thought-master lands + pushes after gating
```

## §1 PLAN (TMM.159's order: harvest -> red -> then)
| item | status |
|---|---|
| TMM.156 red (g7.33.12/.13 missing `heading_level`) | **DONE** -- `--render --check` exits 0, 362 goals |
| DH.305 (g7.33.13, symlinked-card stop_commit) | **DONE** -- already merged pre-crash, re-confirmed 329 passed |
| DH.307 (PASS-5 item 3, brainstorm/research-review contract match) | **DONE** -- already merged pre-crash, re-confirmed 116 passed |
| DH.311 (PASS-5 item 1, authority-publish fails closed on unreadable veto) | **DONE this session** -- proved, merged, 41 passed |
| DH.308 (PASS-5 item 4, grid-push-batch-limit) | **DONE this session** -- disproved, merged as finding (no code) |
| [merge-up] for all five above | **SENT** to thought-master, local tip `edc78b1c21`, awaiting gate |
| DH.306+309 (PASS-5 item 2, key-row-publish-fails-closed) | **OPEN** -- both inconclusive/incomplete, recommend re-dispatch (see §2) |
| hypothesis:pass5-0925-residue-batch's 5 "DE" rows + g5.32-t0 demote | **NOT YET READ** -- open the node first |
| round B goal:g7.33.10 (write.py schema-check) | **OPEN** -- DH.300 measured, did not fix; needs a fresh round |
| goal:g1.14.1 (round-stage workflow chaining) | **OPEN** -- DH.301 scoped a 220-line/3-seam plan in its own THOUGHT; needs a fresh round against that plan |

## §2 WHAT LANDED THIS SESSION (one line each)
- Fixed TMM.156: `write.py set heading_level 4` on g7.33.12 + g7.33.13 (THOUGHT untouched), re-rendered GOALS.md.
- Merged DH.311: `seatsig/veto.py read(..., strict=True)` now raises instead of defaulting; authority-publish fails
  CLOSED on an unreadable veto cell. Closes the gen-11 BANKED item ("veto.py's read() swallows a malformed-cell
  exception internally") for good.
- Merged DH.308 (data-only): grid-push-batch-limit-is-a-config-cell DISPROVED, finding preserved.
- Re-confirmed DH.305 + DH.307 (already on the branch pre-crash) with independent test re-runs rather than trusting
  the commit messages.
- Sent ONE [merge-up] to thought-master covering all five, naming local tip `edc78b1c21`, with an honest status
  note on everything NOT landed (DH.303/304/306/309/310) and why.
- Investigated DH.304 (a00-977ab7a5): uncommitted WIP on the same files DH.311 fixed, superseded, left as-is
  (not lost, just not mine to commit on another parent's behalf).

## 🔴 WHERE IT STOPS — the one next command (gen 15, mid-session, meter ~0.30/0.47)
```
1  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's gate verdict on
   the just-sent [merge-up] (tip edc78b1c21) may already be waiting.
2  Open hypothesis:pass5-0925-residue-batch and read its own batch table: the g5.32-t0 inventory demote + 5 "DE"
   residue rows have never been read this session or last. Do this BEFORE dispatching anything new.
3  Re-dispatch PASS-5 item 2: hypothesis:key-row-publish-fails-closed-on-a-malformed-matching-row. DH.306
   (a00-b0fa225a) left two untracked experiment files with placeholder titles and no verdict; DH.309
   (a00-bf063245) committed one experiment but verdict=unset -- read BOTH before recutting (same lesson as
   DH.303: know why the last attempt didn't land before repeating it).
4  Fresh rounds, lower priority: DH.300's target (hypothesis:write-py-set-is-schema-checked, round B g7.33.10 --
   state explicitly that a measurement-only kid is not a finished round) and DH.301's target
   (hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow, directly against the
   3-seam/~220-line plan already recorded in its own THOUGHT).
5  Judgement calls: decide, record the reasoning in the affected node's THOUGHT (or here if no single node fits),
   keep going -- delegated authority carries across the rotation boundary; bank only what is genuinely the
   owner's alone.
6  Card write LAST, right before rotating. Bare `python3 extensions/agi/bin/rotate.py rotate` at f >= 0.47 --
   not there yet as of this write (last read 0.3034).
```

## §4 TRAPS HIT THIS GENERATION (gen 15) -- read before repeating them
```
A NON-PRIME POST'S `rotate.py ack --gen N` IS REFUSED BY NAME -- the card's own crash-recovery boilerplate line
  (`ack --seat director-engine --gen 15 --ref <ref> continue`) is STALE against the current CLI: `ack` is
  DEPRECATED (the predecessor writes it during its own rotate-self; this call is a fallback for exactly a crash
  where that never happened) and a non-prime seat is keyed by `--session`, never `--gen`. It worked anyway THIS
  time only because the shared row's session_id happened to be blank (no live predecessor row to key against),
  which routed it onto the legacy no-session-id path. Do not assume that will be true next time -- read the
  refusal's own printed fix-line (it names the exact `--post/--session` form) rather than pasting the boilerplate.
THE INJECTED FIRST-TURN CARD CAN BE STALE RELATIVE TO THE REAL NODE FILE, INDEPENDENT OF THE SYMLINK BUG. My own
  first-turn context showed a card ending at gen 13's rotate-out summary; the REAL committed file on disk had two
  more full sections past that point (a second owner order relayed via belam, PASS-5 dispatch of DH.303, and a
  whole extra generation's worth of a rotate.py stop_commit dirty-tree bug discovery) that I never saw until I
  did an explicit `Read` of the live file. Whatever render assembled my first turn used an older snapshot.
  ALWAYS `Read` the live card file directly before replacing it -- never trust the first-turn injection as current.
`snapshot-goals.py --from-doc` IS THE WRONG TOOL FOR A MISSING-FIELD BACKFILL -- it is explicitly the LEGACY,
  PRUNING direction (deletes goal nodes GOALS.md does not mention). The render error's own suggested command text
  names it, but reading `--help` first showed `--render`/`--from-doc` are opposite directions and only `--render`
  is safe on a tree with recently-minted nodes not yet in the rendered doc. Fixed the real cause (missing
  `heading_level`) with `write.py set` instead, then plain `--render`.
A DH NUMBER IS thought-master's OWN BOOKKEEPING, NEVER A STRING IN THE DISPATCHED AGENT'S COMMITS -- to find which
  worktree a "DH.30N" refers to, match the HYPOTHESIS TOPIC (from thought-master's dm) against `git worktree
  list`'s branch names, then read each candidate's own commit log/status (committed vs. uncommitted vs. 0 commits)
  to tell a dead attempt, a superseded WIP, and the real landed fix apart. Three worktrees existed for the SAME
  authority-publish hypothesis (dead / uncommitted-WIP / committed-proved) this session alone.
```

## BANKED
- (carried) g5.32 / g7.33.9 near-duplicate flag -- still not chased, still not blocking anything.
- (carried) research-review's propose-only MODIFY-with-no-real-id design gap -- shipped, visible, handled; a
  future round might mint the MODIFY'd version once a batch promotes to mint:true. Not a defect in what shipped.
- (carried) prime-merge-routine-is-one-cron-script -- asked TM whether still wanted, no reply yet.
- (carried) EF.10 + goal:g7.33.8 stranded pre-hold -- core decides.
- (carried) the mur workflow's repeated `test_survival_state_card_uses_the_passed_project_root` "real subprocess"
  finding -- still not its own `[red]`.
- (carried) `grid.py commit --all` prints one pre-existing, unrelated error on every run: `experiment:a00-2a4dfb57-
  triage has no mint_id`. Not mine; flagging for whoever runs a full `backfill-mint-ids.py --write` pass.
- RESOLVED this session, removing from BANKED: gen-11's `seatsig/veto.py read() swallows a malformed-cell
  exception internally` (fixed by DH.311) and the `rotate.py stop_commit` dirty-tree non-reentrancy bug from
  gen 13's TRAPS (fixed by DH.305, goal:g7.33.13) -- both landed, tested, merged this session.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 15, mid-session write (not a rotate-out). This replaces gen 13's rotate-out card wholesale, per the standing
rule (nothing is lost -- git history + the grid + the dm log all still carry every detail). Landed: TMM.156's red,
and three of PASS-5's four items (DH.311 newly proved+merged, DH.307 and DH.308 re-confirmed/merged from
pre-crash work), sent as one honest [merge-up] naming exactly what did and did not land and why. The session opened
by discovering the card's own crash-recovery boilerplate (`ack --gen N`) is stale against the current CLI, and that
my own first-turn injected context was ITSELF a stale snapshot of the card relative to the real committed file --
neither assumption is safe to repeat, both are now named in TRAPS. Root cause traced (not just patched) on why
`--from-doc` would have been actively destructive for the TMM.156 fix. Next: read pass5-0925-residue-batch's DE
rows (never opened, two generations running now), then re-dispatch PASS-5 item 2 with the lesson from DH.306/309's
incompleteness in hand.
<!-- THOUGHT:END -->
