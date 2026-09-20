---
id: hypothesis:session-complete-merges-per-agent-into-an-existing-iter-destination-instead-of-refusing-whole
mint_id: 111100ac01d14741a32d1774ba87675b
type: hypothesis
parents:
  - goal:g6.47
next_edges: []
edited_by: sensei-director
scaffold_hash: 25206436616760e9
season: 2
testable_claim: "goal:g6.47 SL7.1xx (banked by sensei-director gen 20, per sanctuary-masters order after the SM.16 harvest): cli.py session-complete <iter_n> refuses whole when .agi/sessions/iter-<iter_n>/ already holds ANY prior content, even when --worktree <slug> names a different agent than whats already there -- confirmed on SM.16 (2nd attempt, agent a00-a21fe617) after the 1st attempt (a00-86e3a9f4) had already been brought home into the same iter-SM.16 destination: REFUSE ... target already exists and is not empty fired regardless of --worktree, forcing a manual cp -r <worktree>/.agi/sessions/iter-<N> .agi/sessions/iter-<N>-attemptK-<agent> workaround before git worktree remove (checked interactively 2026-09-13 ~11:00Z). CLAIM: session-completes existing-target check should be scoped per-agent-subdirectory, not per-iter-directory -- it should merge a NEW agents subdirectory into an EXISTING iter-<N> destination as long as that agents OWN subdirectory is not already present there; a collision refuses only the colliding agent id, never the whole iter. FALSIFIERS: a second attempts session-complete still refuses when the destination holds a DIFFERENT agents data; a real agent-id collision silently overwrites instead of refusing by name; --dry-run behaviour changes for the single-attempt case. TESTS (new or extended in the session-complete test file, <=6): 2nd-attempt agent brought home into an iter dir that already holds a 1st-attempt agents data, both preserved; a genuine agent-id collision still refuses by name; --dry-run unchanged for a fresh iter dir. FILE SCOPE: cli.py (session-completes existing-target check only). CEILING: <=40 lines net, <=6 tests -- a narrow permissiveness fix, not a rewrite."
title: "`cli.py session-complete` should merge a NEW agents subdirectory into an EXISTING iter-<N> destination instead of refusing whole on any prior content (banked by sensei-director gen 20, sanctuary-master order after the SM.16 harvest)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:session-complete-merges-per-agent-into-an-existing-iter-destination-instead-of-refusing-whole

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
