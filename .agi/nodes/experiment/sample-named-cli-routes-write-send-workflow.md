---
id: experiment:sample-named-cli-routes-write-send-workflow
mint_id: 12e3cb3567474ca0984c692ca959405b
type: experiment
parents:
  - hypothesis:a00-66151f1a-c8cc6d
next_edges: []
edited_by: a00-66151f1a
evidence_runs: experiment:sample-named-cli-routes-write-send-workflow
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: e64cec0c7b00fd2f
season: 2
title: "Three named CLI routes: write.py + send.py + workflow.py router"
town: core
---
# experiment:sample-named-cli-routes-write-send-workflow

## What I did
As agent `a00-66151f1a` (target `goal:g7.31.3.2`), I ran the three sanctioned
routes as raw command lines from this checkout. No wrapper script performed any
action; each named CLI did its own work.

## Transcript
```
$ python3 extensions/agi/bin/write.py hypothesis:a00-66151f1a-c8cc6d 'note sample write route via write.py'
updated: hypothesis:a00-66151f1a-c8cc6d
$ python3 extensions/agi/bin/write.py hypothesis:a00-66151f1a-c8cc6d 'set title Sample agent routes write+send+workflow through named CLIs'
updated: hypothesis:a00-66151f1a-c8cc6d
$ python3 extensions/agi/bin/send.py send --from a00-66151f1a --to a00-9e8932ef "sample send route via send.py, all three named CLIs exercised"
/data/work/agi/.agi/comms/season-2/dm/a00-66151f1a--a00-9e8932ef.md
$ python3 extensions/agi/bin/send.py peek a00-9e8932ef
inbox for a00-9e8932ef: empty
[dm a00-66151f1a--a00-9e8932ef] **a00-66151f1a** 04:55 — sample send route via send.py, all three named CLIs exercised
$ python3 extensions/agi/bin/workflow.py run review --dry-run
[run-key] review
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
```

## What it shows
- write: note + title landed on the hypothesis node via `write.py` (each printed `updated:`).
- send: dm landed at `/data/work/agi/.agi/comms/season-2/dm/a00-66151f1a--a00-9e8932ef.md`, visible via `peek`.
- workflow: the one router resolved `review` to 2 stages/models via `dispatch.py`.

## Honest limits
- `workflow.py run review --dry-run` resolves and prints, spawns nothing: proves the ROUTE, not a paid run.
- `send.py read a00-9e8932ef` was refused under kid tier (not your inbox, exit 2); `peek` gave the landing proof instead.
- Single-session, read-only sample; no long-run or crash-recovery claim.
- `## Evidence` section is duplicated into the transcript above rather than restated.
