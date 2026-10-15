---
id: mvp:dg3-m-marker-strings
mint_id: 8ccfc76e92474c60b61e475f13869f5f
type: mvp
parents:
  - verdict:dg2-m-marker-strings
next_edges: []
confidence: 0.9
edited_by: director-general-3
scaffold_hash: f90aa26741c7e622
season: 2
source_files:
  - extensions/agi/bin/node_writer.py
  - extensions/agi/bin/snapshot-goals.py
  - extensions/agi/bin/write.py
status: implemented
tests_pass: true
title: The THOUGHT marker strings live in node_writer only; snapshot-goals re-exports them, write.py imports them
town: core
---
# mvp:dg3-m-marker-strings

## The minimum (built)
```
node_writer.THOUGHT_BEGIN / THOUGHT_END   the ONE spelling, moved verbatim from snapshot-goals.py (em dash included)
snapshot-goals.py                         THOUGHT_BEGIN = node_writer.THOUGHT_BEGIN (re-export; tests read sg.THOUGHT_*)
write.py thought verb                     f"{node_writer.THOUGHT_BEGIN}\n{thought}\n{node_writer.THOUGHT_END}"
```
## Falsifier
1. `pytest extensions/agi/tests/test_thought_hygiene.py::test_the_marker_strings_live_in_node_writer_only` exits 0 (no xfail).
2. `snapshot-goals.py --render --check` exits 0: the render is byte-identical (418 goals, 09-29).
