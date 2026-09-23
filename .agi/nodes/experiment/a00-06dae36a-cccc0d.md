---
id: experiment:a00-06dae36a-cccc0d
mint_id: a374f3b8da424fb6a04653cdd2b09017
type: experiment
parents:
  - hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
next_edges: []
confidence: 0.9
edited_by: a00-f49a12cf
evidence_runs:
  - experiment:a00-06dae36a-cccc0d
loop: hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "fetch-timeout", "class": "gate", "cmd": "pytest test_rotate_key_authority.py -k ef86_fetch_timeout; stubbed subprocess.run raises TimeoutExpired on the FETCH and answers rc 2 on ls-remote", "expected": "pre-fix: TimeoutExpired escapes (RED). post-fix: authority: FAILED, no SKIPPED, swap still deferred", "observed": "BASE: 3 failed in 1.29s (RED, OSError/TimeoutExpired escaped). TIP: 3 passed", "result": "held"}
  - {"conjunct": "probe-timeout", "class": "gate", "cmd": "pytest ... -k ef86_probe_timeout; fetch answers rc 1, ls-remote raises TimeoutExpired", "expected": "authority: FAILED naming ls-remote, never raised, swap deferred", "observed": "BASE RED; TIP green", "result": "held"}
  - {"conjunct": "fetch-oserror", "class": "gate", "cmd": "pytest ... -k ef86_fetch_oserror; fetch raises OSError(git not found), probe rc 2", "expected": "authority: FAILED naming the launch failure, never raised, never SKIPPED", "observed": "BASE: OSError escaped the function; TIP: authority: FAILED -- could not launch git fetch", "result": "held"}
  - {"conjunct": "ef84-retry-refusal", "class": "wire", "cmd": "_retry_authority_publish_for_pending_swap(tmp g, aa) with the hanging-fetch stub and a deferred_for authority .key.pending", "expected": "returns the refusal line (NOT completed ... AUTHORITY), never raises; key byte-identical; pending present", "observed": "returned key swap NOT completed ... AUTHORITY; key bytes unchanged; pending present", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "probe_ef86.py P1 -- stub subprocess.run inside rotate: raise TimeoutExpired on git fetch, answer rc 2 on git ls-remote", "expected": "authority: FAILED; the exception does not escape; a probe rc 2 must NOT downgrade it to SKIPPED", "observed": "authority: FAILED -- fetch of authority branch season2/main timed out after 60s", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_ef86.py P2 -- stub: git fetch rc 1, git ls-remote raises TimeoutExpired", "expected": "authority: FAILED naming ls-remote, never raises, never SKIPPED", "observed": "authority: FAILED -- ls-remote of season2/main timed out after 60s", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "probe_ef86.py P3 -- stub: git fetch raises OSError(git not found), git ls-remote rc 2", "expected": "authority: FAILED naming the launch failure, never SKIPPED, never raises", "observed": "authority: FAILED -- could not launch git fetch for season2/main: git not found", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "probe_ef86.py P4 -- _retry_authority_publish_for_pending_swap(g, aa) with a deferred_for authority .key.pending and a hanging fetch stub", "expected": "returns the refusal line carrying NOT completed and AUTHORITY, never raises; key byte-identical; pending present", "observed": "key swap NOT completed -- pending ... deferred on the AUTHORITY leg; key byte-identical; pending present", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "probe_ef86.py P5 -- rotate._authority_publish_gates_swap on the FAILED line the timeout path returns and on a SKIPPED line", "expected": "FAILED gates the swap (True); SKIPPED does not gate (False)", "observed": "True / False", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "probe_red_base.py -- guard-stripped copy of _publish_row_to_authority (text transform of the live source) run with the same fetch/probe timeouts", "expected": "TimeoutExpired escapes the function on both, proving the two guards are load-bearing (RED base)", "observed": "P6a fetch escaped True; P6b probe escaped True -- both escaped without the guards", "result": "held"}
production_lines: 25
profile: balanced
role: kid
scaffold_hash: c5aa5b4cbb750477
season: 2
title: A hanging key authority fails and defers the swap, never raises
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-06dae36a-cccc0d

## Why this round (parent hypothesis, round 2)

```
EF.73 (merged)   : a FAILED fetch now probes `ls-remote --exit-code` -> rc 2 SKIPPED, else FAILED.
RESIDUAL (EF.84): `_publish_row_to_authority` says "never raises" (rotate.py ~10401),
                   but its fetch (~10431) and ls-remote probe (~10498) call
                   subprocess.run(..., timeout=60) with NO TimeoutExpired/OSError guard.
                   A HANGING authority -- the very case EF.73 names -- raises OUT of the
                   function instead of yielding `authority: FAILED`; the EF.84 retry at the
                   rotate-self site (~17547) then raises BEFORE cmd_rotate_self mints.
```

## What was built

Guard the fetch call and the ls-remote probe call INSIDE `_publish_row_to_authority` only
(25 added / 7 removed lines, measured with `git diff --numstat`):

| Site | Exception | Result |
|---|---|---|
| fetch (~10431) | `TimeoutExpired` | `break` the retry loop (a hang will not un-hang), `last` names the timeout, `unreadable=True` |
| fetch | `OSError` | same, `last` names the launch failure |
| ls-remote probe (~10506) | `TimeoutExpired` | `return authority: FAILED -- ls-remote ... timed out` |
| ls-remote probe | `OSError` | `return authority: FAILED -- could not launch git ls-remote` |

`unreadable` suppresses the rc-2 -> `SKIPPED` branch: if the fetch itself could not be
read, a later probe rc 2 must still FAIL (we could not read the authority). The EF.73
rc-2 -> SKIPPED path is preserved for a NORMALLY failed fetch (non-zero rc, no exception).
The swap machinery (`_authority_publish_gates_swap` / `_complete_pending_key_swap` /
the EF.84 retry) is untouched: FAILED defers as before, and the retry returns its refusal
line instead of raising because the callee no longer raises.

## Tests (committed, `test_rotate_key_authority.py`)

Fixtures/monkeypatch only -- no real origin, key, fetch or push.

| Test | Conjunct |
|---|---|
| `test_ef86_fetch_timeout_fails_and_defers_the_swap` | fetch `TimeoutExpired` -> FAILED (not SKIPPED even at probe rc 2); retry refusal; pending present, key byte-identical |
| `test_ef86_probe_timeout_fails_and_defers_the_swap` | fetch rc 1 + probe `TimeoutExpired` -> FAILED naming ls-remote; swap deferred |
| `test_ef86_fetch_oserror_fails_and_never_raises` | `OSError('git not found')` -> FAILED naming the launch failure; never SKIPPED |
| `_assert_retry_defers` (used by tests 1-2) | EF.84 `_retry_authority_publish_for_pending_swap` returns `key swap NOT completed ... AUTHORITY`, never raises |

## Evidence

```
RED  (base bytes, guard removed): env -u TMUX -u TMUX_PANE python3 -m pytest
     extensions/agi/tests/test_rotate_key_authority.py -q -k ef86
     -> 3 failed, 12 deselected in 1.29s
        OSError: git not found  (and TimeoutExpired) escaped _publish_row_to_authority
GREEN (tip): the same command -> 3 passed, 12 deselected in 0.41s

Full named suite on the tip:
  env -u TMUX -u TMUX_PANE python3 -m pytest
    extensions/agi/tests/test_rotate_key_authority.py
    extensions/agi/tests/test_rotate_pending_swap_authority.py
    extensions/agi/tests/test_rotate_alert_two_tree.py -q
  -> 29 passed, 1 xfailed, 22 warnings in 6.02s
```

Raw logs: `.agi/sessions/iter-EF.86/a00-06dae36a/{red,green,suite}.txt`.
The EF.73 test `test_ef73_unreachable_origin_fails_and_defers_the_swap` is unchanged and
still passes in the 29.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f49a12cf, EF.86) -- ACCEPTED as proved. (1) WHAT THE INSTRUCTION SAID: from the EF.86 orders, 'a timeout (and an OSError launching git) on either call yields the same authority: FAILED ... line the non-zero rcs yield, never raises; the swap then defers exactly as for any FAILED', and 'run one negative probe per claim conjunct yourself and record them as probes'. (2) WHAT THE MACHINE ACTUALLY DOES, built and run by me: rotate.py:_publish_row_to_authority now wraps its fetch (rotate.py:10431) in try/except (subprocess.TimeoutExpired, OSError) -> unreadable=True, names the failure, breaks the retry loop, and wraps the ls-remote probe (~10520) -> returns authority: FAILED directly; the rc-2 SKIPPED branch carries 'and not unreadable'. My six parent probes (probe_ef86.py P1-P5 + probe_red_base.py P6, recorded in this node probes:) all held: a fetch timeout yields 'authority: FAILED -- fetch of authority branch season2/main timed out after 60s' even when the stubbed probe answers rc 2; a probe timeout yields FAILED naming ls-remote; an OSError on the fetch yields FAILED; _retry_authority_publish_for_pending_swap returns its 'NOT completed ... AUTHORITY' refusal with the key byte-identical and the pending file present; _authority_publish_gates_swap reads the returned FAILED as True and a SKIPPED as False; and a guard-stripped copy of the SAME function raises TimeoutExpired on both legs (RED base), so the guards are load-bearing and the added tests pin the changed bytes. (3) THE NEAR MISS: a fix that returned SKIPPED whenever the fetch raised would satisfy 'does not raise' and lose the mechanism -- an unreadable authority would stop gating the swap, the exact regression EF.73 removed; the 'and not unreadable' suppression on the rc-2 branch is what prevents it, and P1 pins it (probe rc 2 yet FAILED). A second near miss: catching only TimeoutExpired and not OSError leaves the unlaunchable-git path raising; P3 pins it. (4) DEVIATION: none. The review edit is parent-scoped (probes, thought, note) and the kid's rotate.py and test bytes are untouched. CAVEAT recorded for the next round, not a demotion: the push call inside the same function (rotate.py ~10491) and the _g() git calls are still bare subprocess.run with no guard, so the 'never raises' contract still has a third leg unfixed; it is outside the ordered FILE SCOPE (fetch + ls-remote probe), so this round is accepted with that residue named.
<!-- THOUGHT:END -->

## Agent Notes
Guarded the fetch and ls-remote probe in rotate.py:_publish_row_to_authority against TimeoutExpired/OSError -> authority: FAILED (never SKIPPED, never raises), unreadable suppresses rc-2 SKIPPED, swap defers via untouched machinery; 3 new monkeypatch-only tests RED on base, GREEN on tip, named suite 29 passed/1 xfailed

Parent ACCEPTED experiment:a00-06dae36a-cccc0d as proved: read the rotate.py guard bytes and the three committed tests, ran six independent negative probes (fetch timeout -> FAILED even at probe rc 2; probe timeout -> FAILED; fetch OSError -> FAILED; EF.84 retry refusal with key byte-identical and pending present; gate True on FAILED / False on SKIPPED; guard-stripped copy raises on both legs = RED base). Residual, out of ordered scope: the push call and _g() git calls in the same function remain unguarded.
