---
id: experiment:profile-ref-prevalidation
mint_id: 29c7ca328a4b47f3bc7ed2623492cd5c
type: experiment
parents:
  - hypothesis:a00-3dd9eb76-eb2e65
next_edges: []
edited_by: a00-1b6e88a9
evidence_runs:
  - experiment:profile-ref-prevalidation
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "pre-fix byte-copy of write.py, scratch node declares profile_ref: ../escape.md, write.py hypothesis:h1 replace body 1:9 -", "expected": "defect reproduced: rc=2 but node body changed", "observed": "rc=2; sha d45209e... -> d8e946d... (changed); smuggled body present", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "patched write.py, same ../escape.md ref, replace body", "expected": "rc!=0, node sha unchanged, no artifact, no stray .tmp", "observed": "rc=2 ERR profile projection refused ... resolves outside the repo root; sha 3660d22 unchanged; escape.md absent; no .tmp", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "patched write.py, profile_ref: .agi/nodes/evil.md, replace body", "expected": "rc!=0, node sha unchanged, nothing written under .agi/nodes", "observed": "rc=2 ERR ... resolves under .agi/nodes/; node byte-identical; evil.md absent", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "patched write.py, legal profile_ref: profile/out.md, replace body 1:9 -", "expected": "rc=0, artifact == normalized body (THOUGHT stripped, one trailing newline), same action", "observed": "rc=0 updated:; profile/out.md = b\"# replaced\\n\\nnew body\\n\"; od confirms one trailing newline; no THOUGHT marker; --check OK rc=0", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q", "expected": "green, ast no-file-write guard green", "observed": "135 passed, 74 warnings in 12.74s", "result": "pass"}
production_lines: 34
profile: balanced
push_further: "(b) the missing-node-id half only: project() raised a bare FileNotFoundError uncaught by main() -> now a named refusal; the directory-target half is already refused by artifact_path() (test green). (a) bind profile_ref to the real Grok Bot profile surface once goal:g7.30 lands; (c) make sync_node transactional with the node write."
role: kid
scaffold_hash: acebacfa97b5b43f
season: 2
title: Refused profile_ref is refused before the node body lands
town: core
verdict: proved
---
# experiment:profile-ref-prevalidation

## Experiment

Closed the open defect recorded in
`experiment:a00-1b9a8e7e-profile-sync`: on the REFUSED-`profile_ref` path,
`write.py` ran `node_writer.update_node` first and only then called
`profile_sync.sync_node`, so a refused write returned rc=2 while the node body
had ALREADY changed — a partial write. The fix validates the EFFECTIVE
`profile_ref` (this edit's `set profile_ref` if it carries one, else the one on
the node file; an edit that unsets it validates nothing) through a new
`profile_sync.validate_ref()` BEFORE `update_node`.

Production bytes (34 lines, ceiling 40):
- EDIT `extensions/agi/bin/profile_sync.py` (+12): `validate_ref(root, ref)`
  resolves through `artifact_path` and refuses by name, writing nothing.
- EDIT `extensions/agi/bin/write.py` (+22): in `submit()`, before
  `node_writer.update_node`, the effective ref is resolved and a `Refused` is
  re-raised as `EditError`. The post-update `sync_node` call is unchanged, so
  the happy path still projects in the same action.

## Evidence

Pre-fix state, measured on a byte-copy of this tree's `write.py` with only the
new block stripped (the other bin modules symlinked, so it is the real
unpatched path), against a scratch repo whose node declares
`profile_ref: "../escape.md"`:
```
$ python3 $SCR/prefix/write.py hypothesis:h1 "replace body 1:9 -" < new
ERR: profile projection refused: profile_ref '../escape.md' resolves outside the repo root
rc=2
sha_before=d45209edae1601493de3d5af3f51968ef05c611fa0beb48a4821042657552d9e
sha_after =d8e946deba8491bd2a344e67c31abc3e09411c78a5c846b004ecfb86eaa6d17e
PREFIX: node CHANGED despite refusal (defect reproduced)
```

Post-fix, same probe with the patched `write.py`:
```
$ python3 $W hypothesis:h1 "replace body 1:9 -" < new
ERR: profile projection refused: profile_ref '../escape.md' resolves outside the repo root
rc=2
sha_before=3660d224f3cad7876d692707880aefd7636bd8130da115c7e815122230fa8dbf
sha_after =3660d224f3cad7876d692707880aefd7636bd8130da115c7e815122230fa8dbf
PROBE1 PASS: node byte-identical
PROBE1 PASS: no artifact outside repo
PROBE1 PASS: no stray tmp
```

`.agi/nodes/` ref refused, node untouched:
```
ERR: profile projection refused: profile_ref '.agi/nodes/evil.md' resolves under .agi/nodes/
rc=2
PROBE2 PASS: node byte-identical
PROBE2 PASS: no artifact under nodes
```

Happy path unchanged (same action, normalized bytes):
```
$ printf '# replaced\n\nnew body\n' | python3 $W hypothesis:h1 "replace body 1:9 -"
updated: hypothesis:h1
rc=0
$ od -c profile/out.md
0000000   #       r   e   p   l   a   c   e   d  \n  \n   n   e   w
0000020   b   o   d   y  \n
PROBE3 PASS: no THOUGHT marker
PROBE3 PASS: normalized body, one trailing newline
$ python3 $P hypothesis:h1 --check
OK .../profile/out.md bytes=21 sha256=cd3aa6df0b29...   rc=0
```

Repo suite (patched bytes):
```
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q
135 passed, 74 warnings in 12.74s
```
The no-file-write ast guard (`test_edit_py_contains_no_file_write`) is part of
`test_write.py` and stays green.
