---
id: hypothesis:a00-94ba34d6-55f548
mint_id: 384bf0331aaf47ad88de220d28f60e17
type: hypothesis
parents:
  - goal:g9.4
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: bef9e00c638c34e5
season: 1
thought_session: season
title: A00 94ba34d6 55f548
verdict: pending
---
# hypothesis:a00-94ba34d6-55f548

## Hypothesis

The existing viewport rendering pipeline (confirmed functional across zoom, time, and unified-stream axes by experiment:a01-bc698083-9c5980) can be extended to show live agents as distinguishable "spiders on the web" by wiring iteration manifest data (agent id, role, working nodes) into the viewport frame renderer at the node-display level, without breaking the unified stream invariant.

### What would prove it
1. `viewport.py --live` renders agents as distinct glyphs (`✶` for kids, `◆` for parents, `◈` for director) positioned on or adjacent to their working nodes in the graph
2. Agent glyphs update when the manifest changes between iterations (visible agent motion across `--live` refreshes)
3. The unified stream invariant still passes (`--emit both --verify`)
4. The zoom axis still passes (depths 1-5 render correctly with agents aggregated at higher levels)

### What would disprove it
1. The iteration manifest lacks working-node assignments needed to place agents on specific nodes — agents can only be positioned at the top of the viewport or not at all
2. Agent glyphs collide with/resemble existing node-type or damage glyphs, making the graph noisier rather than more informative
3. Wiring live data into the renderer requires breaking the single-stream invariant (different frames for human vs LLM views)
4. Refresh/repaint complexity makes the viewport unusable as a "watch it move" tool — agents flicker, lag, or require manual


## Agent Notes
Hypothesis: live agents as spiders on the web by wiring iteration manifest into viewport renderer. Builds on experiment:a01-bc698083-9c5980 which proved the viewport pipeline itself works.