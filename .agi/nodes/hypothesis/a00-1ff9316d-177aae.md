---
id: hypothesis:a00-1ff9316d-177aae
mint_id: 03ca561ab1404d25b725668c7255e531
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-1ff9316d
evidence_runs:
  - experiment:a00-1ff9316d-tasksmax
loop: goal:g7.33.17@s2
model: stealth/space-bunny-alpha
production_lines: 33
profile: balanced
role: kid
scaffold_hash: 86b75578c8f15a2d
season: 2
testable_claim: A round's kid cannot fan out processes past the box's bound.
title: A round scope carries a per-tree TasksMax, so a kid cannot fan out past the box bound
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-1ff9316d-177aae

## Claim

A round's kid cannot fan out processes past the box's bound.

DH.419's kid forked 127 pytest processes; user@ went over `memory.high` and DT's model
round was SIGTERMed. The suite lock and `spawn_budget` bound neither -- a bound on
AGENTS is not a bound on PROCESSES. `wrap_argv` gave every round a `MemoryMax` and
nothing else, so a round's own tree could always grow without limit.

## What would prove it

* the wrapped scope carries a per-TREE process bound on the SAME scope as `MemoryMax`
  (one bound, one scope, one argv);
* a fan-out past that bound is REFUSED -- the fork fails, the scope says so -- while the
  unwrapped path (`cap is None`) is byte-for-byte unchanged;
* a config with no cell still gets a shipped default, because a round may never commit
  `.agi/config.json`;
* the fallback that cannot enforce it says so by name rather than by silence.

## What would disprove it

* a fork past the bound still succeeds (the property is decorative on this box);
* or the bound is enforced by something the wrap does not actually control.

## Outcome

Ran as `experiment:a00-1ff9316d-tasksmax`: **proved on the systemd-run path**, and the
memory ordering it hangs on is **measured and confirmed** (6.000 GiB per round vs user@
`memory.high` 5.123 GiB -- the per-round cap can never bind first; reported, not edited).

The claim is proved for boxes whose `systemd_run_usable()` is True (this one, unforced).
It is **false for the prlimit fallback**, which has no per-tree spelling at all
(`RLIMIT_NPROC` is per-USER) -- that residual is named in the code and in the experiment,
not hidden, and a test fails the day anyone pretends otherwise.

Bound shipped: `--property=TasksMax=` from the cell `values.memcap.tasks_max`, default
**96** (a round's real tree is ~15 procs; the 127-fork incident is above it).

## Agent Notes
TasksMax on the round scope from values.memcap.tasks_max (default 96); 18-fork fan-out refused at 8, unwrapped path unchanged; memory ordering measured: 6.000GiB round cap > 5.123GiB user@ high; prlimit fallback residual named.

## Agent Notes
TasksMax on the round scope from values.memcap.tasks_max (shipped default 96); 18-fork fan-out refused at 8, unwrapped path unchanged; memory ordering measured: 6.000GiB round cap > 5.123GiB user@ high; prlimit fallback residual named in code.
