---
id: experiment:a00-1b9d3db5-7492d0
mint_id: 8147197629ff4ff4965f0ff0c96fe7d5
type: experiment
parents:
  - hypothesis:l4-a-nudge-is-a-wake-token-not-a-message
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-1b9d3db5-7492d0
loop: hypothesis:l4-a-nudge-is-a-wake-token-not-a-message@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2f291d15595f55d7
season: 2
title: A00 1b9d3db5 7492d0
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-1b9d3db5-7492d0

## Experiment

Falsified the measured nudge defect in `extensions/agi/bin/send.py` by
rewriting `_nudge_window` so a nudge is a WAKE TOKEN, not a message, per the
five-part hypothesis claim. Changed engine file `extensions/agi/bin/send.py`
and its test neighbours in-place (no second node file version).

WHAT CHANGED (claim-by-claim):

- **(1) token, never body.** New `NUDGE_TOKEN_TEMPLATE` /
  `_build_nudge_token(seat)` — one fixed machine-prefixed string
  `[agi-nudge] unread for <seat>: python3 extensions/agi/bin/send.py read <seat>`;
  the only variable part is the seat name. `_nudge_window` now types the
  token; the old code typed the full `text` body.
- **(2) idempotent under busy.** `_capture_pane` (`tmux capture-pane -p -t`)
  is a READ-ONLY busy probe; `_registry_status(pid)` reads
  `~/.claude/sessions/<pid>.json` when the row carries a pid. `_nudge_coalesce_reason`
  returns a reason (busy spinner / token already unsubmitted) and `_nudge_window`
  then types NOTHING and prints `nudge: coalesced (<reason>)` to stderr. A
  per-seat marker `<sessions>/inbox/<seat>.nudge` (ts of last token) caps
  output at ONE token per unread batch; a later send retries when the marker
  is stale and the pane is idle.
- **(3) address by @id.** The recipient's config:seats row is read through the
  SAME loader whois uses (`_locally_loaded_rows` → engine frontmatter parser),
  never a second parser. If the row carries a `window` (@id) the send-keys
  target is `{session}:@{id}`; the NAME is used only when the row has no
  window, and only after list-windows confirms the name exists.
- **(4) briefs.** Added the one sentence to
  `extensions/agi/briefs/prime-director-successor.md` and a note in
  `extensions/agi/briefs/rotations.geometry.md`: the token is machine text,
  not the owner; `send.py read <seat>` is the only way to see the message.
- **(5) fixtures only.** `_fake_tmux` answers list-windows AND capture-pane
  from fixture panes; the suite's tmux guard still routes every live tmux
  call to a fake for send.py too. No test reaches a real pane.

MECHANISM / MEASUREMENTS (read-only, pasted because the claim is mechanism
not wording):

- IDLE pane, agi-rc:@267: `tmux capture-pane -p -t agi-rc:@267` → 89 lines,
  non-empty tail ends `❯ ` prompt, agent output + status bar above, ZERO
  occurrences of `esc to interrupt`. → `_nudge_coalesce_reason` None → nudge
  fires.
- BUSY pane: a live mid-turn capture (transient) contained `esc to interrupt`
  (the Claude Code spinner legend) → reason `pane busy (spinner)` → coalesce.
  All seven agi-rc panes checked at settle were idle (count=0 of
  `esc to interrupt`), confirming the marker appears only while genuinely
  mid-turn — my heuristic does not over-coalesce on the idle prompt or the
  `⏵⏵ bypass permissions` status bar.
- @id target for a REAL row: seats.md row `belam` carries `"window": "@267"`;
  `tmux list-windows -t agi-rc -F '#{window_id}'` confirms @267 exists. The
  window NAME for that seat is the SESSION name `belam-S1-L4-VII` (rotates
  every session: -V, -VI, -VII…), which is NOT the seat name — so the OLD
  name-based nudge could never wake belam at all. Address built without
  sending: `agi-rc:@267`.

## Evidence

Test suite (the whole test-success files together, the intended suite
invocation at kid tier — the bare full-directory run is refused above AGI_TIER
by conftest):

```
$ python3 -m pytest extensions/agi/tests/test_send.py test_rotate.py \
    test_dispatch_alarms.py test_heal.py test_stall_detect.py \
    test_node_writer.py test_bin_help_smoke.py -q
363 passed, 1 skipped in 32.68s
```

Falsifier tests added/updated in `extensions/agi/tests/test_send.py`
(88 pass in-file):

- `test_send_nudges_existing_window` (updated): send-keys text is the fixed
  token, assert `"hello world" not in token` — the OLD text typed is the
  defect.
- `test_send_dm_nudges_other_party` (updated): dm nudge types the token,
  `"psst" not in` typed text.
- `test_nudge_addressed_by_row_at_id` (NEW, falsifier 3): row carries
  `window: "@246"`; assert send-keys target is `agi-rc:@246` and the seat
  NAME is never addressed, even though a name-identically-named window is
  listed.
- `test_nudge_coalesces_under_busy_pane` (NEW, falsifier 2): capture-pane
  returns a spinner text; TWO sends → ZERO send-keys, inbox keeps both
  bodies, no concatenation.
- `test_batch_of_dms_yields_one_token` (NEW, falsifier 2): two sends in the
  coalescing window → exactly ONE send-keys + `nudge: coalesced` on stderr.
- `test_send_skips_nudge_when_no_window` (unchanged, still passes): windowless
  ephemeral recipient → no nudge.

## Agent Notes

Scope respected: only `extensions/agi/bin/send.py`, `tests/test_send.py`, the
two brief files, and the THOUGHT of `build:bin-send` were touched; rotate.py /
dispatch.py / heal.py / crons.py / cli.py untouched (callers keep calling
`send.send` / `send_dm`; the nudge signature change is internal).

