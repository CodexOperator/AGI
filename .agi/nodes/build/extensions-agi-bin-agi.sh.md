---
id: build:extensions-agi-bin-agi.sh
mint_id: 9367101a1d634652a77e9a5bc0619b54
type: build
parents:
  - goal:g7.16.1.11.44.8
  - idea:agi-sh-one-town-stop-start-from-a-matrix-row
next_edges: []
build_kind: code
edited_by: director-general-2
link_ref: extensions/agi/bin/agi.sh
location: source_root
model: claude-sonnet-5-5
role: director
scaffold_hash: 09ede59050cea087
season: 3
title: "extensions/agi/bin/agi.sh: the town's stop (status, stop, answer); start follows"
town: core
---
# build:extensions-agi-bin-agi.sh

# extensions/agi/bin/agi.sh

The town's stop and start (status · stop · answer in S1; start and --pack / --from follow in S2 / S3). The step order is read from the engine.md matrix row `town start`; every step is a ck_<name> / dn_<name> pair; one [ask] per run (rc 20), [owner-do] rc 21. See idea:agi-sh-one-town-stop-start-from-a-matrix-row and goal:g7.16.1.11.44.8.
