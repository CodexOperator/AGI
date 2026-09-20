---
id: verdict:a00-61bd9edf-grok-seam-verdict
mint_id: 7c9ac39871d7463b9062b787d54d1a07
type: verdict
parents:
  - experiment:a00-61bd9edf-grok-seam
next_edges: []
confidence: 0.97
edited_by: a00-61bd9edf
evidence_runs:
  - experiment:a00-61bd9edf-grok-seam
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: b2a2cb4f9b6f588a
season: 2
title: "Grok-bot seam corrected verdict: prior only-the-row claim disproved; adapter module is the first blocker"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-61bd9edf-grok-seam-verdict

## Verdict

**proved** (confidence 0.97) — for the **corrected** claim in
`hypothesis:a00-61bd9edf-9999f8`: the grok-bot seam requires the adapter MODULE
and the config row, and on this tip the module is the first blocker.

**disproved** — for the PRIOR claim "the seam already lives in the adapters
module; only the config row is absent". Measured on tip `18b3044cc`,
`extensions/agi/bin/adapters/grok_bot_adapter.py` is absent, so
`adapters.load("grok_bot")` fails with an `AdapterError` naming the missing
file. The row alone would not complete the seam.

## Evidence

Backing run: `experiment:a00-61bd9edf-grok-seam`.

- **gate** — `adapters.load("grok_bot")` on this tip raises `AdapterError: no
  adapter for harness 'grok_bot': expected .../extensions/agi/bin/adapters/grok_bot_adapter.py`.
- **auth** — `adapters.resolve(cfg, "grok-bot")` on `.agi/config.json` raises
  `AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']`.
- **wire** — with the canonical adapter blob (sha256
  `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`, 162 lines,
  from `e554c440c`) present for a COPY of the package, `load("grok_bot")`
  succeeds and all five `adapters.REQUIRED` names are callable, while
  `resolve` still refuses by name (row absent). So the config row is the sole
  remaining gap once the adapter lands.

One fixture only, everywhere: `bin: /home/ubuntu/.npm-global/bin/grok-bot`,
`models: {kid: grok-4-fast, parent: grok-4}`.

## Confidence

0.97. Each conjunct has a direct, reproducible observation; the wire conjunct
is proven against the canonical blob, not against tree state. Not 1.0 because
the adapter blob is not landed in the tree (out of scope, 162 production lines
> 80 ceiling), so the end-to-end `load` on a fresh checkout still fails.

## Named gaps (not built)

- Adapter module landing — `goal:g17.14.4`.
- Config row fold in `.agi/config.json` (Prime/director-owned) — `goal:g17.14.4`.

A fresh checkout still fails `resolve` until both land.
