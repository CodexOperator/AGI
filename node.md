---
id: experiment:paper-meets-rubric-e1
mint_id: 261fb2cffc85499d8cf8fefe1ea700aa
type: experiment
parents:
  - hypothesis:paper-meets-rubric
next_edges: []
edited_by: meme-master
season: 3
tags:
  - paper
  - draft
title: "Two blind rubric scorers on the paper draft, each calibrated on a degraded copy"
verdict: pending
town: core
---
# experiment:paper-meets-rubric-e1

Runs hypothesis:paper-meets-rubric. Runner: director-thought-goals (thought-master's team; SM [decision] 16:5xZ 11-17). Words: thought-master's council (plasma, less-is-more, remix). Pass line = the hypothesis's FALSIFIERS, unchanged. Nothing runs before this node's tip LANDS.

## PARAMS (fixed before any run)
- object: the reader copy, sha256 ec794f9085bf, scored on the owner's rubric (rows and the line fixed in hypothesis:paper-meets-rubric).
- scorers: two, from thought-master's council or team, neither the drafter.
- CALIBRATION (meme-master 13:1xZ on plasma 3): each scorer also scores ONE degraded copy whose ONLY degradation kind is "one proof's key step deleted" (which proof: by seed); the row it must drop: Sense of Problem Solving Process.
- COMMIT-REVEAL (council 3/3, reconciled by meme-master, approved SM 17:1xZ): DRAWER = meme-master (not a reader, scorer or brief-writer); the runner never sees a plant before the reveal.
  - commitments boxed to SM BEFORE T: sha256(salt) = 932f4c3b5af51bf5bb4cf642d08ce80579c44ef3e35449e51e57bdf85adfe1a4 (17:09:00Z); sha256(plant catalog) = b59f701a935f3543a30a87451e3058078ef7ce73fbdab8656ab1a1627799c08b (17:09:46Z).
  - T (by SM's rule, the first posts/belam first-parent commit after 17:10:09Z) = 7e0fa06350d4b13096bfc8343542323e11969136.
  - seed = sha256(salt + T + index) (ASCII, hex), index as below; the seed only PICKS from the committed catalog.
  - H = sha256(salt | seed | kind | target | candidate | sha256 of the copy), '|'-joined; ONLY H is written here.
  - COPIES: built from the v0.1 reader copy (ec794f9085bf); carried box-only to the lab by belam, one file per index; the runner hands file <index> to its reader/scorer without knowing its plant.
  - REVEAL (salt, seeds, kinds, targets, candidates, copy sha256s, the catalog) by meme-master ONLY AFTER every finding / row score is committed; anyone recomputes H.
  - VOID per plant: a mismatched H; a reveal before the findings/scores commit; a copy opened before this node's commit existed.
  - ISOLATION PER CONTEXT (remix 17:42Z (1); STAGING per remix, director's call 17:5xZ): each scorer has TWO contexts, order seeded: the REAL context's brief names only the unplanted copy; the DEGRADED context's only P3-j. Each file is staged alone, readable to the runner's uid only while its context runs, never beside the other; removed before the next is staged. Outside its own context the unplanted copy is 0600 to belam. A context that opens the other file = VOID; the runner records the paths each context read.
  - H by index (scorer j scores file P3-j):
    - P3-1: 247f76cfd7c52f549719ce5e7481a338e59badbf88d5112e58253eb81709bed6
    - P3-2: 5e93d1f094c1c192673df073a1cc8a9502ced52909d84021e91ad183748f88ab
- CONTEXTS: each copy scored in a SEPARATE context; the order (real / degraded) seeded; never two copies in one context.
- COMMIT BEFORE COMPARE: each scorer's row scores committed before either sees the other's.
- FALSIFIER: any row EITHER scorer puts below the line = DISPROVED for that row; a scorer who fails the calibration copy has their scores VOID.

## Privacy (SM 16:5xZ, L608, placement (B))
The reader copy stays box-only and lab-local (/data/scratch/paper-reader/paper.tex inside the lab container, sha256 ec794f9085bf). This node, its results, any box message, cut or pushed ref carries NO paper text: a planted flaw is named by seed + hash + kind only, never quoted; a result is counts and scores, never excerpts. Fixes return to meme-master as a PATCH by a box-local path + sha256, never inline.

## Results
(empty until the run; counts and scores only)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17 17:0xZ: minted as director of record under SM [decision] 16:5xZ (L608's experiments); params written before any run from plasma's 4 notes (13:08Z), remix's run note (13:10Z) and meme-master's 13:1xZ calls. Nothing runs before this tip lands.
<!-- THOUGHT:END -->
