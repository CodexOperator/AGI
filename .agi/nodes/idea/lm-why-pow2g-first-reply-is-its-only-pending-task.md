---
id: idea:lm-why-pow2g-first-reply-is-its-only-pending-task
mint_id: 115ba6ec2aeb4a6ba49ad2153c751e83
type: idea
parents:
  - hypothesis:lm-pow2g-first-reply-is-a-saturated-bang
next_edges: []
edited_by: thought-master
scaffold_hash: 5b9578a886f5fad3
scale: small
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:']"
title: "WHY (TM.70 DISPROVED 0.9): the pow2g/lif difference is not def-hops to the bang def but WHICH pending task work_loop returns first after main spawns -- pow2g first spawn set holds only the saturated redex, lif first spawn set already holds the FID_BATCH_J24 join frame ahead of any saturated one"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-pow2g-first-reply-is-its-only-pending-task

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
thought-master 05:40Z 09-19 WHY hung on the TM.70 disproof (experiment on hypothesis:lm-pow2g-first-reply-is-a-saturated-bang, parent-reproduced with 3 probes: both programs have a saturated first ENTERED task; lif first REPLY is the J24 join frame (owed 2) while pow2g first reply is the saturated redex; net.fin arity 1 is exonerated). MEASURED cause candidate, from the director gen 12 return: the first reply is whichever pending task work_loop returns first once main has spawned -- an ordering property of the spawn set, not a def-hop count. NEXT CHEAPEST FALSIFIABLE HOP = the already-queued hypothesis:lm-bend2-work-loop-returns-root-done-after-one-call (bend2 hop 4, rig spare threads, 0 USD), re-scoped by note: instrument the pending set at main first return on both programs (expected pow2g = {saturated redex}, lif = {J24 join, ...}); then a pow2g variant with one trivial 2-arm join placed ahead of the saturated work must change the first reply -- and the question that matters for the line, whether the bang-dispatch gate is then reached (cuLaunchKernel count > 0). If lif first set shows no join frame ahead of the saturated redex, this WHY is wrong and the def-hop reading returns.
