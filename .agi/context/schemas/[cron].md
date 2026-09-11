---
name: cron
structural: true
derived_from: authored-2026-08-29 for G10.2 -- no prior corpus to survey; this
  schema and its one node are minted together, the node's shape following
  the reader that consumes it rather than a census of existing nodes
fields:
  crons_live: {type: bool}   # master switch; false means every managed line is removed
  cadences: {type: dict}     # job name -> {every_mins: int, schedule: str, enabled: bool}
  services: {type: dict}     # OPTIONAL: service name -> systemd unit settings; absent = no units
validation:
  required: [crons_live, cadences]
  types:
    crons_live: bool
    cadences: dict
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 1
---

# cron

**Structural node type — cadence and enablement declared as graph content
(G10.2, `.geometry`).** Not `[config].md`: that schema's `validation.required`
is `[locations, config_marker_names]`, which a cadence declaration cannot
satisfy, and its `locations.nodes_root` field is a live read path a `cron`
node has no business relaxing. A cadence is a different fact from a
filesystem location, so it gets its own schema rather than a shared one
loosened to fit both.

## What reads this

The cron-applier reads `crons_live` and `cadences` and reconciles the
system's real scheduled-job table against them: an `enabled: true` cadence
gets a managed line, `enabled: false` or an absent job gets none, and
`crons_live: false` removes every managed line regardless of what
`cadences` says. That is the real code path G10.2 requires before a
`.geometry` node is allowed to exist — the node is not documentation about
scheduling, it is the input the applier resolves against.

## Field meanings

- `crons_live` — the kill-switch. One boolean gates the whole set, because
  some operations (a repo migration, a bulk rewrite) are only safe with
  nothing else racing them, and disabling four cadences one at a time is
  four edits where one is correct.
- `cadences` — a map of job name to its schedule and whether it is currently
  wanted. A job entry declares its timing **one of two ways, never both**:
  - `every_mins: <int>` — run every N minutes, for a job whose cadence is a
    simple interval.
  - `schedule: "<5-field cron expression>"` — run at the stated wall-clock
    time(s), for a job whose cadence is not a plain interval.

  This "exactly one of the two" rule is stated here but **not mechanically
  enforced** by this schema — the validation DSL (`required` / `types` /
  `regex`) checks top-level fields only and cannot see inside a nested
  mapping. The applier that reads `cadences` is where a job declaring both,
  or neither, would actually be caught. Recorded honestly as a residual
  rather than claimed as a guard that does not exist.
- `enabled` — per-job, independent of `crons_live`. A job can be declared
  and turned off without deleting its cadence, the same way a node is
  retired by status change rather than removal.
- `services` — **optional**, a map of systemd unit name to its settings
  (`exec_start`, `restart`, `working_directory`, `environment`, `enabled`),
  rendered into unit files by `crons.py apply --unit-dir …` the way
  `cadences` are rendered into a crontab. Absent `services:` means no units,
  a byte-for-byte no-op on the unit directory. Not in `required` and not in
  `types`: the live node predates it and must stay legal, so this field is
  documented here and parsed defensively by the applier, never enforced
  absent.

## Why a declaration beats an unread schedule

Before this schema, a cadence lived only in the system's own scheduled-job
table — real, working, and invisible to the graph: changing it was an edit
the graph had no node for, no version history of, and no way to review
alongside the rest of a session's reasoning. Moving cadence into a node
subject to the same grid, the same schema validation, and the same review
every other node gets is what G10.2 means by "the rules become modifiable
through the graph" — the loop closing on itself, applied to its own
operational schedule rather than to the code that runs it.

## Spawn rule — parented to the goal that asked for it

`min_parents: 1`, `max_parents: 1`, `allowed_parents: [goal]`. `cron` is not
in `[shape].md :: parentless_types`. A `.geometry` node describes the
graph's own shape, but "describes the graph's own shape" is not the same
claim as "has no lineage" — it has a clear parent: `goal:g10.2` ("The graph
describes its own geometry"), the goal that asks for `nodes/.geometry/`
nodes to exist in the first place. A geometry node is downstream of the
goal that made it necessary, not free-floating alongside `idea` and the two
goal roots, which are parentless because there is genuinely nothing
upstream of them in the content graph. Parenting it here also means it
participates in chain depth and `outcome_coverage` like any other node —
which is what G10.2's own words, "subject to every rule other nodes obey,"
actually require, not merely a `.geometry` label with the parent rule
switched off.

## Deliberately absent

No `THOUGHT` block on the node this schema governs: a first version has no
prior version to differ from, and a fabricated one would read as evidence
that was never there (G2.11). No machine-specific value anywhere in a valid
node of this type — no absolute path, no project name — because this schema
ships with the engine and must not encode one project's layout (G8.2). The
node declares cadence and enablement only; a reader resolves those into
actual commands and paths at run time.

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

- **Absent means empty.** No node is required to carry one. Fill it when there
  is something to say; never fabricate one after the fact.
- **It survives regeneration.** Writers that rebuild a body carry this region
  across verbatim via `write_frontmatter(..., preserve_body=...)`.
- **Versioning is free.** The grid snapshots `node.md` once per version, so
  each grid commit already carries the thought current at that version.
- **Not in frontmatter, deliberately.** `write_frontmatter` flattens newlines,
  so multi-line prose in a frontmatter field is silently destroyed.
- **Readers strip it.** Thought is provenance to zoom into, not weight every
  reader carries forever.
