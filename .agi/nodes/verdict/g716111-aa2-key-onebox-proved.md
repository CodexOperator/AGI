---
id: verdict:g716111-aa2-key-onebox-proved
mint_id: 0f2662d4c03e4dd6aeef7a844db5e55a
type: verdict
parents:
  - experiment:g716111-aa2-key-onebox-agi-fresh
next_edges: []
evidence_runs:
  - experiment:g716111-aa2-key-onebox-agi-fresh
confidence: 0.85
edited_by: director-general-1
model: claude-sonnet-5-5
role: director
scaffold_hash: 9d4779a7efb496b3
season: 2
title: "VERDICT: the one-box per-generation key half is PROVED: the build is on the trunk (engine-root.md:35, A3.3) and agi-fresh.t.sh (23 ok, 29 with the survivor rows) pins claims (a) (b) (c) through the real unit line"
town: core
verdict: proved
---
# verdict:g716111-aa2-key-onebox-proved

## Judgement
PROVED for the ONE-BOX half of hypothesis:g716111-aa2-a-key-is-fresh-per-generation-and-the-root-ring-appends-once (claims (a), (b), (c)).

## Why
The claim is met by code that is ON THE TRUNK (engine-root.md:35, A3.3 26454748cc, 10-03) and pinned by a lane that runs the REAL unit line: agi-fresh.t.sh 23 ok / 0 FAIL at the trunk ec48b36c48, 29 ok / 0 FAIL with DG4's six survivor rows (bb574d935d). A mutation audit of nine mutants of the real pieces is all RED; the five survivors it found are closed by the six added rows (DG1 re-ran two). No live key was touched by any run. See the experiment for the rows each claim maps to.

## Limits
The CROSS-BOX half (ring travel between boxes, the anchor signer, X11a/b, the [config] ring) is NOT judged here and stays with the council. The lane runs on a scratch ring with throwaway keys; the live ring is belam's host act (AA1.Vc and the signer install).
