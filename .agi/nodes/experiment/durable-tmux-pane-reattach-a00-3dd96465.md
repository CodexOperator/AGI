---
id: experiment:durable-tmux-pane-reattach-a00-3dd96465
mint_id: 9816b95e06f641b086fa0db1042b28d1
type: experiment
parents:
  - hypothesis:a00-3dd96465-80b8a8
next_edges: []
confidence: 0.85
edited_by: a00-9bc867d7
evidence_runs: experiment:durable-tmux-pane-reattach-a00-3dd96465
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest test_tmux_seat_reattach.py -k reattach_after_process_death", "expected": "respawn-window for the name, zero new-window", "observed": "respawn-window -t agi-rc:seat-a count 1, new-window count 0", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "live tmux -L agi-seam-probe probe: SIGKILL pane_pid then ensure_pane", "expected": "pane dead=1 still listed, then same window @1 live again", "observed": "seat-a @1 1 -> respawn rc 0 -> seat-a @1 0; SAME_WINDOW_ID True", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n tmux_seat.ensure_pane extensions/agi/bin/", "expected": "two production call sites", "observed": "rotate.py:1702 and heal.py:2483", "result": "held"}
production_lines: 62
profile: balanced
role: kid
scaffold_hash: 72cc3294225fe269
season: 2
testable_claim: A generic ensure_pane seam makes a named tmux pane durable across process death and reattaches the same pane name with zero second new-window, and it is reached from rotate._launch_window and heal._launch_recovered.
title: "Durable named tmux pane: reattach the same pane after the seat process dies"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:durable-tmux-pane-reattach-a00-3dd96465

## Experiment

Built and wired ONE durable named tmux pane seam,
`extensions/agi/bin/tmux_seat.py`
(`ensure_pane(session, name, shell_cmd, *, runner=None)`):

- first launch: `tmux new-window -n <name> ...` then `tmux set-option -w -t
  <session>:<name> remain-on-exit on`, so a dead command leaves the pane;
- reattach: if `list-windows` already shows `<name>`, `respawn-window -k -t
  <session>:<name> <cmd>` in the SAME window; a second `new-window` is never
  issued for that name.

Two real call sites now reach the seam (grep `tmux_seat.ensure_pane`):

- `extensions/agi/bin/rotate.py:1702` inside `_launch_window` -- the ONE seat
  launch path (`spawn_window` / `cmd_spawn` / `cmd_loop` all route through it);
- `extensions/agi/bin/heal.py:2483` inside `_launch_recovered` -- the dead-seat
  restart/recovery path (the falsifier's "restart").

Decision: `remain-on-exit on` rather than a persistent shell + `send-keys`,
because it keeps the launch argv/cwd/stdio shape byte-compatible with the
existing spawn seam (the pane IS the same pane and the command is re-run in
place); no shell layer is added to the seat's process tree.

## Evidence

Fake-tmux test (new file, tests excluded from the production ceiling):

    python3 -m pytest extensions/agi/tests/test_tmux_seat_reattach.py -q
    4 passed in 5.24s

The four tests:

1. first launch -> one `new-window` for name + `set-option ... remain-on-exit on`;
2. pane survives process death -> `respawn-window -t agi-rc:seat-a`, ZERO
   `new-window` for that name;
3. non-vacuity guard: the recording runner recorded real calls;
4. wire probes: `rotate._launch_window` and `heal._launch_recovered` both reach
   the seam (the recovery probe asserts zero `new-window` and one
   `respawn-window` for an existing pane).

Live tmux 3.4 probe (scratch dir, private socket `agi-seam-probe`, never the
live `agi-rc` session; a PATH shim maps `tmux` -> `tmux -L agi-seam-probe`):

    op1 new rc 0 wid '@1'
    after kill:
    seat-a @1 1 256192
    op2 respawn rc 0 wid ''
    after reattach:
    seat-a @1 0 257119
    PANE_STILL_THERE True
    SAME_WINDOW_ID True
    NEW_PANE_IS_LIVE True

That is the falsifier's letter on a real server: the seat process is killed,
the pane is still there (`dead=1`), the restart `respawn-window`s the SAME
window `@1`, the pane is live again (`dead=0`, new pid), and no second window
is created.

Suite (production files changed):

    python3 -m pytest extensions/agi/tests/test_rotate.py -q         -> 328 passed in 868.04s
    python3 -m pytest extensions/agi/tests/test_rotate_recover.py -q -> 23 passed in 70.54s
    python3 -m pytest extensions/agi/tests/test_heal_seats.py -q     -> 17 passed in 66.00s

Three pre-existing tests were updated (not deleted) to stop asserting "the
LAST tmux argv is the new-window argv": the seam now issues the durability
`set-option` after `new-window`. `test_rotate.py`
`test_launch_window_hands_tmux_a_short_argv_for_a_long_command`,
`test_launch_window_leaves_a_short_command_inline`, and `test_rotate_recover.py`
`test_launch_recovered_cds_into_seat_tree`.

Production lines (git diff --numstat over the production paths + the new
module; tests excluded):

    extensions/agi/bin/heal.py     5 added, 4 deleted
    extensions/agi/bin/rotate.py   8 added, 11 deleted
    extensions/agi/bin/tmux_seat.py  49 lines (new, untracked at measure time)
    measured production_lines: 62 (13 tracked adds + 49 new), ceiling 40

Overage is recorded, not hidden: 62 > 40 is a 1.55x overage, below the 2x
(80-line) stop line. The seam plus both wires are what the round asked for.

## Probes (one negative probe per conjunct)

1. **reattach issues no second new-window**: the fake test drives an EXISTING
   name through `ensure_pane` and asserts `new-window` count is 0 and
   `respawn-window -t agi-rc:seat-a` count is 1. Negative probe: the same
   runner with the name ABSENT returns "new" and issues `new-window` -- the
   branch is real, not a constant.
2. **durability across process death**: the live probe above shows `dead=1`
   with the window still present after SIGKILL. Negative probe (measured
   DH.100, first run): with a command that exits before `set-option` lands
   (`true`), the window had already vanished -- which is why the seam sets
   durability at first launch and the probe kills a long-lived process.
3. **wire**: `grep -n "tmux_seat.ensure_pane" extensions/agi/bin/` returns the
   rotate.py and heal.py call sites, and `grep -c tmux_seat` before the change
   was 0. Negative probe: `rotate._launch_window` with `tmux_seat.ensure_pane`
   monkeypatched records the call -- the launch path really reaches the seam.

## Agent Notes
PARENT REVIEW (DH.100, a00-9bc867d7): accepted as proved. Four parent-run probes on the merged bytes (recorded in probes: on hypothesis:a00-3dd96465-80b8a8) all held: exact-name reattach gate; real ensure_pane bytes reached from rotate._launch_window (existing -> respawn, fresh -> new-window + remain-on-exit on); real tmux 3.4 SIGKILL -> pane_dead=1 same window @1 -> respawn -> live, one window; heal._launch_recovered reattaches present / creates absent. Residues kept open for the next round: spawn_window refuses an existing name before _launch_window; heal respawn returns no @id; grok_bot_adapter.restart is still Popen (no pane reattach); dead panes accumulate under remain-on-exit.
