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

## §0 State (20:4xZ 09-29 — re-seated after the 17:2xZ crash, ack gen 2 · session_ref 80bf37; stop at 23:00Z, same stop order)
| | |
|---|---|
| post | director-general-1 |
| stage | IDLE · bundle 4 STAGE 1 done (db3e22e55), handed to director-general-2 · bundle 3 CLOSED 1f39ffb1c (SM clean, council 11/11); bundle 4 base moved to 1f39ffb1c (eef097d03), build HOLD lifted · nothing owed |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 · bundle 3 stage 1 (9181cee26) + row R (11b2de165, R1 v3 b2d946498: grouped cutover)
done   bundle 4 stage 1 (db3e22e55): 14 leaves + 12 hyps; retired g7.16.1.3.5/.5.1/.5.2 (row G moved to .4.1)
done   heading_level red fixed (68f23e0f6) · W-G names 6 callers (521334b6b) · RE-SCOPE on DG2 verdicts (68d4c8504): W2b/W2c/W2d -> 7 leaves + 7 hyps, W3c ceiling 90 not split
next   residues addressed to director-general-1 (SM mur / council) until 23:00Z
blocked none
```

## §2 Landed — bundle 4 (goal:g7.16.1.4, base ddea3a61f)
| row | leaf | hypothesis |
|---|---|---|
| input FIRST | g7.16.1.4.3 | core-write-hunks-each-get-a-named-disposition (12 hunks since 8e4b4c286) |
| W-G | g7.16.1.4.1 | goals-md-retires-with-every-caller-in-one-row |
| W0 | g7.16.1.4.2 | none (retitle g4.19) |
| W1 | g4.18.5.1 · .2 · .3 | body-rows-share-one-index-for-write-and-render · a-write-is-its-own-commit-behind-the-gate · posts-rows-have-one-writer-and-one-parser |
| W2 (re-scoped 68d4c8504: .2 -> .2.1/.2.2 · .3 -> .3.1/.3.2/.3.3 · .4 needs .4.1/.4.2) | g4.18.6.1 · .2 · .3 · .4 · .5 | one-resolver-maps-mint-ids-to-addresses · a-write-refuses-a-missing-outbound-id-by-lookup · every-link-reader-resolves-mint-ids · link-lines-migrate-to-mint-ids-counted · none (text) |
| W3 | g4.18.7.1 · .2 · .3 | viewport-renders-one-node-for-both-readers · node-search-lives-beside-node-writer · read-leaves-write-py-with-every-teacher-in-one-row |
Calls (on the THOUGHTs, sent to alive): W-G = one read path at every moment (lands first, .7.3 moves its line) · W0 retitle not park · W2 readers before migration.

## 🔴 Where it stops
20:4xZ 09-29: idle, nothing in flight. My room lines sit uncommitted in the council-loop room with other posts' lines (never commit theirs). Next act on wake:
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
| a goal minted without heading_level (DG2 [red] 20:4xZ, fixed 68f23e0f6) | `--set heading_level=<id segment count>` on every goal create; the render hard-fails without it and reds every closeout |
| a count or claim copied into every leaf of a row | measure it once per row with its own command; a wrong shared Measured line (W2: 8654, no walk, links gates parents) was wrong in 5 leaves at once |
| GOALS.md is retired (owner 17:3xZ) | never render it; goals are read from their nodes |
| moving a live process tree into a scope (R1 cutover, measured 18:4xZ on dummies) | AttachProcessesToUnit needs a Delegate=yes target; a moved parent leaves its children: move EVERY pid; probe with sleep dummies only, never tmux / a post / the RC service |

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
