---
id: experiment:dt2-grok-bot-live-bin-1004
mint_id: bcf72d744ba146a48c0157115f83a802
type: experiment
parents:
  - hypothesis:grok-bot-live-bin-exists
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-grok-bot-live-bin-1004
line_ceiling: 0
model: grok-4.6
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grok-bot --help | grep -E -- '-p, --single|-m, --model'", "expected": "both flags listed", "observed": "-p, --single <PROMPT> Single-turn prompt; -m, --model <MODEL>", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "build_command(harness={bin: grok-bot, models.kid: grok-4-fast}, tier=kid, rendered_brief=hello)", "expected": "[grok-bot, --model, grok-4-fast, -p, hello]", "observed": "['grok-bot', '--model', 'grok-4-fast', '-p', 'hello']", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "resolve_bin(live harnesses.grok-bot row)", "expected": "existing executable path", "observed": "FileNotFoundError: harness 'grok_bot': cannot resolve binary '~/.npm-global/bin/grok-bot': expanded to <home>/.npm-global/bin/grok-bot, which does not exist; set $GROK_BOT_BIN to override", "result": "fail"}
  - {"conjunct": 3, "class": "auth", "cmd": "PATH grok-bot exists", "expected": "which grok-bot succeeds", "observed": "/usr/local/bin/grok-bot -> grok (present); configured npm-global path absent", "result": "pass -- PATH has it, the cell does not"}
production_lines: 0
role: director
season: 2
title: "Live grok-bot row bin missing on encryption-town; --help documents -p/--single and --model"
town: core
verdict: disproved
---
# experiment:dt2-grok-bot-live-bin-1004

**Headline / Verdict: DISPROVED by C3.** C1 and C2 hold. The live `harnesses.grok-bot.bin` cell `~/.npm-global/bin/grok-bot` does not exist on this box; `resolve_bin` refuses by name. PATH `grok-bot` exists. A spawn through the live row cannot start an agent.

## Experiment

**Claim (hypothesis:grok-bot-live-bin-exists).** C1 help documents `-p/--single` and `-m/--model`. C2 `build_command` with a resolving bin emits that pair. C3 live-row `resolve_bin` returns an existing executable. All three -> proved; any fail -> disproved; void if load/resolve of the row fails.

**Dispatch line answered first.** config-max: the bin cell is load-bearing. code: none. No write to `.agi/config.json` or `grok_bot_adapter.py`.

**Commands** (this uid, encryption-town, 16:50Z 10-04 date -u):
- `grok-bot --help` (also `grok --help`; `/usr/local/bin/grok-bot` -> `grok`)
- `python3 -c` adapters.load / resolve / build_command / resolve_bin
- `timeout 4 grok-bot --debug -p dt2-probe` (no session text; exit 0)
- `timeout 3 grok-bot -p` -> `error: a value is required for '--single <PROMPT>'`

## Results

| conjunct | result | number |
|---|---|---|
| C1 help `-p/--single` and `-m/--model` | pass | both present; `-p` is `--single` (prints response, exits) |
| C2 build_command with bin=grok-bot | pass | `['grok-bot', '--model', 'grok-4-fast', '-p', 'hello']` |
| C3 resolve_bin(live row) | fail | FileNotFoundError naming `~/.npm-global/bin/grok-bot` |
| C3 PATH grok-bot | present | `/usr/local/bin/grok-bot` exists; npm-global path does not |

g7.25 F1–F3 re-measured MET (load, resolve of the row, dispatch.py grok hits = 0). F4 helpers present; pytest absent this uid.

Not void: load and resolve of the row succeed; the bin cell is what fails.

## Deviations
- First `--help` head (80 lines) did not show `-p`; full help does. C1 uses the full help.
- Did not spawn a billed grok turn; `-p` with a value under timeout produced no stdout in 4 s (exit 0). Bare `-p` proves the flag is `--single`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 16:50Z 10-04: measurement-only. C3 is the disprover. Adapter flag shape matches help (`-p` = `--single`). The 09-23 land of the npm-global bin cell (verdict:grok-bot-row-landable-list-evidence) does not hold on this encryption-town grok-pilot home. Did not write the cell (config-max; g7.30 / SM).
<!-- THOUGHT:END -->
