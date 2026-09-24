---
id: goal:g1.25
mint_id: f57eb186c8174050a1a086a14f8919f1
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G1.25
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 23240771a187a1b4
season: 2
seeds:
  - hypothesis:commands-manifest-is-jevs-one-choice-surface
status: active
tags:
  - config-maxxing
  - cli-grammar
  - commands
  - jev
  - magic-pane
  - engine
thought_session: belam-S2-L5-IV
title: "G1.25: CLI GRAMMAR = jev's one choice surface -- every engine verb a typed entry in command:commands, ONE machine-readable manifest, propose-only endpoints; the cli-grammar part of g7.33 claimed under config-maxxing, on the local-maxxing town board (owner 09:5xZ 09-23; assigned director-engine)"
town: local-maxxing
---
# goal:g1.25

# goal:g1.25 — CLI GRAMMAR = jev's ONE choice surface (config-maxxing; claimed out of g7.33 by the owner, 09-23)

```
owner     09:2xZ via thought-master (verbatim on goal:g5): "If needed, tell director-engine to expand the commands.py config to include
          more commands and bundle all the various engine functions as api endpoint calls so Jev has a choice surface to grab on to."
          09:5xZ director-engine pane (verbatim on goal:g5): "Go and claim the g7.33 cli grammar part only as its own subgoal directly
          under an umbrella and assign it to our town bundle here so you can work it first thing. G7.33 is held on the other branch
          anyway so it's no issue at all. And go for more spend and more spawning" / then: "Sorry the cli grammar is under config
          template maxxing no?" / "The town board keeps it unified for the town" / "Across different umbrellas"
home      the G1 CONFIG-MAXXING umbrella (commands.py's own goal is goal:g1.10; related: goal:g1.19 engine surface inventory);
          town:local-maxxing's board lists it for the town across umbrellas
claims    ONLY the cli-grammar deliverable of goal:g7.33 (g7.33.md:57, G14.14.6's maxxing pass: every bin verb, its args, invariants,
          traps) -- g7.33 itself stays core's and held
shape     (owner 2026-09-24 20:3xZ steer, verbatim in doc:l5-owner-decisions) an ACTION REGISTRY = every engine action as a typed entry, the ONE choice set jev reads · commands.py = a lightweight query + parse layer over the registry, never the registry itself · the registry stays compatible with off-the-shelf libraries that turn python scripts into CLI commands dynamically via templates ·
          propose (Python / CLI / localhost endpoint) validates and returns the argv, never executes
serves    goal:g5.24.3 the magic pane: MP.02's suggester and held-out set score against this manifest; the town builds no second grammar
work      director-engine (build lane) · first round: hypothesis:commands-manifest-is-jevs-one-choice-surface
done when the manifest lands with its coverage test (every listed CLI verb declared or excluded by name) · merged up to thought-master ·
          director-thought told "[jev] choice surface ready" with the SHA (the director-engine card's standing rule)
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-24 20:5xZ belam-S2-L5-IV: the owner's 20:3xZ steer, verbatim: 'Steer director-engine to shift the work on commands.py into an action registry instead that uses the commands.py as a lightweight query and parse layer, and also so it can be compatible with other command libraries instead that turn python scripts into cli commands dynamically via templates.' The shape line changes from the commands.py manifest being the choice set to an action registry being it, with commands.py only querying and parsing that registry; the 09-23 owner lines stay as the goal's origin. Nothing else here changes: director-engine re-plans its first round (hypothesis:commands-manifest-is-jevs-one-choice-surface) against the new shape.
<!-- THOUGHT:END -->
