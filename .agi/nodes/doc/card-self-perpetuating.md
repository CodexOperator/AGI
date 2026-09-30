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

## §0 State (05:1xZ 09-30 · RESUMED to 11:00Z by the owner; captured for rotation at f=0.405)
| | |
|---|---|
| post | self-perpetuating · CC session agi-53 (ref 21dc2d, session 824fea59) · rotating out at f≈0.41 |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors (owner 02:5xZ): directors bring rulings to the council; alive convenes, ONE ruling per ask |
| messaging | SendMessage by session name ONLY (owner 01:4xZ): no send.py, no rooms, until the bundles land |
| spend | subagents: Opus allowed until ~06:0xZ (owner 05:0xZ "max sub use before reset"), then Sonnet 5.5; workflow.py stays pi-free |
| sessions | belam agi-79 (gen 20) · alive gen 4 agi-e3 · all-is-one agi-8f [242e8c] · DG1 agi-2a · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   B4 goal:g7.16.1.10 minted + true-state fixes · S-remainder leaves corrected · .7 coverage findings to DG5 · rulings
next   DG5: act on /tmp/sp-g717-gaps.md (.7.1.1 regression, .7.1.3 inversion, 6 leaves) -> review what DG5 mints against .7
       alive places g7.16.1.10 (DG1 sketches leaves, builds by g1.31's file-owner map) -> lens on the leaves
then   no OVERVIEW until g7.16.1.1.6 (DG2 proof + census), .6, .7 and bundle 4 close · stop 11:00Z
```

## §2 Landed (09-30)
- goal:g7.16.1.10 (5892d399d, fixes f4a5bd422): merge-up reviews off the Prime; one review per change keyed by git patch-id + base blobs; reuse PROVES coverage (REUSED vs REVIEWED); a persisted round record; rounds polled per commit; one queued launcher (PER x CAP <= 6); unreviewed:budget rows; pi-free until the headless CC route
- S-goal pass: s34 s4 s21 retired in place -> g6.50 · g4.21 · g4.18.5.4 (retire + renumber verbs); s1 -> g1.6.1 (d6f26f856); corrected on an Opus refutation (01a4c74a2): g4.21 = 7 resolvers, g4.18.5.4 = 4 hand renumbers, s1's move was 2 commits
- .7 coverage review -> DG5 agi-5b: regression .7.1.1 (locations.py:740 a second systemd-run builder, 786c1c13a), .7.1.3 7a->7b inversion, 6 leaf sketches .7.1.5-.7.1.7 + .7.2.6-.7.2.8 (/tmp/sp-g717-gaps.md)
- earlier 09-29/30: bundle 2 outcome · g7.16.1.1.6 (proof + census, DG2: .6.1 census, .6.2 home rule) · .7 + .8 rewrites · 4 rulings (keys (C) + witness sha, now in config:key-authority + rotate.py; replace payload NO; W2b body refs = declared regions; residue 154 fail-closed)

## 🔴 Where it stops
05:1xZ 09-30 captured for rotation; the successor's first act is reading SendMessage traffic, then DG5's reply on /tmp/sp-g717-gaps.md
```
python3 extensions/agi/bin/links.py links
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared; verify-suite.lock blocks commits | write.py lands uncommitted under the lock: commit by exact path once it clears (background wait loop) |
| a new file + `git commit -- path` fails | `git add -- <path>` first |
| write.py refuses `set id` (renumber) | git mv + the id line by hand, other fields via write.py, all in ONE commit (a two-commit move leaves two live files per mint_id) |
| shell quoting drops apostrophes | an owner quote keeps its contractions: escape `'"'"'`, never paraphrase a verbatim line |
| stamps | a stamp never post-dates the commit carrying it: check `git log -1 --format=%cI` against `date -u` |
| ack form | non-prime: `rotate.py ack --post <p> --session <sid8> --ref <ref> continue`; a heal-dirty own row: commit heal's write alone first |
| sessions rename after every reboot/rotation | read the posts row's session_name/session_ref; two same names -> `name [ref]` |
| a check narrower than its invariant passes falsely | cite the engine's rule (HOME_PATH_RE), never a hand copy; exclude test fixtures explicitly |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken

## §6 BANKED
(none)
