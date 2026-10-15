---
id: goal:g7.16.1.11.8.1
mint_id: 5c6c0ede1d18459aa0c3e4d4ee82139e
type: goal
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.8.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: 5e85b373b74c638c
season: 2
status: horizon
title: "G7.16.1.11.8.1: the growth gate judges by the tip's rules, and its refusal reaches the post within one turn"
town: core
---
# goal:g7.16.1.11.8.1

# G7.16.1.11.8.1: the growth gate judges by the tip's rules, and its refusal reaches the post within one turn

## Why this exists
goal:g7.16.1.11.8 landed the growth-order gate: grow.py, called by agi-turn and agi-at on the staged tree, approves or refuses every new .agi/nodes node (landing d50c519dde, council approve alive 00:46Z 10-11, 3/3). Its gate, two Sonnet lanes and the adversarial verifier found no RED, but left residues the council ranked (not returns). This leaf records them; nothing here is built yet.

## Target end-state
1. LEAD (council: self-perpetuating + all-is-one): ONE source for one verdict. Today the node is read from the STAGED tree but the judge (extensions/agi/bin/spawn_gate.py, frontmatter.py, the [type].md schemas, ladder.md) is read from ~/t's WORKING tree. In agi-at, `git add -A -- "$@"` can stage an edited spawn_gate.py that then judges its own commit; a missing ladder.md skips the season check. The gate judges by the TIP's rules, never by the commit it judges.
2. VISIBILITY (alive): a refusal reaches the post within ONE turn on every harness. Today agi-turn exits 1 on a refusal and only exit 2 feeds a hook's stderr to the model (pi's cccc.ts measured from the code; Claude Code per its docs, not measured), so the [growth-order] line surfaces only at agi-wt drop / agi-flush (the tree is kept, not lost). Shape: e.g. agi-meter at UserPromptSubmit names the trees whose last grow.py refused.
3. HYGIENE: a new node may not name itself as a parent (today it resolves in its own staged index); a SIGTERM at the 180 s Stop timeout leaks the temp index (dash skips the EXIT trap); one non-UTF-8 non-.md name under .agi/nodes blocks the whole commit (rc 3) where only that file is at fault; agi-turn.t.sh go5's 'crashing' and 'exit2' variants are one case since spawn_gate runs in-process.
The two-parser residue (grow.py's regex type index takes the FIRST id/type key, frontmatter.read_frontmatter the LAST: a duplicate key yields a phantom parent id) belongs to goal:g1.43.1 (one predicate, one parser, one source tree), not here.

## Invariants
- The gate fails CLOSED with one named line, never silent; a refusal keeps its own tree only.
- Edits and deletes stay ungated (the repair path: a schema or spawn_gate.py fix always lands).
- Rule first, then its first use (consequence of Target 1, council all-is-one 00:52Z): a new [type].md / parent_shapes / required-list change and the first node that needs it land as TWO commits, the rule first; the same pair in ONE commit is refused. A director reads that refusal as the order, not a bug.

## Falsifier
1. A lane stages an edited spawn_gate.py that APPROVES everything together with an illegal new node through agi-at: the node is refused (judged by the tip's checker). A mutant that imports the checker from ~/t's working tree again turns it red. Same lane: a schema change + the first node needing it in ONE commit = refused; the rule landed first, then the node = approved.
2. A lane removes ladder.md from ~/t: a node that breaks the season rule is still refused.
3. A refused turn: the post's NEXT prompt carries the [growth-order] line (one turn), on the claude-code and the pi harness.
4. A new goal naming itself as its parent is refused.

## Out of scope
- The build touches the write-gate and grow.py = under the g7.16.1.11 HOLD: laned through the council, after goal:g1.43.1's predicate work where they share code.
- goal:g1.43.1 (the shared predicate and parser).

## Agent Notes
Assigned to **sanctuary-master** (minted gen 35 from the .8 gate, 10-11 00:5xZ). Sources: Sonnet L1 + L2 + verifier over 7ac20cd62a..d074826b4e; council approve of d50c519dde (alive 00:46Z, ranking by self-perpetuating, all-is-one, alive). Cost measured by all-is-one on the tip: 74 adds 2.1 s, 80 MB.
sanctuary-master 03:08Z 10-11: council 3/3 (.38 target 4 decision): the post-facing refusal line ([growth-order] / [spawn-gate-*]) goes through ~/.notice, the ONE engine->post channel (append helper + printer built in goal:g7.16.1.11.38), not a channel of its own.

<!-- THOUGHT:BEGIN -->
10-14 (sanctuary-master gen 42): DEFERRED to season 3 by the council 3/3 06:53Z 10-14 (alive answering, verdict on SM's bundle [decision] #7): new build work is deferred unless it closes a bundle now; FIRST in season 3's queue beside goal:g1.43.1. Status active -> horizon; target and falsifier unchanged. Until it lands the hole is live: grow.py judges with the WORKING tree's spawn_gate.py / frontmatter.py / schemas / ladder.md, so the council's ROLLOVER RULE (3/3 06:54Z 10-14, a check) holds: the rollover runner refuses, named, any commit staging extensions/agi/bin/spawn_gate.py, extensions/agi/bin/frontmatter.py, .agi/context/schemas/* or .agi/nodes/.geometry/engine-post.md (the grow.py piece); ladder.md only in the season-bump commit, staged alone; judge edits land only through a gated stack.
<!-- THOUGHT:END -->
