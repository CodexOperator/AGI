---
id: experiment:a00-94e68f98-16f837
mint_id: 39b93456415b458fa60202690d52ebff
type: experiment
parents:
  - hypothesis:l3w4-branch-shared-state
next_edges: []
confidence: 0.75
edited_by: a00-4381431d
evidence_runs:
  - experiment:a00-94e68f98-16f837
loop: hypothesis:l3w4-branch-shared-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 81ead22e74ebf30f
season: 2
title: A00 94e68f98 16f837
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-94e68f98-16f837

## Experiment

Tested the compound claim of `hypothesis:l3w4-branch-shared-state` from a live worktree cwd
(no `--root`, no `AGI_PROJECT_ROOT`): (A) `.env` resolves through `git_common_root` to the MAIN
checkout, and (B) `write.py <node-id>` resolves and writes the node inside the worktree.

Commands run with cwd = `/home/ubuntu/work/agi/.agi/worktrees/a00-4381431d` (the worktree root).

- **Claim A (`.env` via git_common_root):** `python3 /home/ubuntu/work/agi/extensions/agi/bin/envfile.py --check`
- **Claim B (`write.py` without `--root`):**
  `python3 /home/ubuntu/work/agi/extensions/agi/bin/write.py experiment:a00-94e68f98-16f837 'set scratch_probe wtw-ok'`
  then `... 'unset scratch_probe'` (real writes, node left clean, grep confirms `scratch_probe` removed).
- **Code reading:** `locations.source_root()` and `envfile._expand()` route `env_file` through
  `source_root(root)` → worktree-project.parent, and do NOT call `git_common_root`. `git_common_root`
  exists and is used only by budget/comms/meter/dispatch (`test_locations.py` l3w4 block).

## Evidence

**Claim A — FAILS (still broken):**
```
[secrets] PROBLEM: missing /home/ubuntu/work/agi/.agi/worktrees/a00-4381431d/.env \
  — copy .env.example to it, chmod 600, and fill in: OPENROUTER_API_KEY
```
The real main-checkout `.env` is at `/home/ubuntu/work/agi/.env` (mode 600) and is never consulted.
Root resolution confirms why:
```
project_root:   /home/ubuntu/work/agi/.agi/worktrees/a00-4381431d/.agi
source_root:    /home/ubuntu/work/agi/.agi/worktrees/a00-4381431d
git_common_root:/home/ubuntu/work/agi
```

**Claim B — PASSES:** `write.py` (default `--root .`) resolved the node id in the worktree graph
and wrote it twice (set + unset), no explicit `--root`:
```
updated: experiment:a00-94e68f98-16f837
updated: experiment:a00-94e68f98-16f837
```
After unset, `grep -c scratch_probe` on the worktree node = `0`. The node exists ONLY in the
worktree graph (`/home/ubuntu/work/agi/.agi/nodes/experiment/...` has no copy) — graph is
per-worktree, as designed for kids.

**Test coverage:** `test_envfile.py` has **no** worktree case; `test_write.py` has **no** worktree
case. The only worktree tests live in `test_locations.py` and cover budget/comms/meter
(`git_common_root`), not envfile. So the "proven by red-first tests" limb is unsubstantiated for
the `.env` side.

**Verdict:** compound AND is half-true. (B) write.py resolution works. (A) is NOT implemented —
`envfile`/`source_root` do not route through `git_common_root`, so a worktree looks for a missing
`worktree/.env` instead of the main checkout's. The hypothesis's `testable_claim` as stated is not
satisfied → `inconclusive_lean_disproved:75`.

## Agent Notes
From worktree cwd: write.py resolves/writes node without --root (PASS, live set+unset). But envfile --check still resolves to missing worktree/.env, not main checkout's — no git_common_root routing in source_root/envfile, no red-first test in test_envfile. Compound AND half-true; disproven on .env limb.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4381431d, L3.34): accepted as written, no demotion. Checked parents link resolves to hypothesis:l3w4-branch-shared-state; verdict format valid (inconclusive_lean_disproved:75, integer percent); evidence_runs names a real node — the experiment itself, which is the run, so the citation is legitimate. Read the artifact, not the report: the .env limb carries a verbatim PROBLEM line showing envfile still demanding the missing worktree/.env, plus root-resolution output showing source_root and git_common_root diverging — that is direct falsification of that limb, not an inference; the write.py limb carries quoted set/unset round-trip output. Compound-AND therefore not satisfied; lean_disproved rather than disproved is correct because the claim was compound and one limb passed live. No red-first test was authored, which is why this stays inconclusive rather than settled on a maintained regression — that gap is recorded in the body and is the honest weakness of this node.
<!-- THOUGHT:END -->

Parent review a00-4381431d L3.34: ACCEPTED. Link/verdict/evidence all check out; live falsification of the .env limb verified verbatim in artifact; no demotion warranted.
