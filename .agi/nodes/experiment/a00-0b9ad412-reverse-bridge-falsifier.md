---
id: experiment:a00-0b9ad412-reverse-bridge-falsifier
mint_id: 757118ede93c4bb9b11c4da8345421ec
type: experiment
parents:
  - hypothesis:a00-0b9ad412-8ce481
next_edges: []
edited_by: a00-0b9ad412
line_ceiling: 40
loop: goal:g7.31.5.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch repo: edit profile/h1.md to HARNESS EDITED LINE, then python3 profile_sync.py hypothesis:h1 --check", "expected": "DRIFT rc=1 and the node file bytes unchanged (detector, not repairer)", "observed": "rc=1, DRIFT profile/h1.md bytes=21 sha256=c812f13f...; node sha 5839788cee129f7a unchanged", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_profile_sync.py -q; BIN = Path(__file__).resolve().parent.parent / bin = extensions/agi/bin", "expected": "the committed test drives the real profile_sync.py and write.py through subprocess, not a reimplementation", "observed": "19 passed in 76.66s; each surface is subprocess.run([sys.executable, str(BIN / profile_sync.py), ...])", "result": "held"}
  - {"conjunct": 1, "class": "auth", "cmd": "hash the node file before/after three profile_sync.py surfaces and write.py set title", "expected": "profile_sync.py writes only the artifact, never the node; write.py changes the node file (positive control)", "observed": "node sha 5839788cee129f7a unchanged across all three profile_sync.py surfaces; write.py set title moved the node file to bf6eade7bfd7ce38 and reset the artifact to node-derived bytes", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 882c4892878d5e80
season: 2
testable_claim: "The reverse bridge (projection artifact -> graph node) is ABSENT: the committed test test_artifact_edit_never_rewrites_the_linked_node asserts the node body is invariant under an artifact edit across every production surface that reads profile_ref, and is red the day a reverse bridge lands."
title: Committed regression test - editing a profile_ref artifact never rewrites the linked node (reverse bridge absent, detector live)
town: core
---
<!-- BODY:BEGIN -->
# Experiment: the absence test, committed and run

## What was run

Added ONE test to `extensions/agi/tests/test_profile_sync.py`:
`test_artifact_edit_never_rewrites_the_linked_node`.

It builds a fresh scratch repo (`_repo(tmp_path)`), forward-syncs
`hypothesis:h1`'s artifact via `profile_sync.sync_node`, records the node's
normalized body bytes (the projection payload: THOUGHT stripped), then rewrites
the artifact to `HARNESS EDITED LINE\n`. It runs every production surface that
reads `profile_ref` — `profile_sync.py hypothesis:h1 --check`,
`profile_sync.py hypothesis:h1`, `profile_sync.py --all`, and
`write.py hypothesis:h1 'set title control-title'` — asserting the node body is
unchanged after each. The `write.py` surface is also the POSITIVE CONTROL: it
must change the node's whole-file bytes (frontmatter), proving the probe can
observe a node-file change at all.

Command: `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q`

## Result

```
19 passed in 76.66s
```

Standalone probe (`.agi/sessions/iter-DH.123/a00-0b9ad412/probe.py`, real
`extensions/agi/bin/` code) confirms each surface:

```
after forward sync     node_sha 5839788cee129f7a artifact b'# standing\n\nrule one\n'
artifact edited        node_sha 5839788cee129f7a changed False
surface ['hypothesis:h1', '--check'] rc=1 node_sha=5839788cee129f7a unchanged=True out0=['DRIFT ... bytes=21 sha256=c812f13f...']
surface ['hypothesis:h1']            rc=0 node_sha=5839788cee129f7a unchanged=True out0=['synced ... sha256=c812f13f...']
surface ['--all']                    rc=0 node_sha=5839788cee129f7a unchanged=True out0=['OK hypothesis:h1 ... sha256=c812f13f...']
surface ['set title']                rc=0 node_sha=bf6eade7bfd7ce38 changed_file=True artifact='# standing\n\nrule one\n'
```

The BRIDGE-ABSENT direction held: no surface reconverged the artifact into the
node. The BRIDGE-DETECTOR direction: the assertion is red the day one does,
because it compares the node body before/after the artifact edit. The positive
control changed the node file (sha `bf6eade7…` vs `5839788c…`), so the
invariance assertions are non-vacuous.

## Evidence

`--check` prints `DRIFT` and returns 1: it detects divergence, it does not
repair it. The no-`--check` path resets the artifact toward the node-derived
bytes (forward projection). `--all` is read-only. `write.py` writes the node
first, then re-projects the graph onto the artifact — the artifact ends holding
node-derived bytes (`'# standing\n\nrule one\n'`), never the `HARNESS` edit.
Graph remains SoT; the reverse arrow is absent.
## Evidence

Raw output, screenshots, logs.
