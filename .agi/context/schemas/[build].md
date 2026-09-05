---
name: build
derived_from: corpus-survey-2026-08-25 (n=185 as level3); renamed level3 -> build 2026-08-27, n=190
fields:
  title: {type: str}
  build_kind: {type: str}     # THE DISCRIMINATOR: code | prose
  payload_ref: {type: str}    # path of the file this node IS, relative to `location`
  location: {type: str}       # NAME of the base it resolves against; default source_root
  origin: {type: str}         # build-scan | build-version
  parents: {type: list}
  confidence: {type: float}
  tags: {type: list}
  supersedes: {type: str}
  version: {type: int}
  status: {type: str}         # absent = live; `deprecated` = retired in place
validation:
  required: [id, type, mint_id, title, build_kind, payload_ref, origin, confidence, tags]
  types:
    payload_ref: str
    confidence: float
    tags: list
  regex:
    build_kind: '^(code|prose)$'
spawn:
  discriminator: build_kind
  variants:
    code:
      allowed_parents: [mvp, build, goal]
      min_parents: 1
      max_parents: 2
      parent_shapes:
        - [mvp]
        - [build, goal]
    prose:
      allowed_parents: [mvp, build, goal]
      min_parents: 1
      max_parents: 2
      parent_shapes:
        - [mvp]
        - [build, goal]
---

# build

## Where a build node may come from (2026-09-02)

**Two shapes, and nothing else:**

```
parents: [mvp:<id>]                    a NEW build node, specified by an mvp
parents: [build:<id>, goal:<id>]       a NEW VERSION of an existing build node
```

`parent_shapes` in the `spawn:` block above is an **OR across whole shapes**,
which `allowed_parents` alone cannot express — a flat allow-list would also
permit a lone `goal`, and **a goal must not be able to mint a build node out of
nothing.** A goal can only motivate a new version of a file that already
exists.

**Why an mvp for a new build node.** An `mvp` states the minimum a subsequent
`build` must satisfy plus its falsifier (`[mvp].md`, revised 2026-09-01). A
build node with an mvp behind it is a file somebody argued for; one without is
a file somebody wrote.

**Why `[build, goal]` for a version, and both halves.** The `build` parent says
*which* file this is a new version of. The `goal` says *why this version
differs* — which is the one thing a diff cannot tell you. Neither alone is
enough: a lone `build` parent is a version with no motive, and a lone `goal` is
the mint-from-nothing case above.

**This composes with the version rule rather than replacing it.** A version is
a grid commit, not a second node file (`goal:g6.3`) — you edit the build node in
place and `grid.py commit --all` records it. What this shape governs is the
node's `parents:` when a goal is the reason for the edit: the goal joins the
lineage, so the grid history answers "why" as well as "what".

### The existing corpus is grandfathered, deliberately

**216 build nodes predate this rule** — 192 parented by an `idea` (the
`level3.py` census parent), 19 with no parents at all, 5 by a goal. **None of
them is retro-invalid.** Their empirical worth is established by the fact that
they exist and the engine runs on them; re-deriving an mvp for each would be
archaeology, not evidence.

Two mechanical facts make the grandfathering real rather than a promise:

- **`spawn_gate` is creation-time only.** It does not touch history — it
  already tolerates 51 nodes in this corpus that violate `min_parents`.
- **`level3.py` does not route through `node_writer`/`spawn_gate` at all**, so
  the rescan that re-mints all 216 build nodes with their census parents is
  unaffected by this change. Checked before making it, because tightening a
  schema that a generator wrote through would have broken every scan.

`idea` and `verdict` were dropped from `allowed_parents` for the same reason
they are not in either shape: they were the census-era answer, and the census
is the thing being grandfathered rather than continued.


One file of the engine, as a node. `payload_ref` names where the bytes belong
in the engine tree; since G6.3 the bytes themselves live in the node's grid
ref (`refs/grid/node/<mint-id>:payload`), which is what makes the graph the
source and the engine tree the thing that falls out.

ID prefix: `build:<payload_ref>` — e.g. `build:.gitignore`.

## `location` — the payload's base is a name, not a path (2026-09-05)

`payload_ref` is a **relative** path, and until now the thing it was relative
to lived in the code: three call sites each resolved it against
`locations.source_root()`. That is fine while every payload lives in one tree
and wrong the moment one does not — a doc set beside the repo, a second
checkout, a generated tree, a project that rearranges itself.

**`location:` names the base; it never contains a path.**

```yaml
payload_ref: extensions/agi/bin/write.py
location: source_root          # the default, stamped at creation
```

Names resolve through `locations.payload_base()`, the single place a name
becomes a directory:

| name | is |
|---|---|
| `source_root` | the repo enclosing `.agi/` — the default, and what every node meant before this field existed |
| `graph_root` | the `.agi/` directory itself |
| `repo_root` | the enclosing git repo |
| *anything under `locations:` in the project config* | whatever that key declares — absolute as given, relative against the graph root |

**Absent means `source_root`.** The 224 build nodes that predate the field keep
resolving exactly as they did; nothing was rewritten to add it, and nothing
needs to be.

**An unknown name is a hard error naming the node, never a fallback to the
default.** Silently resolving somewhere plausible would write real bytes into
the wrong tree and report success — the one failure mode a payload base has
that nobody would notice until much later.

**Why a name and not a path.** A path in the node is the same hardcoding, moved
one level: a tree that shifts would mean a sweep over every node pointing into
it. A name means the shift is one config edit. This is `goal:g1`'s rule —
every engine action is declared, never improvised — applied to the question
"where do these bytes live".

