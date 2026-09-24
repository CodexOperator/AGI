---
id: hypothesis:a00-a279d8ff-b2be1f
mint_id: 2a3f020b7ea74e85bed5fa4cbaab014e
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
confidence: 0.95
edited_by: a00-138f4fd5
evidence_runs:
  - experiment:a00-a279d8ff-8c1d02
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 8fc591dbb012df8c
season: 2
testable_claim: Live pi harness resolution selects held_pane, and the production dispatch path bypasses anonymous Popen for that configured holder.
title: Live pi resolution selects the first-spawn held pane
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-a279d8ff-b2be1f

## Hypothesis

The repository's configured `pi` harness will resolve its first-spawn durable
holder from the live `.agi/config.json`, so production `_open_round` selects
`holder.start` before anonymous `Popen`. It is proved when the actual config
resolves `persistent_holder=held_pane`, that module loads, and the production
dispatch test forbids agent `Popen` while observing holder start and the real
returned pane id. It is disproved if live resolution still yields no holder or
the configured dispatch reaches anonymous `Popen`.

## Evidence

Child `experiment:a00-a279d8ff-8c1d02` added the missing live harness cell and
its live-config regression test. The narrow claim is intentionally limited to
production resolution and first-spawn selection; real kill/rejoin identity is
not claimed.

## Agent Notes
Live pi config now resolves held_pane; live resolution plus production dispatch selection tests pass (139 tests).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said the live production pi path must select the durable holder. The machine probe loaded the actual .agi/config.json through adapters.resolve(cfg, pi), printed pi held_pane, and load_holder exposed callable start; the changed dispatch bytes branch on that live cell before anonymous Popen. The near miss would have been only a synthetic test fixture with no production config, but this round carries the actual feature cell. The node is accepted only for its narrow first-spawn selection claim; it does not establish kill -9 rejoin stability.
<!-- THOUGHT:END -->
