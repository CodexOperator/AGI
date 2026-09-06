---
id: hypothesis:l2w5-skill-seasons-constitution
mint_id: f35202c43a024f0aa1c1e8e21eaabc61
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: 57c7e8f87e9795b8
season: 1
testable_claim: "skills/agi/SKILL.md carries a Seasons section and a Constitution section that a cold reader can act on: read order by role, the one comms verb, death per role, rotation, and the season edge, each pointing at the command or node that implements it"
thought_session: agi-master-2026-09-06
title: "L2 wave 5: l2w5-skill-seasons-constitution"
---
# hypothesis:l2w5-skill-seasons-constitution

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: skills/agi/SKILL.md, the payload of build:skills-agi-SKILL.md, written through write.py build:skills-agi-SKILL.md payload <tmpfile> with a thought, never an editor on the live file. ADD two sections after The three tiers. SEASONS (under 60 lines): the ladder node .agi/nodes/.geometry/ladder.md is the declaration (tiers, current_season, caps, budget, read_order, director_rotate_at); tier table from brief section 1 with plan node, report node, judged against, lens, cadence; the judgment record fields on a report node and season.py judge; the season edge season_parents (traversable for zoom, excluded from chain depth and outcome_coverage); season.py status as the count table and its invariants measured never enforced; rollover in two lines; death per role; branches mirror the ladder and grid.py commit --all only on master; rotation via rotate.py meter and spawn with the successor reading HANDOFF.md before replacing. CONSTITUTION (under 40 lines): the five morals as nodes under .agi/nodes/moral/, the only parentless type, owner-edited only (write.py refuses otherwise); the five questions verbatim from the moral nodes; read order by role from the ladder node and the fact that brief.py prepends the head automatically per tier; the one comms verb send.py send, read, peek and the inbox path; ideas as memos with authors. Every claim in both sections names the file, command or node that implements it; nothing is described that does not exist in the tree. Keep the existing sections intact; update the CLI table with season.py, send.py, rotate.py, write_guard.py rows. VERIFY: every command you name runs with --help; python3 extensions/agi/bin/commands.py run tests green; the write guard is silent after your payload write. REPORT: one experiment node under this hypothesis with verdict and evidence_runs. Do not commit, push, or run grid.py commit. Design source: .agi/context/season-ladder-and-morals-brief.md sections 1 to 4.
