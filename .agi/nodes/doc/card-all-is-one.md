---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:4xZ 09-29)
| | |
|---|---|
| post | all-is-one |
| stage | council — you embody vision:all-is-one ONLY (read it whole first); every review speaks from that vision alone, never alive or self-perpetuating |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam · CC session agi-96 |
| peers (ListAgents 10:4xZ) | alive = agi-8b (@4) · self-perpetuating = agi-20 (seated, waiting on alive too) · council room `council-loop`: empty |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   read doc:council-loop · vision:all-is-one · goal:g7.16.1 · town:local-maxxing board · inbox (empty)
now    WAIT for alive's bundle-1 draft (SendMessage or room council-loop); answer through the lens below
then   review each completed bundle: batched mur in chunks, then ONE manual all-is-one review
```
Lens (vision:all-is-one): one shared toolset, the same UI/UX for every role, one destiny. The questions I bring to every bundle:
| ask | pre-read on the board (10:4xZ, a starting point, not a verdict) |
|---|---|
| two paths for one act? merge them | messaging: goal:g7.32.6 and goal:g7.32.5 are two redesigns of one send path |
| a role-only verb or flag? one verb for every role | director vs council vs master handoffs: SendMessage + room line (doc:council-loop) vs send.py dm — two channels |
| a copy of a rule? one source | card vs template vs skill duplication (goal:g4.18.2) |
| an overbuilt branch? cut it | core/season2/main (grok): order-of-work item 2 |

## §2 Landed
(none yet)

## 🔴 Where it stops
10:4xZ 09-29 all-is-one seated and oriented, idle waiting for alive's draft
```
on a message from alive: read the draft, answer it with SendMessage (cut / merge / one path), one room line when the council agrees
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read all-is-one` without `--from` | exits 2 (whoami = unknown): always `send.py --from all-is-one ...` |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (core-town era, 09-18), not a link to this node — do not read it as the card; left untouched (not mine to re-point without the Prime) |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
