---
id: hypothesis:a00-9bcc560d-7dd08c
mint_id: 87bb36164a7c48db9fbedd2b825aa0be
type: hypothesis
parents:
  - goal:g4.6
next_edges: []
confidence: 0.7
scaffold_hash: aeb85565d0d1bb03
title: A00 9bcc560d 7dd08c
verdict: inconclusive_lean_proved:70
---
# hypothesis:a00-9bcc560d-7dd08c

## Hypothesis

**Claim:** the live tree has moved well past the 2026-09-01 baseline recorded
in `outcome:a00-c8365a0c-85a6d1` ("all 4 falsifiers unmet"). Falsifiers 1-3 of
`mvp:unified-spawn-path` now read as **met**, and falsifier 4's admitted weak
joint has been closed, without a fresh outcome node ever having been written
to say so.

Direct inspection of the working tree (2026-09-03), not a remembered claim:

- `extensions/agi/bin/adapters/` exists with `pi_adapter.py` **and**
  `claude_code_adapter.py` — the latter is a real implementation (`NAME`,
  `build_command`, `child_env`, `RESTORED_PREFIXES`/`RESTORED_NAMES` for env
  restoration), not the stub the MVP said was acceptable for this pass.
- `dispatch.py`'s `main()` resolves the harness once via `adapters.resolve` /
  `adapters.load` and calls `adapter.build_command` / `adapter.child_env`
  (dispatch.py:289-291, :439, :458). `pi_model_args` and `build_pi_args` are
  now explicitly marked `LEGACY SHIM — not the live path` (dispatch.py:118,
  :1106).
- `grep '"pi"\|claude-code'` over `dispatch.py` turns up exactly **one**
  string literal outside the adapter lookup: `zoom_command`'s hardcoded
  `--runtime pi` (dispatch.py:111). Its docstring explains this is
  deliberate and orthogonal — it pins zoom's *context-template* flavor
  (goal:s8, fixing a real contradiction from 2026-08-31), not the spawn
  harness — so it is not a harness-name branch in the sense falsifier 2
  means.
- `completion.py::is_complete` compares a stored `scaffold_hash` frontmatter
  field against a freshly-computed hash of the scaffold body
  (completion.py:55-91), not a raw placeholder-text match. This is exactly
  the fix the MVP's own THOUGHT block named as missing ("the honest
  alternative — hashing the scaffold at write time and storing the hash —
  is one more field this node does not currently require"), and it exists
  now.

**What would prove it:** a fresh outcome node re-running the MVP's four
falsifiers against current code and scoring 4/4 (or naming exactly which
remain unmet) — the audit this hypothesis is a prerequisite for.

**What would disprove it:** the third-harness falsifier (spawn a parent and a
kid through a brand-new config entry with zero `dispatch.py` edits) failing
in practice, or `claude_code_adapter.py`'s `build_command`/`child_env`
throwing on a real Claude Code spawn rather than working end to end.

**Caveat noted, not resolved here:** this inspection covers `dispatch.py` and
`completion.py` only. `heal.py`'s pid-polling — the other half of falsifier 4
— was not re-checked this pass; the 2026-09-01 outcome found it still polling
`pid`/`agent.json`, and `goal:g4.7` was named as where that work belongs, so
it may still be true.


## Agent Notes
Live tree has moved past the 2026-09-01 baseline outcome: real adapters/pi+claude_code, dispatch.py delegates via adapters.resolve/load with only one non-branching pi literal left, completion.py now hashes scaffold_hash instead of raw text match. heal.py pid-polling (falsifier 4's other half) not re-checked.
