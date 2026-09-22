---
id: experiment:a00-ecc1c8f5-grok-bot-measured-argv-landed
mint_id: d4f1d9d0bc5c460098402bdeddf7da6c
type: experiment
parents:
  - hypothesis:a00-ecc1c8f5-417666
next_edges: []
confidence: 0.9
edited_by: a00-ecc1c8f5
evidence_runs:
  - experiment:a00-ecc1c8f5-grok-bot-measured-argv-landed
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 76
profile: balanced
role: kid
scaffold_hash: 6eb80332a4d4c72e
season: 2
testable_claim: Recorded grok-bot 0.3.1 --help constant is byte-identical to live re-measurement, and build_command emits the bare bin with no -p/--model.
title: Measured grok-bot 0.3.1 argv landed and re-measured on this base
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ecc1c8f5-grok-bot-measured-argv-landed

## Experiment

DT.69 kid 2 carried kid 1's (`a00-e85c4a82`) measured adapter onto this base as
ordinary file writes (read-only `git show` from branch
`season2/loops/goal-g7.31.1.1-a00-e85c4a82`), then RE-MEASURED rather than
trusting the paste. Bounded surface: there is no installed box `grok-bot`; the
measurement surface is the npm package at `/tmp/grokmeasure`.

Reconcile commands (read-only git; no add/commit/merge):

```
git show season2/loops/goal-g7.31.1.1-a00-e85c4a82:extensions/agi/bin/adapters/grok_bot_adapter.py > extensions/agi/bin/adapters/grok_bot_adapter.py
git show season2/loops/goal-g7.31.1.1-a00-e85c4a82:extensions/agi/tests/test_grok_bot_adapter.py > extensions/agi/tests/test_grok_bot_adapter.py
/tmp/grokmeasure/node_modules/.bin/grok-bot --help > <scratch>/help.txt ; echo $?   # exit 0
wc -l <scratch>/help.txt                                                            # 46
grep -nE '(^| )-p( |$)|--model' <scratch>/help.txt ; echo grep_exit=$?                 # no match, grep_exit=1
sha256sum <scratch>/help.txt   # b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1
python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
```

## Evidence

Measured `--help` on this base: 46 lines, exit 0, 2117 bytes, sha256
`b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1`. The test's
`RECORDED_HELP_0_3_1` constant is **byte-identical** to it (`recorded_len 2117
== live_len 2117`, `byte_identical True`), carries no `-p` token and no
`--model` substring. The full 0.3.1 help is pasted as that constant at
`extensions/agi/tests/test_grok_bot_adapter.py:33`; its sha256 is the digest
above.

Grep for stub-only guessed flags, before/after:

```
HEAD  adapter: line 48 ['--model', model.strip()] ; line 66 '-p', str(context_file)   -> both present
live  adapter: grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py   -> no match
```

`build_command` argv, before (HEAD bytes executed) and after (landed bytes):

```
before: ['/SENTINEL/grok-bot', '--model', 'grok-4.1-fast', '-p', '/tmp/brief.md']
after : ['/SENTINEL/grok-bot']
```

Named-tier contract still fires (validation-only `model_args`, no silent
fallback): `KeyError: "harness 'grok-bot' declares no model for tier 'nope';
known tiers: ['kid']"`.

Test run, this base, this file only:

```
27 passed in 2.44s
```

The binding predicate is not vacuous: `test_the_binding_predicate_is_falsifiable`
rejects `--model`/`-p` against the recorded help and accepts `--json`/`--dir`;
`test_no_model_flag_survives_into_argv` binds argv to the recorded constant.

Production-line measure (`git diff --numstat`, adapter only; test excluded):
`59  17` -> **76** changed lines against ceiling 40 (<2x, no re-brief owed).

## Run Notes (kid 2)

This is the EVIDENCE node that kid 1 left untracked: it is committed on this
branch by `cli.py done` (the `--node-id`), closing the `SL7.136` shape where the
cited evidence run resolves to a node no branch carries. Deviation from the
brief: the experiment's parent is `hypothesis:a00-ecc1c8f5-417666` (itself a
child of `goal:g7.31.1.1`), because the `[experiment]` spawn gate's
`allowed_parents` excludes `goal` (`goal:s22`); `--parent goal:g7.31.1.1` would
have been rejected.

## Agent Notes
Carried kid1 measured grok-bot bytes onto this base; re-measured --help (46 lines, exit 0, sha256 b0865dd7) byte-identical to RECORDED_HELP_0_3_1; argv bare bin, no -p/--model; 27 grok tests pass; production_lines=76 vs ceiling 40.
