---
id: experiment:a00-5cb90957-grok-help-argv
mint_id: a005cb90957b0862b5cb90957000001
type: experiment
parents:
  - goal:g7.31.1.1
next_edges: []
edited_by: a00-5cb90957
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: stealth/space-bunny-alpha
production_lines: 29
profile: balanced
role: kid
season: 2
title: Recorded grok-bot 0.3.1 help removes guessed prompt and model argv
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5cb90957-grok-help-argv

## Claim tested

`grok-bot-cli@0.3.1` is the published CLI named by the configured adapter, and its measured help has neither the adapter's guessed lone `-p` prompt flag nor `--model`. Therefore `build_command` can retire those guessed flags while retaining tier validation and the common adapter signature.

## Measurement

In the session scratch directory, fetched the package tarball and ran the CLI's own entry point:

```
$ npm pack grok-bot-cli@0.3.1
grok-bot-cli-0.3.1.tgz
$ tar -xzf grok-bot-cli-0.3.1.tgz -C package
$ node package/package/src/cli.js --help > help.txt
rc=0
$ wc -l help.txt
46 help.txt
$ sha256sum help.txt
b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1  help.txt
$ grep -nE '(^| )-p( |$)|--model' help.txt
grep_rc=1
```

The recorded help identifies `gbot` as a management CLI (`bots`, `groups`, `send`, `history`, `codex`), not a headless prompt runner. The 46-line measurement is checked into `extensions/agi/tests/fixtures/grok_bot_cli_0_3_1_help.txt`; `cmp` against the scratch capture exits 0 and both SHA-256 values are identical.

## Built bytes

- `extensions/agi/bin/adapters/grok_bot_adapter.py`: `build_command` now validates the configured tier but returns only the resolved bin. The guessed `-p` and `--model` emissions are gone.
- `extensions/agi/tests/test_grok_bot_adapter.py`: checks the fixture's 46 lines and absent guessed flags, then requires exact bare argv.
- `extensions/agi/tests/fixtures/grok_bot_cli_0_3_1_help.txt`: verbatim measured help.

No `dispatch.py`, `rotate.py`, tmux, or restart seam was edited.

## Tests and negative probe

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
................                                                         [100%]
16 passed in 0.44s
$ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
grep_rc=1
```

Negative tier probe: `build_command` with only `models.kid` and `tier="parent"` raised `KeyError` naming `parent` and `['kid']`; it did not silently accept the wrong tier. Production diff measurement is 15 added + 14 removed = 29 lines, under the 40-line ceiling.

## Limitation

This proves flag removal against version 0.3.1, not that a bare management command starts a durable coding agent. The recorded help has no headless-agent command at all; delivery of a brief to an already-running bot belongs to the separate message/route seams and remains unresolved here.
