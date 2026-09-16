---
id: hypothesis:l4-the-stale-base-gate-runs-its-own-sync-when-no-engine-file-differs-and-never-refuses-on-files-empty
mint_id: 75348efb180a4795b75b5595fd8ca217
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 2df42b914014a02e
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (SM lane, 11:51Z) and verified on MAIN 28acb3459: dispatch.py:2206 refuses every stale base (status behind) regardless of `files`; sanctuary-director gen 26 paid 3 dispatch attempts, refusal 2 read {issue: stale-base, behind: 6, files: []} AFTER the post had merged and pushed -- files=[] means no engine file differs, yet the post paid merge+push+dispatch again. The record already enumerates actions [{id: sync, cmd: git merge origin/<integration>}] (dispatch.py:541) and only EMITS. CLAIM: (1) a stale base with files=[] (behind by non-engine commits only) never refuses: the gate records behind N + files=[] in the branch_ref and proceeds; (2) a stale base WITH differing engine files refuses as today unless --sync is passed, in which case dispatch runs the recorded sync action itself (git merge origin/<integration>, ff or clean merge only), re-measures, and proceeds when the re-measure is current or files=[]; a merge that conflicts aborts (git merge --abort, MERGE_HEAD proved absent) and refuses by name; (3) --allow-stale-base keeps its meaning. FALSIFIERS: any refusal whose record carries files=[]; a --sync run that leaves MERGE_HEAD behind or proceeds on a conflicted tree; a sync that runs without --sync when files is non-empty. TESTS (<=5, fixture repos with a bare origin, no live dispatch): behind+files=[] proceeds and records; behind+files non-empty refuses without --sync; --sync ff-merges and proceeds; --sync on a conflict aborts, proves no MERGE_HEAD, refuses by name; --allow-stale-base unchanged. FILE SCOPE: dispatch.py (_stale_base_spawn callers at ~2203-2236, the new --sync flag), the dispatch tests. CEILING: <=40 production lines, 1 kid -- re-brief SM past 2x."
title: L4 the stale base gate runs its own sync when no engine file differs and never refuses on files empty
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-stale-base-gate-runs-its-own-sync-when-no-engine-file-differs-and-never-refuses-on-files-empty

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: dispatch.py:2214-2221 returns 3 on every `behind` unless --allow-stale-base, with no files-empty branch and no --sync flag (MEASURED grep -c '"--sync"' = 0); latest dispatch.py commit 138138120 (TM.11) is credential handling, unrelated. Overlaps the round-less sibling hypothesis:l4-dispatch-performs-the-stale-base-sync-itself-when-the-merge-is-clean-instead-of-returning-the-merge-as-text (INFERRED same --sync half). EVIDENCE: extensions/agi/bin/dispatch.py:2211-2221; 138138120 Never rounded at close (owner 14:1xZ).
