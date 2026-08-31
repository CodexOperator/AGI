---
confidence: 1.0
goal_id: G4.1
goal_kind: subgoal
heading_level: 3
id: "goal:g4.1"
mint_id: 0ce6a836334e430a9f4a0f59c37ec82a
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G4.1: Parallel kids share one working tree and collide"
type: goal
---

Observed live 2026-08-22, by both kids of the same iteration independently.
Two kids doing **engine** work ran concurrently in one checkout: one was
rewriting `evidence_gate.py`, `metrics.py`, `cli.py` and `post_wire.py` while
the other was running the test suite against them. Consequences seen: the test
suite failed for several minutes on code neither kid had broken, and
`evidence_fraction` flipped between 0.365 and 0.035 on an unchanged corpus —
a stale-`.pyc` race against a file being rewritten underneath the interpreter.

Both kids diagnosed it correctly and neither corrupted anything, so the cost
this time was wasted motion and a briefly false test signal. **The failure
mode is that a kid reports a red suite it did not cause, or a green one it did
not earn.**

Kids writing *nodes* are naturally isolated — one file each. Kids writing
*engine code* are not isolated at all, and the closed loop (G6) makes engine
work the normal case rather than the exception.

Options, undecided: give each engine-writing kid its own worktree
(`isolation: worktree` already exists in the dispatch layer); serialise
engine-writing kids within an iteration; or partition by file ownership
declared in the brief. Measure before choosing — the worktree option costs a
checkout per kid and may not be worth it at two kids.

**Partial result, 2026-08-22:** file ownership declared explicitly in the brief
was tried across two iterations of two kids each. No collisions, and both kids
correctly attributed sibling breakage instead of claiming it. That is one
data point at two kids on disjoint files, not a solution — it says nothing
about kids that genuinely need the same file.

**Observed live again 2026-08-25, through the new door G6.1 opened, and this
time it cost work.** Two agents editing `payloads/` in one worktree: one ran
`grid.py checkout --all`, which silently reverted the other's uncommitted edits
to `payloads/extensions/agi/bin/grid.py` to the grid tip. It happened twice in
one session, in both directions.

**The defect was mine, not the collision's.** `checkout` is `git checkout .` on
the payload tree and it shipped without the dirty check `git checkout` itself
has. A payload whose bytes differ from the grid is *unrecorded work*, and
reverting it quietly is the one thing **G7** says must never happen. It now
reports `SKIP (locally modified)` and leaves the file; `--force` discards.

That is a guard, not a fix for this goal. File-ownership-in-the-brief was tried
again here and held for `nodes/` and for the files each agent owned — what it
could not cover is a **whole-tree command** that no ownership statement scopes.
That is a third option this goal had not considered: not "who edits what" but
"which commands are safe to run while someone else is working".

**A third instance, 2026-08-31, and it is the same third option again.** A pi
kid ran `git commit -A` and swept a sibling's half-written node and a human's
uncommitted engine edits into one commit labelled with its own node id
(`d34048aa1`, left in place as the record — nothing was lost, but the history
says something untrue). `git commit -A` is a whole-tree command exactly like
`grid.py checkout --all`: no statement of *who owns what* can scope it, because
it does not read ownership. Both contracts now forbid git in words, and
`goal:g1.4` stage 2 would remove the capability rather than the permission —
but the pattern is now three-for-three, and it is worth stating as a finding
rather than three anecdotes: **every collision this goal has recorded came
from a command whose blast radius is the tree, not from two agents editing the
same file.** File ownership has never once been the thing that failed.

## Open, and deliberately not decided here: worktrees under the hierarchy

The owner's sequencing, 2026-08-31: **finish automated worktree branching
before re-enabling the crons**, then ramp live slowly — one parent that spawns
two kids — rather than turning the schedule back on and finding out.

What is genuinely unresolved is not whether to use worktrees but **what a
worktree means once the tiers are nested**, and this goal predates the
hierarchy it now has to serve. The question was framed when "parallel agents"
meant two peer kids in one checkout. With a parent that spawns its own kids,
at least these are open and none has an obvious answer:

- **Whose worktree is it?** One per parent, with its kids sharing it — which
  reproduces this exact goal's problem one level down, just with a smaller
  blast radius. Or one per kid, in which case a parent reviewing its kids'
  work is reviewing across N trees and has to merge them before it can run a
  test suite over the result.
- **Where does review happen?** The parent's job is to read every node and run
  the gate. If kids wrote in separate trees, the parent needs their work
  *together* to judge it — so the merge is not a tidy-up step at the end, it
  is a precondition of the review, and something has to own it.
- **What does an iteration commit mean?** Today it is one commit carrying the
  thought and the code. Across N worktrees it is N branches that have to become
  one commit without a merge conflict deciding, silently, which kid's thought
  survived.
- **Does the grid change?** `refs/grid/*` versions a node independently of the
  commit that touched it, which may make the merge question smaller than it
  looks — the per-node history survives regardless of which branch the file
  landed on. Or it may hide the conflict rather than solve it. Untested.

`isolation: worktree` already exists in the dispatch layer, so the mechanism is
not the missing piece; the shape is. **This is flagged for a dedicated
brainstorming session with a small context, not for the next kid that reads
this node** — a half-chosen answer here would be built into both runtimes at
once via `goal:g4.3`, and would be expensive to reverse.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two additions, one factual and one structural.

The factual one is the third live collision, which is what turned three
anecdotes into a pattern this node had not stated: all three came from a
whole-tree command (`grid.py checkout --all`, twice, and now `git commit -A`),
and none came from two agents editing the same file. That inverts the goal's
own framing — it opens by describing concurrent *edits* and lists
file-ownership as the leading mitigation, when file ownership has never been
the thing that failed. The options list is left intact rather than rewritten,
because the measurement it asks for still has not been made and reordering it
on one more data point would be the same overclaiming this repo keeps
catching.

The structural one is the owner's sequencing decision plus an honest record
that the goal predates the hierarchy. Written as four questions rather than a
recommendation on purpose: the owner asked for the uncertainty to be recorded,
not resolved, and `goal:g4.3`'s dispatcher would bake whichever answer exists
into both runtimes at once. Naming the questions is what makes the later
brainstorm cheap; guessing now is what would make it expensive.
<!-- THOUGHT:END -->
