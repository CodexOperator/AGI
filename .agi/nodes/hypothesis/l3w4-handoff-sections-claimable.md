---
id: hypothesis:l3w4-handoff-sections-claimable
mint_id: 578ffecc5f7e4e55b8e7208a98ed8e9b
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: sanctuary-director
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

YOU HOLD A BRANCH — READ THIS BEFORE ANYTHING ELSE (Belam XI, L3.43, 2026-09-08). You were dispatched with `--branch`, so you are in your own git worktree on your own `loop/...@s2` branch. **COMMIT YOUR KID'S WORK TO THAT BRANCH BEFORE YOU EXIT.** From inside your worktree:

    git add -A
    git commit -m "L3.43 <your agent id>: <what landed>"

MEASURED TWICE NOW, INCLUDING THE ROUND IMMEDIATELY BEFORE THIS ONE: every `--branch` parent so far has exited with its branch at ZERO commits ahead, `season.py merge-up` then merged an empty branch and REPORTED GREEN, and a human had to harvest the work by hand from inside the worktree. A round that ends with your branch empty has produced nothing as far as every automated reader is concerned. You are the live proof that this can work — see `hypothesis:l3-parent-brief-forbids-the-only-commit`.

Do NOT push. Do NOT merge. Do NOT touch `season/s2`. The director merges. Commit locally on your own branch, that is all.

Run on pi/OpenRouter. Your kid: `python3 extensions/agi/bin/dispatch.py . L3.43 --target <this node> --level small --tier kid --harness pi`. Do NOT run `workflow.py run` for any reason this round.

SANCTUARY-DIRECTOR GEN V, 2026-09-09, item 55 -- CLAIM-TO-READ PROVED LIVE, BY THE ONLY SEAT ALLOWED TO RUN. No seat was launched: under survival mode the active set is the prime and this director, so the mechanism was exercised on the director itself, which is precisely the owner's ask ("Each one can claim a section of handoff to read to conserve individual context space").

MEASURED. HANDOFF.md whole is 77,943 bytes, ~19,485 tokens. handoff.py sections prices every section; the largest, section 6, is 42,226 B / ~10,556 tok, 54 percent of the file on its own. A full claim / read / release cycle on "section 5 Known-good verification sequence" served 936 B / ~234 tok and released clean -- 83 times less than reading the file whole. The section 0 state block prices at ~969 tok, 20 times less. The mechanism works end to end: sections, claim (read and write modes), read, write, release, show, with 9 tests behind it.

THE BLOCKER IS DISCOVERABILITY, AND IT IS THE SAME BLOCKER AS ITEM 54. Nothing names handoff.py to a seat -- not brief.py, not the seat briefs. The evidence is this director's own behaviour one hour before running the test: it read the prime's section 6 with a hand-rolled `sed -n '300,371p' HANDOFF.md`, the exact bypass the tool exists to end, because no brief had ever mentioned the tool. A capability that is built, tested and unnamed is indistinguishable from one that does not exist.

THREE FRICTION POINTS, each measured, each small and each a real tax on adoption:
1. `handoff.py sections` prints section names WITH their "##" heading prefix, and `claim` REFUSES that exact string -- the name must be passed without the prefix. The tool's own output is not copy-pasteable into the tool's own next command.
2. The flag is `--holder` here while every other seat-aware entry point uses `--seat` (rotate.py meter --seat, dispatch.py --seat). Two names for one concept.
3. Omitting --holder produces "REFUSED: None does not hold a claim on section ...", printing the Python None rather than naming the missing flag.

A CORRECTION RECORDED BECAUSE IT WAS NEARLY REPORTED WRONG: the first read refusal looked like proof that claim-to-read was unusable. It was not. `read` does accept --holder; the flag had simply been omitted, and the refusal was correct fail-closed behaviour. Only the error text is at fault. The claim survives measurement; the first reading of it did not.

STATE OF THE OWNER'S ASK, honestly: the handoff-sectioning half that the owner called out as the enabler is BUILT and now PROVED at a real 83x reduction on the real file. What remains unproved is the perpetual half -- a seat that rotates itself and keeps its slice -- which cannot be shown while every seat is shut down, and is banked for the owner rather than claimed.
