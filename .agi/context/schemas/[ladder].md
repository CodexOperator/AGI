---
name: ladder
structural: true
derived_from: authored-2026-09-06 for G12.3 — no prior corpus to survey; this
  schema and its one node are minted together
fields:
  tiers: {type: list}              # four dicts: tier (int), plan_types (list), report_type (str|None), judged_against (str), lens (str), cadence (str)
  current_season: {type: int}      # the active season number
  caps: {type: dict}               # type -> max count, e.g. {moral: 5, vision: 3}
  caps_apply_from_season: {type: int}  # season from which caps are enforced
  budget_usd_week: {type: int}     # weekly budget in USD
  spawn_profiles: {type: list}     # spawn profile names: [fast, cheap, good, balanced]
  read_order: {type: dict}         # role -> list of reading items
  director_rotate_at: {type: float}  # fraction of context at which director rotates
  zoom: {type: str}                # zoom level scheme, e.g. "numeric"
  roles: {type: list}              # one row per (tier, role): harness, model, effort, settings
  season_names: {type: dict}       # season number -> name, written at rollover looking back
  mantles: {type: dict}            # role -> mantle name (e.g. prime_director: Belam)
validation:
  required: [id, type, mint_id, tiers, current_season, caps, director_rotate_at, roles]
  types:
    current_season: int
    caps_apply_from_season: int
    budget_usd_week: int
    director_rotate_at: float
    tiers: list
    caps: dict
    spawn_profiles: list
    read_order: dict
    zoom: str
    roles: list
    season_names: dict
    mantles: dict
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 1
---

# ladder

**Structural node type — the tier ladder declared as graph content (G12.3,
`.geometry`).** Declares tiers 0 through 3 each with plan types, report type,
judged-against, lens and cadence; current season; caps (5 morals, 3 visions);
weekly budget; spawn profiles; reading order by role; director rotation
threshold. One ladder node lives at `.agi/nodes/.geometry/ladder.md`.

## What reads this

`season.py` (G12.3) reads `current_season`, `tiers`, and `caps` to stamp
season on every freshly-minted node, validate judgment records, and enforce
caps from `caps_apply_from_season` onward. The portal and zoom readers read
`read_order` to present tier-appropriate context to each role. The dispatcher
reads `spawn_profiles` and `budget_usd_week` to select models for each spawn
against the budget.

## Field meanings

- `tiers` — an array of exactly four dicts (tiers 0..3), each with:
  - `tier` (int): the numeric level, 0–3.
  - `plan_types` (list of str): which node types serve as the plan at this
    tier (e.g. `["subgoal", "short-term goal"]` at tier 0).
  - `report_type` (str or null): which node type carries the report at this
    tier; `null` for tier 3 (moral has no report — never by machine).
  - `judged_against` (str): what this tier's report is judged against (e.g.
    `its (sub)goal`).
  - `lens` (str): what lens judges this tier (e.g. `the long-term goal above`).
  - `cadence` (str): how often this tier closes (e.g. `the loop (weekly)`).
- `current_season` — the active season number. All newly-minted nodes are
  stamped with this value.
- `caps` — a dict mapping node type name to the maximum count allowed. Applied
  from `caps_apply_from_season` onward.
- `caps_apply_from_season` — the season at which caps start being enforced.
  Season 1 is grandfathering season: all existing nodes get `season: 1` and
  are exempt from caps.
- `budget_usd_week` — the weekly OpenRouter budget, in USD.
- `spawn_profiles` — the named model-selection profiles available for spawning
  agents, typically the engineer's triangle: `fast`, `cheap`, `good`,
  `balanced`.
- `read_order` — a dict keyed by role (`kid`, `parent`, `director`,
  `prime_director`), each value listing the items to read in order at session
  start. Defined in section 4.5 of the design brief.
- `director_rotate_at` — fraction of context used at which a director writes
  its handoff and rotates. Starting value: 0.35.
- `zoom` — the zoom-level naming scheme the graph uses. `numeric` keeps it
  algorithmic and unbounded.
- `roles` — the command-ladder roles table: one row per `(tier, role)` mapping
  to `harness`, `model`, `effort`, `settings` (the tier-selection command
  ladder brief, §2.1). `dispatch.py` resolves a spawn by looking up its row
  here, falling back to `harnesses.*.models` in config when the table has no
  row. `settings: ultracode` tells the claude-code adapter to append
  `--settings {"ultracode": true}`; `settings: ""` (or a missing field)
  emits nothing. Every role the graph knows (`kid`, `parent`, `director`,
  `prime_director`) is resolvable through this table.
- `season_names` — season number to one-line name, written at **rollover
  looking back** by the prime. Season 1 is `genesis`.
- `mantles` — role to mantle name, declared on the ladder and derived into
  the role's head by `brief.py`; never hardcoded there. `prime_director:
  Belam` carries the owner's mantle text (§1.5 of the command ladder brief).
  The legacy flat `mantles_prime_director` field is kept on the node as a
alias.

## Why a declaration beats a hardcoded ladder

Before this schema, the tier ladder existed only in prose (the design brief)
and in the director's reasoning — real, specified, and invisible to the graph:
changing a cadence or adding a tier was an edit the graph had no node for and
no version history of. Moving the ladder into a node subject to the same grid,
the same schema validation, and the same review every other node gets is what
G12.3 asks a `.geometry` node to be.

## Spawn rule — parented to the goal that asked for it

`min_parents: 1`, `max_parents: 1`, `allowed_parents: [goal]`. `ladder` is not
in `[shape].md :: parentless_types`. A `.geometry` node describes the graph's
own shape, and has a clear parent: `goal:g12.3` ("The tier ladder, seasons,
and season.py"), the goal that asks for this ladder node to exist. Parenting
it here also means it participates in chain depth and `outcome_coverage` like
any other node.

## Deliberately absent

No `THOUGHT` block on the node this schema governs: a first version has no
prior version to differ from, and a fabricated one would read as evidence
that was never there (G2.11). No machine-specific value anywhere in a valid
node of this type — no absolute path, no project name — because this schema
ships with the engine and must not encode one project's layout (G8.2). The
node declares only graph-wide structural values; a reader resolves those into
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