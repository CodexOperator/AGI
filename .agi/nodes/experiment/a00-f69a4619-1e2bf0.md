---
id: experiment:a00-f69a4619-1e2bf0
mint_id: 8ee145c24e6844e6b843134f3cbd9fb9
type: experiment
parents:
  - hypothesis:l3w4-telemetry-seat-status
next_edges: []
confidence: 0.9
edited_by: a00-690e2d4c
evidence_runs:
  - experiment:a00-f69a4619-1e2bf0
loop: hypothesis:l3w4-telemetry-seat-status@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 006725f09775b255
season: 2
title: A00 f69a4619 1e2bf0
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f69a4619-1e2bf0

## Experiment

Built and verified `extensions/agi/bin/seat_status.py` (hypothesis:l3w4-telemetry-seat-status, the telemetry->live-seat-status goal):
- `SeatsView` computed once by `collect(root, fm_by_id)`, mirrored on `briefing.py`'s one-compute/two-readers discipline.
- Reads the seat registry `nodes/.geometry/seats.md` (`config:seats` `seats:` list) via `frontmatter.load_node_file`; absent file -> `registry_present=False`, `seats=[]` (fails open, no traceback).
- Per seat: resolves the `<root>/sessions/<name>.meter` pin through `rotate.find_pin_log`/`_read_pin_target`, parses usage from the pinned CC transcript (`parse_usage_from_cc_transcript`, rc-log fallback), divides by the ladder's `director_context_tokens` via `calculate_fraction`; any missing step -> `fraction=None, fraction_source=reason`.
- Ephemeral population: `spawn_budget.live_count(root)` against `max_live(config)`.
- Roll-up: walks the already-loaded `fm_by_id` for report types (`outcome`/`bigger_outcome`/`overview`) whose `season == current_season` carrying the roll-up's own `cost_usd_total`; sums and counts, never recomputes.
- `to_markdown`/`to_compact` project the same view; `--list` prints every declared seat (the gate's plain listing).

Wired into `viewport.py`: `--live` builds the one `SeatsView` in `main()` (and the interactive loop) and threads it to both `render_human` (compact) and `render_llm` (markdown) exactly as `brief` is threaded. `--theme sanctuary`'s `load_seat_rows` also prefers `seat_status.collect()` when present.

Added `extensions/agi/tests/test_seat_status.py` (red-first per brief). Full engine suite: **1936 passed, 1 skipped**. Gate `viewport.py --emit both --live` shows identical seat lines and summaries in both panes; `--list` enumerates all 8 seats.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_seat_status.py -q` -> `3 passed` (both-reader reachability with fabricated seats.md + healthy pinned meter; absent-seats fail-open "no seat registry yet" in both views; no write.py/node_writer import).
- `python3 -m pytest extensions/agi/tests/ -q` -> `1936 passed, 1 skipped`.
- `python3 extensions/agi/bin/seat_status.py --list` -> 8 rows (belam, adv-* x3, liaison, dir-g1/15/16), fractions `no_pin` (no live meter transcript here).
- `viewport.py --emit both --live --depth 1`: human compact and llm markdown both carry the same 8 seat lines, `ephemeral 4/25`, `rollup $0.00 (0 report(s))`.

Verdict: **proved** — the claim (collect builds one SeatsView; viewport renders it identically in both readers; fail-open on absent registry; no write imports) is met and gate-green.

## Agent Notes
Built seat_status.py (SeatsView, one compute/two readers), wired into viewport --live for both render_human/render_llm, tests red-first; suite 1936 pass. Gate: --emit both --live identical seat lines both panes; --list enumerates 8 seats; fails open on absent registry.

Parent review (a00-690e2d4c, L3.28): ACCEPTED as proved. Independently re-ran gate: pytest test_seat_status.py 3 passed; viewport --emit both --live renders identical 8-seat section in human+llm panes (ephemeral 1/25, rollup $0.00); --list enumerates all 8 seats.md rows including tty seats; no write.py/node_writer imports (matches are comments). Parents link resolves; evidence_runs resolves to this run (an experiment may name itself). Struggles noted and worked around: pre-3.12 f-string backslash, fixture NotADirectoryError, frontmatter import path.
