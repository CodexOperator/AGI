---
name: config
written_by: [owner, prime_director]   # list-shaped; links.parse_written_by reads a list (L4.50 flip)
self_row: {list_key: seats, match_key: name, fields: [session_ref, session_id, generation, window, pid]}  # L4.110 prime ruling B + L4.114 r3: a seated non-prime role may update ONLY its own seat row (the one whose `name` it resolved from) and ONLY these fields; role/model/tier/harness/effort/owning_goal/worktree/rotated_by stay prime/owner-only and a write touching any of them is refused whole. Driven generically by write.py `_enforce_written_by` from THIS declaration. r3 added session_id (the successor's session uuid) and pid (its process), both supplied by the L4.114 registry JOIN; the row write records source in the rotation record, never here.
structural: true
derived_from: read-2026-08-25 from lib/find-root.sh, bin/level3.py, bin/grid.py
fields:
  locations: {type: dict}            # role -> {path, derivation, declared_in}
  config_marker_names: {type: list}  # what makes a directory a project
  discovery: {type: dict}            # how the graph root is found
  required_keys: {type: list}        # env keys a project cannot run without
  optional_keys: {type: list}        # env keys it will use if present
  forbidden_keys: {type: list}       # env keys that must never be set
  seats: {type: list}                # hypothesis:l3w4-seat-registry — one row per active seat:
                                      # {name, role, tier, harness, model, effort, settings,
                                      #  session_kind, personality_ref, handoff_file, pin_ref,
                                      #  rotated_by, owning_goal, worktree, session_ref}.
                                      #  `worktree` (added hypothesis:l3w4-hierarchy-one-source,
                                      #  goal:g17): the seat's git worktree path relative to
                                      #  graph_root, empty string for a seat that runs in the main
                                      #  checkout. Owner policy: perpetual seats get their own
                                      #  worktree; a director-kid's bootstrap should read this
                                      #  field rather than carry the path only in its spawn brief.
                                      #  `session_ref` (added same node, 2026-09-08): the
                                      #  disambiguating ref ListAgents shows in brackets, e.g.
                                      #  `518293` for row name `agi-4b` -- ListAgents names like
                                      #  `agi-32`/`agi-9d` are NOT unique (several live sessions
                                      #  share one), so a bare-name SendMessage can silently reach
                                      #  the wrong seat. Empty until the seat's own session states
                                      #  its ref (a seat cannot know its ref before ListAgents
                                      #  shows it any more than it can know its own pin transcript
                                      #  before claiming it) -- write it via the seat's own report
                                      #  to its rotator, never guessed by a third party.
validation:
  required: [locations]
  types:
    locations: dict
    config_marker_names: list
    discovery: dict
    required_keys: list
    optional_keys: list
    forbidden_keys: list
    seats: list

# ===========================================================================
# The three filesystem facts, and the three places each is defined today.
# `derivation` is the load-bearing field: these are not literal paths, they
# are *rules*, and the rules disagree in form while agreeing in value.
# ===========================================================================

config_marker_names:            # canonical first; order is significant
  - config.json                 # accepted ONLY inside .agi/ -- too generic elsewhere
  - agi-tree.config.json
  - autoresearch-tree.config.json

graph_dir_name: .agi            # goal:g11 -- the graph directory inside the repo

