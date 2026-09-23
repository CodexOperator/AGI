---
id: experiment:ingest-key-idempotence
mint_id: f507251d934f4ac4b7f04b4ce25978a6
type: experiment
parents:
  - hypothesis:a00-d0b6a642-f6ee59
next_edges: []
edited_by: a00-d0b6a642
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0e21b6002f70218e
season: 2
title: Ingest key idempotence
town: core
---
<!-- BODY:BEGIN -->
# experiment:ingest-key-idempotence

## Experiment

Offline probe under the kid's scratch dir (never the live graph). A throwaway
project root (`probe-root/.agi`, `nodes/` empty, `context/` symlinked to the
real schemas, `config.json` copied) receives two fixture artifacts in the
session-artifact shape:

```json
{"harness": "grok-bot", "session_id": "grok-sess-2026-09-22-aaaa",
 "path": "fixtures/grok/a.json", "summary": "director helper round DH.147"}
```

`probe_ingest.py` builds `key = sha256(f"{harness}:{session_id}")[:16]`, scans
`nodes/**/*.md` frontmatter for `ingest_key == key`, and only on a miss calls
`node_writer.write_node(root, "hypothesis", f"grok-session-{key}",
parents=["goal:g7.32.1"], extra_fm={"ingest_key": key, ...})` — the same
ledger `cli.py done` writes through, so the test exercises the real writer,
not a hand-rolled one. Two runs over the same two fixtures:

```
$ python3 probe_ingest.py probe-root/.agi fixture_a.json fixture_b.json
--- run 1
  grok-sess-20 -> hypothesis:grok-session-afb51c84760579e3 [written]
  grok-sess-20 -> hypothesis:grok-session-bf1dc429e18abe77 [written]
--- run 2
  grok-sess-20 -> hypothesis:grok-session-afb51c84760579e3 [exists]
  grok-sess-20 -> hypothesis:grok-session-bf1dc429e18abe77 [exists]
node files = 2: ['grok-session-afb51c84760579e3.md', 'grok-session-bf1dc429e18abe77.md']
```

Falsifier (1) holds: each artifact produced a node id on stdout and a file under
`nodes/`. Falsifier (2) holds: run 2 returned the same ids and the node-file
count stayed at 2 — no fork. Two distinct `session_id`s produced two distinct
keys, so the key does not collapse sessions together.

## Evidence

Raw output above. Probe source is inlined in the hypothesis's evidence chain at
`.agi/sessions/iter-DH.148/a00-d0b6a642/probe_ingest.py` (scratch; the command
and both fixtures are reproduced verbatim above, so the result is re-runnable).

**Boundary of the claim:** the fixture is synthetic. There is no Grok transcript
on this box to parse, so this proves the *ingest + idempotence mechanism*, not
Grok transcript field mapping. The key is (harness, session_id) only — a
checkpoint that later completes keeps its key and its first-ingest content is
frozen; an update/supersession path is out of scope here and is the obvious
child experiment. Writes went to a throwaway root, so the live node count is
unaffected by this experiment (it adds only this node and the hypothesis).
