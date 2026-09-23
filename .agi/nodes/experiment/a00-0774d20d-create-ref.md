---
id: experiment:a00-0774d20d-create-ref
mint_id: f1d895e66c6d41eaadf27aa485d8d6f5
type: experiment
parents:
  - hypothesis:a00-0774d20d-cbb0c4
next_edges: []
edited_by: a00-0774d20d
evidence_runs: experiment:a00-0774d20d-create-ref
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 32
profile: balanced
role: kid
scaffold_hash: cfe1a69a4dd24ebc
season: 2
title: "Create-path profile_ref: the pre-fix hole and the fix probes"
town: core
---
# experiment:a00-0774d20d-create-ref

## Experiment

Measured the pre-fix state and the fix on the built bytes at tip bf0240529,
then wired the create path through the edit route's helpers and re-measured.

Pre-fix (measured, scratch repo under
`.agi/sessions/iter-DH.78/a00-0774d20d/`):
```
$ write.py create hypothesis probe-ill2 --parent goal:g7.31.5.1 --set profile_ref=../escape2.md
created: hypothesis:probe-ill2 ...  rc=0   # node minted with an illegal ref
$ write.py create hypothesis probe-ok --parent goal:g7.31.5.1 --set profile_ref=profile/out.md
created: hypothesis:probe-ok ...   rc=0   # profile/out.md does NOT exist
$ write.py create hypothesis probe-ok ... --dry-run
create hypothesis:probe-ok ...     rc=0   # dry run printed success
```

Residues from DH.72, re-measured and holding:
- illegal on-disk ref + body edit: dry-run rc=2 AND real rc=2, node sha
  unchanged, no artifact;
- `profile_sync.py hypothesis:nope` -> `REFUSED: no node file for
  'hypothesis:nope'` rc=2, no traceback.

Fix (32 production lines in `write.py`, ceiling 40): `_profile_ref_refusal`
calls `profile_sync.refuse_effective_ref`; `main`'s create branch calls it
before the dry-run short-circuit; `create()` calls it before `write_node` and
then `profile_sync.sync_node` after a successful mint (catching `NoRef`).

Post-fix, same probes:
```
$ write.py create hypothesis probe-ill ... --set profile_ref=../escape2.md
ERR: profile projection refused: profile_ref '../escape2.md' resolves outside the repo root  rc=2
   -> probe-ill.md absent, ../escape2.md absent
$ write.py create hypothesis probe-ill2 ... --dry-run
ERR: profile projection refused: ...  rc=2   -> no node
$ write.py create hypothesis probe-ok ... --set profile_ref=profile/out.md
created: hypothesis:probe-ok ...  rc=0   -> profile/out.md EXISTS, body projected
$ write.py create hypothesis probe-nodes ... --set profile_ref=.agi/nodes/evil.md
ERR: profile projection refused: ... resolves under .agi/nodes/  rc=2 -> no node
$ write.py create hypothesis probe-none --parent goal:g7.31.5.1
created: ... rc=0   -> no artifact (unlinked create unchanged)
```

## Evidence

`probe.sh` / `probe.result` in
`.agi/sessions/iter-DH.78/a00-0774d20d/` — full transcript above; every
assertion PASS.

Repo suite on the patched bytes:
```
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q
143 passed, 75 warnings
```
(140 before, 3 added in `test_write.py`: illegal-ref refusal before writing,
legal-ref same-action projection, create dry-run refusal.) The
`test_edit_py_contains_no_file_write` ast guard in `test_write.py` stays green.
