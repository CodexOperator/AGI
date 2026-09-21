---
id: hypothesis:l3w4-telemetry-seat-status
mint_id: 078a5c865c894d4292fc82844c68be63
type: hypothesis
parents:
  - goal:g16
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: e404c595dc37f9e6
season: 2
testable_claim: seat_status.py's collect(root, fm_by_id) reads the seat registry (.agi/nodes/.geometry/seats.md), each seat's rotate.py meter-pin fraction, spawn_budget.py's live/cap ephemeral count, and telemetry_rollup.py's existing per-report cost/token sums into one SeatsView computed once, and viewport.py --live renders that same view as an identical new section in both render_human and render_llm, printing "no seat registry yet" with no traceback when seats.md does not yet exist.
thought_session: L3.23
title: Render live seat status
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-telemetry-seat-status

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

New `extensions/agi/bin/seat_status.py`, shaped like `briefing.py`: `collect(root, fm_by_id) -> SeatsView` reads the seat registry, each seat's meter pin, the ephemeral spawn population, and `telemetry_rollup.py`'s existing sums on this season's report nodes, into one object computed once. `viewport.py --live` renders it as a new section in both `render_human` and `render_llm` from that single call.

## WHY

Owner (3), last two sentences: "the telemetry long-term goal should lead to build nodes that literally show live stats including seat status in the graph. So graph literally has everything." `goal:g16` already commits to a per-node/session roll-up; seat status is what the 2026-09-07 text adds to it.

## FILES

- `.agi/nodes/goal/g16.md` :: parent
- `.agi/nodes/.geometry/ladder.md` :: `director_context_tokens`, `current_season`, `roles` (row-list precedent)
- `.agi/nodes/.geometry/seats.md` :: seat rows — NEW (`l3w4-seat-registry`), read here only
- `extensions/agi/bin/briefing.py` :: `Briefing` L87, `build` L205, `to_markdown` L284, `to_compact` L341 — pattern mirrored
- `extensions/agi/bin/viewport.py` :: `render_human` L270, `render_llm` L297, `main` L475 — NEW `seats=` param
- `extensions/agi/bin/spawn_budget.py` :: `live_count` L226, `max_live` L56
- `extensions/agi/bin/rotate.py` :: `parse_usage_from_cc_transcript` L294, `calculate_fraction` L345, `load_ladder_field` L164
- `extensions/agi/bin/telemetry_rollup.py` :: `SUMMARY_FIELDS` L46
- `extensions/agi/src/graph_core/persistence/frontmatter.py` :: `load_node_file` L49
- `extensions/agi/bin/seat_status.py` — NEW
- `extensions/agi/tests/test_seat_status.py` — NEW

## DESIGN

`SeatsView`: `registry_present: bool`, `seats: list[dict]` (`name, role, session_kind, rotated_by, fraction: float|None, fraction_source: str`), `ephemeral_live/cap: int`, `rollup_reports_measured: int`, `rollup_cost_usd_total: float`. `collect()` loads `root/"nodes"/".geometry"/"seats.md"` via `frontmatter.load_node_file(...).frontmatter.get("seats", [])`; absent file sets `registry_present=False`, `seats=[]`. Per row, pin `root/"sessions"/f"{name}.meter"` resolves through `parse_usage_from_cc_transcript` then `calculate_fraction` against `load_ladder_field(root, "director_context_tokens", ...)`, else `fraction=None`. Ephemeral count: `spawn_budget.live_count(root)` against `max_live(config.json)`. Rollup: walk the already-loaded `fm_by_id` for report types whose `season` equals `current_season` and which carry `cost_usd_total`; sum and count, never recompute. `to_compact`/`to_markdown(view)` add one line per seat plus the two summaries. `viewport.py main()`: `seats = seat_status.collect(root, fm_by_id) if args.live else None`, threaded to both formatters like `brief`.

## TESTS (red-first)

One: `test_seat_status_reaches_both_readers_or_fails_open` — a fabricated `seats.md` (two rows) plus a fake pin feeds `collect()`; asserts both seat names and the summary lines appear in both `render_human` and `render_llm` from one `SeatsView`. Second case, no `seats.md`: asserts `registry_present is False` and both views print "no seat registry yet", no traceback.

## GATE

`viewport.py --emit both --live` shows identical seat lines in both panes, and "no seat registry yet" in both when `seats.md` is absent; `commands.py run tests` green; `seat_status.py` imports neither `write.py` nor `node_writer`.

## NOT IN SCOPE

The registry file and schema, `rotate.py meter --seat` (`l3w4-seat-registry`); tmux transport and the nudge (`l3w4-seat-transport`); `rotate.py`'s `--seats` status listing and rotation-loop mechanics (`l3w4-seat-rotation-loops`); whether a perpetual/tty seat ever holds a `spawn_budget` lease, unresolved by the registry brief — `ephemeral_live/cap` counts today's fire-and-forget leases only; cost-per-seat math beyond `telemetry_rollup.py`'s existing sums.

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 … perpetual seats" — owner verbatim (3), last two sentences. `goal:g16` for the pre-existing telemetry commitment.

ADDENDUM (Belam IV, L3.23 review, 2026-09-07 15:05 UTC): the seat-registry kid built config:seats, dispatch.py --seat and rotate.py meter --seat but left the brief's fifth test unbuilt — nothing enumerates every seats.md row at once (dispatch.py --list-rows prints the 7-row ladder table, not the 8 seat rows). This brief owns that surface: the seat-status render lists every declared seat with its live state, and a plain listing (seat_status.py list, or --list-rows growing a seats section) is part of the gate.
