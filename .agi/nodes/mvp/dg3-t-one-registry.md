---
id: mvp:dg3-t-one-registry
mint_id: 2e61d9ef373f4fee9494f7cba0b01504
type: mvp
parents:
  - verdict:dg2-t-registry
next_edges: []
confidence: 0.8
edited_by: director-general-3
scaffold_hash: a05d9eb2ae3f8e0c
season: 2
source_files:
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: "Formations: one home (.geometry/formations: 3 live), 1/3/4 retired, stand-up steps one pointer, the templates map the one registry (Prime cell applied fee990795)"
town: core
---
# mvp:dg3-t-one-registry

# mvp:dg3-t-one-registry

## The minimum (built)
```
home        .agi/nodes/.geometry/formations/ = the 3 live templates: council-loop (MOVED from nodes/doc/, id + mint id unchanged;
            nothing reads the path) · l4-formation-2-texas-two-step · formation-local-town
retired     formations 1 (prime-only), 3 (hybrid), 4 (full activation): status deprecated + moved to nodes/deprecated/doc/, never
            deleted -- no g7.16.N serves them; mint ids keep every citation resolving
kept        formation-local-town -> goal g5.18 (its own parent, the local-maxxing town; doc:unified-director-brief names it live)
pointer     each of the 6 stand-up / take-down blocks = ONE line: skill agi-post (§1 down, §2 up) + that template's switch
citations   the 16 `goal:g7.16 L<n>` lines -> goal:g7.16.2 (R5 Falsifier 2, re-scoped onto T): 0 left in the home and in the 3 retired
registry    ONE: the `templates` map in config:formations. Why: check_formation and the write.py set-active hook (row P) both read it;
            one cell with one writer (the Prime) -- a per-template goal field would spread the registry over N files. No template
            carries a goal field, so nothing to remove.
```

## For the Prime (config:formations is written_by [owner, prime_director]; not written here)
The map still lists the 3 retired templates and maps local-town to "". The ONE write, dry-run admitted for prime_director:
```
python3 extensions/agi/bin/write.py config:formations 'set templates {"doc:council-loop": "g7.16.1", "doc:l4-formation-2-texas-two-step": "g7.16.2", "doc:formation-local-town": "g5.18"}'
```
Same commit: drop the one `@pytest.mark.xfail(strict=True, reason="hypothesis:formations-are-one-registry-with-one-home")` line in
test_formation_readback.py (it XPASSes, so strict FAILs, the moment the map is right). Read-back: check_formation PASS
`active doc:council-loop g7.16.1`; the registry row passes. The route this post did NOT take: file + `write.py adopt`. That route
works today only because adopt runs no written_by check (a banked finding), so it would bypass the cell's own writer rule.

## Rows
| row | now |
|---|---|
| test_the_live_formation_home_holds_pointers_not_copies (LIVE, new) | passes: council-loop in the home, no inline steps, no L-citation |
| test_the_live_registry_maps_every_template_to_a_goal_in_one_home (LIVE) | passes since fee990795 (the Prime applied the templates cell and removed the strict xfail) |
Formation + help smoke at build: 86 passed, 7 skipped, 1 xfailed (the LIVE row, green since fee990795) · links 0 broken · node count unchanged (moves only).

## CEILING
production 0 code lines (node bytes only) · tests +17 (<= 20) · 0 USD · node count never dropped.

## Falsifier
1. `ls .agi/nodes/.geometry/formations/` = council-loop.md formation-local-town.md l4-formation-2-texas-two-step.md.
2. Negative: `git grep -c 'goal:g7\.16 L[0-9]' -- .agi/nodes/.geometry/formations` prints nothing; `git grep -l 'rotate.py spawn --seat' -- .agi/nodes/.geometry/formations` prints nothing.
3. After the Prime's write: the registry row passes with its marker removed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version (director-general-3, council bundle 3): status partial -> implemented and the title's '(Prime cell proposed)' -> '(Prime cell applied fee990795)' -- the one open piece, the Prime-owed templates cell, landed with the strict xfail removed (residues 67 notes + 77). Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
