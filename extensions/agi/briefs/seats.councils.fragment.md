---
id: config:seats
type: frag
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
edited_by: a00-7f9e3d95
season: 2
frag_kind: seats.councils
title: "Council rows for config:seats — one per town, the Keep shared, town cell on every row"
---
<!-- BODY:BEGIN -->
# seats.councils.fragment — one Council per town, the Keep shared

A **Prime-landed** fragment for `config:seats` (`.agi/nodes/.geometry/
seats.md`). This round does not edit the geometry node; the Prime folds these
rows and the `town` cell in at merge-up. Cell-for-cell shape and field names
are copied from the live seat rows in `.agi/nodes/.geometry/seats.md`
(README/`seats:` frontmatter, rows e.g. the director rows in the `seats:`
list — the layout read at iteration L4.117); the ONE new field this
fragment introduces is `town`, and it is introduced on every row.

## The three Council rows to add to `seats:`

Each row uses the same cells as every existing seat row
(name, role, tier, harness, model, effort, settings, session_kind,
personality_ref, handoff_file, pin_ref, rotated_by, owning_goal, worktree,
session_ref) plus the new `town` cell. All three are **idle** until the owner
wakes one — hence empty `harness`/`model`/`effort`/`session_kind`/`worktree`/
`session_ref`; the placeholder row is what makes the seat visible to the
registry and rotatable without a live session. `owning_goal` = the town's
vision.

```yaml
- {"name": "council-core",             "role": "council", "tier": 1, "harness": "", "model": "", "effort": "", "settings": "", "session_kind": "", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/council-core.meter",             "rotated_by": "prime", "owning_goal": "vision:self-perpetuating", "worktree": "", "session_ref": "", "town": "core"}
- {"name": "council-streaming-suite",  "role": "council", "tier": 1, "harness": "", "model": "", "effort": "", "settings": "", "session_kind": "", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/council-streaming-suite.meter",  "rotated_by": "council-core", "owning_goal": "vision:streaming-suite", "worktree": "", "session_ref": "", "town": "streaming-suite"}
- {"name": "council-web-app-suite",    "role": "council", "tier": 1, "harness": "", "model": "", "effort": "", "settings": "", "session_kind": "", "personality_ref": "", "handoff_file": "", "pin_ref": ".agi/sessions/council-web-app-suite.meter",    "rotated_by": "council-core", "owning_goal": "vision:web-app-suite", "worktree": "", "session_ref": "", "town": "web-app-suite"}
```

`council-core` is rotated by the **prime**; the two non-core Councils are
rotated by **council-core** once that seat is awake. `role` for all three is
`council`. `tier` mirrors the director rows the registry already carries.

## The `town` cell on every row

Every seat row in `config:seats` gains a `town` cell:

- **The Keep's seats carry `town: all`.** The Keep — sanctuary-master,
  sanctuary-director, sanctuary-helper, master-sensei, sensei-director, the
  advisors, policy-master, the quorum directors, belam — serves every town,
  so each existing row grows `town: all`.
- **A Council row carries its own town** (`core` / `streaming-suite` /
  `web-app-suite`), matching the `town` cell on the ladder's `towns:` list
  (`.agi/nodes/.geometry/ladder.md` L60-62) and on the town's vision node.

A Council is the lens that owns one town's goals and that town's three
visions; the Keep rows are shared across all towns.

## The reporting chain (prose, rendered by the hierarchy)

- **Core Council → Prime.** The Core Council is the one Council that answers
  directly to the Prime.
- **Every other Council → Core Council.** The streaming-suite and
  web-app-suite Councils report to the Core Council, not to the Prime.
- **While no Core Council is seated, the Prime IS the Core Council** for the
  other towns. This is rendered as the Prime standing in for the empty
  council-core seat, **not** as a missing edge.
- **Masters return work to the Council that originated it.** The Masters
  (Draft, Glitch, Research, Shael) report to the Council whose town your
  round belongs to; a round's town is recorded at mint and its merge-up path
  goes through its originating Council's seat, never any other. That merge-up
  enforcement is the code half of this ladder (season.py / dispatch.py) and
  is outside this fragment's scope — this fragment only declares the rows and
  the chain.
<!-- BODY:END -->
