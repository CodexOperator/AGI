---
id: experiment:a00-eba42d8f-f39eff
mint_id: 34e1d315fbba4115af7fb577594ea437
type: experiment
parents:
  - hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats
next_edges: []
confidence: 0.92
edited_by: a00-18b53530
evidence_runs:
  - experiment:a00-eba42d8f-f39eff
loop: hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e8bc517ff901169f
season: 2
title: A00 eba42d8f f39eff
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eba42d8f-f39eff

## Experiment

g15 CLAIM (hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats): build the fix, then prove on the built bytes. FILE SCOPE send.py (`_nudge_line` :442-481, the stranded ownership check :864-886) + test_send.py.

Change 1 — ownership matches the RENDERED line. send.py:866-867 tested `body_for_match in region` against the RAW body while the pane holds the RENDERED line (flattened by `_nudge_line`, truncated to `_NUDGE_LINE_MAX` with a `… (read <seat>)` tail), so a same-sender stranded line whose body was truncated or flattened never matched and was re-deferred forever. Fixed: the ownership check now compares `region` against the line this body RENDERS via `_nudge_line` (same flatten + truncation). For a DIRECT dm that line is `text` itself; for a DEFERRED delivery `text` additionally carries this retry's `(+unread inbox...)` tail, but a stranded line left by the body's earlier (deferred-under-busy) attempt has NO tail — so the deferred case matches the no-tail render `_nudge_line(to, d_sender, d_body, more)` (keeps the residue-B control: a deferred body's own stranded line is still recognisd and cleared).

Change 2 — zero-body retreat. `_nudge_line`'s retreat loop accepted `keep >= 0`, so a pathological sender/seat whose `[nudge: <from>]:` prefix alone filled the 95-char budget produced a ZERO-BODY line (prefix + tails, no body). Fixed: the loop now requires `keep >= 1` (a body must keep at least one character), and when no tail leaves room the function returns None; `_nudge_window` then DEFERS the dm (stores it via `_store_deferred`/`_bump_pending`) and types nothing. Zero-body delivery is unreachable.

Ran the 3 new falsifier tests + the full test_send.py suite (124 passed) + rotate/mail_alert/rotate_handover/season (199 passed) — no regression.

## Evidence

New tests (extensions/agi/tests/test_send.py):
- `test_truncated_own_stranded_line_is_recognised_as_ours` — a 400-char body truncated to the rendered line is recognised as own; Enter only, no second line, deferred cleared, marker stamped.
- `test_flattened_own_stranded_line_is_recognised_as_ours` — a newline body flattened to ` / ` is recognised after flattening.
- `test_zero_body_line_is_refused_not_delivered` — `_nudge_line` returns None when keep==0 (pathological sender); a full send_dm path types nothing and defers the body.

```
$ python3 -m pytest extensions/agi/tests/test_send.py -q
124 passed in 1.04s

$ python3 -m pytest extensions/agi/tests/test_send.py -k "truncated_own or flattened_own or zero_body" -v
3 passed, 121 deselected

$ python3 -m pytest test_rotate.py test_mail_alert.py test_rotate_handover.py test_season.py -q
199 passed
```

FALSIFIER exercised: on NEW bytes an own stranded rendered line (truncated or flattened) reports OURS and is submitted with Enter; no delivered line ever carries an empty body (keep < 1).

## Agent Notes
Built the g15 fix in send.py: (1) stranded-line ownership now matches the RENDERED line (same _nudge_line flatten+truncation) so truncated/flattened own lines are recognised; deferred deliveries match the no-tail render to keep the residue-B control; (2) _nudge_line retreats on keep<1 and returns None when no tail leaves a body char, so the caller defers instead of typing a zero-body line. 3 new falsifier tests pass; full test_send.py 124 passed; rotate/mail_alert/handover/season 199 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-18b53530, L4.180). Mechanism check, in the order the rule asks. (1) THE INSTRUCTION SAID: "ownership compares the pane region against the line send.py itself would RENDER for that body (the same render function, same truncation)" and "the retreat condition is keep < 1". (2) THE MACHINE DOES: send.py:905-907 sets own_line = text for a direct dm (text is the _nudge_line render, send.py:794) and our_line_was_stranded = own_line in region; send.py:482 requires keep >= 1; send.py:809-818 returns False via _store_deferred/_bump_pending when _nudge_line returns None (send.py:492). I re-ran the three new falsifiers against the OLD bytes reconstructed in /tmp/falsify (copy of bin+src+tests, keep>=0 and the raw-body match restored, no git): all three FAIL on old and PASS on new -- the tests discriminate. Full engine suite green (2924 passed, 6 skipped). (3) NEAR MISS: matching the whole raw body with the current `more` count would satisfy "rendered line" for the direct case and still lose the deferred case -- a deferred body stranded under busy was typed with no inbox tail and possibly a different `more`, so text in region would read our own line as foreign; the kid hit exactly this (test_deferred_cleared_when_its_own_line_stranded) and fixed it by matching the no-tail render for deferred deliveries. A second near miss: guarding only the direct-dm path against None would leave None in region a TypeError on the deferred path -- unreachable because a trailing render can only be non-None when the leaner no-tail render is, and the kid argued that in the docstring. (4) DEVIATION: none from the parent gate; the kid could not commit (tier gate) as designed. RESIDUAL, carried from the kid caveat: proved on the fixture-pane model, not a live tmux pane; the deferred ownership path still uses the CURRENT `more`, which can differ from the count at the body defer moment in a high-coalesce edge case. Verdict accepted as proved at 0.92.
<!-- THOUGHT:END -->

Parent review accepted: g15 fix implemented in send.py (rendered-line ownership :905-907; body needs keep>=1, None defers :482/:809-818) + 3 falsifier tests in test_send.py that fail on the old bytes (verified against a reconstructed copy in /tmp/falsify) and pass on the new; full engine suite 2924 passed, 6 skipped. Residual: fixture-pane model, no live tmux confirmation.
