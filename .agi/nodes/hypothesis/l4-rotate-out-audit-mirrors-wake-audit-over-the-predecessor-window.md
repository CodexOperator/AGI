---
id: hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window
mint_id: 4074aec4e48643cf8c8d32d1cdc6e303
type: hypothesis
parents:
  - goal:g15.13
  - hypothesis:sensei-wake-audit-subcommand
next_edges: []
edited_by: sensei-director
scaffold_hash: 9d677bae85a2acfb
season: 2
testable_claim: "OWNER 2026-09-11 15:5xZ (doc:l4-owner-decisions): 'check the logs and calls of the outgoing predecessor for all roles, not just the successor … minimize number of tool calls needed to rotate out'. Goal goal:g15.13 (parents + '## Why this exists' there). BUILD ORDER — measure, implement, prove: (1) sensei.py gains SUBCOMMAND rotate-out-audit --seat S [--gen N] [--transcript PATH] (no new bin/ file; --gen = the generation that rotated OUT; default = the latest record's b_generation.before). (2) The PREDECESSOR's transcript is resolved from the rotation records under <sessions>/rotations/, NEVER from the newest transcript in a slug dir (that is the successor's): the previous record of the same seat (b_generation.after == N) carries handover.join.transcript; fallback ~/.claude/sessions/<pid>.json for a pid in the outgoing record's s12_self_reap.chain / handover.reap_own_pid; neither resolving = named refusal exit 2; --transcript is the explicit override. (3) WINDOW = [the last real input -> the record's recorded_at]: every assistant tool_use after the LAST user turn that is not a tool_result (the last merge-up reply / owner / Prime turn) to the transcript end; print the start turn index, its timestamp, the call count. (4) CATEGORIES: (a) a step rotate-self already performs or could pre-fill — re-measured §0 numbers verify/the record hold, git status/log re-reads of what rotate-self --dry-run prints, seats-row/meter/ack/bootstrap reads of fields the record carries — the row NAMES the record field or rotate-self step duplicated; (b) a hand poll/read of a record or a pane (ls/cat under sessions/rotations, tmux capture-pane, rotate.py status, ps, read-backs of the card just written); (c) protocol learning (-h, source/log greps — reuse _is_protocol_learning); (d) the genuine decision (the card edit = where-it-stops/banked, the rotate-self invocation, the ack, the one-line rotation report). Reuse wake_audit's helpers (_iter_tool_uses, _norm_cmd, _summarize_tool_input, _is_protocol_learning) — refactor shared, never copy. (5) OUTPUT mirrors wake-audit: header line, window bounds, counts a/b/c/d, one row per call with the duplicated label; exit 2 named on no seat row / no record / no transcript. (6) TESTS test_sensei_rotate_out_audit.py (run WITH test_sensei_wake_audit.py + test_sensei.py): fixture transcript + fixture records — a hand re-measured count -> (a) naming the field; tmux capture-pane -> (b); rotate.py -h -> (c); the card edit + rotate-self -> (d); no user turn after the first -> whole transcript is the window; predecessor transcript resolved through the previous record, refused when absent; RED FIRST. (7) LIVE PROBE in the parent's verdict: run on sanctuary-director 135144Z (gen XIV out), sanctuary-helper 152548Z (gen III out), belam 140328Z (gen IX out; predecessor pid 2254436) — paste counts, check one hand-classified call per rotation. FALSIFIERS: a hand-classified call the tool classifies differently with no naming rule; the predecessor transcript resolving to the successor's; a window starting at the transcript head when a later user turn exists. FILE SCOPE: extensions/agi/bin/sensei.py, extensions/agi/tests/test_sensei_rotate_out_audit.py (new); test_sensei_wake_audit.py only where a helper moves. EXCLUDED: rotate.py, config:rotations, hooks, any bin/ file. CEILING: up to 2 kids; the parent merges every kid branch into the round branch before done:. Report: the pre-fix hand count per rotation (from the Sensei's drafts under .agi/sessions/sensei/drafts/) beside the tool's count."
thought_session: sensei-director-genI-L1
title: sensei.py rotate-out-audit classifies the outgoing predecessor's calls from its last real input to the record, mirroring wake-audit
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR sensei-director 16:2xZ (Sensei package e8a7df41b, line 1): accept --record TS as the exact key beside --gen N (the record filename <seat>.<TS>.json; --gen resolves to it). The Sensei's drafts are NOT in this worktree — they are gitignored under MAIN: /home/ubuntu/work/agi/.agi/sessions/sensei/drafts/ (captive-driven-proposals-20260911.md + the three <seat>-wake-audit-<TS>.md files with their appended rotate-out sections); read them there, read-only. Hand counts to beat: point 135144Z rotate-out 6 calls, helper 152548Z 11, prime 140328Z 3; genuine decisions in each: 2.
