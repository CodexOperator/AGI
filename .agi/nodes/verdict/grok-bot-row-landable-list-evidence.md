---
id: verdict:grok-bot-row-landable-list-evidence
mint_id: cff1079963cb495a8c392c4434cd4c4a
type: verdict
parents:
  - experiment:grok-bot-config-row-resolves-live
next_edges: []
confidence: 0.95
edited_by: a00-89094f2f
evidence_runs:
  - experiment:grok-bot-config-row-resolves-live
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "probe": "E1/E3 resolve with row inserted and with adapter deleted", "observed": "adapter=grok_bot both times; bin matches parent row", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "probe": "E4 dispatch.py grok-free; verdict evidence_runs is a list", "observed": "grep exit 1 no output; this node carries evidence_runs as a YAML list and probes as a list", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "probe": "E5 real cfg without row raises, with row resolves, config byte-identical", "observed": "AdapterError naming declared harnesses; git status for .agi/config.json empty", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 19133a20d704bf0d
season: 2
title: "Grok-bot row proved: resolve cell lands live while dispatch.py and config stay untouched"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-row-landable-list-evidence

## Verdict

proved

## Evidence

`experiment:grok-bot-config-row-resolves-live` ran the five conjunct probes
live against the loaded `.agi/config.json`. All ten probe checks passed:

- **AUTH (conjunct 1):** with the parent-supplied row inserted in memory,
  `resolve(cfg, "grok-bot")` returns `("grok-bot", row)` with
  `adapter == "grok_bot"` and `bin ==
  /home/ubuntu/.npm-global/bin/grok-bot`. With `adapter` deleted, the
  dash→underscore default still yields `grok_bot`. The row is the cell
  `resolve` reads, not a decoration.
- **GATE (conjunct 2):** this verdict carries `evidence_runs` as a YAML
  LIST of node ids and `probes` as a real list of per-conjunct dicts. That
  is the exact shape the MUR defect lacked (scalar `evidence_runs` +
  uncommitted harness row). The gate conjunct also holds at the code level:
  E4 shows `dispatch.py` is grok-free, so no round commit may carry the
  row through the engine path.
- **WIRE (conjunct 3):** on the REAL config without the row, `resolve`
  raises `AdapterError: no harness 'grok-bot' in config; declared:
  ['claude-code', 'copilot-cli', 'pi', 'pi-local']`; inserting the row
  resolves it. `git status --porcelain -- .agi/config.json` is empty, so
  the landing must come from a director-owned commit; any merge-up that
  discards the row re-breaks the name.

No code changed. Zero edits to `extensions/agi/bin/dispatch.py`, zero edits
to any adapter file, and `.agi/config.json` is byte-identical to HEAD.

## Confidence

0.95 — the five probes are direct, live, and each has a named falsifier;
the residual 0.05 is that the row's canonical landing on the helper branch
is verified by the parent's merge/land probe, not re-run here (git is
forbidden to this kid).
