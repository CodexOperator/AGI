---
id: experiment:a00-d12b0f11-235864
mint_id: 020559fb05114b34bfdf1196d3ac8e9e
type: experiment
parents:
  - hypothesis:l3w0-test-skips
next_edges: []
confidence: 0.95
edited_by: ubuntu
evidence_runs:
  - experiment:a00-d12b0f11-235864
loop: hypothesis:l3w0-test-skips@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 06592eae8c73ab64
season: 1
title: A00 d12b0f11 235864
verdict: proved
---
# experiment:a00-d12b0f11-235864

## Experiment

Repointed the three stale post-g11 test skips at the `.agi` layout and added a
real argparse `--help` to the five CLI scripts that lacked one; left
`node_writer.py`'s library skip in place.

**Three stale skips repaired (files edited in place):**

1. `extensions/agi/tests/test_grid.py` — `test_sanitize_real_agi_tree_corpus_round_trips_distinctly`
   looked for `Path.parents[4] / "agi-tree" / "nodes"` (two-repo era, never
   exists now) and skipped. Repointed at the engine repo's own
   `.agi/nodes` **and** `.agi/nodes/deprecated` (`engine_root = parents[3]`),
   so the real live corpus (1427 live + 189 deprecated node files) is swept.
2. `extensions/agi/tests/test_spawn_gate.py` — `test_shipped_schemas_load_without_error`
   searched only `context/schemas` and `agi-tree/context/schemas`, neither of
   which exists post-g11; added `.agi/context/schemas` to its candidates.
   (The sibling `_shipped_schemas_dir` already covered `.agi`.)
3. `extensions/agi/tests/test_brief.py` — `test_adapter_accepts_director_tier`
   skipped because the `_cmd` harness declared no director/prime_director
   model. Added `"director": "d"` and `"prime_director": "pd"` to the default
   harness `models` in `_cmd`, so both command paths are actually exercised.

**Five scripts got a real `--help`** (kept existing positional/stdin/command
behaviour); removed from `NO_HELP` in `test_bin_help_smoke.py`, which now lists
only `node_writer.py`:

- `brief.py` — already had argparse; was stale-listed, removed from `NO_HELP`.
- `briefing.py` — was a main-less library; added a `main()` with argparse
  (`root` positional, `--compact`) that reuses `zoom._load_wired_graph`, plus
  kept the `to_markdown`/`to_compact` library functions intact.
- `completion.py` — was `sys.argv[1]`/`argv[2]`; added argparse with `root` +
  `node_id` positionals, same exit contract (0 complete, 1 not).
- `payload_boundary.py` — was `sys.argv[1] if len>1 else "."`; added argparse
  with an optional `repo` positional (default `"."`).
- `write_guard.py` — custom argv; `--help`/`-h` now print the docstring and
  exit 0 (was `unknown command '--help'` exit 2). `check`/`hook` untouched.

`node_writer.py` remains in `NO_HELP` with its library-module reason.

## Evidence

First pass had a defect I introduced and then fixed: my `briefing.py` edit
overwrote the `to_compact` function body (2 test failures in `test_viewport.py`);
restored it and re-ran. Final suite run (full repo suite, after all edits):

```
$ python3 -m pytest extensions/agi/tests/ -q -rs
...
1735 passed, 1 skipped in 98.11s

SKIPPED [1] extensions/agi/tests/test_bin_help_smoke.py:48:
  node_writer.py: library module, not a CLI tool; no --help
```

Targeted verification of the three repointed tests + the help smoke:

```
$ python3 -m pytest test_bin_help_smoke.py test_brief.py::test_adapter_accepts_director_tier \
    test_grid.py::test_sanitize_real_agi_tree_corpus_round_trips_distinctly \
    test_spawn_gate.py::test_shipped_schemas_load_without_error -v
44 passed, 1 skipped in 7.92s
```

Per-script `--help` smoke (all exit 0, non-empty stdout): brief.py (167B),
briefing.py (369B), completion.py (315B), payload_boundary.py (307B),
write_guard.py (648B).

`git status --short` shows only the 8 edited engine files plus this scaffolded
node — no unexpected files.

## Agent Notes
Repointed 3 stale post-g11 skips at .agi layout; added argparse --help to 5 scripts; NO_HELP now only node_writer. 1735 passed, 1 skipped.

Parent review: proved upheld. Verified independently — full suite green (1734 passed, 1 skipped), only skip is node_writer. Targeted: 44 passed, 1 skipped. NO_HELP now lists only node_writer.py. git status shows only the 8 edited engine files + nodes. Caveat: suite result fluctuates +/-1 (1733/1734/1735) because sibling kid a00-4854a4bc edits the shared tree concurrently mid-run (test_metrics reads live graph state); transient, environmental, not a defect of this work.
