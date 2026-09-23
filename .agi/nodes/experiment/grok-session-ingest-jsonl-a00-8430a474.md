---
id: experiment:grok-session-ingest-jsonl-a00-8430a474
mint_id: 3c34b51703d04e4faa52e01f12164de1
type: experiment
parents:
  - hypothesis:a00-8430a474-c9d617
next_edges: []
edited_by: a00-8430a474
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 5007efa7ec3fbb02
season: 2
thought_session: iter-DT.101
title: Grok JSONL session ingest — falsifier run, 80 production lines
town: core
---
## Experiment

Built the canonical ingest pipe on this tip against the **JSONL** contract
(chosen because the real Grok Bot artifacts are JSONL — first line
`{"session_id": ...}`, then `{role, content, ts}` turns; the single-JSON-object
contract in the other worktree does not match the shipped artifacts).

Files landed:
- `extensions/agi/bin/ingest_grok_session.py` (80 lines)
- `extensions/agi/tests/test_ingest_grok_session.py` + fixtures

The goal's own falsifier was run end-to-end against a throwaway graph root
(`<scratch>/falsifier/.agi/` containing the live schemas and a copy of
`goal:g7.32.1.md`), never the live graph.

### Run 1 — fresh fixture -> id + file

```
$ python3 extensions/agi/bin/ingest_grok_session.py <scratch>/grok-session-sample.jsonl \
    --root <scratch>/falsifier --actor a00-8430a474 --thought-session iter-DT.101
hypothesis:grok-2026-09-22-abc123
node files:
.../falsifier/.agi/nodes/goal/g7.32.1.md
.../falsifier/.agi/nodes/hypothesis/grok-2026-09-22-abc123.md
mint_id after run 1:
mint_id: 8c51bcff86e94374bafe33300f29e26b
```

### Run 2 — SAME fixture -> same id, no second file, no second mint_id

```
$ python3 extensions/agi/bin/ingest_grok_session.py <scratch>/grok-session-sample.jsonl \
    --root <scratch>/falsifier --actor a00-8430a474 --thought-session iter-DT.101
hypothesis:grok-2026-09-22-abc123
node count:
2
mint_id after run 2:
mint_id: 8c51bcff86e94374bafe33300f29e26b
```

### Run 3 — malformed artifact -> refused BY NAME, nothing written

```
$ python3 extensions/agi/bin/ingest_grok_session.py <scratch>/malformed.jsonl \
    --root <scratch>/falsifier --actor a00-8430a474 --thought-session iter-DT.101
refused: unparseable JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
exit=2
node count:
2
```

## Evidence

Falsifier stdout above is real, captured to `<scratch>/falsifier-run.log`.
Test suite: `python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q`
-> **6 passed** (mint+provenance, re-ingest no second mint, malformed refused,
empty refused, env provenance, missing provenance refused).

### Measurement

Production lines added: 80 (`wc -l extensions/agi/bin/ingest_grok_session.py`);
line ceiling 40. 80 is exactly 2x the ceiling, not above it — no re-brief
required. The test file is excluded from the production measurement.
