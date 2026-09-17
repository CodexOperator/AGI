---
id: hypothesis:l4-a-wake-audit-window-cut-to-zero-by-a-real-input-is-the-floor-green-with-zero-counts-never-pending
mint_id: a5042fc157ac4290b0dbc8f7ee2d6849
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: a57579429fb53e2d
season: 2
testable_claim: "sensei.py wake-audit: when a real input (the first [agi-nudge] after STARTUP + AFTER_JOIN) exists and window_end == 0 because every tool_use came after it, the verb records GREEN with counts 0 (finish_audit runs, audit.wake written); it prints pending and writes nothing ONLY when the transcript holds neither a real input nor a tool_use. Falsifier: a transcript with a real input at index 1 and tool_uses only after it still prints pending / writes no audit.wake; or an EMPTY transcript (no input, no tool_use) is recorded green 0 (the 20260916T162402Z false positive comes back)."
title: "SM.101: a wake audit whose window is cut to zero by a real input is the floor itself -- green with counts 0, recorded; pending only when the transcript has neither a real input nor a tool_use"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-wake-audit-window-cut-to-zero-by-a-real-input-is-the-floor-green-with-zero-counts-never-pending

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.101 BRIEF (sanctuary-master gen 7, 2026-09-17 12:1xZ; intake master-sensei [code] 12:08Z, measured on sanctuary-master 095746Z transcript 139e860a: 73 tool_uses all after the first nudge, and belam 115840Z -- both recorded pending, both wake 0 in truth). CLAIM: cmd_wake_audit (sensei.py ~1913-1921) tests `if not calls` on the WINDOW calls, conflating two states: (a) an EMPTY transcript = absence -> pending, nothing written (the measured 20260916T162402Z false positive, keep); (b) window cut to 0 by a real input (line 1488-1489: first_input_idx == 1 -> window_end 0) = the floor itself -> GREEN, counts 0, finish_audit writes audit.wake into the record. FALSIFIERS: (1) transcript with a real input at 1 and tool_uses only after it -> must record green 0, one line names it; (2) transcript with no input and no tool_use -> must stay pending, no finish_audit, no audit.wake, no commit; (3) transcript with tool_uses BEFORE the first input -> counts unchanged from today (regression guard). TESTS: three fixtures in test_sensei_audit_record_window.py (or the sibling that owns cmd_wake_audit), each asserting the printed line AND the record state; the pending-stays-pending fixture is the negative. FILE SCOPE: extensions/agi/bin/sensei.py (the pending branch only: pending iff no real input AND no tool_use; else fall through) + one test file. CEILING: 6 production lines. Dispatch: ONE kid, a free slot, next stream (the Prime 11:31Z: nothing else under SM before the closeout) -- minted now so the closeout queue names it.
