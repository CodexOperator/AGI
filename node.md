---
id: hypothesis:l2-goals-active-exempt
mint_id: 137b6bb1add44136acbb9b3e30a5dee5
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 3b0549da9279e871
season: 1
testable_claim: metrics.py's max_goals_active check exempts goals marked exempt_from_max_active (or a fixed always-active set naming g15/g16) from the active count and warning, matching wave 1's stated design that g15 (bugfix/optimization) and g16 (telemetry) are always active
title: L2 goals active exempt
---
# hypothesis:l2-goals-active-exempt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED L2.13 close: bash extensions/agi/driver.sh --smoke printed METRIC-WARNING goals_active=20 exceeds cc_dispatch.max_goals_active=18. goal:g15's own body (wave 1 mint) says it is long-term, active, always active, exempt from max_goals_active -- but extensions/agi/bin/metrics.py line ~1118-1123 just compares a raw goals_active count against the config cap with no exemption mechanism at all: FILE: extensions/agi/bin/metrics.py (the check near line 1118) plus context/schemas/[goal].md if a new frontmatter field is needed. ADD: a goal frontmatter field, e.g. exempt_from_max_active: true (or a fixed allowlist matching goal ids named in the ladder/config -- pick whichever is less invasive and say why in the experiment), so a goal that is deliberately always-active does not count toward or trip the cap. Retroactively set it on goal:g15 and goal:g16 through write.py (their minting notes both say 'always active' / 'exempt' for g15 explicitly; check g16's own wording before assuming the same for it). VERIFY: with g15 (and g16 if applicable) marked exempt, goals_active count and the warning both exclude them; a temp-graph test with N active goals at cap-1 plus one exempt active goal shows no warning; suite green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with actual output. Engine files edited in place; new node fields via write.py set on g15/g16 directly, never a hand edit. Do not commit, push, or grid.py commit. Suite via commands.py run tests. Report unexpected files in git status, never touch them.

RE-BRIEFED 2026-09-06 by owner decision (HANDOFF §6 item 10, brief .agi/context/l3-command-ladder-brief.md §2.6): do NOT build an exemption. Long-term goals become goal_kind perpetual and there is no active goal count at all. FIX: remove cc_dispatch.max_goals_active from config.json and the METRIC-WARNING branch in metrics.py (~line 1118-1123) outright; keep goals_active as a plain descriptive count only if something else reads it (grep first; if nothing does, drop it too). Red-first test: a graph with 30 active goals prints no warning. Suite green.
