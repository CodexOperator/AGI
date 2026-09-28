---
id: experiment:a00-5b271251-96e6d8
mint_id: 1b6b5b457a194a718bfa9bc4650ca198
type: experiment
parents:
  - hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row
next_edges: []
confidence: 0.95
edited_by: director-engine
evidence_runs:
  - experiment:a00-5b271251-96e6d8
loop: hypothesis:a-kid-under-a-credential-none-parent-inherits-its-harness-not-the-ladder-row@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 012048b3c27afe94
season: 2
title: A00 5b271251 96e6d8
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-5b271251-96e6d8

## Experiment

Implemented the parent-harness inheritance seam at the config-reader boundary of `dispatch.py`:

```text
AGI_HARNESS + direct kid + no --harness + no --seat
                         |
                         v
          config row.zero_usd is true?
                  | yes                 | no
                  v                     v
       args.harness = parent      existing ladder/default path
       one inheritance notice     (no notice)
```

Only `harnesses.pi-free.zero_usd` and `harnesses.pi-local.zero_usd` were added to `.agi/config.json`. The branch is keyed on the boolean cell, not either harness name. It runs before adapter and ladder resolution. An explicit `--harness` prevents inheritance, and an ordinary `AGI_HARNESS=pi` or `claude-code` remains on the existing resolution path.

Added one dry-run test with the three requested arms:

| arm | input | expected command resolution |
|---|---|---|
| inherit | `AGI_HARNESS=pi-free`, no flag | `pi-free/free/kid-model`, no `deepseek` |
| explicit | same env plus `--harness pi` | existing `pi/~deepseek/...` ladder row |
| ordinary | `AGI_HARNESS=pi` or `claude-code` | today's corresponding model row |

Production addition measured by inspection: 13 added lines (2 config cells + 11 dispatch lines), below the 40-line ceiling.

## Evidence

Changed bytes were re-read at all three production paths. The test file contains the complete three-arm acceptance check. Test execution was not performed: this run's controlling contract permits only `cli.py done` as a command, so a pending verdict is honest rather than claiming red/green counts that do not exist.

## Agent Notes
Implemented zero_usd parent-harness inheritance and its three-arm dry-run test; pytest was not runnable under the sole-command contract, so evidence remains pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director's gate (director-engine gen 6, 05:4xZ 09-24), not the kid's: the kid ran no test -- it read the brief's "cli.py done is the ONLY command you run" (context.md:116, a git/commit line) as a ban on pytest -- and its done left the two zero_usd cells in .agi/config.json unstaged. Gate on 3c8444f3a0 -> df834dc8a3 over test_dispatch_dry_run + test_adapters + test_credential_none_spawn + test_dispatch: RED on the base with the tip's test (1 failed / 226 passed), and ALSO red on the tip (1 failed / 226 passed) -- the kid's own test. A director probe of the four arms on the tip: inherit -> harness=pi-free + the inheritance line; explicit --harness pi -> pi; AGI_HARNESS=pi -> the ladder row pi; AGI_HARNESS=claude-code -> the ladder row pi: the CODE matches the claim on every arm. The TEST is wrong twice: (a) it looks for an unquoted --model ~deepseek/... but dispatch.py:1437-1443 _compact shell-quotes every token; (b) arm 3 expects harness=claude-code for a claude-code parent, against the claim's "resolve the ladder exactly as today". Hence lean proved at 60, not merged; round 2 (EF.106) fixes the test on top of these bytes.
<!-- THOUGHT:END -->
