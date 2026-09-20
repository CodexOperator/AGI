---
id: experiment:a00-ed5d3f6d-grok-seam
mint_id: 899737b2ba874748aef1c09d7acc6728
type: experiment
parents:
  - hypothesis:a00-ed5d3f6d-f6a858
next_edges:
  - verdict:a00-ed5d3f6d-grok-seam-verdict
confidence: 0.97
edited_by: a00-ed5d3f6d
evidence_runs:
  - experiment:a00-ed5d3f6d-grok-seam
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 30f8a51cea9fbb26
season: 2
testable_claim: The grok-bot seam is already in the adapters module; the only missing input on this tip is the harnesses.grok-bot row in .agi/config.json, which is out of scope here.
title: "Grok-bot seam measured live: dispatch and shipped adapters clean, row absent, wired row resolves"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ed5d3f6d-grok-seam

## Experiment

Measure the `harnesses.grok-bot` seam on THIS tip (off `core/season2/main`,
merge-base `18b3044cc`), with zero edits to `dispatch.py` and zero edits to
`.agi/config.json`. The claim is that the seam is already in the right place
(the adapters module), the config row is simply absent on this tip, and the
absence is the only thing left for the out-of-scope helper branch
(`season2/loops/goal-g17.14.2-helper-cfg-land`) to land.

Everything cited below is a **tracked file in this repo**:
`extensions/agi/bin/dispatch.py`, `extensions/agi/bin/adapters/__init__.py`,
`extensions/agi/bin/adapters/{pi,claude_code,copilot_cli}_adapter.py`, and
`.agi/config.json`. No `.agi/sessions/**` path is cited as evidence.

### Probe script (run from the repo root)

```
python3 .agi/sessions/iter-DT.18/a00-ed5d3f6d/probe_grok_seam.py
```

The script hard-codes a **negative control**: a scratch file that DOES contain
`grok`, so a zero hit on the real files is a measurement and not a dead
pattern. It then loads `.agi/config.json` through `adapters.resolve` twice —
once with the tip's real config (row absent) and once with an in-memory copy
carrying the row.

## Evidence

Observed output (2026-09-20, this worktree):

```json
{
  "adapter_hits": {
    "claude_code_adapter.py": 0,
    "copilot_cli_adapter.py": 0,
    "pi_adapter.py": 0
  },
  "config_harnesses": ["claude-code", "copilot-cli", "pi", "pi-local"],
  "control_hits": 1,
  "dispatch_hits": 0,
  "resolve_tip": "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']",
  "resolve_wired": {
    "adapter": "grok_bot",
    "models": {"kid": "grok-kid", "parent": "grok-parent"},
    "name": "grok-bot"
  }
}
```

1. **Control live.** `control_hits = 1` — the pattern matches a file known to
   contain `grok`. Zero on the real files therefore means something.
2. **`dispatch.py` clean.** `grep -Ein grok extensions/agi/bin/dispatch.py`
   returns 0 hits. The seam did not leak into the dispatcher.
3. **Shipped adapters clean.** `pi_adapter.py`, `claude_code_adapter.py`,
   `copilot_cli_adapter.py` each return 0 hits. The three shipped harnesses
   are untouched by the grok work.
4. **`resolve` refuses by name on this tip.** `.agi/config.json` declares only
   `['claude-code', 'copilot-cli', 'pi', 'pi-local']`; `adapters.resolve(cfg,
   "grok-bot")` raises `AdapterError` naming `'grok-bot'` and the declared
   set. This is the parent goal's expected pre-row state.
5. **The wire resolves.** The SAME `resolve` on an in-memory config copy with a
   `grok-bot` row returns `("grok-bot", {adapter: grok_bot, models: kid/parent})`.
   No code change is needed for the row to work; the row is the only missing
   input.

### What this does NOT do (out of scope, follow-on)

`.agi/config.json` is hard-excluded from this round (`cli.py:2093`), so the row
is NOT landed here. The gap is owned by the helper branch
`season2/loops/goal-g17.14.2-helper-cfg-land`; if that branch does not reach
the merge target, the follow-on node is **`goal:g17.14.2` route to a config-row
landing step (suggested id `goal:g17.14.4`)** carrying exactly the in-memory
row above into `.agi/config.json`. Documented, not built.

### Historical note (no machine edge)

The earlier attempt at this seam lived on
`season2/loops/goal-g17.14.2-a00-f694a5f1` (`hypothesis:a00-3d540aa5-fa98ee`,
`hypothesis:a00-bfd0d94a-d67716`). Neither id resolves on this tip, and this
node deliberately carries **no** `supersedes:` field and **no** `next_edges`
pointer at them: the reference is prose, not an asserted link.
