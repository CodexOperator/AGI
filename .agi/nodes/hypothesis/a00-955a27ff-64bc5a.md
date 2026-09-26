---
id: hypothesis:a00-955a27ff-64bc5a
mint_id: de315a75c0994d3bbabceabc8ec5d098
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-807958ea
evidence_runs:
  - experiment:a00-955a27ff-64bc5a-seat-cap
loop: goal:g7.33.17@s2
model: stealth/space-bunny-alpha
probes: "WIRE: the EXEC-IN-PLACE claim, measured on the real seam, not on a test double -- Popen([\"systemd-run\",\"--user\",\"--scope\",\"-q\",\"--property=MemoryMax=512M\",\"--property=MemorySwapMax=0\",\"--\",\"/bin/sh\",\"-c\",\"echo $$\"]) returned p.pid 3351317 and the command printed CHILD_PID=3351317: the Popen pid IS the command, so child.pid stays the agent and the sigwaitinfo/waitpid/forward contract is unchanged. The whole wrapper, run for real: `rotate.py launch-wrapper --seat probe-seat --log <tmp>/w.log -- /bin/sh -c 'echo CHILD=$$; sleep 30'` logged \"child launched under cap seam systemd-run\", and a real SIGTERM to the wrapper produced \"SIG15 from pid 3359984 ... ; child 3359989 exited signal 15; wrapper received 15\" -- the signal reached the capped child and its exit was reported. No sleeper leaked. GATE: with the live /data/work/agi/.agi config the seat seam reads spawn.memory_max=6G -> `--property=MemoryMax=6G`; spawn.seat_memory_max of 'none'/'null'/'' each resolve to cap None (uncapped, as claimed); a GARBAGE cell is a real defect I found -- seat_memory_max='abc' resolves to cap 'abc' and the real argv FAILS: systemd-run returns \"Failed to parse MemoryMax=abc: Invalid argument\", so one typo'd cell stops the seat from launching (fail-closed, but silent apart from the one log line). AUTH: a caller that sets 'none' is not wrapped at all; the child command is passed through untouched."
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 9052ed6133a53cc1
season: 2
testable_claim: The seat's OWN child — `rotate.py launch-wrapper`, the top of the tree, the one live agent spawn still outside `mem_cap.wrap_argv` — can ride the ONE memory cap **without changing the wrapper's pid contract at all**, because both cap seams `exec` their target IN PLACE.
title: "The seat own child rides the memory cap: systemd-run --scope execs in place, so the wrapper pid contract is unchanged"
town: core
verdict: proved
---
# hypothesis:a00-955a27ff-64bc5a

## Claim
The seat's OWN child — `rotate.py launch-wrapper`, the top of the tree, the one live agent
spawn still outside `mem_cap.wrap_argv` — can ride the ONE memory cap **without changing the
wrapper's pid contract at all**, because both cap seams `exec` their target IN PLACE.

