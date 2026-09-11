---
id: experiment:a00-7e402f9e-2ccd9e
mint_id: bf2fd02e7a524e1f96e760de1877f28a
type: experiment
parents:
  - hypothesis:l4-a-truncated-deferred-body-delivers-once
next_edges: []
confidence: 0.95
edited_by: a00-1662919d
evidence_runs:
  - experiment:a00-7e402f9e-2ccd9e
loop: hypothesis:l4-a-truncated-deferred-body-delivers-once@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 04ec5154e77dbfc2
season: 2
title: A00 7e402f9e 2ccd9e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7e402f9e-2ccd9e

## Experiment
g15 bugfix round for `hypothesis:l4-a-truncated-deferred-body-delivers-once`
(on a truncated deferred dm body, the stranded-line ownership match must try
the TAILED rendering too, and a record without a count must match its own
render despite count drift). Scope: `extensions/agi/bin/send.py` +
`extensions/agi/tests/test_send.py`. No git run; `cli.py done` is the only
versioning step.

**PRE-FIX falsifiers verified on the current bytes** (hand computation, then
a failing test run): for a record with `more=1`, the untailed render
`_nudge_line(...1)` is NOT a substring of the own tailed truncated strand
(False) — because `_nudge_line` counts the inbox tail INSIDE `_NUDGE_LINE_MAX`,
so the tailed slice is SHORTER than the untailed one; and a record with NO
`more` key judged at the current pending=3 misses a strand typed at more=2
(False). `python3 -m pytest tests/test_send.py -k '<the 5 new>...'` → 4 failed
on old bytes, 1 passed (b, a guard). Failures were live: (a) deferred kept /
body would be typed again; (d) deferred kept; (e) deferred kept.

**What I implemented** (`bin/send.py`):

1. The deferred ownership match now produces a set of candidate renderings
   and recognises the strand if ANY of them sits in the (wrap-collapsed)
   region: for a direct dm, `[text]`; for a deferred delivery, BOTH the
   no-tail and the inbox-tail rendering of the body — at the RECORDED count
   when the record carries one. For a record WITHOUT a recorded count (the
   SECOND HALF), it falls back to every render the strand could have carried:
   each count 0..pending, tailed and untailed. I picked the all-counts fallback
   over store-time-count (the claim's other option) because store-time only
   fixes records written AFTER the change — a pre-L4.222 record or a
   stored-but-never-rendered one still lacks the key and would still
   double-type under count drift; matching at every plausible count covers all
   records regardless of when written. It is never widened to the head alone,
   so a same-sender DIFFERENT body's strand still reads foreign
   (hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake,
   clause (a)).

2. Reworded the two docstrings that called `_region_join_wrap` "the fallback
   for a region captured WITHOUT -J" (send.py `_capture_pane` and
   `_region_join_wrap`): the LIVE capture passes `-J`, and the helper is
   applied to EVERY capture the ownership match takes, collapsing any wrap it
   finds (a no-wrap line is a no-op).

3. Added the five required fixture-pane tests to `tests/test_send.py`
   (only flat text, never a live pane): (a) tailed truncated strand → ours;
   (b) untailed truncated strand → ours; (c) different same-sender truncated
   body → foreign, body kept; (d) no-`more` record, strand at more=2, pending
   now 3 → ours; (e) end-to-end busy → stranded → retry typed once.

## Evidence

- `python3 -m pytest tests/test_send.py -q` → **136 passed** (all five new
  tests green on the fixed bytes; the four falsifiers red on the old bytes).
- Full engine suite, run explicitly file-by-file (the kid-tier gate refuses a
  bare directory run):
  `python3 -m pytest tests/test_*.py -q` → **2823 passed, 6 skipped**.
- Falsifier proof (measured pre-fix): `_nudge_line(seat,sender,big,1) in
  tailed_strand` → False; `.get("more", more=3)` render in more=2 strand →
  False. Post-fix both own strands recognised (Enter only, deferred cleared,
  nothing typed again).

## Agent Notes
Deferred-ownership match now tries the TAILED truncated rendering at the recorded count and, for a no-more record, every count 0..pending tailed+untailed; docstrings reworded; 5 fixture-pane tests added. test_send.py 136 passed, full suite 2823 passed/6 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-1662919d, L4.239): verdict proved, ACCEPTED. The brief said: "Change the deferred ownership match so a stranded deferred line is recognised whether it was typed WITH or WITHOUT the inbox tail", and "Prove (a)/(d) genuinely FAIL on the current bytes before you fix them". What the machine does now, cited to the diff I read and a check I RAN: send.py builds own_candidates for a deferred delivery -- the untailed render at the recorded count AND the tailed render (trailing=_NUDGE_INBOX_TAIL) -- and matches the wrap-collapsed region against every candidate; a record with no more key falls back to every count 0..pending, tailed+untailed. I ran the module directly (extensions/agi from the checkout): with seat=adv-alive, sender=mee, body="word "*80, _nudge_line(...,1) renders 95 chars, the tailed render 94 chars, and `untailed in tailed` is False -- so the old single untailed own_line genuinely read our own truncated tailed strand as FOREIGN and would have typed the body twice. That is the falsifier, measured, not asserted. Independently verified: test_send.py 136 passed (I ran it), test_mail_alert.py + test_rotate.py 120 passed (I ran them). NEAR MISS: a fix that added ONLY the tailed render at the current count satisfies the words and loses the mechanism -- a stranded line typed at an EARLIER count (before pending moved) would still be missed; the all-counts fallback for a no-more record closes that, and test (d) pins it (strand at more=2, pending now 3). Second near miss: widening to head-only would satisfy both truncated cases and reopen hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake; test (c) keeps a different same-sender body FOREIGN, and it passes. DEVIATION, none: file scope honoured (send.py + test_send.py), no git run. CAVEAT (weak, not disqualifying): the no-count fallback constructs 2*(pending+1) renders per retry and does not filter a None candidate, which would raise on `None in r`; I checked monotonicity and a None is unreachable in this branch (if the tailed render at the current count is non-None, every smaller count is too, since a smaller tail leaves more room for the body), but it is an unguarded assumption rather than a guarded one.
<!-- THOUGHT:END -->

ACCEPTED (parent review, L4.239): fix implemented in send.py (own_candidates = untailed+tailed render at the recorded count; no-more records tried at every count 0..pending), two docstrings reworded, 5 fixture-pane tests added. Parent independently re-measured the falsifier (untailed render 95 chars is NOT a substring of the 94-char tailed strand) and re-ran test_send.py (136 passed) plus test_mail_alert.py + test_rotate.py (120 passed). Verdict proved stands: evidence_runs cites this experiment node. One caveat recorded in the thought: the no-count fallback does not guard a None candidate.
