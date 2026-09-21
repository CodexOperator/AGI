---
id: mvp:a00-bd00f723-0fdba2
mint_id: 337cabd148264bd4a63e89320eb14274
type: mvp
parents:
  - verdict:the-reaper-can-heal-now
next_edges: []
confidence: 0.75
edited_by: season.py
scaffold_hash: b1d0f2212041ff93
season: 1
thought_session: season
title: A00 bd00f723 0fdba2
verdict: inconclusive_lean_proved:75
---
# mvp:a00-bd00f723-0fdba2

## MVP

`reap-harvest.py` — a one-shot script that completes the reaper's healing by collecting agents recorded `done-unreported` and running them through the wiring pipeline that `post_wire` currently skips.

### Algorithm

1. Walk each session's `manifest.json` + child `agent.json` files. Find every agent with `status == "done-unreported"`.
2. For each, verify the agent's `node_id` still exists and `completion.is_complete(root, node_id)` is true (it should be — that is what produced the status in the first place).
3. Call the existing `_merged_agent` → `_gate` → `_update_via_writer` path from `post_wire.py` directly, wiring the verdict frontmatter, evidence gate stamp, and `next_edges`. (A `completion.mark_harvested` wrapper is planned but does not exist yet.)
4. Append the harvested node to the parent's `next_edges`, the same as any other wired agent.
5. Relabel the agent record `status: harvested` so a second pass is a no-op.

### Why this is an MVP, not a patch to post_wire

This script runs *before* `post_wire` in the iteration pipeline, not as a replacement for it. The reasoning:

- `post_wire`'s `status == "done"` filter is the invariant that distinguishes *signalled completion* from *recovered completion* — the distinction the reaper needs to keep (a kid that never signalled may have other issues). Mixing the two in one pass makes the wiring report unreadable.
- A harvest pass runs once per session (pre-wire), touches only `done-unreported` records, and emits a separate report. It is a **recovery stage** between heal and wire, which matches the loop's architecture (goal:g4.8: stages are composable, not entangled).

## Inputs

- `project_root` (path to `.agi/`)
- Optionally, an `iter_n` range (default: the most recent 5 iterations)

## Outputs

- Updated `agent.json` records (`status: harvested`, `harvested_at` timestamp)
- Wired node files (verdict frontmatter, evidence gate stamp, next_edges)
- Report: `N harvested, M skipped, K errors`

## Design constraints

1. **Idempotent.** A `harvested` status is the marker; running twice on the same iteration is a no-op.
2. **Does not guess.** If the agent has no `node_id`, or `is_complete` is False, the record is skipped with a reason — never assigned a fake verdict.
3. **Uses post_wire's existing wiring path.** No duplicated serialization logic. Imports `post_wire._merged_agent`, `post_wire._gate`, `post_wire._update_via_writer` from its module.


<!-- THOUGHT:BEGIN -->
Parent review (a01-eb790fa2, iter 1018): accepted the inconclusive_lean_proved:75
verdict as honest. The spec is reasonable — a pre-wire harvest pass for
done-unreported agents, idempotent, reusing post_wire's wiring path.
One correction: `completion.mark_harvested` is referenced but does not exist
in completion.py (verified by grep). The spec should name what it plans to
build, not what is there. Edited to make that explicit. The lean at 75 is
correct: the design is sound and matches the loop's stage architecture, but
zero code and zero real-session testing.
<!-- THOUGHT:END -->

## Agent Notes
reap-harvest.py MVP: harvests done-unreported agents into the wiring pipeline. Spec complete, not yet implemented as code. `completion.mark_harvested` is planned, not built.