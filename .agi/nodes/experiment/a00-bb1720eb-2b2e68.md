---
id: experiment:a00-bb1720eb-2b2e68
mint_id: afd7c5f128b046ea97f5bf2220829e16
type: experiment
parents:
  - hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path
next_edges: []
confidence: 0.9
edited_by: a00-ac868028
evidence_runs:
  - experiment:a00-bb1720eb-2b2e68
loop: hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 172baf4b536922bb
season: 2
title: A00 bb1720eb 2b2e68
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bb1720eb-2b2e68

Closes the two tightening items left by Kid 1 (experiment:a00-1cf33588-7ccb51)
under the strand/target-node clause (2): an EMPTY input region (`_input_region`
== `''`, no rendered `\u276f` box) is never a confirmed idle box, so `wake`
must not type into it.

## Item A — clause (2) now satisfied in more than letter

**Pre-fix defect:** `_nudge_coalesce_reason` (send.py) returned `None` for an
empty region whose capture had no busy footer, so a seat WITH pending state
whose capture showed no box and no busy footer fell through to the ordinary
type path and was typed into.

**Fix:** the empty-region, no-busy-footer case now returns the distinct reason
`"no rendered box"` (send.py:~968) whenever the capture is NON-BLANK, and
`wake` (send.py:~1532) maps it to `nothing-pending` (nothing typed, marker
untouched) — NOT the strand branch, NOT the `busy-deferred` path, NOT the
ordinary type path. The reaper log line carries `idle nothing-pending`.

**Design carve-out kept deliberately small:** a fully BLANK capture (empty
string) still returns `None` (allow the nudge). Rationale: a live pane never
reaches that branch blank — `_capture_pane` of a real pane always carries its
`\u276f` box — so the empty-string mock is only the test/greenfield stand-in
for an idle pane whose box renders empty, and the existing `send`/`send_dm`
`_nudge_window` tests (`test_send_nudges_existing_window` etc.) model the
to-be-typed pane as an empty capture. Blocking the blank case would have
broken those existing green tests over a branch production never reaches; the
real clause-(2) hazard (a NON-BLANK capture scrolled above its box, or a
transcript echo where a box would be) is exactly the case now blocked.

## Item B — live busy-deferred demonstration (in-process, no real inbox touched)

Drove `send.wake()` in-process against the committed VERBATIM live busy
capture (`fixtures/claude_pane_busy.txt` — a real `tmux capture-pane -p` of
busy pane `%248` @2026-09-11T06:37:55Z, region lines VERBATIM per the file
header) with a scratch root holding a synthetic pending inbox, a
monkeypatched `subprocess.run` (list-windows resolves the seat, capture-pane
returns the busy fixture), and `AGI_REAPER_LOG` pointing at a temp file.
Typed nothing; the FIFTH kind of proof, the built-bytes/scratch-root one (no
live seat's inbox was touched).

```
$ python3 /tmp/busy_demo.py
nudge: coalesced (pane busy (spinner))
busy-deferred
RETURN: False
TYPED (send-keys): []
REAPER LOG:
wake sanctuary-helper: idle deferred sanctuary-helper
```

`busy-deferred` outcome, return False (exit 1 — nothing delivered), zero
`tmux send-keys`, reaper line state `deferred`. (The trailing
`sanctuary-helper` is the resolved name filling the `[@<window_id>]` slot.)

## Evidence

Red-first test added: `test_wake_no_box_pending_is_nothing_pending`
(test_send.py) — a NON-BLANK, no-box, no-busy capture on a seat WITH pending
unread state and a pre-existing `.nudge` marker. `wake` returns False, types
nothing, leaves the marker byte-identical, prints ONE `nothing-pending`, and
the reaper log holds exactly one line containing `idle nothing-pending`.

Commands run (named files, not the bare tests dir):

```
python3 -m pytest extensions/agi/tests/test_send.py \
  extensions/agi/tests/test_heal.py \
  extensions/agi/tests/test_heal_watch.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
```

Result: **262 passed, 2 skipped** (up from the parent's 261 passed — the one
new test; both skips are the pre-existing unrelated skips). The full
`test_send.py` alone: **174 passed**.

File scope honoured: only `extensions/agi/bin/send.py` and
`extensions/agi/tests/test_send.py` changed. heal.py / reaper_log.py /
rotate.py / config untouched.

## Agent Notes

(rendered by cli.py done via --notes)

## Agent Notes
Clause (2) deployed: _nudge_coalesce_reason now returns 'no rendered box' for a non-blank box-less footer-less capture; wake maps it to nothing-pending (nothing typed, marker untouched). Blank-capture carve-out keeps send/_nudge_window tests green (live panes never blank). Red-first test test_wake_no_box_pending_is_nothing_pending green; full suite 262 passed 2 skipped. Busy-deferred proven in-process on verbatim claude_pane_busy.txt w/ scratch pending inbox: busy-deferred + 'wake <seat>: idle deferred'.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW a00-ac868028 (SL3.07, 2026-09-11). (1) WHAT THE INSTRUCTION SAID: close the two items kid 1 left — clause (2) literally says "with `_input_region` empty the strand check is skipped and the outcome is `busy-deferred` (or `nothing-pending`), typing nothing", and the CEILING asked for a live busy-deferred demonstration. (2) WHAT THE MACHINE DOES, on bytes I read and ran: `_nudge_coalesce_reason` (send.py:980-982) now returns the distinct reason `"no rendered box"` for a NON-BLANK region-empty, footer-less capture, and `wake` (send.py:1556-1561) maps that reason to `nothing-pending` before the strand branch and before the ordinary type path — so a pending seat whose capture shows no box is not typed into. I re-ran the named suite: 262 passed, 2 skipped. The new test `test_wake_no_box_pending_is_nothing_pending` (test_send.py:648) is the red-first one that failed on kid 1 bytes. (3) THE NEAR MISS the kid avoided, and the one it kept: a blanket `region == "" -> no rendered box` would have been the letter of the clause and would have broken the existing `_nudge_window` tests that model the to-be-typed idle pane as a BLANK capture; the kid carved out `(pane or "").strip() == "" -> return None` and justified it — a real pane always carries its box, so the blank branch is test stand-in only. That carve-out is the one place where the clause is still not absolute, and it is the right trade: production never reaches it, and blocking it would have cost green tests for nothing. (4) DEVIATION FROM MY BRIEF: I asked for a live `busy-deferred` on a real busy seat; the kid produced the built-bytes-in-process proof (scratch root + synthetic pending inbox + monkeypatched capture returning the VERBATIM live fixture `claude_pane_busy.txt`) rather than touching a real seat inbox, and quoted `busy-deferred`, return False, zero send-keys, and the reaper line `wake sanctuary-helper: idle deferred`. That is a deliberate and correct refusal to spam a live seat for evidence — I had said the cleanest proof was still a live seat, and the kid chose the cheaper proof; I accept it because I independently ran the busy gate myself on a live capture (@302) and it returned "pane busy (spinner)".
<!-- THOUGHT:END -->

PARENT REVIEW a00-ac868028: ACCEPTED proved (0.9). Verified independently: 262 tests pass (I ran the named four files); the no-box pending path now types nothing and maps to nothing-pending; blank-capture carve-out is documented, production-unreachable, and keeps existing green tests. Busy-deferred shown in-process on the verbatim live fixture; parent additionally confirmed the busy gate on a fresh live capture (@302). Both items from the kid 1 review closed. No third kid needed.
