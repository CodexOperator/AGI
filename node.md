---
id: hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript
mint_id: cb58e6a5b49c460f9c97e85347e0f158
type: hypothesis
parents:
  - goal:g15.14
  - hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears
next_edges: []
edited_by: sensei-director
scaffold_hash: 7433441348a5192f
season: 2
testable_claim: "goal:g15.14 fix-only #3 (Prime XII 22:44Z, mur-SL2.3-5 reviewed by name wf_8f7f3ca5-8e0: SL3.05 + SL4.01 accept_with_residue; P1 = live hazards, P2 = test integrity, both in this ONE round). Sites anchored by name on the seat at 4dad57c3b (the Prime's numbers were measured on the reviewed merge-up; grep by name): P1-a rotate.py `_prepare_checks` perform block (~8015-8040): `_merge_applies_clean(root, _sb)` measures conflict-freeness against the LOCAL `origin/<sb>` and then `_perform_season_merge` FETCHES and merges the REFRESHED ref — a different merge, with no abort path. CLAIM: measure and merge the SAME ref — fetch first (or pass the exact sha measured), then `_merge_applies_clean` on that sha, then merge THAT sha; on ANY conflict abort (`git merge --abort`) and BLOCK naming the paths; never leave a half-merge; the record names the sha merged. P1-b `cmd_prepare` (8146) never calls `_check_branch_guard` (524) — the perform path runs first, so a `--prepare --perform` on master would merge season into master: the guard runs FIRST in cmd_prepare AND in rotate-self's own prepare gate, refusing by name before any merge. P1-c `rotate-self --name <unregistered>` on a behind worktree merges as a side effect before the registry gate: the registry gate (seat must exist in config:seats) runs before the prepare/perform step; an unregistered name refuses with NO merge performed. P1-d check 5's clear line (`clear5`, ~8119) prefers the STALE pin's transcript over the row's — when check 5 blocks, the pin is another generation's by definition: prefer the row's `session_id` transcript (`~/.claude/projects/<slug>/<session_id>.jsonl` resolved the way the meter resolves it), fall back to the pin's only when the row has none. P2-a `_merge_applies_clean` / `_merge_conflict_paths` are patched out in EVERY committed test — add ONE test on a real git fixture (two branches, one clean merge, one conflicting) that exercises the real merge-tree gate and the abort path from P1-a. P2-b `_background_tasks` counts `.agi/.claude/tasks`, a path that never exists — fix the path to the one the harness actually writes (measure: `~/.claude/tasks` or the scratchpad tasks dir; if none is stable, DELETE the reader and its check, never keep a reader that never reads). FALSIFIERS: a prepare --perform on a fixture where the local ref is clean but the refreshed ref conflicts leaves a half-merge or merges anyway; a --perform on a fixture master branch merges; an unregistered --name merges; check 5's clear line names a pin transcript while the row has a session_id; the merge gate test passes with the gate patched; `_background_tasks` still names a never-existing path. TESTS: test_rotate*.py + test_session_start*.py + test_after_join_service.py + test_bin_help_smoke.py, with neighbours; a real time.sleep in a fixture shows as a 20 s test — gate delays on the fixture seam. RULES: merge, never rebase (in every clear line); never lower a guard; the kid's experiment-node prose never quotes the literal THOUGHT marker. FILE SCOPE: rotate.py (prepare/perform, cmd_prepare guard order, rotate-self registry-gate order, clear5, _background_tasks), tests. EXCLUDED: send.py, write.py, config nodes, the ack path (g15.24 SL5.08 is live there), the spawn writes (g15.21 SL5.07 is live there). CEILING: 1 parent, up to 3 kids (P1-a+P2-a / P1-b+P1-c / P1-d+P2-b), small."
thought_session: sensei-director-genV-L5
title: prepare --perform measures and merges the SAME ref with an abort path, the branch guard runs first, an unregistered --name never merges, check 5 prefers the row's transcript; the real merge gate is tested; _background_tasks reads a real path or is deleted
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
