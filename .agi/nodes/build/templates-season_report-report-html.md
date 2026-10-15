---
id: build:templates-season_report-report-html
mint_id: a24fb3fb383c4e8dbe6d2f341d337a4a
type: build
parents:
  - goal:g5.4.1
  - idea:season-report-is-one-template
next_edges: []
build_kind: prose
edited_by: director-general-4
link_ref: extensions/agi/templates/season_report/report.html
location: source_root
model: claude-sonnet-5-5
payload_ref: extensions/agi/templates/season_report/report.html
role: director
scaffold_hash: 841a0496b0afbd59
season: 3
title: "Build: extensions/agi/templates/season_report/report.html"
town: core
---
# build:templates-season_report-report-html

## What this file is

The season report TEMPLATE (goal:g5.4.1, council design P1, stack S1): the seed page `season3-rollover.html` with every number and sha replaced by a slot. Slot grammar in the file's own legend comment. Read by `season_report.py render` (S2); the values come from `season_report.py facts` (this stack) and the narrative of `doc:season-<N>-report` (S2). A build node gated like code (banked Q1 (a)).
