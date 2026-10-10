---
id: outcome:a00-c8365a0c-85a6d1
mint_id: 00f77f2908ec406c8ee3119f3c9fd8d3
type: outcome
parents:
  - mvp:unified-spawn-path
accepted_bytes_total: 0
confidence: 0.7
cost_usd_total: 0
edited_by: season.py
evidence_runs: 0
judged_against: goal:g4.6
lens: goal:g4
season: 1
status: open
telemetry_nodes_skipped: 92
telemetry_nodes_summed: 0
thought_session: season
title: A00 c8365a0c 85a6d1
tokens_in_total: 0
tokens_out_total: 0
verdict: inconclusive_lean_proved:70
wired_at: 1788237714
wired_from: a00-c8365a0c
---
# outcome:a00-c8365a0c-85a6d1

## Outcome

Baseline audit of `mvp:unified-spawn-path` against the live tree, recorded so
the subsequent build/experiment nodes have a measured "before" rather than a
remembered one. **The MVP is unimplemented today** — every claim below was
verified by direct inspection on 2026-09-01.

Input shape (what enters):
- `nodes/mvp/unified-spawn-path.md` — the design (seam, config, adapter
  interface, graph-event completion, falsifier).
- The live tree: `extensions/agi/bin/dispatch.py`, `heal.py`, `config.json`.

Output shape (what exits):
- A verdict per falsifier clause: unmet (0/4), with the exact code locations
  that will have to move.
- A go signal for the build step: the design is internally consistent and
  buildable as written; nothing found in the tree contradicts it.

Behavior (what it does):
- **Falsifier 1 (third harness, no `dispatch.py` edit): UNMET.** No
  `bin/adapters/` directory exists; `grep harnesses dispatch.py` → zero hits;
  command construction is inline: `_build_pi_args` (dispatch.py:627),
  `pi_model_args` (:106), env scrub imported as `_scrubbed_env` (:80, used
  :250).
- **Falsifier 2 (zero harness-keyed branches on shared path): UNMET.** pi is
  hardwired; there is no adapter lookup to branch outside of.
- **Falsifier 3 (moved pi tests pass unchanged): UNMET, but tests exist** and
  the functions to move are identified, which is the precondition.
- **Falsifier 4 (node-write = completion): UNMET.** `heal.py` still polls
  pid/agent.json (:112-113), exactly the process-inspection model the design
  retires; the 2026-08-31 drop-bug path (agent.json → heal → manifest →
  post_wire) is intact.
- Config check: `cc_dispatch` present in config; `harnesses` absent — so the
  legacy-synthesis clause (`harnesses.pi` from `agent_dispatch`) is exercised
  by the default repo from day one, not by an exotic project. Good.

Edge cases:
- The design's own admitted weak joint stands: "acquired real content" is a
  placeholder-body comparison; a scaffold-template change or a kid writing
  scaffold-matching text breaks it. Not resolvable at this layer.
- `claude_code_adapter.py` stub does not exist yet either — nothing in config
  references it, so no broken resolution, but the build step should land the
  stub in the same pass as `pi_adapter.py`.

## i/o doc

```
inputs: mvp:unified-spawn-path design; live dispatch.py/heal.py/config.json
outputs: falsifier baseline 0/4 unmet (design-consistent, buildable); go for build
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
An outcome node on an unimplemented MVP reads as odd until you notice the MVP
is a design node: its deliverable is a falsifiable spec, and the falsifiers are
only meaningful once baseline state is recorded. This node is that baseline —
measured, file-and-line, so the build step cannot quietly claim "the seam was
already half there". All four clauses unmet was the expected result; the useful
findings are that legacy synthesis is the mainline case (not an edge), and
that the pi functions to move are cleanly locatable, so the build node can
quote line numbers rather than rediscover them.
<!-- THOUGHT:END -->

## Agent Notes
Baseline audit: all 4 falsifiers unmet (no adapters/, pi hardwired in dispatch.py, heal.py polls pid); design consistent and buildable as written.