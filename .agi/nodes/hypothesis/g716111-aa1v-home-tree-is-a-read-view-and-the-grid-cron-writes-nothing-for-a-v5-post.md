---
id: hypothesis:g716111-aa1v-home-tree-is-a-read-view-and-the-grid-cron-writes-nothing-for-a-v5-post
mint_id: fcd8bc1b291e44a3b3c27e5ea8e8e1ef
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 7d1439e495770c30
season: 2
testable_claim: "In a live v5 turn a stray edit made directly in ~/t prints `[out-of-tree] ~/t has N unversioned change(s)` and lands nowhere (V2); 24 h after the switch refs/grid/* gains 0 refs from a v5 post, and with AA3's cron retirement 0 from anyone (V3); because a payload can only change inside its node's tree, every code change is versioned WITH its node by construction."
title: "AA1.V: ~/t is a DETACHED read view of the post's tip (a stray edit there is reported `[out-of-tree]`, never committed), agi-link retires, and a v5 post adds no refs/grid refs"
town: core
---
# hypothesis:g716111-aa1v-home-tree-is-a-read-view-and-the-grid-cron-writes-nothing-for-a-v5-post

## Measured
- doc:rse-aa1-boxes AA1.V honest limit (1): ~/t becomes a read view: a post that edits there loses nothing (the edit stays in ~/t) but versions nothing, and is told so every turn; the briefs and agi-node-write's replacement must say 'edit in agi-wt pull's directory'. (2) with ~/t detached, agi-flush's `git merge trunk` is replaced by merge-tree + commit-tree on a DOWN handoff (AA2: the child's tip moves only on the parent's handoff mail).
- Scratch G5 (a stray edit in ~/t -> `[out-of-tree]` on stderr, NOT committed), G9 (trunk untouched, 0 refs/grid).
- This changes how EVERY v5 post (DG1 included) edits nodes: the skills and briefs must change in the same round (goal:g7.16.1.11.14).

## CLAIM
In a live v5 turn a stray edit made directly in ~/t prints `[out-of-tree] ~/t has N unversioned change(s)` and lands nowhere (V2); 24 h after the switch refs/grid/* gains 0 refs from a v5 post, and with AA3's cron retirement 0 from anyone (V3); because a payload can only change inside its node's tree, every code change is versioned WITH its node by construction.

## Dispatch line
config-max: none / template-max: the brief line 'edit in the node's tree' / code: agi-turn's `git checkout --detach` + `[out-of-tree]` report (already in the 1,074 B).

## FALSIFIERS
AA1.V2 a stray ~/t edit in a live turn prints [out-of-tree] and lands nowhere · AA1.V3 24 h after the switch refs/grid/* gains 0 refs from a v5 post · negative: `git grep -n 'agi-link' -- <engine-post pieces>` returns 0 hits after the retirement.

## TESTS
scratch G5 + G9 on the built bytes; a live 24 h refs/grid count (shared with AA3's V1).

## FILE SCOPE
agi-turn (the detach + report), the retirement of agi-link, the brief/skill text (goal:g7.16.1.11.14). Never delete a refs/grid ref.

## CEILING
1 parent · kids <= 1 · 0 B in the zygote · regular review. HORIZON behind AA1.V's commit-surface hypothesis.
