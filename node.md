---
id: hypothesis:l4-the-assembled-brief-names-the-session-dir-as-the-only-scratch-dir
mint_id: 05e82e6c6f654be4a83900502d861f62
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 03a51bb3beca67a0
season: 2
testable_claim: "Measured by master-sensei 2026-09-16 11:0xZ on SL7.128: a parent or kid reads ONLY brief.py assemble() (the spawn.json brief) - no schema or ladder prose reaches it - so the kid scratch-dir rule has no template surface; it is one code clause. Today: SL7.128 parent a00-a0f3395e staged .agi/tmp/sl7128-kid-brief.md plus 3 untracked probes in .agi/tmp/ because .gitignore:118-120 literally points there; 27 files are tracked under .agi/tmp in MAIN; three hand fix-ups on record dropped parent strays (8cc3b8e9c, dc6c33b6a, a34a1a0f9). Claim: brief.py session_line (brief.py:1119-1121, printed for every tier) gains one clause - the session dir is the ONLY scratch dir: probes, kid briefs, notes, result files go under it, never .agi/tmp/ or the repo root, anything outside it is a stray the harvest drops; the .gitignore:118-120 comment is repointed to the session dir; a test asserts the assembled brief for each tier names session_dir as the only scratch dir. Sibling of hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate (SM.40, live - not folded in mid-round). Ceiling 15 production lines, one kid, brief.py + .gitignore comment + one test."
title: L4 the assembled brief names the session dir as the only scratch dir
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-assembled-brief-names-the-session-dir-as-the-only-scratch-dir

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.42 reviewed by sanctuary-master 11:2xZ: ACCEPT at the parent inconclusive_lean_proved:80 (post branch 1c7a04cdd). Parent corrected the brief before dispatch: the cited brief.py:1119-1121 is inside _advisor(), so the kid threaded a shared _scratch_dir_clause() into _kid() and _parent() via the session_dir dispatch.py already passes; no-op when session_dir absent; parent fixed its own .gitignore comment typo in review; 128+155 green; ~24 vs 15 lines (1.6x) disclosed accurately by kid and parent. The claim wording each tier is broader than tested (kid+parent only, by design) - accepted as such.
