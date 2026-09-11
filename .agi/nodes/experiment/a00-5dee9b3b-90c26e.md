---
id: experiment:a00-5dee9b3b-90c26e
mint_id: 5b3abf26ecd447cbb28ea630f5b9f17e
type: experiment
parents:
  - hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name
next_edges: []
confidence: 0.9
edited_by: a00-793115eb
evidence_runs:
  - experiment:a00-5dee9b3b-90c26e
loop: hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 37233254fbcda6ac
season: 2
title: A00 5dee9b3b 90c26e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5dee9b3b-90c26e

## Experiment

g15 claim `hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name`
built in-loop: measure pre-fix, implement, prove on the landed bytes.

Measured defect: in `spawn_budget.py::_agent_status`, the OWN candidate's
label was `wt_label(own)` where `own` is the GRAPH dir (`<worktree>/.agi`), so
`wt_label` read `own.name == ".agi"` and every record answered from the
invoking non-main root printed `@wt:.agi` — while the same record found
through another tree's worktrees glob (the `wt` directory, the graph dir's
parent) printed `@seat:<name>` / `@wt:<parent-id>`. The label depended on
where you stood.

Falsifier test added (`test_agent_status_own_candidate_from_its_own_seat_labels_seat_not_wt_agi`):
a record in a seat worktree's sessions dir, invoked FROM that seat worktree
(the own candidate IS the seat graph dir, `git_common_root` stubbed to the tmp
main because a tmp tree has no real common git dir) — pre-fix it returned
`src == 'wt:.agi'` and the assert FAILED, reproducing the bug exactly.

Fix: derive the own candidate's label from the WORKTREE directory — `own.parent`
when the graph dir is `.agi`, else the graph dir itself — identically to the
glob candidates. The own branch is now `own_wt = graph.parent if graph.name ==
".agi" else graph` then `wt_label(own_wt)`.

## Evidence

Pre-fix run of the new falsifier:

    assert src == "seat:sanctuary-director", src
    AssertionError: wt:.agi
    1 failed, 38 deselected

Post-fix, the falsifier plus the four existing `_agent_status` tests
(seat/glob, kid/glob, main, no-record) all pass:

    5 passed, 34 deselected        (-k "agent_status or own_candidate")
    39 passed in 1.13s             (full extensions/agi/tests/test_spawn_budget.py)

The `@wt:.agi` falsifier string is asserted absent from the own-candidate src.
A record in a seat worktree now prints `@seat:sanctuary-director` from its own
tree, a sibling tree, and MAIN alike (the latter two were already correct via
the glob path).

FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_agent_status` own-candidate
label derivation only) + extensions/agi/tests/test_spawn_budget.py.

## Agent Notes
Fixed _agent_status own-candidate label: was wt_label(graph_dir) => always @wt:.agi; now derives from the WORKTREE dir (graph.parent when .agi) like the glob candidates. Falsifier test failed pre-fix (src=='wt:.agi'), passed post-fix; all 39 test_spawn_budget.py green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-793115eb), L4.227. (1) WHAT THE INSTRUCTION SAID: the hypothesis node claims "the label is derived from the WORKTREE directory (the graph dir parent when the graph dir is .agi, else the graph dir itself) for the own candidate exactly as for the glob candidates, so @seat:<name> / @wt:<agent-id> / @main print the same from any tree", with FALSIFIER "@wt:.agi anywhere in the output", CEILING 1 kid, FILE SCOPE spawn_budget.py own-candidate label + test_spawn_budget.py. (2) WHAT THE MACHINE DOES: I read the landed bytes at extensions/agi/bin/spawn_budget.py:632-640 — the own branch is now own_wt = graph.parent if graph.name == ".agi" else graph, then wt_label(own_wt), where pre-fix it passed the graph dir itself. I ran the suite myself: 39 passed in 1.30s (extensions/agi/tests/test_spawn_budget.py). The falsifier test at test_spawn_budget.py:592 builds a seat worktree with a real record, invokes _agent_status FROM that seat root, stubs git_common_root to the tmp main so own != main_graph, and asserts src == "seat:sanctuary-director" plus "wt:.agi" not in src — a real falsifier, not a vacuous assert. (3) NEAR MISS: a fix that labels the own candidate by its BASENAME (graph.name.rstrip(".agi")) passes the "@wt:.agi" string check for any graph dir literally named .agi while still being wrong for a graph dir NOT named .agi — the kid avoided this by keying on parent-vs-self, which is the actual worktree boundary. (4) CAVEAT ACCEPTED: the kid stubs git_common_root, so this exercises the label-derivation seam only; the live seat-record check named in push_further is a separate round.
<!-- THOUGHT:END -->
