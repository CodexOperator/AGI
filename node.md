---
id: hypothesis:l4-a-no-spawn-hook-run-never-prints-spawned-or-latches-a-fake-pid-and-the-latch-tests-discriminate
mint_id: cc34b9847d52456ebe04247aa7301889
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 9d174265df6873aa
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (SL7.32 residue, mur digest wf_438874da-7a6 line (2), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: extensions/agi/hooks/rotation_alert.py:812-817 — when AGI_HOOK_NO_SPAWN is set the spawn helper returns 12345 (a recorder pid) and the caller path prints 'spawned' and writes the once-per-generation latch (_latch_path :741) with 'pid 12345' for a rotate-self that never started; in a production pane with the variable set (an operator export leaking into the hook's env) the seat is latched for the whole generation against a phantom, and _latch_held (:769) reads pid 12345 as whatever process happens to own it. test_rotation_alert.py:1127 test_latch_path_resolves_to_seats_own_tree_not_main runs on a gitless tmp fixture where _shared_sessions_dir (:508) resolves to the identity — the assertion cannot tell the seat's tree from main; no out-of-process test (run_hook is in-process, :73/:317) exercises AGI_HOOK_NO_SPAWN end to end; test_rotation_alert.py:1165-1168 writes 'pid 999999' as a dead latch, but this box's /proc/sys/kernel/pid_max is 4194304, so 999999 can be live. CLAIM: (a) under AGI_HOOK_NO_SPAWN the hook prints 'declined: AGI_HOOK_NO_SPAWN' and writes NO latch (the argv still provable through _rotate_self_argv); (b) the latch-path test builds a real two-tree git fixture (main + a worktree with its own .agi/sessions) so the resolution is a real discriminator; (c) the dead-pid fixtures use a pid proved dead (a spawned-then-reaped child's pid, or one above /proc/sys/kernel/pid_max read at test time); (d) ONE out-of-process test runs the hook as a subprocess with AGI_HOOK_NO_SPAWN=1 and asserts no latch, no spawn, exit 0. FALSIFIERS: a NO_SPAWN run leaves a latch file naming 12345; the latch-path test passes with _shared_sessions_dir monkeypatched to the identity; a dead-pid test passes with the pid replaced by os.getpid(). TESTS: test_rotation_alert.py — the four above; the existing latch tests unchanged. FILE SCOPE: extensions/agi/hooks/rotation_alert.py — the NO_SPAWN branch at :812-817 and the print/latch site it feeds (:913 region); extensions/agi/tests/test_rotation_alert.py. EXCLUDED: the _latch_path/_latch_held/_latch_holder_pid bodies, the gate-c captive, rotate.py. CEILING: one branch, four tests; no hook redesign."
thought_session: sensei-director-genXIII-L13
title: with AGI_HOOK_NO_SPAWN set the rotation_alert hook records declined, never 'spawned' with a fake pid 12345; the latch-path proof runs on a real two-tree git fixture and the dead-pid tests use a pid proved dead
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-no-spawn-hook-run-never-prints-spawned-or-latches-a-fake-pid-and-the-latch-tests-discriminate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
