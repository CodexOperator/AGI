---
id: experiment:a00-d3ee4161-07c983
mint_id: 6f2f7dd547804907b16bc5001d44c05b
type: experiment
parents:
  - hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi
next_edges: []
confidence: 0.85
edited_by: a00-cd9b4aa1
evidence_runs:
  - experiment:a00-d3ee4161-07c983
loop: hypothesis:l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-claude-code-and-pi@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3cd92605a100d6d7
season: 2
title: "rotate.py now REFUSES an unknown --harness by name: unknown and declared-but-unbuildable (pi) refused rc!=0 empty shell, copilot-ci seat and claude default byte-identical, 4583 suite green"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d3ee4161-07c983

**BUILD, not measurement.** The parent is a build order: `rotate.py` must refuse
an unknown `--harness` by name instead of silently seating a claude post. This
node reproduces the defect, implements the refusal, and re-proves conjunct 6 on
the BUILT bytes. Suite green.

## The reproduced defect (pre-fix)

```
$ python3 extensions/agi/bin/rotate.py spawn --name bogus-test-a00 \
      --harness does-not-exist --tier director --dry-run

export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && \
  claude --remote-control bogus-test-a00 --permission-mode bypassPermissions \
    --debug-file .../bogus-test-a00.log --model claude-fable-5-1 --effort max '<card>'
RC=0
```

An unknown harness id fell through `_build_harness_command` to the claude branch.
A typo (`copilot_cli`, `copilot`, `copilot-clli`) therefore seated a **claude**
post and burned the owner's 3%-left Claude Code budget -- the exact cost the
third-harness claim exists to conserve. `dispatch.py` refuses the same input by
name (`adapters.resolve`: "no harness 'X' in config; declared: [...]").

## The fix

`extensions/agi/bin/rotate.py`: a new `_validate_harness(root, harness)` called
at the TOP of `spawn_window`, before any model resolution or command build.

- absent / `claude-code` -> accepted, argv byte-identical to today.
- root is not None -> the config's `harnesses` keys are the declared set; a
  name not in it prints `ERR: no harness 'X' in config; declared: [...]` and
  returns `(1, "")`.
- root is None (no config to consult) -> only the two known buildable ids are
  accepted; anything else refused by name against that two-id list.
- a DECLARED but unbuildable harness (`pi` is declared in this project's live
  config for dispatch, but rotate has no pi argv builder) is also refused, by
  its own message, rather than falling to the claude branch -- same cost defect,
  one name further out.

The refusal returns before `_existing_windows`, `_launch_window` and every other
write, so a bad name cannot open a window or write anything.

## The built commands (post-fix, dry-run, quoted)

```
$ python3 extensions/agi/bin/rotate.py spawn --name bogus-test-a00 \
      --harness does-not-exist --tier director --dry-run
ERR: no harness 'does-not-exist' in config; declared: ['claude-code', 'copilot-cli', 'pi']
RC=1                      # stderr; stdout empty

$ python3 extensions/agi/bin/rotate.py spawn --name cop-test-a00 \
      --harness copilot-cli --tier director --dry-run
export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && \
  /home/ubuntu/.npm-global/bin/copilot --model auto --allow-all-tools -i '<card>'
# no --remote-control, no --debug-file

$ python3 extensions/agi/bin/rotate.py spawn --name cc-test-a00 --tier director --dry-run
export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 && \
  claude --remote-control cc-test-a00 --permission-mode bypassPermissions \
    --debug-file .../cc-test-a00.log --model claude-fable-5-1 --effort max '<card>'

$ python3 extensions/agi/bin/rotate.py spawn --name pi-test-a00 --harness pi --tier director --dry-run
ERR: harness 'pi' is declared but rotate.py cannot build it; buildable: ['claude-code', 'copilot-cli']
RC=1
```

## Tests (fixture-only, no live copilot)

`extensions/agi/tests/test_rotate_copilot_harness.py` gains 4 tests:
`test_unknown_harness_is_refused_by_name` (rc!=0, empty shell, declared list),
`test_unknown_harness_refused_with_no_config_root` (`copilot_cli` vs the two-id
list), `test_known_harness_accepted_with_no_config_root`,
`test_declared_but_unbuildable_harness_refused`.

```
$ python3 -m pytest extensions/agi/tests/test_rotate_copilot_harness.py -q
12 passed in 0.21s

$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_copilot_harness.py \
    extensions/agi/tests/test_spawn_name.py extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_copilot_cli_adapter.py \
    extensions/agi/tests/test_dispatch_dry_run.py -q
369 passed, 331 warnings in 39.64s

$ python3 -m pytest <every extensions/agi/tests/test_*.py> -q
4583 passed, 15 skipped, 1 xfailed, 1581 warnings in 438.88s (0:07:18)
```

The counts move exactly as the new tests require (365->369 covering, 4579->4583
full; kid 3's 8 tests are unchanged and still pass).

## Code changed

| File | Change |
|---|---|
| `extensions/agi/bin/rotate.py` | `_KNOWN_HARNESSES`, `_validate_harness`, called first in `spawn_window` |
| `extensions/agi/tests/test_rotate_copilot_harness.py` | +4 fixture-only tests |

## Agent Notes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version exists because kid 3's material was demoted: the copilot seat was
built correctly, but `--harness does-not-exist` still fell to the claude branch
and spent the budget the claim is about. The gate probe, not a code read, is
what found it (`experiment:a00-5510f914-f1ae48` note), which is why the fix is
proven on the dry-run output rather than by inspection.

The seam is one validator in front of the existing builder: nothing inside
`spawn_window`'s resolution or `_build_harness_command` changed, so the default
and `claude-code` lines stay byte-identical (the covering test
`test_explicit_harness_claude_code_matches_absent` still passes).

One deliberate divergence from the brief's literal wording: the brief says to
refuse when the name is absent from `config.json`'s `harnesses` map. That leaves
`--harness pi` (declared for dispatch, no rotate builder) falling to claude --
the same silent-claude cost, one name out. So `_validate_harness` also refuses a
declared-but-unbuildable id by its own message. It is one extra refusal on a
path the brief left undefined, not a widened surface.
<!-- THOUGHT:END -->

## Agent Notes
rotate.py now REFUSES an unknown --harness by name before building anything: 'ERR: no harness does-not-exist in config; declared: [claude-code, copilot-cli, pi]' + rc=1 + empty shell, and a declared-but-unbuildable harness (pi) is refused by its own message rather than falling to claude; copilot-cli still builds copilot --model auto --allow-all-tools -i <card>, no-harness/claude-code byte-identical; 12 tests in test_rotate_copilot_harness.py, 369 covering, 4583 full suite passed/15 skipped/1 xfailed.

PARENT REVIEW PROBES (a00-cd9b4aa1, 2026-09-14): gate — "rotate.py spawn --name bogus2-a00 --harness does-not-exist --tier director --dry-run" now prints "ERR: no harness "does-not-exist" in config; declared: [claude-code, copilot-cli, pi]" and exits 1 with empty stdout (was: silently built claude). Extra: "--harness pi" refuses by its own message; "--harness claude-code" stdout is byte-identical to no --harness (diff empty). wire — copilot dry-run still emits "copilot --model auto --allow-all-tools -i", default still "claude --remote-control cc2-a00". ACCEPTED, proved: conjunct 6 refusal proved and copilot seat re-proved.
