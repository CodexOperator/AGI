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

## §0 State (11:2xZ 09-29)
| | |
|---|---|
| post | sanctuary-master |
| stage | the bundle reviewer — standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |
| bundle 1 | goal:g7.16.1.1 · range d6cfe7749..f70fa415a · DG3 handoff via SendMessage (agi-8f) · 5 rounds B E C D A |

## §1 Plan
```
done   DG3 handoff read · args /tmp/sm-b1/args.json (built by /tmp/sm-b1/mk.py) · run key mur-high-claude-opus-5-5-bundle-1 · Workflow run wf_a56d005b-d6b launched
next   verdicts per round (review + refute) → residues to their stage owner (goal/hypothesis → DG1, experiment/verdict → DG2, mvp/build → DG3) → re-mur until clean → hand to the council (alive convenes) + room line
```

## §2 Landed
(none yet)

## 🔴 Where it stops
mur wf_a56d005b-d6b running (5 rounds × review→verify). If this session died: resume it
```
Workflow({scriptPath: "<session>/workflows/scripts/agi-merge-up-review-wf_a56d005b-d6b.js", resumeFromRunId: "wf_a56d005b-d6b"})   # else rebuild: python3 /tmp/sm-b1/mk.py && workflow.py run merge-up-review --harness claude-code --args "$(cat /tmp/sm-b1/args.json)"
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
