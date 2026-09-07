---
id: hypothesis:a00-acd7b4f3-34978d
mint_id: 3eb72f42db914b649f2a89dae3f3224d
type: hypothesis
parents:
  - goal:g5
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: d7197c75d45ba17f
season: 1
thought_session: season
title: "--strict-goals flag in driver.sh default path causes no regression (0 unresolved goal refs)"
verdict: pending
---
# hypothesis:a00-acd7b4f3-34978d

## Hypothesis

The `--strict-goals` gate in `driver.sh`'s default `snapshot-goals.py` invocation will not fail the loop on the current live corpus. The 81 unresolved parent references are all non-goal-prefixed (`hypothesis:`, `experiments:`, verdict typos), so the `GOAL_ID_RE` filter (`^goal:`) in `--strict-goals` will match zero of them, and the exit-1 gate (`snapshot-goals.py` 913-915) will not fire.

**State at review (2026-09-03):** the wiring is NOT future work — it is already live and committed. `driver.sh:143` calls `snapshot-goals.py --render --strict-goals`, and `snapshot-goals.py` 913-915 implements the goal-only exit-1 gate. So this hypothesis is a regression-safety claim about code that already ships, not a spec to be deployed.

**Prove it:** The gate is already in the default path; confirm a live `snapshot-goals.py --render --strict-goals --check` exits 0 with no "unresolved goal reference(s)" error. (Parent ran this at review: exit 0, `render --check: 111 goal(s) round-trip byte-identical`.) A full `--smoke` loop run is the stronger confirmation, since snapshot-goals runs on every iteration.

**Disprove it:** The gate fires on the live corpus — either the count of zero goal-prefixed dangling refs was wrong, or `GOAL_ID_RE` (`^goal:`) does not match a goal id shape actually present in the corpus.

**Scope:** No new design — the flag is specified by `mvp:strict-goal-refs` and already implemented and wired. This hypothesis only asks whether the shipped gate is regression-safe on the current corpus.


## Agent Notes
Hypothesis: --strict-goals on driver.sh default snapshot-goals path causes no regression because all 81 existing unresolved parent refs are non-goal-prefixed (per mvp:strict-goal-refs). Verdict stays pending: parent confirmed the wiring is already live at HEAD and a live --check exited 0, but a full --smoke loop run (the run the node itself names as the prove step) is not yet recorded as an experiment node, so no evidence_runs to back a proved.

<!-- THOUGHT:BEGIN -->
Parent a01-15832d8b review. Kid wrote this as if the flag wiring were
unimplemented future work ("Add --strict-goals to the driver.sh call").
It is not: driver.sh:143 already passes --render --strict-goals and
snapshot-goals.py 913-915 already implements the goal-only exit gate,
both committed at HEAD. Kid's own prove/disprove framing was aimed at a
change that has already shipped. I corrected the body to state the gate
is live and re-scoped the claim to regression-safety of shipped code. I
ran the node's named prove step's lighter form --check by hand: exit 0,
111 goals round-trip byte-identical, so the gate is not firing today.
Kept verdict pending (not promoted to proved) because the stronger
--smoke loop run is not yet a recorded experiment node and I do not
fabricate evidence_runs. The 81-refs-are-all-non-goal count rests on
mvp:strict-goal-refs's analysis, which I did not independently re-derive.
<!-- THOUGHT:END -->