discovery:
  phase_0: graph_dir            # walk up for <d>/.agi/ holding a config (goal:g11)
  phase_1: up                   # walk up from cwd for a config marker
  phase_2: down                 # else descend into <start>/<basename>-tree/, then <start>/*-tree/
  interleaved: [phase_0, phase_1]  # ONE walk, phase 0 first per dir: nearest enclosing wins
  ambiguous: error              # >1 candidate is a hard error, never a guess
  declared_in:
    - extensions/agi/bin/locations.py :: find_project_root
    - extensions/agi/lib/find-root.sh :: find_project_root

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

  # --- goal:g11 -------------------------------------------------------------
  # The two roots that stop being the same directory once the graph moves
  # inside the repo it builds. Both are CONFIGURABLE, which is the point: one
  # binary has to express the legacy layout and the .agi layout at once, with
  # no branch on project name anywhere (goal:g8.2).

  repo_root:
    role: "the repository enclosing the graph"
    derivation: parent-of-graph-dir-else-identity
    path: "<graph_root>/.. if .agi layout else <graph_root>"
    declared_in:
      - "extensions/agi/bin/locations.py :: repo_root"

  source_root:
    role: "the source the graph describes -- where payload_ref resolves"
    derivation: config-else-layout-default
    config_key: locations.source_root      # relative resolves against graph_root
    path: "<repo_root> if .agi layout else <graph_root>/agi if it exists else <graph_root>"
    declared_in:
      - "extensions/agi/bin/locations.py :: source_root"
    note: >-
      The "run against a custom source location" dial. Under the .agi layout a
      payload_ref names a tracked file in the same worktree, which is what
      removes payload_root's reason to exist -- there is no second repo to
      write the bytes into.

  # --- goal:g1.8 ------------------------------------------------------------
  # The one file class the graph must describe and must never hold. Both are
  # per-project and both resolve against source_root, so a project with the
  # engine cloned in gets its own pair rather than sharing the engine's.

  env_file:
    role: "provider credentials — the VALUES, set once by hand on each box"
    derivation: relative-to-source-root
    path: "<source_root>/.env"
    declared_in:
      - "extensions/agi/bin/envfile.py :: DEFAULT_ENV_FILE"
    gitignored: true
    note: >-
      Has no history, remotely or locally, and that is the design rather than a
      limitation: a version history of a secret is a leak with a changelog. Its
      SHAPE is versioned instead, as env_template below.

  env_template:
    role: "the committed shape of env_file -- which keys, and what each is for"
    derivation: relative-to-source-root
    path: "<source_root>/.env.example"
    declared_in:
      - "extensions/agi/bin/envfile.py :: DEFAULT_TEMPLATE"
    gitignored: false
    note: >-
      An ordinary tracked file with an ordinary build node and an ordinary grid
      ref. Adding, retiring or re-explaining a key is a version; changing a
      value is not.

  goals_file:
    role: "where snapshot-goals.py --render writes the goal document"
    derivation: config-else-layout-default
    config_key: goals_file                 # bare name | relative path | absolute
    path: "<repo_root>/GOALS.md if .agi layout else <graph_root>/GOALS.md"
    declared_in:
      - "extensions/agi/bin/locations.py :: goals_path"
      - "extensions/agi/bin/snapshot-goals.py :: GOALS_MD"
    note: >-
      A bare name goes to the repo root, never inside .agi/ -- the one document
      a human opens first must not be hidden in a dot directory. An override
      also settles the drop-in collision: a repo that already ships its own
      GOALS.md sets goals_file and keeps both.
---

# config

**Structural node type — where things are on the filesystem (G10.2,
`.geometry`).** Declared so the locations are *one* stated fact with its
duplicates named, rather than three constants a reader has to go find.

## What reads this

`bin/spawn_gate.py` reads `locations.nodes_root.path` to resolve where the
node corpus lives, falling back to `<graph_root>/nodes` when the schema is
absent. That is one real read path, which is the bar G10.2 sets.

**`bin/locations.py` (goal:g11) is the second, and it is the one that starts
collapsing the duplication this file was written to document.** It reads
`locations.source_root` and `goals_file` from the project config and owns
`find_project_root`, `repo_root`, `source_root` and `goals_path` for the whole
Python side. `lib/find-root.sh` is its bash half and implements the same phase
order; `tests/test_locations.py::test_bash_and_python_agree` fails if the two
drift.

**What is collapsed, and what is not.** Before G11 the ancestor walk existed
eleven times — ten `CONFIG_NAMES`-plus-walk copies under `bin/`
(`benchmark.py`, `cli.py`, `dispatch.py`, `metrics.py`, `post_wire.py`,
`render-context.py`, `snapshot-build-site.py`, `snapshot-goals.py`,
`spawn_gate.py`, `zoom.py`), plus `lib/find-root.sh`. That shell file is not
one of the residuals — it is the deliberate bash half of the same rule,
cross-checked against `locations.py` by `test_bash_and_python_agree` rather
than trusted to agree on faith. `snapshot-goals.py` is a half-case: it already
calls `locations.goals_path()` but still declares its own `CONFIG_NAMES` and
`config_path()`, so it counts as one of the ten residuals despite already
being a consumer of the new resolver. The other nine still carry their own
copy untouched. That residual is tracked as `goal:g11.1`. `engine_root` also
remains defined twice in Python with two different index arithmetics, off by
one because `level3.py` counts from a directory and `grid.py` counts from a
file — a second, separate duplication class, out of `goal:g11.1`'s scope.
Both are named here rather than fixed, because a resolver duplicated eleven
times cannot be given a new rule once — it has to be given ten new rules that
might drift, which is the whole reason G11 starts here.

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

## The first minted node — 2026-08-31, `goal:g1.8`

`nodes/.geometry/secrets.md` is the first node of this type in the corpus, and
`bin/envfile.py` is the code path G10.2 was waiting on: it reads `locations
.env_file.path`, `locations.env_template.path`, `required_keys`,
`optional_keys` and `forbidden_keys` — five fields, not one — and both
`driver.sh` and `bin/env-get.sh` go through it rather than each spelling `.env`
for themselves. A geometry node earns its place by removing a literal from
code, and this one removes it from two languages at once.

**`validation.required` dropped `config_marker_names` when that node was
minted.** The rule was written speculatively, against zero nodes, and it turned
out to demand that a declaration about *credentials* restate an unrelated list
about *project discovery* — a duplication invented by the validator rather than
by the graph. `locations` alone is required now; a config node still declares
whichever facts it owns and no others.

## Deliberately absent

No `active`/`inactive` variant and no `spawn:` block: `config` nodes are
structural declarations a human or a migration writes, never something a kid is
dispatched to produce.

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
