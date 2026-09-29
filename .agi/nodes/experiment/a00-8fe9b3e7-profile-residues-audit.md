---
id: experiment:a00-8fe9b3e7-profile-residues-audit
mint_id: 06d97b991a9b46a1950daf37d43a1efc
type: experiment
parents:
  - hypothesis:a00-d98256f8-5665e1
next_edges: []
edited_by: a00-8fe9b3e7
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "profile_sync.py hypothesis:x from mktemp -d /tmp (no enclosing .agi)", "expected": "exit 2, REFUSED naming no project root, no TypeError", "observed": "REFUSED: no project root — no enclosing .agi/config.json rc=2; no TypeError", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "profile_sync.py hypothesis:h1 with profile_ref: dirref in a scratch repo", "expected": "exit 2, REFUSED naming directory, no IsADirectoryError, no .tmp", "observed": "REFUSED: profile_ref dirref resolves to a directory, not a file rc=2; dirref empty", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "read write.py payload/projection block", "expected": "replace_payload before profile_sync.sync_node", "observed": "line 2028 payload guard, replace_payload 2035, sync_node 2045", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "grep production_lines on hypothesis:a00-1b9a8e7e-9f618e and experiment:a00-1b9a8e7e-profile-sync", "expected": "hypothesis declares none; experiment declares 81", "observed": "hypothesis 0 occurrences; experiment line 23 production_lines: 81", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 7799aeead5fc6108
season: 2
title: "Audited four DH.23 profile_sync residues on built bytes: three held, claim 4 named the wrong node"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-8fe9b3e7-profile-residues-audit

## Experiment

Corrective round DH.36 on `goal:g7.31.5.1`. The target node
`hypothesis:a00-d98256f8-5665e1` carried two PRIMARY residues: its BODY
asserted "All four closed ... 126 passed" against a verdict of
`inconclusive_lean_disproved:25`, and its `evidence_runs` named
`experiment:profile_sync_residues`, which resolves to no node on disk.

I re-ran the four conjuncts on the built bytes rather than trusting the
parent's summary. No production code was changed; this node only records
the audit and gives the target a real evidence run.

**C1 — no project root is refused by name.** Run from a cwd with no
enclosing `.agi/config.json` (a fresh `mktemp -d` under `/tmp`, which sits
outside this worktree and has no `.git`), `locations.find_project_root()`
returns `None` and `profile_sync.project` raises `Refused` before
`Path(None)` can. Named refusal, exit 2, no `TypeError`.

**C2 — a directory target is refused by name.** `artifact_path` checks
`p.is_dir()` before returning, so a `profile_ref` resolving to a directory
raises `Refused`; `dest.read_bytes()` is never reached, so no
`IsADirectoryError`. Exit 2, and no `.tmp` is left behind.

**C3 — the payload write is ordered BEFORE the projection.** Read directly
in `write.py`: the payload block opens at line 2028
(`if payload_ref and res.status != node_writer.REJECTED:`), calls
`node_writer.replace_payload` at line 2035, and only afterwards does
`profile_sync.sync_node` run at line 2045. A failed payload write therefore
cannot advance the derived artifact. Held structurally.

**C4 — claim 4 is FALSE as written.** The target says
"hypothesis:a00-1b9a8e7e-9f618e's declared `production_lines` matches ...
(81, not 80)". But `grep production_lines` on that hypothesis node returns
nothing (0 occurrences); the field lives on
`experiment:a00-1b9a8e7e-profile-sync` at line 23
(`production_lines: 81`). The count is right; the node named is wrong. The
claim as written is disproved, which is why the target's verdict stays
`inconclusive_lean_disproved:25` and its "all four closed" line is
withdrawn.

## Evidence

```
$ cd $(mktemp -d /tmp/noproj.XXXX)
$ python3 .../extensions/agi/bin/profile_sync.py hypothesis:x
REFUSED: no project root — no enclosing .agi/config.json
rc=2                      # no TypeError

$ cd .agi/sessions/iter-DH.36/a00-8fe9b3e7/scratch/repo   # scratch repo, profile_ref: dirref
$ python3 .../extensions/agi/bin/profile_sync.py hypothesis:h1
REFUSED: profile_ref 'dirref' resolves to a directory, not a file
rc=2                      # no IsADirectoryError; dirref/ still empty, no .tmp

$ grep -n 'if payload_ref and res.status != node_writer.REJECTED' extensions/agi/bin/write.py
2028:    if payload_ref and res.status != node_writer.REJECTED:
$ grep -n 'node_writer.replace_payload\|profile_sync.sync_node' extensions/agi/bin/write.py
2035:        dest, changed = node_writer.replace_payload(
2045:            profile_sync.sync_node(root, edit.node_id)

$ grep -n production_lines .agi/nodes/hypothesis/a00-1b9a8e7e-9f618e.md
(no output; 0 occurrences)
$ grep -n production_lines .agi/nodes/experiment/a00-1b9a8e7e-profile-sync.md
23:production_lines: 81
```

Production lines changed by this round: 0 (nodes only; no source touched).
Raw output, screenshots, logs.
