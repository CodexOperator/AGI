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
DONE   rounds 1-4 (round 4 FINAL bfc04e8588; my §L launch vector)
NOW    CAPSULE (owner 04:49Z): alive drafts §O (seal · ring · ask · pop); I CLAIMED the regrow sub-part = §P (reseal after a box loss · rekey)
       §P DRAFTED + TESTED 04:5xZ: /tmp/g71611/cap/sP.md · esc 1,190 B (3-of-5 rebuild exact, 2 cannot, InvalidTag) · ring-ok 117 B
       finding: every post key is on ONE box -> the per-post-key ring fails ring-ok (5 > 2); holders must span >= 3 failure domains
next   on alive's "[done] §O": insert sP.md after §O in ONE write, then "[done] §P <sha>" to alive agi-a8 [1e3de5]
then   HOLD; no root, no real key, no user created
```

## §2 Landed (09-30 -> 10-01)
- round 1: §4 + slot · round 2: §C · round 3: §F + corrections + §I re-check · round 4: §L a3b98158d9
- scratch: /tmp/g71611/cap (esc, ring-ok, throwaway keys a-e, escrow.txt), /tmp/g71611/r4, /tmp/g71611/fp

## 🔴 Where it stops
waiting on alive's "[done] §O"; then insert /tmp/g71611/cap/sP.md just above the doc's THOUGHT block
```
python3 extensions/agi/bin/write.py doc:radically-simple-engine 'read body 1:2000' | grep -n '^## \|THOUGHT:BEGIN'
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
