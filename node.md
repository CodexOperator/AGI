---
id: experiment:dt2-grok-bot-env-bin-1004
mint_id: fae0cd7d44014f76ab35184f1a5118ed
type: experiment
parents:
  - hypothesis:grok-bot-env-bin-overrides-missing-cell
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-grok-bot-env-bin-1004
line_ceiling: 0
model: grok-4.6
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "GROK_BOT_BIN=grok-bot resolve_bin(live row); build_command(tier=kid, rendered_brief=hello)", "expected": "bin grok-bot; argv [grok-bot, --model, grok-4-fast, -p, hello]", "observed": "grok-bot ; ['grok-bot', '--model', 'grok-4-fast', '-p', 'hello']", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "GROK_BOT_BIN=/usr/local/bin/grok-bot resolve_bin(live row)", "expected": "that absolute path", "observed": "/usr/local/bin/grok-bot", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "GROK_BOT_BIN=/no/such/grok-bot resolve_bin(live row)", "expected": "FileNotFoundError naming harness, path, $GROK_BOT_BIN", "observed": "FileNotFoundError: harness 'grok_bot': cannot resolve binary '/no/such/grok-bot': does not exist; set $GROK_BOT_BIN to override", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "unset GROK_BOT_BIN; resolve_bin(live row)", "expected": "FileNotFoundError on ~/.npm-global/bin/grok-bot", "observed": "FileNotFoundError: harness 'grok_bot': cannot resolve binary '~/.npm-global/bin/grok-bot': expanded to <home>/.npm-global/bin/grok-bot, which does not exist; set $GROK_BOT_BIN to override", "result": "pass"}
production_lines: 0
role: director
season: 2
title: "$GROK_BOT_BIN overrides the missing live grok-bot bin cell; unset env still fails C3"
town: core
verdict: proved
---
# experiment:dt2-grok-bot-env-bin-1004

**Headline / Verdict: PROVED.** C1–C4 all pass. The documented `$GROK_BOT_BIN` override starts a resolving `build_command` without a config write. Unset env still dies on the live cell.

## Experiment

**Claim (hypothesis:grok-bot-env-bin-overrides-missing-cell).** C1 PATH name. C2 existing absolute. C3 missing absolute refuses by name. C4 unset env still the live-cell FileNotFoundError.

**Dispatch line answered first.** config-max: none. code: none. No write to `.agi/config.json` or `grok_bot_adapter.py`.

**Commands** (this uid, encryption-town, 17:27Z 10-04 date -u):
- `python3 -c` adapters.load / resolve / grok_bot_adapter.resolve_bin / build_command / model_args / is_alive / needs_credential under four env states
- `box n` empty; live `harnesses.grok-bot.bin` still `~/.npm-global/bin/grok-bot`

## Results

| conjunct | result | number |
|---|---|---|
| C1 `GROK_BOT_BIN=grok-bot` | pass | resolve `grok-bot`; argv `--model grok-4-fast -p hello` |
| C2 existing absolute | pass | `/usr/local/bin/grok-bot` |
| C3 missing absolute | pass | FileNotFoundError names harness + path + `$GROK_BOT_BIN` |
| C4 unset env (regression) | pass | same npm-global FileNotFoundError as 16:50Z |

Helpers (not conjuncts): `is_alive(self)` True; `is_alive(1)` False; `needs_credential` False; `restart` callable; missing-tier `model_args` KeyError by name; both-empty `build_command` ValueError by name; `child_env` drops `OPENROUTER_API_KEY`; dispatch.py grok hits = 0.

Not void: load and resolve of the row succeed.

## Deviations
- Did not spawn a billed grok turn (ceiling). `restart` callable only.
- pytest absent this uid; no test file.

## Re-probe 00:42Z 10-05 (date -u)
After merge `a350709a8` (et `6ae27d46c` grok provider arm). `box n` empty. `GROK_BOT_BIN` unset. Live cell still `~/.npm-global/bin/grok-bot`. C4 still FileNotFoundError (same named refuse). Adapter/config bytes vs `25d915620`: no diff. Did not write the cell.

## Re-probe 04:56Z 10-05 (date -u)
After merge `f8f7c4cf2` (et `e2bc6ff50` DG2 Y2/Y3.6). `box n` empty. `$GROK_BOT_BIN` unset. Live cell still `~/.npm-global/bin/grok-bot`. C3/C4 still FileNotFoundError. No new hyp. Did not write the cell. Did not implement mint.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 04:56Z 10-05: owner go. box n empty, C3 still FileNotFoundError after DG2 land. Recorded re-probe, no second top (trap idle-fill). Did not write the cell. Did not implement mint.
<!-- THOUGHT:END -->
