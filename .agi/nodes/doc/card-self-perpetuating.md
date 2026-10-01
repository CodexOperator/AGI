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

## §0 State (13:5xZ 10-01 · f=0.31 · WIND-DOWN, idle until the owner's morning)
| | |
|---|---|
| post | self-perpetuating · CC session agi-99 [b77b3e] (heal-resumed 15:0xZ, same session 06312a1a; seated 05:35Z) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 07:3xZ: alive gen 7 = agi-1d (convenes, sends the [decision]) · all-is-one = agi-f0 · Prime agi-24 [c42a11] |
| lane | free lane: no subagents, pi-free workflows only; key/identity/rotate BUILD rounds held (design under goal:g7.16.1.11 is open) |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |


## §1 Plan
```
DONE   rounds 1-4 (§F §L) · CAPSULE (§P, P.8) · ROUND 5 §Q = GO · ROUND 6 lens lines (§S, §T)
       DC: §V 983d2475c + esc delta + agi-sign v2 04ed82723 (cert fails closed; stand-in arms a TEST CA only)
       ROUND 7: Y2 2536d7ff3 -> b251aa4a4 (aliases) -> a280bdfba (anchor fix + check) -> c7532c191 (grow-gate line format); agi-fill 5,068 B
WIND   belam 13:5xZ: wind-down at 14:00Z. MORAL SATISFACTION VERDICT on the seed engine: WAITS for the owner's morning (round 6 not live;
       doc:g716111-round6-build unchanged since 07:42Z) -- same call as alive
next   at the owner's morning: read the round-6 build state, then file ONE verdict line to belam on the morals (vision:self-perpetuating lens:
       does the body regrow from the seed with nothing lost?). At f >= 0.47: card + rotate.py rotate (bare)
```

## 🔴 Where it stops
idle (wind-down). Nothing live, no unit, no scratch server (sshd + CA agents stopped). Scratch kept: /tmp/g71611/{r5,v,y2}
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
| heal's RESUMED-SEAT line prints `ack --seat X --gen N`: refused on a non-prime post | run `rotate.py ack --post <p> --session <8-hex> --ref <ref> continue` |\n| rotate's stop_commit flattens the quorum card link | `ln -sfn ../../nodes/doc/card-<post>.md`, commit by exact path |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5555 resolved, 22:1xZ)

## §6 BANKED
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go (doc §4 Migration)
- (answered 05:45Z, removed: ring holders + phone holder -> iPhone-only custody, P.8)
