---
id: goal:g9
mint_id: 21b70478f4414c09ae658a4caa63d686
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G9
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g9.1
  - goal:g9.2
  - goal:g9.3
  - goal:g9.4
  - goal:g9.5
  - idea:engine-cc-session-start
  - idea:engine-render-context
  - idea:engine-renderers
status: horizon
tags:
  - goal
  - root
thought_session: season
title: "G9: Legibility: a human can see what the loop is doing"
---
**Stated plainly by the owner, and it is the sharpest usability signal this
project has had:** *"You keep referencing these items and I have no idea what
you are talking about."* Every artefact this system produces today is addressed
to an agent. `INJECTION.md` is generated for a spawn prompt. `GOALS.md` and
`TODO.md` are dense on purpose. The ASCII map is capped at 200 lines and
truncates silently. There is no view built for a person.

That is not a documentation gap, it is a **product gap**, and it gates every
other goal: a system whose state only agents can read cannot be evaluated,
corrected, or handed to anyone else. G8 (forkability) is unreachable without it.

**Invariant:** the dashboard is a *reader*, never a writer. It must be safe to
run at any moment, mid-iteration, with zero possibility of touching the corpus.

**Design constraint that shapes the whole thing:** it renders the graph
*truthfully*, including its damage. Truncation, dangling references,
unevidenced verdicts and deprecated mass are the things a human most needs to
see — a dashboard that shows a clean graph over a broken one is worse than none.