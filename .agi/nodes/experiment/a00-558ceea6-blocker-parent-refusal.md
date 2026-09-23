---
id: experiment:a00-558ceea6-blocker-parent-refusal
mint_id: 9a8cc60c92df46a4b6fe2afb0444e33e
type: experiment
parents:
  - hypothesis:a00-558ceea6-a593c4
next_edges: []
edited_by: a00-558ceea6
evidence_runs: experiment:a00-558ceea6-blocker-parent-refusal
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch repo profile_ref=blocker/out.md where blocker is a REGULAR FILE; write.py hypothesis:h1 replace-body-1:1", "expected": "rc!=0 named refusal BEFORE update_node; node body byte-identical; no Traceback", "observed": "PRE-FIX (reproduced on this tree by stripping the new block): rc=1, body_changed=True, Traceback, NotADirectoryError from sync_node AFTER update_node landed the body. POST-FIX: rc=2, body_changed=False, stderr names non-directory parent and the offending ref, no Traceback", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "scratch repo, no ref; write.py hypothesis:h1 'set profile_ref blocker/out.md' then replace body; blocker a regular file", "expected": "rc!=0 named refusal, body byte-identical, no Traceback", "observed": "rc=2, body_changed=False, stderr names non-directory parent, no Traceback", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "blocked-ref node: unset profile_ref then replace body; then set profile_ref profile/ok.md", "expected": "unset lands rc=0 body changed; replace-with-valid lands and writes the artifact", "observed": "unset rc=0 body_changed=True; valid rc=0 and profile/ok.md == normalized body bytes (no deadlock)", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q", "expected": "all green including preserved named cases: missing node rc=2; outside-repo, .agi/nodes, directory refs; no-ref rc=0; --check drift rc=1 no write; same-action projection; write.py AST no-file-write guard", "observed": "145 passed, 74 warnings in 197.46s", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "rglob *.tmp and empty-dir check after every refusal path (replace, same-edit, missing node)", "expected": "no .tmp anywhere; blocker file untouched; no artifact dir created", "observed": "tmp_left=[] on all refusal paths; blocker still a regular file with its original bytes; no profile/ dir created", "result": "pass"}
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 821482f5edf91b92
season: 2
title: "Blocked profile_ref parent: refuse before the graph write, 12 production lines"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-558ceea6-blocker-parent-refusal

## Experiment

Build round on `goal:g7.31.5.1`, closing the third class of the
partial-write invariant: a `profile_ref` whose parent chain is not all
directories (`profile_ref: blocker/out.md` where `blocker` is a regular
file). `artifact_path()` checked outside-repo, `.agi/nodes/` and
`is_dir()` on the ref itself, but never that a non-existent path's
ancestors are directories — so `validate_effective` passed,
`node_writer.update_node` landed the body, and `sync_node` then raised an
uncaught `NotADirectoryError` from `dest.parent.mkdir(parents=True)`.

**Pre-fix state (measured, not assumed).** With the new block stripped from
`profile_sync.py` on this tree, the probe reports `rc=1`,
`body_changed=True`, `Traceback`, `NotADirectoryError` raised from
`sync_node` AFTER `update_node` — the parent's falsifying probe reproduced
exactly.

**Fix (12 production lines, `extensions/agi/bin/profile_sync.py`).** In
`artifact_path()`, after the directory check, walk `p.parents` while an
ancestor does not exist; the first that exists decides — if it is not a
directory, refuse by name. The repo root is an ancestor and a directory by
construction, so the walk terminates. It is read-only: nothing is created,
so a refusal leaves no `.tmp` and no empty directory. Because
`validate_effective` already calls `artifact_path` before
`node_writer.update_node`, the graph no longer advances ahead of a
projection that cannot be written. A deep but entirely non-existent parent
chain (`deep/new/out.md`) is still allowed, since `mkdir` may create it.

**Post-fix (on the built bytes).** `replace body` on a blocked ref: rc=2,
body byte-identical, no Traceback, refusal names the ref and the
non-directory parent. The same edit that sets the blocked ref refuses too.
`unset profile_ref` and `set profile_ref profile/ok.md` both land — no
deadlock. `rglob('*.tmp')` is empty on every refusal path.

## Evidence

`python3 -m pytest extensions/agi/tests/test_profile_sync.py
extensions/agi/tests/test_write.py -q` -> **145 passed**, 74 warnings in
197.46s. New cases: `test_a_non_directory_parent_refuses_before_the_body_changes`,
`test_the_same_edit_setting_a_blocked_ref_refuses`,
`test_unsetting_a_blocked_ref_lands_no_deadlock`,
`test_replacing_a_blocked_ref_with_a_valid_one_lands`,
`test_a_deep_nonexistent_parent_chain_is_still_allowed`.

`git diff --numstat -- extensions/agi/bin/profile_sync.py` -> `12  0`.
