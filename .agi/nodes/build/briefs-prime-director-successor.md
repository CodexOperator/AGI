---
id: build:briefs-prime-director-successor
mint_id: 59284f74c6ef44ebaacfff1647507e49
type: build
parents:
  - mvp:briefs
next_edges: []
build_kind: prose
confidence: 1.0
edited_by: owner
link_ref: extensions/agi/briefs/prime-director-successor.md
location: source_root
origin: mvp-minted
payload_ref: extensions/agi/briefs/prime-director-successor.md
scaffold_hash: 16bef268798dc533
season: 2
tags:
  - build
  - prose
  - g15
thought_session: rc-XVI
title: Briefs prime director successor
---
<!-- BODY:BEGIN -->
# build:briefs-prime-director-successor

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by hand by sanctuary-director gen VI (SD.17), not by level3.py: this file is outside level3's scan set, which is .py/.sh/.js under extensions/ skills/ src/ bin/. DEVIATION, recorded per the delegated-authority rule. The dispatch order said .agi/config.json should carry location: graph_root. It must not. grid.py resolve_payload is location-blind -- it computes engine_root/payload_ref and never consults locations.payload_base -- so graph_root + payload_ref config.json resolves correctly through write.py while grid.py returns None, and 'grid.py payload' (the close this round was judged on) would have returned nothing against a node that looked well-formed. Measured both shapes before minting; source_root with a repo-root-relative payload_ref is the only one both paths agree on. Shape copied from build:drafting.json, the one proven non-code payload: BOTH link_ref and payload_ref set, because write.py create --payload stamps only link_ref while grid.py and grid_coverage_check.py read only payload_ref -- a node minted with --payload alone is invisible to the grid. Closed by reading the real bytes back out of the grid after commit --all, not by trusting the created: line. Parent mvp:briefs was minted with it, in the established per-subsystem pattern (mvp:bin-modules, mvp:hooks, mvp:tests, mvp:sources, mvp:workflows, mvp:scripts), because extensions/agi/briefs/ had no mvp and goal:s29 needs one.
<!-- THOUGHT:END -->