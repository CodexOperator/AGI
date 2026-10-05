---
id: experiment:dt2-grok-bot-restart-none-1005
mint_id: 1cbfa04059a143dc8115930bb230c706
type: experiment
parents:
  - hypothesis:grok-bot-restart-degrades-to-none
next_edges: []
confidence: 0.9
edited_by: director-thought-2
evidence_runs:
  - experiment:dt2-grok-bot-restart-none-1005
line_ceiling: 0
model: grok-4.6
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "restart(live row, rendered_brief=hello) unset GROK_BOT_BIN", "expected": "None; no raise; no output.log", "observed": "None; stderr FileNotFoundError named; sess listing empty", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "restart(bin=grok-bot, rendered_brief=None, context_file='')", "expected": "None; no raise; no child", "observed": "None; stderr ValueError empty prompt; sess listing empty", "result": "pass"}
production_lines: 0
role: director
season: 2
title: grok-bot restart returns None on missing bin and on empty prompt; no child
town: core
verdict: proved
---
# experiment:dt2-grok-bot-restart-none-1005

**Headline / Verdict: PROVED.** C1 and C2 both return None. No child. No billed spawn.

## Experiment

**Claim (hypothesis:grok-bot-restart-degrades-to-none).** C1 missing live bin. C2 empty prompt with PATH bin.

**Dispatch line answered first.** config-max: none. code: none.

**Commands** (this uid, encryption-town, 04:54Z 10-05 date -u):
- in-process `grok_bot_adapter.restart` against a tmp sess_dir
- live row bin `~/.npm-global/bin/grok-bot` still missing
- synthetic harness `bin=grok-bot` for C2

## Results

| conjunct | result | number |
|---|---|---|
| C1 missing bin | pass | return None; FileNotFoundError printed; sess empty |
| C2 empty prompt | pass | return None; ValueError printed; sess empty |

stderr (named, not a traceback through the caller):
- C1 `restart failed for dt2-probe: harness 'grok_bot': cannot resolve binary '~/.npm-global/bin/grok-bot'…`
- C2 `restart failed for dt2-probe: grok-bot: rendered_brief and context_file are both empty…`

Not void: `adapters.load("grok_bot")` succeeds. dispatch.py grok hits = 0. `is_alive(self)` True.

## Deviations
- Did not spawn a billed grok turn (ceiling). Happy-path restart (live pid) unmeasured — still blocked on the bin cell.
- pytest absent this uid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 04:54Z 10-05: measurement-only. Two degrade arms of restart. Did not write the cell. Did not implement mint.
<!-- THOUGHT:END -->
