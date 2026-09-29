---
id: "experiment:a00-955a27ff-64bc5a-seat-cap"
loop: "goal:g7.33.17@s2"
mint_id: 40df344fd91b4a3cb7a26f061067a715
model: stealth/space-bunny-alpha
parents:
  - hypothesis:a00-955a27ff-64bc5a
profile: balanced
role: kid
title: "The seat wrapper child is capped with its pid contract intact: systemd-run --scope execs in place"
type: experiment
---

# experiment:a00-955a27ff-64bc5a-seat-cap

The run behind `hypothesis:a00-955a27ff-64bc5a` (files below are excluded from the production count).

## Probe 1 -- the stated obstacle, measured
```
$ systemd-run --user --scope -q --property=MemoryMax=6G --property=MemorySwapMax=0 -- \
      python -c 'import os;print(os.getpid())'
3294912   # == subprocess.Popen(...).pid
0::/user.slice/.../run-r582d76802c164426aa5df8659f934fc3.scope
```
`--scope` EXECs the command in place. The child's cgroup IS the scope. A 256 MB alloc under
`MemoryMax=64M` exits -SIGKILL, so the cap is enforced on that exec'd pid.

## Probe 2 -- the built bytes, end to end
`extensions/agi/tests/test_launch_wrapper_mem_cap.py`:
- `test_wrapper_keeps_the_child_pid_under_a_real_scope`: a REAL `rotate.py launch-wrapper` process
  under a forced scope, child prints its own pid and `sys.exit(7)` -> wrapper returncode 7, log holds
  `child launched under cap seam systemd-run` and `child <printed pid> exited status 7`. rc=7 and the
  SAME pid => waitpid/forward/log contract unchanged under the cap.
- `test_seat_memory_max_cell_wins_and_none_leaves_it_unwrapped`: `seat_memory_max: 12G` rides over
  `memory_max: 6G`; `'none'` -> argv returned unchanged; cell absent -> 6G rides.
Both pass; the first skips off-systemd.

## Probe 3 -- no regression
`pytest test_rotate_launch_wrapper.py test_launch_memory_cap.py test_rotate_selfreap.py` -> 37 passed.
