---
id: hypothesis:l3w4-seat-graph-view
mint_id: dc635a96642f4d9d960d8b5e97074c73
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 1827976bb8972753
season: 2
testable_claim: "After the change, viewport.py --live renders every seat and every live ephemeral agent INLINE on the rendered line of the graph node it is currently working on, joined from the per-iteration manifest.json target field and the spawn-budget leases; seats with no current node render in a named idle band so none is invisible; and three red-first tests pass that fail today: given a fixture seat attached to a known node id that node's rendered line contains the seat name, the idle band does NOT contain it, and a seat with no target appears in the idle band and on no node line."
title: Seats render ON the graph, not beside it
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-graph-view

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD IT. Your artefact is a DIFF. The claim above is FALSE today and you are the one who makes it true; a faithful description of the current state with zero changed lines has FAILED this brief. If git diff --stat is empty you are not done. OWNER ASK, 2026-09-07 23:1x UTC, near-verbatim: a simple seat visualization, a more basic CLI graph render in graph form, showing which seat is on which node or subnode in the graph — base-level view, no zoom, nothing fancy, just something to actually visualize. The owner's opening line is the requirement in one sentence: I don't see what's happening now. WHAT EXISTS TODAY, measured before this brief was written so you do not rediscover it. viewport.py --live already prints a seat block and then the graph tree, but THE TWO ARE DISCONNECTED: the seats are a flat list of eight names with roles, the graph is a tree of goals and hypotheses and experiments, and nothing anywhere says which seat is on which node. seat_status.py collect() already returns one SeatsView joined from seats.md, the meter pins, spawn_budget and telemetry_rollup, and viewport renders it identically in the human and llm panes (that parity is a goal:g9.7 invariant — DO NOT BREAK IT, whatever you add must appear in both). What collect() does NOT carry is the one field this brief needs: the node each seat is currently on. THE JOIN YOU NEED ALREADY EXISTS ON DISK. Every .agi/sessions/iter-*/manifest.json row carries a target field naming the node that agent is working, alongside its agent_id, tier and role; the spawn-budget lease dir carries which agents are live right now; the meter pins carry a seat's session. Join seat or agent to target node through those, newest iteration wins, and render the result on the node's own line. DESIGN CONSTRAINTS, deliberately small. Base-level only: no zoom, no new flag if you can avoid one, no three.js, no colour dependency — this must read in a plain terminal over ssh. Distinguish a PERPETUAL seat from an EPHEMERAL round agent by glyph, because they mean different things: a seat persists and a kid is gone in twenty minutes. Show the idle band explicitly rather than omitting idle seats — the single most useful fact this render can show the owner right now is that all eight seats read no_pin and the only live agents are ephemeral round kids, which is to say there are no live directors yet. A visualization that hides emptiness is worse than none. Keep it additive: viewport.py already carries the sanctuary theme from experiment:a00-caa19281-236ed5, so match its idiom rather than inventing a second one.
