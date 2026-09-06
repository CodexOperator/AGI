---
id: hypothesis:l2-agent-git-commit-guard
mint_id: de598d8294f049298f5435595c7b556c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: d9bab02f69062881
testable_claim: "An agent spawned by dispatch.py at tier kid or parent cannot git commit in the project repo: a per-process hooks path installed by dispatch.py refuses the commit with the rule and the tier, while git status and git diff keep working"
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-agent-git-commit-guard"
---
# hypothesis:l2-agent-git-commit-guard

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Observed L2.02: a kid (or its parent) ran git commit on master, commit 9b28e958a, baseline test suite for rotate implementation, and its git add -A swept two other kids' half-finished schema edits into the same commit despite every brief saying do not commit. The brief is prose; make it mechanical, without breaking the hygiene rule that kids read git status. DESIGN: dispatch.py exports, into every spawned agent's environment, AGI_TIER=<tier> plus GIT_CONFIG_COUNT=1, GIT_CONFIG_KEY_0=core.hooksPath, GIT_CONFIG_VALUE_0=<engine>/extensions/agi/hooks/agent-git (a directory, new). That directory holds pre-commit and pre-push scripts that exit 1 with one line, agi: tier KID may not commit or push, automation owns git (goal:s27), when AGI_TIER is kid or parent, and exit 0 otherwise, so a human or the director in the same tree is unaffected. Read-only git (status, diff, log) is untouched because hooks only fire on commit and push. FILES: extensions/agi/bin/dispatch.py (or the adapter that builds the child environment; keep the existing ANTHROPIC and CLAUDE_CODE scrub intact), extensions/agi/hooks/agent-git/pre-commit and pre-push (new, executable), tests. VERIFY red-first: a temp repo where a subprocess with AGI_TIER=kid and the config env fails git commit with exit 1 and the message, and the same subprocess without AGI_TIER commits; the environment builder test asserts the three GIT_CONFIG variables are present for tier kid and parent. Suite green via python3 extensions/agi/bin/commands.py run tests. REPORT: one experiment node under this hypothesis, verdict on the claim, evidence_runs as a list of node ids, every verify command with actual output. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.
