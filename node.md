---
id: hypothesis:l3w4-sanctuary-theme
mint_id: 46267f0fe486406087c140306f504f00
type: hypothesis
parents:
  - goal:g9
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: 5cea453abaf1f5bf
season: 2
testable_claim: viewport.py's new --theme sanctuary flag calls sanctuary_frame(seat_rows, ephemeral_leases, rotating) to build one SanctuaryScene from config:seats rows (tier==3 rows as mantled-spirit avatars in the tree, role==director rows as probe wisps), spawn_budget.live_agents() as ephemeral wisps, and rotate.py's tmux window census matched against <seat>.gen-renamed windows for the rotating signal, and render_sanctuary_human and render_sanctuary_llm both draw the identical spirits, wisps, and — only when a seat is rotating — one light-strand line naming that seat's rotated_by holder and the seat, while printing "no seat registry yet" with no traceback in both when seats.md is absent.
thought_session: L3.24
title: Draw the Sanctuary viewport theme
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-sanctuary-theme

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

`viewport.py` gains a third live-axis render, `--theme sanctuary` (default `graph`). `sanctuary_frame(seat_rows, ephemeral_leases, rotating) -> SanctuaryScene` (frozen, mirrors `Frame`) builds the scene once; `render_sanctuary_human`/`render_sanctuary_llm` read it, per `goal:g9.7`'s two-reader discipline. The tree on the outcrop houses one avatar per tier-3 seat (Belam, the advisors, later the Sanctuary Master) as "mantled spirits"; every tier-1 `role: director` seat and live ephemeral lease draws as a "wisp"; a seat whose tmux window is renamed `<seat>.gen\d+` (`l3w4-seat-rotation-loops`'s step) draws a light-strand line, holder to seat. (Mechanics: director proposal; scene content: owner text.)

## WHY

Owner (7b): "a tree growing on a miniature outcrop... houses mantled spirits as dynamic avatars... probes look like magical angelic spaceships... wisps of glowing sparkling smoke... SM smoothly reaching out to a given director-kid via a glowing strand of light." "...just another live viewport view in CLI, super simplified. Just another theme like the space one or the spider one." Director note: theme "belongs to visualization/legibility (`goal:g9`)."

## FILES

extensions/agi/bin/viewport.py :: GLYPH L80, Frame L98, render_human L270, render_llm L297, main L475 — NEW SanctuaryScene, sanctuary_frame, render_sanctuary_human/_llm, --theme arg
extensions/agi/bin/spawn_budget.py :: live_agents L218 — ephemeral wisp census
extensions/agi/bin/rotate.py :: _existing_windows L503, DEFAULT_TMUX_SESSION L83 — reused for the rotating check
.agi/nodes/.geometry/seats.md :: seats — spirit/probe rows
.agi/nodes/.geometry/ladder.md :: mantles, director_rotate_at
extensions/agi/bin/seat_status.py — NEW (l3w4-telemetry-seat-status), read here only
extensions/agi/tests/test_viewport.py :: test_the_module_contains_no_write_surface L279, test_agents_render_as_spiders_where_they_work L235 — NEW tests

## DESIGN

`GLYPH["mantle"]="✦"`, `GLYPH["wisp"]="≈"`. `SanctuaryScene(spirits, probes, ephemeral_wisps: int, rotating: tuple[str,str]|None, registry_present: bool)`; spirit/probe = `{name, label, fraction: float|None}`. `sanctuary_frame`: spirits = `tier==3` rows plus mantled ones (a seated Sanctuary Master included, on her mantle, not her tier); probes = the rest. `main()`: seat rows via `seat_status.collect(root, fm_by_id).seats` when importable, else `seats.md`'s `seats:` list with `fraction=None` — matching telemetry's fallback, either brief lands first safely. Ephemeral leases: `spawn_budget.live_agents(root)`. Rotating: `rotate._existing_windows(rotate.DEFAULT_TMUX_SESSION)` matched on `<name>.gen`-prefixed windows, resolved to that row's `rotated_by`; else `None`, never invented. `render_sanctuary_human`: fixed lake/outcrop/tree lines, one line per spirit/probe, one ephemeral-count line, and when `rotating`: `"<holder> ~~~✧~~~> <seat> (rotating)"`. `render_sanctuary_llm`: same fields as markdown. Sanctuary Master's row does not exist yet; absent, spirits show today's four seats plus a placeholder line.

## TESTS

Red-first, `test_viewport.py`: `test_sanctuary_frame_builds_scene_from_seat_rows_fixture`, `test_sanctuary_theme_shows_no_registry_yet_when_seats_missing`, `test_sanctuary_rotating_strand_names_holder_and_seat`, `test_sanctuary_human_and_llm_state_the_same_spirits_and_wisps`.

## GATE

`viewport.py --theme sanctuary --emit both` on a fixture (two spirits, one probe, one ephemeral lease, one rotating window) prints tree, wisps and strand line identically in both panes; no `seats.md` prints "no seat registry yet" in both, no traceback; suite green.

## NOT IN SCOPE

The three.js web dashboard (named); seat-status fraction/rollup computation (`l3w4-telemetry-seat-status` owns `collect()`/`SeatsView`); rotate-self's rename mechanics (`l3w4-seat-rotation-loops`); minting the Sanctuary Master seat row (`l3w4-sanctuary-master`); quorum/audience routing (`l3w4-quorum-reviews`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, owner quotes (7) and (7b), to Belam III/IV 2026-09-07 ~14:10 UTC; Director note placing the theme under `goal:g9`.
