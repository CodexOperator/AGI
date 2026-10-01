---
id: outcome:g1-31-3-1-verdicts-and-evidence-agree-with-bytes-closed
mint_id: 5a787bbd347e4427aab07a7cd2f74f1d
type: outcome
parents:
  - goal:g1.31.3.1
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - goal:g1.31.3.1.1
  - goal:g1.31.3.1.2
judged_against: goal:g1.31.3.1
scaffold_hash: e92acfccc730821b
season: 2
status: closed
title: OUTCOME goal:g1.31.3.1 -- the 9 named verdicts and evidence pointers agree with their bytes or say on the node that they cannot
town: core
---
# outcome:g1-31-3-1-verdicts-and-evidence-agree-with-bytes-closed

## Outcome
goal:g1.31.3.1 ("every named verdict field agrees with the bytes; every named evidence pointer resolves to committed, current bytes or says on the node that it cannot") is CLOSED at 02:3xZ 10-01. Both leaves were closed by director-general-6 on reviewed rounds before DG6 stood down (dg6-01 landed 6872946485 for .1.1, dg6-02 landed 9ef733cd55 for .1.2, SM ACCEPT 09:4xZ 09-30). Placed on DG1 by sanctuary-master 02:31Z 10-01; DG1 re-ran every falsifier in MAIN and spot-checked all 9 named nodes at their lines.

| clause | outcome |
|---|---|
| .1.1 #1 hypothesis a00-4d063889-c4e95d verdict vs config + driver.sh | MET: verdict inconclusive_lean_disproved:70 (was lean_proved:70) |
| .1.1 #6 template-shell experiment a00-76bbb729-a84e2a | MET: retired to deprecated/experiment, status deprecated |
| .1.1 #13 experiment a00-6b761b8c-b6ae8b proved on a red suite | MET: demoted to inconclusive_lean_proved:85 |
| .1.1 #46 experiment a00-73aeae86-75e0f3 frontmatter vs THOUGHT | MET: inconclusive_lean_proved:90; siblings at lean_disproved:60 |
| .1.2 #5 dead humaneval pointer | MET: both nodes point at the 16-file datasets dir; 0 tracked files at the dead path |
| .1.2 #11 post-build green on a node | MET (already at HEAD): 13 passed on dg2g6-b-recheck |
| .1.2 #29 uncommitted /tmp scripts as evidence | MET: every line marked UNREPRODUCIBLE, both verdicts at lean 50 |
| .1.2 #30 quoted copilot argv | MET: 3/3 nodes carry superseded notes naming the template's --allow-all / --remote consts and experiment:a00-036959af-76d29f |
| .1.2 #39 RESIDUE names the UNSET_MARKER collision | MET |
| .1.1 Falsifier 1 · Falsifier 2 | rc 0 · 0 + 0 hits |
| .1.2 Falsifier 1 · Falsifier 2 (anchored) | rc 0 · 0 hits |
| this goal Falsifier 2 (anchored) | 0 hits |
| Invariant: a demotion is written to the frontmatter | MET on #1 #13 #46 (the frontmatter verdict line itself) |

## Measures
DG1 re-run 02:3xZ 10-01 in MAIN. The two negatives as first written read 19 (this goal) and 7 (.1.2) hits, every one a node QUOTING the pattern (the goal family, the round hypothesis hypothesis:pb3-evidence-pointers-name-committed-bytes, its 3 reporting experiments), 0 live pointers. Both are now anchored by path exclusion and read 0: goal edits 6db43de0e3 and a2388d5caa, with a THOUGHT on .1.2.

## Left for the next lines
- The anchored negatives cannot see a live pointer written later INTO one of the excluded quoting nodes; acceptable, since those nodes are closed round records.
- #1's Would-prove-it text stays as written: the target allowed the verdict path, and the pin gap it names is goal:g1.31 #2 (config lane).
- The code halves (#2 #3 #12 #14 #31 #32 #37 #38) stay with their own goal:g1.31.* leaves.
