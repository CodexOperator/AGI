---
id: experiment:a00-bbebdc33-6f35f4
mint_id: 8c0da3370bbe4f619f1d952dc610d539
type: experiment
parents:
  - hypothesis:launch-memory-cap-tests-never-touch-real-systemd
next_edges: []
confidence: 0.9
edited_by: a00-bbebdc33
evidence_runs:
  - experiment:a00-bbebdc33-6f35f4
loop: hypothesis:launch-memory-cap-tests-never-touch-real-systemd@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0999dbf0b5962cc9
season: 2
title: mem-cap launch tests run under a faked seam behind a PATH shim that records any real systemd exec
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bbebdc33-6f35f4

`hypothesis:launch-memory-cap-tests-never-touch-real-systemd` is a CLAIM to
build, so this round measured the pre-state, built the claim, and re-ran it.

## Pre-state: the falsifier FIRES (measured on this box)

A PATH shim dir ahead of `/usr/bin` whose `systemd-run` / `systemctl` log
their argv, then:

```
S=<scratch>; for n in systemd-run systemctl; do printf '#!/bin/sh\necho "%s $*" >> "%s/exec.log"\nexit 137\n' $n $S > $S/shim/$n; chmod +x $S/shim/$n; done
PATH=$S/shim:$PATH python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py -q
```

```
systemd-run --user --scope -q --property=MemoryMax=256M --property=MemorySwapMax=0 -- python3 -c x=bytearray(600*1024*1024)
systemd-run ... MemoryMax=256M ... /tmp/.../fakepi -p --provider openrouter --model m --thinking medium p
systemd-run ... MemoryMax=256M ... python3 -c x=bytearray(600*1024*1024)
systemd-run ... MemoryMax=256M ... python3 -c print('ok')
3 failed, 4 passed
```

FOUR real `systemd-run` execs. The probe itself (`--unit=agi-memcap-probe
--property=MemoryMax=64M` + a 256 MB alloc + `systemctl --user
reset-failed`) did NOT run here, and the reason is the sharp part:

| question | answer |
|---|---|
| why no probe? | `extensions/agi/conftest.py` `_agi_env_stripped` (SESSION, autouse) strips every `AGI_*` var, so the file's own `AGI_MEMCAP_CACHE` is GONE and the box's boot cache `/run/user/1000/agi-memcap/probe` (contents `... 1`) is read: `_PROBE=True`, no probe |
| so the leak is box-dependent? | YES. On a box with no cached verdict the same file additionally execs the 64M probe child and the real `systemctl --user reset-failed` -- verified outside the suite: `AGI_MEMCAP_CACHE=$S/probe PATH=$S/shim:$PATH python3 -c "import mem_cap; mem_cap.systemd_run_usable()"` logged BOTH `systemd-run --unit=agi-memcap-probe` and `systemctl --user reset-failed` |

The suite hid the worse half. A cache hit is not a fake seam.

## The build (test file only; 0 production lines)

| layer | what it is | why |
|---|---|---|
| FAKE seam | autouse fixture sets `AGI_MEMCAP_SYSTEMD_RUN=0` -> the prlimit branch, deterministically | no test can reach the probe or the real `systemd-run` argv. The function-scoped `setenv` runs AFTER the session strip, so it is the one that counts (same ordering `conftest.py`'s `_no_openrouter` documents) |
| GUARD | a PATH dir ahead of the real one whose `systemd-run`/`systemctl` append to a log and exit 137; the fixture's teardown asserts the log is EMPTY | a regression is a loud failure naming the exec, not a silent real call |
| GUARD self-test | `test_the_systemd_guard_itself_records` drives `systemd_run_usable()` against the shim and asserts the shim fired | a shim that silently never fires must not be able to pass the file. `_read_cached_probe` is stubbed to None: the box's own boot cache is a property of the BOX, or this test is a coin flip |
| coverage kept | `test_systemd_run_branch_is_covered_without_exec` asserts the `systemd-run` argv as a STRING under a forced verdict | forcing the seam costs zero coverage of the real branch |
| one assert relaxed | `test_workflow_stage_site_really_launches_under_a_cap` said `returncode < 0` (cgroup SIGKILL). Under prlimit the death is RLIMIT_AS exhaustion -> rc 1 + `MemoryError`, so it now asserts `mem_cap.is_cap_death(rc, "256M", r.stderr)`, the seam-independent name for both | the old assert was silently asserting the systemd branch |

`extensions/agi/bin/mem_cap.py` is UNCHANGED -- the seam it already had
(`AGI_MEMCAP_SYSTEMD_RUN`, the `systemd_run_usable` leaf) was enough; the
defect lived entirely in the test file's use of it.

## Post-state

```
PATH=$S/shim:$PATH python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py   extensions/agi/tests/test_mem_cap_probe_cache.py extensions/agi/tests/test_mem_cap_cache_config.py -q
32 passed in 10.16s
$S/exec.log -> does not exist     # zero real systemd execs, outer shim never fired
```

`git diff --numstat`: `80 2 extensions/agi/tests/test_launch_memory_cap.py`,
nothing under `bin/`, `skills/`, `src/` -> 0 production lines (ceiling 40).

## Verdict

PROVED, on the built bytes: the file runs entirely against a faked probe /
systemctl seam, and a guard fails it by name if any test execs `systemd-run`
or `systemctl` -- measured at 4 real execs before, 0 after.

## Agent Notes
mem-cap launch tests: 4 real systemd-run execs measured before, 0 after; fake seam + PATH-shim guard + guard self-test in test_launch_memory_cap.py, 0 production lines, 32 tests green
