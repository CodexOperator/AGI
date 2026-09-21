---
id: mvp:prose-derives-from-the-command-node
mint_id: 10d19b3c96b14e41a995a39cd34c8105
type: mvp
parents:
  - verdict:declared-commands-delete-four-copies
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: e5442aa40ebf527e
season: 1
status: open
thought_session: season
title: The command lists in prose derive from the node instead of restating it
---
# mvp:prose-derives-from-the-command-node

## What this must satisfy

`verdict:declared-commands-delete-four-copies` says plainly what its own title
overstates: **the four prose copies are not deleted.** iteration 111 made a
fifth copy that happens to be executable. Four copies plus one source of truth
is worse than four copies, because now there is a right answer *and* four
places that can disagree with it.

### The interfaces

- A marked region in `CLAUDE.md`, `QUICKSTART.md` and `skills/agi/SKILL.md`,
  regenerated from `.geometry/commands.md` — the same
  `<!-- BEGIN … END -->` discipline the `THOUGHT` block already uses, so the
  authored prose around it survives.
- `commands.py render --target claude|quickstart|skill` writes those regions.
- The `--check` inverse: exit non-zero when a region disagrees with the node,
  so drift is a failing command rather than a discovery.

### The invariants

1. **Authored prose around the region is never touched.** `goal:g2.10` is the
   standing proof of what a generator that rewrites a whole document does to
   authored content.
2. **The node stays the source.** Editing the prose region is not a way to add
   a command; the `--check` inverse makes that a failure rather than a silent
   revert, which is the failure `GOALS.md` hand-edits already produce.
3. **A project with no commands node renders nothing** and the documents stay
   exactly as authored. Absence stays supported.

### The falsifier

Add one command to `.geometry/commands.md`, run the render, and all three
documents gain it with nothing else changed — verified by diff. Then edit one
document's region by hand and `--check` exits non-zero naming the file. Then
delete the node and re-render: the documents are unchanged rather than emptied.

### Why this is not `goal:g6.9` again

`GOALS.md` renders from goal *bodies*, and a hand-edit to it vanishes at the
next `--smoke` **with no warning** — a failure this project confirmed by losing
one. The `--check` inverse is the lesson applied: the same derivation, plus a
command that says so before the loss.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The "four plus one is worse than four" framing is the reason this is an mvp
rather than a nice-to-have. Iteration 111 improved the situation on one axis
(there is now a right answer) and worsened it on another (there is now one
more place to disagree). Leaving it there would be the worst available resting
point, and naming that plainly is more useful than a task list.

The `--check` inverse is lifted directly from `snapshot-goals.py --render
--check`, which exists because this project already lost a hand-edit to a
generator once. Reusing the shape rather than inventing one is the whole point
of noticing the precedent.
<!-- THOUGHT:END -->