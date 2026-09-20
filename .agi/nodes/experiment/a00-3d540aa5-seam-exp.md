---
id: experiment:a00-3d540aa5-seam-exp
mint_id: 1350a8954a8e448bb6edd58d70839ea3
type: experiment
parents:
  - hypothesis:a00-3d540aa5-fa98ee
next_edges: []
edited_by: a00-3d540aa5
line_ceiling: 40
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
season: 2
title: "live seam measurement in the a00-f694a5f1 worktree: zero grok hits in dispatch.py and the three shipped adapters, grok-bot row absent from this branch"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-3d540aa5-seam-exp

## Experiment

Live measurement in this worktree (`a00-f694a5f1`, base `core/season2/main`)
of the three conjuncts of `hypothesis:a00-3d540aa5-fa98ee`, plus a negative
control proving the grep is live. No file outside `.agi/nodes/**` changed.

### C1 — grok literal in the shared dispatch path

    $ grep -Ein grok extensions/agi/bin/dispatch.py
    (no output)
    exit=1

Zero hits, 0 lines.

### C2 — grok literal in the three shipped adapters

    $ grep -Ein grok extensions/agi/bin/adapters/pi_adapter.py \
        extensions/agi/bin/adapters/claude_code_adapter.py \
        extensions/agi/bin/adapters/copilot_cli_adapter.py
    (no output)
    exit=1

Zero hits, 0 lines.

### C3 — the config row (the deliverable, measured, NOT asserted as a seam condition)

    $ python3 -c 'load .agi/config.json; adapters.resolve(cfg,"grok-bot")'
    json valid
    harness keys: ['claude-code', 'copilot-cli', 'pi', 'pi-local']
    grok-bot row: null
    resolve grok-bot: RAISED AdapterError
      no harness 'grok-bot' in config; declared:
      ['claude-code', 'copilot-cli', 'pi', 'pi-local']

The row is ABSENT on this branch. Per the hypothesis this is a fact about
this branch, not a seam failure. `adapters.resolve` refuses **by name** with
the existing `AdapterError` shape (`adapters/__init__.py` `resolve`), which is
the closed-not-silent behaviour the seam requires.

For comparison, the shipped adapters expose `DEFAULT_BIN`:

    pi_adapter            DEFAULT_BIN=/home/ubuntu/.npm-global/bin/pi
    claude_code_adapter   DEFAULT_BIN=claude
    copilot_cli_adapter   DEFAULT_BIN=/home/ubuntu/.npm-global/bin/copilot

so the well-formedness check for a future `harnesses.grok-bot` row is
mechanical: `adapter == "grok_bot"`, `bin ==`
`/home/ubuntu/.npm-global/bin/grok-bot`.

### Negative control — the grep is live

The same grep against a file known to contain the token DOES hit, so the zero
hits above are a measurement and not a dead pattern:

    $ grep -Ein grok .agi/nodes/goal/g17.14.2.md
    20:  - grok-bot
    23:title: "G17.14.2: harnesses.grok-bot config row only (no dispatch.py edit)"
    30:...grok-bot...
    exit=0

### RECORD

    C1 dispatch.py                        0 lines  exit 1
    C2 three shipped adapters             0 lines  exit 1
    C3 .agi/config.json grok-bot row      absent; resolve raises AdapterError by name
    NC control (goal:g17.14.2.md)         3 lines  exit 0

Raw transcript of the run is saved to
`.agi/sessions/iter-DT.15/a00-3d540aa5/measure.txt` (scratch, not graph).

## Agent Notes
Live seam measurement: 0 grok hits in dispatch.py (exit 1) and in the three shipped adapters (exit 1); harnesses.grok-bot absent from this branch's config (declared: claude-code, copilot-cli, pi, pi-local) and adapters.resolve raises AdapterError by name; negative control against goal:g17.14.2.md hits 3 lines (exit 0), so the zero is live.
