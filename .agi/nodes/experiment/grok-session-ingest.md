---
id: experiment:grok-session-ingest
mint_id: 04ba56fbe9174dbc8a873119e6468b0b
type: experiment
parents:
  - hypothesis:a00-8884b651-613fda
next_edges: []
edited_by: a00-8884b651
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 79
profile: balanced
role: kid
scaffold_hash: c6b0d8264c6ed0e0
season: 2
title: "Grok session ingest: first ingest path, idempotent on re-run"
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-session-ingest

## Experiment

Built one ingest script, one test file, one fixture, and activated the
`agent_session` schema.

**Files**

| file | role |
|---|---|
| `extensions/agi/bin/ingest_grok_session.py` | ingest CLI (79 lines) |
| `extensions/agi/tests/test_ingest_grok_session.py` | pytest, 5 tests |
| `extensions/agi/tests/fixtures/grok_session_sample.jsonl` | 1 header + 4 turns |
| `.agi/context/schemas/[agent_session].md` | activated schema |

**Fixture shape** (JSONL, line 1 = header):

```
{"session_id": "grok-9f3a2b7c-2026-09-22", "agent_id": "grok-bot",
 "started_at": "...", "thought_session": "owner-ask-2026-09-21"}
{"role": "user", "content": "...", "timestamp": "..."}
```

**Wire.** `ingest()` calls `node_writer.write_node(root, "agent_session",
slug, parents=["goal:g7.32.1"], extra_fm={...}, body=...)`. The slug is
deterministic (`grok-<sanitized session_id>-<sha1[:8]>`), and `write_node` is
called with its default `on_exists=SKIP`, so the second ingest of the same
artifact reuses the node and its `mint_id`. No frontmatter is written by hand.

**Schema activation.** `.agi/context/schemas/[agent_session].md` is new;
the unbracketed `agent_session.md` design doc stays inactive. `required`
is `[id, type, mint_id, title, tags]`; `spawn: allowed_parents: [goal],
min_parents: 1, max_parents: 2`. The design doc's `run_id`,
`source_files`, `input_shape` were deliberately NOT copied — no session
artifact carries them.

## Evidence

Ingest against the live graph (first run):

```
$ python3 extensions/agi/bin/ingest_grok_session.py \
    --fixture extensions/agi/tests/fixtures/grok_session_sample.jsonl
SPAWN-GATE APPROVED agent_session:grok-grok-9f3a2b7c-2026-09-22-8b292f2c ...
agent_session:grok-grok-9f3a2b7c-2026-09-22-8b292f2c
```

Minted node — `.agi/nodes/agent_session/grok-grok-9f3a2b7c-2026-09-22-8b292f2c.md`:

```
id: agent_session:grok-grok-9f3a2b7c-2026-09-22-8b292f2c
mint_id: 858b955991fc49679d6ba78f21f433b4
type: agent_session
parents:
  - goal:g7.32.1
agent_id: grok-bot
edited_by: grok-bot
session_id: grok-9f3a2b7c-2026-09-22
thought_session: owner-ask-2026-09-21
tags: [agent-session, grok, session-ingest]
turn_count: 4
```

Second run of the same fixture: same node id printed, `ls` shows ONE file,
`grep mint_id` shows ONE `mint_id` (858b955991fc49679d6ba78f21f433b4).

Refusals, all exit 2, no node written:

```
$ ... --fixture bad_header.jsonl
refused: missing-session_id: header carries no usable 'session_id'
$ ... --fixture bad_turn.jsonl
refused: bad-turn-json line 2: Expecting value: line 1 column 1 (char 0)
$ ... --fixture empty.jsonl
refused: empty-fixture: ... empty.jsonl has no JSONL records
```

Tests:

```
$ python3 -m pytest extensions/agi/tests/test_ingest_grok_session.py -q
5 passed
$ python3 -m pytest extensions/agi/tests/test_spawn_gate.py \
    extensions/agi/tests/test_grok_bot_adapter.py -q
96 passed
$ python3 -m pytest extensions/agi/tests/schema_registry/test_schema_files.py \
    extensions/agi/tests/schema_registry/test_brackets.py \
    extensions/agi/tests/test_verification.py -q
70 passed
```

One test spies `node_writer.write_node` and asserts the ingest call site
reaches it — the node file existing is not by itself proof of the wire.

## Production lines

`extensions/agi/bin/ingest_grok_session.py` = **79 lines** (ceiling 40, under
the 2x=80 rebrief threshold). `git diff --numstat` reports nothing for it
because the file is new and untracked in a shared worktree; the physical count
is recorded here rather than the numstat zero.
