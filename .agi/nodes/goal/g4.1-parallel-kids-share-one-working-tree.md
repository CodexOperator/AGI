---
id: goal:g4.1
mint_id: 0ce6a836334e430a9f4a0f59c37ec82a
type: goal
parents:
  - goal:g4
confidence: 1.0
edited_by: owner
goal_id: G4.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: L1.07
title: "G4.1: Parallel kids share one working tree and collide"
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
Owner direction, 2026-09-03: this goal is the PREREQUISITE for how concurrency is meant to be used, and L1.03 measured why. At spawn.parallel 8 aimed with a single --target, six of eight kids wrote substantially the same hypothesis -- every slot got the same 2-hop subtree and independently picked its most salient open thread, because none can see the others work in flight. So spawn.parallel is a THROUGHPUT knob, not a coverage knob. The owner intent was never one target: it is several chains built simultaneously, whole sections of graph at a time -- parallel experiment -> mvp -> build chains. That is what worktree-per-kid is for, and it is the real gate on ramping past 8: without isolation, concurrent agents touching the same node or the same source file break each other work. WHEN SAME-TARGET CONCURRENCY IS RIGHT: when a goal is genuinely open-ended and the point is to explore competing options. The owner read of this tree is that the vast majority of goals do not need it -- they are clear-cut feature goals where the direction is already obvious and the chain just needs standard validation, straight through to a node edit, or verdict -> mvp -> new node. A handful may benefit from exploratory fan-out; most will not. Aiming every slot at one target should therefore be the exception a director chooses, not the default a run falls into.
<!-- THOUGHT:END -->