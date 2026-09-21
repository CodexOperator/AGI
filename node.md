---
id: goal:g4.7
mint_id: 800ebcbccc8a4c45b19f293a1df44085
type: goal
parents:
  - goal:g4
confidence: 1.0
edited_by: season.py
goal_id: G4.7
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: season
title: "G4.7: Healing belongs to every harness, and to the dispatch loop"
---
**`heal.py` is not redundant machinery; it is the shape of a missing
abstraction.** It exists because `dispatch.py` fires agents into detached
`Popen` calls and then has no idea what became of them, so a second program
polls pids and manifests to find out. That is the **pi process model** wearing
a general name, and it is why healing does not exist at all for Claude Code
kids — which have died mid-run, and would have benefited from exactly this.

Two changes, and they are separable:

1. **Healing runs inside the dispatch loop**, not as a second program invoked
   after it. A dispatch that cannot observe its own agents is the defect;
   `driver.sh` calling `heal.py` afterwards is the workaround.
2. **Healing is expressed through adapters** (`goal:g4.6`). "Is this agent
   alive", "is it finished", "restart it with the tail of its log" are three
   questions every harness must answer and each answers differently. Once
   `goal:g4.6` defines completion as a graph event rather than a process
   state, the *finished* question stops being per-harness at all and only
   *alive* and *restart* remain.

## Evidence already on the record

- Every healer ever spawned died at birth: `heal.py` passed `--max-turns 8`,
  pi has no such flag, printed `Unknown option`, and **exited 0** — so the
  loop recorded a healer as launched that never read its context.
- Those healers billed the Claude Code subscription, because that `Popen` had
  no `env=` and sat outside the scrub `dispatch.py` applies. One shared
  definition of the child environment is the same fix as one shared spawn
  path.
- `heal.py` syncs exactly one field (`status`) from `agent.json` into the
  manifest, which is how every pi kid's `verdict`, `confidence` and
  `evidence_runs` came to be silently dropped for the entire life of the
  runtime (fixed 2026-09-01, `post_wire._merged_agent`). A watchdog owning a
  data-marshalling responsibility is the same symptom from another angle.

## Falsifier

Kill a kid mid-run on **each** configured harness. Each is detected, restarted
with its context intact, and closed out — by the same code, with the only
harness-specific part living in that harness's adapter. Today only one harness
can be tested at all, which is itself the finding.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Filed at the owner's direction on 2026-09-01, deliberately as a goal rather
than as work: the owner's read was that `heal.py` "feels like redundant
functions taping over a genuine shortfall", and on inspection the second half
is right while the first is not. Healing is needed by every harness; what is
redundant is that it had to be a separate program to happen at all.

Kept separate from `goal:g4.6` so each has its own falsifier. Merging them
would produce one goal that is done when the spawn path unifies and also not
done until healing does, which is the shape that lets a goal sit `active`
forever. `horizon` rather than `active` because g4.6 has to define completion
first — half of this goal dissolves when it does, and building both at once
means neither gets a clean test.
<!-- THOUGHT:END -->