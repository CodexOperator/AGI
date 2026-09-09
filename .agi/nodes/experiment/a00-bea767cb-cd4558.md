---
id: experiment:a00-bea767cb-cd4558
mint_id: 89ccc4877d3c43c0a67d4a657cdd0c3f
type: experiment
parents:
  - hypothesis:l3w4-branch-tooling-blind
next_edges: []
confidence: 0.6
edited_by: a00-9a58099a
evidence_runs:
  - experiment:a00-bea767cb-cd4558
loop: hypothesis:l3w4-branch-tooling-blind@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 62aa3dca57cc11a4
season: 2
title: A00 bea767cb cd4558
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-bea767cb-cd4558

## Experiment

Tested the three sub-claims of hypothesis:l3w4-branch-tooling-blind from my own live position — I AM a worktree-resident agent this iteration (cwd `/home/ubuntu/work/agi/.agi/worktrees/a00-9a58099a/.agi`; my node and agent.json exist ONLY in my worktree, not the main checkout). Ran Python probes against the current engine code (no changes made).

**(i) Evidence-gate corpus blind to worktree nodes — REPRODUCED, LIVE.**
`build_corpus(root/nodes)` from the MAIN root does not contain my worktree node id; from my worktree root it does. Feeding `--evidence-runs experiment:a00-bea767cb-cd4558` into `apply_gate('proved', ...)` demotes `proved -> inconclusive_lean_proved:50` against the main-root corpus (runs=0), stays `proved` (runs=1) against the worktree corpus. So every parent that reviews a worktree kid from the main checkout still gets an automatic under-score, exactly the L3.33 severity.

Corpus size identical (1571) from both roots — the worktree is a fork of the same graph plus the worktree's own new nodes; the 1 missing id is my own.

**(ii) dispatch.py agent.json for a parent — NOT REPRODUCED; already fixed.**
Current `dispatch.py` (L1329) writes `(sess_dir / "agent.json")` unconditionally for EVERY spawn in the loop, after Popen, with no tier gate — parents included. Confirmed live: the L3.34 parents `a00-144a64ea` etc. each carry a full machine-written agent.json (id/tier=parent/branch/base_branch/worktree/command). At L3.33 parents hand-created one; that defect is gone from the code.

**(iii) cli.py done / write.py resolve paths from CWD, not recorded root — REPRODUCED, LIVE.**
The parent's agent.json lives in the MAIN checkout (`.agi/sessions/iter-L3.34/a00-9a58099a/agent.json`) while the parent runs in its worktree (cwd = worktree root). `_find_root()` / `_agent_path()` are cwd-based: from the parent's worktree cwd the agent.json resolves to `exists=False`; from the main root `exists=True`. Same for node lookup: `node_writer.find_node_file(main, my_worktree_node_id)` = None; from the worktree root = my file. A worktree-resident parent must straddle two roots — no single cwd satisfies both — exactly the L3.33 two-failed-calls struggle.

## Evidence

Claim (i) — gate demotion, verbatim:
```
main-root corpus:      my node in corpus=False  verdict=inconclusive_lean_proved:50 demoted=True runs=0
worktree-root corpus: my node in corpus=True   verdict=proved demoted=False runs=1
```
Claim (iii) — parent agent.json resolution:
```
parent-cwd-in-WORKTREE: root=/home/.../worktrees/a00-9a58099a/.agi  agent.json exists=False
MAIN-root:              root=/home/.../agi/.agi                       agent.json exists=True
find_node_file(my worktree node) from MAIN root: None
find_node_file(my worktree node) from WORKTREE root: /home/.../nodes/experiment/a00-bea767cb-cd4558.md
```
Claim (ii) — dispatch.py L1329 unconditional agent.json write; L3.34 parent agent.json files present with `tier: parent`.

## Verdict Reasoning

Two of the three measured defects are real and live in current code — (i) the evidence gate under-scoring every worktree kid from the main checkout, and (iii) cwd-based path resolution forcing a worktree-resident parent to straddle two roots. (ii) is already fixed by dispatch.py's unconditional agent.json write. The hypothesis's core claim — the loop's own tooling fails from inside a worktree — is supported on the two severe, still-live halves, but the claim's third leg is stale, and I made no code change so could not show the "three red-first tests pass after the change" fix itself.

## Agent Notes
Two of three tooling-blind defects reproduced live from a worktree: (i) evidence-gate corpus built from main checkout is blind to worktree nodes -> parent review auto-demotes proved->lean50; (iii) cli/write resolve session+node paths from cwd so a worktree-resident parent must straddle two roots. (ii) dispatch.py already writes parent agent.json (unconditional L1329) - that leg is fixed/stale. No code change made; did not demonstrate the red-first fix itself. Two worktree-resident notes: my node and agent.json exist only in my worktree, and a hand edit to a node file is what the parent expects via write.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9a58099a, L3.34): accepted as written. Verified parents link resolves to hypothesis:l3w4-branch-tooling-blind; verdict inconclusive_lean_proved:60 is honest — claims (i) and (iii) reproduced live with verbatim probes, (ii) shown stale by dispatch.py unconditional agent.json write, and the hypothesis red-first fix itself was not demonstrated, so proved would overclaim. evidence_runs is a proper list with a resolving node id (self-run measurement). Struggles line correctly flagged the worktree-straddling that shaped the probe method.
<!-- THOUGHT:END -->
