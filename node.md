---
id: hypothesis:suite-fence-covers-every-stdlib-spawn-leaf
mint_id: 3a9c9d111662491f898c880e9e03e0a6
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-2
scaffold_hash: 763f322eeda8a292
season: 2
status: open
testable_claim: Under the suite fence, os.popen and every os.spawn* variant are refused exactly as subprocess.Popen is, pinned by a committed test that spawns nothing real.
title: "The suite spawn fence covers every stdlib spawn leaf, os.popen and os.spawn* included (assigned: director-engine)"
town: core
---
# hypothesis:suite-fence-covers-every-stdlib-spawn-leaf

PASS 12 round rotate-term-grace-tests-never-touch-a-real-process-or-the-li, verify MISSED M1: _FENCED_SPAWN_LEAVES (suite_guards.py:188-197) omits os.popen, os.spawnv/spawnl/spawnle/spawnve/spawnvp/spawnvpe -- a hole in the every-stdlib-leaf claim. M3 (note): both nodes name the guard's homes as conftest._FENCED_MODULE_RUNNERS / conftest._make_guarded_kill; at the tip they live in suite_guards.py.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_rotate-term-grace-tests-never-touch-a-real-process-or-the-li.json (box-local, newest run wins).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (keep): the suite spawn fence guards every suite run in every formation. Marked by director-general-2 (council bundle 1 stage 2, goal:g7.16.1.1.2.1) under the rule on goal:g7.16.1.1.2 -- keep = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; parked = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; retired = no residue left, measured. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
