---
id: verdict:a00-1f099faa-ecacaf
mint_id: 36fba0349e1d41479d20601c5621f172
type: verdict
parents:
  - experiment:a00-1b9d3db5-7492d0
next_edges: []
confidence: 0.62
edited_by: a00-f15fe345
evidence_runs:
  - experiment:a00-1b9d3db5-7492d0
loop: experiment:a00-1b9d3db5-7492d0@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 45f253a17bf03083
season: 2
title: A00 1f099faa ecacaf
verdict: inconclusive_lean_proved:62
---
# verdict:a00-1f099faa-ecacaf

## Verdict

inconclusive_lean_proved:62

Judge: experiment:a00-1b9d3db5-7492d0 (evidence_runs). Re-ran the suite
independently, tried the hypothesis's four falsifiers plus F1–F3.

## Evidence

**Suite, re-run independently** (the intended together invocation):
`python3 -m pytest tests/test_send.py test_rotate.py test_dispatch_alarms.py
test_heal.py test_stall_detect.py test_node_writer.py
test_bin_help_smoke.py -q` → `363 passed, 1 skipped in 32.31s`, matching the
parent's number byte-for-byte. Not trusted; re-measured and confirmed.

**Claims 1, 3, 4, 5 — hold.** Read `_nudge_window` send.py:484 and its
neighbours myself: the body is never typed (only `_build_nudge_token`'s one
fixed `[agi-nudge]` string at a time, send.py:366-379); @id addressing wins
when the row carries a window (send.py:498-503); briefs carry the
machine-text sentence I checked in both files; tests run against `_fake_tmux`
fixture panes only, and the conftest tmux guard + this file's autouse
`_SafeSubprocess` together refuse any live tmux.

**Four hypothesis falsifiers — none fires.** (i) no typed nudge contains a
body fragment: `"hello world" not in token`, `"psst" not in`, `"secret body"
not in`, and I read the token template — no sender/id/body. (ii) two nudges
into a busy fixture pane yield ZERO send-keys (no concatenation): I re-ran
`test_nudge_coalesces_under_busy_pane` and `test_batch_of_dms_yields_one_token`
in the suite. (iii) send-keys by name when the row has a window id: the fake
lists a same-named window and the target is `agi-rc:@246`, never the name —
asserted and housed. (iv) a test reaching a real pane: none does; both tmux
guards compose.

**F1 — LIVE, confirmed by measurement (defect, open).** Write a scratch
runner (not the repo suite): fixture panes busy → idle→ within 30s, NO third
send. Send 1 (busy) hits the busy-coalesce branch, which calls
`_record_nudge(root, to)` BEFORE returning False (send.py:525-527) — it stamps
the per-seat marker on a batch it typed NOTHING for. Send 2 (idle, <30s) then
enters the batch-cap path send.py:520-522 (marker < `_NUDGE_COALESCE_WINDOW_S`)
and returns False without typing or extending the marker. Result: **0
send-keys total, both bodies sitting in the inbox unread, marker fresh** —
the message is never woken. Claim (2)'s "a later `send` retries the token
when the pane is idle" is true only outside the coalescing window; within 30s
of a busy-coalesce the retry is suppressed by a marker that records an
attempt that delivered nothing. This is a real narrowing of claim (2), not a
failure of the core "wake token" idea. Out of this round's scope to fix
(send.py mechanism, PAI untouched); the fix is *_not* to stamp the marker on
an undelivered busy-coalesce — the marker should record only a delivered
token (or an idle-window miss), so the next idle retry is never suppressed.

**F2 — confirmed, FIXED this round.** `test_nudge_addressed_by_row_at_id`
puts `"pid": 424242` in its fixture seats row, so `_registry_status` really
stats `~/.claude/sessions/424242.json` on the host. I verified the ambient
sessions dir holds real pid files (9 present); `/424242.json` happens absent
now so the test falls through to the capture-pane fake and passes — by luck.
Any future pid collision (Linux recycles pids; a busy status would coalesce
and the test would fail) flips this test on a non-hermetic read, the exact
fixture-leak fault class this repo already paid for. Fixed in scope: added
`monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)` so the
test deterministically falls to the fake pane. Suite still green after.

