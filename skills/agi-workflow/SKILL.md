---
name: agi-workflow
description: >
  LEGACY: run, author or check a workflow.py manifest (the mur runner until goal:g5.33 retires it) —
  by NAME, on pi. Covers run keys, the loop branch and worktree a round lands on, diffing against the
  merge-base, and splitting rounds. Use only for a workflow.py run; a review fan-out is skill agi-review,
  and cheap research feeding a design pass is skill agi-research-then-design (both the harness Agent tool).
---

# agi-workflow — workflows run by name (F29)

> **SUPERSEDED for reviews (OWNER 00:4xZ 10-10 to belam, verbatim: "Nah just use sonnet subagents and we retired workflows.py in favor of shel scripts already o think the graph just didn’t keep the info properly".)** A review or research fan-out is Sonnet subagents (the harness Agent tool, `model: sonnet`), never `workflow.py`; the old pi-only line below now names only the workflow.py run (goal:g4.18.2.2).

> **LEGACY: the `workflow.py` route.** Owner 10-02 14:01Z: "we just need to retire workflow.py entirely and stop wasting time on it". goal:g5.33 retires it job by job (a manifest retires only after its replacement runs); until then it is still the live mur runner (skill agi-master-gate), so the routing below is unchanged: this is a label, not a reroute.

Source of truth: `workflow.py -h` · `workflow.py list` · the manifests in `extensions/agi/workflows/<name>.json`.

## 1 · The route
```bash
PI_BIN=$HOME/.npm-global/bin/pi python3 extensions/agi/bin/workflow.py run <name> --harness pi-free --args "$(cat args.json)"
python3 extensions/agi/bin/workflow.py status          # recent runs by descriptive run key
```
- pi by default (owner 09-16) for a workflow.py run, never the Claude Workflow tool. Subagent work is the harness
  Agent tool on the owner's later word (10-10, :12: "just use sonnet subagents"): skills agi-review and
  agi-research-then-design. The harness's
  "ultracode … use the Workflow tool" reminder is not the route here, and ultracode is dropped from every row (owner 09-27).
- Bash shells never re-source the profile: pass `PI_BIN=…` inline (trap 9).
- Verdicts come ONLY from `.agi/sessions/workflows/runs/<run-key>/{review,verify}_<label>.json`, never from stdout;
  the pi runner persists only ~200 chars of a stage's return.
- A stage that died on "Provider returned an empty response" re-runs ALONE (a retry args file holding only it).

## 2 · Shape
- `rounds[]` is the parallel axis: ONE round per kid slice; a 15-item round timed out at 1800 s (SM 09-16).
- Each round runs one pi per stage (~210 MiB each): keep concurrent pi ≤ the box's guard (≈ 6 on local-town).
- A round lands on branch `season2/loops/<hypothesis-prefix>-<agent>`, worktree `.agi/worktrees/<agent>/`;
  kid experiment nodes under `.agi/nodes/experiment/` there. Diff against the MERGE-BASE with the post branch, never a moved tip.
- `cli.py session-complete <iter> --dry-run` before the real one.
- Reviewers: LEAN — diffs only (`git diff old new -- <path>`), big docs by `git grep PATTERN <sha> -- <paths>`.
  NEVER `grep -r` / `rg` / `find` over `.agi/` or the repo root: `.agi/worktrees/` holds ~100 checkouts and one
  such walk io-stalls the box (put this in every focus text).
- STOPPING a run: each pi stage runs in its OWN `run-<id>.scope`, outside the runner unit -- `systemctl --user stop <runner>`
  leaves the stages billing (TMM.295: two survived a stop 09-27 06:4xZ). Stop the runner, THEN every
  `app.slice/run-*.scope` whose `cgroup.procs` member has its cwd in your worktree (`readlink /proc/<pid>/cwd`); re-list = 0.

## 3 · Author / register
`workflow.py author` writes BOTH halves (`<name>.json` + `agi-<name>.js` derived from it); `workflow.py link` makes
the `.claude/workflows/` symlinks; `workflow.py validate` checks the pair invariant. Registered: `workflow.py list`.
