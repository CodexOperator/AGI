---
id: hypothesis:l4-a-workflow-run-on-the-claude-code-harness-says-it-executed-nothing-and-names-the-two-real-routes
mint_id: 2912488d655f4bd3b40c3d308196eee4
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
edited_by: belam
scaffold_hash: 3348111d3d751964
season: 2
testable_claim: "(1) `workflow.py run <name> --harness claude-code` from a plain shell still exits 0 and tracks the run exactly as today, AND prints ONE line to stderr naming that no stage was executed by workflow.py, that the manifest's .js runs under the Claude Code Workflow tool, and that a headless run is `--harness pi` (the default). (2) the pi path's output is byte-identical to today (the line never prints there). (3) director-thought's exact invocation (brainstorm, --harness claude-code, two stages) reproduces: before = silent resolved summary; after = the same summary plus the one named line -- one test with a two-stage fixture manifest."
thought_session: dissolve-legacy-2026-09-19
title: "SM.120 (thought-master [ask] 19:57Z, owner-ordered brainstorm workflow on goal:g14): a workflow run on the claude-code harness SAYS it executed nothing -- the resolve-and-describe branch prints one named line pointing at the two real routes (the .js under the Workflow tool, or --harness pi) instead of a silent all-resolved summary"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-workflow-run-on-the-claude-code-harness-says-it-executed-nothing-and-names-the-two-real-routes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.120 BRIEF (sanctuary-master 20:2xZ 09-18). MEASURED: workflow.py run_workflow `if harness != "pi":` branch resolves every stage with "model=... script=..." then view.summary() + _track_run and returns 0 -- nothing spawns by design (docstring at RunView.stage_resolved: "claude-code path: the script is the runner there"); note_workflow records the wf_ id the harness mints later. thought-master measured 19:57Z: two live brainstorm runs, both stages resolved in < 5 s, no session dir, nothing minted, no error. SHAPE: one print(..., file=sys.stderr) in that branch (~3 lines, wording names the .js path and `--harness pi`). CEILING 3 production lines. TEST: test_workflow_claude_code_branch_names_itself.py (fixture manifest, 2 stages; claude-code -> line present, exit 0, tracked; pi dry-run -> line absent). FILE SCOPE: workflow.py + one test. Queue: dispatch when a sanctuary slot is free (cap 3), before SM.119. Deliver batch + review in ONE line; foreground-wait the kid.
