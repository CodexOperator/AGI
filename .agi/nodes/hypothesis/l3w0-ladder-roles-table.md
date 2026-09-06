---
id: hypothesis:l3w0-ladder-roles-table
mint_id: 09cd8b551cde456b94d1da49ac56ef83
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: 0e3d6db2287d8e55
season: 1
testable_claim: The ladder node declares a roles table (tier x role -> harness, model, effort, settings) and season_names, dispatch.py resolves harness/model/effort/settings from it with config harnesses.* as fallback, and every spawn exports AGI_LOOP and AGI_ROLE so node_writer stamps loop and role at mint
title: L3w0 ladder roles table
---
# hypothesis:l3w0-ladder-roles-table

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: .agi/nodes/.geometry/ladder.md (via write.py set, never a hand edit), .agi/context/schemas/[ladder].md, extensions/agi/bin/dispatch.py, extensions/agi/bin/adapters/claude_code_adapter.py, tests. TABLE (brief section 2.1, collapsed ladder): rows for (3, prime_director, claude-code, claude-fable-5-1, max, ultracode), (3, parent, claude-code, claude-opus-5, max, ultracode), (2, director, claude-code, claude-fable-5-1, max, -), (2, parent, claude-code, claude-opus-5, max, -), (1, director, claude-code, claude-fable-5-1, xhigh, -), (1, parent, pi, ~z-ai/glm-flash-latest), (0, parent, pi, ~z-ai/glm-flash-latest), (0, kid, pi, ~deepseek/deepseek-v4-flash-latest). settings=ultracode means the adapter appends --settings with the JSON object ultracode true; effort is passed as --effort as today. dispatch.py gains --role (default kid) and --ladder-tier and resolves the row; config.json harnesses.*.models stays the fallback when the ladder has no row. Also add season_names to the ladder (1: genesis) and to the schema. ENV: dispatch exports AGI_LOOP (the loop id it was given, e.g. s2-L1 or the iter prefix) and AGI_ROLE for every spawn; node_writer already stamps loop from AGI_LOOP (line ~661) and must also stamp role. VERIFY: red-first tests for row resolution, fallback, the --settings argument, and the two env stamps on a minted node; on this repo a dry dispatch prints the resolved command for each row. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/l3-command-ladder-brief.md

ADDENDUM 2026-09-06 (owner, L3 focus): the L3 shape has no tier-2 opus parents; the three tier-3 opus ultracode advisors embody the visions and spawn the Fable-max directors directly. Rows in scope for L3: (3 prime_director fable ultracode), (3 parent = advisor, opus ultracode), (1 director fable xhigh... NO: owner fixed director-kids at fable 5.1 MAX for L3, use max), (1 parent pi glm), (0 director pi glm, one per LT subgoal), (0 parent pi glm), (0 kid pi deepseek). Add mantles as a declared field (mantles_prime_director already set on the node) and season_names (1: genesis). Every row still resolvable by dispatch --role.

CORRECTION 2026-09-06 to the addendum above (director's slip, kept for the record): the tier-1 director row for L3 is claude-fable-5-1 at effort MAX, per the owner's fixed mapping (Belam ultracode, advisors opus ultracode, director-kids fable 5.1 max). xhigh is not used anywhere in the L3 shape; it would only apply if a deeper full ladder later inserts a tier-2 director layer above the perpetual directors. Tier-2 rows are declared but unused in L3.
