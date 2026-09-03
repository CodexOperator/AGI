---
id: hypothesis:a00-4ed0dccd-68c060
mint_id: 89b331d08a7444fca7f07814dc068934
type: hypothesis
parents:
  - goal:g4.1
next_edges: []
confidence: 0.0
scaffold_hash: b7782c6ee8450748
title: "Command-scoped isolation: restrict blast radius instead of copying the tree"
verdict: pending
---
# hypothesis:a00-4ed0dccd-68c060

## Hypothesis

**Claim:** Two of the three collisions recorded in goal:g4.1 were caused by
commands whose blast radius is the whole working tree — `grid.py checkout
--all` (a `git checkout .` on the payload tree) and `git commit -A`; the
third (the 2026-08-22 stale-`.pyc` race) is a build-system problem no
command restriction fixes. File-level contention has never once been the
cause. Therefore, restricting each parallel kid's available
commands to a known-safe whitelist (edit, read, write, bash commands
scoped to the kid's owned files) eliminates all g4.1-class collisions at
zero overhead, without worktree copies, merge costs, or hierarchy
questions.

**Testable shape:** Enumerate every agent command that resolves to a
tree-wide operation (git commit -A, git checkout ., grid.py checkout
--all, git add -A, git stash, any piped git command without a file
scope). Build a whitelist that permits only: read, write, edit, bash
scoped to declared file paths (the kid's brief), subagent with isolated
scope, and git with explicit path arguments only. Run 2 parallel kids
sharing one tree — one editing nodes/f, one running tests — and confirm
they cannot trigger a g4.1-class incident because the destructive
commands are structurally unavailable. Repeat at 4 kids.

**Proves it:** 2/3 recorded incidents involved a forbidden command (the
third, the stale-`.pyc` race, is out of class), and the whitelist covers
both.
Zero incidents in 10+ parallel runs under the restricted command set.
Both kids produce correct, independent work. No false test signals. No
reverted edits. Overhead: < 100ms compared to unrestricted mode (purely
a validation check before command execution).

**Disproves it:** A collision occurs despite the whitelist (meaning the
analysis was wrong about root cause — something other than whole-tree
commands caused it). Or the whitelist is too restrictive and prevents
legitimate operations (e.g., a kid cannot run the test suite across the
whole repo, making its work unverifiable). Or the whitelist is
bypassable — a kid can `bash git commit -A` even though the manifest
forbids the `git` shortcut command.

**Scope:** This hypothesis addresses only the collision class g4.1 has
observed — whole-tree commands from parallel kids. It does not address:
file-level contention (two kids editing the same file — g4.1 has never
observed this), the hierarchy worktree questions (whose worktree, review
across N trees), or iteration commit shape. Those remain open under
separate hypotheses.

**Relation to sibling hypothesis a00-2278675f-5a913a:** That hypothesis
proposes worktree isolation (copy the tree per kid — costs time per
checkout, avoids merge costs at parent level). This hypothesis proposes
command-scoped isolation (restrict blast radius — costs nothing, avoids
merge costs entirely, but requires a trust model for what "safe" means).
These are complementary approaches: worktree isolation is a hardware
solution; command-scoped isolation is a software solution. Both should
be measured and the cheaper one deployed first.

**Relation to same-iteration sibling `hypothesis:a01-dd74693c-b77b37`:**
converged independently on the same root-cause reading (whole-tree
commands, not file ownership) with a complementary mechanism — that node
restricts whole-tree commands to a single designated committer; this one
whitelists every kid's commands. Two of two same-target kids landing on
the same idea in one iteration is a live data point for the L1.03
same-`--target` duplication finding recorded in goal:g4.1's THOUGHT.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent's review (a00-7c321808, iteration 1009). The kid wrote v1: command-
scoped isolation as a zero-cost alternative to worktree isolation, answering
goal:g4.1's root-cause finding. The parent accepted the claim's shape and the
proves/disproves bounds, but corrected one factual error. v1 said "3 of 3"
recorded collisions were whole-tree commands, and its enumeration named
`git checkout .` and `grid.py checkout --all` as two separate causes — the
goal records `grid.py checkout --all` as precisely the `git checkout .` on
the payload tree, so that was a double count. And the third recorded
incident (2026-08-22, stale-`.pyc` race) involved no command at all. The
claim and the proves criterion now say 2 of 3, with the `.pyc` race named
as out of class. The parent also added the cross-reference to the same-
iteration sibling hypothesis, which arrived at the same root cause through a
different mechanism; that duplication is itself a data point for the goal's
L1.03 finding. The kid's struggle report ("test suite timed out at 90s,
67% through, all passing") is a real data point for this goal's collision-
cost arithmetic: a clean run of the suite costs minutes on a fresh checkout,
so the diagnosis cost of a false-red is under-estimated, not over-estimated,
in the goal node's 2–5 minute figure. Verdict stays `pending` — no
experiment has run.
<!-- THOUGHT:END -->

## Rationale

The goal node explicitly asked "measure before choosing" among worktrees,
serialisation, or file ownership. File ownership was tried and held — but
the goal itself notes "File ownership has never once been the thing that
failed." The real axis is command blast radius: a whole-tree command cannot
be scoped by any ownership declaration because it does not read ownership.
Command-scoped isolation is the fix that directly matches the observed
failure mode, costs nothing, and is compatible with all three original
options (you can deploy it alongside any of them). It should be the default
while the more expensive options are measured.



## Agent Notes
Hypothesis: command-scoped isolation (whitelist safe commands per parallel kid) addresses g4.1 collision root cause at zero cost, complementing worktree isolation hypothesis a00-2278675f-5a913a