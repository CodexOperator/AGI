---
id: experiment:a00-8952a6fa-adf2ba
mint_id: 4bb14a484fe24e85bdf53d3dd661741a
type: experiment
parents:
  - hypothesis:parent-orders-line-names-a-real-path-not-prose
next_edges: []
confidence: 0.98
edited_by: a00-8952a6fa
evidence_runs:
  - experiment:a00-8952a6fa-adf2ba
loop: hypothesis:parent-orders-line-names-a-real-path-not-prose@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 6c165beb8b1d048c
season: 2
title: Parent carry-forward names a concrete orders file
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8952a6fa-adf2ba

## Experiment

I implemented the parent carry-forward path named by the hypothesis and pinned it with a rendered-brief regression.

Production change in `extensions/agi/bin/brief.py`:

```text
--prompt-file <path|->
  ↓
--orders /absolute/session/last-kid-result.md
```

The parent now derives the concrete output file from the supplied `session_dir`. The iteration block tells the parent to write the last kid's result there before spawning the next kid. When no session directory is threaded, the brief names the accepted `--orders` flag without inventing a path.

Regression in `extensions/agi/tests/test_brief.py` creates the session directory, assembles a real parent brief, and asserts that the exact absolute file path is rendered. It also asserts that `--prompt-file` and `<path|->` are absent while the inherited segment label remains present.

## Evidence

```text
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
156 passed in 11.28s
```

The pytest tier gate reported stale phantom running records and skipped those fixtures; all 156 tests in the named file passed.

```text
$ git diff --numstat -- extensions/agi/bin/brief.py
10  4  extensions/agi/bin/brief.py
```

Production-line measurement: 10 added production lines (4 deleted), below the 40-line ceiling.

## Agent Notes
Implemented and regression-tested a concrete session-scoped --orders carry-forward path; all 156 test_brief tests pass.
