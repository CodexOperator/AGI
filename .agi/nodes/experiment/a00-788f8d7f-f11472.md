---
id: experiment:a00-788f8d7f-f11472
mint_id: e6abba767d8e424cb29eba9e438e00d3
type: experiment
parents:
  - hypothesis:a00-0d182e77-3f4501
confidence: 0.9
evidence_runs:
  - experiment:a00-788f8d7f-f11472
scaffold_hash: 2e127f8f500cab2a
title: A00 788f8d7f f11472
verdict: proved
wired_at: 1788245310
wired_from: a00-788f8d7f
---


# experiment:a00-788f8d7f-f11472

## Experiment

Executed the two-line gate change plus the kid-contract change from
`hypothesis:a00-0d182e77-3f4501`, then ran the hypothesis's seven proof
checks.

**Edits made (4 files, all in the tracked tree, no node files touched):**

1. `.agi/context/schemas/[mvp].md` — `allowed_parents:`
   `[verdict, goal, experiment, hypothesis]` → `[verdict, experiment, hypothesis]`
   (frontmatter + the `# parents` comment + the Spawn-rule prose, which now
   says why `goal` left and that the 5 existing `goal -> mvp` edges stay
   prior art).
2. `.agi/context/schemas/[experiment].md` — `allowed_parents:`
   `[hypothesis, verdict, goal, task, idea, experiment, build]` →
   `[hypothesis, verdict, task, idea, experiment, build]` (same three places).
3. `extensions/agi/bin/zoom.py` lines 594 and 691 — kid contract now reads
   `Acceptable: spawn one child node (hyp from idea, exp from hyp, verdict
   from exp, outcome from mvp).` (`mvp from exp` removed, `verdict from exp`
   added; both copies identical).
4. `extensions/agi/tests/test_spawn_gate.py` — two new tests: `goal` is
   absent from the mvp/experiment rules and present in hypothesis/idea/cron/build
   (all build variants); and a read-both test asserting every `X from Y` the
   zoom.py kid contract advertises is a spawn the gate approves, that the two
   contract lines have not drifted, and that `mvp from exp` is gone.

## Evidence

All seven proof criteria, run against `.agi` as the graph root:

1. `spawn_gate.py check --type mvp --parent goal:g13` → **exit 2**,
   `mvp may not be parented by 'goal' … allowed: ['experiment', 'hypothesis',
   'verdict']`. ✓
2. `check --type experiment --parent goal:s22` → **exit 2**, naming `goal`
   unallowed, allowed `['build', 'experiment', 'hypothesis', 'idea', 'task',
   'verdict']`. ✓
3. `check --type hypothesis --parent goal:s22` → **exit 0**, APPROVED. ✓
4. `check --type cron --parent goal:s22` → **exit 0**, APPROVED — the
   structural exception (`allowed=['goal']`, cron's only legal parent) is
   intact. ✓
5. `spawn_gate.py rules --root .` shows `goal` absent from mvp and
   experiment, present in hypothesis and cron. ✓
6. grep: neither zoom.py:594 nor :691 contains `mvp from exp`; both contain
   `verdict from exp`. No other live copy of the contract exists in
   `extensions/`, `skills/`, or `src/` (GOALS.md and session contexts still
   carry the old string, but both are derived or historical). ✓
7. Node count: 841 non-deprecated node files, unchanged by this run — no
   node was touched, and the gate gates spawns, not history, so no existing
   `goal -> mvp` / `goal -> experiment` edge is invalidated. ✓

Test suite: `pytest extensions/agi/tests/test_spawn_gate.py` → **51 passed
in 1.21 s** (49 pre-existing + 2 new), including
`test_goal_may_not_parent_mvp_or_experiment` and
`test_kid_contract_advertises_only_gate_legal_routes`.

**Evidence link.** `evidence_runs` names this node: the run above *is* the
experiment, and this node is the only `experiment` in the corpus recording
it — a bare count (`--evidence-runs 8`) resolves to 0 under `goal:g7.3`
("an unverifiable count … stops being self-certifying"), which is what
made the first `cli.py done` call demote `proved` to
`inconclusive_lean_proved:50`. Citing the run node is the shape the gate
asks for.

One pre-existing wrinkle found, not caused by this change: the
`test_shipped_schemas_load_without_error` candidate search only knows the
legacy `context/schemas` and `agi-tree/context/schemas` layouts, so it
silently **skips** under the new `.agi/` layout. The new `_shipped_schemas_dir`
helper used by the two new tests adds the `.agi/context/schemas` candidate so
the s22 assertions actually run in this checkout.

## Agent Notes
All 7 proof criteria green: gate rejects goal->mvp and goal->experiment (exit 2), still approves goal->hypothesis and goal->cron; zoom.py kid contract now says 'verdict from exp'; 51/51 spawn_gate tests pass with 2 new read-both tests