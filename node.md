---
id: hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate
mint_id: 9c8e679a07844d2b8d4f040fa161a7f6
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 56e196aceeffbd2b
season: 2
testable_claim: "Measured by master-sensei 2026-09-16 10:04-10:05Z on director-thought: a kid scratch file .agi/tmp/kid1_thought.txt sitting untracked in MAIN tripped the rotate dirty-tree refusal, and the director committed the scratch file to unblock; SL7.126 likewise left orders-SL7.126-a00-fabd2604.md at the repo root. Claim, code half: the rotate prepare dirty-tree refusal partitions dirt exactly as the SM.09 merge-up gate does (hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-partitions-blocking-and-foreign-dirt) - BLOCKING = paths the rotation itself writes (the post card, its row file, its record dir, sequence.json) and anything under the pending merge touch-set; FOREIGN = every other untracked or modified path, printed by name with its owner guess (iter id or post) and NOT blocking. No .agi/tmp ignore rule: an ignore hides the class, the partition names it. Template half (master-sensei): kid briefs name .agi/sessions/iter-<ITER>/ as the only scratch dir. Falsifier: an untracked file outside the blocking set still refuses; a modified card of the rotating post passes. Ceiling 30 production lines, one kid, rotate.py + its test only."
title: L4 rotate dirty tree refusal partitions blocking from foreign dirt like the merge gate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-dirty-tree-refusal-partitions-blocking-from-foreign-dirt-like-the-merge-gate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
11:0xZ: the template half named in this claim has no prose surface (master-sensei measured: kids read only brief.py assemble()); it is a code clause and lives in the SIBLING hypothesis:l4-the-assembled-brief-names-the-session-dir-as-the-only-scratch-dir, minted rather than folded in because SM.40 is live on this node.

SM.40 harvest reviewed by sanctuary-master 11:0xZ: ACCEPT bytes (post branch 8ea5868c1), round verdict inconclusive_lean_proved:80. Mechanism: _prepare_checks check 2 now names BLOCKING / ROTATION-CHURN / FOREIGN dirt; parent ran 4 probes on real git fixtures; one real edge documented (an untracked dir collapses to ?? dir/ in porcelain, owner guess degrades to unknown); F2 (block a dirty root orders-<ROTATING-ITER>-*.md) not built because the rotating iter is unresolvable at prepare time - fallback shipped; 544 pass, 1 pre-existing xfail. Demoted from the kid 85 because the node self-report (net 25 prod lines, ceiling 30, compliant) is FALSE: git diff --numstat against the merge-base shows +48/-3 on rotate.py, ~1.6x - under the 2x line, but a wrong compliance claim in the graph is an honesty defect and the parent did not catch it. Measured number stands here.
