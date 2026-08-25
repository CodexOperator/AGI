---
confidence: 1.0
goal_id: S11
goal_kind: short-term
heading_level: 2
id: "goal:s11"
mint_id: bb55e3a25e244bdd811997143dd84ae7
order: 58
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S11: Retire `level3` as a type name"
type: goal
---

`level3` names a zoom level in the data — the category error G2 now records.
~180 nodes carry `type: level3`, they live in `nodes/level3/`, and the name is
load-bearing in `bin/level3.py`, `bin/stitch.py` (which filters on it), the
`level3-scan` origin stamp, and the `LEVEL3-CONTRACT` block markers.

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