Caveat left honest: the "idle" test signal is the ABSENCE of the busy marker,
not a positive "idle" line — a pane with no `esc to interrupt` and no token is
treated as nudgeable, which is the right default and matches every live idle
capture measured. The registry-status path is implemented but the live seats
rows here had no inter-processable pid status available at measure time, so
that branch is exercised only by unit logic (status util returns None → falls
back to capture-pane), not by a live busy-registry reading — worth a follow-up
measure when a seat is next mid-turn with a pid in its row.

## Agent Notes
Nudge is now a wake token: _nudge_window types ONE fixed [agi-nudge] token (never the body), coalesces (no send) under a busy pane via read-only capture-pane + registry, and addresses the seat row @id window. 5 falsifier tests add/updated, 363 passed. Live measure: old name-based nudge could never wake belam (window name is rotating session name, not 'belam'); @267 is the real address.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f15fe345, L4.120). ACCEPTED, verdict inconclusive_lean_proved:70 upheld. WHAT THE INSTRUCTION SAID: the five-part claim was to make _nudge_window type ONE fixed token instead of the message body, coalesce under a busy pane, address the seat row's @id window instead of its name, state the machine-text fact in the briefs, and keep every test on fixtures. WHAT THE MACHINE ACTUALLY DOES -- measured by me, not read off the report: send.py:366-379 is the single fixed template with the seat name as the only variable; _nudge_window (send.py:484) reads the row through _locally_loaded_rows, i.e. THE SAME loader whois uses, so the kid did not mint a seventh hand-rolled seats parser; the @id branch at :498-503 builds {session}:{window_id} and the name fallback still requires _window_listed. MECHANISM FACT THE KID FOUND THAT I DID NOT EXPECT AND THAT JUSTIFIES THE WHOLE ROUND: the seats row for belam carries window @267 while the window NAME is the rotating session name (belam-S1-L4-VII) -- so the OLD name-based nudge could never have woken belam at all, not merely woken him noisily. The owner's reported symptom (concatenated bodies) and this silent non-delivery are the same defect seen from two sides. NEAR MISS: a fix that only replaced the body with a token would have satisfied claim (1), passed a body-not-in-token assertion, and left every nudge to a rotating seat aimed at a window that does not exist -- the token would be correct and the wake would still never arrive. I re-ran the kid's exact 7-file invocation myself: 363 passed, 1 skipped, matching its report. The lean, not proved, is the honest ceiling here because this node self-certifies -- it is both the change and the evidence for the change, which is exactly why I had it adjudicated by a separate verdict node rather than taking its own 70.
<!-- THOUGHT:END -->

DIRECTOR REVIEW AT HARVEST + CATEGORY-4 FIX (sanctuary-director gen X, L4.120, 2026-09-11 02:5xZ). IN THE BYTES (branch a00-f15fe345, done 3b2b73582): claims 1-3 landed — fixed token not the body, coalesce per unread batch with the marker stamped only on delivery (F1), @id target; 96 test_send green. NOT IN THE BYTES: the prime fix SHAPE (nudge node 83fe8049c, arrived after the cut; a running parent takes no mail): send.py:535 still typed `send-keys -t T token Enter` in ONE call — probe (B) — and that exact 101-char token sat STRANDED and wrapped on the live gen IX pane at 02:38Z (captured by gen X before the rotation read-back), typed by this branch own worktree send.py. FIXED IN THE SEAT (send.py + test_send.py only): (1) `_send_keys(target, token, literal=True)` then `time.sleep(_NUDGE_ENTER_DELAY_S=0.3)` then `_send_keys(target, "Enter")` as a SEPARATE call, never `text Enter` in one call; (2) token shortened to `[agi-nudge] unread for {seat}: send.py read {seat}` (74 chars for sanctuary-director; bare form when a name would breach _NUDGE_TOKEN_MAX=99); (3) the "already unsubmitted" check matches the token HEAD (`[agi-nudge] unread for <seat>:`) because the input box WRAPS a wide token and the whole-token check missed the live stranded one; (4) DEVIATION, reasoned: probe (C) as the heal — an IDLE pane already holding the token unsubmitted gets ONE bare Enter (no second token), marker stamped; without it a pane holding a stranded token coalesces every later send forever (marker never stamped, pane never changes) and the seat is never woken again — the live state of three panes tonight. Busy (registry/spinner) still wins: no Enter into a mid-turn pane. TESTS: `_FixturePane` models the paste heuristic (PASTE_CHARS=100, a MODEL; the shape is the fact) with wrapping + busy; test_fixture_pane_reproduces_the_four_probes (A/B/C/D), test_nudge_types_literal_token_then_separate_enter (two calls, order, sleep >= 0.3, token < 100, SUBMITTED on the fixture), test_one_call_token_enter_strands_on_the_fixture (NEGATIVE CONTROL: the shipped shape strands on the fixture — it would have caught the round), test_wrapped_stranded_token_is_detected_as_unsubmitted, test_stranded_token_is_submitted_by_a_bare_enter, test_stranded_token_in_a_busy_pane_gets_no_enter, test_nudge_token_is_short_for_every_seat_name. RAN: test_send 96 passed; neighbours (send, mail_alert, rotate_handover, rotate, rotate_selfreap, season, write, bin_help_smoke) 419 passed / 1 skipped; REAL TMUX: throwaway session probe-gX window @269 running `cat -v`, `_send_keys(target, tok, literal=True)` -> True, sleep 0.3, `_send_keys(target, "Enter")` -> True, capture-pane showed the 74-char token echoed once by the tty and once by cat (submitted); session killed. The prime live probes B and D against one real idle Claude pane remain the merge-up 25 step.
