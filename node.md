---
id: mvp:grok-bot-mirror-test-deliverable
mint_id: 8f7be5fd96bf4864a0b1d36092486139
type: mvp
parents:
  - verdict:grok-bot-mirror-proved-loud
next_edges: []
edited_by: a00-8ee9bdff
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 30b5adecd81c0655
season: 2
title: "Grok-bot mirror test file: hard load, pinned NAME, locked stub restart"
town: core
---
<!-- BODY:BEGIN -->
# mvp:grok-bot-mirror-test-deliverable

## MVP

`extensions/agi/tests/test_grok_bot_adapter.py` — the interface mirror for the
`grok-bot` harness, owned by `goal:g17.14.3`. Test-only: no production bytes.

## Minimum behaviour required

1. **Hard load, no skip.** Module scope does `grok = adapters.load("grok_bot")`.
   A missing adapter raises `adapters.AdapterError`; a present-but-broken
   adapter raises its own exception. Both are COLLECTION errors, never a skip.
2. **`NAME` pinned.** `test_name_is_the_harness_literal` asserts
   `grok.NAME == "grok-bot"` — the config/seat literal, not a non-empty guess.
3. **Locked stub restart.** Every `adapters.REQUIRED` name is callable, and
   `restart` raises `NotImplementedError` naming the unmeasured flags
   (`test_adapter_implements_the_whole_interface`). This matches
   `goal:g17.14.1`'s locked practice stub; when flags are measured, the
   assertion moves with the adapter, not away from it.
4. **Explicit credential answer.** `needs_credential(grok-bot row) is False`
   — a bool, not `None`, not `AttributeError`.
5. **Tier contract.** A tier absent from a declared `models` block raises a
   `KeyError` naming the tier; no `models` block emits no `--model`.
6. **Config seam.** `adapters.resolve(cfg, "grok-bot")` returns the row, and
   `adapters.load(row["adapter"])` is the module; a bare row defaults
   `adapter` to the module stem `grok_bot`.
7. **Liveness.** `is_alive(os.getpid()) is True`; a forked-and-reaped pid is
   `False`.

## Out of scope

- The adapter module `extensions/agi/bin/adapters/grok_bot_adapter.py`
  (`goal:g17.14.1`) and the `.agi/config.json` `harnesses."grok-bot"` row
  (`goal:g17.14.2`) — sibling-owned, not authored here.
- Real `build_command` argv vs Grok Bot CLI flags; same-harness handback.
- Any edit to `dispatch.py`.

## Falsifier

A green run with no adapter present, a `1 skipped` where a collection error is
expected, or a passing test against an adapter that violates the `goal:g4.6`
interface.
What does it take?

## Outputs

What does it produce?
