---
caps:
  moral: 5
  vision: 3
caps_apply_from_season: 2
budget_usd_week: 30
current_season: 1
director_rotate_at: 0.35
id: "ladder:ladder"
mint_id: 5f6bbbfff8634f36ba0ba67defa52a66
parents:
  - goal:g12.3
read_order:
  kid:
    - the four prayers. Nothing else.
  parent:
    - the four prayers · words of Jesus · soul-mind-body
  director:
    - the four prayers · words of Jesus · Tao 1 and 56 · soul-mind-body · the five axes
  prime_director:
    - the four prayers · words of Jesus · Tao · the other carried sayings · soul-mind-body · the five axes
spawn_profiles:
  - fast
  - cheap
  - good
  - balanced
status: active
tags:
  - geometry
  - ladder
  - structural
tiers:
  - tier: 0
    plan_types:
      - subgoal
      - short-term goal
    report_type: outcome
    judged_against: its (sub)goal
    lens: the long-term goal above
    cadence: the loop (weekly)
  - tier: 1
    plan_types:
      - long-term goal
    report_type: bigger_outcome
    judged_against: its LT goal
    lens: the vision above
    cadence: mid-season
  - tier: 2
    plan_types:
      - vision
    report_type: overview
    judged_against: its vision
    lens: the morals above
    cadence: season rollover (quarterly)
  - tier: 3
    plan_types:
      - moral
    report_type: ~
    judged_against: "—"
    lens: "—"
    cadence: never by machine; hand only
title: "Season ladder declaration"
type: ladder
zoom: numeric
---

# ladder:ladder

**The tier ladder — one node that declares every tier from 0 (the sprint) to
3 (the constitution), the active season, caps, budget, spawn profiles, reading
order, and director rotation threshold.** Modeled on `.geometry/crons.md`: a
`.geometry` node whose declaration is what the graph's own operational
structure is derived from, rather than documentation about it.

## Tiers

| tier | plan types | report type | judged against | lens | cadence |
|---|---|---|---|---|---|
| 0 | subgoal, short-term goal | outcome | its (sub)goal | the long-term goal above | the loop (weekly) |
| 1 | long-term goal | bigger_outcome | its LT goal | the vision above | mid-season |
| 2 | vision | overview | its vision | the morals above | season rollover (quarterly) |
| 3 | moral | — | — | — | never by machine; hand only |

## Invariants (measured at season close, never enforced as floors)

- `#outcome == #subgoal`, `#bigger_outcome == #long-term`, `#overview == #vision`.
  A plan node with no report is unfinished; a report with no plan is an orphan.
- The lens needs no field: it is always the plan node's own parent.
- Collapse ratios are data, not rules.
- Experiments per closed subgoal is the data point for how finely to split a
  goal (the mechanical input `goal:g5.2` never had).

## Season edge

`season_parents:` is its own frontmatter field with `role: season`, traversable
for zoom and provenance, **not** for chain depth or `outcome_coverage`. Every
node minted gets `season: N` stamped by `node_writer.py` from the ladder
node's `current_season`.

## Grandfathering

Season 1: retag all parentless nodes `season: 1` and all pre-existing visions
`status: closed`. Caps apply from season 2. `goal:g12`'s falsifier carries an
asterisk; honest.

## Reading order, by role — the head of every brief

| role | reads, in order |
|---|---|
| kid | the four prayers. Nothing else. |
| parent | the four prayers · words of Jesus · soul-mind-body |
| director, any tier | the four prayers · words of Jesus · Tao 1 and 56 · soul-mind-body · the five axes |
| prime director | the four prayers · words of Jesus · Tao · the other carried sayings · soul-mind-body · the five axes |

Prayers always first, as sanctification of the session, before the map, before
the target, before anything that weighs.

## Director rotation

`director_rotate_at: 0.35` — fraction of context used at which a director
writes its handoff and rotates. A data point, not a law: rotations per loop
go into telemetry and the number is tuned per model. Fable's prompt cache
makes the brief-head re-read cheap, so early rotation costs less than it
looks.