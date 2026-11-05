---
id: build:extensions-agi-tests-recompose.t.sh
mint_id: 9df7f423b58c428ab31342e6fd696c97
type: build
parents:
  - goal:g7.16.1.11.46.18
  - mvp:g7161146-w2-g1b1-recompose-view
next_edges: []
build_kind: code
edited_by: director-general-3
link_ref: extensions/agi/tests/recompose.t.sh
confidence: 0.8
origin: build-scan
payload_ref: extensions/agi/tests/recompose.t.sh
tags:
  - g7.16.1.11.46.17
  - G1b-1
  - g7.16.1.11.46.18
  - G1b-2
location: source_root
role: director
season: 3
title: "recompose.t.sh -- the lane of goal:g7.16.1.11.46.17's view (rows + mutants)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# build:extensions-agi-tests-recompose.t.sh

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-28 (v2, goal:g7.16.1.11.46.18 G1b-2 slice (a)): 31 -> 39 rows. New: t11 + mutant (a git-rm'd live node = unread <mint>; membership from the trunk listing = diff 0), t11b (a never-landed row on a live node), m-ahead-by-inequality (T12), t13 + mutant (a path row added after the freeze), u2 + mutant (a never-landed row added after the freeze passes; T13 over every row reads it RED). Re-cut, same intent: the fixture map gains '<n7> never-landed'; t6 and k5 now read BEHIND (their trunk bytes are on no version of the ref: what T12 is for); k7 and s1's maps carry their never-landed rows; k6m's anchor follows the row parser into map_rows. PARENTS: the goal moved .46.17 -> .46.18, as its payload's build node.
<!-- THOUGHT:END -->
