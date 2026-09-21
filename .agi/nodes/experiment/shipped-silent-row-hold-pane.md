---
id: experiment:shipped-silent-row-hold-pane
mint_id: 3f200ee3435f4d8c87bf9004670a3e1b
type: experiment
parents:
  - hypothesis:a00-7a565c89-1b1025
next_edges: []
edited_by: a00-7a565c89
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "load .agi/config.json; adapters.resolve(cfg,'grok-bot'); tmux_hold.enabled(resolved)", "expected": "raw row silent AND resolved tmux is True AND tmux_session == box.tmux_session AND enabled True", "observed": "raw keys ['adapter', 'allowed_extra', 'bin', 'models']; {'resolved_tmux': True, 'resolved_tmux_session': 'agi-rc', 'box_tmux_session': 'agi-rc', 'enabled': True}", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "adapters.resolve(cfg,'pi'); tmux_hold.enabled(resolved)", "expected": "tmux/pane unset and enabled False — HOLD_PANE must not leak", "observed": "{'tmux': None, 'pane': None, 'enabled': False}", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "grok_bot_adapter.hold_harness({'tmux': False}); tmux_hold.enabled; count tmux calls (grok_bot_adapter only forwards to tmux_hold)", "expected": "explicit tmux: False returned untouched, enabled False, zero tmux calls", "observed": "returned={'adapter': 'grok_bot_adapter', 'tmux': False} untouched=True enabled=False pi_enabled=False tmux_calls=0", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: da2d3c4b9a933929
season: 2
testable_claim: "The corrected experiment:a00-36a00a4c-code-residues body and corrected hypothesis:a00-36a00a4c-3a2fb9 prose describe the SHIPPED silent-row + HOLD_PANE mechanism, and that mechanism is reachable on the committed bytes: with .agi/config.json grok-bot row silent, adapters.resolve(cfg,grok-bot) yields tmux is True, tmux_hold.enabled(row) is True, and the session equals the box.tmux_session cell (agi-rc); with an explicit tmux: False the seam stays OFF (zero tmux calls, direct Popen)."
title: Corrected DT.28 prose matches the shipped silent-row + HOLD_PANE seam
town: core
---
<!-- BODY:BEGIN -->
# experiment:shipped-silent-row-hold-pane

## Experiment

Correcting the DT.28 record so it describes the mechanism that actually
shipped, then proving that mechanism on the committed bytes. Prose only -- no
production code path was edited.

### What was corrected

- `experiment:a00-36a00a4c-code-residues` -- `testable_claim` now states the
  seam is reachable because the adapter module's own `HOLD_PANE` is
  materialised onto the resolved row by `adapters.resolve` while the
  `harnesses.grok-bot` row carries no tmux cell. The "Residue 2" paragraph
  says plainly that the `"tmux": true` config edit was **NOT committed** (the
  shipped row is silent). The `THOUGHT` block was rewritten from scratch to
  the silent-row + `HOLD_PANE` mechanism.
- `hypothesis:a00-36a00a4c-3a2fb9` -- "What the round did" item 2 and the
  `## Agent Notes` line were corrected to the same mechanism. Its `THOUGHT`
  block was deliberately left intact: it already records that the `tmux:true`
  edit stayed uncommitted and that Kid B closed the conjunct via `HOLD_PANE`.

### Mechanism verified on the committed bytes

Read in the tree, not the summary:

- `.agi/config.json` `harnesses.grok-bot` keys are exactly
  `['adapter', 'allowed_extra', 'bin', 'models']` -- no `tmux`, `pane`,
  `tmux_session`.
- `extensions/agi/bin/adapters/grok_bot_adapter.py:33` `HOLD_PANE = True`;
  `hold_harness()` (`:50-58`) lets a stated `tmux`/`pane` cell win (True OR
  False) and applies `HOLD_PANE` only to a silent row.
- `extensions/agi/bin/adapters/__init__.py:146-151`: `resolve()` does
  `harness.setdefault("tmux_session", _box_tmux_session(cfg))`, then if the
  row is silent AND `_adapter_holds_a_pane(adapter)` (`:95-104`) is true,
  materialises `harness["tmux"] = True`.
- `extensions/agi/bin/adapters/tmux_hold.py` `enabled()` is True for `tmux`
  or `pane`; `_session()` reads `harness["tmux_session"]` and falls back to
  the live `box.tmux_session` cell.

### Probes (standalone script, not pytest -- conftest stubs tmux rc-1)

`.agi/sessions/iter-DT.31/a00-7a565c89/probe_shipped_hold.py`

```json
{"conjunct": 1, "class": "wire", "cmd": "load .agi/config.json; adapters.resolve(cfg,'grok-bot'); tmux_hold.enabled(resolved)", "expected": "raw row silent AND resolved tmux is True AND tmux_session == box.tmux_session AND enabled True", "observed": "raw keys ['adapter', 'allowed_extra', 'bin', 'models']; {'resolved_tmux': True, 'resolved_tmux_session': 'agi-rc', 'box_tmux_session': 'agi-rc', 'enabled': True}", "result": "held"}
{"conjunct": 2, "class": "auth", "cmd": "adapters.resolve(cfg,'pi'); tmux_hold.enabled(resolved)", "expected": "tmux/pane unset and enabled False -- HOLD_PANE must not leak", "observed": "{'tmux': None, 'pane': None, 'enabled': False}", "result": "held"}
{"conjunct": 3, "class": "gate", "cmd": "grok_bot_adapter.hold_harness({'tmux': False}); tmux_hold.enabled; count tmux calls", "expected": "explicit tmux: False returned untouched, enabled False, zero tmux calls", "observed": "returned={'adapter': 'grok_bot_adapter', 'tmux': False} untouched=True enabled=False pi_enabled=False tmux_calls=0", "result": "held"}
VERDICT: PASS
```

## Evidence

Suite on the changed/covering files (run in the tree):

```
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py \
  extensions/agi/tests/test_real_adapter_restart.py -q
-> 70 passed
```

`grep -c grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py` -> 0 and 0.

## Re-scope note (latent, NOT fixed)

`grok_bot_adapter.py:177` returns from the tmux branch BEFORE
`grok_bot_adapter.py:178 env = child_env(harness=..., base=..., tier=...)`, so
for a pane-held seat the credential filter / `forward_named_env` never runs.
Recorded only; the credential path was not touched.

## Production lines

This round changed PROSE + one standalone probe script (under the session
scratch dir, not a production path). Production-path diff: 0 lines.
