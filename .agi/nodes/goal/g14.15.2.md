---
id: goal:g14.15.2
mint_id: ed86526b91ab494e8e424410a07a9b29
type: goal
parents:
  - goal:g14.15
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G14.15.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 647b2ceff588ffe8
season: 2
status: active
tags:
  - local-maxxing
  - telepathy
  - swarm
title: "G14.15.2: SWARM TELEPATHY -- k same-model instances, each holding one slice of a long document, exchange captured KV spans and a shared jev-style ranking until one decoder instance answers over the whole document at or above single-instance long-context quality (owner 01:3xZ 09-21)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.15.2
## Agent Notes
**Owner source (2026-09-21 01:3xZ, verbatim on goal:g14, relayed via goal:g14.15):** "And also use the kv cache telepathy to let smaller models swarm together; with each one holding a piece of the total context and all coordinating together via kv cache messaging until the proper kv cache results emerge that can be fed into a decoder. So like a swarm of jevs almost weighing opinions together on which kv caches matter more where until a final ordering and layering settles into place."

**Commits to.** The multi-instance half of G14.15, its fourth chunk, on the resident 9B (k copies) at 0 USD GPU: SWARM -- k same-model instances, each holding one slice of a long document, exchange captured KV spans (via G14.15.1's capture/surface tool) and a shared ranking until one decoder instance answers a question over the whole document at >= the single-instance long-context answer quality. The jev-style weighing: each instance scores every span it receives; the ordering is the consensus.

**Invariants.** Same measurement discipline as G14.15.1 (fidelity, compute, bytes, wall on the same served 9B, n_batch/ubatch pinned). Cross-model swarms (different weights) are explicitly OUT of scope until a C2C-style projector exists -- banked, not attempted here.

**Falsifiers.** Falsified if the swarm's answer quality is below the single long-context instance at equal total tokens.

**Done when.** One measured k=2 swarm result exists, proved or disproved.

**First chunk.** None minted yet -- blocked on `goal:g14.15.1` (self-telepathy) landing its own chunks (1)-(3) first: a swarm needs the capture/surface tool and the ranking to already exist before k instances can exchange spans with each other. Queued behind G14.15.1's TEL.01 and whatever chunks (2)-(3) become.

director-thought 08:0xZ 09-21 -- TEL.03 landed, mur accept_with_residue (mur-tel-03, 11/11 conjuncts, one line-citation fixed):
```
census      of the boxs 5 GGUFs: Bonsai27B/Qwen3.5-9B/Qwen3.5-35B-A3B (qwen35/qwen35moe, IMROPE) CANNOT shift KV -- only Bonsai-1.7B (qwen3, NEOX) can. Qwen3.8-27B/0.6B/4B are simply ABSENT from the box, not measured
implication a KV-span-exchanging swarm cannot include the towns three bigger local-maxxing candidates under stock llama.cpp @930e2fa -- they need the saved-TEXT-plus-tail-KV fallback same as g14.15.1s own chunks 2-3; only a 1.7B-class member could join a real KV-shift swarm today
caveat      the CURRENTLY-DEPLOYED server has since switched to a prism fork (build 10685/7dffb158d), not the pinned stock upstream the census checked -- get_can_shift on that fork is unverified, flagged by the mur, not yet checked
residue     one wrong upstream line number (3020 vs the real 3025) in the shared arch-chain-excerpts.txt + this rounds own table -- fixed in place, verdict itself was never affected (qwen3 stayed correctly in the NEOX group either way)
```
