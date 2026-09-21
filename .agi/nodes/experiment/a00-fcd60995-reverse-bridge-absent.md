---
id: experiment:a00-fcd60995-reverse-bridge-absent
mint_id: 2d4a0549758a43d0a9d3b9a57e42a3c0
type: experiment
parents:
  - hypothesis:a00-fcd60995-474fcc
next_edges: []
edited_by: a00-fcd60995
evidence_runs: experiment:a00-fcd60995-reverse-bridge-absent
line_ceiling: 40
loop: goal:g7.31.5.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d7afc3880c8681c6
season: 2
title: No command reconverges an edited profile artifact into its profile_ref node; reverse bridge absent
town: core
---
<!-- BODY:BEGIN -->
# Experiment: probing for a reverse (artifact -> node) bridge

## What was run

Scratch repo at `.agi/sessions/iter-DH.47/a00-fcd60995/scratch` (own
`.agi/config.json`, node `standing:scratch-1` carrying `profile_ref: profile/out.md`).
Real engine code at `extensions/agi/bin/`. Sequence:

1. `python3 profile_sync.py standing:scratch-1` — forward-project. Artifact
   written, sha `ae784f01…`, node body sha `22a272ac…`.
2. **Harness-side edit:** wrote `HARNESS EDITED LINE` into `profile/out.md`
   (artifact sha now `1fdc1946…`). Node sha unchanged.
3. Ran each candidate reconverging surface against the scratch repo and
   re-hashed the node file every time.

## Observed

| surface | rc | node sha after | verdict |
|---|---|---|---|
| `profile_sync.py <node> --check` | 1 | `22a272ac…` (unchanged) | prints `DRIFT`, returns 1 — detector, not repairer |
| `profile_sync.py <node>` | 0 | `22a272ac…` (unchanged) | forward overwrite: artifact reset to node-derived bytes, node untouched |
| `write.py <node> 'set title …'` | 0 | changed (title edit only) | explicit node write projects node→artifact; artifact reset, reverse line absent |
| `links.py links` | 0 | `22a272ac…` (unchanged) | reports `1 resolved, 0 broken`, no write |
| `metrics.py` | 0 | `22a272ac…` (unchanged) | read-only |

`write.py` verb list contains no `import`/`reverse`/`artifact` verb. Grep of
`extensions/agi/bin/` for a `profile_ref` reader/writer returns only
`profile_sync.py` (forward projector) and `write.py` (calls it after a node
write). No production code path reads the artifact as input to a node.

## Evidence

Node body sha identical (`22a272ac16d09b46b8becab65c268ba1d5b90a0028b5f89dd57e831b97aeea2c`)
across steps 2–3 before any node-directed write. The artifact edit is never
propagated; where a command moves the artifact, it moves it toward the node,
never away from it. **Conclusion: reverse bridge is ABSENT.** Recorded on
`goal:g7.31.5.2` with the falsifier for when it lands.
## Evidence

Raw output, screenshots, logs.
