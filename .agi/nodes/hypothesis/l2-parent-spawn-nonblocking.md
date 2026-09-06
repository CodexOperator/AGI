---
id: hypothesis:l2-parent-spawn-nonblocking
mint_id: a67b290a89674e86bae784b861af3c04
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: 5a8d4d69cb1e2f13
testable_claim: A pi parent's kid spawn returns within seconds with the kid's agent id, and the parent brief tells it to wait with cli.py status, so no parent tool call outlives the harness tool timeout while a kid runs
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-parent-spawn-nonblocking"
---
# hypothesis:l2-parent-spawn-nonblocking

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Observed L2.01, parent a00-a9fddc13: its blocking python3 dispatch.py ... --tier kid call was killed by the 20-minute tool timeout while the kid kept running, and the parent had to reconstruct the kid's identity from manifest.json; see .agi/sessions/iter-L2.01/a00-a9fddc13/output.log. Investigate first: which timeout killed it (agent_timeout_mins in .agi/config.json, the pi harness bash tool limit, or heal.py) and record the answer. Then fix at the spawn seam, not by raising timeouts: dispatch.py gains --detach (or makes it the default for --tier kid when the caller is a parent, decide and document) which spawns the kid, writes the manifest entry, prints the agent id and node id and returns; the reaper and heal.py keep owning the kid's lifetime. brief.py's parent brief (function _parent) changes its spawn instruction to: spawn with --detach, then poll python3 extensions/agi/bin/cli.py status ITER until the kid's manifest status is done or failed, sleeping 30 seconds between polls, each poll a separate short tool call. FILES: extensions/agi/bin/dispatch.py, extensions/agi/bin/brief.py, tests in extensions/agi/tests/test_dispatch.py and test_brief.py or their existing equivalents. VERIFY: a fake-adapter test where --detach returns before the fake kid finishes and the manifest still reaches done via the reaper; a brief test asserting the parent brief names --detach and cli.py status; suite green. REPORT: one experiment node under this hypothesis with a verdict on the testable claim, evidence_runs as a list of node ids, every verify command with its actual output in the body. Engine files are edited in place; suite via python3 extensions/agi/bin/commands.py run tests, green before you report; each new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.
