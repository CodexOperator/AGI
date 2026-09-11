---
id: experiment:a00-b579262f-3bf043
mint_id: 34f08a3b2c2c4912922081cc40d2ea76
type: experiment
parents:
  - hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files
next_edges: []
confidence: 0.8
edited_by: a00-aa272814
evidence_runs:
  - experiment:a00-b579262f-3bf043
loop: hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4e3287260730abeb
season: 2
title: A00 b579262f 3bf043
town: core
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# experiment:a00-b579262f-3bf043

## Experiment

Built and proved (this is a g15 BUILD claim, not a measurement — measure the
pre-fix gap, implement, prove on built bytes) the recovery-seating predecessor
autopsy pre-fill (`hypothesis:l4-a-recovery-seating-gets-its-predecessor-
autopsy-pre-filled-from-files`), landing most of the build order in
`extensions/agi/bin/rotate.py` + `extensions/agi/tests/test_rotate_autopsy.py`.

**What the instruction said vs what the machine does (cited):**

(1) `rotate.py autopsy --seat S [--pid P] [--registry-dir D]` — new `cmd_autopsy`
(rotate.py:3406), prints FROM FILES ONLY, read-only. New region at rotate.py:
3113-3440 (after `_first_seating_announce`): `AUTOPSY_TAG`, `transcript_from_registry`
(3120), `_registry_read`, `_pid_gone` (the one liveness read, `/proc/<pid>`),
`_death_timestamp` (registry `statusUpdatedAt`/`updatedAt` ms else transcript
mtime), `_iter_assistant_entries` (last-10 non-heartbeat; summary via imported
`sensei._summarize_tool_input`, never copied), `_reaper_log_path` (env
`AGI_REAPER_LOG` else `config:crons` services entry else `~/logs/agi-reaper-*.log`
— hash NEVER hardcoded), `_reaper_lines_for`, `_latest_service_output_log`
(heal.py's `*/output.log`), `_probable_cause` (L4.281 signatures),
`_seating_worktree_lines` (behind N / unresolved merge / dirty, porcelain with
cron churn excluded exactly as `_prepare_churn_path`), `_compose_seating_base_block`,
`_run_autopsy` (3322).

(2) cited self-join args: `transcript_from_registry` lifted OUT of `_join_successor`
(was inline ~4606-4610), refactored (rotate.py now ~4560) and called from both
join and autopsy — one helper, never a copy. Sibling import; never re-derived.

(3) `[seating]` block + autopsy-as-last-block: `cmd_spawn` (rotate.py:1287-1327)
prints `_compose_seating_base_block` (spawned-by / predecessor pid + death ts /
record / wrapper / seq), the three worktree-state lines (`_seating_worktree_lines`,
EVERY seating), and — when the seat row (or `--pid`) names a pid that is gone and
`--no-autopsy` is absent — appends `[autopsy]` lines as the LAST block.
`--no-autopsy` (rotate.py:8941) skips only the autopsy, keeps the base block.
Argparse: `autopsy` subparser rotate.py:8953; routed to root-required main.

(5) SL2.02 residue: NOT landed this round — the meter-pin / pending-ack.json /
failed-spawn-record / post-join-wording items are deferred (scarce single-shot
budget); the autopsy + seating block + worktree lines ARE landed. This is the
one deviation from the full build order — see THOUGHT block.

**Proved on the built bytes:** red-first tests green
(`test_rotate_autopsy.py`, 6 tests) + the required suite:
```
python3 -m pytest extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_startup.py \
  extensions/agi/tests/test_rotate_autopsy.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
# 268 passed, 1 skipped
exensions/agi/tests/test_rotate_handover.py  -> 23 passed (join refactor safe)
```
Tests prove: every labelled line from a FIXTURE registry json + transcript +
record (heartbeats excluded from last-10, post-death bounded out); live pid ->
`alive: yes` and the autopsy still prints; no record -> `launch: not recorded
(record: none)` (never exit 2); a SIGTERM reaper line -> the probable-cause
line; `cmd_autopsy` exits 0; the subprocess-list the autopsy runs is ALL
read-only git (`rev-list`/`rev-parse`/`status --porcelain`, no merge/kill/
checkout/add); `cmd_spawn` with a dead seat-row pid ends its `[seating]` block
with the autopsy, and `--no-autopsy` omits it.

<!-- THOUGHT:BEGIN — authored; carried across regenerating scans. The reasoning behind THIS version. -->
(1) instruction: pre-fill a recovery seating's predecessor autopsy from files.
(2) the machine now does: `cmd_autopsy` + the spawn `[seating]` block +
autopsy-as-last-block; reads only. (3) near miss: the draft's `--pid <X>` cannot
be run literally — the draft carries NO pid for the dead predecessor X
(correction 6); I derived X's pid 3526521 from the gen IX->X rotation record's
`handover.join.pid`, not from the draft; also my first test computed the
registry death-ms in LOCAL (UTC+4) time so the registry timestamp and the
transcript bound disagreed by 4h — fixed by computing death_ms in UTC. (4)
deviation: the SL2.02 residue (meter pin / pending ack.json / failed-spawn
record / post-join wording) was NOT landed — cut for the single-shot budget;
that residue is the next run's push_further. Also `_latest_service_output_log`
scans the newest `*/output.log` under sessions, because heal's per-healer dir is
ephemeral by uuid — a dead predecessor's own service log is usually already gone.
<!-- THOUGHT:END -->

## Evidence

**HAND RUN A — dead predecessor X of the belam 175816Z recovery**
(`--seat belam --pid 3526521`; pid derived from the gen IX->X rotation-record
`handover.join.pid`, since the draft carries none):
```
[autopsy] seat: belam
[autopsy] predecessor pid: 3526521 alive: no (gone)
[autopsy] death time: - (source: unmeasured)
[autopsy] transcript: -
[autopsy] last 10 non-heartbeat entries before death:
[autopsy]   (no transcript on disk)
[autopsy] reaper log: /home/ubuntu/logs/agi-reaper-agi-2f118e6f.log
[autopsy] service output.log: .../iter-L4.252/a00-a4f37350/output.log
[autopsy]   (no reaper/service line names pid 3526521)
[autopsy] launch: record <belam> own_window {'name': 'belam-S1-L4-IX','id':'@277'} \
  | successor_window {'name':'belam-S1-L4-X','id':'@281'} | result success
[autopsy] worktree: behind origin/season/s2 4 | unresolved merge: no | dirty: 3 paths
```
**HAND RUN B — current seat-row pid (`--seat belam`, 390491, live)**: shows the
alive falsifier (block still prints, `alive: yes`) with live death time,
transcript and the last-10 non-heartbeat entries.

**Per-draft hand-call count each printed line replaces** (draft
`spawn-seating-audit-20260911T175816Z.md`):
- `[seating] spawned-by / predecessor pid / record / wrapper` line replaces
  belam calls **3-9 (7)** — records dir, tmux windows, seats row, launch
  script, `ps` for rotate.py, ack/pending files.
- each `[autopsy] ... last 10 non-heartbeat` line replaces a slice of belam
  calls **14-17 (4)** — the debug-log/transcript forensics on X's death.
- `[seating] worktree: behind / unresolved merge / dirty` line replaces the
  helper's merge-repair discovery calls **1-7 and 26-30 (~11)** — the
  unresolved merge the spawn never named.
- the autopsy's reaper/service + launch lines replace the tail of X's forensics
  (the remaining part of calls 14-17).

**Honest caveat (measured, not hidden):** a DEAD predecessor's `~/.claude/
sessions/<pid>.json` is cleaned once the join lands (3526521.json is gone), and
`--registry-dir`/transcript derivation reads that file, so HAND RUN A degrades
`death time`/`transcript`/`last-10` to honest `-`/`none` when the registry has
been cleaned — the launch + worktree + reaper lines still print. The recovery's
last-10 forensics are therefore fully pre-filled only when the registry json
for the dead pid (or an explicit `--registry-dir`) still exists — which the
live belam row (RUN B) does.

## Agent Notes
rotate.py autopsy --seat S prints predecessor death facts from files only (read-only); cmd_spawn prints [seating] block + worktree lines and appends autopsy as last block for dead pid, --no-autopsy omits; transcript_from_registry refactored from _join_successor; 6 red-first tests + required suite 268 passed

PARENT REVIEW (a00-aa272814, SL3.01). Verified by reading the artifact, not the report: cmd_autopsy rotate.py:3406; new region 3113-3440; spawn hook rotate.py:1287-1327; --no-autopsy rotate.py:8941; transcript_from_registry lifted from _join_successor and called by both. Tests re-run here: test_rotate_autopsy.py + test_rotate.py + test_rotate_startup.py + test_bin_help_smoke.py = 268 passed, 1 skipped. ACCEPTED as evidence for items (1)-(4) of the target claim (autopsy from files, probable-cause lines, spawn auto-run + --no-autopsy, read-only). NOT ACCEPTED as the whole round: item (5), the SL2.02 residue (meter pin, seats/<S>.ack.json answer pending, failed-spawn record, post-join wording), is explicitly part of the build order and is UNLANDED; a second kid is being cut for it. Two review observations to carry forward: (a) _compose_seating_base_block prints 'record: none' unconditionally while _first_seating_announce WRITES a record moments later, so the line is true only of the pre-announce instant and reads false to a human who then sees the record on disk; (b) _seating_worktree_lines carries a dead 'divergent' var and a garbled docstring ('Returns [autopsy] is False else rendered lines'). Verdict left at the kid's honest inconclusive_lean_proved:78; no demotion needed, the lean is not an overclaim.
