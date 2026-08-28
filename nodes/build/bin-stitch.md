---
build_kind: code
confidence: 1.0
id: "build:bin-stitch"
mint_id: ad6809b5d43b4983827231158b779f69
origin: build-scan
parents:
  - idea:engine-stitch
payload_ref: extensions/agi/bin/stitch.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/stitch.py"
type: build
---

`extensions/agi/bin/stitch.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-stitch`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/stitch.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 142'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 144'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: importlib.util
  how: '`import importlib.util` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 146'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 147'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 148'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 149'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 150'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: collections.Counter
  how: '`from collections import Counter` at line 151'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 152'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml
  how: '`import yaml` at line 154'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: yaml.safe_load
  how: '`yaml.safe_load(parts[1])` at line 239'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: md_path
  how: '`md_path.read_text(encoding=''utf-8'')` at line 275'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: StitchSafetyError
  how: defines public class `StitchSafetyError` at line 164
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: Level3Node
  how: defines public class `Level3Node` at line 213
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _parse_frontmatter
  how: 'defines private function `_parse_frontmatter` at line 231, signature: (text:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: load_level3_nodes
  how: 'defines public function `load_level3_nodes` at line 250, signature: (project_root:
    Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _entry_pairs
  how: 'defines private function `_entry_pairs` at line 316, signature: (entries)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: diff_contract
  how: 'defines public function `diff_contract` at line 322, signature: (stored: dict,
    fresh: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _group_by_payload_ref
  how: 'defines private function `_group_by_payload_ref` at line 349, signature: (nodes:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_well_formed_chain
  how: 'defines private function `_is_well_formed_chain` at line 361, signature: (group:
    list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _chain_order
  how: 'defines private function `_chain_order` at line 394, signature: (group: list[Level3Node])'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: verify_tree
  how: 'defines public function `verify_tree` at line 399, signature: (project_root:
    Path, engine_root: Path, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: has_drift
  how: 'defines public function `has_drift` at line 521, signature: (report: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _is_within
  how: 'defines private function `_is_within` at line 530, signature: (path: Path,
    root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git_is_clean
  how: 'defines private function `_git_is_clean` at line 538, signature: (repo: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _guard_out_dir
  how: 'defines private function `_guard_out_dir` at line 549, signature: (out_dir:
    Path, project_root: Path, engine_root: Path, publish: bool=False, from_grid: bool=False)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _grid_payload
  how: 'defines private function `_grid_payload` at line 603, signature: (project_root:
    Path, node: Level3Node, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: materialize
  how: 'defines public function `materialize` at line 637, signature: (project_root:
    Path, engine_root: Path, out_dir: Path, force: bool=False, version: int | None=None,
    from_grid: bool=False, publish: bool=False, grid_version: int | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_verify_report
  how: 'defines public function `print_verify_report` at line 782, signature: (report:
    dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: print_materialize_report
  how: 'defines public function `print_materialize_report` at line 827, signature:
    (stats: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 861, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 36 `print()` call(s) at line(s) [783, 784, 786, 788, 790, 792, 794, 796, 798,
    800, 802, 803, 806, 809, 812, 816, 818, 819, 822, 824, 828, 829, 831, 834, 836,
    840, 842, 844, 847, 849, 852, 854, 855, 906, 917, 925]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
*The reasoning below was authored as `build:bin-stitch@v2` and migrated here when the `@v2` convention was retired (G2.10): a version is a grid commit, not a second node file.*

Teaches `stitch.py` the version dimension `goal:g6.3` introduces this iteration, so a v1→v2 build-node pair sharing a `payload_ref` reads as a version chain instead of drift.

**The defect.** `verify_tree()`'s category 3 grouped nodes by `payload_ref` and reported every group of size > 1 as `duplicate_payload_ref`, which feeds `has_drift()` — a nonzero `--strict` exit. `materialize()` sorted by `payload_ref` and let first-writer-wins (`seen_refs`) pick whichever node happened to sort first by filename, silently skipping the rest as duplicates. Neither function knew a v2 build-node was a legitimate evolution of v1 rather than an ambiguous claim. The first time this iteration's convention actually got used — two v2 nodes minted in parallel by sibling kids this same run, `build:lib-find-root.sh@v2` and `build:skills-agi-SKILL.md@v2` — both would have broken the drift gate and had their materialization outcome depend on filename sort order rather than on which version was intended. That would have blocked G6.3's whole mechanism on its first real use.

**The predicate implemented for "well-formed chain".** Within one `payload_ref` group of size > 1 (`_is_well_formed_chain` in `stitch.py`):
1. Every node has a distinct integer `version` (no two nodes at the same version).
2. Sorted ascending, those versions form a contiguous run: `max(version) - min(version) + 1 == len(group)` — a missing version number leaves an orphan with no defined predecessor, so a gap is not a chain even if every present `supersedes` link looks correct.
3. Every node except the one with the lowest version has `supersedes` equal to the `node_id` of the group member exactly one version below it (its immediate predecessor).

Only a group passing all three is reported under the new `version_chains: {payload_ref: [ids ascending by version]}` key — informational, deliberately excluded from `has_drift()`'s check list, so it cannot make `--strict` fail. `materialize()` writes the chain **head** (highest version) for such a group instead of the old arbitrary first-writer.

**Why everything else stays drift.** A version collision, a `supersedes` naming the wrong predecessor or an id that isn't in the group at all, or a version gap all fail the predicate above and stay in `duplicate_payload_ref`, exactly as before this change. The failure this refuses to introduce is *silently materializing an arbitrary version of a group that only looks ordered* — e.g. two nodes both claiming `version: 2`, or a `supersedes` typo pointing at a node that doesn't exist. `_is_well_formed_chain` does not attempt to salvage a partial order out of an ambiguous group; it returns `False` and the whole group is reported, unresolved, same as the pre-chain behavior. A `--version N` flag was added to `materialize()`/CLI to pick a specific chain member deterministically (reports, never guesses, when no member has that version) — it does not touch genuine-duplicate groups at all, on the same "ambiguity is not this script's to resolve" principle.

**Verification.** `cd extensions/agi && python3 -m pytest tests/test_stitch.py -q`: 31 passed before this change, 42 passed after (11 new tests total, across both passes described here: well-formed chain is not drift + materializes v2 head; same-version collision still drift; `supersedes` naming a missing id still drift; a version gap (v1→v3, no v2) still drift; `--version 1` materializes v1 both via the Python API and the CLI; `--version` with no matching chain member is reported under a new `skipped_no_version` key, not guessed; a non-integer `version` in frontmatter is coerced to 1 with a warning, not a crash; a `build-version` node with an absent contract block is informational not drift; the same node with a *malformed* block still is drift; a `level3-scan` node with an absent block still is drift). Full engine suite (`pytest tests/`): 505 passed, unaffected. Real-corpus `--verify` against `/home/ubuntu/work/agi-tree` (181 level-3 nodes, final run, three real `origin: build-version` nodes present including this one): `duplicate_payload_ref: 0`, `version_chains: 3` (`extensions/agi/bin/stitch.py`, `extensions/agi/lib/find-root.sh`, `skills/agi/SKILL.md`, each `v1 -> v2`); `stale_contracts: 2` (`build:bin-stitch` and `build:tests-test-stitch` — both this change's own payload files, stale only because their stored contracts predate this edit and `level3.py` hasn't rescanned them, which is out of scope here and owned by other kids); `unreadable_contracts: 0`; `contracts_not_derived: 3` (the three real v2 nodes, informational, not drift). See the parent-review paragraph below for how `unreadable_contracts` went from 3 to 0 across two passes on this same node.

**What this node does not claim.** This makes `stitch.py` version-*aware* — it can tell a provably ordered v1→v2 pair from an ambiguous duplicate, and it can materialize a chosen version deterministically. It does **not** make the git grid the payload source; `payload_ref` still resolves against the live engine tree exactly as before (untouched), and grid-as-payload-source is still blocked on S9 per `goal:g6.3`. It also does not make `build-version` nodes *verified* — see the parent-review paragraph below for what changed in category 4 and what is still open.

**Parent review, same version.** The first pass above shipped `version_chains` for category 3 but left category 4 unfixed: a `build-version` node's absent contract block still landed in `unreadable_contracts`, which is drift. Parent review caught that this was not pre-existing — `build-version` nodes did not exist before this iteration — so the net effect of the first pass was to move a false positive from category 3 to category 4 rather than remove it, which would have made G6.5's planned drift cron ("reports drift, writes nothing") permanently noisy the moment it read a real build-version node, on every future run, not just this one. Fixed in this same version, not a v3, because it is the same payload edit still under parent review, not a later change branching off an accepted one: `verify_tree()` now distinguishes *absent* from *malformed*. A node with **no** BUILD-CONTRACT block at all, stamped `origin: build-version`, is reported under a new `contracts_not_derived` key — informational, excluded from `has_drift()`, exactly the same pattern already used for `version_chains`. That exemption is narrow and stays narrow: a block that is *present but malformed* (bad YAML, truncated, wrong shape) stays in `unreadable_contracts` and stays drift on every node regardless of origin — an absent block is not the same fact as a broken one, and this change only ever excuses the former. A `level3-scan` node with an absent block also stays drift unchanged — the exemption checks `origin`, not just "no block found," so it does not widen to cover a genuine generator failure. To be plain about what this does and does not fix: `build-version` nodes still carry **no derived contract at all** — this change makes that fact visible and non-blocking, it does not make those nodes verified in the sense category 4 verifies everything else. Closing that gap for real means `level3.py` deriving contracts for `build-version` nodes the same way it does for `level3-scan` nodes — straightforward for a Python payload like this file itself, but overlapping `goal:g6.6`'s still-open non-code-surface problem for the two real chains whose payload isn't Python (`find-root.sh`, `SKILL.md`). Not attempted here.
<!-- THOUGHT:END -->