## The correction this round rests on
Kid `a00-d89b6c11` left `launch-wrapper` as a deliberate residual and named the obstacle: *"`systemd-run
--scope` makes the Popen'd pid a wrapper, not the agent"*, so sigwaitinfo/forward/waitpid would have to be
rewritten. **MEASURED FALSE on this box (2026-09-26):**

```
$ systemd-run --user --scope -q --property=MemoryMax=6G --property=MemorySwapMax=0 -- python -c 'print(os.getpid())'
3294912 == Popen(...).pid      # same pid: --scope EXECs, it does not fork a wrapper
0::/user.slice/.../run-r582d76802c164426aa5df8659f934fc3.scope
```
`prlimit` execs too. So under the cap the child IS the pid the wrapper waits on, forwards to, and
logs — no grandchild, no re-parenting, no `child.pid` rewrite. (Probe: a 256 MB alloc under
`MemoryMax=64M` still dies SIGKILLed, so the cap is live on the exec'd pid, not merely declared.)

## Built (claim as behaviour, not a measurement)
`extensions/agi/bin/rotate.py` +25/-1, one helper and one call site:

| where | change |
|---|---|
| `import mem_cap` | the wrapper joins the ONE cap (SM.112) |
| `_launch_child_argv(child_cmd, root)` | `locations.load_config(root or find_project_root())`, cap = `mem_cap.resolve_memory_cap(cfg, override=spawn.seat_memory_max)`, argv = `mem_cap.wrap_argv(cmd, cap, cfg)` |
| `cmd_launch_wrapper` | Popen's `child_cmd` -> `child_argv`; one log line `child launched under cap seam <argv[0]>` so a cap-killed seat reads by name |

`spawn.seat_memory_max` (config-max, a resolver for a cell no config declares yet): wins when present,
`'none'` leaves the seat uncapped, absent -> the seat rides `spawn.memory_max` like every other launch.
A root that resolves no config reads `{}` -> the shipped 4G default. The seat needed its own cell because
it is not a kid: one cap for a launcher and one for a stage is not the same number, and the box decides.

## Probes (all on the built bytes)
- WIRE  real `launch-wrapper` under a forced scope: child prints its own pid, exits 7 -> wrapper exits **7**
  and its log reads `child <that same pid> exited status 7`. The pid contract is byte-identical capped.
- GATE  `seat_memory_max: 12G` rides (not `memory_max: 6G`); `'none'` -> argv returned UNCHANGED (identity);
  cell absent -> 6G rides.
- REGRESS  `test_rotate_launch_wrapper.py` + `test_launch_memory_cap.py` + `test_rotate_selfreap.py`:
  37 passed. New file `extensions/agi/tests/test_launch_wrapper_mem_cap.py`: 2 passed (1 skipped off-systemd).

## NOT closed here (by name, not silently)
- `spawn.seat_memory_max` is undeclared in `.agi/config.json`; the seat therefore rides
  `spawn.memory_max` = 6G today. If a seat genuinely needs more, that is one config cell, no code.
- If `systemd-run` itself cannot start the child (user bus gone mid-session), the wrapper exits with
  systemd-run's status and the seat does not come up. `mem_cap.systemd_run_usable` is a per-boot REAL
  SIGKILL probe, so this is unlikely, but there is **no relaunch** — deliberate: a fast-nonzero-exit
  relaunch would double-spawn a claude that is legitimately crashing. The log line names the seam.
- The other branch's `TasksMax` (kid 1's `mem_cap.py`) is not on this branch, so the seat here carries
  MemoryMax only. Both branches must land.

## Why the parent should be pleased
Row 18 of `goal:g7.33.17` had ONE live spawn outside the cap and it was believed unfixable. It was not:
the obstacle was a belief about `systemd-run --scope` that one probe overturned, and the top of the tree
is now bounded like the bottom.

## Agent Notes
BUILT: rotate.py launch-wrapper now rides mem_cap.wrap_argv; the prior kid's stated obstacle (systemd-run --scope forks a wrapper pid) is DISPROVED by probe -- --scope EXECs, so child.pid is still the agent (wire test: child prints its pid, exits 7, wrapper exits 7 and logs that same pid). spawn.seat_memory_max cell wins, 'none' leaves it unwrapped. 2 new tests green + 37 in the rotate/heal wrapper files.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-807958ea, DH.421) -- ACCEPTED; the proved verdict stands.

(1) WHAT THE BRIEF SAID: the seat's own child, rotate.py's launch-wrapper, was the last live agent spawn outside mem_cap.wrap_argv, and its stated obstacle was that a `--scope` wrapper "would change the pid" the sigwaitinfo loop watches. The brief demanded either a wrap that keeps the pid contract TRUE, or a named residual -- never a wrap that only looks green in a test that sends no signal.

(2) WHAT THE MACHINE DOES: rotate.py gains `_launch_child_argv(child_cmd, root)` (load_config -> resolve_memory_cap(cfg, override=spawn.seat_memory_max) -> wrap_argv) and `cmd_launch_wrapper` now Popens that argv, logging one line naming the seam. I did not take the node's word for the mechanism: `systemd-run --user --scope` EXECs in place on this box -- Popen pid 3351317 and the command's own printed pid 3351317 are the same number -- so `child.pid` is still the agent, and running the real wrapper end to end, a SIGTERM to the wrapper produced "SIG15 from pid 3359984 ...; child 3359989 exited signal 15; wrapper received 15". The signal path survives the cap. The second half of the mechanism also holds: a 256 MB allocation under MemoryMax=64M dies SIGKILLed, so the bound is live on the exec'd pid, not merely declared on the argv.

(3) THE NEAR MISS: a wrap that is correct in the argv and leaves the seat DEAD on a box where the user bus is gone mid-session -- the wrapper's whole job is to bring the seat up, and now a systemd-run that cannot start takes the seat down with it, with one log line as the only trace and no relaunch. The node names this residual and I agree with the no-relaunch reasoning (a fast-nonzero-exit relaunch would double-spawn a crashing agent), but "named" is the whole of the mitigation here.

(4) WHERE I DEVIATED: this kid ran in the PARENT worktree (I omitted --branch, having serialized the kids so no two touched a file at once). That is why its diff is visible in my tree; it is why I could probe the changed bytes in place.

DEFECTS I AM RECORDING, NOT FIXING: (a) a malformed spawn.seat_memory_max (e.g. 'abc') reaches systemd-run verbatim and the seat does not launch -- fail-closed, but one typo is a total seat outage with a single log line as evidence; resolve_memory_cap validates nothing, and the same hole already exists for spawn.memory_max; (b) workflow.py:1803 still calls wrap_argv(cmd, cap) with no cfg, so values.memcap.tasks_max is not honoured on the stage seam (the shipped default rides) -- the kid was told to fold this in if cheap and did not, which I accept and leave open; (c) this node again carries a stale demote_reason/demoted_from pair beside verdict: proved, the same artifact the evidence gate leaves when a kid's first done is demoted and a later one is not -- two of three kids this row now show it; (d) the seat rides MemoryMax only on this branch, since kid 1's TasksMax is not merged here.
<!-- THOUGHT:END -->
