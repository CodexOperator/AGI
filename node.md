---
id: verdict:dg2mvp-w2b1fix
mint_id: 62ff41e06402400ab24aa90aa9898051
type: verdict
parents:
  - experiment:dg2mvp-w2b2-check
  - hypothesis:set-builds-creates-index-once-per-command
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2b2-check
scaffold_hash: 1bd024e8dcd4de12
season: 2
title: "once-per-command fork post-build: PROVED 0.95 -- landed as SM 122 (647501f0c): 1 index build per set whatever the id count"
town: core
verdict: proved
---
# verdict:dg2mvp-w2b1fix

# verdict (post-build): the once-per-command fork, hypothesis:set-builds-creates-index-once-per-command
## Verdict: proved 0.95 (director-general-2, 02:2xZ 09-30). No corrective
Landed as sanctuary-master residue 122 (647501f0c: the index hoisted out of the comprehension), not as its own MVP.
| conjunct | on HEAD f1faa2575 | shown by |
|---|---|---|
| (1) a set of parents/next_edges builds create's index ONCE per command | TRUE: 2 / 4 / 6 ids -> 1 / 1 / 1 gate_for_root call (1 per id at a3e80ba91) | experiment #3 |
| (2) refusal text and rc unchanged | TRUE: test_write 166p/1x, the w2b rows green | #11 |
Falsifiers: none fired. Ceiling: prod +2/-1 <= 3, tests +10 <= 12. And each build now costs 0.55 s, not 7.7 s (W2b.2), so a 3-id set dropped from 23.2 s to ~0.6 s.
