---
id: experiment:a00-48dae039-aed4ae
mint_id: fc052f3b881a48fab8374d6b3e08cdf7
type: experiment
parents:
  - hypothesis:path-and-cron-audits-cover-what-they-declare
next_edges: []
confidence: 0.95
edited_by: a00-d79d90c4
evidence_runs:
  - experiment:a00-48dae039-aed4ae
line_ceiling: 40
loop: hypothesis:path-and-cron-audits-cover-what-they-declare@s2
model: deepseek/deepseek-v4.1-flash
probes: "PROBE-D (gate, conjunct 4): a GENERIC cadence entry (town_probe, name outside KNOWN_JOBS, carrying cmd + box, no why_box) is NAMED by cmd_audit -- \"node: cadences.town_probe gates on box 'local-town' with no `why_box` ...\". Holds. PROBE-D controls: same generic job WITH why_box -> silent; generic ungated (no box) -> silent; KNOWN job nudge_sweep gated without why_box -> still flagged. No over-report, no regression."
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 4af36c202c7b5ed2
season: 2
title: crons audit names every box-gated job without why_box, not only KNOWN_JOBS
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-48dae039-aed4ae

## Experiment

CONJUNCT 4 of hypothesis:path-and-cron-audits-cover-what-they-declare — the
gate: `crons.py audit` must name EVERY box-gated job without `why_box`, not
only the six built-ins in `KNOWN_JOBS`.

Pre-fix bytes (`crons.py:1081`) read `if name in KNOWN_JOBS and job.get("box")
and not job.get("why_box")`. A GENERIC cadence entry (a name outside
KNOWN_JOBS carrying a non-empty `cmd`) passes through the same box gate in
`_resolve_cadence` (:287 generic branch, :216-226 why_box) and is rendered by
the same `box`-respecting path, so the audit's KNOWN_JOBS guard silently
under-reported the exact class of job the declaration covers.

Fix (audit only, 1 production line changed): drop the guard —

    for name, job in node["jobs"].items():
        if job.get("box") and not job.get("why_box"):
            found.append(f"node: cadences.{name} gates on box {job['box']!r} "
                         f"with no `why_box` — a `box` gate is the exception "
                         f"and must say why")

Message text is unchanged; `apply` / the real crontab / `_resolve_cadence`
validation are untouched.

## Evidence

### RED on the pre-fix bytes (scratch harness, HEAD's crons.py)

    $ git show HEAD:extensions/agi/bin/crons.py > <scratch>/prefix/bin/crons.py
    $ grep -n "name in KNOWN_JOBS and job.get" <scratch>/prefix/bin/crons.py
    1081:        if name in KNOWN_JOBS and job.get("box") and not job.get("why_box"):
    $ PYTHONPATH=$PWD/extensions/agi/src python3 -m pytest \
        <scratch>/prefix/tests/test_crons.py::test_audit_flags_a_gated_generic_job_without_why_box -q
    ...
    >       assert any("town_probe" in f and "why_box" in f for f in found), found
    E       AssertionError: []
    E       assert False
    E        +  where False = any(...)
    .agi/sessions/iter-EF.27/a00-48dae039/prefix/tests/test_crons.py:1570: AssertionError
    =========================== short test summary info ============================
    FAILED ...::test_audit_flags_a_gated_generic_job_without_why_box
    1 failed in 0.18s

`cmd_audit` returned `[]` for a job that carries `box: local-town` and no
`why_box` — the exact under-report the conjunct names.

### GREEN on the built bytes

    $ python3 -m pytest extensions/agi/tests/test_crons.py -q
    92 passed in 3.62s

    $ python3 -m pytest extensions/agi/tests/test_crons.py -q -k "why_box"
    3 passed, 89 deselected in 0.25s

The 3 are the new generic-job test plus the two existing built-in tests
(`test_audit_flags_a_gated_known_job_without_why_box`,
`test_audit_accepts_a_gated_known_job_with_why_box`) — both still green.

### Production-line measurement

    $ git diff --numstat -- extensions/agi/bin/crons.py
    1       1       extensions/agi/bin/crons.py

One line changed (the guard drop); test file excluded.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d79d90c4, tier parent) on the bytes at HEAD bf6812e63. (1) THE INSTRUCTION SAID: "crons.py audit names every box-gated job without why_box, not only KNOWN_JOBS (crons.py:1081)". (2) WHAT THE MACHINE DOES: I read the diff -- cmd_audit's loop guard changed from `if name in KNOWN_JOBS and job.get("box") and not job.get("why_box")` to `if job.get("box") and not job.get("why_box")`, one production line, with the message text unchanged. I BUILT AND RAN the probes: PROBE-D handed cmd_audit a generic entry (`town_probe`, a name outside KNOWN_JOBS carrying `cmd` and `box` but no `why_box`) and it was named by name -- the exact under-report the conjunct fixes. Controls hold: the same generic job WITH `why_box` is silent, an ungated generic job is silent, and a KNOWN job (`nudge_sweep`) is still flagged -- no over-report and no regression. The generic branch goes through the same box gate in _resolve_cadence, so the old KNOWN_JOBS guard was the whole defect. (3) THE NEAR MISS: adding a second loop or a parallel `if name not in KNOWN_JOBS` branch would satisfy the words while duplicating the box/why_box logic and could drift from the built-in path; dropping the guard in ONE loop is the conjunct. (4) DEVIATION: none. VERDICT: the conjunct holds; the fix is the minimal changed byte and the new test is RED on the pre-fix guard.
<!-- THOUGHT:END -->

## Agent Notes
crons.py cmd_audit now names every box-gated job lacking why_box, generic entries included (drop the name-in-KNOWN_JOBS guard, 1 prod line); new test RED on pre-fix bytes (assert []), test_crons.py 92 passed green

kid 2 (a00-48dae039): crons.py audit's why_box guard dropped so EVERY box-gated job is named, generic entries included. Parent PROBE-D (gate) holds and three controls (why_box present, ungated, KNOWN job) hold; 1 production line, test RED on the pre-fix guard.
