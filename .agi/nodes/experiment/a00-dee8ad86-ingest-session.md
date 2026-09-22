---
id: experiment:a00-dee8ad86-ingest-session
mint_id: e58e716f1e944062a506f48d90e4aae3
type: experiment
parents:
  - hypothesis:a00-dee8ad86-1ab674
next_edges: []
edited_by: a00-dee8ad86
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 6a3aaa40259f2e39
season: 2
tags:
  - grok-session
  - ingest
testable_claim: ingest_session.py mints exactly one node per session id, re-ingest forks no new mint, malformed input exits non-zero with a named reason
title: One CLI mints one graph node per Grok session, idempotent and refusing by name
town: core
---
# experiment:a00-dee8ad86-ingest-session

## Experiment

Target `goal:g7.32.1` via `hypothesis:a00-dee8ad86-1ab674`. Built one CLI,
`extensions/agi/bin/ingest_session.py` (79 production lines), plus
`extensions/agi/tests/test_ingest_session.py`. A live session from the repo-root
`sessions/` corpus was copied to
`.agi/sessions/iter-DT.66/a00-dee8ad86/fixture.jsonl` as the fixture.

### Conjunct 1 — given a fixture, ≥1 new node id on stdout + a file under nodes/

Throwaway root (`<scratch>/graph`, schemas copied in):

```
$ python3 extensions/agi/bin/ingest_session.py \
    .agi/sessions/iter-DT.66/a00-dee8ad86/fixture.jsonl --out-root <scratch>/graph
INGEST ok doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262

$ find <scratch>/graph/nodes -name '*.md'
<scratch>/graph/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md
```

### Conjunct 2 — re-ingest does not fork duplicate mint ids

```
$ python3 extensions/agi/bin/ingest_session.py ... --out-root <scratch>/graph
INGEST skip doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262

$ find <scratch>/graph/nodes -name '*.md' | wc -l
1
```

Against the REAL worktree graph root, so "a file under `.agi/nodes/`" is met
literally:

```
$ python3 extensions/agi/bin/ingest_session.py ... --out-root .agi
INGEST ok doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262

$ test -f .agi/nodes/doc/grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262.md \
    && echo FILE-EXISTS
FILE-EXISTS

$ python3 extensions/agi/bin/ingest_session.py ... --out-root .agi
INGEST skip doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262
```

The minted frontmatter (first lines of the file) carries the source session's
identity and provenance:

```
id: doc:grok-session-019ddd0f-6751-75bc-a374-6c0fe036e262
mint_id: 853a9c0b21cb423fa5bb6ab6a2646002
type: doc
parents:
  - goal:g7.32.1
edited_by: ingest_session.py
source_session: 019ddd0f-6751-75bc-a374-6c0fe036e262
thought_session: .agi/sessions/iter-DT.66/a00-dee8ad86/fixture.jsonl
town: core
```

### Conjunct 3 — malformed input refuses by NAME, non-zero

```
$ : > <scratch>/empty.jsonl
$ python3 extensions/agi/bin/ingest_session.py <scratch>/empty.jsonl --out-root <scratch>/graph
INGEST refuse no-session-record: no {"type":"session"} line
$ echo $?
2
```

A JSONL file whose lines parse but carry no `{"type":"session"}` record takes
the same branch (a unit test covers it); a non-JSON line refuses as
`malformed-jsonl: line N: ...`.

### Mechanism (why this version and not another)

- **Idempotence key = the file itself.** The slug is a deterministic function
  of the session id (`grok-session-<sanitized-id>`), and the mint goes through
  `node_writer.write_node(..., on_exists=SKIP)`. Re-run hits the existing path
  and returns `SKIPPED` with the SAME node id — no ledger that can drift from
  the node tree, no second mint.
- **Mint through the one writer**, not a hand-written file: schema gate,
  `mint_id`, `scaffold_hash`, `town`, and the write-log all apply.
- **Type `doc`, parent `goal:g7.32.1`.** `[experiment].md` removed `goal` from
  `allowed_parents` (`goal:s22`), so an experiment under the goal would be
  refused by the real gate; `doc` permits a `goal` parent and is the honest
  shape for ingested residue. `--parent` is a flag, so another call site can
  point at the seat's live goal.
- **`announce=False`** on the mint keeps stdout to exactly the one INGEST
  line, so a caller can parse it.

### Repo test run

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
....                                                                     [100%]
4 passed in 7.35s
```

## Evidence

Raw stdout of fresh / re-ingest / refusal runs above, plus `test -f` of the
node file and the minted frontmatter. Mechanism and the falsifier are in the
body, not in prose about it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this node; nothing preceded it. Chose the file-exists
idempotence key over a side ledger precisely because the falsifier's second
conjunct is about the mint, and `write_node` already refuses to re-mint an
existing slug — reusing that makes the property structural rather than
maintained. Chose `doc` over `experiment` because the gate forbids a goal
parent for experiments since goal:s22, and the brief's default parent is the
goal itself.
<!-- THOUGHT:END -->
