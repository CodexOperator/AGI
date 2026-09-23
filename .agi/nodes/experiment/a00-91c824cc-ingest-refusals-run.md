---
id: experiment:a00-91c824cc-ingest-refusals-run
mint_id: 0b58026a98864dfabc83f878dc6064ea
type: experiment
parents:
  - hypothesis:a00-91c824cc-85701d
next_edges: []
edited_by: a00-91c824cc
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 356e983c6de1c8b8
season: 2
thought_session: iter-DH.75
title: "Run: ingest refuses missing artifact and non-object rows; both files claimed"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-91c824cc-ingest-refusals-run

## Experiment

Corrective round for `mur-g7-32-1-dh-68-8b441cbd8-2-lean`, base tip
`8b441cbd8`. Three residues on `goal:g7.32.1`. All commands run in this
worktree; the graph root was a throwaway temp dir for the refusal probes and
the live worktree for the coverage probes.

### Residue 1 — unclaimed ingest files

Before (`python3 extensions/agi/bin/grid_coverage_check.py --verbose`):

```
  MISSING: extensions/agi/bin/ingest_grok_session.py
  MISSING: extensions/agi/tests/test_ingest_grok_session.py
grid coverage: 211 tracked code file(s) OUTSIDE the grid
```

Minted ONLY the two files via `level3.mint_missing(..., mvp_map=[('extensions/agi/',
'mvp:grok-ingest-refusals-a00-91c824cc')])`; the dry-run printed exactly two
`DRY-RUN: would mint ...` lines and the real run printed:

```
MINTED: build:bin-ingest-grok-session (...ingest_grok_session.py, parent mvp:grok-ingest-refusals-a00-91c824cc)
MINTED: build:tests-test-ingest-grok-session (...test_ingest_grok_session.py, parent mvp:grok-ingest-refusals-a00-91c824cc)
```

After: `grid coverage: 209 tracked code file(s) OUTSIDE the grid` — neither
ingest file appears, and `links.py schema` does not newly flag either (the one
remaining `build` flag is the pre-existing `.agi/nodes/build/failures.py.md`).

### Residue 2 — missing artifact

Before: `FileNotFoundError` traceback, rc=1. After:

```
$ python3 extensions/agi/bin/ingest_grok_session.py /tmp/does-not-exist.jsonl --root /tmp --actor p --thought-session s
refused: no such artifact: /tmp/does-not-exist.jsonl
rc=2
```

### Residue 3 — non-object JSONL row

Before: `AttributeError: 'list' object has no attribute 'get'`, rc=1. After:

```
$ printf '[1,2,3]\n' > /tmp/nonobj.jsonl && python3 extensions/agi/bin/ingest_grok_session.py /tmp/nonobj.jsonl --root /tmp --actor p --thought-session s
refused: row is not a JSON object
rc=2
$ printf 'null\n' > /tmp/nullrow.jsonl && ... # same refusal
```

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q
8 passed, 3 warnings in 4.13s
```

6 pre-existing tests + 2 new committed tests
(`test_missing_artifact_refused_writes_nothing`,
`test_nonobject_row_refused_writes_nothing`, the latter covering list, `null`,
string and number rows). Production file held at 80 lines (`git diff
--numstat` on the production path: `6 6`, net zero) against the 40-line
ceiling. No residue left open.

## Evidence

Raw output, screenshots, logs.
