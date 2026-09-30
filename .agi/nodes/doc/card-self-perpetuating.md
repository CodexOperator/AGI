---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: self-perpetuating
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (22:0xZ 09-30 · f=0.13)
| | |
|---|---|
| post | self-perpetuating · CC session agi-5b [1edcee] @36 |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 22:0xZ: alive agi-e3 [761106] @16 · all-is-one agi-15 [c6276e] @35 · Prime agi-a3 [446ae8] @30 |
| lane | free lane since 21:00Z: no Sonnet subagents, pi-free workflows only |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
DONE   goal:g7.16.1.11 design: doc:radically-simple-engine FINAL @ 586f2b4e9c (alive sent the council's ONE [decision] to belam)
       my part: §4 no standing worktrees + §8 (g)(h)(i) + the 415 B slot (inline in §7, verbatim 6/6 lines)
       result: wrap 1,272 B, a post 34 B ("tens" MET; "hundreds" missed by 273 B, stated in §1)
next   HOLD until belam relays the owner's read; then lens DG3's build (Opus 5.5 subagents, up to 3) against §8's spike
       no Unix user and no sudo before the owner's go (getent agi- = 0 at 22:1xZ)
then   no OVERVIEW until g7.16.1.1.6, .6, .7, bundle 4 close
```

## §2 Landed (09-30)
- f16cf993f9 re-linked the quorum card (trap 10)
- c98d3c680e + 0a7eb74b61: doc:radically-simple-engine §4 (716 trees ~96 GB; tree-free write 64 ms; slot 1.05 s fresh / 0.69 recycled / 0.15 mixed) + §8 (g)(h)(i) + §7 RETIRE row
- the slot script, 415 B, tested: fill · recycle · 3-way mix · keep · clean keep writes no ref · a conflicting mix exits non-zero
- agreed with all-is-one: ~/t = slot-0, clone --shared, gc.pruneExpire=never on the shared bare repo

## 🔴 Where it stops
idle: the design is with belam -> the owner; wake on belam's relay or a DG3 build line to lens
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| `replace body N:M` refuses to split a table (a table is one paragraph) | replace from a heading to the end in ONE read-modify-write, only while you hold the serialized turn |
| MAIN is shared; verify-suite.lock blocks commits | write.py lands uncommitted under the lock: commit by exact path once it clears |
| a pre-commit hook refuses owner email / GPU name / box tokens | redact and commit again; never --no-verify |
| a sha from memory is wrong after the scrub | map it through the commit-map, or re-read git log |
| an owner quote keeps its contractions; a stamp never post-dates its commit | escape `'"'"'`; check `git log -1 --format=%cI` |
| du over .agi/worktrees runs for minutes | sample one tree and multiply; never du the whole dir |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
