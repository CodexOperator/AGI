---
id: hypothesis:attractor-list-must-hide-deprecated-ideas
mint_id: 9fc0f6190db34d3d8d3e72f2873e02b0
type: hypothesis
parents:
  - goal:g9.7
next_edges: []
edited_by: season.py
scaffold_hash: a9c2efd9f194132f
scale: engine
season: 1
testable_claim: briefing.py's attractive-ideas ranking excludes deprecated nodes and their subtrees, exactly as frame_stream(hide_deprecated=True) already does for the map, so the seven deprecated idea:domain-* roots (75/45/44/41/40/39/38 descendants) drop out of INJECTION.md and idea:engine-tests / idea:engine-graph-core head the list; a test with a deprecated idea fixture goes red when the filter is removed
thought_session: season
title: Attractor list must hide deprecated ideas
---
# hypothesis:attractor-list-must-hide-deprecated-ideas

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Measured 2026-09-03 after L1.09 deprecated all 159 build-site nodes: the injected map hides them (goal:s23, frame_stream hide_deprecated=True) but the attractive-ideas list in extensions/agi/bin/briefing.py (around lines 207-210) ranks every idea by raw descendant count with no deprecation filter, so INJECTION.md still hands every agent idea:domain-graph-core (75 descendants) as the top target. Two readers, two views of the same graph -- the goal:g9.7 violation in one line. Also worth doing in the same change: [task].md and [idea].md status regexes reject status: deprecated (precedent idea:engine-todo); add it. Falsifier: fixture graph with one deprecated idea holding many descendants; assert it is absent from the rendered attractor list; remove the filter and watch it go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director-minted from the L1.09 agent caveat #1; the survey claimed target selection would fall through naturally and it does not on this surface."
<!-- THOUGHT:END -->