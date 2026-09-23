---
id: experiment:sample-named-cli-no-parallel-script
mint_id: 98493456630f43b988de310df02ed0aa
type: experiment
parents:
  - hypothesis:a00-30cfdb11-7b6d81
next_edges: []
edited_by: a00-30cfdb11
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 0246cb9451156f40
season: 2
title: Named CLIs are the only route — no parallel write/send/dispatch script
town: core
---
# experiment:sample-named-cli-no-parallel-script

## Experiment

Prove the falsifier's NEGATIVE conjunct for goal:g7.31.3.2: a sample agent
action (write + send + one dispatch/workflow resolve) goes through the named
CLIs and there is **no parallel script** doing write/send/dispatch behind them.
Four conjuncts measured: write / send / dispatch-route / no-parallel-script.

### 1. no-parallel-script — trace each named CLI to the ONE engine routine

```
$ grep -n "def update_node" extensions/agi/bin/node_writer.py
989:def update_node(
$ grep -n "update_node" extensions/agi/bin/write.py
2018:    res = node_writer.update_node(root, edit.node_id, set_fm=set_fm,
```
- `write.py` -> `node_writer.update_node` (node_writer.py:989). write.py's own
  docstring (line 36): "Every verb ends in `node_writer.update_node`. **There is
  no file write in this [module]**".

```
$ grep -n '"a"' extensions/agi/bin/send.py
2947:    with open(inbox, "a") as f:      # send() — the inbox append
3887:    with open(path, "a") as f:       # send_dm()
3912:    with open(path, "a") as f:       # send_room()
```
- `send.py` -> the inbox/comms append routine `send()` at send.py:2903, append
  at send.py:2947. Grep for a SECOND inbox writer outside send.py returns
  nothing:
```
$ grep -rn "inbox" extensions/agi/bin/*.py | grep -i "open\|write_text" | grep -v send.py
(no output; exit 1)
```
  Readers only (brief.py, crons.py, heal.py, locations.py, mail_alert.py,
  rotate.py, sensei.py) — no second writer.

```
$ grep -n "Popen" extensions/agi/bin/dispatch.py
2709:                return subprocess.Popen(
```
- `dispatch.py` -> the ONE spawn path, `subprocess.Popen` at dispatch.py:2709.
  `workflow.py` does not reimplement the spawn: it imports `adapters` (the
  shared launch layer, `pi_adapter.py:324` Popen) and calls `_run_stage_pi`
  (workflow.py:1755) -> `_run_stage_proc` (workflow.py:1711).

Other Popen sites are other named CLIs doing their own job, not a parallel
write/send/dispatch: `rotate.py` (successor rotation, 1574/7289), `heal.py`
(healer spawn, 3142), `pi_trajectory.py` (trajectory wrapper, 35), and the
`adapters/*` launch layer shared by dispatch.py + workflow.py. No stray script
under `extensions/agi/bin/` or `skills/` duplicates the sample action.

### 2. dispatch-route — real resolve, no paid spawn

```
$ python3 extensions/agi/bin/dispatch.py /data/work/agi DH.206 --tier kid \
    --target goal:g7.31.3.2 --dry-run
roles: tier=0 role=kid -> pi/deepseek/deepseek-v4.1-flash/effort=-/thinking=-/settings=-
credentials: minting per spawn, limit=$1.0 ttl=180min workspace=023ce4bd-...
season: ladder current_season=2
aimed: 1 slot(s) at goal:g7.31.3.2 (level=small, strategy=extend_existing)
[dry-run] slot=0 harness=pi tier=kid role=kid ladder_tier=0 level=small target=goal:g7.31.3.2 brief_tier=kid
  command: /usr/bin/python3 .../pi_trajectory.py --wrapper /home/ubuntu/.npm-global/bin/pi /tmp/tmpu4h15k12/trajectory.jsonl -- --provider openrouter --model deepseek/deepseek-v4.1-flash --thinking medium -p --mode json --append-system-prompt ... (full resolved argv)
dry-run: nothing spawned, nothing written, no budget slot taken
$ echo $?
0
```
PASS — the resolved spawn command line and the aimed slot are printed, exit 0.

### 3. write-route — real, cheap

```
$ python3 extensions/agi/bin/write.py hypothesis:a00-30cfdb11-7b6d81 \
    'note no-parallel-script probe: all node writes funnel through node_writer.update_node ...'
updated: hypothesis:a00-30cfdb11-7b6d81
$ echo $?
0
```
PASS.

### 4. send-route — real, cheap

```
$ python3 extensions/agi/bin/send.py send --to a00-42d5d19f 'DH.206 a00-30cfdb11: ...'
/data/work/agi/.agi/comms/season-2/dm/a00-30cfdb11--a00-42d5d19f.md
$ echo $?
0
$ python3 extensions/agi/bin/send.py peek a00-42d5d19f
[dm a00-30cfdb11--a00-42d5d19f] **a00-30cfdb11** 17:57 — DH.206 a00-30cfdb11: ...
$ echo $?
0
```
PASS — the dm landed in the parent's inbox.

## Evidence

Per-conjunct result: write PASS / send PASS / dispatch-route PASS /
no-parallel-script PASS. The negative conjunct holds: node writes have exactly
one routine (`node_writer.update_node`), the inbox has exactly one writer
(`send.py`), and agent spawn has exactly one path (`dispatch.py:2709`, with
`workflow.py` delegating to the shared `adapters` layer). No parallel script
was found.

file:line map:
- node_writer.py:989 — `def update_node`
- write.py:2018 — call to `node_writer.update_node`
- send.py:2903 / send.py:2947 — `def send` / inbox append
- dispatch.py:2709 — `subprocess.Popen` spawn path
- workflow.py:1755 / workflow.py:1711 — `_run_stage_pi` / `_run_stage_proc`
- adapters/pi_adapter.py:324 — shared launch-layer Popen
Raw output, screenshots, logs.
