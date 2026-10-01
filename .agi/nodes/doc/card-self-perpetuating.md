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

## §0 State (06:0xZ 10-01 · f=0.19 · ROUND 5 delivered, idle)
| | |
|---|---|
| post | self-perpetuating · CC session agi-c9 [a0490b] gen 4 (seated 05:35Z) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name (owner 01:4xZ); READING the send.py inbox is allowed |
| history | the whole history was rewritten 06:3xZ-08:0xZ 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| sessions | 06:0xZ 10-01: alive agi-a8 [1e3de5] · all-is-one agi-15 [c6276e] (rotating) · Prime agi-24 [c42a11] · use "name [ref]" after rotations |
| lane | free lane: no subagents, pi-free workflows only; key/identity/rotate BUILD rounds held (design under goal:g7.16.1.11 is open) |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
DONE   rounds 1-4 (my §F §L) · CAPSULE (alive §O + my §P) · card re-linked c5e219e07
       ROUND 5: §Q ZYGOTE b60af0b63 = GO (owner 06:1xZ) · config:engine 7,342 B · engine-post 7,671 · engine-wrap 3,817 (+ agi-infer 549 B)
       CUSTODY: P.8 09c38103c -- escrow 2-of-2 (iPhone, E), E.key k-of-n over posts; esc +363 B (P-256 holder)
NOW    ROUND 6 REVISED (owner 06:2xZ, @57bdb465a): ONE script + ONE expansion MATRIX, 4 paths; alive CLAIMED §T. My lens lines sent:
       matrix = ### matrix in config:engine, ~~~ TSV (target node verb), row 1 populates itself · conflict = refs/conflicts/<box>/<hash>, create-only; inbox only notifies · seed state = refs/seed/<box>
       earlier (§S):
       F40 regrow from an EMPTY dir (blobless depth-1 fetch 483 KB + 57 KB lazy; bad hash refused; no allowFilter = silent 76 MB) · gate NOT in the seed
next   if alive rotates before §T lands, §T is MINE (alive's card names where it stopped). Else HOLD. At f >= 0.47: card + rotate.py rotate
```

## 🔴 Where it stops
idle: alive writes §T. Scratch: /tmp/g71611/r5 (v5 drafts, clone = scratch repo with allowFilter + allowAnySHA1InWant, empty2 = the blobless seed test)
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
