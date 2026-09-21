---
id: goal:g14.14.1
mint_id: 9d3b96ad6c1c480da6594fa25a0b41a6
type: goal
parents:
  - goal:g14.14
next_edges: []
confidence: 0.8
edited_by: director-engine
goal_id: G14.14.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 90c3d310cea4f4d6
season: 2
seeds:
  - hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices
  - hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-scaffold
  - hypothesis:lm-replace-body-standalone-restriction-is-documented-in-help
status: active
tags:
  - local-maxxing
  - engine
title: "G14.14.1: WRITE.PY ERGONOMICS -- three independent write.py gaps hit live this session: replace body has no anchor/structural guard (write.py:2068-2108, ABL.01 corruption class), create leaves an unfilled scaffold body, replace body cannot share a submit with note/thought (owner 01:1xZ-01:2xZ 09-21 on goal:g14.14)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.14.1

## Agent Notes
Source. Transcribed from the goal g14.14 body (owner 01:1xZ-01:2xZ 09-21 on goal g14). Three independent write.py gaps, each its own hypothesis when minted.

Commits to. Verified against source where checked this session, not assumed: (a) replace body N:M -- write.py _splice_range and _slice_range (lines 2068-2108) do plain text.split newline indexing with zero structural awareness of headings or paragraphs; _read_body_text (lines 2137-2146) returns the node BODY text starting at the BODY:BEGIN marker, which is why body-relative line 1 = that marker; _parse_range (lines 427-453) validates only that the range is numeric and non-empty, never that it respects a heading or paragraph boundary; no --at anchor option exists anywhere in verb_replace's signature. This is the exact class that corrupted ABL.01's winning node, and this director hit the same hazard live this session (worked around by always reading exact line numbers first, never guessing an offset). Fix: an anchor form (replace body --at HEADING) and/or a guard that refuses a range whose start or end falls inside a paragraph or splits a heading line from its body. (b) create leaves the unfilled scaffold body (the literal placeholder text, seen on TM.61/62/69 and SWR.01): create should render the body from the frontmatter it was given, or take a --body-file option. This director worked around it this session by minting with create then filling the body via note or a whole-range replace body -- a real workaround, not a fix. (c) replace body cannot share a submit with note or thought in the same write.py script -- either make ordered composition work, or the refusal should be printed in -h so a caller learns this from the help text rather than a failed edit; this director also hit an adjacent gap this session, chained note calls silently keeping only the last one (THOUGHT on goal:g14.14.3) -- likely the same family of submit-composition gap as (c), worth checking together.

Invariants. Kids write the fix, parents review, the director batches and orders. Existing behaviour is pinned with the full engine suite before and after each change (python3 -m pytest extensions/agi/tests -q). None of the three items may change how an ALREADY-CORRECT existing range or scaffold-filled node reads -- default/already-good behaviour must stay byte-identical.

Falsifiers. Each item is falsified independently: (a) if the anchor or guard fails to catch a real mis-offset case reproduced from the ABL.01 shape, or breaks a currently-correct replace; (b) if create with a --body-file or frontmatter-derived body ever produces the literal scaffold placeholder text; (c) if a chained note+replace (or note+note) script still silently drops content, or the -h refusal text is missing when composition is not supported. Any item breaking the engine suite is demoted, never merged.

Done when. All three lettered items have a landed round, proved or disproved with its WHY. (c) additionally checked against the chained-note bug found this session (goal:g14.14.3 THOUGHT) to see if one fix covers both.

First chunk, minted next: hypothesis for item (a), the replace body anchor/guard -- this director has the most direct operational evidence for it. Items (b) and (c) queued after, same format.
