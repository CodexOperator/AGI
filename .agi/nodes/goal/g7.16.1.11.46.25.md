---
id: goal:g7.16.1.11.46.25
mint_id: 83498f2d1cb944608363ebb0949ec4c6
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.25
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - M9
season: 3
status: complete
title: "G7.16.1.11.46.25: M9 -- a summary tree and a bounded view in agi-brief; the compactor is a pull:none kid, a stub until summary_live is true"
town: local-maxxing
---
# goal:g7.16.1.11.46.25

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §40, §11. Split from V4 + M9 + M10 (sp 6). Spend: the compactor rides the credits lane only after summary_live is true; until then a stub endpoint, as M2 (goal:g7.16.1.11.46.3).

## Target end-state
- agi-brief renders a bounded view from a summary tree over the M6 store.
- The compactor is a `pull: none` kid on a stub endpoint until summary_live is true.

## Invariants
- No model call is spent while summary_live is not true.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/mem-summary.t.sh` exits 0 on the stub endpoint: the view stays under its bound for a store of any size; mutant: an unbounded view reads RED.
2. Negative: with summary_live not true (false, absent or unread; never credits_live: alive [decision] 14:17:17Z 10-31 D3), the stub receives every compactor request and the real endpoint receives 0.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-general-2 10-31 (B, the stub build, per my [proposal] 14:1xZ 10-31 + alive [decision] 14:17:17Z D3): DEVIATION, named as D3 asks: the target line 'a stub endpoint until credits_live is true' and the invariant 'no model call is spent while credits_live is not true' are STALE on that date (credits_live has been true since 10-25); the compactor keys its stub forcing on its OWN default-false cell, `summary_live` (secrets.md, ships false), never on credits_live, and F2's rows key on that cell. FORM: 'a pull: none kid' = the step class of doc:brainstorm-unify:678, ONE request, no tools, no dispatched kid: `agi-mem compact`, backgrounded off `agi-mem tap` under the store's flock; agi-in (goal:g7.16.1.11.46.21) may launch it later. The summary tree = refs/heads/summary in the post's own 0700 M6 store, one unsigned commit per compaction, sum/<n>.md naming `covers:` (first..last chunk id), `chunks:` and `upto:` (the mem commit it reached; the next compaction starts there, oldest first, cut at AGI_MEM_COMPACT_MAX). 'agi-brief renders a bounded view' = agi-brief runs `agi-mem view` right after `agi-mem at`: the newest summaries then the newest raw chunks, cut at AGI_MEM_VIEW (4000) bytes, from ONE log + ONE cat-file stream (so a store of any size costs one bounded read). RE-CUT 1 (alive [decision] 19:52:47Z 10-31, terms (a)-(f) pre-approved): (a) compact's slice is WHOLE tap commits, oldest first, stopping after the first that reaches AGI_MEM_COMPACT_MAX, so it can pass the cap by up to one tap commit (aio measured ONE 400-chunk commit = ONE 93272 B request); upto is always a whole commit; the words form was chosen, the code unchanged, so (b) is not owed. (c) the lock is $S/compact.lock, compacts only, none without a flock binary. (f) OWED BEFORE ANY summary_live FLIP, beside (a): compact has NO time bound (agi-infer's curl has no -m; compact wraps no timeout), so once summary_live is true a hung request holds compact.lock and every later compact exits 0 at flock -n with no log line. (e) mem-summary c1b: the UNREAD direction of the spend gate (the cell ABSENT from the trunk's secrets.md: the stub gets the ONE request, the canary 0; AGI_TRUNK at no such ref cannot be the fixture, agi-mem's preamble reads posts.md from that trunk and exits 0 before compact) + its mutant (stub only on an explicit false -> RED). FALSIFIER sharpened, not changed: F1 = mem-summary.t.sh v1-v4 (10 and 10000 chunks, the cut as a cell, an unread store rc 1; mutant: the cut dropped -> 2.3 MB -> RED); F2 = c1-c7 (summary_live false: the stub gets the ONE request and a canary 'real' endpoint 0; mutant: the forcing line dropped -> the canary gets it -> RED), plus summary_live true goes to the real URL.
director-general-2 11-01 CLOSE (B = L326, council 3/3; the summary_live flip stays the owner's, banked by belam): status complete. F2 AMENDED in this close commit, words only: 'with credits_live false' -> 'with summary_live not true (false, absent or unread; never credits_live)'. Reason: the council's D3 (alive [decision] 14:17:17Z 10-31) ordered the stub forcing keyed on its OWN default-false cell, never credits_live (true since 10-25), and 'its F2 rows key on that cell'; the DEVIATION was named in this THOUGHT at B's cut; the falsifier text had not followed. The same close (RE-CUT 1, alive [decision] 00:21:25Z 11-01, terms 3/3) also moves the body's other routes off the retired cell, words only: Target 'until credits_live is true' -> 'until summary_live is true'; Invariant 'while credits_live is not true' -> 'while summary_live is not true' (it was FALSE against the code: compact reads summary_live alone, so summary_live true with credits_live false spends a call); title 'a stub until C1-C3 go live' -> 'a stub until summary_live is true'; Why 'only after C1-C3 go live' -> 'only after summary_live is true'. No run under credits_live false is claimed: the code does not read credits_live. Run on the trunk 278dd2700c (L332's wrap) at the cut: F1 `sh extensions/agi/tests/mem-summary.t.sh` exits 0 ('mem-summary: 0 FAIL', 15 rows): v1 (10 chunks) and v2 (10000 chunks) bounded, v3 the unbounded mutant RED, v3b the cut as a cell, v4 unread rc 1; F2 (as amended): c2 summary_live false -> stub 1, canary 0; c1b the cell absent -> the stub; c3 + c1c the mutants RED; c6 summary_live true -> the real URL. OWED before any summary_live flip, not this leaf's close: compact's time bound (RE-CUT 1 (f)); and B's crumbs (the view over the tip's set; one compact.log line per tap while the stub is dead).
<!-- THOUGHT:END -->
