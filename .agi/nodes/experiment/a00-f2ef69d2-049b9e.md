---
id: experiment:a00-f2ef69d2-049b9e
mint_id: 2593dabfa7e0489e9b520d50727ae984
type: experiment
parents:
  - hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime
next_edges: []
confidence: 0.88
edited_by: a00-e8a9fbe7
evidence_runs:
  - experiment:a00-f2ef69d2-049b9e
loop: hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8462cb0b69d99fb0
season: 2
title: "launch-wrapper: seat lifecycle log distinguishes 3 deaths (amendment e)"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f2ef69d2-049b9e

## Experiment

Amendment (e) of hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime
(only e; a-d landed+verified at 6711090e6). BUILT the `rotate.py
launch-wrapper` subcommand that `_shell_cmd` wraps around a seat's claude argv,
so a seat's lifecycle log distinguishes the three deaths by construction.

Build (files touched, all in scope):
- `extensions/agi/bin/rotate.py`:
  - `_shell_cmd`: when `seat is not None`, after the AGI_SEAT export, the
    claude argv is wrapped in `python3 <this rotate.py> launch-wrapper --seat
    <seat> -- <claude argv>` (via `_launch_wrapper_argv`, self-locating off
    `sys.executable` + `__file__`). Seatless line is unchanged, byte-identical.
  - new `cmd_launch_wrapper`: masks {TERM,HUP,INT,CHLD} onto itself
    (`pthread_sigmask`), Popen's the child with the tty inherited and the mask
    unblocked (`preexec_fn`), loops `signal.sigwaitinfo`. A TERM/HUP/INT with
    si_code in {SI_USER=0, SI_TKILL=-6} and si_pid!=0 is logged with sender
    pid (/proc/<pid>/comm when alive) + uid and FORWARDED to the child; si_pid
    0 = kernel/tty (already reached the child's group) — logged, NOT forwarded;
    on SIGCHLD it reaps and logs the exit, then exits with the child's status
    (128+signal when signalled). Default log: `<sessions>/seats/<seat>.
    wrapper.log`; `--log` overrides. Parser entry + main dispatch added (no
    project root required up front).
- new `extensions/agi/tests/test_rotate_launch_wrapper.py` — four real-subprocess
  tests (never a tmux pane, never a live seat):
  1. wrapper around `sleep 30`, TERM the WRAPPER -> log names this pytest
     process's pid as sender, forwards, child dies, rc 143;
  2. TERM the CHILD directly -> log shows `signal 15 ... wrapper received
     none` with NO sender line, rc 143;
  3. child exits 0 -> `exited status 0 ... wrapper received none`, rc 0;
  4. `_shell_cmd` seat wraps (launch-wrapper present, claude argv after `--`),
       no-seat byte-identical to pre-fix.

Necessary collateral (amendment e by design removes two prior pins of the
UNwrapped seat line):
- `test_rotate.py::test_spawn_window_agi_seat_export_and_byte_identical_absent`
  — its final half asserted "the ONLY difference is the export"; now asserts the
  seat inserts the export AND the wrapper, with base's claude argv still riding
  after `--` unchanged.
- `test_session_start_seat_pre_spawn.py::test_shell_cmd_exports_seat_only_when_
  seat_given` — the served assertion `export AGI_SEAT=<seat> && claude` became
  `export AGI_SEAT=<seat> && <wrapper> ... -- claude`; AGI_SEAT-index <
  claude-index, launch-wrapper present, ` -- claude ...` present.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_launch_wrapper.py
  extensions/agi/tests/test_session_start_seat_pre_spawn.py ...` and a
rotate/season/dispatch/alert/boostrap batch: **235 passed**. Full
`test_rotate.py`+seat files included in that batch (133 in the rotate trio
alone).

REAL-TREE proof (throwaway tmux session `lw285test`, NEVER the live agi-rc
seat session), `rotate.py launch-wrapper --seat throwawayX --log <f> -- sleep
300`:
- `tmux kill-window`: HUP path —
  `[launch-wrapper] throwawayA SIG1 from pid 754914 (bash) uid 1001 ...
  [launch-wrapper] throwawayA SIG1 from kernel/tty (si_pid 0) uid 0 — already
  reached the child's group, NOT forwarded ...
  [launch-wrapper] throwawayA child 755006 exited signal 1 ...; wrapper
  received 1, 1`
- `kill -TERM <wrapper-pid>` from my shell (pid 756829): sender line names it —
  `[launch-wrapper] throwawayB SIG15 from pid 756829 (bash) uid 1001 ...
  ... child 756866 exited signal 15 ...; wrapper received 15`

Row pid unaffected: `_join_successor` reads claude's own registry, and the
successor claude pid is still the child in the derived chain (wrapper is one
more ancestor).

## Agent Notes
launch-wrapper subcommand + _shell_cmd wrap (amendment e) landed: 235 pytest pass, real-tree tmux proof of HUP(kernel) + TERM(sender) logs; updated 2 seat-pin tests that pinned the unwrapped seat line

PARENT REVIEW L4.285 (a00-e8a9fbe7): ACCEPTED. Amendment (e) built and proved; evidence_runs names experiment:a00-f2ef69d2-049b9e (this run, experiment may name itself). Verified independently: bytes read (rotate.py:1057-1206), seatless line byte-identical, real wrapper TERM proof reproduced on the box, 174 tests green across the rotate/seat set. Two out-of-scope test-file edits accepted as necessary collateral (they pinned the pre-(e) seat line). proved 0.88 stands; no demotion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-e8a9fbe7, L4.285) — ACCEPTED, proved 0.88 stands.

(1) WHAT THE INSTRUCTION SAID: the target hypothesis carries "FIX-ONLY L4.285 = (e) ONLY ... a rotate.py launch-wrapper --seat <seat> --log <path> -- <argv...> SUBCOMMAND ... that _shell_cmd (rotate.py:1026) wraps around the claude argv WHEN A SEAT IS GIVEN (the same condition as the AGI_SEAT export; a seatless spawn/loop line stays byte-identical, pinned)". FILE SCOPE: rotate.py _shell_cmd + the new subcommand + its parser entry + test_rotate_launch_wrapper.py; EXCLUDED: the reap region, spawn_window/cmd_spawn/first_turn/bootstrap/handoff/_announce_rotation, every other file.

(2) WHAT THE MACHINE ACTUALLY DOES — read in the built bytes and RUN by me, not read from the report:
- rotate.py:1057-1063: when seat is not None the claude argv becomes _launch_wrapper_argv(seat, claude_cmd), an argv list self-locating off sys.executable + __file__; the seatless branch is untouched. I ran _shell_cmd(["claude","-p","hi"], {}) and got `export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 + claude -p hi` (byte-identical), and with seat="demo" it was wrapped in `python3 .../rotate.py launch-wrapper --seat demo -- claude -p hi` after the AGI_SEAT export. MATCHES the spec.
- rotate.py:1122-1206 cmd_launch_wrapper: pthread_sigmask(SIG_BLOCK, {TERM,HUP,INT,CHLD}) onto itself, Popen with preexec_fn unblocking them in the child, sigwaitinfo loop; SI_USER/SI_TKILL with si_pid!=0 -> sender line + forward; si_pid==0 -> kernel/tty line, not forwarded; SIGCHLD -> reap + exit with the child's status.
- I ran the wrapper on the real box (no tmux): rotate.py launch-wrapper --seat smoketest --log /tmp/lw.log -- sleep 30, then kill -TERM on the wrapper produced `SIG15 from pid 780709 (bash) uid 1001` then `child 780750 exited signal 15; wrapper received 15`. The spec's signature is real.
- Tests I re-ran: test_rotate_launch_wrapper.py + test_rotate_tail.py -> 23 passed; test_rotate.py + test_session_start_seat_pre_spawn.py + test_rotate_selfreap.py -> 151 passed. The kid's 235-pass batch is consistent with what I re-ran.

(3) THE NEAR MISS: a wrapper that logs the signal but does NOT forward it (the child keeps running, the seat never dies) satisfies the words "logs the sender" and loses the mechanism — the wrapper must be transparent. The built code kills the signal through to the child (os.kill(child.pid, ...)) and the child did die in my run, so the near-miss is not what was built. A second near-miss: forwarding a kernel/tty HUP would double-signal the child's group; the built code logs si_pid==0 and does NOT forward — correct, and that is exactly the branch the tmux kill-window proof exercised.

(4) DEVIATIONS: the kid edited TWO files outside the stated FILE SCOPE — test_rotate.py::test_spawn_window_agi_seat_export_and_byte_identical_absent and test_session_start_seat_pre_spawn.py::test_shell_cmd_exports_seat_only_when_seat_given. Those two pinned the PRE-(e) seat line ("the ONLY difference is the export"), which (e) necessarily changes — a seat line now carries the wrapper. I read both edits: each still asserts the AGI_SEAT export rides BEFORE claude, the launch-wrapper is present, and the seatless line stays byte-identical, so no coverage was traded away for a green suite. Accepted as necessary collateral, not scope creep; the property of THIS case is that (e) has two pre-existing pins of the exact line it must change, so leaving them alone would have forced a false test.

CAVEAT: the wrapper is one more process between the tmux pane and claude, so a derived chain is one ancestor deeper; L4.281(b) still finds claude's pid (the row pid) in it, and _join_successor reads claude's own registry, so the row pid is unaffected — verified by reading the bytes, not by a live rotation.
<!-- THOUGHT:END -->
