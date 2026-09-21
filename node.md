---
id: mvp:a00-7055dc72-445ff3
mint_id: 2fc1c3166e024e5baaa59c51a0ca2ab8
type: mvp
parents:
  - verdict:a00-1f099faa-ecacaf
next_edges: []
confidence: 0.75
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-f15fe345
evidence_runs:
  - mvp:a00-7055dc72-445ff3
loop: verdict:a00-1f099faa-ecacaf@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7421a1ff3832b503
season: 2
title: A00 7055dc72 445ff3
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# mvp:a00-7055dc72-445ff3

## What this MVP is

Fixes F1 — the confirmed live defect from `verdict:a00-1f099faa-ecacaf` and
closes that verdict's `## Open items` entry ("fix belongs in send.py next
round"). The per-seat nudge marker in `extensions/agi/bin/send.py` /
`_nudge_window` used to be stamped on an **undelivered** busy/registry
coalesce, so a batch that coalesced *because the pane was busy* was marked as
if it had actually been nudged. A later `send` inside
`_NUDGE_COALESCE_WINDOW_S` (30s) then hit the batch-cap path and returned
False without typing — the message was never woken, even after the pane went
idle.

Scope: only the marker-stamp semantics inside `_nudge_window` (send.py) and
the new falsifier test (test_send.py). No new bin/*.py; token text, @id
addressing, claims 1–5, rotate/dispatch/heal/crons/cli/config/geometry all
untouched.

## (b) Before / after — which branch stamps the marker

**Before** — the busy/registry coalesce stamped the marker while nothing was
typed, and so did the send-keys-failure path:

```python
reason = _nudge_coalesce_reason(_capture_pane(...), token, _registry_status(pid))
if reason:
    _record_nudge(root, to)   # remember the attempt; absorb this batch  ← BUG
    print(f"nudge: coalesced ({reason})", file=sys.stderr)
    return False
...
except (FileNotFoundError, subprocess.TimeoutExpired):
    _record_nudge(root, to)   # ← also stamped though nothing was typed
    return False
```

This matched `_record_nudge`'s "absorb this batch" intent but flatly
contradicted `_last_nudge_age`'s own docstring, which says the age is
"Seconds since the last **typed** nudge token".

**After** — the marker is recorded only on an actually DELIVERED token (the
send-keys that returned successfully, right before `return True`):

```python
reason = _nudge_coalesce_reason(_capture_pane(...), token, _registry_status(pid))
if reason:
    # F1: batch NOT typed into the pane. NEVER stamp the marker here.
    print(f"nudge: coalesced ({reason})", file=sys.stderr)
    return False
...
except (FileNotFoundError, subprocess.TimeoutExpired):
    return False                # nothing typed → not marked delivered
...
_record_nudge(root, to)         # only delivery reaches here
return True
```

Net effect: the marker now genuinely means "a token was typed recently".
When the pane is busy, sends do not stamp, so once the pane goes idle the
very next send is not batch-cap-suppressed and the wake token fires.

## (a) Fixture-pane transcript — busy → idle with NO third send

Recipient `director` carries no pid (hermetic: registry status None, so
capture-pane decides). The fake's capture source is a **mutable list** the
test rewrites — the pane changes state BETWEEN the two sends, which a static
`capture_text` cannot express:

```
send(project, "director", "first", "kid")    # capture-pane → "...⠋...\nesc to interrupt\n"  (busy)
send(project, "director", "second", "kid")   # capture-pane → ""                             (idle)

tmux capture-pane  → busy  → reason="pane busy (spinner)" → coalesced, NO marker, NO send-keys
tmux capture-pane  → idle  → reason=None                   → send-keys typed, marker stamped

tmux send-keys =-t "agi-rc:director" "[agi-nudge] unread for director:... read director" "Enter"
```

Result: **exactly ONE send-keys** — the idled retry fires. Verified two ways:

1. Fixed code: `364 passed, 1 skipped` (required 7-file run; new test made it
   364 from 363). Whole repo suite green across all test files.
2. Falsifier cross-check: temporarily restoring the old `_record_nudge` in
   the busy branch makes the new test fail exactly as the verdict predicted —
   stderr shows `nudge: coalesced (pane busy (spinner))` then
   `nudge: coalesced (already nudged within 30s)` and assertion
   `the idled retry must fire exactly one token, saw []`. The test catches
   the bug; the fix makes it green.

## The verdict's Open item is CLOSED

`verdict:a00-1f099faa-ecacaf`'s `## Open items` named F1 live and said "the
fix belongs in send.py next round" — that item is now resolved: the marker
records only a delivered token, the busy→idle retry fires, and the suite is
green. Claims 1, 3, 4, 5 and the F2/F3 fixes from that verdict stand
unchanged.

## Inputs

A fixture project (`.agi/config.json`) plus the existing `_fake_tmux`-style
stub layer; the new test inlines a fake whose `capture-pane` return is
popped from a `["busy", "idle"]` list.

## Outputs

`send.py` stamps the per-seat `<sessions>/inbox/<seat>.nudge` marker only for
actually-typed tokens; `test_send.py` gains `test_busy_then_idle_fires_token_on_retry`,
the F1 falsifier (364 total).

## Agent Notes
F1 fixed: _nudge_window stamps the per-seat marker only on a DELIVERED token (busy/registry + tmux-failure branches no longer _record_nudge). New falsifier test_busy_then_idle_fires_token_on_retry (mutable capture: busy->idle, no 3rd send) fires exactly one send-keys. Falsifier cross-checked: old code fails it with 'nudge: coalesced (already nudged within 30s)', saw []; fixed code green. Required 7-file run: 364 passed 1 skipped (was 363). Full repo suite green. Verdict's Open item F1 is CLOSED.

## Agent Notes
F1 fixed: _nudge_window stamps the per-seat marker only on a DELIVERED token (busy/registry + tmux-failure branches no longer _record_nudge). New falsifier test_busy_then_idle_fires_token_on_retry (mutable capture busy->idle, no 3rd send) fires exactly one send-keys. Cross-checked: old code fails it ('already nudged within 30s', saw []); fixed code green. Required 7-file run: 364 passed 1 skipped (was 363); full repo suite green. Verdict Open item F1 CLOSED. Lean (not proved) only because the evidence gate credits experiment-type nodes and this node is an mvp.

## Agent Notes
F1 fixed: _nudge_window stamps the per-seat marker only on a DELIVERED token. Falsifier test_busy_then_idle_fires_token_on_retry (mutable capture busy->idle, no 3rd send) fires exactly one send-keys; cross-checked to fail on old code with 'already nudged within 30s'. Required 7-file run: 364 passed 1 skipped; full repo suite green. Verdict Open item F1 CLOSED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f15fe345, L4.120). ACCEPTED with the gate's demotion upheld. WHAT THE INSTRUCTION SAID: the kid was briefed to stop stamping the nudge marker on an undelivered busy-coalesce and to add a busy->idle-no-third-send falsifier. WHAT THE MACHINE ACTUALLY DOES -- verified by me on the bytes, not the report: send.py now returns from the busy/registry branch WITHOUT _record_nudge and without it in the tmux-failure except; the only _record_nudge is the one before return True (delivered token only). tests/test_send.py::test_busy_then_idle_fires_token_on_retry drives a MUTABLE capture list [busy, idle] -- a static capture_text genuinely cannot express the transition, and the kid did not settle for one. I INDEPENDENTLY INJECTED THE OLD BEHAVIOUR myself (_record_nudge restored in the busy branch, atomically restored afterwards, file byte-identical) and the new test failed exactly as predicted -- 0 tokens, stderr nudge: coalesced (pane busy (spinner)) then nudge: coalesced (already nudged within 30s). The falsifier is real and the fix is what makes it green. Full 7-file run re-run by me after the cross-check: 364 passed, 1 skipped. NEAR MISS: a busy probe built on a STATIC capture string would pass this test while leaving the defect live, because it cannot represent the pane changing state between two sends -- the test's value is entirely in the mutable sequence. DEMOTION UPHELD: the gate demoted proved -> inconclusive_lean_proved:75 on demote_reason "no experiment evidence (evidence_runs=0) for proved" and that is the correct outcome -- the claim is backed by a TEST, and a test that fails on the old code is evidence for the code, not an experiment node adjudicating the original hypothesis; the honest lean is right. ONE NODE DEFECT LEFT UNFIXED, RECORDED NOT REPAIRED (I will not hand-edit a body): this node carries THREE "## Agent Notes" headings -- two hand-written in the body by the kid plus the one cli.py done rendered -- so the "rendered exactly once however many times you call done" guarantee did not hold here. The fix is that a kid must not hand-author Agent Notes in the body at all; the writer owns that region. LOW-MEDIUM harm (reading noise, and a reader cannot tell which copy is authoritative), zero behaviour effect.
<!-- THOUGHT:END -->
