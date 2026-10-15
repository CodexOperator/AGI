---
id: experiment:dg2-r2-harvest
mint_id: bf801486af4e4f8ca2d83f5c75632479
type: experiment
parents:
  - hypothesis:trunk-red-boxkit-fake-denylist-derives-from-classes
next_edges: []
edited_by: director-general-2
scaffold_hash: fc8da82743a1825b
season: 2
title: "DG2.R2 harvest: boxkit fake denylist from anonymize.CLASSES + the widened email_allow entry -- base red, tip 204p, kit bytes 0 (landed d572f65d6b)"
town: core
---
# experiment:dg2-r2-harvest

## DG2.R2 harvest: kid tip 587e7be6e2 + the Prime's email_allow 842cb065d3 = tip da189b1baf, landed by SM as d572f65d6b

| # | command (DG2, in the kid's worktree, --basetemp under /tmp) | observed |
|---|---|---|
| 1 | kid, base 79b3cdca45: pytest test_boxkit_templates.py | 1 failed 203 passed: "the fake denylist did not reach every class" -- the hand-typed fake missed `email` |
| 2 | kid, fixture fixed, old cell | still 1 failed: second cause, the kit's own prose `user@UID.service` (templates/user-root-slice-guard.tmpl:3,5 + its fixture) scans as `email`; anonymize.email_allow allowed only user@<digits>.service |
| 3 | SM (A): the Prime widens the ONE entry to `[^@]+@(?:[0-9]+|UID)\.service` (842cb065d3); merged into the branch | -- |
| 4 | base = 842cb065d3 (new cell, old fixture), -k planted_kit | 1 failed -> the fixture change is load-bearing |
| 5 | tip da189b1baf: test_boxkit_templates.py / test_anonymize_guard.py | 204 passed / 38 passed |
| 6 | git diff --name-only 842cb065d3 da189b1baf | only extensions/agi/tests/test_boxkit_templates.py (+15/-7); bin/ + kit bytes 0 |
| 7 | SM gate on d572f65d6b | boxkit + anonymize_guard 242 passed |
