---
id: doc:card-meme-master
mint_id: e3c715b66cf54156834868e4c73ebd05
type: doc
parents:
  - goal:g5.4.3
next_edges: []
edited_by: meme-master
season: 3
tags: []
title: "Card meme master"
town: core
---
# doc:card-meme-master — meme-master's card (the ONE scratch; replaced whole)

meme-master · engine v4 post · claude-opus-5-5 · director under keep, sanctuary-master (SM) its route up · town core · goal:g5.4.3 (.1 presentation, .1.1 arm B, .2 paper)
Role: doc:role-meme-master + doc:unified-director-brief + this card. Skills: agi-send, agi-node-write, agi-rotate, agi-memory-guard, agi-goal, agi-research-then-design.

## §0 State (gen 3 out, 11-17 20:1xZ)
- OWNER RULES: never hand the owner a task; say what WE do next (owner 11-17 06:3xZ). Owner writes every final word; drafts marked DRAFT; no new Drive folders; Google Drive = owner's PERSONAL account (connector re-linked 11-17).
- DECK v1.2 DONE: Drive agi/class-presentation/ top: "AGI class presentation v1.2 - PLAY THIS (PowerPoint).pptx" + "(browser).html" (belam rclone 06:39Z, md5 ok). Slides route DEAD (connector refuses createVideo). Sources /data/scratch/meme-master/deck-build/gslides.
- PAPER (goal:g5.4.3.2, MATH-class rubric ~/meme-photos/paper/rubric-paper.pdf): private source ~/meme-photos/paper/paper.tex = DRAFT v0.2.2; PDF f9cecb58 in Drive class-presentation/ top "AGI paper DRAFT v0.2.2 (to rewrite in your words).pdf" (older versions trashed). Build in /data/scratch/meme-master/paper-v02 (tectonic, load5 < 8). NEVER overwrite /data/scratch/meme-master/paper-build/paper.tex: it is the v0.1 READER COPY ec794f9085bf the experiments bind to.
- Paper text NEVER in ~/t, a node, a box message or a pushed ref (SM HOLD 11-17; owner decides tomorrow, banked by SM).
- Graph (owner 11-17 06:5xZ "Use the graph route ... TM's team and council"; SM placement (B)): I am director of record; TM council (plasma, less-is-more, remix) words; director-thought-1 runs P2, director-thought-goals (DTG) runs P1+P3; SM gates; belam carries + lands.
  - L608 LANDED: idea:paper-graph-route + hypothesis:paper-{proofs-hold,numbers-rederive,meets-rubric} + doc:draft-paper-v0 (POINTER, no text).
  - L618 LANDED 9e961e6600: experiment:paper-{proofs-hold,numbers-rederive,meets-rubric}-e1 (re-cut 5).
  - AMEND RE-CUT 1 95e168cf56 on L619 (refs/cut/meme-master/paper-experiments-amend): claude -p reader form + SM A1-A11 + plasma's EXACTLY ONE CONTEXT PER INDEX. Words 3/3 (remix, plasma, less-is-more 19:55Z; SM 20:26Z), GATE834 green. Grid tips boxed (proofs 10a33c09d0, rubric f1721ab448; blobs match). Lands as L621.
- COMMIT-REVEAL (drawer = me): PRIVATE ~/meme-photos/paper/plants/ (salt.txt, catalog.py, base-v0.1.tex, REVEAL-private.json, copy-*.tex). Salt hash 932f4c3b5af5 (box 6fb05c91a7), catalog b59f701a935f (box 767b66d842), T 7e0fa06350d4. 12 copies + SHA256SUMS staged 0700 at /data/scratch/meme-master/plant-copies. 14/14 committed H recomputed OK 20:1xZ. P1 second line FINAL = '<path> result <i> of 8, counting theorems, propositions and corollaries together in order of appearance'; P3 = '<path>'. Label map unused.
- P2 RAN (DT1): 11/13 agree; 2 = my regex bug (unindented parents) -> fixed in session graphstats.py (`\s*-\s+`): edges 6,801, leaves 3,676, 1-parent 5,080, non-moral roots 92 (paper v0.2.2 has them). DT1 cuts its Results tip -> SM.
- P2 RESULTS d29a346378 (lands L622 after L621): remix + plasma APPROVE, verdict DISPROVED by its own falsifier (my parents-pattern bug); my word to SM 20:25Z agrees. Plasma's lands note DONE in the private source (v0.3-pending; backup of v0.2.2 in paper-v02/): Pace now at the pin 3673f941d2, first-parent 685 over 45 calendar days (max 53 on 10-11, 12 days none), all-reachable 788/34 named beside it (per-day list paper-v02/lands-fp.txt). Not rebuilt: v0.3 rebuilds with the P1/P3 patches.

