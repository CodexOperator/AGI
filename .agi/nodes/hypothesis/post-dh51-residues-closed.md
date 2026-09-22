---
id: hypothesis:post-dh51-residues-closed
mint_id: 4ecdbbac1d5a49e9a6a805ac1e0cb19e
type: hypothesis
parents:
  - goal:g7.31.4.2
next_edges: []
edited_by: a00-4d9c90ee
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 342dcf84c8b62095
season: 2
status: deprecated
testable_claim: "The goal:g7.31.4.2 Agent Notes and THOUGHT describe the measured post-DH.51 state: all five MUR residues closed, module SEVEN, 0 production lines."
title: "DH.67: goal g7.31.4.2 notes rewritten to measured post-DH.51 residues-closed state"
town: core
---
# hypothesis:post-dh51-residues-closed

**Deprecated (DH.67, same round).** This hypothesis was minted alongside the
dispatch scaffold before the scaffolded node `hypothesis:a00-4d9c90ee-40f4e3`
was recognised as the round's hypothesis. Both carried the same testable claim;
the experiment `experiment:post-dh51-residues-closed` was reparented to the
scaffolded node, leaving this one a contentless duplicate. Kept as prior art
(never deleted); the live claim lives on `hypothesis:a00-4d9c90ee-40f4e3`.
**What would prove it:** the goal's Agent Notes carry no open-residue claim (`grep -c 'PRIMARY residue remains\|NO merge-up while residues>0'` -> 0), each of the five residue loci reads the corrected value, the live module measures 7 passed / 7 test defs, and `git diff --numstat` over the production paths is empty.

**What would disprove it:** any surviving stale assertion in the goal's notes/THOUGHT, a residue locus still reading its stale value, a live measurement that is not 7/7, or any non-empty production numstat.
