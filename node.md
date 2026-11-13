---
id: doc:card-director-review
mint_id: bb2ae3f496c14e55a365ad7f774ba702
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-review
season: 3
tags: []
title: Card director review
town: local-maxxing
---
# doc:card-director-review

director-review · engine v4 post · director under sanctuary-master (SM) · town local-maxxing · box encryption-town · role doc:role-director-review (on top of doc:unified-director-brief).
Gen 1 (10-22 .. 11-12) rotates OUT at its idle close for the owner's model order (11-12 02:12Z, relayed by SM 02:14:57Z): directors -> claude-sonnet-5-5; the successor starts on Sonnet.

## §0 State
```
skills    agi-send (mail BOX ONLY, SM is my one edge) · agi-rotate · agi-review (on call) · agi-memory-guard · agi-node-write · agi-goal
placement council 3/3 10-28 and 10-31: NO leaf; on call for SM's reviews. Never invent a goal (scope creep is the failure mode)
data      /data/work/media/season3 (mine): deliver/ = what the Drive watcher uploads; deliver-tmp/ = built, NOT published; report/ = checks
code      extensions/agi/tests/media_*.py on the trunk (run from MY worktree; python3 -B, nice 10, one heavy process at a time, start test first)
mail      read `AGI_POST=director-review box read` (from the worktree: outside it the send fails 'off-matrix'); send = printf ... | AGI_POST=director-review box send sanctuary-master
prayer    first tokens of the session's first reply and the last text before idle/rotate, no tool call after it (L354 interim)
break     short breaks as needed (owner 11-05); free-day Sundays 05:00Z Sun -> 05:00Z Mon; break files stay where they are (owner's deeper review later)
```

## §1 Plan
- DONE: first act (joinprobe good ANIMATED / stale STATIC, 10-22); sync pair (published GREEN / -itsoffset 1 RED, 10-24); M5 inspector run 1 (11-05: 5 FAIL / 4 WARN) and run 2 after L359 (0 FAIL / 4 WARN).
- DONE 11-13: measure-fix tip written in the worktree (media_html.py:191 one CSS line; test_media_html.py row RED on trunk, GREEN with fix; 19 pass); [merge-up] sent to SM.
- NEXT (SM's order 02:17:11Z 11-12, HOLD): (1) cut the measure fix as ONE tip on the live trunk for SM's narrow gate: media_html.py:190, cap `.bytes p, details>summary, details>p` at 60ch, pre.ex stays wide; WITH a test row that reads the rendered measure (RED on the trunk, GREEN on the tip). (2) After it lands: rebuild the page from the trunk (NOT the deliver-tmp/ copy), check + inspector, publish to deliver/ replacing the 10-16 page, one-line [published] to SM.
- BLOCKED on the owner: the §6 items.

## §2 Landed
- 10-22 first act; 10-24 sync pair; 11-05 inspector runs 1+2 (report /data/work/media/season3/report/inspect-explainer.md, both runs + SM's allow word inside).
- 11-01 free day: 15 notes in ~/free/ (INDEX.md) + the song "Twenty-Three Nevers" in /data/scratch/art/director-review/ (owner heard it as 7/8; take 2 not needed).

## 🔴 Where it stops
Fix tip sent to SM as [merge-up] (turn end commits it). Waiting for SM's gate; deliver/ keeps the 10-16 page.
Next command at wake: `AGI_POST=director-review box read`; once the tip is on the trunk: rebuild from the trunk (`python3 -B extensions/agi/tests/media_html.py build .agi/context/media/season3-explainer-script.md $PWD /data/work/media/season3/deliver-tmp/season3-explainer.html`), `media_html.py check PAGE $PWD /data/work/media/season3/deliver` (findings=0), inspector as in §5, publish to deliver/, one-line [published] to SM.

## §4 Traps (this generation only)
- My worktree takes the trunk only at a prompt's agi-in merge; to run trunk code sooner: `git archive <sha> extensions/agi/tests .agi/context/media | tar -x -C <dir under report/>`, REPO = my worktree. Never a hand merge.
- An onset autocorrelation hears the loudest rhythmic layer, not the melody (the 7/8 song read 6/8 to it; the owner heard 7/8).
- The inspector applies any direction.json allowances silently: check report/ and .taste-skill/ hold none before a run.

## §5 Verification
- media_html check: findings=0 on the page; a mutant (one excerpt byte + one audio src) reads findings=2.
- Inspector: `cd /data/work/media/season3/report && CHROME_PATH=/usr/bin/chromium nice -n 10 node /data/work/skills-vendor/taste-skill@f624f37a8c/scripts/inspect.mjs <page> --out <dir> --allow few-pictures,still-page` (belam: read-only vendored path, no install, throwaway profile, never Playwright). LOOK at the screenshots before saying anything about quality.

## §6 BANKED (owner)
Voice pick, the word sed, the music pick (sung Lyria candidates; HOLD on new music), sung vs instrumental, the music-video visuals, four taste points (keyframes in video/banked/), the optional C6 timestamped STT (one key via belam, cap <= $0.10 + the $0.50 floor).

## §7 ATOMS
- CLOSED 11-12 02:17:11Z (SM: HOLD, its miss that it waited a week): the publish ask of ecfe7128c6. Became §1 NEXT (1)+(2), SM's order: the fix is OURS to cut now: cap `.bytes p, details>summary, details>p` at 60ch in media_html.py:190, leave pre.ex wide (the probe's 110 chars = 62rem / 9 px).
- CLOSED 10-28 placement (no leaf) · 10-31 placement (nothing to place) · 11-01 prayer P0 (by hand) · 11-01 free day + Sunday rule + art allowance · 11-05 resume · 11-05 inspector allow word · 11-12 model order (this rotation).
