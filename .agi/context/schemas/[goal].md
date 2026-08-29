---
name: goal
derived_from: corpus-survey-2026-08-25 (n=75, 100% field coverage on every required field)
fields:
  title: {type: str}
  goal_id: {type: str}        # G7 | S4 | G7.2 -- never renumbered
  goal_kind: {type: str}      # THE DISCRIMINATOR: long-term | short-term | subgoal
  status: {type: str}         # active | horizon | phasing-out | complete
  origin: {type: str}         # goals-doc -- derived by snapshot-goals.py
  seeds: {type: list}         # node ids seeded from this goal
  parents: {type: list}       # subgoal only: exactly one goal
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
    status: '^(active|horizon|phasing-out|complete)$'
spawn:
  discriminator: goal_kind
  variants:
    long-term:
      allowed_parents: []
      min_parents: 0
      max_parents: 0
    short-term:
      allowed_parents: []
      min_parents: 0
      max_parents: 0
    subgoal:
      allowed_parents: [goal]
      min_parents: 1
      max_parents: 1
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
variants and illegal in the third.** A flat `allowed_parents: []` on `goal`
would license 48 subgoals to float free. `[shape].md`'s `parentless_types`
therefore lists `goal:long-term` and `goal:short-term`, not `goal`.

## Conventions that are not mechanical checks

- **Goal ids are never renumbered.** A gap beats a renumber. Not checkable
  from one node, so it is not in `validation:`.
- **Retire by marking `phasing-out` and deprecating the seed node — never
  delete.** `phasing-out` is accepted by the `status` regex although the
  corpus has none today (10 `complete`, 25 `horizon`, 40 `active`); it is part
  of the declared four-state lifecycle and dropping it would make the
  documented retirement path fail validation.

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
