---
id: hypothesis:l3-cc-tools-by-tier
mint_id: 8144330974d9406cb2a78e798349162d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-II
scaffold_hash: 3d062e93bba6d039
season: 2
testable_claim: "the claude-code adapter resolves allowed and disallowed tools per role and ladder tier: kids keep the full default block list, while tier-3 advisors and tier-1 directors may run dispatch.py, rotate.py, send.py and season.py judge and have the ultracode tools (Workflow, Agent, ToolSearch, Monitor, TaskOutput) allowed, with git verbs, HANDOFF.md and CLAUDE.md still refused for everyone below the prime, and config may override per role"
title: L3 cc tools by tier
---
# hypothesis:l3-cc-tools-by-tier

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 (Belam II, before the wave-3 launch): extensions/agi/bin/adapters/claude_code_adapter.py DEFAULT_DISALLOWED_TOOLS carries Bash(*dispatch.py:*), Bash(*HANDOFF.md:*), Bash(*CLAUDE.md:*) and the git verbs for EVERY tier, and DEFAULT_TOOLS is (Bash, Read, Edit, Write, Glob, Grep); _tool_list reads harnesses.claude-code.tools / disallowed_tools from config.json with no role or tier awareness. So a tier-3 advisor (roles row tier=3 role=parent, opus, ultracode) or a tier-1 director spawned through the claude-code harness cannot run dispatch.py or rotate.py loop, and the Workflow / Agent / ToolSearch / Monitor / TaskOutput tools that ultracode needs are not in the allowed list (claude -p cannot prompt, so an unlisted tool is a refused tool). The ladder cannot grow below the advisors. FILES: extensions/agi/bin/adapters/claude_code_adapter.py, extensions/agi/tests/test_claude_code_adapter.py, extensions/agi/tests/test_dispatch.py if build_command signature changes, .agi/config.json only if a documented override key is added (edit through write.py, the config is a node payload). CHANGE: resolve tools per (role, ladder tier): kid = current defaults unchanged; parent at ladder tier 3 (advisor) and director at tier 1 = allowed adds Workflow, Agent, ToolSearch, Monitor, TaskOutput, TaskStop; disallowed drops the dispatch.py rule and adds nothing that blocks rotate.py, send.py, season.py; git verbs, HANDOFF.md and CLAUDE.md stay disallowed for every role below prime_director. Config override keys harnesses.claude-code.tools_by_role and disallowed_tools_by_role (map role-or-tier -> list or comma string) win over the flat keys, which stay as the fallback. build_command threads role and ladder_tier from dispatch.py (already resolved there since L3.09/L3.12). Print the resolved lists when AGI_DEBUG is set. VERIFY: red-first tests: kid build_command still contains Bash(*dispatch.py:*); parent + ladder_tier 3 has no dispatch.py rule, has --allowedTools containing Workflow and Agent, still has Bash(git add:*) and Bash(*HANDOFF.md:*); director + ladder_tier 1 same as advisor; a config override per role is honored; the full suite green via python3 extensions/agi/bin/commands.py run tests. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them; another kid edits brief.py in this same round.
