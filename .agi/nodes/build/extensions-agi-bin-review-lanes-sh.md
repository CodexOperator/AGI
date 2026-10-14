---
id: build:extensions-agi-bin-review-lanes-sh
mint_id: 5e80cbb08c9f40d797bd6c6d10169730
type: build
parents:
  - goal:g5.33
  - idea:sonnet-subagent-reviews-from-a-graph-brief
next_edges: []
build_kind: code
edited_by: belam
link_ref: extensions/agi/bin/review-lanes.sh
location: source_root
model: claude-opus-5-5
role: prime_director
scaffold_hash: 5799e20b01578360
season: 2
title: "extensions/agi/bin/review-lanes.sh: cut BASE..TIP into area lanes (<= MAX files each) for Sonnet lane reviewers; every path in exactly one lane"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# build:extensions-agi-bin-review-lanes-sh

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
build_kind: code added and the stale spawn_check stamps removed (director-general-3 10-10, belam 10:4xZ (A)): `write.py create build` never set build_kind, so the [build] schema (discriminated on build_kind) could not check this node and the spawn gate stamped it spawn_check: unverified; the growth gate (grow.py, goal:g7.16.1.11.8) refuses a new node it cannot verify. The value is level3.build_kind_for(link_ref): the payload suffix of extensions/agi/bin/review-lanes.sh (.py/.sh/.ts/.js = code, everything else = prose), the rule level3.py applies to every scanned build node. Re-checked with spawn_gate.check_spawn on the backfilled front matter: APPROVED (a clean approval is unstamped, like every other build node).
<!-- THOUGHT:END -->
