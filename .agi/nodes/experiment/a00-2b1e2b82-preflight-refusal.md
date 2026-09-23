---
id: experiment:a00-2b1e2b82-preflight-refusal
mint_id: b0483c61694f4af7b13208f37dbb4760
type: experiment
parents:
  - hypothesis:a00-2b1e2b82-739979
next_edges: []
confidence: 0.9
edited_by: a00-2b1e2b82
evidence_runs: experiment:a00-2b1e2b82-preflight-refusal
line_ceiling: 40
production_lines: 26
title: A refused profile_ref refuses before the node write
verdict: proved
---
# experiment:a00-2b1e2b82-preflight-refusal

## Experiment

Closed residue (b) of `experiment:a00-1b9a8e7e-profile-sync`: a `write.py`
edit whose node declares a `profile_ref` that will be refused is now
all-or-nothing. The parent experiment recorded the open defect verbatim —
"on the refused write.py path the NODE body was already updated before the
refusal (grep smuggled==1) -- the artifact is refused, the graph write lands,
rc=2".

### Pre-fix state (inherited, measured by the parent)

`submit()` ordered `node_writer.update_node` BEFORE `profile_sync.sync_node`.
`sync_node` then raised `Refused` -> `EditError`, so `write.py` exited rc=2
while the node body had already advanced and the artifact stayed stale. That
is a partial write: graph and projection disagree, and the failure reports a
reason that arrived too late to prevent it.

### Built bytes

EDIT `extensions/agi/bin/write.py`, +26 lines (no removals):
- In `submit()`, immediately after the existing `link_ref`/`payload_ref`
  outside-repo guard and BEFORE any write, a pre-flight resolves the
  *effective* `profile_ref` — `set_fm["profile_ref"]` when this edit sets it,
  else the value already on disk — and calls `profile_sync.artifact_path`,
  which raises `Refused` for a ref that escapes the repo root, resolves under
  `.agi/nodes/`, or names a directory. The refusal re-raises as `EditError`
  before `node_writer.update_node`, so nothing is written.
- NEW helper `_disk_fm(root, node_id, field)` reads one frontmatter field
  read-only. This is validation only; the projection itself still runs AFTER
  the payload write, preserving residue 4 (a failed payload must not advance
  the projection). No new file write — the `write.py` ast guard stays green.

Test file (separate): `extensions/agi/tests/test_profile_sync.py`, +3 cases
(parametrized over the two refusal reasons + directory target + same-edit
`set profile_ref`).

## Evidence

Targeted suite, after the change:
```
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py extensions/agi/tests/test_write.py -q
135 passed   # pre-change baseline, both files
$ python3 -m pytest extensions/agi/tests/test_profile_sync.py -q
22 passed    # includes the 3 new residue-(b) cases
```

Probes on the REAL built engine, in a scratch repo with its own
`.agi/config.json` (session dir `iter-DH.159/a00-2b1e2b82`), writing a body
via `write.py hypothesis:h1 'note CHANGED'`:

```
[outside]   ref '../escape.md'        rc=2 body_advanced=0
            ERR: profile projection refused: ... resolves outside the repo root
[nodesref]  ref '.agi/nodes/evil.md'  rc=2 body_advanced=0
            ERR: profile projection refused: ... resolves under .agi/nodes/
[dirtarget] ref 'profile_dir' (dir)   rc=2 body_advanced=0
            ERR: profile projection refused: ... resolves to a directory, not a file
[good]      ref 'profile/out.md'      rc=0 body_advanced=1
            artifact == ORIGINAL BODY + '## Agent Notes' + CHANGED
[noref]     no profile_ref            rc=0 body_advanced=1, no profile dir created
```

`escape.md` and `.agi/nodes/evil.md` were never created. `--check` regression
on the good repo: mutate artifact -> `DRIFT ... rc=1`, artifact left as
`mutated` (--check never writes).

Production lines measured with `git diff --numstat -- extensions/agi/bin/write.py`:
`26 0 extensions/agi/bin/write.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue (b) of the parent experiment, chosen over the alternative "record the
node write as landed + a named repair". The pre-flight is 26 lines and closes
the split at its source; the repair-record variant would need a durable
repair journal for one failure mode and still leaves a reader to reconcile two
states. The parent's residue 4 (payload before projection) is preserved because
the pre-flight only *validates* a path; it never writes. A same-edit
`set profile_ref ../escape.md` is pre-flighted too, so the bad field cannot
land either. Scope kept deliberately to `Refused`: a post-`update_node`
failure of `sync_node` for a non-refusal reason (e.g. an unwritable artifact
directory) is a different residue and is not claimed here.
<!-- THOUGHT:END -->
