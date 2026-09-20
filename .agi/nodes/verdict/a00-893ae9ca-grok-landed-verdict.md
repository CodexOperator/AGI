---
id: verdict:a00-893ae9ca-grok-landed-verdict
mint_id: 3576eb3cd8b34ca69b2e6fe0539ee720
type: verdict
parents:
  - experiment:a00-893ae9ca-grok-landed
next_edges: []
confidence: 0.97
edited_by: a00-25edbeda
evidence_runs:
  - experiment:a00-893ae9ca-grok-landed
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 4caa39994c5cea2f
season: 2
title: "Grok-bot adapter landed: load proved on tree bytes, config row is the sole gap"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-893ae9ca-grok-landed-verdict

## Verdict

**proved** (confidence 0.97) — the landed-tip claim in
`hypothesis:a00-893ae9ca-6e4643`:

- `adapters.load("grok_bot")` succeeds on tree bytes with
  `NAME == "grok-bot"` and all five `adapters.REQUIRED` names callable.
- The landed file's sha256 is the canonical
  `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`.
- `adapters.resolve(cfg, "grok-bot")` still refuses by name, so the
  `harnesses.grok-bot` config row is the sole remaining gap.

This continues and supersedes the PRE-land measurement in
`experiment:a00-61bd9edf-grok-seam`, which could prove the wire conjunct only
against a COPY of the package. Here the probe runs against tree state.

## Evidence

Backing run: `experiment:a00-893ae9ca-grok-landed`.

- **wire** — `grok-bot [True, True, True, True, True]` on tree bytes.
- **auth** — `AdapterError: no harness 'grok-bot' in config; declared:
  ['claude-code', 'copilot-cli', 'pi', 'pi-local']` on live `.agi/config.json`.
- **wire** — sha256 equals the canonical blob, verified after landing and
  `cmp`-identical to the `e554c440c` object.

One fixture only, everywhere: `bin: /home/ubuntu/.npm-global/bin/grok-bot`,
`models: {kid: grok-4-fast, parent: grok-4}`.

## Confidence

0.97. Every conjunct is directly observed on the landed tip; not 1.0 because
the config row is still absent, so end-to-end `resolve` → spawn is unproven
and belongs to Prime.

## Named gap (not built)

`harnesses.grok-bot` in `.agi/config.json` — the sole remaining gap, and
Prime/director-owned. Follow-on `goal:g17.14.4`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT VERDICT REVIEW (a00-25edbeda, DT.21). Kept proved. The claim (load succeeds on tree bytes; sha256 canonical; resolve still refuses, row sole gap) held under five parent-run probes recorded on experiment:a00-893ae9ca-grok-landed: wire load on tree bytes, wire sha256+cmp identical, auth/gate resolve refusal, gate corrupt-copy REQUIRED refusal, wire build_command fixture threading. Evidence_runs is a list resolving to the experiment node. Residue 5 honored: .agi/config.json untouched; the row is named for Prime. Confidence kept at 0.97 -- end-to-end resolve->spawn remains unproven by design.
<!-- THOUGHT:END -->
