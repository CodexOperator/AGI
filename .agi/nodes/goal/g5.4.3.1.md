---
id: goal:g5.4.3.1
mint_id: 4843ab8dd9b74fe497efc5552307e12a
type: goal
parents:
  - goal:g5.4.3
next_edges: []
confidence: 0.5
goal_id: G5.4.3.1
goal_kind: subgoal
origin: goal
role: director
season: 3
status: active
seeds: []
tags: []
title: "G5.4.3.1: The class presentation, rough draft Tue 11-10 morning: a LaTeX deck (PDF) with short animations, every on-screen line the owner's"
town: core
---

# goal:g5.4.3.1

## Why this exists
goal:g5.4.3 holds the owner's first ask (the post, the presentation, then the paper) but none of the presentation's own requirements; those came in the owner's chunk answers 11-09 and 11-10 and sat only on the post's card and in its private drafts. A card never tracks goals, so they are placed here, in their own leaf: the presentation is one target end-state, the paper (goal:g5.4.3.2) another. The owner also asked that the talk's closing reveal show this very chain, so the leaf is the record the reveal points at.

## The owner's words 2026-11-09 08:18:05Z (c:787879d6bc35), verbatim [meme-master store; not an OWNER heading under the interim rule (self-perpetuating 19:55:55Z 11-09) until goal:g7.16.1.11.46.34 lands]
> 1. Yes our class and professors. This is rough draft so no one really other than professor but overall the directors of departments may also be there. [...]
> 2. Super short 5-10 mins tops. Try to do under 7. Rough draft due Tuesday evening I believe but morning would be best. Tuesday morning.

## The owner's words 2026-11-10 03:56:00Z (c:c083f191f98d), verbatim, the parts that set requirements [meme-master store; same interim rule]
> Let's just roll through all of them until all of the text is properly re-worded from me, in a way that makes sense. I know the data may be lagging [...] we can at least work out what sort of visuals and graphs we need.
> I want to be able to basically have short snippet animations in the presentation I can play as either videos or embedded (the final presentation should be a latex file exported to pdf and both need to be there for submission. We can also add the videos as linked sources or whatever as needed)
> I want it to be step-by-step friendly almost like a pitch deck as the style and pacing should almost feel like a youtube video. In practice this presentation is practice for a future youtube/twitter video i'll be releasing [...] And somehow I want to include that the presentation itself was a graph chain in and of itself
(The same message asks for Sonnet research kids first, then a Fable pass, manim and HyperFrames, and the "why the long way" reasons with references; whole in the store. One detail in it is elided here [elided, c:2763ec818294].)

## The owner's words 2026-11-10 04:10:51Z (c:2763ec818294), verbatim [meme-master store; same interim rule]
> Could we maybe avoid the monetary justification and mentioning the [elided, c:2763ec818294] in text directly as that's something I want to have as a verbal only note that I can reveal or withhold depending on what my professor advises on actual presentation day. Also the reveal could have some animations, and overall spread out the motion graphic media across more of the presentation [...]
> 3. Every chunk of text needs to be mine including the hook. That is the key thing I want your help with [...] stay as much mostly on task as possible. One line at a time this presentation will get filled in. One slide at a time.
(Elided by the post on that same word; one sentence of c:787879d6bc35 elided the same way, SM A2 as widened by alive 04:39:59Z.)

## The owner's words 2026-11-10 04:19:32Z (c:972f86002970) and 04:25:34Z (c:1a218a218cd7), verbatim [meme-master store; same interim rule]
> I wanna keep it all as is and just push past the 7 minute mark slightly if I have to. I'd rather do that and give a fuller picture.
> spread things out as needed the speaker bits could be lines on subsequent slides or reused if needed

## The owner's words 2026-11-10 (c:31a2e2b871f1), verbatim [meme-master store; same interim rule]
> can we be sure all the chunks and requirements I have included for the presentation are included in the goal shape properly to demonstrate in the reveal why the goal shape matters, as that will be included in the slides as one of the key things I explored

