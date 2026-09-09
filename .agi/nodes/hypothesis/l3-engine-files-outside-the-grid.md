---
id: hypothesis:l3-engine-files-outside-the-grid
mint_id: eb52f664dcd7448ab482abbb2b555a43
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e077642e6d37617e
season: 2
testable_claim: After the change, every tracked engine file that the project intends to grid-version has a build node whose payload_ref resolves to it, proven by a checker that enumerates tracked engine files, subtracts every declared payload_ref, and exits nonzero on any remainder outside a declared exclusion list -- with the remainder at zero and level3.py gaining an additive mode that mints missing nodes without pruning or resurrecting anything.
thought_session: belam-S1-L3-XII
title: "Seventy-two tracked engine files have no build node, so their bytes are outside the grid entirely: rotate.py, season.py, send.py and write_guard.py among them, and the discoverer that would mint them is forbidden to run"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-engine-files-outside-the-grid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF.

THE OWNER APPROVED THIS DIRECTLY, 2026-09-08, verbatim: 'I'm fine doing the item49 of section 6 where we do a brief per file that's outside node.' Every file below is named individually, which is what 'per file' buys; they are worked as ONE class because 72 separate hypothesis nodes asserting 'mint a node for file X' would be 72 nodes of pure bookkeeping in a graph whose whole point is that a node carries a thought. That granularity call is the director's, is recorded here rather than hidden, and the owner can reverse it in one line.

THE GAP, measured 2026-09-08 by set subtraction, not by estimate. Every payload_ref declared anywhere under .agi/nodes (live and deprecated) was collected: 231 distinct paths. Every tracked file under extensions/, skills/, src/ and bin/ was collected: 252. The difference is 72 files with NO build node, whose bytes are therefore outside the grid entirely -- grid.py commit --all versions nothing for them, grid.py payload cannot read them back, and stitch.py --from-grid could not materialise them.