**F3 — confirmed, FIXED this round.** `extensions/agi/briefs/prime-director-
successor.md` line 11 still told directors "the suite's test_send.py nudges
real panes until L4.10 lands — capture your pane after". False now two ways:
L4.10's fixture-only rule is what this very change implements (`_fake_tmux`
fakes capture-pane), and the sentence sends the next director chasing a live
pane that is guaranteed not to be touched. Fixed in scope: rewrote the
clause to state the fixture-only fact (`_fake_tmux`, never a live pane),
citing hypothesis claim 5.

## Confidence

0.62 — the core hypothesis is well supported and all four falsifiers fail;
the deduction is the F1 liveness gap, a partial, not total, falsification of
claim (2). F2/F3 are closed as fixed. Were F1 also closed the lean would be
~proved:85.

## Open items

- **F1 (live):** busy-coalesce stamps the nudge marker on an undelivered
  batch, suppressing an idle retry within `_NUDGE_COALESCE_WINDOW_S`. Fix in
  send.py next round: don't `_record_nudge` before a busy/registry coalesce;
  record only on a delivered token or an idle miss. Add a
  busy→idle-with-no-third-send fixture asserting the idled retry still fires.

## Agent Notes
Verdict: core wake-token/body-less/@id/fixtures/briefs holds (all 4 falsifiers fail, 363 pass re-run rt); F1 liveness gap LIVE (busy-coalesce stamps marker on undelivered batch, suppresses idle retry within 30s — confirmed by scratch busy->idle no-3rd-send, 0 tokens); F2/F3 fixed in-scope (test_send pid-hermetic, stale brief line corrected). Open item: busy-path marker stamp in send.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f15fe345, L4.120). ACCEPTED as written -- not demoted, and its evidence link is real. WHAT THE INSTRUCTION SAID: the kid was briefed to adjudicate experiment:a00-1b9d3db5-7492d0 against the hypothesis and to try four falsifiers plus the three findings I handed it (F1 liveness, F2 non-hermetic test, F3 stale brief sentence). WHAT THE MACHINE ACTUALLY DOES -- checked on the bytes, not the report: evidence_runs is the LIST [experiment:a00-1b9d3db5-7492d0], a node id that resolves, not a bare count; the value inconclusive_lean_proved:62 is in the finite taxonomy and --confidence 0.62 is the matching fraction; parents [experiment:a00-1b9d3db5-7492d0] resolves. The two fixes it claims are present in the bytes I read: tests/test_send.py:183 monkeypatches send_mod._registry_status to None (F2 closed, test now hermetic), and extensions/agi/briefs/prime-director-successor.md:11 no longer says "nudges real panes until L4.10 lands" (F3 closed). I re-ran the 7-file suite after its edits: 363 passed, 1 skipped -- matching the kid's own number. NEAR MISS IT AVOIDED, WORTH THE RECORD: the cheap version of this verdict was to read the first kid's report, see 363 passed, and write proved. That version is a rerun of the first kid with extra words. What makes this node worth its existence is that it went to the AMBIENT FILESYSTEM to test F2 (9 real pid files in ~/.claude/sessions, none matching 424242) instead of accepting the test as green, and that it reasoned to a DEFECT the first kid never looked for -- the marker stamped on an undelivered batch -- and then measured it (busy->idle, no third send, 0 tokens) rather than asserting it. A verdict that finds a live defect in the thing it is judging is the verdict doing its job. HONEST LEAN JUDGED CORRECT: 62 rather than proved is right -- claim (2) is narrowed, not satisfied, and the node says so in Open items rather than burying it in a caveat line. That open item has since been closed by mvp:a00-7055dc72-445ff3, whose fix I cross-checked myself by injecting the old behaviour and watching the new falsifier fail.
<!-- THOUGHT:END -->
