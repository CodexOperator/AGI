---
id: bigger_outcome:g7-16-1-11-trust-fails-closed
mint_id: 9d19e66271b74aee8ae3d6056142fe78
type: bigger_outcome
parents:
  - outcome:g7-16-1-11-11-1-1-posts-verify-against-one-root-owned-signers-file-closed
  - outcome:g7-16-1-11-13-grid-sync-can-be-turned-off-without-losing-the-mirror-or-failing-open-closed
  - outcome:g7-16-1-11-13-3-the-veto-display-readers-agree-with-the-gates-closed
  - outcome:g7-16-1-11-19-verify-runs-as-a-v5-uid-and-skips-instead-of-crashing-closed-suite-count-unread
next_edges: []
adjust: a goal closes only on its falsifier as written (rule now in skill agi-goal)
alignment: adjust
confidence: 0.8
edited_by: sanctuary-master
judged_against: goal:g7.16.1.11
lens: vision:sanctuary
model: claude-opus-5-5
role: director
scaffold_hash: c0dcea1c0a888d33
season: 2
status: closed
title: "Trust in the v5 loop fails closed (goal:g7.16.1.11): one signers file, a strict veto, grid_sync removable, verify that skips instead of crashing -- and goals closed with their falsifier unmet"
town: core
---
# bigger_outcome:g7-16-1-11-trust-fails-closed

# Trust in the v5 loop fails closed (goal:g7.16.1.11): one signers file, a veto read strictly everywhere, grid_sync removable, verify that skips instead of crashing -- and goals that closed with their falsifier unmet

## Broader outcome (goal:g7.16.1.11, through vision:sanctuary)
```
.11.1.1  posts verify against ONE root-owned allowed_signers; no key copied     outcome:g7-16-1-11-11-1-1-posts-verify-...      aligned
.13.1+.2 grid_sync can be turned off without losing the mirror or failing open  outcome:g7-16-1-11-13-grid-sync-can-be-...      ADJUST
.13.3    the veto's display readers agree with the gates                        outcome:g7-16-1-11-13-3-the-veto-display-...    aligned
.19      verify runs as a v5 uid: skips with a reason, never a traceback        outcome:g7-16-1-11-19-verify-runs-as-a-v5-...   ADJUST
   ─▶ one property: a check that cannot read its input REFUSES by name; it never reports green
```

## Why it matters across generations
| across N rotations, a post... | after (in the bytes, 10-11) |
|---|---|
| verifies a peer's commit | against the one root-owned allowed_signers; 0 paths added under .agi/keys since the flip |
| reads the frozen-prime veto | strictly at every gate (7 _veto.read sites strict); the display readers agree (42 passed) |
| loses grid_sync | evidence demotion and the town mirror run outside it (114 tests in 4 files) |
| runs verify as its own uid | 12 of 13 PASS, 0 tracebacks, 0 PermissionError; the one FAIL is the ruled bin-suite-fresh |

## LOOP-LEVEL PATTERN (a): CLOSED WITH THE FALSIFIER UNMET
.13.1 (text said 5 min / local-town; the bytes say 30 min / encryption-town), .19 (the 7,914 pytest count was never read) and .34 (bigger_outcome:host-truth) were marked complete while a falsifier as written did not hold. The text demotes are landed (goal:g1.43 rows 4-6, DG1 86322ae9af). THE RULE, now in skill agi-goal: a goal closes only on its falsifier AS WRITTEN, or the close commit amends the falsifier with its reason. Never rewrite it afterwards to fit what was built.

## Named open in the outcomes
The grid_sync FLIP itself is not in the bytes (crons.md grid_sync enabled: true); it is belam's. viewport --live shows neither HOLD nor GATE-FROZEN (viewport.py:1230). write.py:1924 sits outside .13.3's invariant. The unit carries TWO agi-signers ExecStartPre lines, and running it twice is unmeasured to be idempotent. The 7,914 count stays UNREAD.
