---
id: hypothesis:l2w3-season-py
mint_id: e3b7d7bca63b4f9589905b3283620410
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: a977b28399901009
testable_claim: season.py status prints the per-tier plan and report counts, ratios, mismatches and cost from the live graph; judge scaffolds the judgment record on a report node with the lens derived from the plan node's parent; rollover --dry-run lists what season N+1 would mint without writing
thought_session: agi-master-2026-09-06
title: "L2 wave 3: l2w3-season-py"
---
# hypothesis:l2w3-season-py

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/season.py (new) plus tests. Reads the ladder node .agi/nodes/.geometry/ladder.md for tiers and current_season; every write goes through write.py (shell out), never a direct file write. STATUS: one table, one row per tier from the ladder: plan type(s), plan count (active only and total), report count, ratio, plan-without-report count, report-without-plan count (a report whose judged_against is empty or does not resolve), and cost_usd summed from telemetry stamps where present (blank when none). Then the season-1 baseline line the brief measured (section 1, Season 1 data point) for comparison. JUDGE <report-node-id> [--against <plan-node-id>]: stamps judged_against (given, or the report's first parent that is a plan type for its tier), lens (the plan node's own first goal or vision parent, derived, never asked), alignment unknown, season current, through write.py set; refuses when the report's type is not a report type on the ladder. ROLLOVER --dry-run: prints what a real rollover would do: current_season plus one; up to caps.vision visions for the new season, each with parents = the five morals, season_parents = the closed overviews of the current season, proposes_goals empty, moral_adherence all unknown; and the retag of the current season's visions to status closed. Real rollover (no --dry-run) performs it through write.py and bumps current_season on the ladder node; it must refuse when any overview of the current season lacks a judgment record. VERIFY red-first with a temp graph for each subcommand; on this repo run status and rollover --dry-run and paste both outputs. Section 1 (Invariants, Season edge), section 6 is not needed. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done), every verify command with its actual output in the body. Engine files are edited in place; a new engine file goes directly under extensions/agi/bin/. Suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md

DEFECT 2026-09-06 after L2.10: season.py rollover --dry-run reports Vision cap (3) reached; no new visions, because it counts the 17 closed season-1 visions against caps.vision. The cap applies to visions of the new season only (ladder caps_apply_from_season 2; brief section 1, Grandfathering: caps apply from season 2). Fix: count only visions whose season equals the new season; the dry run must then offer up to 3 season-2 visions and say their parents are the five morals and their season_parents the season-1 overviews; the real rollover must refuse to mint a vision without the owner's text for its body (a vision is owner-tier: bank, do not invent). Red-first test, suite green, then report.

ADDENDUM 2026-09-06 (agi-master-2, round 12 brief): bundle with the cap-count DEFECT above, same file. season.py judge <report-node-id> on an overview must also scaffold moral_audit: a five-key dict (faith, love, empathy, antifragility, beauty), each value {value: unknown, evidence: null} on first judge call if the field is absent; never overwrite an existing key's value, only fill missing keys. Field shape is in .agi/context/schemas/[overview].md lines ~22 and ~69-79 — read it before writing. VERIFY: judge on an overview lacking moral_audit fills all five keys unknown; judge on one that already has partial moral_audit leaves existing keys untouched and fills only missing ones; red-first test; suite green. Fold into the same experiment node and verdict as the cap-count fix — one kid, one file, one report.
