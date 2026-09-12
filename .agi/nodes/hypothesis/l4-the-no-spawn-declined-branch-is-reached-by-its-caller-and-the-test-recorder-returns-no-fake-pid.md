---
id: hypothesis:l4-the-no-spawn-declined-branch-is-reached-by-its-caller-and-the-test-recorder-returns-no-fake-pid
mint_id: 48f26b6823294f2383601200d81ebcab
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 04de500e5af74248
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.45 residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (8)). MEASURED (Prime): after SL7.45, _spawn_rotate_self's NO_SPAWN -> None branch (rotation_alert.py:812-820 at 0cd8c5c87) is UNREACHABLE through its only caller because gate e in _gated_rotate (:903-908) checks AGI_HOOK_NO_SPAWN first and returns 'no-spawn' before the spawn helper runs — dead code that reads as the fix; and the test recorder _no_real_spawn (test_rotation_alert.py:75) still returns a FakeProc whose pid is 12345 on the seam path, so a test through the recorder can still latch a fake pid. CLAIM: either the helper's NO_SPAWN branch is deleted (gate e is the one check, named in the helper's docstring) or gate e is removed and the helper's branch is the one check reached end to end — one check, not two; the recorder returns a FakeProc whose pid is a proved-dead or sentinel value that the latch writer refuses, or the recorder never reaches the latch write; the SL7.45 out-of-process test still passes. FALSIFIERS: coverage shows the helper's NO_SPAWN branch unexecuted by any test while it still exists; a test through _no_real_spawn leaves a latch naming 12345. TESTS: test_rotation_alert.py — the one-check reach test; a recorder-path test asserting no 12345 latch. FILE SCOPE: extensions/agi/hooks/rotation_alert.py — _spawn_rotate_self's NO_SPAWN branch and/or gate e; extensions/agi/tests/test_rotation_alert.py _no_real_spawn. EXCLUDED: the latch helpers, the SL7.56 sweep. CEILING: one branch removed, one recorder change, two tests."
thought_session: sensei-director-genXIII-L13
title: the rotation_alert NO_SPAWN declined branch is reachable through its only caller (or deleted), and the _no_real_spawn test recorder no longer returns a FakeProc with pid 12345 on the seam path
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-no-spawn-declined-branch-is-reached-by-its-caller-and-the-test-recorder-returns-no-fake-pid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
