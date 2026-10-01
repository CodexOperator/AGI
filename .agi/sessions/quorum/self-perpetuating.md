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

## §0 State (05:0xZ 10-01 · f=0.40 · idle)
| Field | Value |
|---|---|
| Rotation record | gen n/a, window @36, pid 2899273, model_confirm ok. |
| Node counts | active n/a, deprecated n/a. |
| Tree | branch local-maxxing/season2/main, behind season2/main 0, unpushed 22. |
| Meter | 0.399881 · role director · model claude-opus-5-5. |
| Account | total=$192.00 used=$191.39 remaining=$0.61 |
## §1 Plan
```
DONE   rounds 1-4 (round 4 FINAL bfc04e8588; my §L) · CAPSULE: alive §O 0f1ec1fc6 · my §P 7dbb033ed + THOUGHT 7ebb6c384
       (escrow Shamir + X25519 shares, esc 1,190 B tested · ring-ok 117 B · rekey = a pop into a rotate route · refs/capsule by kernel ownership)
NOW    CAPSULE CLOSED: alive sent the [decision] to belam @59cbe58c6 (§O + my §P P.1-P.7 + O.5 passkey route with my 4 amendments)
next   HOLD: belam -> the owner; wake on the owner's read or a DG3 build line. At f >= 0.47: card + rotate.py rotate (bare)
```

## §2 Landed (09-30 -> 10-01)
- round 1: §4 + slot · round 2: §C · round 3: §F + corrections + §I re-check · round 4: §L a3b98158d9 · capsule §P 7dbb033ed
- scratch: /tmp/g71611/cap (esc, ring-ok, throwaway keys a-e), /tmp/g71611/r4, /tmp/g71611/fp

## 🔴 Where it stops
idle: the capsule is with belam -> the owner; wake on belam's relay or a DG3 build line
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
auto-captured at f=0.3999 at the captive ratio 0.85 x the line, no self-rotate
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
- CAPSULE ring holders (doc §P.2): every post key lives on ONE box, so a per-post-key ring fails the spread rule (per box <= min(K-1, N-K)). Options: (a) the owner's device(s) + posts on 2 other boxes, (b) hardware keys, (c) a different K-of-N. Recommendation: 3-of-5 with 2 here, 2 on another town box, 1 owner device. Owner's call
- CAPSULE phone holder (doc §P + the passkey route): the iPhone's escrow share must be opened ON the phone (iOS CryptoKit Curve25519 + ChaChaPoly = esc's construction) -> a tiny app on the owner's dev plan, or the phone is a signer only and a third box holds that share. Recommendation: the tiny app. Owner's call
