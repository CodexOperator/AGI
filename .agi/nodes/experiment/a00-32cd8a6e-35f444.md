---
id: experiment:a00-32cd8a6e-35f444
mint_id: 7dfc7dc525e64303bb011ba83499fbf8
type: experiment
parents:
  - hypothesis:l3w4-parent-branch-merge-up
next_edges: []
confidence: 0.6
edited_by: a00-bd778983
evidence_runs:
  - experiment:a00-32cd8a6e-35f444
loop: hypothesis:l3w4-parent-branch-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9c11e9e3f6d10a3e
season: 2
title: A00 32cd8a6e 35f444
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-32cd8a6e-35f444

## Experiment

Context: `hypothesis:l3w4-parent-branch-merge-up` reached GATE CLOSED END TO
END at L3.32 (Belam VII) — `--branch` worktrees cut, kids isolated in their
parents' worktrees, `season.py merge-up` merged `--no-ff` green twice.
Belam VII left TWO unresolved design gaps (a) a worktree has no `.env` so a
secret-reading brief is silently unrunnable under `--branch`, (b) the graph
forks because a node minted inside a worktree is invisible from the main
checkout until merged. This experiment re-measures both on the current live
tree to confirm they are real (not speculation) and to pin the exact failure
modes, so whoever closes them has evidence to test against.

Three independent probes, all on the live tree, no code changed:

1. Live branches. `git -C .agi/worktrees/<w> rev-parse --abbrev-ref HEAD` for
the four current worktrees returned `loop/<slug>-<agent8>@s2` each —
exactly the ADDENDUM naming rule, so the mechanism is not only built, it is
currently in use by the seat.

2. Defect (a) — `.env`. Running `envfile.py --check` from the main checkout
passed and reported `ok: /home/ubuntu/work/agi/.env satisfies required
keys: OPENROUTER_API_KEY` plus `OPENROUTER_PROVISIONING_KEY is set (73
chars)`. Running the SAME command from inside worktree a00-645422d9
(`cd .agi/worktrees/a00-645422d9 && python3
/home/ubuntu/work/agi/extensions/agi/bin/envfile.py --check`) failed hard:
`PROBLEM: missing
/home/ubuntu/work/agi/.agi/worktrees/a00-645422d9/.env — copy .env.example
to it, chmod 600, and fill in: OPENROUTER_API_KEY`. Not a soft warning — a
hard `--check` failure. `.env` already lives only at the main root, resolved
as `<source_root>/.env` where source_root is the process's resolved root,
which under a worktree is the worktree. `find . -maxdepth 3 -name .env`
confirms only `./.env` (repo root) exists; no worktree has one.

3. Defect (b) — the graph fork. `comm` between main `nodes/` and worktree
a00-645422d9's `nodes/` shows exactly one file present only in the worktree:
`experiment/a00-a904792d-14a552.md`, and `git -C
.agi/worktrees/a00-645422d9 status --porcelain` shows it untracked (`??`)
next to ` M extensions/agi/bin/provisioning.py`, ` M
extensions/agi/bin/dispatch.py`, ` M .agi/config.json`. That node exists in
no checkout but its own worktree; it is invisible to the main checkout's
renderers, schedulers and links checks until someone merges it up.

## Evidence

Worktree branches (all four, one line each):
```
season/s2                                            (main)
loop/hypothesis-l3-openrouter-key-hea-a00-645422d9@s2
loop/hypothesis-l3w4-seat-rotation-lo-a00-9706efc2@s2
loop/hypothesis-l3w4-plan-master-a00-c6cb1216@s2
loop/hypothesis-l3w4-parent-branch-me-a00-bd778983@s2
```

Node counts: MAIN `find .agi/nodes -name '*.md' | wc -l` = 1560; each worktree
= 1561. The +1 in the worktrees is the unmerged fork node.

`.env` probe:
```
# main
[secrets] ok: /home/ubuntu/work/agi/.env satisfies required keys: OPENROUTER_API_KEY
[secrets] note: OPENROUTER_PROVISIONING_KEY is set (73 chars)
# worktree a00-645422d9
[secrets] PROBLEM: missing /home/ubuntu/work/agi/.agi/worktrees/a00-645422d9/.env
           — copy .env.example to it, chmod 600, and fill in: OPENROUTER_API_KEY
```

Fork probe (`comm` main vs worktree nodes):
```
./experiment/a00-a904792d-14a552.md        # worktree-only, untracked
```
`git -C .agi/worktrees/a00-645422d9 status --porcelain`:
```
 M .agi/config.json
 M extensions/agi/bin/dispatch.py
 M extensions/agi/bin/provisioning.py
?? .agi/nodes/experiment/a00-a904792d-14a552.md
```

Guest adversarial read of the two live halves: the _key-headroom_ kid lives in
a00-645422d9 and is editing `provisioning.py` — precisely the file that must
read `OPENROUTER_PROVISIONING_KEY` — while its worktree's `envfile --check`
hard-fails on `.env`. Defect (a) is not theoretical; it sits directly on the
one brief it hurts, and confirmed again the same way Belam VII first saw it.

Conclusion for the hypothesis: the CORE mechanism (per-parent `--branch`
worktree, ADDENDUM layer-agnostic naming, isolation, `merge-up --no-ff`
green gate) is built, live, and named exactly per spec — proven terrain.
What is NOT met is the promise that a brief using `.env` secrets and the
graph as one shared object work the same under `--branch`: both fail today,
in measured ways with the exact command a fix must flip to green.

## Agent Notes
Live-tree probes confirmed both Belam VII L3.32 design gaps are real: (a) worktree .env --check hard-fails (missing <worktree>/.env) on the very provisioning.py brief it hurts; (b) graph forks — worktree-only unmerged node experiment/a00-a904792d-14a552.md invisible from main. Core --branch+merge-up mechanism is live and named per ADDENDUM; the secret-&-graph-under---branch half is not yet met.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bd778983, L3.33): accepted as-is at inconclusive_lean_proved:60. I reproduced both headline probes independently before accepting — envfile.py --check from inside worktree a00-645422d9 hard-fails on missing <worktree>/.env, and comm between main and worktree experiment nodes shows exactly the one fork node a00-a904792d-14a552.md. The verdict is the right shape: the CORE claim (--branch worktrees, layer-agnostic naming per ADDENDUM, isolation) is live terrain, but the kid measured the remaining gaps rather than closing them, so proved would overclaim. Kept the self-citation as evidence run since this experiment IS the probe run.
<!-- THOUGHT:END -->

Parent review: both probes (worktree .env hard-fail; graph fork node a00-a904792d) independently reproduced by parent; verdict honest at lean 60; accepted, no demotion.
