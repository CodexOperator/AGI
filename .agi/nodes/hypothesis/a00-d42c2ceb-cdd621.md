---
id: hypothesis:a00-d42c2ceb-cdd621
mint_id: 54ece77a131e441aa403a49496ac9378
type: hypothesis
parents:
  - goal:g7.31.1.1
next_edges: []
confidence: 0.9
edited_by: a00-d42c2ceb
evidence_runs:
  - experiment:a00-0349f27c-grok-measured-argv
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 7d2dcde64f4b3099
season: 2
testable_claim: "Independent-verdict step for `goal:g7.31.1.1`. Claim: on the LANDED bytes of this checkout, `adapters.load(\"grok_bot\").build_command(...)` emits the bare resolved bin with no `-p` and no `--model` (matching the recorded `grok-bot --help`), the stub flags are absent from the adapter path, and the landed test file's `_stat_reader` import-open delegation test exists and is executed."
title: Independent verdict on landed measured grok-bot argv
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d42c2ceb-cdd621

## Hypothesis

Independent-verdict step for `goal:g7.31.1.1`. Claim: on the LANDED bytes of
this checkout, `adapters.load("grok_bot").build_command(...)` emits the bare
resolved bin with no `-p` and no `--model` (matching the recorded
`grok-bot --help`), the stub flags are absent from the adapter path, and the
landed test file's `_stat_reader` import-open delegation test exists and is
executed.

## What would prove it

- `grep -nE '"--model"|"-p"'` over the landed adapter exits 1.
- A live call from the call site returns `['<bin>']`.
- The verbatim `grok-bot --help` re-measurement is 46 lines, exit 0, sha256
  `b0865dd7...`, and names neither flag.
- `pytest extensions/agi/tests/test_grok_bot_adapter.py` is green and the
  `_stat_reader` delegation test fails on a scratch-copy mutation.
- Both committed nodes carry `evidence_runs:` in YAML LIST form (MUR D1).

## What would disprove it

Red if the adapter still contained `-p`/`--model`, if `build_command` emitted
anything but the bare bin, if the delegation test were skipped, or if the
mutation did not make it fail.

## Result

Green, all five checks re-derived independently. `29 passed`; the mutation
`real_open = _REAL_OPEN` -> `builtins.open` on a scratch copy turns the
delegation test red; D1 list form confirmed on both nodes; D2 moot on this
base. Judgement recorded as
`verdict:measured-argv-independent-verdict` (`proved`, 0.90).

## Scope / honesty

No code edits by this run; read-only on the adapter, its test, and
`goal:g7.31.1.1`. Production lines changed = 0. Scratch artifacts live under
`.agi/sessions/iter-DT.98/a00-d42c2ceb/`.

## Agent Notes
Independent verdict on landed measured grok-bot argv: grep exit=1, live build_command=['\''/SENTINEL/grok-bot'\''], --help 46 lines/exit0/sha256 b0865dd7, 29 passed, D3 scratch-copy mutation fails, D1 list-form confirmed; authored verdict:measured-argv-independent-verdict (proved 0.9).