**`write.py create --payload` stamps it** with the default rather than leaving
it implicit, so the field is visible on the node and can be changed by hand
later. `write.py <id> "payload_text <bytes>"` and `"payload <path>"` both
resolve through it, and a `location` set in the same edit wins over the one on
disk — naming a new base and moving the bytes is one intention, not two.

## Renamed from `level3` on 2026-08-27

The old name was a **zoom level**, and G2/G10.2 both record that as a category
error: zoom is a property of the view, never of the node, and naming the grain
on the node tells an agent to identify with a grain instead of working at one.
S11 asked for a name describing what the node *is*. It is a build artifact —
a file, plus the thought attached to it.

The rename was atomic across six surfaces in one commit, because a
half-applied one is H0i with a new spelling: node type, `id:` prefix,
directory, `origin` stamp, `BUILD-CONTRACT` body markers, and the writer in
`bin/level3.py`. Two asymmetries carry the safety:

- **Readers accept both names; the pruner recognises only the new one.**
  `stitch.py` reads `nodes/build/` and falls back to `nodes/level3/`, and
  matches either contract marker. But `level3.py` prunes only nodes stamped
  with its current `ORIGIN` (`build-scan`) — a straggler still stamped
  `level3-scan` is *left alone*, never deleted. "This scan does not recognise
  it" and "this node is stale" are different statements and only the second
  licenses removal.
- **The module is still `bin/level3.py`.** Renaming the file is **G7.9**, held
  deliberately: the type rename is the one with 190 nodes behind it, and
  bundling a module rename into the same commit would have made a bisect
  impossible if either half went wrong.

## The discriminator, and an honest limitation

`build_kind` is derived mechanically from the payload suffix —
`.py .sh .ts .js` are `code`, everything else is `prose` — so G6.8's boundary
answers without a human adjudicating. Measured over 190: **145 code, 45
prose**.

**Both variants currently declare the same `allowed_parents`, and that is
worth stating rather than hiding.** The intent is that code and prose build
nodes diverge — different spawn workflows, different review. They do not
diverge *yet*, and there is a mechanical reason they cannot fully:
`allowed_parents` matches on a parent's **type**, which is `build` for both
kinds, so "a prose node may be parented by a code node but not vice versa" is
not expressible in today's grammar. Variant-aware parent matching is the
follow-up; the discriminator is declared now so the field exists and is
populated before anything depends on it.

`idea` stays in both lists because 180 of 190 nodes use it. Dropping it to
match a cleaner design would have made 95% of the corpus violate a rule
invented the same day, which is a rule about nothing.

## Spawn rule

Observed over 190 nodes: `idea` 180, `goal` 5, parentless 5. `min_parents: 1`
— a build node is a census entry under a decomposition idea; floating free it
belongs to no decomposition. The 5 parentless are a **report, not a purge**.

`verdict` and `mvp` are newly admitted: a fix that lands as a new version of a
build node descends from the verdict that justified it, which is G6.3's and
G6.4's shape. No node uses it yet.

## The harness-owned contract block

Each node body carries a `BUILD-CONTRACT:BEGIN/END` block derived by
`bin/level3.py` from the payload. It is **harness-owned**: a model may fill
`why`/`perf`/`security` and must never add, remove or reorder fields. Not
expressible in the field DSL (it lives in the body, not the frontmatter), so
it is stated here and enforced by the writer.

**A stored value the derivation does not reproduce makes the graph
permanently dirty**, which silently shuts the publish cron's first gate — one
character of YAML quoting did that for weeks before 2026-08-27. See G6.5.

## `status: deprecated` — retirement, and where a retired node lives

**Absent means live.** `status` is optional and unset on every live build node;
it is not in `required` for that reason, and adding it there would invalidate
185 nodes to express a default.

`deprecated` marks a node retired in place. **A retired node is kept, never
deleted.** The reason is not sentiment about prior art — it is that a node's
grid ref (`refs/grid/node/<mint-id>`) *outlives its file*. Deleting the file
does not shrink the durable structure; it decouples it, leaving a ref and any
`supersedes:` edges with nothing live behind them. An orphaned ref is worse
than a marked-dead file, and G10's hypergraph is what would have to reconcile
the difference.

A retired node moves to **`nodes/deprecated/<type>/`** — the same per-type
split, one level down. That changes its **address**, which is derived and
expected to change on regroup, and never its **mint id**, so every grid ref and
provenance link keeps resolving (goal:g2.5).

Retirement is deliberately **not** visible in `node_count`, which still counts
every node file. It shows up in `active_node_count` and `deprecated_node_count`
instead. A shrinking total is the shape that hides loss, which is what G7
forbids; a flat total plus a second number that moves is what makes retiring in
place trackable rather than silent.

Readers that walk `nodes/` recursively need nothing. The four that globbed a
single type directory — `stitch.py`, `level3.py`, `node_writer.py`, `zoom.py` —
read both, live first. **The order is load-bearing** wherever a reader takes the
first hit: a live node must win over a retired namesake. And `stitch.py` must
keep reading retired nodes at all, because a retired node still *claims* its
`payload_ref` — dropping it would turn its engine file into an `orphan_files`
report and refuse the publish, purely because the node was regrouped.

`level3.py` writes a node back to **the path it already occupies**, not the
address a fresh mint would choose, so a scan cannot recreate a retired node at
its live address and leave one id in two files.

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
