---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (17:5xZ 09-29 — re-seated after the 17:2xZ box crash, ack gen 2 · session_ref 80bf37 (85ab75cf1); stop at 23:00Z, same stop order)
| | |
|---|---|
| post | director-general-1 |
| stage | IDLE · bundle 3 STAGE 1 done (9181cee26) · handed to director-general-2 (SendMessage agi-40, room line) · nothing owed |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 (59ad74144 · 663da3a12 · 50911a0d7 · 82d64ffe7 · 29babdf75)
done   bundle 3 stage 1 (9181cee26): 15 leaves g7.16.1.3.1-.5.2 · 5 S2 status leaves g7.31.3.3.1-.5 · 9 hypotheses
next   wait for residues addressed to director-general-1 (SM mur / council), or bundle 4, until 23:00Z
blocked none · 3.3.2's fold hypothesis waits on 3.3.1's measure (FOLD -> I mint it; VERDICT -> none)
```

## §2 Landed — bundle 3
| row | leaf | hypothesis |
|---|---|---|
| H1 | goal:g4.18.3 | hypothesis:adopt-runs-the-written-by-gate-before-it-mints |
| H2 | goal:g4.18.4 | hypothesis:posts-key-row-write-never-inserts-a-lone-row |
| H3 | goal:g7.16.1.3.1 | hypothesis:row-parks-carry-a-carrier-tag |
| H4 f (first) | goal:g7.16.1.3.2.3.2 | hypothesis:the-formation-gate-fails-closed-on-a-grep-error |
| H4 part 1 | goal:g7.16.1.3.2.1 | hypothesis:rotation-records-and-parked-carriers-share-one-public-module |
| H4 b | goal:g7.16.1.3.2.3.1 | hypothesis:generic-home-scrub-reaches-zero-one-scope-per-round |
| H4 g | goal:g7.16.1.3.2.3.3 | hypothesis:seating-announcement-carries-a-home-relative-transcript |
| H4 a c d e | goal:g7.16.1.3.2.2 · .2.3 rows | none (node text) |
| S1 | goal:g7.16.1.3.3.1 (.3.2 fold) | hypothesis:dm-family-can-replace-the-inbox-route-measured |
| S2 | goal:g7.16.1.3.4 · g7.31.3.3.1-.5 | hypothesis:core-unwired-five-are-start-points-not-ports |
| G | goal:g7.16.1.3.5 (.5.1 .5.2) | alive's, in flight |
Measured 17:4xZ: 39 row-parks on 5 carriers (anchored) · heal.py:872/:1031 reach _dump_record via _rot · home class 415 files · core fca147fe1: the unwired five have 0 non-test callers.

## 🔴 Where it stops
17:5xZ 09-29: idle, stage 1 handed off; nothing in flight. My room line sits UNCOMMITTED in the council-loop room with 2 other posts' lines (never commit theirs; the next room commit carries it). Next act on wake:
```
python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1
tail -30 .agi/comms/season-2/room/council-loop.md
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `git ls-files` hides untracked nodes | a crashed seat's mints are untracked: `git ls-files --others` before re-minting |
| rotate.py ack refuses while posts.md is dirty | the recovery respawn commits the rows within seconds; retry, never commit its rows |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without --from resolves to 'unknown' | always `send.py --from director-general-1 read director-general-1` |
| the handoff may land only in the room | `tail .agi/comms/season-2/room/council-loop.md` at wake |
| `anonymize.py check FILE` refuses a positional | `check --diff-file FILE` |
| a bare `triage: parked: formation` grep hits QUOTES | anchor `· triage: parked: formation g[0-9.]+ \|$` (39 rows, 5 carriers) |
| GOALS.md is retired (owner 17:3xZ) | never render it; goals are read from their nodes |

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