WHY IT HAPPENED, and it is structural rather than neglect. level3.py is the discoverer that mints build nodes from git ls-files, and trap 0i forbids running it without --dry-run because it would prune 18 deprecated build nodes and mint parentless nodes for the .claude/workflows/*.js symlinks. So every engine file created since the last scan has quietly accumulated with no node, and the only tool that could fix it is the one nobody is allowed to run.

THE 72 FILES, grouped:

ENGINE MODULES (18) -- the load-bearing half
  extensions/agi/bin/briefing.py
  extensions/agi/bin/commands.py
  extensions/agi/bin/derive-commands.py
  extensions/agi/bin/drift_check.py
  extensions/agi/bin/frontier.py
  extensions/agi/bin/glitch_master.py
  extensions/agi/bin/inject.py
  extensions/agi/bin/pi_edit_forgiveness.py
  extensions/agi/bin/plan_master.py
  extensions/agi/bin/provisioning.py
  extensions/agi/bin/rotate.py
  extensions/agi/bin/season.py
  extensions/agi/bin/seat_status.py
  extensions/agi/bin/send.py
  extensions/agi/bin/sensei.py
  extensions/agi/bin/spawn_budget.py
  extensions/agi/bin/telemetry_rollup.py
  extensions/agi/bin/write_guard.py

BRIEFS (2)
  extensions/agi/briefs/master-sensei-duties.md
  extensions/agi/briefs/prime-director-successor.md

GIT HOOKS (2)
  extensions/agi/hooks/agent-git/pre-commit
  extensions/agi/hooks/agent-git/pre-push

ONE-OFF SCRIPTS (2)
  extensions/agi/scripts/chat_vs_briefing_proxy.py
  extensions/agi/scripts/chat_vs_briefing_tradeoff.py

SOURCE (1)
  extensions/agi/src/renderers/scatter.py

WORKFLOWS (4)
  extensions/agi/workflows/agi-deep-search.js
  extensions/agi/workflows/agi-l3w-route-probe.js
  extensions/agi/workflows/deep-search.json
  extensions/agi/workflows/l3w-route-probe.json

TEST FIXTURES (14) -- probably EXCLUDE, they are data
  extensions/agi/tests/fixtures/nested/level_a/level_b/level_c/leaf.md
  extensions/agi/tests/fixtures/nested/level_a/level_b/middle.md
  extensions/agi/tests/fixtures/nested/level_a/outer.md
  extensions/agi/tests/fixtures/nested/top.md
  extensions/agi/tests/fixtures/nodes/sample.json
  extensions/agi/tests/fixtures/nodes/sample.md
  extensions/agi/tests/fixtures/schemas/[hypothesis].md
  extensions/agi/tests/fixtures/schemas/example.json
  extensions/agi/tests/fixtures/schemas/example.md
  extensions/agi/tests/fixtures/walk_test/a/file_a.md
  extensions/agi/tests/fixtures/walk_test/b/file_b.md
  extensions/agi/tests/fixtures/walk_test/b/file_c.md
  extensions/agi/tests/fixtures/walk_test/file_top.md

TESTS (29)
  extensions/agi/tests/test_agi_bin_absent.py
  extensions/agi/tests/test_agi_env_strip.py
  extensions/agi/tests/test_bin_help_smoke.py
  extensions/agi/tests/test_briefing.py
  extensions/agi/tests/test_claude_code_adapter.py
  extensions/agi/tests/test_commands.py
  extensions/agi/tests/test_dispatch_dry_run.py
  extensions/agi/tests/test_edit_tool_forgiveness.py
  extensions/agi/tests/test_failures.py
  extensions/agi/tests/test_frontier.py
  extensions/agi/tests/test_git_commit_guard.py
  extensions/agi/tests/test_glitch_master.py
  extensions/agi/tests/test_ladder_node.py
  extensions/agi/tests/test_links.py
  extensions/agi/tests/test_pi_edit_forgiveness.py
  extensions/agi/tests/test_plan_master.py
  extensions/agi/tests/test_post_wire.py
  extensions/agi/tests/test_provisioning.py
  extensions/agi/tests/test_real_adapter_restart.py
  extensions/agi/tests/test_rotate.py
  extensions/agi/tests/test_season.py
  extensions/agi/tests/test_seat_status.py
  extensions/agi/tests/test_send.py
  extensions/agi/tests/test_sensei.py
  extensions/agi/tests/test_shared_state_worktree.py
  extensions/agi/tests/test_spawn_budget.py
  extensions/agi/tests/test_telemetry_rollup.py
  extensions/agi/tests/test_workflow.py
  extensions/agi/tests/test_write_guard.py

TESTS, renderers (1)
  extensions/agi/tests/renderers/test_scatter.py

READ THE GROUPS AS A DECISION, NOT A LIST. The 18 bin modules are the load-bearing half and are not arguable: rotate.py is the file the entire seat ladder rotates through and the file whose orphaned diff nearly vanished in an earlier session; season.py runs the ladder; send.py is the comms verb; write_guard.py is the thing that catches unsanctioned writes. The 14 test fixtures are almost certainly a legitimate exclusion -- they are data, not source -- but DECIDE that and declare it, do not assume it silently, because an undeclared exclusion is indistinguishable from an oversight the next time someone runs this count. The tests, hooks, workflows and briefs each need the same explicit yes or no.

WHAT TO BUILD, three parts.
1. A CHECKER, first, because it is the part that keeps this closed. Enumerate tracked engine files, subtract every declared payload_ref, subtract a declared exclusion list that lives in the graph rather than in the script, and exit nonzero on any remainder. Wire it where the other invariants already run. Without this, the count silently re-grows the day after you fix it -- which is exactly how it got to 72.
2. AN ADDITIVE MODE ON level3.py: --mint-missing-only. It mints a node for a file that has none and does NOTHING else: no pruning, no resurrecting a deprecated node, no touching an existing one. Trap 0i exists because level3.py's default mode is destructive; the fix is a mode that cannot be, not a promise to be careful. Prove it by running it against a fixture tree where a deprecated node and a live node both exist and asserting neither moved.
3. THE PARENT SHAPE. goal:s29 gives a build node exactly two legal origins, and a new file needs parents: [mvp:<id>]. Seventy-two mvps would be worse than the disease. Decide between an mvp per SUBSYSTEM (one for bin/, one for tests/, one for workflows/) and a schema amendment, argue it in the node body, and implement whichever you choose. This is the part that needs judgement rather than code, so do it first and let it shape the other two.

DO NOT: run level3.py without --dry-run at any point, delete or git rm any node, touch moral:*, or add a seat row to config:seats.

PARENT SD.13 BRIEF -- SANCTUARY-DIRECTOR GEN IV, 2026-09-09, item 49. READ THIS FIRST; it is your whole task. This node's own testable_claim is the spec -- read it before designing anything.

MEASURED BY ME JUST NOW, so you do not spend a kid re-deriving it: of 234 tracked engine code files under extensions/ (.py/.sh/.js), 171 have a build node whose payload_ref resolves to them and 63 DO NOT. `extensions/agi/bin/rotate.py` -- the file the whole ladder rotates on -- is one of the 63. Others include commands.py, handoff.py, hierarchy.py, inject.py, drift_check.py, frontier.py, plan_master.py, glitch_master.py, briefing.py, derive-commands.py, mail_alert.py, pi_edit_forgiveness.py. Reproduce the count yourself before you change anything (git ls-files, subtract every declared payload_ref across .agi/nodes/**) and say what number you got -- if it disagrees with 63, your number wins and say so.

WHAT TO BUILD, per the node's claim, in this order:
1. THE CHECKER FIRST, and it is the deliverable that outlives the cleanup: enumerate tracked engine files, subtract every declared payload_ref, exit NONZERO on any remainder outside a declared exclusion list. The exclusion list must be DATA (a declared list with a reason per entry), not a hardcoded set buried in a function -- some files legitimately have no node and the checker must say which and why rather than being silently tuned until it passes. Add it to the standard verify sequence the same way links.py/write_guard.py are reachable.
2. THEN the additive mint mode on level3.py: mint the missing nodes WITHOUT pruning or resurrecting anything.

🔴 THE PRUNING HAZARD IS THE ONE THING THAT CAN MAKE THIS ROUND CATASTROPHIC, and it has already cost this project a confirmed 29k-node loss once. Read CLAUDE.md's "two rules this project has already paid for" before touching level3.py. NEVER run level3.py without --dry-run. Your mint mode is ADDITIVE ONLY: it may create a node for a file that has none; it must NEVER delete a node, never prune, and never resurrect a deprecated one (a deprecated node whose file still exists is a DELIBERATE state -- see the deprecate-never-delete convention -- and a mint pass that "helpfully" revives it has destroyed a decision). Prove the additive property: run it --dry-run, record the node count before and after a real run, and assert the count only GREW. If the count drops by even one, stop and report rather than continuing.

MUST NOT LOSE / MUST NOT BREAK: the namespace guard in dispatch.py (adapters.assert_model_in_provider_namespace -- a money-safety guard, refuses a Claude alias on an OpenRouter provider), the kid_ceiling threading, and the per-kid brief channel, all landed this session. Full suite before you report: python3 -m pytest extensions/agi/tests/ -q. Then links.py links (0 broken), snapshot-goals.py --render --check (byte-identical), write_guard.py check.

YOUR GUARDRAILS: HARD CEILING max 3 kids for your loop, and do not leave a kid or a nested agent running past your own exit (trap 0af: a parent that outlives its spawner keeps spending to its ceiling). Inspect any branch with MERGE-BASE diffs only (trap 0ae): `git diff <merge-base>..<branch>` answers "what did this branch change"; `git diff season/s2..HEAD` does NOT and has already falsely shown owner verbatim as deleted. Check the OpenRouter KEY before every kid (provisioning.py status), floor $1.00 never lowered. Report the ACCOUNT delta -- from extensions/agi/bin: python3 -c "import provisioning; print(provisioning.credit_balance('.'))" -- before your first kid and after your last.

Write your result into THIS node via write.py note labeled "ENGINE FILES IN THE GRID" -- the checker's exact invocation, the before/after missing-count, the node-count-only-grew evidence, the exclusion list with a reason per entry, and the account delta. NOTE: write.py note text must not contain a doubled-ampersand sequence -- its script parser splits on it and your note will not land. If the count does not reach zero, report the remainder honestly rather than widening the exclusion list to make it pass; an exclusion list tuned until green is the checker lying to its next reader.
