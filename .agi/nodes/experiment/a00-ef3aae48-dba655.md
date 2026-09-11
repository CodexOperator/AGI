---
id: experiment:a00-ef3aae48-dba655
mint_id: 299b424f16d342768d49a376cfc42cc1
type: experiment
parents:
  - hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
next_edges: []
confidence: 0.78
edited_by: a00-be97b565
evidence_runs:
  - experiment:a00-ef3aae48-dba655
loop: hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3b8bb46b835f1f03
season: 2
title: A00 ef3aae48 dba655
town: core
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# experiment:a00-ef3aae48-dba655

## Experiment

Fixed the round's falsifier (defect A from the amended build order), measured
pre-fix and proved post-fix on the real tree.

**Pre-fix measurement (the falsifier):** every seat row in the real
`config:seats` carries a RELATIVE worktree of the shape
`.agi/worktrees/seat-<name>` (verified: `sanctuary-director`,
`sensei-director`, `sanctuary-helper` — reproduced with `load_seats`).
`_worktree_modified_ids` (graphweb.py ~L342) resolved a relative worktree as
`Path(graph_root) / worktree`, i.e. `.agi/.agi/worktrees/seat-<name>` — never a
directory — so **every** relative seat row returned `working_on: []`. That is
the claim's OWN falsifier: "a seat with a modified node file in its worktree
whose id does NOT appear in /live.json working_on". The L4.235 harvest already
observed it (`sanctuary-director ... working_on: []` at 15:20Z with a node
modified in that worktree).

**Fix (graphweb.py):** added `_resolve_worktree(worktree, graph_root)`.
A relative worktree is resolved against the candidates, in order
`[git_common_root(graph_root), graph_root.parent]` (deduped); the first
`<base>/<worktree>` that is a directory wins; none -> None -> `[]`.
`locations.git_common_root` returns the MAIN CHECKOUT ROOT (measured:
`/home/ubuntu/work/agi` from this worktree), which is the dir that owns
`.agi/worktrees/`. In the repo-less fixture `git_common_root` returns
`graph_root` unchanged and `graph_root.parent` is the fallback that catches
the tmp fixture layout. Import guards mirror `find_root`'s existing
try/except + `sys.path` sibling pattern.

**Fixture (test_graphweb.py):** the seat rows' `worktree` strings changed from
the buggy `worktrees/wt1` (graph_root-relative) to the REAL shape
`.agi/worktrees/wt1` / `.agi/worktrees/wt2` (checkout-root-relative). The wt1
directory already sits at `<project>/.agi/worktrees/wt1`, so nothing moves.
Added `test_relative_checkout_root_worktree_resolves`, asserting `_resolve_worktree`
returns a directory and `live_view` lists `goal:g17child` under
`sanctuary-director.working_on` from the relative row, while the dead wt2 stays
`[]` and never fires git.

## Evidence

Tests (fixture-only, the only command the round asks for):

```
python3 -m pytest extensions/agi/tests/test_graphweb.py extensions/agi/tests/test_bin_help_smoke.py -q
71 passed, 1 skipped in 5.63s
```

Real-tree proof (run from this worktree, `extensions/agi/bin` on `sys.path`):

```
graph_root   : /home/ubuntu/work/agi/.agi/worktrees/a00-be97b565/.agi
git_common   : /home/ubuntu/work/agi            # from locations.git_common_root
```
```
mine = '.agi/worktrees/a00-be97b565'            # the relative shape the bug broke
_resolve_worktree(mine, root) -> /home/ubuntu/work/agi/.agi/worktrees/a00-be97b565  (is_dir True)
_worktree_modified_ids(mine, root) -> ['experiment:a00-ef3aae48-dba655']
```
Direct git status of the same worktree agrees exactly:
```
?? .agi/nodes/experiment/a00-ef3aae48-dba655.md
```
Pre-fix this same call returned `[]` (the relative path joined under `.agi/`
was not a directory). The other seat worktrees return `[]` because they hold
no modified node right now — correct, not the bug.

## Scope

Defect A only (the falsifier — a build-order claim, so measure → implement →
prove on built bytes). Defect B (the O(n²)×180 cold layout, id-set-keyed
persisted layout + parse cache + incremental relaxation + `graph_version`) and
Kid C (ghost nodes / the owner's 2026-09-11 15:5xZ addendum) are separate
sub-builds assigned to the round's other kids; not done here. index.html and
the palette untouched; no new Python deps; no live pane; nothing but my own
scaffolded node added to this worktree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-be97b565, L4.250) — ACCEPTED, verdict kept at inconclusive_lean_proved:78.
(1) INSTRUCTION: the AMENDED build order said "a relative worktree resolves against the SOURCE root ... with graph_root.parent as the fallback".
(2) MACHINE: graphweb.py:342 `_resolve_worktree` builds candidates [git_common_root(graph_root), graph_root.parent], dedupes, first existing dir wins; `_worktree_modified_ids` calls it (graphweb.py:389). I re-ran the real-tree call: `_worktree_modified_ids(".agi/worktrees/a00-be97b565", root)` -> ["experiment:a00-ef3aae48-dba655"]; `pytest test_graphweb.py test_bin_help_smoke.py -q` -> 71 passed, 1 skipped, reproduced at review time. `git status` of that worktree agrees (`?? .agi/nodes/experiment/a00-ef3aae48-dba655.md`).
(3) NEAR MISS: on THIS checkout the two candidates coincide (git_common_root == graph_root.parent == /home/ubuntu/work/agi), so the fixture cannot distinguish the ordering; an implementation joining under graph_root.parent ALONE would pass every test here and still be wrong for a graph nested below the repo root. The candidate ORDER is load-bearing and untested — that is the node's weakness, not its claim's.
(4) DEVIATION: none. The kid split defect A from defect B on its own and said so, which is why the round needed a second kid for B.
<!-- THOUGHT:END -->

## Agent Notes
Fixed the round's falsifier (defect A): relative .agi/worktrees/seat-* rows now resolve against git_common_root instead of graph_root; pre-fix all seats returned working_on=[], post-fix real-tree call returns the modified node id matching git status. 71 tests pass.

PARENT REVIEW (a00-be97b565, L4.250): accepted, inconclusive_lean_proved:78; fix verified on the real tree (relative seat worktree now lists its modified node id) and 71 tests reproduced; weakness is that the two candidate roots coincide here so the ORDER is untested.
