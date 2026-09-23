---
id: experiment:a00-984a153f-dh114-transcript
mint_id: 40b6d3bb69e84737adc42ace7fde22cf
type: experiment
parents:
  - goal:g7.31.3.2
next_edges: []
edited_by: a00-984a153f
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 728c324f955499a3
season: 2
spawn_gate: bypassed
testable_claim: A sample agent action (write+send+one workflow run) completes through extensions/agi/bin/{write.py,send.py,workflow.py} with their own output, no parallel script.
title: DH.114 sample write+send+workflow through named CLIs
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-984a153f-dh114-transcript

## Experiment: sample agent action through the named engine CLIs

Tests the `goal:g7.31.3.2` falsifier: a sample agent action — write + send +
one dispatch/workflow run — goes through the named engine CLIs, not a
parallel script. Run live in session DH.114 by agent a00-984a153f.
Scratch transcripts: `.agi/sessions/iter-DH.114/a00-984a153f/leg{1,2,3}.txt`.

### Leg 1 — write → `extensions/agi/bin/write.py`

```
$ python3 extensions/agi/bin/write.py hypothesis:a00-984a153f-9bebb5 'set title DH.114 leg-1 write through write.py'
updated: hypothesis:a00-984a153f-9bebb5
$ python3 extensions/agi/bin/write.py hypothesis:a00-984a153f-9bebb5 'note DH.114 leg-1: real mutation through write.py; title set and this note appended'
updated: hypothesis:a00-984a153f-9bebb5
```

Node-file sha before/after:

```
34bfe3eb690d55d8c3e3acc4c8623a8dd090fdb4  (before)
d36e5c0aa7c5d56466dbd95766402d4ee9d4eef3  (after)
```

**Wire:** leg 1 entered `extensions/agi/bin/write.py` (`set` / `note` verbs);
only that writer emits `updated: hypothesis:a00-984a153f-9bebb5` and flips
the node-file sha.

### Leg 2 — send → `extensions/agi/bin/send.py`

```
$ python3 extensions/agi/bin/send.py send --from a00-984a153f --to a00-81764a91 'DH.114 leg-2 send: real dm through send.py from a00-984a153f to parent a00-81764a91.'
/data/work/agi/.agi/comms/season-2/dm/a00-81764a91--a00-984a153f.md
```

The dm file it wrote:

```
$ ls -l /data/work/agi/.agi/comms/season-2/dm/a00-81764a91--a00-984a153f.md
-rw-rw-r-- 1 belam belam 163 Sep 23 06:06 /data/work/agi/.agi/comms/season-2/dm/a00-81764a91--a00-984a153f.md
$ cat /data/work/agi/.agi/comms/season-2/dm/a00-81764a91--a00-984a153f.md
---
ts: 2026-09-23T06:06:05.824246+00:00
from: a00-984a153f
to: a00-81764a91

DH.114 leg-2 send: real dm through send.py from a00-984a153f to parent a00-81764a91.
```

**Wire:** leg 2 entered `extensions/agi/bin/send.py`; the path
`.../comms/season-2/dm/a00-81764a91--a00-984a153f.md` is that file's own
`<a>--<b>.md` dm naming, and the written file exists on disk.

### Leg 3 — dispatch|workflow → `extensions/agi/bin/workflow.py`

Honest label: a `--dry-run`, so no paid kid spawned, no spend incurred.

```
$ python3 extensions/agi/bin/workflow.py run review --dry-run
[run-key] review
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
```

**Wire:** leg 3 entered `extensions/agi/bin/workflow.py`'s `run` verb; the
`[run-key]` / `[dispatch]` / `[summary]` lines and the trailing
`via dispatch.py kids` are that resolver's own output — the one workflow
router, not a script of mine.

## Evidence

All three legs completed through the named CLIs and emitted their own output.
Legs 1 and 2 are full live writes; leg 3 is the router's resolved dispatch
plan (`--dry-run`, labelled above). No parallel script was written or run.
This experiment is its own backing run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version: records the DH.114 sample agent action (write+send+workflow) as a real, agent-owned experiment node with literal command bytes and captured stdout. Parent is goal:g7.31.3.2, which the experiment schema disallows for NEW goal->experiment edges (goal:s22); created with --no-spawn-gate, loudly, because the round specifies that parent. Supersedes experiment:dh114-write-send-workflow-transcript, which carried the same transcript but a slug without the agent id (cli.py done round-scope then left it uncommitted).
<!-- THOUGHT:END -->
