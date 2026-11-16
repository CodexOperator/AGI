---
id: build:bin-hub-move
mint_id: 2662b5b2b84342868b5787d8af7f733b
type: build
parents:
  - goal:g7.16.1.11.46.37
  - idea:g7161146-b1-console-openrouter-failure-healing
next_edges: []
build_kind: code
confidence: 0.7
edited_by: director-general-2
link_ref: extensions/agi/bin/hub_move.py
location: source_root
model: claude-sonnet-5-5
origin: build-version
payload_ref: extensions/agi/bin/hub_move.py
role: director
scaffold_hash: 2181709a59849da3
season: 3
status: active
tags:
  - build
  - code
  - hub
  - quota
  - fallback
title: "hub_move.py -- the automatic hub fallback on a recorded QUOTA limit: decides from the host state and route files, moves a post to the other hub only when the other hub reads ok, never on hub-down alone, one automatic move per post, LOUD (the loud line, a standing line, the moved post's own-box line); edits no route (belam's host step)"
town: core
---

# build:bin-hub-move

`extensions/agi/bin/hub_move.py` -- the ENGINE half of goal:g7.16.1.11.46.37, the owner's Q3 yes (11-15, c:696556deb72a): an automatic hub fallback on a recorded QUOTA limit and nothing else. `decide` reads the host-written `<HUBDIR>/state` (through hub_quota.read_state, the ONE reader) and `<HUBDIR>/route` (`POST HUB MODEL` | `POST direct`, line 1 `written EPOCH`, older than --max-age = unread, no move, rc 1) and its own memory file, and decides: a post routed to HUB whose (HUB, MODEL) line reads `quota` moves to THE OTHER hub (--hubs, default A,B) only when that hub's (MODEL) line reads `ok` (any age: an idle hub records nothing; only the file's `written` must be fresh) and it has no hub-wide down line. It never moves on hub-down alone, never into a hub that is quota / down / without a line (ONE said refusal per hub, model and reset, naming the posts held), never a post with no route row or `direct` (`NAME: off-hub, no move`, never unread), and never a post twice: ONE automatic move per post, so a moved post reading quota on its NEW hub is not moved back (ONE said refusal naming the standing move) until `clear POST` (belam's or the owner's).

A move says three things: the LOUD line to --said and the alarm spool (`post X (M) DECIDED B -> A on quota (B until HH:MMZ), pending the host step; A ok as of MM-DD HH:MMZ, unconfirmed since`: the age of the target line it trusted; DECIDED because the route changes only when the host step applies it), the STANDING line to --said only (`post X decided onto hub A at HH:MMZ, moved from B on quota, pending the host step`; the host writes 'on hub A since' when it applies). A move BACK is `hub_move.py clear X` THEN the route edit: --moves is rewritten whole from memory, so a route edit alone is re-applied; a post seen on its `to` hub and later on its `from` hub with the standing move kept gets ONE said line naming `clear X` Every spool line carries a DETERMINISTIC alarm id hm-<kind>-<hash of the DECISION (post, from, to, model, reset)>, never of the wording, so a replayed partial delivery is one id to the drain (all-is-one). (child of 269cd97451, sp + alive + all-is-one 11-16; both are a PRECONDITION of the host half's gate), and ONE line to the moved post's OWN box (a spool line --to the post). It writes --moves, the route rows the host should apply (`POST HUB MODEL`, replaced whole each run from memory). It edits no route and no hub: the route file is root-only and holds the hub token, so the APPLYING step is belam's host act, and the decider carries no token and no account name. A line not delivered leaves the memory unsaved, so it is decided and said again next run. hub_quota.py `say` and stall_watch.sh still move nothing.

Tests: extensions/agi/tests/test_hub_move.py, rows f1-f6 of the leaf's Falsifier on fixture files, each with a mutant (a one-edit copy of hub_move.py that must read RED; a mutant whose anchor is gone fails the row, never a vacuous pass). Row 7 (live: one decided move applied on a SCRATCH route, the said file and the post's own box, and when the new route takes effect) is belam's host step.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-16, director-general-2: first version, the engine half SM placed (20:12Z 11-15) for goal:g7.16.1.11.46.37. Parents [goal, idea], the shape bin-hub-quota used (the idea b1 names the bundle). DECISIONS where the goal left a choice, for the council to check: (1) the decider is its OWN file and unit; hub_quota.py `say` and stall_watch.sh keep acting on nothing, as the leaf's Invariant says. (2) The state is read through hub_quota.read_state, not a copy: ONE parser of the host's file, so a shape change in .46.35 reaches the mover. (3) The route is read by a small reader here (read_route): `POST direct` is OFF-HUB (never moved, never unread), a malformed or stale route is unread rc 1, nothing moved. (4) The other hub is named by --hubs (default A,B), never inferred from the state: an idle hub records no line, so a hub set derived from the state would lose the very hub we move to. (5) FRESH is the FILE's `written` line only; an ok line of any age counts (measured 11-15: written 1794774432, hub A opus T 1794581580). The fixture of row 1 is that shape, and a per-line age mutant reads RED. (6) A refusal because the target is not ok is ONE line per (hub, model, reset, why) naming the posts held, not one per post: twelve posts on one hub in quota must not mail twelve lines each cycle. (7) The standing line goes to the said file only, the loud line to the said file AND the spool, the moved post's line to the spool addressed to the post: whether the drain can deliver to a post the seat is not adjacent to is the matrix's, and row 7 pins it on belam's scratch. (8) --moves is the route rows the host should apply, rewritten whole from memory each run, so a failed host step or a lost file heals on the next run. (9) The move-back is NOT built: the standing move is cleared by `clear POST` (belam or the owner) and only then may the post move again. NEAR MISS that shaped row 5: the first sketch cleared a standing move when the first hub recorded a 200; that is a move back by another name, and its mutant is a row. Not seen: the live host step (row 7).
<!-- THOUGHT:END -->
