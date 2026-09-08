---
id: hypothesis:l3w4-handoff-sections-claimable
mint_id: 578ffecc5f7e4e55b8e7208a98ed8e9b
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: f47591ce2a15fd53
season: 2
testable_claim: "After the change, a seat reads only the handoff sections it claims and writes only the sections it holds: a claimed section is served alone at a fraction of the whole-file token cost, two seats holding different sections can write concurrently without clobbering each other, and the prime still reads and renders the whole file unchanged - proven by measured token counts for a sectioned read against the whole file and by two concurrent section writes both surviving."
thought_session: belam-S1-L3-XI
title: "HANDOFF.md is read whole by every reader and written only by the prime, so a seat cannot be cheap and cannot help write it: sections must be separately claimable to read and to write"
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-handoff-sections-claimable

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

THE OWNER ASKED FOR THIS, 2026-09-08, verbatim: "Each one can claim a section of handoff to read to conserve individual context space" — said while asking how close a perpetual Sonnet quorum is to helping dispatch parents and write handoff briefs on the prime's behalf.

THE MEASUREMENT THAT MAKES IT URGENT. `HANDOFF.md` is ~232KB, roughly 46,000 tokens, on a file every cold reader is instructed to read first. A Sonnet seat that reads it whole has spent a large fraction of its usable context before doing anything. That is the single largest fixed context tax in the ladder, it is paid per seat per session, and it is why seats have stayed a one-at-a-time luxury: **the handoff is what makes a seat expensive.** Cut it and a quorum becomes affordable.

TWO HALVES, AND THE SECOND IS THE HARDER ONE.
1. CLAIM TO READ. A reader asks for the sections it needs and gets those, not the file. The prime still reads and writes the whole thing.
2. CLAIM TO WRITE. The owner's ask is that seats write handoff briefs ON THE PRIME'S BEHALF. Today exactly one writer is safe because the file is rewritten whole; two seats writing concurrently would clobber each other, and the losing write would vanish silently — the failure shape this project has been bitten by three times already this loop. A section held by one writer at a time is what makes delegated handoff writing possible at all. Without half 2 this brief only saves tokens; with it, it unblocks the quorum.

WHAT TO BUILD.
- Stable section identity. The file already has natural sections (`## §0`, `## §0.7`, `### 🔴 Where it stops — ...`, `## §4`, `## §5`, `## §6`). Anchor them by a name that survives a rewrite, and DO NOT invent a new document format or reorder the file — every generation reads it and a reshuffle costs more than it saves. A reader must still be able to `cat HANDOFF.md` and get exactly what it gets today.
- A claim, held by one holder at a time, released on exit, and visible. `spawn_budget` already models exactly this shape for agent slots and `send.py` already models per-reader cursors — read both and follow whichever fits rather than inventing a third locking scheme. Say in your node which you chose and why.
- A read path that serves one or more claimed sections and reports what it cost. Put real token or byte numbers for a sectioned read against the whole file in your node; a claim that this saves context is worthless without the two numbers side by side.
- A write path that refuses a write to a section the caller does not hold, loudly, naming the holder. Fail closed. A silent lost handoff write is strictly worse than a refused one.
- The prime is exempt and stays exempt: it reads whole and may write whole. Do not build anything that can lock the prime out of its own scratchpad.

DO NOT change what any section SAYS. You are building addressing and locking, not editing content. Do not delete the 2026-09-06 owner plan or any `§6` owner-answer item — those are permanent and carried forward in place by every successor.

PROVE IT. Two measured token counts (one section vs whole file). Two concurrent section writes from different holders, both surviving, with the file valid afterwards. One refused write naming the holder. One `cat HANDOFF.md` showing the file still reads exactly as before. Paste actual output.

DO NOT touch `workflow.py`, `rotate.py`, `dispatch.py`, `brief.py`, `cli.py` or `zoom.py` — other parents hold them. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted straight from the owner's sentence, and the framing deliberately promotes their aside into the load-bearing half. They said sections would conserve context; the measurement says the handoff is the reason a seat is expensive at all, so this is not an optimisation of the quorum, it is a precondition for one. The write-claim half is not in the owner's words and is added because delegated handoff writing without it is a silent-clobber generator, which is the exact failure shape that has cost this loop three separate defects.
<!-- THOUGHT:END -->
