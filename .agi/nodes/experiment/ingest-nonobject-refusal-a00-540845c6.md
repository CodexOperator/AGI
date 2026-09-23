---
id: experiment:ingest-nonobject-refusal-a00-540845c6
mint_id: 98cd3af1fef74d01b166abf8ea480a6a
type: experiment
parents:
  - hypothesis:a00-540845c6-7283f0
next_edges: []
edited_by: a00-540845c6
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 8
profile: balanced
role: kid
season: 2
thought_session: dh148-a00-540845c6
title: Non-object artifact refusal built and probed
town: core
---
<!-- BODY:BEGIN -->
# experiment:ingest-nonobject-refusal-a00-540845c6

## Experiment

Close the parent probe that falsified `hypothesis:a00-0263e9f7-7b89ff`:
a readable-JSON-but-not-an-object artifact (`[{"harness":"grok-bot",
"session_id":"s-2"}]`) reached `art.get` and raised
`AttributeError: 'list' object has no attribute 'get'` instead of a named
refusal. The production CLI `extensions/agi/bin/ingest_session.py` now refuses
any non-object by name before touching `.get`, and `--root` is refused unless
it has an existing `nodes/` dir (or a resolvable config) — an empty
`.agi`-named directory no longer gets a node written into it.

The fix and the array test were already present uncommitted in this worktree
when the round opened; this run added the missing `null`/scalar coverage,
tightened the root guard from "dir named `.agi`" to "has `nodes/`", and proved
the whole branch on the built bytes.

## Evidence

Built bytes, throwaway graph with `nodes/` pre-created, artifact written per
shape:

```
$ python3 extensions/agi/bin/ingest_session.py --root <graph> nonobject.json
REFUSED nonobject.json: expected a JSON object, got list      # [..]  exit=2
REFUSED nonobject.json: expected a JSON object, got NoneType  # null  exit=2
REFUSED nonobject.json: expected a JSON object, got int       # 42    exit=2
REFUSED nonobject.json: expected a JSON object, got str       # "x"   exit=2
nodes written: 0
$ python3 extensions/agi/bin/ingest_session.py --root <empty>/.agi arr.json
REFUSED --root <empty>/.agi: not a graph root (no nodes/ dir and no config.json)
exit=2 ; nodes written: 0
```

Repo suite (the changed test file, named, not the bare directory):

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
............                                                             [100%]
12 passed in 76.39s
```

12 tests = the 6 inherited ones (wire, idempotent re-run, provenance, flags,
missing-field refusal, non-graph root) plus parametrized non-object refusals
for `list` / `NoneType` / `int` / `str` and the empty-`.agi` root refusal.
Every refusal asserts `REFUSED` on stderr, the type/filename named,
`Traceback` absent and no node file.

Production diff measured with `git diff --numstat`:
`8  0  extensions/agi/bin/ingest_session.py` (read-only; nothing staged).
8 < 40 ceiling, no re-brief owed.

## Boundary

The key contract (`key_of`, `ingest_key` frontmatter) is untouched.
`null` and scalar JSON are refused at the same `isinstance(art, dict)` branch
the array is; no separate code path. The experiment artifact is synthetic — no
Grok transcript on this box.
