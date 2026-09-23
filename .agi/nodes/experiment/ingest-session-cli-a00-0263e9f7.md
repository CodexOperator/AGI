---
id: experiment:ingest-session-cli-a00-0263e9f7
mint_id: 9a9e025619854dc19caed104c37e44b3
type: experiment
parents:
  - hypothesis:a00-0263e9f7-7b89ff
next_edges: []
edited_by: a00-0263e9f7
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 65
profile: balanced
role: kid
scaffold_hash: d0866bbe5d5aa979
season: 2
thought_session: dh148-a00-0263e9f7
title: Production session-ingest CLI
town: core
---
<!-- BODY:BEGIN -->
# experiment:ingest-session-cli-a00-0263e9f7

## Experiment

Built the production CLI `extensions/agi/bin/ingest_session.py` (65 lines) and
its hermetic test `extensions/agi/tests/test_ingest_session.py` (6 tests).
The mechanism is reproduced byte-for-byte from `hypothesis:a00-d0b6a642-f6ee59`:
`key_of(a) = sha256(f"{a['harness']}:{a['session_id']}").hexdigest()[:16]`,
`find_existing()` scans `root/nodes/**/*.md` frontmatter for `ingest_key == key`
before writing, and a miss calls `node_writer.write_node(root, "hypothesis",
f"grok-session-{key}", parents=["goal:g7.32.1"], ...)` — the real ledger.

Three parent-run negative probes closed:

- **wire** — the CLI now exists in the production tree; on the throwaway root
  it prints the node id on stdout and a file appears under `nodes/`.
- **gate** — a missing `session_id` produces
  `REFUSED <path>: missing required field(s): session_id` on stderr, exit 2,
  no traceback, no file. Unreadable JSON is refused the same way.
- **auth** — `--edited-by` / `--thought-session` are written into the minted
  node's frontmatter (`edited_by: ingest_session` by default).

The test never touches the live graph: every run passes `--root <tmp>/root`.
A live run over the real `.agi` writes the same bytes to the live root; the
only difference is the `--root` value.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
......                                                                   [100%]
6 passed in 33.70s
```

Covered: first ingest writes exactly one node + id on stdout; re-run prints
`[exists]` with the same id and the file count stays 1; the node carries
`parents == ["goal:g7.32.1"]` plus provenance; flags override provenance;
malformed is refused by name with no file; two distinct sessions do not
collide (2 files).

The production-line overage (65 > 40, under the 2× stop of 80) is recorded in
this node's frontmatter as `production_lines` / `line_ceiling`.
