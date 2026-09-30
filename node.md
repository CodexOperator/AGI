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
DONE   round 1 586f2b4e9c · round 2 FINAL c9800a4537 / 9d4076f96a (4,253 B living system; my §C 1,459 B)
NOW    ROUND 3 (belam 23:01Z; owner: ".geometry could about contain all the graph build nodes"). Serialized:
       me part 1 = §F the SHAPE TEST (DONE 81f0620954) -> all-is-one part 2 (links = symlinks, vector brief A^k e_post)
       -> alive's successor part 3 (injection on start/resume/compact · transparency · diagram · falsifiers · the [decision])
next   read parts 2 + 3 through my lens (F13-F15 carried? symlinks kept out of a node's page?), accept or amend
then   HOLD until the owner's go; no Unix user, no sudo
```

## §2 Landed (09-30)
- f16cf993f9 card re-link · round 1: §4 + the 415 B slot · round 2: §C (projector 664 B fixed point · seed 291 B · frontier 384 B · V)
- round 3 §F 81f0620954: bar = 1 page 4,096 B · genome runs FROM .geometry nodes (fixed point tested) · 6/18 fit, overflow = prose except commands + posts · engine as .geometry ~31 KB vs 327 KB
- pieces + the scratch clone: /tmp/g71611/fp-src (g-*.md = the three genome nodes), /tmp/g71611/fp (--shared clone; trunk spike-only)

## 🔴 Where it stops
waiting on all-is-one part 2, then alive's successor part 3; read the doc when pinged
```
python3 extensions/agi/bin/write.py doc:radically-simple-engine 'read body 1:600' | grep -n '^## '
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
