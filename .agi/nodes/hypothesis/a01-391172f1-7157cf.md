---
id: hypothesis:a01-391172f1-7157cf
mint_id: d56668e41cf844f9806294ac24980cd3
type: hypothesis
parents:
  - goal:g4.6
next_edges: []
confidence: 0.75
scaffold_hash: f7d52ff171c7f75e
title: A01 391172f1 7157cf
verdict: inconclusive_lean_proved:75
---
# hypothesis:a01-391172f1-7157cf

## Hypothesis

**Claim:** `claude_code_adapter.py`, implemented 2026-09-03 (the week the pi
harness went dark on an OpenRouter budget cap), satisfies `mvp:unified-spawn-
path`'s falsifiers 1-3 as a *second* live harness, not just as the stub that
existed at `outcome:a00-c8365a0c-85a6d1`'s baseline (0/4 unmet). The seam drawn
by that MVP — `build_command`/`child_env` behind a config-named adapter, zero
harness-keyed branches on the shared path — was designed against one adapter
(`pi_adapter.py`) and never load-bearing-tested against a second until now.

**What would prove it:**
- `dispatch.py` calls only `adapters.load(harness["adapter"])` — no string
  literal `"claude-code"` or `"claude_code"` appears in `dispatch.py` itself.
  Confirmed: `grep -n "claude-code\|claude_code\|harness\[" dispatch.py` shows
  three hits, all `adapters.load(harness["adapter"])` or `harness["adapter"]`
  lookups — zero adapter-name branches.
- The new adapter's own test suite passes standalone:
  `test_claude_code_adapter.py` — 22 passed.
- The adapter documents real measured CLI behavior (repeated
  `--append-system-prompt` is last-wins, variadic flags swallow the
  positional prompt, auth lives on disk not env) rather than assumed
  behavior, matching the MVP's discipline for `pi_adapter.py` ("moved, not
  rewritten" / probed, not assumed).

**What would disprove it:** any branch in `dispatch.py` keyed on harness name
outside the adapter-lookup call sites; a `child_env`/`build_command` that
does not conform to the two-function interface `mvp:unified-spawn-path`
declared; or the moved/added tests failing.

## Evidence gathered this pass

- `grep -n "claude-code\|claude_code\|harness\[" extensions/agi/bin/dispatch.py`
  → lines 130, 290, 1116, all `adapters.load(harness["adapter"])` — no
  harness-name string literal anywhere in `dispatch.py`.
- `python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -q` →
  `22 passed in 0.08s`.
- The adapter file itself (module docstring) records the falsifier claim
  explicitly: "`dispatch.py` was not edited — `mvp:unified-spawn-path`'s
  first falsifier holds for the second harness too."

**Not run this pass:** the full suite (`extensions/agi/tests/`) — several
other files are mid-edit and uncommitted in this working tree
(`evidence_gate.py`, `grid.py`, `metrics.py`, their tests) by other
concurrent work, unrelated to this adapter; running and reporting on the
whole suite would attribute pass/fail noise from that unrelated work to this
claim. The targeted adapter test file is the relevant evidence here.


## Agent Notes
claude_code_adapter.py landed 2026-09-03 as a live 2nd harness; grep shows zero harness-name branches in dispatch.py outside adapters.load(), test_claude_code_adapter.py 22/22 pass