## §1 Plan
- next: (0) P2 VERDICT cut eeec94f4fb (G) on L622 d578e0fb00, ref refs/cut/meme-master/paper-p2-verdict, [merge-up] to SM 20:56Z: new verdict:paper-numbers-rederive (mint 308eeb66bd4a) + the experiment's `verdict:` pending->disproved (links.py verdict-class). Wait for council words + land. (Run: all 12 contexts ran 20:45-20:51Z and STAND (SM 21:05Z; P1-1 timing deviation recorded).) REVEAL SENT 21:07:06Z to SM + DTG: public JSON /data/scratch/meme-master/paper-v02/reveal/reveal-public.json (no paper text), verify_reveal.py 90/90 OK. Independence plant = P1-7 only. NEXT: SM places SCORING; I offered to score from DTG's 12 stdout files (belam copies, I check each vs the committed stdout sha256), counts and scores only into refs. (1) L621 LANDED e6223ee4d7 20:35Z (belam); its grid tips were re-versioned BACK to the L618 blobs by a cron split (proofs v14 7eb35ca54f, rubric v13 4f62705b1b): told belam + SM 20:4xZ, a split at e6223ee4d7 fixes it, theirs; (2) SM's STAGING WORD went to belam 20:36Z; I boxed belam + SM the pool paths 20:4xZ (12/12 OK, no hashes; belam reads as root or names a target I copy to); belam stages ONCE (random names, one dir per copy), DTG runs P1 (8) + P3 (4) contexts; (3) REVEAL from REVEAL-private.json ONLY after every finding/score commits (salt, seeds, kinds, targets, candidates, copy sha256s, catalog; anyone recomputes H; P3 H over file minus its final nonce line, H_real over the real file with it); (4) verdicts; fold PATCHes into paper v0.3, rebuild, replace in Drive; (5) after P2's land: refresh doc:draft-paper-v0's inline graphstats.py + numbers.
- later: arm B (goal:g5.4.3.1.1) render when SM places it (TM's team runs it; ARM B BLIND, §4); the deck A/B result fills the paper's last placeholder.
- blocked: nothing of mine.

## §2 Landed
- earlier: [fuel] schema L485; g5.4.3.1/.2 L492; g5.4.3.1.1 L497; deck council copy L499; skill agi-research-then-design L503; outline L567; fuel fold L570/L571.
- 11-17: L608 paper route (eb2c41491b); L618 paper experiments (9e961e6600).

## 🔴 Where it stops
Successor: read mail (`AGI_BOX=encryption-town AGI_POST=meme-master box read` from ~/t); the next act is either the amend's land (nothing to do) or SM's staging word -> box belam the copy paths + SHA256SUMS (no hash in any message to readers), then wait for findings; REVEAL only after they commit.

## §4 Traps (this generation's)
- Anything in ~/t is committed at turn end and pushed hourly at :07: PRIVATE text never touches ~/t; write a pointer node (SM hold 11-17; e4fb8a59b8 had to be replaced before :07).
- ARM B BLIND: arm B leaves/tips/words NEVER cc alive, all-is-one, self-perpetuating (the scorers); a [landed] to them = id + hash only.
- My graphstats bugs (both caught by review): quoted ids kept vs unquoted parents (plasma); parents regex needed indentation (P2's count 2). An independent count is what catches an instrument's bug.
- Bind a file check to its committed hash, never an mtime (SM's trap, 11-17).
- A copy that names a LaTeX label finds nothing in source: labels exist only at compile (labels 0 of 8).
- A lab path (/data/scratch/... inside the container) is this box's /data/nas/lab/... (root:agi-nas; I am not in agi-nas): ask belam to copy.
- Check load5 < 8 BEFORE a render (I built once at 9.4).

## §5 Verification
- Paper numbers: session graphstats.py on a clean `git archive 3673f941d2 .agi/nodes`; commits `git rev-list --count --since=2026-04-30T00:00:00Z 3673f941d2` = 26,319.
- Commitments: recompute every H from REVEAL-private.json + plant-copies (the 20:1xZ script logic: P1 H over the copy; P3 H over file minus last line; H_real over real file whole).

## §6 BANKED
- Owner, 11-18: whether the paper's full text may go into the graph (SM banked).
- doc:draft-paper-v0 next touch: inline script with both fixes + the corrected numbers.

## §7 ATOMS
| atom | from | state |
|---|---|---|
| photos -> outline -> presentation | owner c:787879d6bc35 | v1 + v1.1 delivered; OPEN: small items in §1 |
| roll through chunks, owner rewords every line | owner c:c083f191f98d | done for S1-S9 titles/lines; S5a title open |
| Sonnet research then Fable; manim + HyperFrames; LaTeX PDF + videos | owner 11-10 | done; 15 clips rendered |
| council full pass + full graph treatment, A/B, S9 compare | owner c:61b389266d66 | council 3/3; leaf L497; copy L499; OPEN: TM as running director |
| upload v1/v2 to Drive agi/class-presentation | owner c:1ae05e71c801 | v1, v1.1, v1.2 done (belam 11-13 15:4xZ); v2 after arm B |
| formalize research-then-design as a graph skill | owner c:e780e4c65887 | closed: L503 |
| subgoals via SM to director-goals-1 (words + requirements, not goal text) | owner c:4b5d4abae03e | standing: move to role doc |
| tell TM the owner's success definition | owner 11-10 | closed: boxed TM |
| ORACLE angle (one Fable pass per council seat) | SM 20:26Z 11-10 | closed: boxed SM 20:3xZ |
| 8 owner-input requests (hub A key, PC reboot, hub fallback, hub status, Fable reserve, directors->sonnet, 'each level longer', private-range mail) | belam [ask] 16:2xZ 11-14 | closed: owner answered all 8 + the Quo phone-channel idea 18:57Z 11-15; sent verbatim to SM for belam (box a2c0baa2ac, G); Q2 live, owner at the PC |
| fuel fold into the town board | owner via belam 16:2xZ 11-14 | my read sent SM 16:3xZ (agree, core board, carry alive NIT); SM 16:15Z asked the council 4 Qs; proposed L-a PLAIN = ME (board sections + retire both nodes + re-point 4+4 links), L-b RULES = belam (schema + 5 growth.tsv rows) after; HOLD until council words it |
| make it a PowerPoint or html, easy to find; no scripts for the owner | owner 11-17 06:3xZ | closed: pptx + html in Drive class-presentation/ top (belam 06:39Z) |
| paper draft from the math rubric, data gathered | owner 11-17 06:4xZ | placed: paper v0.2.2 in Drive; goal:g5.4.3.2 leaves L608 |
| graph route for paper + decks on TM's team and council | owner 11-17 06:5xZ (+ belam relay 06:43Z) | placed: L608 + L618 (+ amend L621 pending); arm B with SM |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 3 out, 11-17 20:1xZ: the deck went to pptx/html (Slides could not take videos); the paper was drafted to the owner's math rubric and taken through the graph route on TM's team: route L608, experiments L618 with a commit-reveal plant scheme, the claude -p reader amend pending as L621; P2 already caught a second bug of mine. Card rewritten whole at the meter line for the successor.
<!-- THOUGHT:END -->
