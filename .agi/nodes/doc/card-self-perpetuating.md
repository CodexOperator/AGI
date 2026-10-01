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

## §0 State (07:1xZ 10-01 · f=0.21 · §V delivered, idle)
| | |
|---|---|
| post | self-perpetuating · CC session agi-c9 [a0490b] gen 4 (seated 05:35Z) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 07:1xZ: alive gen 7 = agi-1d [claims §U §X, sends the [decision]] · all-is-one agi-15 (§W) · Prime agi-24 [c42a11] |
| lane | free lane: no subagents, pi-free workflows only; key/identity/rotate BUILD rounds held (design under goal:g7.16.1.11 is open) |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |


## §1 Plan
```
DONE   rounds 1-4 (§F §L) · CAPSULE (§P, P.8 09c38103c) · ROUND 5 §Q b60af0b63 = GO · ROUND 6 lens lines (§S F40, §T matrix + conflict refs)
       DC NIGHT PLAN (owner 06:3x-07:0xZ): §V 983d2475c + esc delta 52ad87a72 -- keys no one can write: fresh key per login, cert for minutes,
         CA = 32-B seed in a capsule + 2-of-2 escrow, armed for a window · CORRECTION: esc <= 64 B · agi-sign v2 04ed82723: the cert fails closed (-O clear + restrict opts) · stand-in arms a TEST CA only (agreed with alive)
NOW    alive (agi-1d) integrates §U-§X and sends the ONE [decision] to belam
next   HOLD: wake on alive / belam / the owner / DG3. Night rulings: after round 6 is built every post files a satisfaction verdict ON THE MORALS
       (figure eight); Phase 3 PREPARED, executed when the owner wakes. At f >= 0.47: card + rotate.py rotate (bare)
```

## 🔴 Where it stops
idle: §V landed. Scratch: /tmp/g71611/v (agi-sign, agi-login, v.md) · tmpfs harness /run/user/<uid>/g71611v (unprivileged sshd on a loopback high port; pid in sshd.pid -- stop it when done) · /tmp/g71611/r5 (round 5, p8)
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| `replace body N:M` refuses to split a paragraph (a table or a list + line is ONE paragraph) | widen N back to the line after the last blank; the doc moves under you: re-read line numbers right before each write |
| MAIN is shared; verify-suite.lock / index.lock block commits | write.py lands uncommitted under the lock: commit by exact path once it clears; wait on .git/index.lock, never delete it |
| a pre-commit hook refuses owner email / GPU name / box tokens | redact and commit again; never --no-verify |
| a sha from memory is wrong after the scrub | map it through the commit-map, or re-read git log |
| `git show REV:<path>` on a SYMLINK returns the link text | at-REV readers address by mint path; a projection that comes out empty must fail loud |
| a command inside `while read` eats the loop's stdin | give it `</dev/null` |
| systemd 255 empties `${x}` even inside `sh -c '...'` in a unit | bare `$x` only in unit command lines (measured 05:4xZ) |
| `git worktree add` of the full repo at load > 50 hangs past 120 s | test extraction on a copy of `.geometry` only |
| `printenv ${X:-_}` with X unset prints `$_` | guard with `[ "$X" ]&&` first |
| rotate's stop_commit flattens the quorum card link | `ln -sfn ../../nodes/doc/card-<post>.md`, commit by exact path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
- (answered 05:45Z, removed: ring holders + phone holder -> iPhone-only custody, P.8)
