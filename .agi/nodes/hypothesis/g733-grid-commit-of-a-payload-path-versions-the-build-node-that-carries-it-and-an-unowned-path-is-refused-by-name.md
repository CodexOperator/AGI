---
id: hypothesis:g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name
mint_id: 6dacb22d21bb4ea3a881c5ab8f6636a7
type: hypothesis
parents:
  - goal:g7.33.19.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "`grid.py commit <path>` where <path> is a build node's payload (the value of some node's `payload_ref`) commits THAT node as one version (node.md + payload in one tree), exactly what `grid.py commit <node file>` makes: in a scratch repo, editing only the payload and running `commit extensions/x.sh` makes v2 with the new payload blob and the unchanged node.md blob, a second identical call makes no version, and `commit <node file>` afterwards makes none; a path that no node carries as payload_ref and that is not a node file prints `ERR: no build node carries payload_ref <path>`, exits non-zero and writes no ref."
title: "grid.py commit of a payload path versions the build node that carries it, and an unowned path is refused by name (SM 02:2xZ, belam GO 02:2xZ)"
town: core
---
# hypothesis:g733-grid-commit-of-a-payload-path-versions-the-build-node-that-carries-it-and-an-unowned-path-is-refused-by-name

## Measured
- DG1 10-03: the grid already versions node + payload as ONE tree when the NODE is committed (commit_file, grid.py:852; the per-path and --all loops share the payload resolution): scratch v1 / payload-only v2 / node-only v3 / unchanged no version; live 310 of 310.
- The gap (SM 02:2xZ): the v5 HEAD says to version a change by path, and cmd_commit's per-path loop (grid.py ~:1095) takes node files only; a payload path has no `id:` frontmatter, so the loop reports skip (no id) and makes no version. The build-node index already exists in the module: parse_payload_ref(p) per node file (iter_node_files), resolve_payload(root, ref, engine_root, location) for where the bytes live.
- Not measured here: how many callers pass a payload path today (the HEAD's wording is the only one known).

## CLAIM
`grid.py commit <path>` where <path> is a build node's payload (the value of some node's `payload_ref`) commits THAT node as one version (node.md + payload in one tree), exactly what `grid.py commit <node file>` makes; an unowned path is refused by name, exit non-zero, no ref written.

## Dispatch line
config-max: none / template-max: none / code: grid.py cmd_commit, a path-to-node map built once per command from iter_node_files + parse_payload_ref (+~12 lines), the refusal; test_grid*.py gains the scratch cases. NOT dispatched until handed (DG2 falsifier, DG3 or a kid builds).

## FALSIFIERS
The three of goal:g7.33.19.1 (the scratch payload-only v2 and its idempotence; the unowned-path refusal; the grid tests pass).

## TESTS
a scratch-repo pytest like DG1's 10-03 mechanism check (build node + payload, v1, payload-only edit, `commit <payload path>`, version count and tree entries); the unowned-path case asserts exit != 0 and `refs/grid` unchanged.

## FILE SCOPE
extensions/agi/bin/grid.py · extensions/agi/tests (one grid test file). Never the live refs (the tests use a scratch repo).

## CEILING
1 parent · kids <= 1 · <= 35 production code lines, docstring and blanks excluded (was +12; DG1 02:5xZ, measured: DG2 patch 21, DG3 fix about 31) · +35 test lines · 0 USD · regular review.
