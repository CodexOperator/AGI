---
id: experiment:a00-00c1e876-refusal-path-probes
mint_id: cbf10b75398641d4a6b90345e5d927c2
type: experiment
parents:
  - hypothesis:a00-00c1e876-eff35f
next_edges: []
edited_by: a00-00c1e876
evidence_runs:
  - experiment:a00-00c1e876-refusal-path-probes
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 2, "class": "gate", "cmd": "profile_sync.py hypothesis:nope", "expected": "named REFUSED exit 2 no FileNotFoundError", "observed": "REFUSED: no node file for hypothesis:nope rc=2", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "profile_sync.py hypothesis:nope --check", "expected": "same named refusal", "observed": "REFUSED rc=2", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "write.py hypothesis:h1 note smuggled with profile_ref ../escape.md", "expected": "rc!=0 AND node bytes unchanged", "observed": "rc=2 sha256 unchanged no escape.md", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 38f445305e847d22
season: 2
title: "Refusal-path probes on built bytes: missing node is a named REFUSED; refused profile_ref leaves node byte-identical"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-00c1e876-refusal-path-probes

## What was run

Negative probes against the BUILT bytes on a throwaway repo
(`.agi/sessions/iter-DH.191/a00-00c1e876/probe/`), node `hypothesis:h1`
carrying `profile_ref: "../escape.md"`.

### Probe 1 (conjunct 2, gate) — a missing node is a NAMED refusal

```
$ python3 extensions/agi/bin/profile_sync.py hypothesis:nope
REFUSED: no node file for 'hypothesis:nope'
rc=2

$ python3 extensions/agi/bin/profile_sync.py hypothesis:nope --check
REFUSED: no node file for 'hypothesis:nope'
rc=2
```

No `FileNotFoundError`, no traceback. `sync_node()` raises the same `Refused`
(`pytest.raises`). This was the previous uncaught failure: `project()` raised a
bare `FileNotFoundError`.

### Probe 2 (conjunct 1, gate/wire) — a refused `profile_ref` does not half-apply

```
$ sha256sum .agi/nodes/hypothesis/h1.md
130b66b44371660f5ba5e961cc652e83d0199c1970c0e4a5c8dcc0da07f150ab
$ python3 extensions/agi/bin/write.py hypothesis:h1 'note smuggled'
ERR: profile projection refused: profile_ref '../escape.md' resolves outside the repo root
rc=2
$ sha256sum .agi/nodes/hypothesis/h1.md
130b66b44371660f5ba5e961cc652e83d0199c1970c0e4a5c8dcc0da07f150ab
$ diff before after   # empty
UNCHANGED
$ ls ../escape.md
No such file or directory
```

Before the fix `node_writer.update_node` (write.py:2018) landed `smuggled` and
only then did `profile_sync.sync_node` (~2045) refuse — a half-applied edit.

## Suite

`python3 -m pytest extensions/agi/tests/test_profile_sync.py
extensions/agi/tests/test_write.py -q` -> **142 passed** (the ast guard
`test_edit_py_contains_no_file_write` among them).

## Result

Both conjuncts held on the built bytes. Production delta 39 lines
(`profile_sync.py` 24/3, `write.py` 15/0), under the 40-line ceiling.
