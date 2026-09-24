---
id: experiment:a00-feeb98c4-probe
mint_id: a00feeb98c4probe
type: experiment
parents:
  - hypothesis:a00-feeb98c4-d0be8f
next_edges: []
confidence: 0.1
edited_by: a00-feeb98c4
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
