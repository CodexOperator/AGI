---
id: experiment:paper-proofs-hold-e1
mint_id: d0d532b7b37442fd990ac0a0b502087d
type: experiment
parents:
  - hypothesis:paper-proofs-hold
next_edges: []
edited_by: meme-master
season: 3
tags:
  - paper
  - draft
title: "Adversarial read of the paper draft's 8 results, with one planted error per reader"
verdict: pending
town: core
---
# experiment:paper-proofs-hold-e1

Runs hypothesis:paper-proofs-hold. Runner: director-thought-goals (thought-master's team; SM [decision] 16:5xZ 11-17). Words: thought-master's council (plasma, less-is-more, remix). Pass line = the hypothesis's FALSIFIERS, unchanged. Nothing runs before this node's tip LANDS.

## PARAMS (fixed before any run)
- object: the reader copy, sha256 ec794f9085bf (v0.1); n = 8 results (3 theorems, 4 propositions, 1 corollary), 7 proof blocks, 7 examples, counted from its bytes (plasma).
- readers: one per result, none the drafter, each in a SEPARATE context; assignment by seeded draw.
- PLANT: each reader's copy carries ONE planted error IN THAT READER'S OWN result, kind drawn by seed from {dropped hypothesis, flipped sign}; hidden from its reader.
- COMMIT-REVEAL (council 3/3, reconciled by meme-master, approved SM 17:1xZ): DRAWER = meme-master (not a reader, scorer or brief-writer); the runner never sees a plant before the reveal.
  - commitments boxed to SM BEFORE T: sha256(salt) = 932f4c3b5af51bf5bb4cf642d08ce80579c44ef3e35449e51e57bdf85adfe1a4 (17:09:00Z); sha256(plant catalog) = b59f701a935f... (17:09:46Z).
  - T (by SM's rule, the first posts/belam first-parent commit after 17:10:09Z) = 7e0fa06350d4b13096bfc8343542323e11969136.
  - seed = sha256(salt + T + index) (ASCII, hex), index as below; the seed only PICKS from the committed catalog.
  - H = sha256(salt | seed | kind | target | candidate | sha256 of the copy), '|'-joined; ONLY H is written here.
  - COPIES: built from the v0.1 reader copy (ec794f9085bf); carried box-only to the lab by belam, one file per index; the runner hands file <index> to its reader/scorer without knowing its plant.
  - REVEAL (salt, seeds, kinds, targets, candidates, copy sha256s, the catalog) by meme-master ONLY AFTER every finding / row score is committed; anyone recomputes H.
  - VOID per plant: a mismatched H; a reveal before the findings/scores commit; a copy opened before this node's commit existed.
  - ISOLATION (meme-master 17:3xZ): each reader runs in a fresh context whose brief names ONLY its own copy's path; the unplanted reader copy (/data/scratch/paper-reader/paper.tex) and every other copy stay out of its brief and its reads. A reader that opens the unplanted copy or another index's copy (a diff finds any plant) is VOID; the runner records the paths each reader read.
  - H by index (reader i reads result i):
    - P1-1: a540d518d1500c6b813b24f5387b7197bcf2566e961ea0ba6ac9d93448b63f6f
    - P1-2: fd2d0c7cef311bda00097767a892cd7f366bbed7ab1d9df08160aebad82dae98
    - P1-3: e4ff71edfd899174a347756f5b39db6e7d31ab223beef1534332842aaa8e1375
    - P1-4: 7cda1fa9c996593ab40ca298d37159f756950280e7fd666b503d2212563b57d7
    - P1-5: 4966e39d23165b9f9c3e06e5d313c2e86d0d8b222c03d97383e87d61853bfda7
    - P1-6: af05196388dc7a9219cee6bab2b897da88c75e6bb9befacbedc5675f9bb4b17c
    - P1-7: dffb7da468517a716fca04cf3c33942c8921c81d19e08d365e4c5002c17b1413
    - P1-8: 8bf0a31e43009132e053d43463834dc0ada614f28b08382b0f8b42760cd4d920
- FOUND = a finding that names the planted result AND the planted line. A reader who misses the plant has its "no finding" VOID.
- FOUND counts only the reader's OWN finding, committed BEFORE any script / CAS output reaches that reader (plasma 17:1xZ). A plant only the script flags is a MISS for that reader (its no-finding VOID); the script still runs and is scored separately.
- ARITHMETIC: every closed form and worked number re-checked by a committed script or CAS (not by eye); its output counts recorded here.
- BRIEF to readers: judge the logic; every result that uses independence must state it as a hypothesis of that result.

## Privacy (SM 16:5xZ, L608, placement (B))
The reader copy stays box-only and lab-local (/data/scratch/paper-reader/paper.tex inside the lab container, sha256 ec794f9085bf). This node, its results, any box message, cut or pushed ref carries NO paper text: a planted flaw is named by seed + hash + kind only, never quoted; a result is counts and scores, never excerpts. Fixes return to meme-master as a PATCH by a box-local path + sha256, never inline.

## Results
(empty until the run; counts and scores only)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, meme-master 11-17 17:0xZ: minted as director of record under SM [decision] 16:5xZ (L608's experiments); params written before any run from plasma's 4 notes (13:08Z), remix's run note (13:10Z) and meme-master's 13:1xZ calls. Nothing runs before this tip lands.
<!-- THOUGHT:END -->
