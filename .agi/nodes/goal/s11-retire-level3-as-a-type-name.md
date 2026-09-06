---
id: goal:s11
mint_id: bb55e3a25e244bdd811997143dd84ae7
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S11
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S11: Retire `level3` as a type name"
---
`level3` names a zoom level in the data — the category error G2 now records.
~180 nodes carry `type: level3`, they live in `nodes/level3/`, and the name is
load-bearing in `bin/level3.py`, `bin/stitch.py` (which filters on it), the
`level3-scan` origin stamp, and the `BUILD-CONTRACT` block markers.

Rename to something that describes what the node *is* rather than which view it
came from — these are code nodes: a file plus the thought attached to it. `code`
is the obvious candidate.

**Why it is not a five-minute `sed`:** the string appears as a node type, a
directory name, a file-name prefix, an `origin` value, an HTML comment marker
inside every node body, and a Python module name. Changing the `origin` stamp is
the sharp edge — `level3.py` prunes exactly the nodes whose origin it recognises,
so a half-applied rename means a scan that no longer recognises its own output
and prunes ~180 real nodes. That is the H0/H0i failure mode with a new spelling.

Sequence it: teach the reader both names first, migrate the data, then retire the
old name from the writer. Never the reverse. Pairs with **G7.5** — a rename that
silently drops nodes must fail loudly, not return exit 0.

## Complete 2026-08-27 — all six surfaces, one commit

Done in commit `de08acaff`, atomically, because a half-applied rename is H0i
with a new spelling. What moved: node `type:`, `id:` prefix, directory
(`nodes/level3/` -> `nodes/build/`), the `origin` stamp
(`level3-scan` -> `build-scan`), the body markers
(`LEVEL3-CONTRACT` -> `BUILD-CONTRACT`), and the writer in `bin/level3.py`.

190 ids renamed, 0 collisions, 253 occurrences across 209 files. Verified at
each step: dry run reported 185 `would update` and **0 prunes**, the real run
wrote 185 and pruned 0, node count 785 -> 785.

**The sharp edge this goal warned about was disarmed by an asymmetry**, not by
care: readers accept both names (`stitch.py` reads `nodes/build/` and falls
back to `nodes/level3/`, and matches either contract marker), while the
**pruner recognises only the new one**. `LEGACY_ORIGIN` exists to be
recognised, never pruned on — a straggler still stamped `level3-scan` is left
alone. `test_a_node_stamped_with_the_LEGACY_origin_is_never_pruned` holds that
open so the two rules cannot quietly converge.

`build_kind: code | prose` was added as a discriminator, derived mechanically
from the payload suffix: 145 code, 45 prose.

**Two things this goal did NOT do, both deliberate:**

- **`bin/level3.py` keeps its filename.** Renaming the module is **G7.9**, held
  back so a bisect stays possible if either half went wrong.
- **The `@v2` convention survives.** See **G2.10**: those five nodes are
  currently the only durable place a build artifact's reasoning can live,
  because the scan wipes build-node bodies. Collapsing them now would delete
  prior art to satisfy a naming rule.

One miss worth remembering for the next rename: `[experiment].md` still listed
`level3` in `allowed_parents`, which an id-rename pass cannot see because a
bare type name has no `:` in it. Caught afterwards by running the spawn gate
over the whole corpus. **Do that as the last step of any type rename.**
