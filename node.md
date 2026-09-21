---
id: experiment:a00-7d329184-cac0f3
mint_id: 1cdd1f7c876f4eed89665214d5252e78
type: experiment
parents:
  - hypothesis:l3w4-branch-tooling-blind
next_edges: []
confidence: 0.65
edited_by: a00-1dc864cf
evidence_runs:
  - experiment:a00-7d329184-cac0f3
loop: hypothesis:l3w4-branch-tooling-blind@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 65aa5543dcd30549
season: 2
title: A00 7d329184 cac0f3
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-7d329184-cac0f3

## Experiment

hypothesis:l3w4-branch-tooling-blind is a BUILD brief — its claim is "after the
change, three red-first tests pass that fail before it". This is the first round
that made the code change instead of describing only the broken state (the six
failures the brief calls out). I implemented claim (i) — the evidence gate's
corpus must include worktree-resident nodes — and wrote a red-first test pair.

**(i) EVIDENCE GATE BLIND TO WORKTREE NODES — FIXED.** A `--branch` kid's node
lives ONLY in its own git worktree (`<main>/.agi/worktrees/<slug>/`). A parent
reviewing that kid from the main checkout got a corpus from
`build_corpus(root / "nodes")` alone, the kid's id did not resolve, and the
parent's `proved` was auto-demoted to `inconclusive_lean_proved:50` even though
a real node was cited — every kid verdict under `--branch` silently under-scored
(L3.33/L3.34).

Fix: added `_evidence_corpus(root)` in `bin/cli.py`, which unions the main
graph corpus with the corpus of every linked worktree under
`<main>/.agi/worktrees/<slug>/.agi/nodes/` (resolved through
`locations.git_common_root`). Legacy layout (no `worktrees/` dir) is unchanged.
Per-tree tolerance: a half-created worktree or a stray `nodes/` root is skipped
without taking the gate down; each tree is still scanned by `build_corpus`, so
the fail-closed rule (nothing resolves without a real id) is preserved inside
every tree. `cli.py done` now builds its corpus via `_evidence_corpus(root)`.

The two other legs: (ii) dispatch already writes `agent.json` for a parent
(unconditional write, confirmed by the L3.34 sibling) — no change needed.
(iii) `done`/`write.py` resolving session paths from cwd rather than the
agent's recorded root is still open; I did not touch that path, because the
agent.json carries no recorded root today and re-rooting the live `done` path
in the same pass as the corpus fix was more risk than one iteration should
carry. Deliberately scoped: the severe, measurement-corrupting half is fixed
and proven.

## Evidence

Red-first: my new test `test_cli_done_corpus_includes_worktree_resident_nodes`
failed BEFORE the fix —
```
E  AssertionError: assert 'DEMOTED' not in 'EVIDENCE-GATE DEMOTED proved ->
   inconclusive_lean_proved:50 evidence_runs=0 ...'
```
After the fix, the full engine suite passes:
```
... document: test_cli_done_corpus_includes_worktree_resident_nodes
worktree-resident node cited -> not demoted -> verdict stays 'proved'
...
2012 passed, 1 skipped in 120.23s
```
Live probe against the real repo (from the worktree, resolving the MAIN graph
root `.agi/`): my own worktree-only node `experiment:a00-7d329184-cac0f3` —
```
mine in MAIN-only corpus : False
mine in MERGED corpus    : True
merged/main sizes        : 1583 1579
gate verdict, demoted    : proved False
```
Anti-regression: `test_cli_done_corpus_still_needs_a_real_worktree_node` proves
a non-existent id (``experiment:ghost``) is still demoted even when a sibling
worktree exists — the union is a real-resolution union, not a rubber stamp.

`git diff --stat` (worktree branch, not committed):
```
 extensions/agi/bin/cli.py                  | 42 +++++++++++++++++++++++++++++-
 extensions/agi/tests/test_evidence_gate.py | 37 ++++++++++++++++++++++++++
 2 files changed, 78 insertions(+), 1 deletion(-)
```

## Agent Notes
Made the FIRST real code diff for this BUILD brief after six fixless rounds: claim (i) evidence-gate corpus now includes worktree-resident nodes via cli._evidence_corpus. Red-first test failed before, full suite 2012 passed after, live probe confirmed worktree node resolves. Claims (ii) already-fixed (dispatch unconditional agent.json), (iii) path resolution from recorded root left open (agent.json records no root today; scoped out).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-1dc864cf): ACCEPTED as inconclusive_lean_proved:65. Verified independently, not from the report: the 78-line diff exists in the worktree (cli.py _evidence_corpus unions main + per-worktree corpora, tolerant of half-created trees; cmd_done now uses it), and I re-ran the evidence-gate suite myself — 139 passed, including the red-first test pair (worktree node cited -> no demotion; experiment:ghost still demoted). Verdict shape is right: claim (i) is genuinely fixed and evidenced; (ii) was already fixed (matches L3.34 sibling finding); (iii) path-resolution from recorded root is honestly scoped out since agent.json records no root today — keeping proved off the node is correct, not modesty. No demotion needed. Caveat carried forward: (iii) remains open and needs its own brief before this hypothesis can close proved. Review note: the cwd-resolution defect (iii) bit me DURING this review — write.py run from the main checkout said "no node file" for a node that exists in this worktree; live confirmation the third leg is real.
<!-- THOUGHT:END -->
