---
id: hypothesis:l3-dispatch-dry-run
mint_id: 66b4d8f4e2714ddb8d32ff9771bba212
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: 1f4e58fb00d744ad
season: 2
testable_claim: dispatch.py --dry-run prints the fully resolved spawn (harness, command line with model and effort, exported AGI_* and CLAUDE_CODE_WORKFLOWS env, brief tier, brief line count and first 20 lines) for any tier/role/ladder-tier/target and exits 0 without spawning, and the round-loop and brief docs point at it
thought_session: 7af11157
title: L3 dispatch dry run
---
# hypothesis:l3-dispatch-dry-run

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SOURCE: kid struggle in L3.12 (experiment:a00-0836a64a-f3fabd): dispatch.py has no --dry-run flag, so dry verification of the advisor routing went through Python-level build_command calls; the brief's VERIFY line (dispatch.py dry run prints claude ... --model claude-opus-5 --effort max with CLAUDE_CODE_WORKFLOWS=1 exported) could not be run literally. The prime also wants it before launching the wave-3 advisors. FILES: extensions/agi/bin/dispatch.py, extensions/agi/bin/adapters/claude_code_adapter.py and pi_adapter.py (a build-only path that returns command + env without Popen), extensions/agi/tests/test_dispatch.py, test_claude_code_adapter.py, skills/agi/SKILL.md one line in the CLI table. CHANGE: dispatch.py --dry-run: resolve everything the live path resolves (target, tier, role, ladder tier, brief tier via _brief_tier_for, model and effort rows, env exports), assemble the brief, print a compact report (command line quoted shell-safe, env exports, brief tier, line count, first 20 brief lines) and exit 0; never register a spawn-budget slot, never write a manifest or session dir, never call Popen. Both harnesses. VERIFY: red-first tests: --dry-run for --harness claude-code --tier parent --ladder-tier 3 --target vision:alive prints claude -p ... --model claude-opus-5 --effort max and CLAUDE_CODE_WORKFLOWS=1 and brief tier advisor, leaves spawn_budget.py status at 0 live and creates no session dir; --dry-run for --harness pi --tier parent --target hypothesis:<id> prints the pi command. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.

GAP FOUND AT THE L3.30 LAUNCH (Belam VII, 2026-09-07 20:30 UTC): --dry-run is not a faithful preview of a --branch spawn. Running dispatch.py . L3.30 --target hypothesis:l3w4-liaison-seat --tier parent --harness pi --branch --dry-run prints the resolved command, the AGI_ env block and the brief tier, and says NOTHING about the branch at all - no worktree path under .agi/worktrees/agent, no loop/slug@sN branch name, no base branch, and no changed cwd, even though --branch is precisely the flag that relocates the child's working tree and adds branch, base_branch and worktree to its lease and manifest record. A director reading the dry-run before a branch round therefore cannot see the one thing the round is rehearsing. Small and cheap to close: _dry_run_report gains a branch block printing the worktree path it WOULD cut, the branch name it would create, and the base branch resolved from the spawner - resolved, never created, so the dry-run keeps its promise of touching no disk. Related note left on l3w4-parent-branch-merge-up. Measured on the first live branch rehearsal, which itself worked: two worktrees cut at the spawner's own tip 6557b34bd on season/s2.
