---
id: experiment:a00-feeb98c4-probe
mint_id: a00feeb98c4probe
type: experiment
parents:
  - hypothesis:a00-feeb98c4-d0be8f
next_edges: []
confidence: 0.1
edited_by: a00-0ae2a917
evidence_runs:
  - experiment:a00-feeb98c4-probe
loop: goal:g7.31.1.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
title: Grok-bot help unavailable; adapter remains stub-shaped
town: core
verdict: pending
---
# experiment:a00-feeb98c4-probe

## Experiment

Measured the real configured harness path and the adapter's emitted argv.

- Live `.agi/config.json` declares `harnesses.grok-bot.bin` as
  `/home/ubuntu/.npm-global/bin/grok-bot`.
- That path is not executable/present in this checkout, so
  `/home/ubuntu/.npm-global/bin/grok-bot --help` cannot be obtained.
- `adapters.load("grok_bot").build_command(...)` on the live-shaped row emits
  `[/home/ubuntu/.npm-global/bin/grok-bot, --model, grok-4-fast, -p, /tmp/context.md]`.
- `python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` passed: 15 tests.

## Result

The central measured-help conjunct is unproven: the binary/help transcript is unavailable. The current `-p` is visibly the old stub and must not be retired without a real help measurement. No production bytes were changed.

## Agent Notes
Measured live config and adapter argv, but configured grok-bot executable/help is absent, so measured-CLI claim cannot be proved or disproved; adapter tests pass 15.

Parent review: Instruction said review bytes and run one negative probe per claim conjunct. Machine check at .agi/config.json:114-120 resolves /home/ubuntu/.npm-global/bin/grok-bot; a direct --help probe raises FileNotFoundError, while adapters.load("grok_bot").build_command(...) at extensions/agi/bin/adapters/grok_bot_adapter.py:60-66 returns [bin, --model, grok-4-fast, -p, /tmp/context.md]. Thus help/flag compatibility and stub retirement remain unproved; accept the kid as a pending measurement, not as proof. probes: gate: configured executable absent, help probe refused by FileNotFoundError; wire: build_command still emits -p and reaches the stub-shaped argv.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to judge the kid adversarially, not trust its passing tests. The machine instead shows the configured executable is absent and build_command still contains the old -p flag. The near miss is treating the 15 passing adapter tests as help measurement; they exercise a shape, not the real CLI. I therefore retain the experiment as pending and record the two named negative probes, with no production change.
<!-- THOUGHT:END -->
