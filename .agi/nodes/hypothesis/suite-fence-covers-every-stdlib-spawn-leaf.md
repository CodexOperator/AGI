---
id: hypothesis:suite-fence-covers-every-stdlib-spawn-leaf
mint_id: 3a9c9d111662491f898c880e9e03e0a6
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: belam
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
