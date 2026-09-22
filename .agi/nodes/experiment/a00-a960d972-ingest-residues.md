---
id: experiment:a00-a960d972-ingest-residues
mint_id: dcc3051aab8645389e193292813237fd
type: experiment
parents:
  - hypothesis:a00-a960d972-431933
next_edges: []
edited_by: a00-a960d972
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 6a4d1ad432a86db1
season: 2
testable_claim: "Two conjuncts: named refusal for every malformed shape, and scope-check rc=1 unowned / rc=0 owned for the residue"
title: "DT.73 ingest residues: named refusals plus owner-scoped residue commit"
town: core
---
<!-- BODY:BEGIN -->
## Experiment

Close the two named residues on `goal:g7.32.1` (Grok session ingest) with
committed tests and a landed artifact. The testable claim has TWO conjuncts,
both of which must hold on the built bytes:

1. **No malformed shape raises a traceback.** Every non-dict JSONL record, and
   every wrong-shaped `message` / `content` / content block, exits 2 with a
   NAMED `INGEST refuse <reason>` on stderr — never `AttributeError`, never
   exit 1, never a silent drop.
2. **The real-corpus residue node is committable by the round that owns it.**
   Ingesting the real session against the real graph root creates
   `.agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md`, and
   the SAME `_round_scope_ok` predicate the hook and `done` use
   (`cli.py scope-check`) accepts that path exactly when the round names it in
   `--own`.

### Conjunct 1 — the fix

`read_session` guarded every shape before `.get`:

- a parsed line that is not a `dict` -> `malformed-record: line N: expected JSON object, got <type>`
- `message` not an object -> `malformed-message: line N: message is not an object`
- `content` not a list -> `malformed-content: line N: content is not a list`
- a content block not an object -> `malformed-content: line N: content block is not an object`

Records are kept as `(lineno, rec)` pairs so the reason carries the real source
line number even though blank lines are skipped. `main` already turned every
`ValueError` into `INGEST refuse <msg>` + return 2, so nothing there changed.
Production: 40 added / 10 deleted lines in
`extensions/agi/bin/ingest_session.py` — at the 40-line ceiling.

### Conjunct 1 evidence — malformed matrix (before and after)

Before the fix, each of the five shapes exited 1 with an `AttributeError`
traceback (`'list' object has no attribute 'get'`, `'int' object ...`,
`'str' object ...` x3). After:

```
s1 `[1,2,3]`                      rc=2  INGEST refuse malformed-record: line 1: expected JSON object, got list
s2 `42`                           rc=2  INGEST refuse malformed-record: line 1: expected JSON object, got int
s3 message:"oops"                 rc=2  INGEST refuse malformed-message: line 2: message is not an object
s4 message.content:["oops"]       rc=2  INGEST refuse malformed-content: line 2: content block is not an object
s5 message.content:{"a":1}        rc=2  INGEST refuse malformed-content: line 2: content is not a list
```

Happy path unchanged: a session with no `message` records mints
`INGEST ok doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262` rc=0; an
empty `content` list and a text block with no `text` key both ingest.

Tests committed in `extensions/agi/tests/test_ingest_session.py`: a
5-case parametrized matrix (`test_non_dict_shape_is_refused_by_name_not_traceback`)
asserting rc==2, `INGEST refuse`, the named reason, no `Traceback`, and zero
nodes — plus `test_valid_session_with_no_message_records_still_ingests`.
`python3 -m pytest extensions/agi/tests/test_ingest_session.py -q` -> **15 passed**.
With `test_node_writer.py` -> **121 passed**.

### Conjunct 2 evidence — the residue lands when owned

Real corpus, real graph root (no `--out-root`):

```
$ python3 extensions/agi/bin/ingest_session.py \
    sessions/2026-04-30T06-24-27-474Z_019ddd0f-6751-75bc-a374-6c0fe036e262.jsonl
INGEST ok doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262
rc=0   (file present at .agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md)
```

Same predicate the hook and `done` use:

```
$ printf '%s\0' .agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md \
    | python3 extensions/agi/bin/cli.py scope-check --agent-id a00-9dd3937b
rc=1                       # WITHOUT owning — the residue today

$ ... --own .agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md
rc=0                       # WITH owning
```

The residue file is left in place (not deleted). **Hand-off to the parent:**
`done` must carry
`--owns doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262`
so the file lands on the tip. The doc node id to own is exactly
`doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262`.

### Why the ingest does NOT write under a round-owned basename

Putting the agent id into the filename would put it inside the idempotence key:
the SAME session ingested by two different agents would mint two nodes. That
breaks the injectivity / no-silent-drop property the prior round proved
(`hypothesis:a00-a317e857-9dba03`), and it forks one session per ingesting
agent. The correct mechanism is ownership at commit time (`--owns`), not
identity at write time — the path stays a pure function of the session id, and
the round that created it names it.

### OPTIONAL, not taken

`ingest_session.py` already exposes `--parent` (default `goal:g7.32.1`).
Making it mandatory would break existing callers/tests for no measured gain, so
it is left as is.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.73 corrective round on the DT.66 residue. The prior round's fix addressed
slug injectivity but left `read_session` assuming every JSON shape was a dict:
five distinct malformed inputs all died on `.get` with exit 1. This version
guards each nesting level and raises a named reason, and it proves the
real-corpus node is committable only because the round can own it — I chose
commit-time ownership over baking the agent id into the slug because the slug
is the idempotence key and must stay a pure function of the session id.
<!-- THOUGHT:END -->
