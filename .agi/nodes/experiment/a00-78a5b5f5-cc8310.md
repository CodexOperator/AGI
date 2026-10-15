---
id: experiment:a00-78a5b5f5-cc8310
mint_id: 52c82b6049094cdeb294386501d40535
type: experiment
parents:
  - hypothesis:grid-commit-guard-and-writer-read-one-namespace
next_edges: []
confidence: 0.9
edited_by: a00-03596c1e
evidence_runs:
  - experiment:a00-78a5b5f5-cc8310
loop: hypothesis:grid-commit-guard-and-writer-read-one-namespace@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "direct cmd_commit(root,[],do_all=True,session=None) on a tree configured grid.storage_trunk=refs/grid/t7 with the module global REF_NS pre-set to refs/grid/WRONG (not the default)", "expected": "exactly one version under refs/grid/t7/node/<mint>; none under refs/grid/WRONG/ nor refs/grid/node/", "observed": "refs=[refs/grid/t7/node/c3c3...]; trunk=True no_wrong=True no_default=True; same probe on pre-fix bytes FAILS (writes refs/grid/WRONG/node/...)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "seed only refs/grid/t9/session/1/a01/level3-g, blank grid.storage_trunk, then direct cmd_commit on the configured-then-blanked tree", "expected": "SystemExit naming refusing commit and refs/grid/t9, and the ref set byte-identical before/after (nothing written)", "observed": "refused=True, named=True, untouched=True (before==after==[refs/grid/t9/session/1/a01/level3-g]); same probe on pre-fix bytes FAILS (not refused, re-mints refs/grid/node/<mint>)", "result": "pass"}
production_lines: 18
profile: balanced
role: kid
scaffold_hash: 8cdbd31922a06ee5
season: 2
title: "Grid commit guard and writer read one namespace: direct cmd_commit resolves trunk; session-only nested trunk refused"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-78a5b5f5-cc8310

## Experiment

BUILD round (hypothesis:grid-commit-guard-and-writer-read-one-namespace).
Measured the pre-fix state, implemented both conjuncts in `grid.py`, proved the
new tests RED on a scratch copy of the pre-fix bytes and GREEN on the fix.

```
conjunct 1  guard reads `ref_ns_for(root)` (config-aware); writer used the
            module-global `REF_NS`, set only by `main()`->apply_storage_trunk.
            FIX  cmd_commit calls apply_storage_trunk(root) after ensure_repo.
conjunct 2  migrated_trunk_namespaces skipped refs without `/node/`, so a
            nested trunk holding ONLY session refs escaped the refusal.
            FIX  namespace = refname up to its first `/node/` OR `/session/`.
```

FILE SCOPE kept: `extensions/agi/bin/grid.py` (18+ / 4- prod lines) and
`extensions/agi/tests/test_grid.py` (test lines excluded from the ceiling).

## Evidence

Scratch pre-fix copy: `.agi/sessions/iter-EF.76/a00-78a5b5f5/grid_prefix.py`
(both edits reverted programmatically). Same two scenarios run through both
modules:

```
--- PRE-FIX ---
A wrote default refs/grid/node: True      <- configured trunk ignored
B detected: []  | refused: False          <- session-only trunk escapes
B re-minted refs/grid/node: True
--- POST-FIX ---
A refs: ['refs/grid/t7/node/a1a1...']     <- trunk only
A wrote default refs/grid/node: False
B detected: ['refs/grid/t9'] | refused: True
B re-minted refs/grid/node: False
```

New committed tests (`extensions/agi/tests/test_grid.py`):

```
test_direct_cmd_commit_resolves_configured_trunk_itself
test_commit_refuses_nested_trunk_with_only_session_refs
```

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grid.py -q
137 passed, 14 warnings in 16.08s
```

Regression set (configured-trunk isolation, reminming refusal, worktree
resolver, unconfigured default) also green. CLAIM: proved.

## Agent Notes
Both conjuncts fixed in grid.py: cmd_commit resolves its own trunk via apply_storage_trunk; migrated_trunk_namespaces detects node OR session refs. Two new tests red on pre-fix scratch copy, green on fix; test_grid.py 137 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-03596c1e (verdict: accept proved; probes recorded). (1) THE BRIEF SAID: "a direct cmd_commit on a configured tree writes only under its trunk namespace and a nested trunk holding only session refs is refused, proved by a committed test red on the pre-fix bytes, with test_grid.py green." (2) WHAT THE BYTES DO: grid.py:956 cmd_commit now calls apply_storage_trunk(root) after ensure_repo, so the writer functions (node_ref:390, session_ref:398, mint_node_ref:545) and the guards at grid.py:958/988 all read the config-resolved namespace; migrated_trunk_namespaces (grid.py:143) now strips at the first /node/ OR /session/ segment (grid.py:161-162). Proven by BUILDING AND RUNNING: the tree copy with both edits reverted (git show eb74839eec^:extensions/agi/bin/grid.py) fails BOTH new tests, and the tip passes test_grid.py 137/137. (3) NEAR MISS: keeping the guard on ref_ns_for(root) while cmd_commit relies on main() having called apply_storage_trunk satisfies the words "guard reads one namespace" and still lets a library/test caller write the module-global default -- the fix had to sit INSIDE cmd_commit, and it does. A second near miss: detecting the migrated trunk by `/node/` only reads "refs under the nested trunk" and loses the session dimension the claim names. (4) NO DEVIATION: file scope grid.py + test_grid.py (plus the kid own node) is exactly as briefed; probes ran on tmp fixtures only, never the live refs, so the 5-min grid_sync path was untouched. CAVEAT: the nested-trunk detector reserves the literal segments node/ and session/; a trunk named refs/grid/node or refs/grid/session is structurally impossible (it collides with the default namespace own node/session refs), so the regex is safe here, but that is an argument not a test.
<!-- THOUGHT:END -->

PARENT REVIEW a00-03596c1e: ACCEPT proved. Diff reviewed: grid.py +18/-4 (cmd_commit self-resolves trunk; migrated detector counts session refs), test_grid.py +2 tests. Independently reproduced red-on-prefix for both new tests and green tip (test_grid.py 137 passed). Two parent-run negative probes recorded under probes:, one per conjunct, both discriminating (fail on pre-fix bytes). No change outside FILE SCOPE. Title is kid-set.
