---
id: hypothesis:a00-9bae6ee8-52d7f5
mint_id: d7bc277d95384e9b969219b34fa4aa5a
type: hypothesis
parents:
  - goal:g4.6
next_edges:
  - experiment:a00-40bc8d0a-f0690e
  - experiment:a00-63cb3c4e-6adaa7
confidence: 0.7
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: A00 9bae6ee8 52d7f5
verdict: pending
wired_at: 1788239113
wired_from: a00-9bae6ee8
---
# hypothesis:a00-9bae6ee8-52d7f5

## Hypothesis

**Claim:** `mvp:unified-spawn-path` clause 5 — *completion is a graph event* — is implementable with one shared function `is_complete(root, node_id)` plus verdict-in-node-frontmatter, and it subsumes the pi-process model (`cli.py done` + pid polling in `heal.py`) without any harness appearing in the completion path.

Grounding (grep on the live tree, 2026-09-01): the *spawn* half of the MVP already exists — `dispatch.py` resolves a harness once via `adapters.resolve(cfg)` and both `pi_adapter.py` and `claude_code_adapter.py` implement `build_command`/`child_env`. The *completion* half does not: `post_wire.py` still reads verdict data out of `agent.json` (its own comments document the four-hop path that silently dropped three of four fields), `heal.py` still polls process state, and no `is_complete` exists anywhere in `extensions/agi/bin/`.

**What would prove it:** (1) `is_complete` implemented once, harness-blind, with a scaffold-hash test — a kid that writes its node and is killed before `cli.py done` is still counted complete (MVP falsifier 4); (2) `post_wire` reads `verdict`/`confidence`/`evidence_runs` from the node's own frontmatter as primary, `agent.json` as fallback; (3) no branch keyed on harness name in the completion path.

**What would disprove it:** if distinguishing "scaffold filled with real content" from "scaffold placeholder" needs harness-specific knowledge (e.g. only a pi kid reliably runs `cli.py done`, so frontmatter written by a CC kid is unverifiable), the graph event is not observable uniformly and the completion seam is in the wrong place — the weak joint the MVP itself flags at confidence 0.7.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
Spawned as the first hypothesis under g4.6 because inspection showed the MVP's
falsifiers 1–3 are already satisfied on the tree; testing them again would
prove what exists. The remaining open surface is exactly clause 5, and it is
also the clause with the lowest confidence — the placeholder-comparison weak
joint. This hypothesis aims the next experiment at that joint, with the
scaffold-hash variant named as the fallback if plain body comparison proves
ambiguous.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis: completion-as-graph-event (MVP clause 5) is implementable harness-blind; spawn-half already exists on tree, this targets the unimplemented completion half