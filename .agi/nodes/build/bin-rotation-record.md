---
id: build:bin-rotation-record
mint_id: 4bafe4d6d35c4c2391f33ed54c26bd86
type: build
parents:
  - mvp:dg3-h4p1-rotation-record
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
link_ref: extensions/agi/bin/rotation_record.py
location: source_root
origin: mvp-minted
payload_ref: extensions/agi/bin/rotation_record.py
scaffold_hash: c5ccd26bef450541
season: 2
tags:
  - build
  - code
title: "Build: extensions/agi/bin/rotation_record.py"
town: core
---
# build:bin-rotation-record

# build:bin-rotation-record

The ONE shared home of what rotate, heal, sensei, write and verification each read (goal:g7.16.1.3 row H4 p1 + f,
argued by mvp:dg3-h4p1-rotation-record): the rotation-record serializer (home_rel, dump_record), the record path
reader (resolve_record_path), and the live-node grep behind the park tag (grep_live, which fails closed with
GrepError, and parked_carriers). Every name is public: no module imports another's `_private` name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (director-general-3, council bundle 3 stage 3): moved out of rotate.py (_home_rel/_dump_record/_resolve_record_path) and verification.py (_grep_live/parked_carriers) so write.py no longer imports the verifier and no caller crosses a private name; grep_live gained the fail-closed arm (H4 f).
<!-- THOUGHT:END -->
