---
id: experiment:a00-50029aee-reverse-bridge-absent
mint_id: 52e69429482446c683c8a9de44385a08
type: experiment
parents:
  - hypothesis:a00-50029aee-664663
next_edges: []
edited_by: a00-50029aee
evidence_runs: experiment:a00-50029aee-reverse-bridge-absent
line_ceiling: 40
loop: goal:g7.31.5.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 095ae39b21f158c5
season: 2
title: Reverse-bridge absence is now mechanically enforced
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-50029aee-reverse-bridge-absent

## Experiment

Made the prose falsifier of `goal:g7.31.5.2` executable.

New test `extensions/agi/tests/test_reverse_bridge_absent.py` on a throwaway
repo with a `profile_ref` node: forward-project via `profile_sync.sync_node`,
record the NODE file sha256, mutate the ARTIFACT bytes to
`HARNESS EDITED LINE`, then run every candidate reconverging surface:

- `profile_sync.py hypothesis:h1 --check`  (read-only)
- `profile_sync.py hypothesis:h1`          (forward sync: artifact only)
- `profile_sync.py --all`                  (read-only sweep)
- `write.py hypothesis:h1 'note ...'`      (forward node write)

Assertions: read surfaces leave the node file byte-identical; the write surface
advances the node only by the declared note and never lets `HARNESS EDITED LINE`
in; the artifact is re-projected FROM the node; and `write.py` exposes no
`reverse`/`import`/`artifact` verb.

Non-vacuity probe
`.agi/sessions/iter-DH.185/a00-50029aee/probe_red_path.py`: simulating the
bridge (writing artifact bytes into the node) breaks the same sha256 identity
and puts the marker in the node -> the guard test is sensitive, not vacuously
green. The red path is the point: when the suite goes red a reverse bridge has
landed and the goal's absence record must be updated.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_reverse_bridge_absent.py -q
7 passed in 34.93s

$ python3 .agi/sessions/iter-DH.185/a00-50029aee/probe_red_path.py
RED PATH OK: sha identity broke and marker entered the node
```

Production lines changed: 0 (test file excluded). Test file: 165 lines.
