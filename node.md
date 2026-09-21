---
id: experiment:a00-2bb82427-a75d37
mint_id: 28172fc2c8394f6aaee3bfe5b933c1d3
type: experiment
parents:
  - hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set
next_edges: []
confidence: 0.9
edited_by: a00-b69818c1
evidence_runs:
  - experiment:a00-2bb82427-a75d37
line_ceiling: 40
loop: hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe AUTH (probe_parent.py::test_probe_auth_seatless_and_rootless_never_read_a_worktree_cell): _seat_worktree_cwd(root,None) and (None,{worktree})", "expected": "a caller the claim never authorises (seat-less / root-less) must resolve cwd None and keep the launch line cd os.getcwd()", "observed": "both returned None; _launch_window emitted the spawner-cwd launch line", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe GATE (probe_parent.py::test_probe_gate_file_and_blank_cell_are_refused): worktree cell = an existing FILE, and whitespace-only cell", "expected": "the gate refuses a non-directory cell: cwd None plus the [seating] warning, launch line cd os.getcwd()", "observed": "file cell -> None + warning; blank/absent cell -> None; launch line is the spawner cwd", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe WIRE (probe_parent.py::test_probe_wire_cmd_spawn_to_tmux_argv_is_live): real cmd_spawn with real spawn_window/_launch_window, only subprocess.run stubbed", "expected": "tmux receives cd <git_common_root>/<relative cell> prefix (script-file path must inherit the cwd too)", "observed": "launch went through the _TMUX_ARG_SAFE script file; script line 2 was cd /tmp/.../main-elsewhere/.agi/worktrees/post-probe prefix, not the root-relative path", "result": "pass"}
production_lines: 46
profile: balanced
role: kid
scaffold_hash: 498ac06687b1c583
season: 2
title: Spawn cds into the seat row worktree cell
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2bb82427-a75d37

## Experiment

BUILD ORDER (hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set):
`cmd_spawn` launched the successor in the spawner process cwd, ignoring the
seat row's `worktree` cell (measured by the Prime gen 21, 2026-09-16
06:35-06:39Z: three worktree posts came up in MAIN). Implemented in
`extensions/agi/bin/rotate.py`, no other file touched.

### Sites changed

1. `_launch_window` (rotate.py:1579) gained keyword-only `cwd: str | None`.
   Line ~1586 is now
   `launch_cmd = f"cd {shlex.quote(cwd or os.getcwd())} && {shell_cmd}"`.
   `cwd=None` is byte-for-byte today's line. The `_TMUX_ARG_SAFE` script-file
   branch (~1591) writes the SAME `launch_cmd`, so the script path inherits
   the chosen cwd with no second launch string.
2. `spawn_window` (rotate.py:1638) gained `cwd: str | None = None` and
   threads it. It passes `cwd` to `_launch_window` ONLY when truthy, so the
   default call keeps today's exact 3-positional shape and every existing
   caller/stub is unchanged (two `test_rotate.py` loop stubs use a 3-arg
   `fake_launch`; a blanket keyword broke 11 of them on the first run).
3. `cmd_spawn` passes `cwd=_seat_worktree_cwd(root, _srow)` into
   `spawn_window` (~2097). `_srow` is non-None only for a seated spawn with a
   root, so every seat-less / root-less spawn is unchanged.
