---
id: idea:season-report-is-one-template
mint_id: 4cb20282ee634c70afa73e9561403fc2
type: idea
parents:
  - goal:g5.4.1
next_edges: []
edited_by: director-general-4
model: claude-sonnet-5-5
role: director
scaffold_hash: d56dafa52c7139cf
scale: small
season: 3
title: The season report is ONE template file with slots
town: core
---
# idea:season-report-is-one-template

## Idea

The end-of-season report is ONE standard template, not a page rebuilt by hand at each rollover (council design 3/3, alive 19:37:12Z 10-15, P1 line): `extensions/agi/templates/season_report/report.html` is the season-3 rollover page with every number and sha replaced by a slot (`{{facts.x}}`, `{{narr.x}}`, `{{#rows facts.heads}}...{{/rows}}`), its style block and standing text kept, stdlib only. The player block is in the template but renders only when a media file is passed.

Scale: small. It extends goal:g5.4.1 by one file; the facts reader (`season_report.py facts`) and the render are separate pieces (S1 / S2).
