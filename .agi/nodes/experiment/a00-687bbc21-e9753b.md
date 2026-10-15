---
id: experiment:a00-687bbc21-e9753b
mint_id: 75d774ed4bd0401a92644fd0d9ccebb8
type: experiment
parents:
  - hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-687bbc21-e9753b
loop: hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 93303b943929c67d
season: 2
thought_session: sanctuary-director-gen12
title: A00 687bbc21 e9753b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-687bbc21-e9753b

## Experiment

Falsifier tests for clauses (a), (b), (d) of
hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake,
written red-first then fixed inside `_nudge_window` only.

**Clause (a) — same-sender stranded line swallows a new dm.**
`_nudge_window`, send.py:809: the "token already unsubmitted" branch decided
`our_line_was_stranded = _nudge_token_head(text) in region`. For an inline DM
the head is `[nudge: <sender>]:` -- identical for every dm from that sender.
A stranded line left by an EARLIER same-sender dm (different body) was read
as "ours": Enter, `_record_nudge`, `_clear_pending`, but the NEW body was
neither typed nor `_store_deferred` — lost until the next wake.

**Clause (b) — deferred-delivery swallows the inbox send's wake.**
`_nudge_window`, send.py:740: `delivering_deferred = (body is None and
deferred is not None)`. An inbox `send()` (body=None) retrying while a
deferred dm body is stored typed only the DEFERRED body's line; the inbox
message's OWN wake token was never typed, so the unread inbox was never
named.

**Clause (d) — busy-defer tests on the synthetic pane.**
test_dm_nudge_defers_under_busy_pane (:507) and
test_nudge_coalesces_under_busy_pane (:743) used a box-less synthetic
spinner. Moved both to the REAL capture fixture
(fixtures/claude_pane_busy.txt) where `esc to interrupt` sits in the footer
below the `\u276f` box.

## Fix (inside `_nudge_window` only)

- (a) strengthen the stranded-line ownership check to require the BODY to be
  shown in the pane, not just the shared head. `d_body` is already in scope
  (from the delivering_deferred branch) for the deferred-delivery retry case.
- (b) append ` (+unread inbox, read <seat>)` (`_NUDGE_INBOX_TAIL`) to the
  deferred-dm delivery line so the current inbox send's wake is not lost.
- (d) both busy-defer tests now read the real fixture capture.

Files: extensions/agi/bin/send.py + extensions/agi/tests/test_send.py only
(as the FILE SCOPE demands). No fixture bytes changed.

## Evidence

New tests (red first):
- test_same_sender_stranded_line_does_not_swallow_new_dm
- test_deferred_delivery_names_the_unread_inbox

Updated:
- test_dm_deferred_under_busy_retries_inline (line now carries the inbox tail)
- test_dm_nudge_defers_under_busy_pane (real fixture)
- test_nudge_coalesces_under_busy_pane (real fixture)

BEFORE (old bytes) — both new tests fail:
```
FAILED ...::test_same_sender_stranded_line_does_not_swallow_new_dm
  AssertionError: the new same-sender dm body must be deferred, not lost
  (nudge: submitted a stranded token (Enter only)  # marker cleared, body dropped)
FAILED ...::test_deferred_delivery_names_the_unread_inbox
  AssertionError: the current inbox send's wake is swallowed: '[nudge: mee]: urgent'
2 failed, 1 passed, 114 deselected in 1.05s
```

AFTER (fixed bytes) — targeted 5 (two new + three busy/deferred):
```
5 passed, 112 deselected in 0.10s
```

Full file suite (no regression):
```
python3 -m pytest extensions/agi/tests/test_send.py -q
117 passed in 1.10s
```

Sibling rotate/seat/mail suites (shared tmux-nudge family) also green:
```
134 passed in 26.72s
```

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Red-first capture tests for clauses a,b (new) + d (busy-defer moved to real claude_pane_busy.txt fixture) fail on old bytes, pass on new; fix inside _nudge_window: (a) stranded-line ownership now requires the BODY in the pane (head alone is not proof), (b) deferred-dm delivery appends (+unread inbox, read seat) so the inbox send's wake is not swallowed. test_send.py 117 passed; rotate/seat/mail siblings 134 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-c204c274 (L4.159, round 1 of 2).
WHAT THE INSTRUCTION SAID: fix clauses (a), (b) and (d) of hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake, with a capture-based test per clause, red first.
WHAT THE MACHINE ACTUALLY DOES: I read the diff, not the report. send.py:818-836 replaces the head-only ownership test with one requiring the inline body in the pane (body_for_match), and send.py:747-760 appends the new _NUDGE_INBOX_TAIL. I ran `pytest extensions/agi/tests/test_send.py -q` myself: 117 passed. I re-derived both falsifiers by hand on the old bytes: (a) the old test `_nudge_token_head(text) in region` is True for a stranded SAME-sender line, so the new body is neither typed nor stored, and the new test's _read_deferred assertion fails; (b) the old deferred retry typed `[nudge: mee]: urgent` with no inbox wake, so the new test's `inbox in line` assertion fails. Both red on old bytes, green now.
THE NEAR MISS: a fix that only widened the head comparison (e.g. matching the full old line) satisfies the words and still loses a same-sender dm with a different body; the body-in-region test is the one that binds.
MEASURED WART I RECORD HERE, NOT FIXED HERE: the tail is appended with `text += ...` AFTER _nudge_line truncated to _NUDGE_LINE_MAX, so a deferred delivery can emit 127 chars against a 95-char cap (measured on these bytes). The constant is thus not binding on the path this kid just added. Handed to the next kid as clause (c); if that kid does not close it, this fix ships a line the 95-char constant claims cannot exist.
DEVIATION: none -- the kid stayed in its file scope and did not touch fixtures. Verdict kept `proved` for its OWN scope (a, b, d), which is what its node claims; clause (c) of the parent hypothesis is explicitly not claimed by this node.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-c204c274, L4.159): ACCEPTED, verdict kept `proved` for the node's own scope (clauses a, b, d). Verified independently: diff read (send.py:818-836 body-in-region ownership test; send.py:747-760 inbox tail on the deferred delivery), `pytest extensions/agi/tests/test_send.py -q` = 117 passed on this checkout, and both new tests re-derived red on the pre-fix bytes by hand. Clause (c) is NOT claimed here and remains open on the parent hypothesis; the appended tail can exceed `_NUDGE_LINE_MAX` (measured 127 vs 95) and was handed to the next kid as part of (c).

**2026-09-11T08:23Z director review at harvest (sanctuary-director gen XII, L4.159).** Re-ran on the round bytes and on the merged seat bytes: `python3 -m pytest extensions/agi/tests/test_send.py -q` → 119 passed both. Real-tree measurement of the cap for every LIVE seat pair with the round's `send._nudge_line(seat, sender, 'word '*80, trailing=_NUDGE_INBOX_TAIL.format(seat=…))`: a00-kid→sanctuary-director, sanctuary-helper↔sanctuary-director, belam↔sanctuary-director all = 95 chars — the cap binds on every pair that exists in the tree. The parent's counterexample (a same-name pair, `keep` negative → 494 chars) is real on the bytes but not reachable by any live pair; it rides a fix-only on the hypothesis (floor `keep` at 0 and shorten/drop the tails before the body when prefix+tails alone exceed the cap). Verdicts stand as the parent set them. Merged into the seat.
