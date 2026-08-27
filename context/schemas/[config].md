---
name: config
structural: true
derived_from: read-2026-08-25 from lib/find-root.sh, bin/level3.py, bin/grid.py
fields:
  locations: {type: dict}            # role -> {path, derivation, declared_in}
  config_marker_names: {type: list}  # what makes a directory a project
  discovery: {type: dict}            # how the graph root is found
validation:
  required: [locations, config_marker_names]
  types:
    locations: dict
    config_marker_names: list
    discovery: dict

# ===========================================================================
# The three filesystem facts, and the three places each is defined today.
# `derivation` is the load-bearing field: these are not literal paths, they
# are *rules*, and the rules disagree in form while agreeing in value.
# ===========================================================================

config_marker_names:            # canonical first; order is significant
  - agi-tree.config.json
  - autoresearch-tree.config.json

discovery:
  phase_1: up                   # walk up from cwd for a config marker
  phase_2: down                 # else descend into <start>/<basename>-tree/, then <start>/*-tree/
  ambiguous: error              # >1 candidate is a hard error, never a guess
  declared_in: extensions/agi/lib/find-root.sh

locations:
  graph_root:
    role: "the graph repo -- GOALS.md, agi-tree.config.json, nodes/"
    derivation: ancestor-walk-for-marker
    path: "<dir containing agi-tree.config.json>"
    declared_in:
      - extensions/agi/lib/find-root.sh :: find_project_root
      - extensions/agi/bin/cli.py :: _find_root
      - extensions/agi/bin/post_wire.py :: _find_root
    env_override: AGI_TREE_PROJECT_ROOT   # legacy: AUTORESEARCH_TREE_PROJECT_ROOT

  engine_root:
    role: "the assembled code repo -- what stitch.py --publish writes to"
    derivation: relative-to-this-file
    path: "<engine>"
    declared_in:
      - "extensions/agi/bin/level3.py :: DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]"
      - "extensions/agi/bin/grid.py :: default_engine_root() = Path(__file__).resolve().parents[3]"
    note: >-
      Same value, two different index arithmetics, off by one because level3
      counts from a directory and grid counts from a file. Neither is wrong
      and either breaks silently if bin/ moves (S1 proposes exactly that).

  payload_root:
    role: "staged checkout of build-node payloads -- where engine code is edited"
    derivation: relative-to-graph-root
    path: "<graph_root>/payloads"
    declared_in:
      - "extensions/agi/bin/grid.py :: checkout --dir (default <root>/payloads)"
      - "extensions/agi/bin/grid.py :: resolve_payload (priority 1 over engine_root)"
    gitignored: true

  nodes_root:
    role: "the graph itself"
    derivation: relative-to-graph-root
    path: "<graph_root>/nodes"
    declared_in:
      - "extensions/agi/bin/evidence_gate.py :: build_corpus(root / 'nodes')"
      - "extensions/agi/bin/spawn_gate.py :: build_type_index"

  schemas_root:
    role: "node-type schemas -- [name].md active, name.md inactive"
    derivation: relative-to-graph-root
    path: "<graph_root>/context/schemas"
    declared_in:
      - "extensions/agi/src/schema_registry/loader.py :: load_schemas_from_dir"
---

# config

**Structural node type — where things are on the filesystem (G10.2,
`.geometry`).** Declared so the locations are *one* stated fact with its
duplicates named, rather than three constants a reader has to go find.

## What reads this

`bin/spawn_gate.py` reads `locations.nodes_root.path` to resolve where the
node corpus lives, falling back to `<graph_root>/nodes` when the schema is
absent. That is one real read path, which is the bar G10.2 sets. **The
remaining locations are declared and not read** — `engine_root` in particular
is still defined twice in Python and once in shell, and collapsing those three
into this file means editing `level3.py` and `grid.py`, which this change does
not own. Recorded as the residual; the duplication is *documented* here, not
*removed*.

## Field meanings

- `derivation` — **how** the path is computed, not what it currently is. The
  three kinds observed: `ancestor-walk-for-marker` (search up for a file),
  `relative-to-this-file` (index arithmetic on `__file__`),
  `relative-to-graph-root` (a fixed subdirectory).
- `declared_in` — every place the engine states this fact today. A location
  with more than one entry is a duplication that has not been collapsed yet.
- `path` — the resolved shape, with `<...>` for what is filled in at runtime.
  Never an absolute path: this schema ships with the engine and must not
  encode one machine's layout (G8.2 — no project-specific branch anywhere).

## Deliberately absent

No `active`/`inactive` variant, no `spawn:` block, no `parents` rule: there
are zero `config` nodes in the corpus. This file declares a shape; nothing has
been minted against it. Minting a `.geometry/` node from it is G10.2's job and
waits on a code path that reads more than one field.

## The `THOUGHT` block (goal:g2.11)

A node body may carry one authored region, marked exactly like the harness
markers it sits beside:

```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one
<!-- THOUGHT:END -->
```

**`body` is state; `thought` is delta.** The body says what this node asserts
now. The thought says why *this version* differs from the previous one — it is
rewritten from scratch on each change, not accumulated.

- **Absent means empty.** No node is required to carry one, which is why
  introducing the block churned 0 of 786 existing nodes. Fill it when there is
  something to say; never fabricate one after the fact.
- **It survives regeneration.** Writers that rebuild a body (`level3.py`,
  `snapshot-build-site.py`, `decompose-engine.py`) carry this region across
  verbatim via `write_frontmatter(..., preserve_body=...)`. Before 2026-08-27
  they did not, and 8,034 authored contract fields were destroyed unread
  (goal:g2.10).
- **Versioning is free.** The grid snapshots `node.md` once per version, so
  each grid commit already carries the thought current at that version.
- **Not in frontmatter, deliberately.** `write_frontmatter` flattens newlines,
  so multi-line prose in a frontmatter field is silently destroyed. The short
  scalar `thought_session:` is reserved there for goal:g2.7 / goal:g10.1 to
  point at the chat that produced a version; it is not populated yet.
- **Readers strip it.** Thought is provenance to zoom into, not weight every
  reader carries forever. `snapshot-goals.py --render` strips it explicitly via
  `strip_thought()`; `render-context.py` and `zoom.py` never see it because
  they read frontmatter only (`load_node_file(..., body=False)`) and so carry
  no body text at all. The rule binds any future reader that *does* read
  bodies.
