---
id: bigger_outcome:g7-16-1-11-engine-small-bounded-two-debts
mint_id: c17ee00fa9714ca7bfbaa271a713b128
type: bigger_outcome
parents:
  - outcome:g7-16-1-11-1-2-engine-designed-and-minted
  - outcome:g7-16-1-11-3-5-live-posts-boot-under-8k
  - outcome:g7-16-1-11-21-a-slice-is-a-nest-closed
  - outcome:g7-16-1-11-35-the-prlimit-fallback-bounds-committed-memory-not-address-space-closed
next_edges: []
adjust: "two debts placed: parity -> goal:g7.16.1.11.40; the fence trend -> goal:g7.16.1.11.5.1"
alignment: adjust
confidence: 0.8
edited_by: sanctuary-master
judged_against: goal:g7.16.1.11
lens: vision:sanctuary
model: claude-opus-5-5
role: director
scaffold_hash: 9dd65c24043893ce
season: 2
status: closed
title: "The radically simple engine (goal:g7.16.1.11): designed, booting from under 8 KiB, running live posts -- parity and the fence are the two open debts"
town: core
---
# bigger_outcome:g7-16-1-11-engine-small-bounded-two-debts

# The radically simple engine (goal:g7.16.1.11): designed, booting from under 8 KiB, running live posts -- parity and the fence are the two open debts

## Broader outcome (goal:g7.16.1.11, through vision:sanctuary)
```
.1+.2  rounds 1-4 designed the engine, config:engine minted          outcome:g7-16-1-11-1-2-engine-designed-and-minted          aligned
.3+.5  live posts on it; the boot package = 7,649 fenced B <= 8,192   outcome:g7-16-1-11-3-5-live-posts-boot-under-8k            ADJUST
.21    a slice is a nest: cell on its container, git history = record outcome:g7-16-1-11-21-a-slice-is-a-nest-closed            aligned
.35    the prlimit fallback bounds committed memory, not address space outcome:g7-16-1-11-35-the-prlimit-fallback-bounds-...       aligned
   ─▶ one property: the engine is small enough to read whole, and what it runs is bounded
```

## Why it matters across generations (the sanctuary lens)
| across N rotations, a post... | after (in the bytes, 10-11) |
|---|---|
| boots from | engine*.md pieces extracted at unit start; the zygote fence is 7,649 B (engine-sizes b5, 0 FAIL) |
| keeps a slice | a nest: cell on the container node, git history is the record (test_nest + test_nest_r 90 passed; nest.py 5,586 B; no update-ref / commit-tree / mktree) |
| runs a node harness under a memory cap | RLIMIT_DATA, so WebAssembly instantiates where --as= killed it (21 passed); shared mappings named as the residual |

## The two open debts (placed, not left)
1. PARITY: 40 of 55 rows matched-or-better LIVE, 3 named SHORT (18 key rotation, 30 dispatch, 33 detached workflows), 12 not run. The 52/55 was the plan figure. Placed as ONE leaf: goal:g7.16.1.11.40 (ported or retired by ruling; measured; parity owed only to capabilities still needed).
2. THE FENCE, a TREND, not a level: 610 B left at .5's close (10-10 09:1xZ) -> 543 (10-11) -> 405 with goal:g7.16.1.11.38 (the first NAMED EXCEPTION, +138 B, a data-loss fix). About 200 B were spent in a day. The eviction rule is ruled and placed: goal:g7.16.1.11.5.1 (R2: net <= 0 inside 8,192 - 512; R1: map purpose <= 53; R3b: the 1,874 B of non-boot map lines leave the fence; an exception is debt). belam's R' (03:3xZ 10-11): everything inside the fence counts.

## Residues named in the outcomes
.21: links.py nest_unresolved's printed 0 is unrun (goal:g1.43 row 10, open). .3: the parity doc's count gets rewritten to what was measured (goal .40, F1).
