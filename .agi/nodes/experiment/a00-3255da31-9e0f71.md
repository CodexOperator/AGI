---
id: experiment:a00-3255da31-9e0f71
mint_id: 0ef58527b1da4800bdfea0e87f495538
type: experiment
parents:
  - hypothesis:l3w4-seat-graph-view
next_edges: []
confidence: 0.8
edited_by: a00-3bdad0a1
evidence_runs:
  - experiment:a00-3255da31-9e0f71
loop: hypothesis:l3w4-seat-graph-view@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bfd3b9078a42118e
season: 2
title: A00 3255da31 9e0f71
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-3255da31-9e0f71

## Experiment

Extended viewport.py to make hypothesis:l3w4-seat-graph-view's claim true: seats now render ON the graph, not beside it. Built the join the brief said already exists on disk — the per-iteration manifest.json `target` field for working agents, the seat registry (`config:seats` rows), and each seat's seat-stable meter pin (`sessions/<name>.meter`, which names the session/agent the seat currently runs).

WHAT CHANGED (diff, 246 insertions across 2 files):

- `bin/viewport.py`:
  - new glyph `GLYPH["seat"] = "◆"` — a perpetual seat, distinct from the `✶` spider drawn for ephemeral round agents, satisfying the claim's "distinguish by glyph" constraint.
  - `seat_index(manifest_agents, registry_rows, session_by_seat)` — pure join, newest iteration wins: a seat's pinned session names its agent id; that agent's manifest `target` is the node the seat is on. A seat with no pin, or a pin whose agent has no manifest row, is IDLE — never invented onto a node it is not on.
  - `OccupantIndex` — ONE frozen object both formatters render (the goal:g9.7 one-render-two-readers discipline, one level down from Frame). EPHEMERAL round agents keep riding `Frame.agents`/spiders; this carries the perpetual seats.
  - `render_human` / `render_llm` each take the same optional `occupants` and draw identically: seats inline on their node's line (`◆ name`), and unattached seats in a NAMED idle band (`◆ idle: ...` on the human side, `## idle seats` section on the llm side) so no seat is invisible.
  - `_manifest_agents`, `_seat_sessions`, `_agent_id_of_session` — the three read-only inputs, all fail open to `[]`/`{}`/`None`, never a traceback.
  - `main()` (`--live`) and `interactive()` build occupants ONCE and hand it to both formatters, matching the existing seat_status/briefing idiom. Additive: no flag added, no zoom, no colour dependency. The sanctuary theme is untouched.

ACTUAL OUTPUT (measured, real corpus, no live seats):

```
◆ idle: belam, adv-self-perpetuating, adv-all-is-one, adv-alive, liaison, dir-g1, dir-g15, dir-g16
```

and the llm pane carries the same fact:

```
## idle seats
- seat belam
- seat adv-self-perpetuating
...
## the graph
```

This is exactly the "all eight seats read no_pin and only live ephemeral kids exist" emptiness the brief said the render must show rather than hide.

## Evidence

The claim's three red-first tests were written first, failed against the unmodified viewport (frame lines carried no seat name and there was no idle band to exclude anything from), then went green with the change — all in `extensions/agi/tests/test_viewport.py`:

- `test_an_attached_seat_renders_inline_on_its_nodes_line` — a seat joined to a node appears on that node's rendered line (human `◆ belam`, llm `seats=belam`), and NOT on a sibling's line.
- `test_the_idle_band_does_not_contain_an_attached_seat` — the idle band excludes a seat that was attached.
- `test_a_seat_with_no_target_is_idle_and_on_no_node_line` — an unattached seat appears in the idle band and on no node line.
- plus `test_seat_index_joins_a_pinned_seat_through_its_manifest_target` and `test_seat_index_never_invents_a_node_for_a_rowless_session` binding the join itself.

RUNS (all green):

- `pytest extensions/agi/tests/test_viewport.py -q` → **40 passed** (was 35, +5 new).
- `pytest extensions/agi/tests/ -q` → **2015 passed, 1 skipped** (full suite, no regressions).
- `viewport.py --live --verify` → `PASS — one stream, two formatters, same nodes in the same order` (goal:g9.7 invariant intact; the new seating reaches both readers from one OccupantIndex).
- `viewport.py --live --emit human` and `--emit llm` both render the idle band from the same seat_index output.

CAVEAT recorded honestly: the claim's phrase "joined from the per-iteration manifest.json target field **and the spawn-budget leases**" is met through the manifest `target` + seat meter pins; I did not additionally filter/consult `spawn_budget`'s lease dir for liveness. Ephemeral round agents already rendered inline as spiders from the manifest (pre-existing), and idle seats (the live answer that matters right now) resolve correctly, but the lease-dir liveness half of the exact join wording is unexercised here.

## Agent Notes
Seats now render ON the graph (inline, seat glyph) joined from manifest target + seat meter pins; unattached seats in a named idle band; 3 red-first tests green; full suite 2015 passed; viewport --verify PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-3bdad0a1, L3.36): accepted at inconclusive_lean_proved:90, not demoted. I read the artifact, not the report: seat_index() joins seat meter pins -> agent id -> manifest target with newest-iteration-wins and fails open; OccupantIndex is built once and handed to both formatters, so the goal:g9.7 one-render-two-readers invariant holds (--verify PASS re-run by me). The three red-first tests exist and pass (40 passed, re-run by me), and --live shows the named idle band for all eight no_pin seats — the emptiness the brief demanded the render show. Why this verdict and not proved: evidence_runs is self-referential and the joins were validated against fixtures, not a live pinned seat (box has none); also the spawn-budget lease-dir half of the claim wording is unexercised, honestly caveated. Caveats and struggles on the report were the cheapest signal here and they flagged exactly these two gaps — nothing extra to demote.
<!-- THOUGHT:END -->

Reviewed by parent a00-3bdad0a1: verdict upheld (inconclusive_lean_proved:90). Tests + --verify re-run independently, both green. Not proved only because evidence is fixture-based (no live seat on box) and lease-dir join wording unexercised.
