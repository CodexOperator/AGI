---
id: hypothesis:g716111-t3-a-test-is-a-nodes-falsifier-line-starting-dollar-space-run-by-agi-frontier-observe-sh-reports-five-states
mint_id: 1ae91f27fa8b416a8cd6304fdb6e4146
type: hypothesis
parents:
  - goal:g7.16.1.11.16
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 1ab6d07c887b76a0
season: 2
testable_claim: "(T3) a `## Falsifier` line that starts with `$ ` is a runnable test row: agi-frontier runs it and observe.sh reports one of met (exit 0) \u00b7 red (exit != 0) \u00b7 unrunnable (the command cannot start) \u00b7 BROKEN (the row is malformed) \u00b7 mute (no row), per goal; the 13 gate lanes of lanes.sh (goal:g7.16.1.11.13 falsifier 1, `sh extensions/agi/tests/aa3-lanes.t.sh`) become rows; the expansion is about +155 B in the engine pieces and 0 B in the base."
title: "Shell tests T3: a test is a node's ## Falsifier line starting `$ `, run by agi-frontier; observe.sh reports met / red / unrunnable / BROKEN / mute per row; the 13 gate lanes (lanes.sh) become rows"
town: core
---
# hypothesis:g716111-t3-a-test-is-a-nodes-falsifier-line-starting-dollar-space-run-by-agi-frontier-observe-sh-reports-five-states

## Measured
- belam [decision] 14:5xZ 10-02 (cc SM) accepting the council's shell-tests rule (alive [rule] 14:54Z); council numbers: 324 py files, 173,231 lines, 7,965 tests, 0 shell tests; full suite 7,911 passed / 0 failed at 96140880b; v5 uids cannot import pytest. HORIZON: ordered AFTER phase W of goal:g7.16.1.11.15 (or beside it, if no file overlaps).
- Pieces already in engine.md: agi-frontier (460 B, each active goal runs its falsifier), observe.sh (255 B, what the body IS). The five states and the ~+155 B are belam's/the council's figures; not re-measured by me.
- all-is-one 14:07Z/14:08Z: the row for goal .13 falsifier 1 is `sh extensions/agi/tests/aa3-lanes.t.sh` (exit 13 while agi-land is unbuilt, 2 once built, 0 after the four byte fixes); a row that sat green because the script exited 0 early would read falsely: the row lands WITH the script.

## CLAIM
(T3) a `## Falsifier` line that starts with `$ ` is a runnable test row: agi-frontier runs it and observe.sh reports one of met (exit 0) · red (exit != 0) · unrunnable (the command cannot start) · BROKEN (the row is malformed) · mute (no row), per goal; the 13 gate lanes of lanes.sh (goal:g7.16.1.11.13 falsifier 1, `sh extensions/agi/tests/aa3-lanes.t.sh`) become rows; the expansion is about +155 B in the engine pieces and 0 B in the base.

## Dispatch line
config-max: none / template-max: the `## Falsifier` line form `$ <command>` in the goal schema's body rules (owner/Prime anchor if it is a schema edit: not decided here) / code: agi-frontier + observe.sh deltas (+155 B). NOT dispatched: HORIZON.

## FALSIFIERS
one goal node whose Falsifier line is `$ true` reads met and `$ false` reads red in observe.sh; a malformed `$ ` row reads BROKEN, a missing command reads unrunnable, a goal with no row reads mute · the 13 lanes read as 13 rows · base bytes unchanged (<= 8,192 B), seed <= 1 KB · negative: a row that exits 0 without running its command (the early-exit case) is caught by the lanes script's own FAIL count.

## TESTS
a scratch tree with 5 goal nodes, one per state, run through agi-frontier + observe.sh; `wc -c` on the pieces before/after (expansion <= 160 B); the base size check.

## FILE SCOPE
extensions/agi/ pieces agi-frontier + observe.sh (engine*.md pieces, belam's [config]/anchor ring where it applies) · the goal body rules text · its own experiment node. NEVER the base beyond the budget.

## CEILING
1 parent · kids <= 1 · regular review; any anchor/schema edit is belam's. HORIZON.
