---
id: experiment:a00-91c69720-576915
mint_id: c1db139bcaf241d1b965903f2b0ec41a
type: experiment
parents:
  - hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom
next_edges: []
confidence: 0.8
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-91c69720-576915
line_ceiling: 40
loop: hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 6198243bb6661db8
season: 2
title: "Memory cap enforced: swap-max 0 plus a real-kill probe, 7/7 + 222 green"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-91c69720-576915

## Experiment

SM.112 corrective round 2: the memory cap in `extensions/agi/bin/mem_cap.py`
was a silent no-op on a swap-enabled box. Two fixes to `wrap_argv`'s
systemd-run branch and one to the probe:

1. `--property=MemoryMax=<cap>` (long form) replaces `-p MemoryMax=<cap>`.
   On THIS box `-p` was already accepted (measured: `MemoryMax=268435456`),
   so this change is defensive/cosmetic here, not the operative fix -- see
   the falsified sub-claim below.
2. `--property=MemorySwapMax=0` is added alongside it. **This is the fix.**
   A 4G swapfile is live (`swapon --show`), and cgroup v2 `memory.max` alone
   does not SIGKILL when swap absorbs the overage.
3. `systemd_run_usable()` now probes ENFORCEMENT, not launchability: once per
   process it launches a real 256MB allocation past a real 64M cap via the
   corrected invocation and requires the observed `-SIGKILL`.
4. `dispatch.py` / `workflow.py` untouched -- their wiring was already
   correct.

## Evidence

PRE-FIX measured on this box (raw, before touching the file):

```
$ systemd-run --user --scope -q -p MemoryMax=256M -- \
    python3 -c "x=bytearray(600*1024*1024); print('allocated', len(x))"
allocated 629145600        # 600MB under a 256M cap
$ echo $?
0                          # silent no-op, the hypothesis's own falsifier

$ systemctl --user show <scope> -p MemoryMax -p MemorySwapMax
MemoryMax=268435456
MemorySwapMax=infinity     # <- the absorption path

$ systemd-run --user --scope -q --property=MemoryMax=256M \
    --property=MemorySwapMax=0 -- python3 -c "x=bytearray(600*1024*1024)"
Killed
$ echo $?
137                        # 128+SIGKILL: real enforcement
```

`python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py -q`:

```
.......                                                                  [100%]
7 passed in 0.91s
```

Regression, same round:
`python3 -m pytest extensions/agi/tests/test_workflow.py
extensions/agi/tests/test_workflow_slice_isolation.py
extensions/agi/tests/test_dispatch.py -q`:

```
222 passed, 6 warnings in 129.59s (0:02:09)
```

Post-fix functional probe on the built bytes:

```
probe True
['systemd-run', '--user', '--scope', '-q', '--property=MemoryMax=256M',
 '--property=MemorySwapMax=0', '--', 'echo', 'x']
rc -9 cap_death True
```

MEASURED PRODUCTION LINES: `git diff --numstat -- mem_cap.py` -> `12 5`,
i.e. 12 added / 5 removed against HEAD; well inside the 40 ceiling.

## Falsified sub-claim (named, not hidden)

The brief's Bug 1 ("`-p` short flag is silently swallowed to 4G on this
box") did NOT reproduce here: with `--unit` pinned,
`systemd-run --user --scope -q -p MemoryMax=256M -- sleep 4` showed
`MemoryMax=268435456`. The long form is kept anyway (it is the canonical
spelling and costs nothing), but the operative defect was Bug 2 alone.
The prior parent's diagnosis ("launchability is not enforceability") is
correct and is now the probe.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Standing in for the dead parent (a00-0c39bd83, died-no-work at 305s, never reviewed its own kid). Independently re-ran extensions/agi/tests/test_launch_memory_cap.py: 7/7 passed, matching the kid own claim exactly this time (unlike the prior round, where the same claim did not reproduce). Independently measured the diff: git diff --cached --numstat -- mem_cap.py = 12 added/5 removed, matches the claimed 12 production lines. ACCEPTED: MemorySwapMax=0 alongside MemoryMax is the real fix (this box has a live 4G swapfile, and cgroup v2 memory.max alone does not SIGKILL while swap absorbs the overage -- confirmed by the kid own raw pre-fix repro showing a 600MB allocation succeed under a 256M cap with MemorySwapMax=infinity, then fail correctly once MemorySwapMax=0 is set). The prior corrective brief own Bug 1 guess (the -p short flag being swallowed) did not reproduce and the kid says so plainly rather than padding -- the long --property= form is kept anyway as the canonical spelling, cosmetic here. Verdict proved:0.8 stands as delivered.
<!-- THOUGHT:END -->
Raw output, screenshots, logs.

## Agent Notes
Memory cap now really enforces: --property=MemorySwapMax=0 alongside MemoryMax (swap was absorbing the overage on this 4G-swap box) and systemd_run_usable() became an enforcement probe requiring an observed SIGKILL. 7/7 target + 222 regression green; 12 production lines. Dispatch-side cap-death naming not directly exercised this round.
