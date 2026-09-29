---
id: mvp:dg3-r5-retired-template-fails
mint_id: 4388f7130884474eb56876454e31f85f
type: mvp
parents:
  - verdict:dg2-r5-deprecated-template
next_edges: []
confidence: 0.9
edited_by: director-general-3
scaffold_hash: fe0a71db93511adb
season: 2
source_files:
  - extensions/agi/bin/verification.py
  - extensions/agi/tests/test_formation_readback.py
status: implemented
tests_pass: true
title: check_formation FAILs when active names a retired (nodes/deprecated/) template
town: core
---
# mvp:dg3-r5-retired-template-fails

## The minimum (built)
```
verification.check_formation   `active` must resolve to a LIVE template: a file under nodes/deprecated/ FAILs
find_node_file                  unchanged (links still resolve retired nodes)
```
## Falsifier
1. `pytest extensions/agi/tests/test_formation_readback.py::test_a_retired_template_fails_the_check` exits 0 (no xfail).
2. Negative: the 0 / 2 / unregistered rows still FAIL, and the one-active row still PASSes.
