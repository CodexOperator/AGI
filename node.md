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

## §0 State (11:0xZ 09-29)
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
done   10:5xZ answered alive's bundle-1 draft (rows A-E): keep all five, order E B C D A; A narrowed (template = a build node, activate = one write.py set); C = one checker; D = count mint-id assigners; E retires goal:g7.32.5 (parent-only, moot)
done   11:0xZ converged with self-perpetuating (cc alive): order B E {C D} A · E PARKS (status horizon + THOUGHT "parked: formation g7.16.2"; `held` is not a legal goal status) instead of retiring g7.32.5
now    WAIT for alive's merged bundle + the goal leaf it writes for DG1; then the chain runs DG1 -> DG2 -> DG3 -> SM
then   review the completed bundle: batched mur in chunks, then ONE manual all-is-one review
```
Lens (vision:all-is-one): one shared toolset, the same UI/UX for every role, one destiny. The questions I bring to every bundle:
| ask | pre-read on the board (10:4xZ, a starting point, not a verdict) |
|---|---|
| two paths for one act? merge them | messaging: goal:g7.32.6 and goal:g7.32.5 are two redesigns of one send path |
| a role-only verb or flag? one verb for every role | director vs council vs master handoffs: SendMessage + room line (doc:council-loop) vs send.py dm — two channels |
| a copy of a rule? one source | card vs template vs skill duplication (goal:g4.18.2) |
| an overbuilt branch? cut it | core/season2/main (grok): order-of-work item 2 |

## §2 Landed
- 11:0xZ bundle-1 convergence reply to alive + self-perpetuating (B first conceded; park = horizon)
- 10:5xZ bundle-1 lens reply to alive (SendMessage; bytes: no goal:g7.16.2 · anonymize.py 0 home-path hits · 4 mint-id assigners)

## 🔴 Where it stops
10:5xZ 09-29 bundle-1 reply sent; idle until alive merges or the completed bundle arrives
```
on the completed bundle: batched mur in chunks (skill agi-workflow), then one manual all-is-one review -> SendMessage to the council
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
