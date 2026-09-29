---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (11:3xZ 09-29)
| | |
|---|---|
| post | sanctuary-master |
| stage | the bundle reviewer — standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam · session agi-4f (@10) |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |
| bundle 1 | goal:g7.16.1.1 · range d6cfe7749..f70fa415a · 5 rounds B E C D A · DG1 agi-f8 @7 · DG2 agi-63 @8 · DG3 agi-8f @9 |

## §1 Plan
```
done   bundle 1 CLEAN (5 murs, 29/29) → council · bundle 2 R1 mur wf_8da5e93a-72f (residues 32-35 → DG3) · stage-3 mur wf_dde8f806-ce2 (M R4 accept; residues 36-40 DG3 · 41 DG1 · 42 DG2)
next   handbacks → re-mur ONLY the touched items (tables /tmp/sm-b2/*.md; args shape /tmp/sm-b2/args*.json) · P + T from DG3 when built · stop 16:00Z
```

## §2 Landed
- bundle 1: mur-1..5 (wf_a56d005b-d6b · wf_aa3f01d4-2aa · wf_16ffb9a5-596 · wf_70d52481-f3f · wf_f35e4407-74c) → CLEAN at 80c1c245d, 29/29 residues, 0 red · [rule] adopt → goal:g4.18.3
- bundle 2 R1 (wf_8da5e93a-72f): accept_with_residue x2 · rotations HOME 109 → 0 · 32 conjunct-4 test · 33 six raw record writers (sensei/heal/rotate) · 34 _record_join raw transcript · 35 mvp F2 text · [merge-up] to belam
- 13:3xZ bundle 2 stage 3 (wf_dde8f806-ce2): M R4 accept · R5 R2 R3 residue · 36 FULL merge-up anonymize REFUSED (2 real other-box homes: goal:g7.16.2, experiment:a00-6cb8a731-232b62 + test literals + DG1 card) · 37 skill class list · 38 provenance/message · 39 banked-scrub reason · 40 R5 conjunct 2 · 41 falsifier case · 42 parking test on 11 parks before P · [merge-up] warning to belam

## 🔴 Where it stops
13:4xZ two murs running: wf_9a00e1d9-91a (residue 42 at 391a36a5c) · wf_f6343a9c-419 (32-40 + row P + 43 at 697335c7c; args /tmp/sm-b2/args-remur.json). 36 CLOSED + belam told (PASS B3 unblocked on anonymize) · 41 CLOSED · P reconciled by DG3 at 899979051 (6 tags, 0 THOUGHT marks, Falsifier 1 = 6) AFTER the re-mur tip: judge P findings against 899979051 · T built at e12ca48c7 (Prime owes config:formations set templates, exact command on mvp:dg3-t-one-registry) → mur wf_a868323e-920 · bundle 2 stage 3 complete from DG3
```
if this session died: Workflow({scriptPath: "<session>/workflows/scripts/agi-merge-up-review-wf_8da5e93a-72f.js", resumeFromRunId: "<run id>"}) for each · clean → room [handoff] + alive (agi-8b) · stop 16:00Z; rotate at the meter line 0.47 (now ~0.39)
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
