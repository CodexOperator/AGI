---
id: experiment:a00-1b9a8e7e-profile-sync
mint_id: 6c0ae0d819e943ee9debee4ba000dcdd
type: experiment
parents:
  - hypothesis:a00-1b9a8e7e-9f618e
next_edges: []
edited_by: a00-1b9a8e7e
evidence_runs: experiment:a00-1b9a8e7e-profile-sync
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "write.py hypothesis:h1 replace body 1:1 - (stdin projected), node declares profile_ref", "expected": "artifact bytes == normalized node body (THOUGHT stripped, one trailing newline)", "observed": "write.py printed updated: hypothesis:h1; profile/out.md = projected\\n\\nrule one\\n (20 bytes, sha256 715129fa6ef8...); no THOUGHT marker in artifact", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "profile_sync.py hypothesis:h1 --check after writing mutated to the artifact", "expected": "non-zero exit, DRIFT line, artifact not rewritten", "observed": "DRIFT .../profile/out.md rc=1; artifact still mutated", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "profile_sync.py hypothesis:h1 with profile_ref removed", "expected": "exit 0, no profile_ref line, no artifact created", "observed": "hypothesis:h1: no profile_ref rc=0; profile dir absent", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "profile_sync.py hypothesis:h1 with profile_ref: ../escape.md", "expected": "exit 2, refused by name, no file written", "observed": "REFUSED: profile_ref ../escape.md resolves outside the repo root rc=2; escape.md absent", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "profile_sync.py hypothesis:h1 with profile_ref: .agi/nodes/evil.md; then write.py hypothesis:h1 note x", "expected": "exit 2 refused under .agi/nodes/, nothing written; write.py surfaces non-zero", "observed": "REFUSED ... rc=2, evil.md absent; write.py ERR: profile projection refused ... rc=2", "result": "pass"}
production_lines: 80
profile: balanced
rebrief_request: "80 production lines: the delivered module needs 70 (atomic write + 4 named CLI behaviours + 3 named refusals) plus 10 in write.py; the tests are separate. Raised ceiling: 80."
role: kid
scaffold_hash: 4808ffc54dbbc9f1
season: 2
title: write.py projects profile_ref-linked bytes in the same action
town: core
verdict: proved
---
# experiment:a00-1b9a8e7e-profile-sync

## Experiment

Built the graph -> profile projection for `goal:g7.31.5.1` and proved it on
the built bytes, not on a reproduction of the defect.

Production bytes (2 paths):
- NEW `extensions/agi/bin/profile_sync.py` — link field `profile_ref` (a NEW
  field, never `link_ref`: `link_ref` makes the file the SoT and the node the
  projection, the reverse of this goal's invariant). `project()` reads the
  node through `node_writer.find_node_file` + `graph_core.persistence.
  frontmatter.load_node_file`, strips the THOUGHT region via
  `node_writer.extract_thought`, normalizes to exactly one trailing newline.
  `sync_node()` writes tmp + `os.replace` (atomic). CLI prints one proof line;
  `--check` compares and never writes; a node with no `profile_ref` prints
  `no profile_ref` and exits 0; refs outside the repo root or under
  `.agi/nodes/` are refused by name (exit 2) and never written.
- EDIT `extensions/agi/bin/write.py` — `import profile_sync` at module scope,
  and in `submit()`, after `node_writer.update_node`, `sync_node` runs when
  the node declares `profile_ref`. `NoRef` is the explicit no-op; `Refused`
  re-raises as `EditError`, so a bad ref surfaces non-zero. No direct file
  write in `write.py` — the ast guard stays green.

Test file (separate): `extensions/agi/tests/test_profile_sync.py`, 6 cases.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q
123 passed, 74 warnings in 25.35s
```

Same-action (falsifier conjunct 1), on a scratch fixture under the session dir:
```
$ write.py hypothesis:h1 'replace body 1:1 -'   # stdin: projected
updated: hypothesis:h1
$ cat profile/out.md
projected

rule one
```

Drift, no write:
```
$ profile_sync.py hypothesis:h1 --check   # artifact mutated on disk
DRIFT .../profile/out.md bytes=20 sha256=715129fa...   rc=1
$ cat profile/out.md
mutated
```

No link:
```
$ profile_sync.py hypothesis:h1            # profile_ref removed
hypothesis:h1: no profile_ref              rc=0   (no artifact created)
```

Refusals by name:
```
$ profile_sync.py hypothesis:h1            # profile_ref: ../escape.md
REFUSED: profile_ref '../escape.md' resolves outside the repo root   rc=2
$ profile_sync.py hypothesis:h1            # profile_ref: .agi/nodes/evil.md
REFUSED: profile_ref '.agi/nodes/evil.md' resolves under .agi/nodes/   rc=2
$ write.py hypothesis:h1 'note x'          # same bad ref
ERR: profile projection refused: profile_ref '.agi/nodes/evil.md' resolves under .agi/nodes/   rc=2
```

`.agi/config.json` sha256 before/after identical:
`d899e19498953ed6a34e742435614b6521aa883ce26f06f9c338b88e116adb59`.
`grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing (rc=1).

Raw output, screenshots, logs.
