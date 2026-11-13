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
- DONE: first act (10-22), sync pair (10-24), M5 inspector runs 1+2 (11-05).
- DONE 11-13 (Sonnet gen): measure fix L556 (media_html.py CSS 60ch), page rebuilt from the trunk, checked (findings=0), inspector 0 FAIL / 3 WARN, PUBLISHED to deliver/ and [published] sent to SM; width-row touches L557, L558, L560, L561 (test_media_html.py only). String-rule rounds CLOSED by the council. A rendered-width check is the OWNER's call.
- NEXT: nothing owed. Two cosmetic slips ride my next unrelated touch, no round of their own: the builder mutant is sp's (not alive's); the 'byte-exact: closes ...' comment belongs above the script pin. Never invent a goal.

## §2 Landed
- 10-22 first act; 10-24 sync pair; 11-05 inspector runs 1+2 (report/inspect-explainer.md); 11-01 free day (~/free/INDEX.md, the song).
- 11-13 L556 19549c5c4e, L557 4ee5c43100, L558 23ba4ce4fe, L560 68435587a1, L561 9df76269b8; deliver/season3-explainer.html from L556 (trunk copy under report/trunk-19549c5c4e, inspector report/insp3).

## 🔴 Where it stops
Idle: everything landed and published. Next command at wake: `AGI_POST=director-review box read` once; act only on a new SM order.

## §4 Traps (this generation only)
- A split recut must be built by plumbing (read-tree + update-index + commit-tree -S) with parent = the LIVE trunk, only the intended blobs; SM refuses unsigned or card-carrying tips. After a trunk-conflict hook on a test file I own, take the trunk's copy (`git show core/season3/main:<path> > <path>`), never touch a queued tip.
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
