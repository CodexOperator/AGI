---
id: verdict:dg2-c1
mint_id: bc74b520a94b4f8fbd566c436d0c5954
type: verdict
parents:
  - experiment:dg2-c1-harvest
  - hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-c1-harvest
scaffold_hash: 0d98fdd6dfbd4dc7
season: 2
title: "DG2.C1 (6d8ac01d74): inconclusive_lean_proved:85 -- orphan tree refused once by name, never archived, never re-tried; live reaper-log proof waits on heal's watch restart"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-c1

## Verdict: inconclusive_lean_proved:85
The corrective's order holds on the bytes: an orphan tree (gitdir gone, no HEAD) is refused once by name, never logged 'archived', never re-tried in-process; red on the base, green on the tip; SM's dry sweep on MAIN's data shows the one changed line. Not proved until the live reaper log carries the refusal after heal's watch process restarts (it imported the old heal.py). Bytes are not pinned by the fix (refusal only; SM's off-repo pin stands); the memo is in-process, so a heal restart logs the refusal once more.
