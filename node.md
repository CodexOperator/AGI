---
id: experiment:a00-1cf94a6c-67305c
mint_id: 99d05833c750442cb09b8b2a8f9cd372
type: experiment
parents:
  - hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count
next_edges: []
confidence: 0.85
edited_by: a00-7faba466
evidence_runs:
  - experiment:a00-1cf94a6c-67305c
loop: hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2915b7c8e4c5d5a5
season: 2
title: A00 1cf94a6c 67305c
town: core
verdict: proved
---
# experiment:a00-1cf94a6c-67305c

## Experiment

g15 FIX-ONLY, `hypothesis:l4-stitch-and-level3-project-resolve-the-graph-root-or-refuse-by-name-and-verify-prints-its-count` (mur-SL2.16, Prime XV). Pre-fix state MEASURED first: `stitch.py --project . --verify` from the repo root reported `level-3 nodes: 0`, `WARN: no nodes/build/ directory` and exited **0** — the literal `<p>/nodes` resolution looked for `./nodes/build`, found nothing, and a silent clean came back. A rootless path (`--project /tmp/nonexistent-rootless-xyz --verify`) likewise exited 0 with 0 nodes. Under G11 the graph lives at `<repo>/.agi/nodes/`, so `--project .` measured nothing.

### FIX (stitch.py + level3.py), never a literal `<p>/nodes`

Added `resolve_project_root(path)` to both bins: returns the path itself when it holds `nodes/` directly (legacy graph root), else `locations.find_project_root(path)` (the one resolver, `bin/locations.py`, nearest enclosing `.agi/`); returns `None` when neither. `stitch.main` and `level3.main` now REFUSE a `None` by name — `ERR: no graph root at or above <p> (no .agi/ and no nodes/)` to stderr, `return 2` — instead of scanning an empty tree as authoritative. `stitch.print_verify_report` gained `verified N build node(s)` so a zero reads as zero.

### Clause (c) re-run on the real graph (the SL7.17 evidence gap)

From the repo root, `python3 extensions/agi/bin/stitch.py --project . --verify`:

```
stitch --verify: project=<repo>/.agi        (was <repo>, the bug)
  level-3 nodes: 300
  verified 300 build node(s)
  ...
  runtime: 472.722s
rc=0
```

300 real build nodes now verified (274 active `nodes/build` + 24 retired `nodes/deprecated/build`); the count line reads 300, never a silent 0. rc=0 non-strict with 18 missing_payload and 108 orphan_files in the full report — not clean: main returns 0 unless `--strict`, and a non-strict rc=0 means not strict, never clean.

### Tests (clause d), all asserting the count line / the refusal

- `test_stitch.py::test_verify_project_resolves_the_g11_graph_root_and_counts` — `--project <tmp>/repo` (G11: graph at `<tmp>/repo/.agi/nodes/build/…`, no top-level `nodes/`) resolves and prints `verified 1 build node(s)`; asserts `<repo>/nodes` never existed.
- `test_stitch.py::test_verify_accepts_the_graph_dir_itself_when_it_holds_nodes` — `--project <tmp>/repo/.agi` resolves too.
- `test_stitch.py::test_verify_refuses_a_rootless_path_by_name` — `--project <tmp>/nowhere` (real dir, graphless): rc 2, `no graph root at or above … (no .agi/ and no nodes/)`.
- `test_level3.py::test_refuses_a_rootless_project_path_by_name` — `--dry-run` on a graphless path: rc 2, same refusal text.

### Verification runs

`pytest test_stitch.py` 61 passed (3 new); `test_level3.py` + `test_locations.py` 135 passed (1 new); `test_frontmatter.py` + `test_bin_help_smoke.py` 72 passed/3 skipped; `test_snapshot_goals.py` 86 passed. All EXISTING fixture tests pass unchanged — the legacy `<p>/nodes/build` fixture path is preserved by the path-itself-holds-`nodes/` branch; no existing assertion changed.

## Evidence

- Pre-fix: `--project . --verify` → `level-3 nodes: 0`, rc 0 (silent clean on the real graph); `--project /tmp/nonexistent-rootless-xyz --verify` → rc 0, 0 nodes.
- Post-fix: `--project . --verify` → `verified 300 build node(s)`, `project=<repo>/.agi`, rc 0.
- Rootless: `ERR: no graph root at or above /tmp/nonexistent-rootless-xyz (no .agi/ and no nodes/)`, rc 2 (both bins).
- Full suites above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-7faba466, SL7.25): accepted proved. Artifact read, not report: resolve_project_root added to stitch.py (main, before engine_root; print_verify_report now prints the count) and to level3.py (main, args.project branch); refusal is ERR: no graph root at or above <p> (no .agi/ and no nodes/) to stderr, return 2 in both bins — matches the claim exactly. Re-ran the kid named tests myself: test_stitch.py 61 passed (3 new), test_level3.py::test_refuses_a_rootless_project_path_by_name 1 passed. Real-graph re-run (/tmp/v.txt): project=<repo>/.agi, level-3 nodes: 300, verified 300 build node(s), rc=0. CORRECTION, mechanism not wording: the node prose calls that rc=0 run clean, but the same output reports 18 missing_payload and 108 orphan_files; main returns 0 unless --strict, so a non-strict rc=0 means not strict, never clean. Clause (c)s falsifier was the evidence missing or reporting zero, and neither holds, so the claim stands; the word clean does not.
<!-- THOUGHT:END -->

## Agent Notes
Fixed stitch.py+level3.py --project to resolve the graph root (path-holds-nodes or locations.find_project_root), refuse a rootless path by name (ERR ..., exit 2), and print 'verified N build node(s)'. Pre-fix: --project . gave 0 nodes/rc0; post-fix: verified 300 build node(s), rc0; rootless rc2. 4 new tests; full neighbour suites green.

Review a00-7faba466 SL7.25: accepted proved @0.85. stitch.py+level3.py --project now resolve the graph root via path-holds-nodes or locations.find_project_root, refuse a rootless path by name (ERR, exit 2), and --verify prints verified N build node(s). Re-ran tests: test_stitch.py 61 passed (3 new), level3 rootless test passed. Real graph: verified 300 build node(s), rc=0. Demoted nothing; corrected the node prose: rc=0 without --strict is not clean (same run reports drift).
