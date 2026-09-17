---
id: experiment:a00-be94ec8b-7a1792
mint_id: ed60ae0269674eeab5f7ef7d72d3f025
type: experiment
parents:
  - hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero
next_edges: []
confidence: 0.9
edited_by: a00-be94ec8b
evidence_runs:
  - experiment:a00-be94ec8b-7a1792
line_ceiling: 8
loop: hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 14
profile: balanced
push_further:
role: kid
scaffold_hash: 525aee9f3b7d1baf
season: 2
title: rotate-out-audit out-window starts after the last git push work act not the last input
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-be94ec8b-7a1792

## Experiment — SM.84 ITEM 6 (out-window after the last WORK act)

G15 BUILD ORDER: implemented the fix, not merely measured the defect. The
rotate-out-audit OUT WINDOW now starts AFTER the last round-closing WORK act
(the last class-d `git push` that delivered the round to origin), NEVER at the
last real input — a ~35-minute working turn is no longer counted as out.

### Function + line changed
`extensions/agi/bin/sensei.py` — `rotate_out_audit`. After the existing
last-real-input window loop (still bounded by the record's `recorded_at`), a
small trim block finds the last class-d call whose command performs a `git push`
(a round-deliver; `_AUDIT_VERB` already classes `git push` as d) and drops every
call at-or-before it, recomputing `counts` and advancing `window.start_line` to
just after the push. No push in the window → the frame falls back to the
last-real-input behaviour (legacy tests unchanged). Each call row now also
carries its source `idx` to support the cut.

### Produced vs baseline out-window call counts (fixture)
Fixture mirrors the 20260917T000151Z hand ruling: a working turn (write.py card
edit + tagged send + `git commit` + `git push origin br`) then the closing tail
(own-record grep (b) + three card Edits + `git commit 'card done'` +
`rotate-self`).
- BASELINE (last-input frame): the whole turn is in the window — the out excess
  reads the working turn as out (observed "excess 107 / d=86").
- PRODUCED: out = 6 calls (b=1, d=5), `window.counted` = 6, floor 1,
  `audit_finding_line` = "FINDING … excess 5 over floor 1" — exactly the hand
  ruling. The push and every work call before it are cut; the closing-tail
  commit stays counted (rule is the PUSH, not commit).

### Tests added (test_sensei_rotate_out_audit.py)
1. `test_rotate_out_window_starts_after_the_last_work_push` — the hand-ruling
   fixture: 6 calls, counts {a:0,b:1,c:0,d:5,s:0}, counted 6, start_line ==
   push_line+1, finding line "excess 5 over floor 1".
2. `test_rotate_out_no_push_keeps_the_last_real_input_frame` — no push → the
   legacy last-input frame, nothing regresses.

Full sensei family: **205 passed** (test_sensei + rotate_out + wake_audit +
audit_record_window + audit_record_writeback). No SM.72 classifier conjunct
regressed (shared `classify_tool_use` untouched; the --settled verb untouched;
rotate.py untouched — item 7 is a separate kid).

### Production lines
`git diff --numstat` prod path (tests excluded): sensei.py **14 added / 1
deleted**. This exceeds the item's "+8" slice. The item estimate assumed the
out-cut was one line; the working cut must record the call's `idx` in the loop,
find the last class-d push, trim `calls`, recompute `counts`, and advance the
window's start_line — ~13 net lines is the honest minimum. The change is
complete, tested, and far under the graded STOP gate (2× of the boilerplate
50 = 100). Flagging as a ceiling concern per the report-back contract.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_rotate_out_audit.py -q
43 passed  (incl. the 2 new item-6 tests)
$ python3 -m pytest test_sensei.py test_sensei_rotate_out_audit.py \
    test_sensei_wake_audit.py test_sensei_audit_record_window.py \
    test_sensei_audit_record_writeback.py -q
205 passed
$ git diff --numstat -- extensions/agi/bin/sensei.py \
    extensions/agi/tests/test_sensei_rotate_out_audit.py
14  1  extensions/agi/bin/sensei.py
69  0  extensions/agi/tests/test_sensei_rotate_out_audit.py
```

Fixtures are hermetic synthetic transcripts; no real seat, record or write is
touched.

## Agent Notes
ITEM 6: rotate-out-audit OUT window now starts after the last class-d git push (round-close WORK act), never the last input. Implemented in sensei.py rotate_out_audit; 2 fixture tests prove the 20260917T000151Z hand ruling (out=6, excess 5, never 107/d=86); no-push falls back to legacy frame. 205 sensei-family tests green. Production lines 14 (item slice +8 was underestimated; flagged).
