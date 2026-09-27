---
name: agi-dispatch
description: >
  Drive a goal through dispatched parents and judge what comes back: decompose, dispatch a
  parent with the exact tier/role flags, the spawn bound, the behind-origin refusal, kid
  rebriefs, and season.py judge (continue | adjust | done). Use whenever a director spawns
  a parent or kid, or judges a parent's report against its plan node.
---

# agi-dispatch — decompose ▸ dispatch ▸ judge

Source of truth: `dispatch.py -h` · `season.py judge -h` · `spawn_budget.py status`. A director JUDGES; it never does kid work.

## 1 · The loop
```
goal:gX ──decompose──▶ goal:gX.a  goal:gX.b          write.py create goal … (skill agi-goal)
                          │          │
                       parent     parent             dispatch.py (below)
                          │          │
                       outcome    outcome
                          └────┬─────┘
            season.py judge <outcome-id> --against goal:gX      → continue | adjust | done
```
Nest rather than widen; sketch the leaves first; spawn parents ONLY against sketched leaves.

## 2 · Dispatch a parent
```bash
python3 extensions/agi/bin/dispatch.py <project_root> <iter_n> --tier parent \
  --role parent --ladder-tier 0 --detach --target <goal-or-hypothesis-id> [--dry-run]
```
- `--role parent --ladder-tier 0` is DELIBERATE: `--role` defaults to `kid`, so a bare `--tier parent` resolves
  the tier-0 KID row and spawns the parent on the wrong model (hypothesis:l3w1-tier0-director-brief).
- Exit 3 = your post is behind `origin/season2/main`: that refusal IS the behind check (F9) — no hand fetch + rev-parse.
- `--push-further` re-dispatches at `--target` from its `push_further` text; refused at an overview/vision/moral node.
- Bound: `spawn_budget.py status` (live agents vs the tree-wide cap); `provisioning.py status` (per-spawn keys).
- A director dispatches from ITS OWN worktree; live parents ≤ the cap cell its master names (local-maxxing: `values.local_maxxing.de_live_parents`), ≤ 5 kids each.
- A CORRECTIVE is cut from the round's own loop tip: `git worktree add -b de-base-<N> .agi/worktrees/de-base-<N> <loop tip>`, dispatch from there with `--orders <file> --from <post>` (kids get an empty `.git`: "merge the loop branch first" never works). The whole corrective flow — verdict read, triage, the orders on the node: skill `agi-corrective`.

## 3 · Kids and rebriefs (F31)
A parent that answers a kid's `rebrief_request` in-node dms its director the answer line
(kid id, N/C, proceed-with-N | cut) BEFORE the kid resumes. A kid past 2× its budget with no such dm in your
inbox = self-authorised: cut it. A kid's work is the kid's — brief, do not steer.

## 4 · Judge
`season.py judge <report-id> --against <plan-id> --actor <post>` stamps the alignment:
`continue` (keep going) · `adjust` (reword the plan node) · `done` (close the plan, mint the outcome).
Judge against the plan node's PARENT (the lens this tier sees through), from the report AND the bytes.
Reviews of a round run BY NAME on pi (skill `agi-workflow`), never inline.

## 5 · Orders and harvest — traps already paid for
| trap | do · never |
|---|---|
| nproc | never `prlimit --nproc` in orders: RLIMIT_NPROC is PER-USER → EAGAIN in unrelated tests; the per-round bound is the scope's TasksMax (`spawn.tasks_max`) |
| fork-bound | a test that spawns python/pytest runs under `timeout` + a process cap; never a pytest that re-collects its own dir; a conftest never exec's another (DH.419: 127 procs) |
| anon-quote | a scrub round's own review re-leaks the token by quoting its grep PATTERN: orders say write `<user>` in patterns and THOUGHT |
| uncommitted | a parent can exit leaving edits uncommitted in a KID worktree or its OWN (DH.486/488/489/495): `git status -s` in both at every harvest |
| kid-node | land such an edit ONLY if its bytes == its last write-log sha (`.agi/sessions/write-log.jsonl` in that worktree): commit on the kid branch, merge into the loop branch, name actors + rows; unlogged = never hand-land (TMM.268) |
| no-dm | a parent's harvest dm can be lost or blind to `--owns` kids: reconcile by branch + `spawn_budget.py status`, never by inbox alone |
| vanishing-wt | a CLEAN round worktree is pruned while you test in it (06:25Z 09-27: 58 phantom help-smoke failures, then "file or directory not found"): land its uncommitted edits FIRST, then test on `git worktree add --detach .agi/worktrees/de-h<N> <tip>` |
