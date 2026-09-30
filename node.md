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
DONE   rounds 1-2 · round 3: §F 81f0620954 · corrections 522b57e225 · alive part 3 e7bf243872 ([decision] to belam)
       §I red (silent empty body at boot) folded by agi-6f @44619712d9 with its correction (the post-unit check lives in the CALLERS);
       VERIFIED on fp: trunk rc 0 + 10 units · dangling engine rc 2 · dangling posts rc 2 · fixed point empty · verify clean -> ACCEPTED
next   HOLD: belam re-mints config:engine and reports to the owner; wake on the owner's read or a DG3 build line to review
       no Unix user, no sudo before the owner's go
```

## §2 Landed (09-30)
- f16cf993f9 card re-link · round 1: §4 + the 415 B slot · round 2: §C (projector · seed · frontier · V)
- round 3 §F 81f0620954 + 522b57e225 (§F.7 r() hardened · F13 via -L · F16 · frontier 450 B · V 271 / 266) · §I re-check -> fix folded 44619712d9
- scratch: /tmp/g71611/fp (--shared clone; refs trunk / dangle / dangp spike-only), engine2.md (§I v1 bytes)

## 🔴 Where it stops
idle: round 3 is with belam -> the owner; wake on belam's relay or a DG3 build line
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

| `git show REV:<path>` on a SYMLINK returns the link text, not the node | at-REV readers address by mint path; a projection that comes out empty must fail loud |
| a command run inside `while read` eats the loop's stdin | give it `</dev/null` (the frontier lost 9 of 312 goals to this) |
| a stamp I write is read from `date -u`, never recalled | round 3 I wrote 23:1xZ for a 23:05Z commit: check `git log -1 --format=%cI` first |
## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
