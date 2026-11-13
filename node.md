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

meme-master · engine v4 post · claude-opus-5-5 medium · director under keep, sanctuary-master (SM) its route up · town core · box encryption-town · goal:g5.4.3 (leaves .1 presentation, .1.1 the A/B, .2 paper)
Role: doc:role-meme-master + doc:unified-director-brief + this card. Skills: agi-send, agi-node-write, agi-rotate, agi-memory-guard, agi-goal, agi-research-then-design (L503, built from this post's 11-10 run).

## §0 State (gen 2, 11-10 20:2xZ)
- PRIVATE WORK: ~/meme-photos (700). Deck sources ~/meme-photos/deck/v2/ (deck/deck.tex = THE deck; owner ledger ../owner-lines.md; research-a..g + stats-graph.md; prompts/ = the 13 subagent prompts). Build + renders ONLY under /data/scratch/meme-master (council A4: / is 87% full): toolchain/ (tectonic 0.15.0, venv with manim 0.22.1 + pymupdf, npm cache for hyperframes 0.9.30), deck-build/v2 (rsync of v2 + videos/ + posters/; deck/posters -> ../posters), deck-build/render.sh + render-hf.sh (one render at a time, refuse while load5 > 8).
- DUE DATE: the rough draft was due TUE 11-10 MORNING (not 11-11: my error, fixed in g5.4.3.1 at L497).
- DELIVERED: rough-draft-v1 (PDF, PDF with notes, sources tar) in the owner's Drive agi/class-presentation/rough-draft-v1/ (belam, rclone gdrive:, 10:2xZ, sha256 checked) + sent by SendUserFile. rough-draft-v1.1 = same + 15 rendered clips (10 manim, 5 HyperFrames): /data/scratch/meme-master/deck-build/rough-draft-v1.1 (+ .sha256), PDF sent to the owner; IN the owner's Drive at .../rough-draft-v1/v1.1-with-videos/ (belam 20:1xZ: 20 files, sha256 matched, rclone check 0 differences; v1 untouched).
- Every slide S1-S9 (+1b, 5a, 5b, 8b) carries the owner's titles/lines, marked '% OWNER c:<id>' (on screen) or 'OWNER (c:...)' (notes); 'c:pending-tap' = chunk not yet looked up. 57 AI proposals sit in notes labelled "cleaned up rough draft written by AI:" (owner: leave them for the professor).
- PDF clips: XeTeX cannot embed \movie, so each poster is a click-to-play \href to ../videos/<clip>.mp4.

## §1 Plan
- done: v1.1 Drive upload (belam 20:1xZ).
- DONE 11-13 v6 pass (owner chat ~15:2xZ): rough-draft-v1.2 = /data/scratch/meme-master/deck-build/rough-draft-v1.2 (+ .sha256, 21 files), PDF sent to the owner; Drive upload ASKED of belam via SM 15:4xZ. Sources synced to ~/meme-photos/deck/v2 (deck.pre-v6.tex = before). Changes: threshold ruler (uniform 0.94 scale, no jitter) + band inside the bar; C1b uses C1's 18-block game source; manim in Liberation Sans; C3b 5 beats (reset+handoff, compaction, rotation, fork, graph) with the game source strip; NEW mn_triangle.py (C3t, C3t2); owner note lines promoted to slides via \onscreen (S2, S4 tools, S5b, S8 engine); S8 split into 3 frames; S7 fallback stills made; sizes fixed (hook, S6, bookend, fallbacks). NOT done: the harness slide title (owner slot); 'HTML version' read as the HyperFrames clip sources (ask the owner). TM: no deck data (own card last 11-05; local-town dark since 11-09).
- next: (1) the two queued lanes (outline, fuel) still not on core/season3/main 11-13 15:2xZ (L566 newest): [merge-up] RE-SENT ONCE to SM 11-13 15:2xZ; L567 outline LANDED d419a9a4ce 15:35Z; L568 fuel cutting 15:36Z; no re-cut; (2) arm B (goal:g5.4.3.1.1, the full graph treatment) waits on thought-master accepting as running director (SM asked 09:54Z, I nudged 11:5xZ; no answer); then rough-draft-v2 to Drive .../rough-draft-v2/ and S9 compares basic vs graph; (3) the owner's remaining small items below; (4) then the paper (goal:g5.4.3.2), one chunk at a time.
- owner-side small items: S5a title (optional slide); the C3t/C3t2 triangle clips have NO source (placeholders); the C5 poster renders the made-up acronym, not the verified mantras (storyboard-v3 'C5 poster content, REAL examples' + Google former motto); the reveal clip is the v4 chain, not the v6 beats (storyboard-v4 'C6 v6').
- blocked: nothing of mine.

## §2 Landed
- [fuel] schema L485 (11-09). goal:g5.4.3.1 + .2 L492. goal:g5.4.3.1.1 + due-date fix L497. doc:draft-presentation-deck-v1 (council full-pass copy, v3 004e3089e3) L499. skill agi-research-then-design (DG1) L503.
- QUEUED at SM, plain one-file lanes off posts/belam 164d577536: mm-outline-v1 e2bae92830 (doc:draft-presentation-outline v1.2), mm-fuel-v1 0881087b6b (fuel:s4-retire-the-python-engine). Neither was ever on the trunk before (turn-end commits are not lands).

## 🔴 Where it stops
Gen 2 at an idle spot: v1.1 is in Drive; waiting on TM (arm B) and SM (the two lanes). Next: `cd ~/t && AGI_POST=meme-master box read`, then hand the owner the next open §1 item, one chunk at a time.

## §4 Traps (this generation's)
- A post's turn-end commit is NOT a land: cut a plain one-file lane off posts/belam (temp index: read-tree, update-index --cacheinfo, write-tree; `git commit-tree -S`, check %G? = G) and send SM a [merge-up]. Outline + fuel sat unlanded a day.
- Due dates: compute the weekday (`date -d YYYY-MM-DD +%A`).
- Elision by regex over "quoted" spans pairs quotes one off and eats agent text: elide owner words by matching the ledger, never by quote shape (sp A, 11-10).
- A "% OWNER" guard sees only that marker: guard BOTH markers (64 lines in the deck); label an agent paraphrase of an owner aside as such, never "OWNER's aside".
- The council's copy head fields go BEFORE the first '## ' heading, in the leaf's control form ("'% OWNER' lines: 44"); the records (names, F3 + sha, notes read) go in the COMMIT message.
- Renders: one at a time, refuse while load5 > 8; never in ~ (council A4).
- INTERIM RULE: a `## OWNER` block cites only belam's store; my owner words go under plain headings with c: ids until goal:g7.16.1.11.46.34 lands.
- Chunk lookup: `git -C ~/.mem/meme-master.git grep -l -F '<phrase>' refs/heads/mem -- mem`, then speaker: owner.

## §5 Verification
- Deck: `bash deck/check-owner.sh` from the deck dir (F1 slots, F2 floor; drops \note spans: the owner allows the verbal-only item in notes, c:4b5d4abae03e); never upload the item in a committed copy.

## §6 BANKED
- doc:draft-presentation-deck-v1 next in-place edit: 'deck.tex line' beside 127/128/410/411 (aio); head line "'OWNER (c:' note lines: 20" (sp); arm B's guard reads BOTH markers.
- fuel:s4-retire-the-python-engine next touch (alive NIT, SM relay 15:18Z 11-13): name the trunk its 'Measured' totals were taken on (base e289cd776b gives 120,584 total, rotate.py 23,590; stated 121,168 / 23.8k).
- [fuel].md next touch: name goal:g7.16.1.11.46.34 by id once on the trunk (alive NIT 3); my plain owner headings return to OWNER blocks when .46.34 lands.
- Owner answered (via belam 19:2xZ): the design stage may use Fable (exception to the Sonnet-only SUBAGENTS rule); the owner wants less ritual process, more real talk between posts.

## §7 ATOMS
| atom | from | state |
|---|---|---|
| photos -> outline -> presentation | owner c:787879d6bc35 | v1 + v1.1 delivered; OPEN: small items in §1 |
| roll through chunks, owner rewords every line | owner c:c083f191f98d | done for S1-S9 titles/lines; S5a title open |
| Sonnet research then Fable; manim + HyperFrames; LaTeX PDF + videos | owner 11-10 | done; 15 clips rendered |
| council full pass + full graph treatment, A/B, S9 compare | owner c:61b389266d66 | council 3/3; leaf L497; copy L499; OPEN: TM as running director |
| upload v1/v2 to Drive agi/class-presentation | owner c:1ae05e71c801 | v1 + v1.1 done (belam 20:1xZ); v2 after arm B |
| formalize research-then-design as a graph skill | owner c:e780e4c65887 | closed: L503 |
| subgoals via SM to director-goals-1 (words + requirements, not goal text) | owner c:4b5d4abae03e | standing: move to role doc |
| tell TM the owner's success definition | owner 11-10 | closed: boxed TM |
| ORACLE angle (one Fable pass per council seat) | SM 20:26Z 11-10 | closed: boxed SM 20:3xZ |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, meme-master gen 1: first start, then photos -> outline v1; the [fuel] schema landed (L485).
11-10, gen 1 out: the whole rough draft written line by line with the owner, researched by 8 Sonnet kids and designed by 4 Fable passes, built with tectonic and rendered with manim + HyperFrames under the load guard; v1 in the owner's Drive, v1.1 with videos sent; the goal shape, the council copy and the research-then-design skill landed. Card rewritten whole for the successor at the meter line.
<!-- THOUGHT:END -->
