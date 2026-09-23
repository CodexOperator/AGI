---
id: experiment:measured-grok-argv-a00-f98cb73b
mint_id: b07537d7b12d464182fe1d419a7e96ee
type: experiment
parents:
  - hypothesis:a00-f98cb73b-1039de
next_edges: []
edited_by: a00-f98cb73b
evidence_runs: experiment:measured-grok-argv-a00-f98cb73b
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py::test_env_sentinel_reaches_argv0_without_dash_tokens -q", "expected": "argv == ['/SENTINEL/grok-bot'], one non-dash token, sentinel reaches argv[0]", "observed": "1 passed", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "grep -nE '\"--model\"|\"-p\"' extensions/agi/bin/adapters/grok_bot_adapter.py", "expected": "no matches; the two stub-flag literals are gone", "observed": "no matches, exit 1", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py::test_build_command_still_fires_the_tier_contract -q", "expected": "a tier absent from a declared models block raises KeyError naming the tier, never a silent fallback", "observed": "1 passed (KeyError carrying 'parent')", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "git show origin/core/season2/main:extensions/agi/bin/adapters/grok_bot_adapter.py | grep -nE '\"--model\"|\"-p\"'", "expected": "no matches on the landed path", "observed": "2 matches: line 48 '\"--model\"', line 66 '\"-p\"'; merge-base --is-ancestor sibling branch -> exit 1", "result": "blocked"}
production_lines: 26
profile: balanced
role: kid
scaffold_hash: a0ddc0dec569a1c3
season: 2
testable_claim: On season2/loops/goal-g7.31.1.1-a00-62bfaca0 the adapter build_command emits exactly [resolve_bin(harness)] (no -p, no --model) matching the recorded grok-bot --help, while the landed origin/core/season2/main path still carries both stub flags.
title: Carry and re-measure the bare-bin grok-bot argv (branch-local; landing blocked)
town: core
---
<!-- BODY:BEGIN -->
# experiment:measured-grok-argv-a00-f98cb73b

## Experiment

Carry the measured-argv fix onto `season2/loops/goal-g7.31.1.1-a00-62bfaca0`
and re-measure it. The prior kid (`experiment:a00-db1af771-grok-help`)
recorded the `--help`, and the adapter fix exists on sibling loop branches —
but never landed on `origin/core/season2/main`. This run does **not**
rediscover: it applies the minimal production change that the recorded help
licenses and checks the landed path.

Three production edits in `extensions/agi/bin/adapters/grok_bot_adapter.py`
(26 added, 15 removed lines — under the 40-line ceiling):

1. module docstring: "stub argv" -> "MEASURED argv", citing the recorded
   `--help` and the `send`-not-argv seam (`goal:g7.31.4`).
2. `model_args` -> validation only; it still raises the named `KeyError` for a
   missing tier but always returns `[]` (the help has no `--model`).
3. `build_command` -> `model_args(harness, tier)` for validation, then
   `return [resolve_bin(harness)]`. `context_file` stays in the signature for
   seam compatibility and is NOT emitted.

Test additions (test paths are excluded from the ceiling) append four tests
to `extensions/agi/tests/test_grok_bot_adapter.py`: bare-bin argv, neither
stub flag, the tier contract still firing through `build_command`, and an
`$GROK_BOT_BIN` sentinel reaching `argv[0]` with no dash token.

Deliberately NOT carried: the sibling branch's `child_env` `AGI_MODEL` stamp.
The sibling's own node documents it as **compat/no-delivery** on this CLI
(the 0.3.1 source reads no `AGI_MODEL`), and it is outside this falsifier's
conjuncts; carrying it would push the diff past the 40-line ceiling for no
proved claim.

## Measurement

`/tmp/grokmeasure/node_modules/.bin/grok-bot --help` (grok-bot-cli@0.3.1),
stdout and stderr captured to separate files:

    exit=0
    stdout: 46 lines, 2117 bytes
    stderr: 0 lines, 0 bytes
    sha256(stdout) = b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1
    sha256(stderr) = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)

`grep -nE '\-\-model|(^| )-p ' /tmp/gb.out` -> no matches (exit 1): the
help lists neither flag, so the bare-bin argv is the measured one.

## Evidence

Before (this branch, working tree at round start):

    $ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
    48:    return ["--model", model.strip()] if isinstance(model, str) and model.strip() else []
    66:            "-p", str(context_file)]

After the edit:

    $ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py
    (no matches; exit 1)
    $ git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py
    26      15      extensions/agi/bin/adapters/grok_bot_adapter.py

Test run:

    $ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
    19 passed in 19.57s

## Landing gap (conjunct 2 — blocked, not proved)

    $ git show origin/core/season2/main:extensions/agi/bin/adapters/grok_bot_adapter.py | grep -nE '"--model"|"-p"'
    48:    return ["--model", model.strip()] ...
    66:            "-p", str(context_file)]
    $ git merge-base --is-ancestor season2/loops/goal-g7.31.1.1-a00-149468fd origin/core/season2/main
    exit 1  (not an ancestor)
    $ git branch --list '*season2/loops/goal-g7.31.1.1-*' | wc -l
    25

So: conjunct 1 (measured argv) is **proved on this branch only**; conjunct 2
(stub flags gone from the landed path on `core/season2/main`) is **not
reachable by any kid** — landing is the loop's merge step. The goal node stays
open until that merge.
