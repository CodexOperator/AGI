---
id: experiment:a00-57e7cc65-40dd68
mint_id: 24fdd10b061c4e55b905a3ebb536f417
type: experiment
parents:
  - hypothesis:l4-find-root-sh-stops-at-the-git-boundary-all-the-way
next_edges: []
confidence: 0.85
edited_by: a00-7290e18a
evidence_runs:
  - experiment:a00-57e7cc65-40dd68
loop: hypothesis:l4-find-root-sh-stops-at-the-git-boundary-all-the-way@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b22bd3077462c8e0
season: 2
title: A00 57e7cc65 40dd68
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-57e7cc65-40dd68

## Experiment

g15 build order: implement `l4-find-root-sh-stops-at-the-git-boundary-all-the-way`
on the landed bytes (merge-up 34 residue), then prove the built bytes.

**Mechanism verified on the bytes first** (PARENT-NOTE mechanism, re-read):
- find-root.sh: the `while [[ "$d" != "/" ]]` climb breaks at `$d/.git`, then
  control FALLS THROUGH to an explicit `/` probe (`agi_graph_dir_in "/"`, then
  `agi_tree_config_path "/"`), and only then reaches phase-2 descend.
- locations.py `find_project_root`: the while-True loop probes `/` as its own
  FINAL iteration on a boundary-free walk, but after a `.git` break goes
  STRAIGHT to `_descend(d)` — it never probes `/` after a boundary break.

So bash was one probe longer than python: after a `.git` break bash still
probed `/`, which could resolve an ANCESTRAL project rooted at the filesystem
root — the divergence the python bound does not have.

**Fix applied** (find-root.sh only): a `hit_git_boundary` flag is set at the
`.git` break; the explicit `/` probe block is wrapped in
`if [[ -z "$hit_git_boundary" ]]`. On a boundary-free walk the flag is unset so
`/` is still probed (matching python's free-walk final-iteration probe); after
a boundary break the `/` probe is skipped but phase-2 descend STILL runs.

**The near miss, avoided deliberately:** I did NOT `return 1` at the `.git`
break. python still runs `_descend(d)` after its break (locations.py), so a
`return 1` would have created the opposite divergence — a nested repo whose
start descends into `<start>/*-tree/` would resolve from python and refuse from
bash. The flag guards ONLY the `/` block; descend is common to both halves.

## Evidence

`python3 -m pytest extensions/agi/tests/test_locations.py -q`
=> 85 passed in 2.33s

New tests added (both in test_locations.py):
1. `test_bash_and_python_agree` shape `nested_git_descend` — the near-miss
   pinner: outer repo with `.agi`, nested `git init` WITHOUT `.agi`, and a
   legacy `<start>/<start>-tree/` WITH a config below the boundary. Both halves
   break at the nested `.git`, skip the `/` probe, and descend into that tree;
   bash == python == the tree. This is the shape a `return 1` "fix" would have
   broken (bash refuses, python descends).
2. `test_root_probe_runs_on_boundary_free_walk_not_after_git_boundary` + helper
   `_bash_find_root_stub_graph_at_root` — makes the hidden `/` probe observable
   WITHOUT root access by sourcing find-root.sh in a subprocess and stubbing
   `agi_graph_dir_in` / `agi_tree_config_path` so ONLY `/` looks like a project:
   * boundary-free walk from a deep dir, stub `/`-as-project => the `/` probe
     fires, rc==0, resolves `/__fake_root_graph`.
   * walk under a nested `git init` boundary, same stub => the `/` probe is
     skipped, rc==1 (python agrees: it never probes `/` after a boundary break).

Falsifier check against the pre-fix logic (throwaway copy with the guard
removed, real file untouched): the stub walk under a `.git` boundary resolved
`/__fake_root_graph` with rc==0 — i.e. the pre-fix code probes `/` after a
boundary break, exactly the bug. The new stub test therefore genuinely catches
it. `bash -n` clean; live run from the worktree still resolves its own `.agi/`.

Secondary nit: `/__fake_root_graph` is a fake path on the virtual root; the
test never touches `/` for real — nothing on the actual filesystem root is
created or modified.

## Agent Notes
find-root.sh '.git' break now sets hit_git_boundary flag so the trailing '/' probe is skipped after a boundary break (skipping NOTHING else — phase-2 descend still runs). Deliberately avoided the 'return 1' near-miss that would have skipped descend. bash now agrees with locations.py on every shape; 85 test_locations tests pass incl. new nested_git_descend cross-check shape and a stub-based test proving '/' probe fires on a free walk but is skipped under a .git boundary (verified to fail against pre-fix logic).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7290e18a, L4.224) — accepted proved/0.85, verified independently on the staged bytes rather than read off the report.

(1) WHAT THE INSTRUCTION SAID: goal:g15 / hypothesis:l4-find-root-sh-stops-at-the-git-boundary-all-the-way — "a `.git` break sets a flag (or returns 1 directly) so the `/` probe runs ONLY when the loop exhausted the path without meeting a boundary", FILE SCOPE find-root.sh loop exit + trailing probe, and this is a build order: implement, do not merely reproduce.

(2) WHAT THE MACHINE DOES, cited to bytes I read myself: extensions/agi/lib/find-root.sh:195 sets `hit_git_boundary=1` at the `.git` break and the whole explicit `/` probe is wrapped `if [[ -z "$hit_git_boundary" ]]` at :207, with phase-2 descend left unconditional at :221. extensions/agi/bin/locations.py:217-223 breaks at `.git` and goes straight to `_descend(d)`, never probing `/`. I RAN, not read: `pytest extensions/agi/tests/test_locations.py -q` -> 85 passed in 2.35s.

(3) THE NEAR MISS, stated as the counterfactual I built and ran: the hypothesis text itself offers "returns 1 directly" and that is the trap — python still descends after its break, so `return 1` would refuse the nested_git_descend shape bash-side while python resolves it. I copied the tree to /tmp, replaced the flag line with `return 1`, and ran the kid`s new cross-check shape: `nested_git_descend` FAILED, bash=None python=<outer>/nested/nested-tree. The tempting fix is wrong and the kid`s pinner catches it. I also reverted the guard to unconditional on a /tmp copy and the stub test FAILED with rc=0 out=/__fake_root_graph, so the falsifier is genuinely reproduced by the pre-fix logic — the stub is not decoration.

(4) DEVIATION FROM A STANDING RULE: none. The kid stayed inside FILE SCOPE (find-root.sh + test_locations.py + its own node), implemented rather than measured, and named itself in evidence_runs, which is what an experiment may do.

Residue: none. The one asymmetry this node names is closed and pinned in both directions.
<!-- THOUGHT:END -->
