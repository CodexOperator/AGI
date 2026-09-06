---
name: goal
derived_from: corpus-survey-2026-08-25 (n=75, 100% field coverage on every required field)
fields:
  title: {type: str}
  goal_id: {type: str}        # G7 | S4 | G7.2 -- never renumbered
  goal_kind: {type: str}      # THE DISCRIMINATOR: long-term | short-term | subgoal
  status: {type: str}         # active | horizon | retired | complete  (`phasing-out` = legacy `retired`)
  origin: {type: str}         # goals-doc -- derived by snapshot-goals.py
  seeds: {type: list}         # node ids seeded from this goal
  parents: {type: list}       # subgoal: >=1 goal; any variant may add a build
  confidence: {type: float}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, goal_id, goal_kind, status, origin, seeds, confidence, tags]
  types:
    seeds: list
    tags: list
    confidence: float
  regex:
    goal_id: '^[GS]\d+(\.\d+)*$'
    goal_kind: '^(long-term|short-term|subgoal)$'
    status: '^(active|horizon|retired|phasing-out|complete)$'
spawn:
  discriminator: goal_kind
  variants:
    # goal:long-term and goal:short-term are no longer parentless-legal
    # (parentless_types is now [moral]; the 27 pre-existing roots are
    # season 1, grandfathered, never re-gated).
    long-term:
      allowed_parents: [build, goal]
      min_parents: 1
      max_parents: 2
    short-term:
      allowed_parents: [build, goal]
      min_parents: 1
      max_parents: 2
    subgoal:
      allowed_parents: [build, goal]
      min_parents: 1
      max_parents: 3
      min_parents_by_type: {goal: 1}
---

# goal

The long-term contract. **These nodes are the source; `GOALS.md` is derived
from them** — `driver.sh` runs `snapshot-goals.py --render`, which writes
`GOALS.md` out of `nodes/goal/*.md`. Edit the node. A hand-edit to `GOALS.md`
survives until the next `--smoke` run and then vanishes with no warning.
`--render --check` exits 0 only on a byte-identical round trip.

The arrow reversed on 2026-08-25 (goal:g6.9, commit `2b204a5d4`); this file,
and `CLAUDE.md` in two places, still said the opposite until 2026-08-26. The
`origin: goals-doc` marker is left over from when `GOALS.md` *was* the source —
it now means "participates in the GOALS.md round trip", and `snapshot-goals.py`
still keys its prune on it, so it is load-bearing under a name that no longer
describes it.

ID prefix: `goal:<lowercased goal_id>` — `## G7` → `goal:g7`,
`### G7.2` → `goal:g7.2`, `## S4` → `goal:s4`.

## One schema with a discriminator, not two — and this is not a taste call

G-goals and S-goals are two shapes of one `type: goal` node, and the corpus
adds a third the brief did not name: `subgoal`.

The decision is forced by the registry, not chosen. `SchemaRegistry.resolve()`
(`schema_registry/loader.py`) looks a schema up **by the node's `type:`
field**. Every goal node in the corpus is `type: goal`. A `[g-goal].md` and a
`[s-goal].md` would register under the names `g-goal` and `s-goal`, which no
node's `type:` ever equals — so `resolve("goal")` would miss both, fall
through to the generic schema, and the two files would be dead data that
looked authoritative. **Two files is only defensible if `type:` splits too,
and splitting `type:` renames 75 nodes for no gain.** One file, discriminated
on `goal_kind`.

## The three variants, and why parentlessness is per-variant

Measured over all 75 goal nodes — the correlation is exact, zero exceptions:

| `goal_kind` | n | parents | `goal_id` | example |
|---|---|---|---|---|
| `long-term` | 10 | 0 | undotted `G7` | `## G7` → `goal:g7` |
| `short-term` | 17 | 0 | undotted `S4` | `## S4` → `goal:s4` |
| `subgoal` | 48 | exactly 1 (`goal`) | dotted `G7.2` | `### G7.2` → `goal:g7.2`, `parents: [goal:g7]` |

So "exactly three types may be parentless: G-goal, S-goal, `idea`" is precise
only when stated per-variant: **`goal` is parentless-legal in two of its three
variants and illegal in the third.** `[shape].md`'s `parentless_types`
therefore lists `goal:long-term` and `goal:short-term`, not `goal`. The table
above is the corpus as surveyed on 2026-08-25 and is now a floor rather than a
ceiling — see the next section.

## A goal may be spawned by a build node (2026-09-05)

**Widened at the owner's request, and the widening is small on purpose:**

| `goal_kind` | may have | must have |
|---|---|---|
| `long-term` | up to 2 parents, each a `build` or a `goal` | nothing — parentless stays legal |
| `short-term` | up to 2 parents, each a `build` or a `goal` | nothing — parentless stays legal |
| `subgoal` | up to 3 parents, each a `build` or a `goal` | **at least one `goal`** (`min_parents_by_type`) |

**What this buys.** A goal usually comes from somewhere, and until now the graph
could not say where. `COMPLETE.md` — the post-loop completion report
(`goal:g1.13`) — is the worked example: eight goals were minted *because of what
that report found*, and with `allowed_parents: [goal]` the only way to record it
was an edge pointing the wrong way, from the report at the goals. Now the goals
name the document that produced them and the provenance reads in the direction
the graph already reads everything else: **parents are where this came from.**

**Why `build` specifically, and not "any type".** A build node is a file with a
thought attached, and a document that argues for new work — a report, a survey,
a design note — is exactly a prose build node. Letting `hypothesis` or `verdict`
parent a goal would invert the chain the whole engine is built on (goals seed
hypotheses, not the reverse) and would make `outcome_coverage` circular.

**Why a subgoal still needs its goal.** `min_parents_by_type: {goal: 1}` is an
AND across kinds, so a subgoal may gain a `build` parent and even a second goal,
but it can never float free of the root it belongs under. That root is what
`GOALS.md` nests it beneath and what `goal:s26`'s completion check walks.

**The one place this is not yet symmetric:** `snapshot-goals.py`'s *ingest*
direction (`GOALS.md` → nodes) writes a subgoal's `parents:` from the heading
hierarchy, so it can only reconstruct the goal parent. It now preserves any
non-goal parent already on disk rather than dropping it, which is enough because
`--render` (nodes → `GOALS.md`) is the live direction and the one `driver.sh`
runs. A build parent minted only in `GOALS.md` prose is still unrepresentable —
mint it on the node.

## Conventions that are not mechanical checks

- **Goal ids are never renumbered.** A gap beats a renumber. Not checkable
  from one node, so it is not in `validation:`.
- **Retire by marking `retired` and deprecating the seed node — never
  delete.** Renamed from `phasing-out` on 2026-09-02 (goal:g5): the lifecycle
  already meant "retired" and every document already said so, while the field
  said something else. **`phasing-out` stays in the `status` regex
  permanently**, not for one migration window — projects predating the rename
  carry it, and a reader that stopped accepting it would fail their goals
  validation rather than reading them as retired.
- **`retired` and `complete` are not the same state and must not be scored
  alike.** `complete` = achieved; its chains stay in the corpus and keep
  scoring. `retired` = stopped making sense; its closed chains leave the
  score while staying in the graph. Collapsing them made `outcome_coverage`
  fall 0.27 -> 0.232 on a sweep that undid no work — see `metrics.py ::
  SCORING_GOAL_STATUSES`.

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
