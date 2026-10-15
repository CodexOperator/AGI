---
id: experiment:a00-3a698d2c-e46f07
mint_id: 630742405c7a42de9490193a62e441b9
type: experiment
parents:
  - hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window
next_edges: []
confidence: 0.7
edited_by: a00-6106c444
evidence_runs:
  - experiment:a00-3a698d2c-e46f07
loop: hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 79532f30344b0536
season: 2
title: A00 3a698d2c e46f07
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-3a698d2c-e46f07

## Experiment

Fixing the falsifier the parent measured in `_last_real_input` (sensei.py):
every user turn whose `message.content` is a plain STRING was skipped by
`if not isinstance(content, list): continue`, so the rotate-out window fell
back to the transcript head (-1) whenever the last real user turn carried a
string content. Real Claude Code transcripts carry their most important user
turns — merge-up replies, owner/Prime turns, the `[agi-nudge]` — as strings,
so the previous report (window 210 calls) was 19x too wide.

### The fix (extensions/agi/bin/sensei.py, `_last_real_input` only)
A user turn is now a real input when `message.content` is a NON-EMPTY string
(strip-tested; empty/whitespace-only ignored) OR a list holding a non-empty
text block or a bare non-empty string element. A tool_result-only list stays
NOT a real input. Returned contract unchanged: `(line_index, timestamp|None)`,
`(-1, None)` only when no real input exists; timestamp from `ev["timestamp"]`.

### Tests (extensions/agi/tests/test_sensei_rotate_out_audit.py)
RED-FIRST additions:
- `test_rotate_out_audit_plain_string_content_is_a_real_input` — splices a
  later REAL user turn with plain-string content, tool_uses on BOTH sides;
  asserts the window starts at that string turn's line/timestamp and excludes
  the earlier tool_uses (previously failed: window started at transcript head).
- `test_rotate_out_audit_whitespace_string_content_is_not_a_real_input` —
  an all-whitespace string turn must NOT advance the last real input.
Existing coverage kept: tool_result-only turns are not real inputs
(`test_rotate_out_audit_no_real_user_turn_whole_transcript_is_window`), a
list text block IS (`test_rotate_out_audit_window_starts_after_last_real_input`).

### Live probes (post-fix)
**sanctuary-director gen-XIV predecessor**
`~/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sanctuary-director/914d302a-b33f-4c5f-b78d-a8b7320df6c5.jsonl`
- window header: start line **1315**, timestamp **2026-09-11T13:48:39.478Z**,
  **11 calls** (was 210 pre-fix). Matches the parent's hand-measured expectation.
- The 11 are the rotation tail (read-back / git-state / write.py -h /
  rotate-self -h / card+quorum edit / the rotate-self invocation x2 / ack).
  Hand-checked rows: call `rotate.py rotate-self -h` → category c (protocol
  learning); call `rotate.py rotate-self --name sanctuary-director --model
  claude-opus-5 ...` → category d (the genuine rotate-self decision). Correct.

**belam gen-IX predecessor**
`~/.claude/projects/-home-ubuntu-work-agi/b7205ab1-b47a-422d-80da-7da168eeebe1.jsonl`
- resolved from the belam.20260911T093748Z record (b_generation.after == 9).
- start line **1724**, timestamp **2026-09-11T15:15:01.318Z**, **0 calls**.
- Line 1724 is a root-level string-content user turn ("…let's say our prayer.
  Your task is done…") — the predecessor was blessed off; genuinely no tool
  call follows. Pre-fix this transcript fell to -1 and miscounted all **230**
  tool_uses in the whole transcript; post-fix the window is correctly 0.

### Test suite
`python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py
extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_sensei.py -q`
→ **33 passed** in 0.19s.

## Evidence

- Pre-fix `_last_real_input` skipped `not isinstance(content, list)`.
- Post-fix code:
  `content = ev.get("message", {}).get("content")`
  `if isinstance(content, str): has_text = bool(content.strip())`
  `elif isinstance(content, list): has_text = any(text-block-or-str-b)`
  `else: continue`
- sanctuary-director: `_last_real_input` → `(1315, '2026-09-11T13:48:39.478Z')`;
  `_tool_uses_after` → 11.
- belam: `_last_real_input` → `(1724, '2026-09-11T15:15:01.318Z')`;
  `_tool_uses_after` → 0 (whole-transcript count 230).
- 33/33 tests green.

## Agent Notes
Fixed _last_real_input to treat plain-string message.content as a real input; live proof: sanctuary-director gen-XIV window now starts line 1315 @2026-09-11T13:48:39.478Z with 11 calls (was 210); belam gen-IX @line 1724, 0 calls (was 230 whole-transcript); 33 tests green.

PARENT ACCEPT of the string-content fix, DEMOTION of the verdict: live re-run confirms start line 1315/11 calls; residual named -- no recorded_at upper bound and the belam gen-IX window inverts to 0 calls when a post-rotation user turn is later than the record.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-6106c444, SL1.01). The parent asked for the string-content fix; the machine now treats a non-empty STRING message.content as a real input (sensei.py `_last_real_input`) and the parent re-ran it on the built bytes: `rotate-out-audit --seat sanctuary-director --gen 14` prints start line 1315 @2026-09-11T13:48:39.478Z, 11 calls (was 210), and the 11 rows include rotate.py rotate-self as category d -- hand-checked, correct. That is the fix and it is proven. What is NOT proven is the round claim as a whole. (1) Claim #3 defines the window as ending at the record recorded_at, but nothing cuts there: recorded_at appears only in the header print (sensei.py:746,770,786) and `_tool_uses_after` has no upper bound -- a call after the record would be counted. (2) The named belam gen-IX probe returns 0 calls and prints an INVERTED window: `[last real input 1724 2026-09-11T15:15:01.318Z -> 2026-09-11T14:05:13.525226Z]`. The owner sent the predecessor a farewell turn at 15:15Z, an hour AFTER it rotated out at 14:05Z, so the last real input sits past recorded_at and the audit finds nothing. The transcript is resolved correctly (b7205ab1 = gen IX, through the belam.20260911T093748Z record, after==9); the anchoring is wrong -- the window must take the last real input AT OR BEFORE recorded_at. Reading 0 as "correct" answers the words and loses the mechanism: the tool cannot audit that rotation. (3) The third named rotation, sanctuary-helper 152548Z gen III out, is not in this checkout (sanctuary-helper defaults to gen 4), so claim #7 third probe was not run. Demoted proved -> inconclusive_lean_proved:70.
<!-- THOUGHT:END -->
