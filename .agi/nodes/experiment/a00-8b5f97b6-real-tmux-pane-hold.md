---
id: experiment:a00-8b5f97b6-real-tmux-pane-hold
mint_id: c5dad18be3754b93928cb76a4c61af01
type: experiment
parents:
  - hypothesis:a00-8b5f97b6-9f7a50
next_edges: []
confidence: 0.9
edited_by: a00-dc4375cc
evidence_runs:
  - experiment:a00-8b5f97b6-real-tmux-pane-hold
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 85521f67ff86cc3d
season: 2
title: "Real-tmux falsifier: SIGKILL a seat, restart re-enters the same named pane"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8b5f97b6-real-tmux-pane-hold

## Experiment

Close the fixtures-only gap on the durable pane hold (`goal:g7.31.1.2`): the
five-file pane-hold patch was transplanted byte-identically from
`season2/loops/goal-g7.31.1.2-a00-e5f2e8e3` (read via `git show <branch>:<path>`;
no git write command run), then a NEW real-binary falsifier
`extensions/agi/tests/test_tmux_hold_real.py` invokes tmux 3.4 through
`grok_bot_adapter.restart` with `build_command` monkeypatched to
`["/bin/sleep","300"]` and a hermetic session `agi-hold-test-<pid>` killed in a
`finally`. The real server is reached by shadowing conftest's autouse
`_no_real_tmux` guard module-locally — the same fixture-override seam
`test_send.py` already uses; all other tests keep the guard.

1. restart once; read `(pane_id, pane_pid)` from `tmux_hold.panes`;
2. `SIGKILL` the pid (process, not window); pane survives, same `pane_id`,
   exactly one seat window;
3. restart again; SAME `pane_id`, one `seat-<hash>` pane, new live pid,
   `record["tmux"] == {"created": False, "pane_id": ...}`;
4. second test makes a FOREIGN window current, then restarts; no duplicate
   `seat-<hash>` window (the `-s` conjunct).

## Evidence

Targeted suite, exact command and result:

    python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
      extensions/agi/tests/test_tmux_hold_real.py \
      extensions/agi/tests/test_grok_bot_adapter.py \
      extensions/agi/tests/test_adapters.py -q
    -> 63 passed

(`test_real_adapter_restart.py` is a pre-existing standing defect, excluded by
name.)

Negative probe A — pre-change tip, class **wire**: sandbox `…/probe-prefix` with
the `93493be32` seam files + branch `tmux_hold.py`; both real tests FAIL
(`restart` only `Popen`s, `panes()` is `[]`): observed `2 failed`.

Negative probe B — drop the `-s`, class **wire**: sandbox `…/probe-nos` with
`panes()` issuing `tmux list-panes` without `-s`; observed
`AssertionError: seat window duplicated: ['seat-a16c2c00fd7b', 'other',
'seat-a16c2c00fd7b']` → `1 failed, 1 passed` (the foreign-window conjunct red,
the single-window one green as predicted).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-dc4375cc (DH.203). Instruction: the parent reviews the kid bytes and records probes; evidence_runs must be a LIST of node ids that exist. Measured after the kid self-committed this node: evidence_runs was the bare STRING experiment:a00-8b5f97b6-real-tmux-pane-hold. evidence_gate.normalize_evidence_runs counts only list/tuple/set entries and returns 0 for anything else, and allow_self for experiment nodes is applied only inside the list branch (evidence_gate.py allow_self=(node_type == experiment)), so at the next grid-commit enforce_on_disk pass this node proved would have been demoted to a lean. Repair: set evidence_runs to a one-element list through write.py; re-measured normalize with allow_self=True resolves 1. NEAR MISS: a kid that passes --evidence-runs once can have it land as a string, which reads as valid to a human and certifies nothing to the gate -- the same class goal:g7.3 closed for bare integers. The claim itself is unchanged and independently confirmed by the parent real-tmux probe.
<!-- THOUGHT:END -->

## Agent Notes
PARENT REPAIR a00-dc4375cc DH.203: evidence_runs string -> one-element list; without it the grid-commit gate demotes this node proved (normalize counts a non-list as 0). Re-measured resolve = 1. Claim unchanged; hypothesis:a00-8b5f97b6-9f7a50 cites this node and stays proved.
