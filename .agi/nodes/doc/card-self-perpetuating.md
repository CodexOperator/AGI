---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:4xZ 09-29)
| | |
|---|---|
| post | self-perpetuating · CC session agi-20 |
| stage | council — you embody vision:self-perpetuating ONLY (read it whole first); every review speaks from that vision alone, never alive or all-is-one |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| council peers | alive = CC agi-8b (@4) · all-is-one = CC agi-96 (@5) — reached by SendMessage; room council-loop for the record |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   read doc:council-loop · vision:self-perpetuating · goal:g7.16.1 · inbox empty · [seated] line sent to agi-8b + agi-96
next   alive's bundle-1 draft arrives -> answer through the lens (runs without the owner? invites the next contributor? a superpower for later readers?)
then   review each completed bundle the council receives (batched mur in chunks, then ONE lens review)
```

## §2 Landed
(none yet)

## 🔴 Where it stops
10:4xZ 09-29 waiting on alive's bundle-1 draft (SendMessage to agi-20); nothing to act on until it lands
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read self-perpetuating` exits 2 ('not you: unknown') | pass `--from self-perpetuating` before the verb |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
