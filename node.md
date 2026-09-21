---
id: hypothesis:l3w0-test-skips
mint_id: 418a97fa82b94aa7bee97fbd0fa1f6f3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 25ddebd136f03d36
season: 1
testable_claim: The suite's skip count drops from 9 to at most 1 by repointing the three stale post-g11 skips at the .agi layout and giving the five CLI scripts without --help a real argparse --help, leaving only node_writer.py's library skip
title: L3w0 test skips
---
# hypothesis:l3w0-test-skips

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
THE NINE, measured 2026-09-06 with pytest -rs: test_grid.py:272 skips because it looks for ../agi-tree/nodes (two-repo era; point it at .agi/nodes of this repo, and .agi/nodes/deprecated too); test_spawn_gate.py:628 skips because it looks for context/schemas and agi-tree/context/schemas (point it at .agi/context/schemas); test_brief.py:278 skips because the test harness config declares no director model (declare one in the fixture so the director and prime_director command paths are actually exercised); test_bin_help_smoke.py lists brief.py, briefing.py, completion.py, payload_boundary.py, write_guard.py as no --help (add argparse with a real --help to each, keeping their current positional or stdin behaviour intact; write_guard.py has custom argv parsing that exits 2 on --help, fix that first) and node_writer.py as a library (legitimate; keep that one skip with its reason). VERIFY: pytest -rs shows at most the node_writer skip; the three repointed tests run and pass against this repo's real corpus; suite green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md
