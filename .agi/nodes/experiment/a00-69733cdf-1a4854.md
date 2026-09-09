---
id: experiment:a00-69733cdf-1a4854
mint_id: faef7fecd9834ecabe53cd5f8db18472
type: experiment
parents:
  - hypothesis:l3w4-seat-sessions-and-tiling
next_edges: []
confidence: 0.6
edited_by: a00-69733cdf
evidence_runs:
  - experiment:a00-69733cdf-1a4854
loop: hypothesis:l3w4-seat-sessions-and-tiling@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b1a25b281393b770
season: 2
title: "Close the three parent-review gaps: tty included, read-back, tile --apply"
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-69733cdf-1a4854

## Experiment

Continuation kid on parent-review gaps of the compute half
(experiment:a00-fc211f82-e6927c, hypothesis:l3w4-seat-sessions-and-tiling). That
sibling proved per-seat launch resolution + the pure no-gap tiler geometry;
this experiment CLOSES the three gaps the parent named, all in
`extensions/agi/bin/rotate.py`:

**Gap 1 — tty seats were wrongly excluded.** `_seats_that_launch` kept only
`session_kind == remote-control`; the claim (and the owner ask "all of the
non-ephemeral roles") excludes ONLY fire-and-forget. Fixed: the filter is now
`session_kind != fire-and-forget` (`EPHEMERAL_KIND = "fire-and-forget"`), so
remote-control AND tty rows both resolve a launch line. The sibling's fixture
that asserted the tty exclusion was corrected to assert the tty INCLUSION, so
the red-first test now proves claim test 1 rather than contradicting it. On the
live registry this raises coverage from 5 to 8 seats (belam + 3 advisors +
liaison + dir-g1/dir-g15/dir-g16).

**Gap 2 — no post-launch read-back.** `cmd_seats_launch` trusted spawn rc
alone. Now, on a real (non-dry) run, it re-lists the tmux session
(`_existing_windows`) and confirms every launched seat is a live window;
any launch that reported ok but produced no window fails the read-back with
rc 1 — the trap-0c bug class (L3.32/33) made explicit, no real seat required
(it is exercised with `--window-path` fakes).

**Gap 3 — tiler was geometry-only.** `tile` now has an `--apply` path that
reads the LIVE window set (`_live_window_names`, intersection of the tmux
session with the non-ephemeral seat registry), computes the no-gap partition
over W/H, and hands each rect to a WM on X :1 — `_screen_tool()` probes for
wmctrl then xdotool; `_place_windows` resolves the tool-specific argv and
issues it, logging-and-skipping any single failure. No tool on PATH degrades
gracefully: geometry printed, exit 0, "X :1 not reached". `--names` overrides
the live set; `--window-path`/`--tmux-session` support tests.

Commands run (all dry/no-WM — per the brief's standing prohibition NO real
seat was started):
- `rotate.py seats-launch --dry-run` → resolves exactly 8 non-ephemeral
  launch lines (5 remote-control + 3 tty) with each row's model/effort and
the `export CLAUDE_CODE_WORKFLOWS=1` gate.
- `rotate.py tile --apply --names belam,liaison --width 100 --height 100` →
  graceful degradation (no wmctrl/xdotool on the box), two no-gap rects.
- `pytest extensions/agi/tests/ -q` → 2109 passed, 1 skipped (63 rotate.py
  pass; the 2 failures are in test_send.py from an in-flight send.py edit in
  this shared tree, not this experiment's code).

## Evidence

Red-first: each new/edited test fails against the pre-change behaviour (tty
excluded, no read-back, tile had no --apply) and passes after.

- `test_seats_launch_resolves_one_per_remote_seat` now asserts
  `["belam", "adv-alive", "tty-one"]` (tty INCLUDED) with each row's own
  model/effort/tier.
- `test_seats_launch_read_back_confirms_all_windows`: with all windows listed
  rc 0; with one launched-but-missing rc 1 (read-back catches it).
- `test_tile_apply_places_live_windows_via_wmctrl`: one wmctrl `-e` resize
  per live window; rects sum to the full 100x100 screen, no overlap.
- `test_tile_apply_degrades_gracefully_without_wm`: `_place_windows(...,None)`
  issues 0 commands; `--apply` still rc 0 with geometry printed.

Live dry-run (real registry):
```
remote-control belam / adv-self-perpetuating / adv-all-is-one / adv-alive /
liaison / dir-g1 / dir-g15 / dir-g16
```
(8 non-ephemeral rows; fire-and-forget rows, had any, would be skipped.)

## Agent Notes
Closed all 3 parent-review gaps in rotate.py: tty seats now included (8 non-ephemeral rows resolve, only fire-and-forget excluded), post-launch read-back confirms every launched window exists else rc1, and tile --apply wires the tiler to live X :1 windows via wmctrl/xdotool with graceful degradation. 4 new/edited red-first tests green; 63 rotate tests pass. Live X :1 placement still unproved (real seats forbidden).
