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

## §0 State (11:0xZ 09-30 · STOPPED at the owner's 11:00Z run end, via belam agi-23)
| | |
|---|---|
| post | self-perpetuating · CC session agi-53 (ref 21dc2d, session 824fea59) · meter 0.43 at stop (line 0.47) |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name ONLY (owner 01:4xZ): no send.py, no rooms, until the bundles land |
| history | the WHOLE history was rewritten 06:3xZ-08:0xZ (scrub): old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map`; every sha on this card is post-scrub |
| sessions | (08:xxZ, from ListAgents windows; re-check at wake) belam agi-23 · alive agi-e3 [761106] @16 · all-is-one agi-8f [242e8c] @1 · SM agi-5c [da1a42] @15 · DG1 agi-8c [9e0227] @21 · DG3 agi-34 @20 · DG4 agi-c8 @18 · DG5 @22 none |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   B4 goal:g7.16.1.10 (placed by alive with SM: DG1 sketches leaves) · .7 coverage findings written by DG1 (6 HORIZON leaves) · S-goal pass · 4 rulings
next   on resume: SendMessage traffic first (never an empty read as proof) · lens on DG1's g7.16.1.10 leaves when they land
then   no OVERVIEW until g7.16.1.1.6 (DG2: .6.1 census, .6.2 home rule), .6, .7 and bundle 4 close
```

## §2 Landed (09-29 -> 09-30, post-scrub shas)
- goal:g7.16.1.10 (f50d5f13c, fixes 11c4b0a41): merge-up reviews off the Prime; one review per change keyed by git patch-id + base blobs; reuse PROVES coverage; persisted round record; rounds polled per commit; one queued launcher (PER x CAP <= 6); unreviewed:budget rows; pi-free until the headless CC route
- .7 coverage (Opus pass): finding 1 WITHDRAWN (locations.py:740 already via mem_cap.scope_argv); DG1 wrote the rest: .7.1.3.2 bullet 2 NOT HELD, leaves .7.1.5-.7 + .7.2.6-.8 HORIZON, .7.2.2 + .7.2.4 falsifiers widened; .7 guard wording = box NAME (e74848a415)
- council 05:2xZ-06:0xZ (successor session, same seat): DG6 g1.31.4.2.2 meter fall-back STANDS (alive, 3 conditions to DG6) · bundle-4 lens: a rotation in a suite window rotates on an uncommitted card -> 4a g4.18.5.5 (DG4, prereq) · 4c g4.18.5.6 (DG5, lensed faithful) · 4b g7.16.1.6.1, all HORIZON
- S-goal pass: s34 s4 s21 retired in place -> g6.50 · g4.21 · g4.18.5.4 (retire + renumber verbs); s1 -> g1.6.1 (29580091b); corrected on an Opus refutation (d923761ca)
- .7 + .8 rewrites · g7.16.1.1.6 (proof + census) · bundle 2 outcome · rulings: keys (C) + witness (in config:key-authority + rotate.py) · replace payload NO · W2b body refs = declared regions · residue 154 fail-closed

## 🔴 Where it stops
11:0xZ 09-30 STOPPED at the owner's run end; idle until belam resumes the council
```
read SendMessage traffic; then: python3 extensions/agi/bin/links.py links
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; verify-suite.lock blocks commits | write.py lands uncommitted under the lock: commit by exact path once it clears (background wait loop) |
| a pre-commit hook refuses owner email / GPU name / pytest-of-<user> / box tokens (post-scrub) | redact and commit again; never --no-verify |
| a sha from memory is wrong after the scrub | map it through the commit-map, or re-read git log |
| a new file + `git commit -- path` fails | `git add -- <path>` first |
| write.py refuses `set id` (renumber) | git mv + the id line by hand, other fields via write.py, ONE commit (two commits = two live files per mint_id) |
| an owner quote keeps its contractions | escape `'"'"'`, never paraphrase a verbatim line; a stamp never post-dates its commit |
| a review of the working tree can race a director's fix | re-check a regression against HEAD before routing it |
| sessions rename after every reboot/rotation; posts rows go stale | trust ListAgents' tmux @window against the row's window cell |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken

## §6 BANKED
- TWO live sessions act as self-perpetuating: agi-53 [21dc2d] (this card, 11:03:24) and the rotation successor seated 05:17:20 (rotate-self, sequence 348) -- the predecessor was never reaped. Options: (a) SM retires one session and re-points the posts row (recommended: keep one, the row decides which) · (b) leave both, idle. Owner/SM call
