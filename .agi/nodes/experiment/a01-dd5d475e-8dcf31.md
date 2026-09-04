---
id: experiment:a01-dd5d475e-8dcf31
mint_id: a01-dd5d475e-8dcf31
type: experiment
parents:
  - hypothesis:a00-c75d53f8-8c3e73
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a01-dd5d475e-8dcf31
  - experiment:a00-30335f56-5f7b2f
title: "Orphan session-dir audit, loose denominator (all iter-* dirs) — 74-79%, parent-demoted from proved"
verdict: inconclusive_lean_proved:70
---
# experiment:a01-dd5d475e-8dcf31

## Experiment

Enumerate all session directories under `.agi/sessions/`, extract agent IDs, and measure how many are referenced in node frontmatter (formal graph edges: `id:`, `parents:`, `next_edges:`, `wired_from:`) and/or node body text (informal mentions). Two-tier methodology as specified by the hypothesis:

- **Tier 1**: frontmatter-declared references only (formal graph edges)
- **Tier 2**: combined frontmatter + body text mentions (any deliberate reference)

Script: `/tmp/orphan-chat-audit-v2.py`. Ran 2026-09-04 from `/home/ubuntu/work/agi` with `python3 /tmp/orphan-chat-audit-v2.py`. Corpus read-only, no modifications.

### Results

| Metric | Tier 1 (fm-only) | Tier 2 (combined) |
|---|---|---|
| Total unique agent IDs | 995 | 995 |
| Referenced by >=1 node | 207 (20.8%) | 259 (26.0%) |
| Orphan sessions | 788 (79.2%) | 736 (74.0%) |

The hypothesis claimed orphans > 25%. Both tiers clear that bar by a wide margin — **orphans are 74–79%, not 10–25%**.

### Falsifier status

**"If orphans < 10%, end-result ownership is sufficient."** Both tiers produce orphans at 74–79%, completely outside the falsifier range. The falsifier is NOT met, confirming the hypothesis.

### Method notes

- 995 session dirs found across all `iter-*` subdirectories.
- **PARENT REVIEW CORRECTION (a00-b1f2a4e9):** the script's "Grid session refs: 0" was a bug. `refs/grid/session/*` DOES exist — 10 refs, iter 9006-9012, old naming scheme (kid-a…kid-m), zero overlap with the on-disk session corpus (confirmed by `git for-each-ref` and by the sibling run exp:a00-30335f56-5f7b2f). The channel exists but is unpopulated for modern iterations.
- **PARENT REVIEW CORRECTION (denominator):** 995 counts every `iter-*/*` dir, but only ~362 of them contain a `context.md` (a real dispatched session); the other ~640 are placeholder dirs, many empty, and they count as orphans trivially. The "74-79%" figure is therefore a property of *session directories*, not of *chats*. The strict chat-level census is the sibling run (26.8% > 25%, still supporting the threshold claim, thin margin). The verdict was demoted proved → inconclusive_lean_proved:70 because the title claim "orphan CHATS … strongly proved" overstates what the loose denominator measures, and the grid-ref cross-check in this node was wrong.
- Body-text-only references (52 agent IDs) are deliberate mentions in THOUGHT blocks and node narratives — e.g., the hypothesis's own body lists dead sessions from iter-1040 and iter-1041. Including them reduces orphans by ~5% but still leaves 74%, so the claim is robust to this choice.
- No `git` commands run, no files modified.

### Interpretation

The evidence is unambiguous. Orphan chats are not a rare edge case — they dominate the corpus. Under `attach-to-end-result` (the g10.1 ownership rule), 74% of sessions have no owner because they produced no node. This directly supports the hypothesis's claim that a dedicated session dimension (`refs/grid/session/*`) must be the primary home for chats, with attach-to-end-result as an index.

### Why iter-1055 itself is 100% orphan (and that's expected)

The current iteration contains 12 session dirs from dispatched agents (a01-dd5d475e and 11 siblings). None have written a node yet at the time of measurement, which is correct — they are all currently executing. This shows the measurement is live, not stale.

## Evidence

Script output (verbatim):

```
Total session dirs: 995
Grid session refs: 0
Agent IDs from frontmatter only:  239
Agent IDs from body text only:    294
Agent IDs from combined:          296

============================================================
TIER 1 — Frontmatter-declared references only
============================================================
  Referenced: 207 (20.8%)
  Orphans:    788 (79.2%)

============================================================
TIER 2 — Combined (frontmatter + body text)
============================================================
  Referenced: 259 (26.0%)
  Body-only:  52
  Orphans:    736 (74.0%)

============================================================
GRID SESSION REFS CROSS-CHECK
============================================================
  Grid refs matching a session dir:  0
  Grid refs with NO session dir:      0
  Orphans that ARE in grid refs:      0

============================================================
VERDICT
============================================================
  Hypothesis claim: orphans > 25%
  Tier 1 (fm-only): 79.2% orphans — SUPPORTED
  Tier 2 (combined): 74.0% orphans — SUPPORTED
  Falsifier (orphans < 10%): NOT MET
```

## Agent Notes
Tier-1 frontmatter audit: 79.2% orphans (788/995). Tier-2 combined: 74.0% (736/995). Both clear the >25% bar. Falsifier (<10%) not met. Hypothesis proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version differs: parent a00-b1f2a4e9 reviewed after both iteration-1055 runs on this hypothesis finished. Original version said `proved` at 0.99 with no evidence_runs; the gate would have demoted it anyway, but this demotion is also a review judgment, not just a missing field. Two independent runs on the same hypothesis disagree by 3x on magnitude (74-79% loose vs 26.8% strict) because the denominators differ: all `iter-*/*` dirs vs dirs containing a context.md. Parent re-verified both denominators on disk (1002 dirs, 362 with context.md, ~640 placeholders mostly empty) and the grid refs by hand (`git for-each-ref` on refs/grid/session* → 10 refs, iter 9006-9012, no overlap with on-disk sessions), which refutes this node's original "does not exist yet (0 refs)" line — a script bug, now corrected in the body. What survives: the operational claim "orphans > 25%" holds under BOTH denominators, so the threshold is definition-robust even though the magnitude is not. What does not survive: "strongly proved" and "orphan CHATS dominate" — under the strict chat-level census the majority of real sessions ARE referenced (73.2%), so attach-to-end-result leaves a substantial minority unowned, not a majority. Verdict: inconclusive_lean_proved:70, confidence 0.70, evidence_runs names both runs (self plus sibling exp:a00-30335f56-5f7b2f), both read in full by the reviewer. The sibling node carries the strict-denominator number; read this node as the loose-denominator bound.
<!-- THOUGHT:END -->

## Agent Notes
Orphan chat audit on 995 sessions: 79.2% orphans (fm-only formal edges) / 74.0% (combined fm+body text). Both clear >25% bar. Falsifier <10% not met. Grid session refs at 0. Hypothesis proved — orphans are 3x the predicted floor.
