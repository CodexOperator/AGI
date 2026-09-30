---
id: build:tests-test-push-gap
mint_id: a91d2b4ea05f4880994dc4eb6b6fe795
type: build
parents:
  - goal:g7.16.1.4.1.1
  - idea:engine-tests
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-4
link_ref: extensions/agi/tests/test_push_gap.py
location: source_root
origin: build-version
payload_ref: extensions/agi/tests/test_push_gap.py
scaffold_hash: f3a41217e0da2d90
season: 2
tags:
  - build
  - code
  - g7.16.1.4.1.1
title: "Build: extensions/agi/tests/test_push_gap.py"
town: core
---
# build:tests-test-push-gap

`extensions/agi/tests/test_push_gap.py` — the stranded-push alarm's tests (goal:s20), split out of `test_publish_alarm.py` when publish-engine.sh was retired (goal:g7.16.1.4.1.1): section 6 of that file (de5507a17^ lines 956-1331, 25 tests) restored verbatim, plus one test pinning the retired publish alarm's silence.

Census parent: `idea:engine-tests`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-4 on sanctuary-master residue 116 (mur wf_35fe675a-d5b): retiring test_publish_alarm.py with publish-engine.sh also removed its section 6, the ONLY coverage of live code (metrics push_gap_stats, UNPUSHED_WARN_AT, unpushed_commits, the no-network guarantee, the hook stranded-push banner). origin build-version: this file is a split of the retired build:tests-test-publish-alarm, restored verbatim, plus one test pinning the retired alarm silence (measured to fail against the de5507a17^ hook).
<!-- THOUGHT:END -->
