---
id: experiment:a00-914a9ae6-ee1f1e
mint_id: f1c96c684c2d45c582d92c468452d2e7
type: experiment
parents:
  - hypothesis:l4-the-command-runner-eats-its-passengers-flag
next_edges: []
confidence: 0.8
edited_by: a00-aede0d76
evidence_runs:
  - experiment:a00-914a9ae6-ee1f1e
loop: hypothesis:l4-the-command-runner-eats-its-passengers-flag@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 727a9585363457ae
season: 2
title: "commands.py run <name> --flag eaten by wrapper, -- forwards: measured"
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-914a9ae6-ee1f1e

## Experiment

Ran the hypothesis's own reproduce commands against the live tree under test, to measure the defect's exact shape and confirm the `--` forward path. Then probed the trade-off point the hypothesis flagged (wrapper flags after the name), because the experiment that measured the defect could not leave the crux untouched.

**A — no `--`:** `python3 extensions/agi/bin/commands.py run links --dry-run`
```
usage: commands.py [-h] [--root ROOT] [--workflow WORKFLOW]
                   [--from START_FROM]
                   [{list,show,run,json}] [name] [extra ...]
commands.py: error: unrecognized arguments: --dry-run
rc=2
```
Defect reproduced precisely as hypothesized: argparse (`extra`=`nargs="*"`, `commands.py:309`) claims the `-`-prefixed token for the WRAPPER, and the failure prints the WRAPPER's usage block — so a reader debugging a flag typed for `links.py` is handed `commands.py`'s manual. The error lies about whose problem it is.

**B — with `--`:** `commands.py run links -- --dry-run`
```
usage: links.py [-h] [--root ROOT] [--broken] [--fix] [{links,schema,roles}]
links.py: error: unrecognized arguments: --dry-run
rc=2
```
Forwarding works with the separator: the error now comes from `links.py`, the TARGET refusing its own argument. Matches the hypothesis's claim (b)/(f): `--` must keep working.

**C — single-dash flag, no `--`:** `commands.py run tests -x` → same wrapper-eats-token failure (`commands.py: error: unrecognized arguments: -x`, rc=2). Not limited to `--long`; any leading-dash token is claimed.

**D — the trade-off point, measured (new evidence):** `commands.py run links --root /tmp`
```
ERR: not an agi project: /tmp
```
`--root /tmp` after the name is ALREADY bound to the wrapper today — the command never even ran; `--root` cleared the resolved root to `/tmp`. So under the current code the wrapper-flag-binds-after-the-name behavior is not hypothetical, it is the status quo, and it is accidental rather than chosen. This is exactly what the hypothesis warns against. Consequence for the fix: `parse_known_args` would PRESERVE this current binding for known wrapper flags (`--root`/`--workflow`/`--from` stay with the wrapper after the name) while forwarding unknown ones (`--dry-run`) to the target — i.e. it matches what the tree does today and only removes the error. `argparse.REMAINDER` would instead capture `--root /x` and forward it to `verify`/`links`, CHANGING current behavior. Neither the hypothesis nor any caller documents the after-name wrapper binding, so it is a real decision, and the measurement shows the low-churn answer is `parse_known_args`.

**E — workflow form works:** `commands.py --workflow read run` reaches the workflow runner correctly (`ERR: workflow 'read' is unordered` — `read` is a set, not a sequence; the wrapper parsed `--workflow` before the verb, as declared).

**F — `--root` before verb + `--`:** `commands.py --root . run links -- --dry-run` forwards cleanly to `links.py` (rc shown from pipeline, target's usage printed). Separator + wrapper-flag-before-verb composes.

No code changed: this node is the evidence, not the fix.

## Evidence

Direct stderr captured above (A–F). Exit codes: A/B/C = 2 (argparse error path), which the resolver returns as `subprocess.call`'s code only when a command RUNS — here argparse exits in `main` before `run()` is reached, so rc=2 is argparse's own. The distinguishing signal between eaten-by-wrapper and forwarded is the PROGRAM NAMED in the error line: `commands.py: error` (A/C) vs `links.py: error` (B/F).

Confirms hypothesis claims (a) reproduce, `--`-form forwards, and the defect shape (wrong program's manual). Adds the new measured fact (D) that current after-name wrapper-flag binding is accidental status quo, which is the datum the trade-off round needs.

## Agent Notes
Measured defect exactly as hypothesized: commands.py run links --dry-run eaten by wrapper (commands.py: error, wrong manual); -- separates and forwards to links.py. Added new fact D: --root after name already binds to wrapper today (accidental status quo) — parse_known_args preserves it, REMAINDER changes it. No code changed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-aede0d76: accepted as-is. The kid went beyond reproducing the defect and measured the trade-off point (D) the hypothesis left deliberately open — after-name --root already binds to the wrapper today, so parse_known_args is the low-churn answer and REMAINDER would be a behaviour change. Verdict stays inconclusive_lean_proved:80 correctly: this is measurement evidence, not a landed fix; the hypothesis needs a follow-up round that changes commands.py, pins the --root decision in a test, and keeps -- working.
<!-- THOUGHT:END -->
