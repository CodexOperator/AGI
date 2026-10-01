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

## §0 State (05:4xZ 10-01 · f=0.07 · ROUND 5 working)
| | |
|---|---|
| post | self-perpetuating · CC session agi-5b gen 4 (seated 05:35Z) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 05:0xZ 10-01: alive agi-a8 [1e3de5] · all-is-one agi-15 [c6276e] · Prime agi-24 · names collide after rotations: use "name [ref]" |
| lane | free lane: no subagents, pi-free workflows only; key/identity/rotate BUILD rounds held (design under goal:g7.16.1.11 is open) |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
DONE   rounds 1-4 (my §F §L) · CAPSULE closed (alive §O + my §P, [decision] @59cbe58c6) · card re-linked c5e219e07
NOW    ROUND 5 (owner 05:38Z, goal:g7.16.1.11 @439467eb5): config:engine BOOTSTRAP <= 8,192 B; expansions may be larger; cap 20,480 B
       my lens = the ZYGOTE: the bootstrap holds only what expands; every v4c piece mapped bootstrap | expansion | gone; parity rows unchanged
       work in /tmp/g71611/r5 (v4c copy, split drafts, byte counts, projection diff v4c vs v5 on a scratch clone)
next   doc section §Q in doc:radically-simple-engine -> SendMessage alive + all-is-one -> alive convenes the ONE [decision] to belam
```

## 🔴 Where it stops
drafting the split in /tmp/g71611/r5; nothing written to the doc yet. Resume: re-read belam--self-perpetuating (05:39Z) + goal body "ROUND 5", then measure
```
cat /data/work/agi/.agi/nodes/.geometry/engine.md | wc -c
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
| the captive rotation chain can fail (05:3xZ 10-01: rotate-self rc=3, and no capture-chain.log was found under .agi/sessions) | rotate yourself: card current, then the bare rotate.py rotate |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
- CAPSULE ring holders (doc §P.2): every post key lives on ONE box, so a per-post-key ring fails the spread rule (per box <= min(K-1, N-K)). Options: (a) the owner's device(s) + posts on 2 other boxes, (b) hardware keys, (c) a different K-of-N. Recommendation: 3-of-5 with 2 here, 2 on another town box, 1 owner device. Owner's call
- CAPSULE phone holder (doc §P + the passkey route): the iPhone's escrow share must be opened ON the phone (iOS CryptoKit Curve25519 + ChaChaPoly = esc's construction) -> a tiny app on the owner's dev plan, or the phone is a signer only and a third box holds that share. Recommendation: the tiny app. Owner's call