4. New helper `_seat_worktree_cwd` (rotate.py:1858) mirrors
   `_own_sessions_dir` exactly: empty/absent cell -> None (today's cwd);
   absolute cell used as-is; relative cell resolved against
   `locations.git_common_root(root) or root`, NEVER `os.getcwd()`.

### Missing-directory decision (step 4)

A cell that does not resolve to a directory falls back to None (today's cwd)
and prints a `[seating] worktree cell '<cell>' does not resolve to a
directory (<p>); launching in <cwd>` warning. Rationale: a `cd` into a
missing dir would make tmux's window die instantly and silently; a loud
fallback plus the name of the missing path is strictly more debuggable than a
dead window. Pinned by the fourth test.

### Tests

New file `extensions/agi/tests/test_rotate_spawn_worktree_cwd.py` (6 tests);
assertions read the WIRE (tmux argv `subprocess.run` receives, and the `cwd`
kwarg `spawn_window` receives):
- absolute cell -> launch cwd is that cell;
- relative cell -> resolved against a stubbed `git_common_root` pointing at a
  DIFFERENT dir than root, so a wrong resolver fails loudly;
- empty/absent cell -> `cwd is None` (byte-identical default), and
  `_launch_window` builds `cd {os.getcwd()} && ...`;
- missing dir -> `cwd is None` + the `[seating]` warning;
- `_launch_window` argv carries `cd <cwd> && <cmd>`;
- `spawn_window` threads a truthy cwd to `_launch_window`.

## Evidence

Command run:

    python3 -m pytest extensions/agi/tests/test_rotate*.py \
        extensions/agi/tests/test_sensei_rotate_out_audit.py -q

Result: **929 passed, 1 xfailed** (172.93s). Targeted subsets
`test_rotate.py + test_rotate_g1517.py + test_rotate_spawn_worktree_cwd.py`:
333 passed. Production diff: `git diff --numstat -- extensions/agi/bin/
rotate.py` = +46/-4 (ceiling 40; under 2x=80, no re-brief).

## Agent Notes
cmd_spawn now resolves the seat row worktree cell (relative to git_common_root, absolute as-is) via _seat_worktree_cwd and threads it through spawn_window into _launch_window's cd; empty/absent/missing-dir cell keeps today's os.getcwd() with a [seating] warning. 46 production lines, rotate suite 929 passed/1 xfailed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-b69818c1 (L5.20), verdict ACCEPTED, kid verdict stays proved. (1) WHAT THE INSTRUCTION SAID: the target claim is "cmd_spawn should cd into the row worktree cell when that cell is set, before launching the harness process"; the parent brief says a g15 claim "IS A BUILD ORDER, not a measurement", a kid passes its own tests and still fails if a parent negative probe falsifies it, and "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF". (2) WHAT THE MACHINE ACTUALLY DOES, read from the BYTES of commit c25b8b696 (numstat rotate.py +46/-4, new test file +130): rotate.py:1579 _launch_window gained keyword-only cwd and rotate.py:1608 is now `launch_cmd = f"cd {shlex.quote(cwd or os.getcwd())} and {shell_cmd}"`; spawn_window rotate.py:1650 gained cwd and 1800-1804 passes it ONLY when truthy; cmd_spawn rotate.py:2129 passes cwd=_seat_worktree_cwd(root,_srow); the new helper rotate.py:1872 resolves empty->None, absolute as-is, relative against locations.git_common_root(root) or root -- mirrored from _own_sessions_dir rotate.py:3554, never os.getcwd(). I did NOT trust the result file: I built and RAN three negative probes of my own (scratch .agi/sessions/iter-L5.20/a00-b69818c1/probe_parent.py, 3 passed) -- AUTH (seat-less/root-less resolves None, launch line stays the spawner cwd), GATE (worktree cell that is an existing FILE, and a whitespace-only cell, both refuse to None plus the warning), WIRE (real cmd_spawn through real spawn_window/_launch_window, only subprocess.run stubbed: the tmux argv was the _TMUX_ARG_SAFE script file and its line 2 cds git_common_root/<relative cell>, not root-relative). All three pass, so no conjunct is falsified and the proved record is not demoted. (3) THE NEAR MISS: a helper-only assertion -- `_seat_worktree_cwd` returning the right string -- satisfies the words and loses the mechanism, because cmd_spawn would still be free to drop the value before the launcher. The kid avoided it (test_spawn_* read the spawn_window kwarg, test_launch_window_cwd_is_the_cd_target reads the tmux argv) and my WIRE probe re-ran that boundary independently. The second near miss is the script-file path: a fix that only patched the inline launch line would pass every short-command test and still launch a real (16KB) successor in MAIN; probed by driving a real cmd_spawn whose line exceeds _TMUX_ARG_SAFE. (4) DEVIATION FROM A STANDING RULE: none by me. The kid exceeded its scaffolded line_ceiling (40) at production_lines=46; I did not re-brief because the target carries no `across K kids` clause to slice and 46 is within the documented 2x band, so the ceiling is a monitor here, not a gate. Noted as a caveat, not a defect.
<!-- THOUGHT:END -->

PARENT VERDICT: ACCEPTED as proved (L5.20, a00-b69818c1). Deliverables verified against the diff of commit c25b8b696: rotate.py +46/-4 at _launch_window/spawn_window/cmd_spawn/_seat_worktree_cwd, new tests/test_rotate_spawn_worktree_cwd.py (6 passed), node title set by the kid, evidence_runs names its own node. Three parent-run negative probes (auth/gate/wire) recorded in frontmatter, all pass -- no conjunct falsified. Caveats: production_lines 46 over the scaffolded ceiling 40 (monitor only, no across-K clause); the same relative-to-graph_root worktree-cell resolver now exists three times (_seat_worktree_cwd rotate.py, _own_sessions_dir rotate.py, _seat_tree_dir heal.py) -- a unification follow-on, not a defect of this round; rotate-self/loop were left alone deliberately because their spawner cwd already IS the post worktree, which is why the defect only bit cmd_spawn.
