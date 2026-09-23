---
id: experiment:a00-557ad6f2-profile-residues
mint_id: 93caa17b4bf94667a4eab762b780e27d
type: experiment
parents:
  - hypothesis:a00-557ad6f2-2234c5
next_edges: []
edited_by: a00-557ad6f2
line_ceiling: 40
production_lines: 34
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 7799aeead5fc6108
season: 2
title: "Closed both profile_sync residues on built bytes: 34 production lines, 23+117 tests green"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-557ad6f2-profile-residues

## Experiment

Build round on `goal:g7.31.5.1`. Two residues were live in the built bytes;
both were closed in production and proved on the built bytes.

**Residue 1 — partial write.** `write.py` used to call
`node_writer.update_node` and then `profile_sync.sync_node`; when the
projection raised `Refused`, the `EditError` fired AFTER the node body had
already landed (rc=2 with the graph advanced). Fix: a new read-only
`profile_sync.validate_effective(root, node_id, set_fm, unset_fm)` computes
the POST-EDIT ref (set_fm wins, else unset_fm clears, else the on-disk
value) and calls `artifact_path()` on it when non-empty. `write.py submit()`
calls it immediately before `update_node`; the existing post-write call is
unchanged. An edit that unsets or replaces a bad ref still lands, because
the ref checked is the one the edit leaves behind — no deadlock.

**Residue 2 — missing node.** `profile_sync.project()` raised
`FileNotFoundError(node_id)`; the CLI tracebacked (rc=1). Fix:
`Refused(f"node {node_id!r} not found")`, which `main()` already maps to a
`REFUSED:` stderr line and exit 2.

Production diff (`git diff --numstat`):
`extensions/agi/bin/profile_sync.py` 23 added / 1 removed,
`extensions/agi/bin/write.py` 11 added = **34 lines** against the 40-line
ceiling. No `.tmp` is created on any refusal path (both checks raise before
`sync_node` reaches its `tmp.write_bytes`). `write.py` still performs no
direct file write; `test_edit_py_contains_no_file_write` stays green.

## Probes (all PASS, built bytes)

1. Bad ref (`../escape.md`) + `replace body 1:1`: rc=2, stderr names
   `profile projection refused: profile_ref '../escape.md' resolves outside
   the repo root`, no `Traceback`, node file byte-identical before/after,
   no artifact written.
2. No deadlock: `unset profile_ref && replace body 1:1` rc=0 and the body
   changes; `set profile_ref profile/ok.md` rc=0 and the artifact lands.
3. `profile_sync.py hypothesis:does-not-exist`: rc=2,
   `REFUSED: node 'hypothesis:does-not-exist' not found`, no
   `FileNotFoundError`/`Traceback`, no artifact.
4. No `.tmp` under the repo after both refusal paths.
5. Preserved: no-ref rc=0 no-op; `--check` drift rc=1 without writing;
   same-action projection on `replace body`; outside-repo/`.agi/nodes/`/
   directory refs still refused by name — all re-run green.

## Tests

`python3 -m pytest extensions/agi/tests/test_profile_sync.py
extensions/agi/tests/test_write.py -q` -> **23 passed** and **117 passed**,
run on the built bytes. Five new tests in `test_profile_sync.py` cover the
probes above.

## Verdict basis

Both residues are closed and the preservations hold, so the hypothesis is
proved with the two named test files as the evidence surface.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
A single node was needed: the residues are one invariant (the graph must not
advance ahead of a projection that cannot be written) failing on two paths,
and a fix ordered after `update_node` would have re-created the first. The
post-edit projection of the ref is what makes the no-deadlock conjunct hold.
<!-- THOUGHT:END -->
