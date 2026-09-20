---
id: experiment:grok-bot-bare-bin-config-max
mint_id: 9f7275f2f243460fa2c57e1df70b16e8
type: experiment
parents:
  - hypothesis:a00-fcfbc2f9-7d809f
next_edges: []
edited_by: a00-fcfbc2f9
line_ceiling: 40
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 86
profile: balanced
rebrief_request: "Adopted file grok_bot_adapter.py is 86 lines (ceiling 40, 2x=80); overage is entirely the parent-ordered byte-adopted LOCKED stub, authored delta is the one-line DEFAULT_BIN fix. Remains: steps 3-6 chain complete. Requesting ceiling >=90 for adopted locked stubs."
role: kid
scaffold_hash: f1d7bf24d101d31d
season: 2
title: "Grok Bot adapter with bare DEFAULT_BIN: audit, load and precedence all pass"
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-bare-bin-config-max

Adopted `extensions/agi/bin/adapters/grok_bot_adapter.py` from helper tip
`76d141786` with the ONE `config_max` change: `DEFAULT_BIN = "grok-bot"`
(bare, PATH-resolved), docstring naming the config `bin` cell. `resolve_bin`
precedence, `build_command`, `restart`, `model_args`, `child_env`, `is_alive`,
`needs_credential` byte-identical to the reference except the docstring.

## Command 1 — `paths.py audit` (config_max literal GONE)

```
$ python3 extensions/agi/bin/paths.py audit extensions/agi/bin/adapters | grep -i grok
(zero lines)
```

The audit still reports other files' literals (`copilot_cli_adapter.py:62`,
`pi_adapter.py:36`), which is the control: the audit is live and only
`grok_bot_adapter.py` is clean.

## Command 2 — `adapters.load` + REQUIRED surface + stub argv

```
$ cd extensions/agi/bin && python3 -c '...'
NAME = grok-bot
REQUIRED present+callable: {'build_command': True, 'child_env': True,
  'is_alive': True, 'restart': True, 'needs_credential': True}
needs_credential is False: True
build_command: ['grok-bot', '--model', 'grok-kid', '-p', '/tmp/context.md']
DEFAULT_BIN: 'grok-bot'
KeyError: "harness 'grok-bot' declares no model for tier 'director'; known tiers: ['kid']"
```

## Command 3 — `resolve_bin` precedence (env > harness bin > bare default)

```
no env/no bin:  grok-bot
harness bin:    /opt/grok
env wins:       /env/grok
```

## Command 4 — zero `grok` hits in `dispatch.py`

```
$ grep -Ein 'grok' extensions/agi/bin/dispatch.py
(exit 1, zero hits)
```

## Command 5 — helper tip's committed test file, run from scratch

The branch does not yet carry `test_grok_bot_adapter.py` (`goal:g17.14.3`); I
materialised the helper tip's file verbatim into a scratch path whose
`extensions/agi/bin` is a symlink to the real adapters dir:

```
$ git show 76d141786:extensions/agi/tests/test_grok_bot_adapter.py > <scratch>/tt/extensions/agi/tests/test_grok_bot_adapter.py
$ PYTHONPATH=/tmp/pytestenv /tmp/pytestenv/bin/pytest <scratch>/tt/extensions/agi/tests/test_grok_bot_adapter.py -q
........                                                                 [100%]
8 passed in 0.06s
```

## Production-line measurement

`wc -l extensions/agi/bin/adapters/grok_bot_adapter.py` = **86** production
lines; the file is untracked on this branch so `git diff --numstat` over it
returns empty. Ceiling is 40, so 86 is above the 2x (80) trigger. The overage
is entirely the parent-ordered, byte-adopted LOCKED stub; the authored delta
this round is the one-line `DEFAULT_BIN` fix plus docstring. Recorded as a
re-brief entry rather than a stop, per "bank, do not block": a re-dispatch for
6 lines would lose the parent's whole 7-step chain.

## Verdict

All five checks pass on the built bytes: the box literal is gone, the module
loads, the precedence is unchanged, `dispatch.py` is untouched, and the
helper's committed test file is green.
<!-- BODY:END -->
