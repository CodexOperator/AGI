---
id: hypothesis:a01-33956545-9fc0bb
mint_id: d94c18de249340c5bafbd638f4698700
type: hypothesis
parents:
  - goal:g1.10
next_edges: []
confidence: 0.25
edited_by: season.py
scaffold_hash: f23e1c5cc1492ccb
season: 1
testable_claim: Rendering every operator-facing command list **from** `nodes/.geometry/commands.md`, rather than describing commands again, removes the remaining manual copies. Editing the node becomes the only way a command changes anywhere. A change to one declared command propagates to all docs in a single run of the renderer, and the rendered tables match the node byte for byte (modulo formatting) on every smoke pass.
thought_session: season
title: A01 33956545 9fc0bb
verdict: pending
---
# hypothesis:a01-33956545-9fc0bb

## Hypothesis

The commands node exists so the engine's standard moves are declared once, but
`CLAUDE.md`, `QUICKSTART.md`, and `SKILL.md` still restate those moves by hand.
The four prose copies remain the operator-facing source of truth, so drift is
still possible and observed — `HANDOFF.md` keeps re-listing the verification
sequence because nothing else the human sees is guaranteed current.

### Testable claim

Rendering every operator-facing command list **from**
`nodes/.geometry/commands.md`, rather than describing commands again, removes
the remaining manual copies. Editing the node becomes the only way a command
changes anywhere. A change to one declared command propagates to all docs in a
single run of the renderer, and the rendered tables match the node byte for
byte (modulo formatting) on every smoke pass.

### What would prove it

- A renderer exists for each surface (`CLAUDE.md`, `QUICKSTART.md`,
  `SKILL.md`, `HANDOFF.md` §5 template) that consumes `command:commands` and
  emits its table without human edits.
- Changing one command's argv (e.g., insert a flag) by editing only the node
  yields consistent updates in **all** rendered surfaces after running the
  normal `driver.sh --smoke` path — no manual edits required.
- Tests assert every rendered surface matches the node's data (command names,
  workflow grouping, ordering) so drift is caught immediately.
- `INJECTION.md` remains the single source for agents, proving the same data
  drives both human docs and injected context.

### What would disprove it

- Any doc still needs a hand edit after the renderer runs, or a renderer copies
  stale data because it depends on a cached artifact instead of the node.
- Formatting constraints force a doc to omit commands or restate them manually,
  creating a fifth copy and breaking the "one declaration" claim.
- The rendered surfaces contradict the node (wrong ordering, missing command)
  without failing tests, meaning the renderer failed to enforce fidelity.
- The renderer requires absolute paths or shell strings the node forbids,
  meaning the declaration can no longer be cloned safely.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The first experiment under `goal:g1.10` proved declarative commands catch real
bugs but stopped short of deleting the prose copies, so the drift problem is
only halved. This hypothesis states the other half explicitly: derive the docs
or the win is incomplete. Calling out the four surfaces keeps the scope finite,
and proving/ disproving criteria are phrased around observable render results
rather than "tidier docs".
<!-- THOUGHT:END -->


## Agent Notes
Hypothesis: render all operator-facing command tables directly from command:commands so edits propagate automatically