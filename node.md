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

## §0 State (04:4xZ 09-30 · STOPPED at the owner's 04:00Z council stop, via belam agi-79)
| | |
|---|---|
| post | self-perpetuating · CC session agi-53 (ref 21dc2d, session 824fea59; heal resumed after the 01:55Z reboot) · meter 0.34 at stop |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ 09-30): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name ONLY (owner 01:4xZ): no send.py, no rooms, until the bundles land |
| sessions | belam agi-79 (gen 20) · alive gen 4 agi-e3 · all-is-one agi-8f [242e8c] · DG1 agi-2a · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 closed + SM bigger_outcome reviewed · owner goal rewrites (.7 .8 mine) · S-goal pass (s34 s4 s21 s1 mine) · 4 rulings
next   on resume: SendMessage inbox (never an empty read as proof) · DG5 g7.16.1.7.1.4 keys follow-through · DG2 g7.16.1.1.6 proof leaf result
then   no OVERVIEW until g7.16.1.1.6, .6, .7 and bundle 4 close
```

## §2 Landed (this session)
- bundle 2 outcome:council-bundle-2 (adc228107) -> DG1 adopted; F g7.16.1.2.9 moved unbuilt to g7.16.1.7
- SM bigger_outcome bundles 1-3: aligned 0.8 · minted goal:g7.16.1.1.6 (bundle-1 verdicts -> proved + one-source census in verify) -> DG2
- owner goal rewrites: g7.16.1.7 + .8 (04f08de89) · .7 -> nested pane g7.16.1.7.3 (d6536c856) · lens lines on .6 (4 gen-1000 clauses) · g7.32.6 (a read never wakes) · .5 (one liveness census) · g4.18.5 (rows by name)
- S-goal pass: s34 s4 s21 retired IN PLACE -> g6.50 · g4.21 · g4.18.5.4 (retire + renumber verbs, any type); s1 -> g1.6.1 (d6f26f856, ac2fca463); prose provenance NOT rewritten (house rule)
- rulings (alive consolidated): DG5 keys (C) own-box remint + witness sha + key-template row · DG3 replace payload NO (names replace body) · DG1 W2b (b) + body refs = declared regions, never prose · DG3 residue 154 fail-closed

## 🔴 Where it stops
04:4xZ 09-30 STOPPED at the owner's 04:00Z council stop; idle until belam resumes the council
```
read SendMessage traffic on resume; then: python3 extensions/agi/bin/links.py links
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; verify-suite.lock blocks commits | write.py lands uncommitted under the lock: commit by exact path once it clears (background wait loop) |
| a new file + `git commit -- path` fails | `git add -- <path>` first |
| write.py refuses `set id` (renumber) | git mv + the id line by hand, every other field via write.py; THOUGHT records it (g4.18.5.4 will make it a verb) |
| ack form changed | non-prime: `rotate.py ack --post <p> --session <sid8> --ref <ref> continue`; a heal-dirty own row: commit heal's write alone first |
| sessions rename after every reboot/rotation | a posts row's session_name/session_ref; two same names -> `name [ref]` |
| Claude usage OUT (owner 03:2xZ) | NO Opus subagents: agentic subtasks on pi (workflow.py --harness pi-free) or Sonnet 5.5 at most |
| a check narrower than its invariant passes falsely | cite the engine's rule (HOME_PATH_RE), never a hand regex copy |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken

## §6 BANKED
(none)
