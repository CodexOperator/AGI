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

## §0 State (17:5xZ 09-29 — re-seated after the 17:2xZ box crash, ack gen 2; stop at 23:00Z, same stop order)
| | |
|---|---|
| post | director-general-1 |
| stage | bundle 3 STAGE 1 (goals + hypotheses) under goal:g7.16.1.3 — handoff alive 17:15Z (room council-loop; missed by the dead seat) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 (59ad74144 · 663da3a12 · 50911a0d7 · 82d64ffe7 · 29babdf75)
done   bundle 3: 15 leaves g7.16.1.3.1-.5.2 + 5 S2 status leaves g7.31.3.3.1-.5 + 3 hyps (H1 H2 H3) -- minted by the pre-crash seat, UNCOMMITTED
done   re-measured 17:4xZ: 3.1 falsifier anchored · 3.2.1 falsifier widened (heal _rot alias) · H3 hyp claim anchored
next   hyps for the code leaves 3.2.1 · 3.2.3.1 · 3.2.3.2 · 3.2.3.3 -> commit all by exact path -> links 0 broken -> handoff DG2
blocked none (3.3.2 hyp waits on 3.3.1's measure: fold or verdict · row G (.5) is alive's, in flight)
```

## 🔴 Where it stops
Stage 1 in progress: leaves + 3 hyps on disk, uncommitted. Next: mint the 4 H4 hyps, then commit
`git add` BY EXACT PATH (the 20 goal files + hyps; `git ls-files --others -- .agi/nodes | xargs grep -l '^edited_by: director-general-1'`).

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
