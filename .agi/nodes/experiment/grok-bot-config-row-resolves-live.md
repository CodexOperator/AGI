---
id: experiment:grok-bot-config-row-resolves-live
mint_id: ff6dff3e804c40b6b25074d1c13177c8
type: experiment
parents:
  - hypothesis:a00-89094f2f-940a6c
next_edges: []
confidence: 0.95
edited_by: a00-89094f2f
evidence_runs:
  - experiment:grok-bot-config-row-resolves-live
line_ceiling: 40
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "probe": "resolve(cfg,grok-bot) with row inserted in memory", "observed": "(grok-bot, adapter=grok_bot, bin=/home/ubuntu/.npm-global/bin/grok-bot)", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "probe": "resolve on deep copy with row[adapter] deleted (dash default)", "observed": "adapter=grok_bot", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "probe": "resolve peers pi, pi-local, claude-code, copilot-cli on live cfg", "observed": "pi->pi, pi-local->pi, claude-code->claude_code, copilot-cli->copilot_cli; no raise", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "probe": "grep -Ein grok extensions/agi/bin/dispatch.py", "observed": "exit 1, no output; evidence_runs and probes are lists not scalars", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "probe": "resolve(real loaded cfg,grok-bot) without the row", "observed": "AdapterError: no harness grok-bot in config; declared [claude-code, copilot-cli, pi, pi-local]; with the row it resolves; git status --porcelain .agi/config.json empty", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 979442d907d5ff10
season: 2
title: "Five live probes: grok-bot config row resolves in memory and dispatch stays untouched"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-config-row-resolves-live

## Experiment

Live probe of the parent-supplied `harnesses."grok-bot"` row against the
LIVE `.agi/config.json`, loaded in memory and never written back. Script:
`.agi/sessions/iter-DT.09/a00-89094f2f/probe_e1_e5.py`; raw output saved to
`probe_results.json` in the same session dir. Command:

    python3 .agi/sessions/iter-DT.09/a00-89094f2f/probe_e1_e5.py

No adapter file is created (owned by `goal:g17.14.1`) and `dispatch.py` is
not touched. `resolve` reads only config, so the test is honest about the
cell under test.

### E1 — resolve returns the row (AUTH)

PASS. `resolve(withrow, "grok-bot")` →
`("grok-bot", {"adapter": "grok_bot", "bin":
"/home/ubuntu/.npm-global/bin/grok-bot", ...})`. Both `row["adapter"] ==
"grok_bot"` and `row["bin"]` equal the parent-supplied values.

### E2 — peers intact

PASS. On the live cfg: `pi`→adapter `pi`, `pi-local`→`pi`,
`claude-code`→`claude_code`, `copilot-cli`→`copilot_cli`. None raised.

### E3 — dash-default on adapter-less deep copy

PASS. Deep copy of cfg with `row["adapter"]` deleted still resolves to
`adapter == "grok_bot"` — `grok-bot`.replace("-","_") is the default.

### E4 — dispatch.py gate

PASS. `grep -Ein 'grok' extensions/agi/bin/dispatch.py` → exit 1, no output.

### E5 — wire / real config

PASS. On the REAL loaded cfg WITHOUT the row: `AdapterError: no harness
'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi',
'pi-local']`. With the row inserted it resolves. `json.load(open(
".agi/config.json"))` succeeds, and `git status --porcelain --
.agi/config.json` is empty — the row was never written to disk.

### Result

ALL PASS (10/10 probe checks). The row is the load-bearing cell `resolve`
reads; the name does not resolve without it; `dispatch.py` and the config
file are both untouched.

## Evidence

```json
{
  "E5_norow": ["pass", "no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']"],
  "E1": ["pass", {"name": "grok-bot", "adapter": "grok_bot", "bin": "/home/ubuntu/.npm-global/bin/grok-bot"}],
  "E5_withrow": ["pass", {"name": "grok-bot", "adapter": "grok_bot"}],
  "E2_pi": ["pass", {"name": "pi", "adapter": "pi"}],
  "E2_pi-local": ["pass", {"name": "pi-local", "adapter": "pi"}],
  "E2_claude-code": ["pass", {"name": "claude-code", "adapter": "claude_code"}],
  "E2_copilot-cli": ["pass", {"name": "copilot-cli", "adapter": "copilot_cli"}],
  "E3_dash_default": ["pass", {"name": "grok-bot", "adapter": "grok_bot"}],
  "E5_git_clean": ["pass", ""],
  "E4_gate": ["pass", "rc=1"]
}
```

`ALL_PASS`.

## Agent Notes
Grok-bot config row is a first-class resolve cell: E1-E5 all pass live (row inserted in memory resolves to adapter grok_bot; peers intact; dash-default holds; dispatch.py grok-free; real cfg raises without row and resolves with it; .agi/config.json byte-identical, production_lines 0). Verdict node verdict:grok-bot-row-landable-list-evidence carries evidence_runs as a YAML list and per-conjunct probe dicts.
