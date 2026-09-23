---
id: experiment:a00-06dae36a-cccc0d
mint_id: a374f3b8da424fb6a04653cdd2b09017
type: experiment
parents:
  - hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips
next_edges: []
confidence: 0.9
edited_by: a00-06dae36a
evidence_runs:
  - experiment:a00-06dae36a-cccc0d
loop: hypothesis:unreachable-key-authority-gates-the-swap-missing-ref-skips@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "fetch-timeout", "class": "gate", "cmd": "pytest test_rotate_key_authority.py -k ef86_fetch_timeout; stubbed subprocess.run raises TimeoutExpired on the FETCH and answers rc 2 on ls-remote", "expected": "pre-fix: TimeoutExpired escapes (RED). post-fix: authority: FAILED, no SKIPPED, swap still deferred", "observed": "BASE: 3 failed in 1.29s (RED, OSError/TimeoutExpired escaped). TIP: 3 passed", "result": "held"}
  - {"conjunct": "probe-timeout", "class": "gate", "cmd": "pytest ... -k ef86_probe_timeout; fetch answers rc 1, ls-remote raises TimeoutExpired", "expected": "authority: FAILED naming ls-remote, never raised, swap deferred", "observed": "BASE RED; TIP green", "result": "held"}
  - {"conjunct": "fetch-oserror", "class": "gate", "cmd": "pytest ... -k ef86_fetch_oserror; fetch raises OSError(git not found), probe rc 2", "expected": "authority: FAILED naming the launch failure, never raised, never SKIPPED", "observed": "BASE: OSError escaped the function; TIP: authority: FAILED -- could not launch git fetch", "result": "held"}
  - {"conjunct": "ef84-retry-refusal", "class": "wire", "cmd": "_retry_authority_publish_for_pending_swap(tmp g, aa) with the hanging-fetch stub and a deferred_for authority .key.pending", "expected": "returns the refusal line (NOT completed ... AUTHORITY), never raises; key byte-identical; pending present", "observed": "returned key swap NOT completed ... AUTHORITY; key bytes unchanged; pending present", "result": "held"}
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
EF.73 made an unreachable origin FAIL instead of SKIP, but the fetch and the ls-remote probe still called subprocess.run(timeout=60) with no exception guard, so a HANGING origin raised TimeoutExpired (or OSError) out of a function whose own docstring says "never raises" -- and the EF.84 retry at the rotate-self site then raised before the mint. This version wraps BOTH calls: a fetch exception breaks the retry loop (a hang will not un-hang) and sets unreadable; a probe exception returns FAILED directly; the rc-2 SKIPPED branch is suppressed when the fetch itself was unreadable. Nothing in the swap machinery changed; FAILED defers exactly as before. Tests are monkeypatch-only, no origin.
<!-- THOUGHT:END -->

## Agent Notes
Guarded the fetch and ls-remote probe in rotate.py:_publish_row_to_authority against TimeoutExpired/OSError -> authority: FAILED (never SKIPPED, never raises), unreadable suppresses rc-2 SKIPPED, swap defers via untouched machinery; 3 new monkeypatch-only tests RED on base, GREEN on tip, named suite 29 passed/1 xfailed
