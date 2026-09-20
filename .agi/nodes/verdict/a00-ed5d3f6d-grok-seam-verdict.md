---
id: verdict:a00-ed5d3f6d-grok-seam-verdict
mint_id: fc880f318e3a4fa4bdfe4167617adacd
type: verdict
parents:
  - experiment:a00-ed5d3f6d-grok-seam
next_edges: []
confidence: 0.95
edited_by: a00-ed5d3f6d
evidence_runs:
  - experiment:a00-ed5d3f6d-grok-seam
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -Ein grok extensions/agi/bin/dispatch.py (control: scratch file containing grok)", "expected": "0 hits vs control >= 1", "observed": "0 hits; control=1", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -Ein grok on pi_adapter.py, claude_code_adapter.py, copilot_cli_adapter.py", "expected": "0 hits each", "observed": "0/0/0", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "adapters.resolve(cfg, grok-bot) on .agi/config.json", "expected": "AdapterError naming grok-bot", "observed": "AdapterError naming grok-bot; declared claude-code/copilot-cli/pi/pi-local", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "adapters.resolve(cfg_copy_with_row, grok-bot)", "expected": "resolves to (grok-bot, adapter=grok_bot)", "observed": "resolved; adapter=grok_bot", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 3cbd63e6222de421
season: 2
title: "Grok-bot seam proved: dispatch and shipped adapters clean, resolve refuses by name, wired row resolves"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-ed5d3f6d-grok-seam-verdict

## Verdict

**proved** (confidence 0.95). All four numbered claim conjuncts of
`hypothesis:a00-ed5d3f6d-f6a858` hold on this tip, measured live by
`experiment:a00-ed5d3f6d-grok-seam`.

## Evidence

Every citation names a **committed in-tree file**; no `.agi/sessions/**` path
is offered as evidence.

- **CLAIM (1) — `extensions/agi/bin/dispatch.py` clean.** `grep -Ein grok`
  returns 0 hits, while the scratch **control** file constructed by the probe
  returns 1. Zero is therefore a live measurement, not a dead pattern.
- **CLAIM (2) — shipped adapters clean.** `pi_adapter.py`,
  `claude_code_adapter.py`, `copilot_cli_adapter.py` (all under
  `extensions/agi/bin/adapters/`) each return 0 `grok` hits.
- **CLAIM (3) — refuses by name.** `.agi/config.json` declares only
  `['claude-code', 'copilot-cli', 'pi', 'pi-local']`;
  `adapters.resolve(cfg, "grok-bot")` (reader:
  `extensions/agi/bin/adapters/__init__.py`) raises the existing
  `AdapterError` naming `grok-bot` and the declared set.
- **CLAIM (4) — the wire resolves.** The same `resolve` on an in-memory write
  of the config carrying a `grok-bot` row ({adapter: `grok_bot`, models:
  kid/parent}) returns `("grok-bot", {adapter: "grok_bot", models: {...}})`.
  No code change is required for the row to work.

**Reader named for the field, not the wrong one.** No `supersedes:` field is
used anywhere in this chain, so no supersedes claim is made. Link resolution
for this chain is carried only by `parents` (`hypothesis -> experiment ->
verdict`) and `evidence_runs`, the two fields `links.py` actually reads — and
neither names an id absent from this tip.

## Confidence

0.95. High: each conjunct has a direct, reproducible observation with a live
negative control. Not 1.0 because the four probes establish the *seam*, not
the end-to-end spawn a landed config row would exercise; that is the
out-of-scope follow-on.

## Out of scope (inherited gap, follow-on)

`.agi/config.json` is hard-excluded from this round (`cli.py` prohibits
writing it), so the row is not landed here. Owner: helper branch
`season2/loops/goal-g17.14.2-helper-cfg-land`; follow-on node under
`goal:g17.14.2` — suggested `goal:g17.14.4`, landing exactly the in-memory row
above into `.agi/config.json` and re-running probe (4) end-to-end.
