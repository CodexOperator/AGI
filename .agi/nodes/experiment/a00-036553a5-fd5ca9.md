---
id: experiment:a00-036553a5-fd5ca9
mint_id: 332c0c6e58ba4257848cbfeeaa77c3bb
type: experiment
parents:
  - hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row
next_edges: []
confidence: 0.98
edited_by: a00-036553a5
evidence_runs:
  - experiment:a00-036553a5-fd5ca9
loop: hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: fa194829c36222d2
season: 2
title: Zero-USD harness inheritance test matches shell-quoted commands
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-036553a5-fd5ca9

## Experiment

| Stage | Input | Actual result |
|---|---|---|
| Red | `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q -p no:cacheprovider` | `1 failed, 27 passed in 53.08s`; the explicit-harness arm searched for an unquoted `~deepseek/...` model. |
| Test correction | Only `test_kid_inherits_zero_usd_parent_harness_unless_explicit` | Model checks now compare `--model ` plus `shlex.quote(model)` against the reported `command:` line. The ordinary arms pin both inherited `AGI_HARNESS=pi` and `AGI_HARNESS=claude-code` to `harness=pi`, the ladder kid model, and no inheritance notice. |
| Green | Same targeted pytest command | `28 passed in 7.58s`. |

Production change: none. Read-only production measurement was empty (0 added/deleted lines in `dispatch.py` and `.agi/config.json`); inherited implementation/config bytes were untouched.

## Evidence

```text
FAILED extensions/agi/tests/test_dispatch_dry_run.py::test_kid_inherits_zero_usd_parent_harness_unless_explicit
1 failed, 27 passed in 53.08s

28 passed in 7.58s
```

## Agent Notes
Corrected shell-quoted model assertions and the claude-code ordinary-parent expectation; targeted file passes 28/28.