## Target end-state
1. A LaTeX beamer deck and its PDF, 9 slides in the owner-approved order (hook · problem · why organize (long) · why the long way · solution · what humans give · walkthrough · what it produced · the reveal), about 7:00-7:30 spoken.
2. Short animation clips (manim and HyperFrames) on nearly every slide; each one shipped as a video file, a poster frame in the PDF, an embedded play where the viewer supports it, and a link.
3. Every on-screen line and every speaker line is the owner's own wording, written one line at a time with the post shepherding; the post drafts structure, visuals, animation code, chart specs and cited evidence only.
4. The closing reveal shows this chain with real ids: goal:g5.4 -> goal:g5.4.3 -> this leaf -> doc:role-meme-master -> the drafts -> the owner's chunks; it is animated.
5. Rough draft submitted Tue 11-10 morning (the owner: 'evening I believe but morning would be best', c:787879d6bc35).

## Invariants
- Nothing the owner keeps verbal-only (c:2763ec818294) is on screen, in charts, in the references or in the deck source, except its speaker notes (\note{...}), which the owner allows (c:4b5d4abae03e); % comments and every other line stay clean.
- Evidence on slides only from cited, checked sources; a prediction is labelled a prediction; no invented number. Data the town has not gathered is a visible placeholder.
- The live-engine fact is "~1.2k lines of shell stored in graph nodes run the town; ~100k lines of older Python are being retired", never "104k lines of engine Python" (town:core '## Fuel', meme-master block).
- goal:g5.4.3's invariants hold (finals the owner's; photos never committed; boxes SM and TM, never belam).

## Falsifier
F1 and F2 are ONE script in the deck tooling, `deck/check-owner.sh` (it travels with the deck sources in the submission package; its word list lives there, not in this leaf: alive's A2), run from the dir holding deck.tex. It reads deck.tex, every file deck.tex \input/\includes, every .bib, and the built deck.pdf (pdftotext); any of them missing or unreadable prints `READ NOTHING <file>`, rc 1, RED, never a pass. It drops each \note{...} SPAN (balanced braces) before F2 reads, never the line (owner c:4b5d4abae03e; sp's A4 mechanism); % comments are read. rc 0 = pass. sha256 of v2 (11-10, note spans dropped): b5cf85c3ecbecf47....
1. OWNER LINES: it prints `F1 slots: 0`. CONTROL: on the 11-10 draft the same script prints `F1 slots: 11`, so a 0 at the close is a read that could have failed. THE LEDGER: each owner line in the deck source carries its chunk id in a comment on the same line, `% OWNER c:<12 hex>`; at the close each on-screen line is matched by hand to that id in meme-master's store (speaker: owner). RED if any line has no owner chunk.
2. NOTHING VERBAL-ONLY WRITTEN: it prints `F2 source: none` and `F2 pdf: none`. Its pattern is a FLOOR (a currency sign before a digit and a short word list); a hand read of the PDF beside it catches the rest. CONTROL: an \input file holding a line it matches reads RED; an \input file missing reads READ NOTHING.
3. SUBMISSION: the package holds deck.pdf, one video per clip named in the storyboard, and a links list; read by hand.
4. THE OWNER'S WORD: an owner chunk saying the rough draft is submitted. Read by hand.

## Out of scope
The paper (goal:g5.4.3.2) · the YouTube/Twitter video itself (the owner's, later) · benchmarks themselves (thought-master's; this leaf only shows them).

## Agent Notes
Assigned to **meme-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-goals-1 11-10 (meme-master's [correction] 10:0xZ, SM 10:07:11Z): the DATE only. The owner said Tuesday (c:787879d6bc35, quoted in this node's block of that id); Tuesday is 2026-11-10 (date(1)), and every text after meme-master's first outline copied '11-11'. Title and Target 5 now read Tue 11-10; the owner's words are unchanged. Nothing else changed.
v1, meme-master 11-10, DRAFT for the council's placement (meme-master's grow cell is [idea, doc, task]: a goal is not its to mint). Placed because the owner asked that every requirement live in the goal shape, for the reveal; they had lived only on the card's ATOMS and in private drafts.
<!-- THOUGHT:END -->
