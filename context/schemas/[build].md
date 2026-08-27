---
name: build
derived_from: corpus-survey-2026-08-25 (n=185 as level3); renamed level3 -> build 2026-08-27, n=190
fields:
  title: {type: str}
  build_kind: {type: str}     # THE DISCRIMINATOR: code | prose
  payload_ref: {type: str}    # path of the file this node IS, relative to engine root
  origin: {type: str}         # build-scan | build-version
  parents: {type: list}
  confidence: {type: float}
  tags: {type: list}
  supersedes: {type: str}
  version: {type: int}
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
      allowed_parents: [idea, goal, verdict, mvp, build]
      min_parents: 1
      max_parents: 2
    prose:
      allowed_parents: [idea, goal, verdict, mvp, build]
      min_parents: 1
      max_parents: 2
---

# build

One file of the engine, as a node. `payload_ref` names where the bytes belong
in the engine tree; since G6.3 the bytes themselves live in the node's grid
ref (`refs/grid/node/<mint-id>:payload`), which is what makes the graph the
source and the engine tree the thing that falls out.

ID prefix: `build:<payload_ref>` — e.g. `build:.gitignore`.

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
