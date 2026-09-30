---
id: build:tests-test-push-gap
mint_id: a91d2b4ea05f4880994dc4eb6b6fe795
type: build
parents:
  - goal:g7.16.1.4.1.1
  - idea:engine-tests
next_edges: []
build_kind: code
edited_by: director-general-4
link_ref: extensions/agi/tests/test_push_gap.py
location: source_root
payload_ref: extensions/agi/tests/test_push_gap.py
scaffold_hash: f3a41217e0da2d90
season: 2
title: "Build: extensions/agi/tests/test_push_gap.py"
town: core
---
# build:tests-test-push-gap

`extensions/agi/tests/test_push_gap.py` — the stranded-push alarm's tests (goal:s20), split out of `test_publish_alarm.py` when publish-engine.sh was retired (goal:g7.16.1.4.1.1): section 6 of that file (de5507a17^ lines 956-1331, 25 tests) restored verbatim, plus one test pinning the retired publish alarm's silence.

Census parent: `idea:engine-tests`.
