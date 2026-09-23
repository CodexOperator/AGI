---
id: experiment:a00-28606fd1-payload-ref-reverse-bridge
mint_id: 8c1f4b2a7d9e43c0b6a5f1d2e3c4b5a6
type: experiment
parents:
  - hypothesis:a00-28606fd1-7d3406
next_edges: []
confidence: 0.85
edited_by: a00-28606fd1
evidence_runs: experiment:a00-28606fd1-payload-ref-reverse-bridge
line_ceiling: 40
loop: goal:g7.31.5.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch node hypothesis:lk-1 link_ref: linked/note.md; write HARNESS EDITED into linked/note.md, then run links.py links, metrics.py, write.py hypothesis:lk-1 'payload linked/note.md', write.py hypothesis:lk-1 'read body 1:5'; hash the node file each time", "expected": "node file bytes identical to baf9f486/85d8d733 after every surface -- the linked file is read live, never materialized into the node", "observed": "lk-1 sha 85d8d733efe7 unchanged across all four surfaces; links.py reports '2 resolved, 0 broken'; node sha changed only when a node-directed write stamped edited_by/title", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "build node build:bp-1 payload_ref: linked/data.txt; edit linked/data.txt; re-run the level3.py write path (level3.build_node(..., prior_body=...) -> snapshot-goals.write_frontmatter(out, fm, body, origin='level3-scan', preserve_body=existing_body))", "expected": "if no reverse bridge, node file bytes unchanged", "observed": "node sha 30f935071586 -> e769d270936e (CHANGED); new body carries content_sha256 40c15a68... derived from the edited file; THOUGHT region preserved, BUILD-CONTRACT regenerated", "result": "failed"}
  - {"conjunct": 3, "class": "auth", "cmd": "python3 -c 'import write; print(sorted(write.VERBS))' | grep -iE 'import|reverse|artifact|reconverge'; grep -rl profile_ref extensions/agi/bin/", "expected": "no import/reverse/reconverge verb in the write verb layer", "observed": "VERBS = adopt, body_patch, link, note, patch, payload, payload_text, read, replace, set, thought, unset -- none reverse; only profile_sync.py (forward) reads profile_ref", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "profile_sync.py build:bp-1 --check after the artifact edit", "expected": "detector admits divergence instead of repairing the node", "observed": "build:bp-1: no profile_ref (rc=0, node untouched); for a profile_ref node the prior run's probe shows DRIFT rc=1 with node sha unchanged", "result": "held"}
production_lines: 0
profile: balanced
role: kid
season: 2
title: level3.py rewrites a payload_ref build node's body from the payload file
town: core
---
<!-- BODY:BEGIN -->
# Experiment: probing the `link_ref` / `payload_ref` reverse bridge

## What was run

Scratch repo at `.agi/sessions/iter-DH.129/a00-28606fd1/scratch` with its own
`.agi/config.json` and real engine code at `extensions/agi/bin/`:

- `hypothesis:lk-1` carrying `link_ref: linked/note.md`
- `build:bp-1` carrying `payload_ref: linked/data.txt`

Each linked file was edited harness-side, then every candidate surface was run
with the node file sha256 re-read before/after.

## Observed

| surface | node file bytes |
|---|---|
| `links.py links` | unchanged (`2 resolved, 0 broken`) |
| `links.py` (no verb) | unchanged |
| `metrics.py` | unchanged (`broken_links=0`) |
| `write.py <node> 'payload <path>'` | unchanged (writes the FILE) |
| `write.py <node> 'patch -'` | unchanged (patches the payload FILE) |
| `write.py <node> 'read body 1:5'` | unchanged |
| `profile_sync.py <node> --check` | unchanged (`no profile_ref`, or DRIFT rc=1) |

`write.py`'s verb set: `adopt, body_patch, link, note, patch, payload,
payload_text, read, replace, set, thought, unset` — no `import`/`reverse`/
`artifact`/`reconverge` verb. No production path reads a `link_ref` file as
input to a node write. `links.resolve` reads the file **live at read time** and
returns it as the node's resolved content but never materializes it into the
node file.

## The bridge that exists

`level3.build_node()` (`extensions/agi/bin/level3.py:1104`) derives a body from
the payload file's bytes and `snapshot-goals.write_frontmatter(...,
preserve_body=...)` writes it back; `preserve_body` only splices the authored
THOUGHT region, so the BUILD-CONTRACT block is regenerated every scan.

Ran that exact write path over `docprobe/doc.md` (`payload_ref` target):

```
node sha 30f9350715862e31   (before harness edit)
node sha e769d270936e55ec   (after edit + level3 write path)   CHANGED
+ content_sha256: 40c15a6836aa7cb9096822c01b26008d44745265ffb440f6147e657ec554dffd
```

## Conclusion

`payload_ref` HAS a materializing reverse bridge (`level3.py`): editing the file
rewrites the build node's BUILD-CONTRACT/`content_sha256` region. `link_ref` and
`profile_ref` remain absent. The `goal:g7.31.5.2` absence record must be
re-scoped: absent for `link_ref` + `profile_ref`, PRESENT for `payload_ref` via
`level3.py`.
