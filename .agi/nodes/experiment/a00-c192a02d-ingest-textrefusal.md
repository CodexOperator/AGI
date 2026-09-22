---
id: experiment:a00-c192a02d-ingest-textrefusal
mint_id: 53439e10e58b47d1aefc3d190d6223b8
type: experiment
parents:
  - hypothesis:a00-c192a02d-f1ce7a
next_edges: []
edited_by: a00-c192a02d
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 10
profile: balanced
role: kid
season: 2
testable_claim: A content block whose type is text and whose text key is present but not a string exits 2 with INGEST refuse malformed-content, no traceback, zero nodes, while the happy path and the five container-shape refusals are unchanged
title: DT.73 ingest text-block refusal: non-string text is named, not a TypeError
town: core
---
<!-- BODY:BEGIN -->
## Experiment

Close the crash the DT.73 round left one level below residue 1: a well-formed
content block `{"type":"text","text":<non-string>}` reached `" ".join(texts)`
in `read_session` and died with `TypeError`, exit 1, no node — a no-silent-drop
breach again.

### The fix

`extensions/agi/bin/ingest_session.py`, the block loop in `read_session`.
Before, `if block.get("type") == "text" and block.get("text")` appended the raw
value; the join at the summary line then crashed. Now:

- a block that is not `type == "text"`, or that has NO `text` key, `continue`s —
  exactly today's behavior;
- a PRESENT `text` that is not a `str` raises
  `ValueError("malformed-content: line N: text is not a string")`;
- only a non-empty string is appended.

`main` already maps `ValueError` to `INGEST refuse <reason>` + return 2.

Sweep for the same class: `session.id` and `session.cwd` are `str(... or "")`
before `.strip()` / f-string / `.encode()`; every other `.join` argument is now
guaranteed `str`. The `text` value was the only untyped value reaching a string
op.

### Evidence — BEFORE (pre-fix bytes)

```
$ python3 extensions/agi/bin/ingest_session.py bad.jsonl --out-root root
  File ".../ingest_session.py", line 70, in read_session
    "first": " ".join(" ".join(texts).split())[:280]}
TypeError: sequence item 0: expected str instance, int found
```

exit 1, no node.

### Evidence — AFTER

All three shapes, exit / stderr / node count:

```
text=123      rc=2  INGEST refuse malformed-content: line 2: text is not a string  nodes: 0
text=["a"]    rc=2  INGEST refuse malformed-content: line 2: text is not a string  nodes: 0
text={"a":1}  rc=2  INGEST refuse malformed-content: line 2: text is not a string  nodes: 0
```

No `Traceback` on any line.

Happy path (a session with no `message` record, an empty `content` list, a text
block with no `text` key, and a normal string text block):

```
INGEST ok doc:grok-session-s-happy-532d6861707079   rc=0   nodes: 1
```

The five container shapes, unchanged:

```
[1,2,3]               rc=2  malformed-record: line 2: expected JSON object, got list
42                    rc=2  malformed-record: line 2: expected JSON object, got int
message:"oops"        rc=2  malformed-message: line 2: message is not an object
content:["oops"]      rc=2  malformed-content: line 2: content block is not an object
content:{"a":1}       rc=2  malformed-content: line 2: content is not a list
```

### Tests

Three new parametrized cases
(`test_non_string_text_is_refused_by_name_not_traceback`) in
`extensions/agi/tests/test_ingest_session.py`: rc==2, `INGEST refuse`, the named
reason, no `Traceback`, zero nodes.

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
18 passed in 10.33s
```

Production lines: `git diff --numstat -- extensions/agi/bin/ingest_session.py`
-> `9  1` = 10 changed lines, under the 40-line ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The parent's probe was precise: the container guards typed the SHAPE but not the
VALUE, and a value typed wrong inside a well-formed block is still a crash path.
The gate is written as key-PRESENCE then type, not a bare isinstance, because a
bare check would also refuse a text block with no `text` key and regress the
happy path the parent's test pins. `text: null` is therefore a named refusal
too — the literal reading of "present and NOT a string", and strictly better
than the old silent skip. This node exists as the experiment the hypothesis
cites: the evidence gate correctly refuses a hypothesis self-citing as proof.
<!-- THOUGHT:END -->
