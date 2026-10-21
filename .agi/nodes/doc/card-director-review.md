---
id: doc:card-director-review
mint_id: bb2ae3f496c14e55a365ad7f774ba702
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
season: 3
tags: []
title: Card director review
town: local-maxxing
---
# doc:card-director-review

director-review · engine v4 post · Sonnet 5.5 high · director under sanctuary-master (SM) · town local-maxxing · box encryption-town · goal:g7.16.1.11.45 S1 (owner 10-21: "we need to stand up a separate post for the presentation creation. Call it director-review working under sanctuary master.")

SKELETON. Not yet started: the row is boot false, and its first start waits for (a) TM + DT-1 down, (b) the owner's one login (start S6, owner-do), (c) belam's chown of the g5.4.2 media dirs to agi-director-review. DG3 writes §1 at the hand-over; this post replaces the card whole from its first turn.

## §0 State
```
skills  agi-post (stand up / take down) · agi-send (mail is BOX ONLY) · agi-goal · agi-node-write
role    the EXECUTION of goal:g5.4.2 (the presentation chapters): the work DG3 ran. The g5.4.2 WRITER stays sp (council 10-21): this post executes, it does not write the chapters' prose
mail    SM only. Read `AGI_POST=director-review box read` (once, whole); send `printf '%s\n' '[tag] ...' | AGI_POST=director-review box send sanctuary-master`. SM relays to the council, belam and the other posts. The box matrix is derived from the parent tree (levels differ by <= 1), so it does not stop a mail to a peer at your level: the rule is yours to keep (config:rotations alerts.edges names the one edge)
keepalive  a prompt "keepalive: reply with the one word ok ..." -> reply `ok`, nothing else
```

## §1 Plan (written by director-general-3 at the hand-over, council 14:44Z 10-21)

### paths (under /data/work/director-general-3-media/season3, owner agi-director-review after belam's chown)
- deliver/ = what the Drive watcher uploads: 18 season3-CN-narration.mp3, 18 explainer-chNN-<slug>.mp4 (h264 1280x720 25 fps yuv420p + aac 44100 mono), season3-explainer.html, README-narration.txt (rows + 3 header lines), README-music.txt, music-sample-a/b/c. deliver-static/ = the 18 static cards (undo = one rename back). deliver-tmp/ = rendered, not yet published (sibling of deliver/, same filesystem, NEVER inside deliver/).
- video/ = venv (manim 0.22.0, pip-freeze.txt), chNN-plan.json / -drawn.json / checks/chNN.report.json / checks/chNN.json, keyframes-chNN-k.png, banked/ (taste keyframes), next.sh / wait.sh / sheet.sh (render one chapter, wait for it, stack its 3 keyframes), media-chNN (manim cache, deletable).
- walk/ (voice walk, per-chapter chunks + transcripts), music/ (run.log + request log), m2/script.md = the M2 script copy; the SCRIPT of record is ~/w-sg/.agi/context/media/season3-explainer-script.md at sha 6432bf88d5.
- Code: the worktree ~/w-sg (branch dg3-media-r2, local, NOT pushed; check `git config --global --get-all credential.https://github.com/helper` before any push): extensions/agi/tests/media_video.py (beats, timing, checks, start test, watcher, publish/undo/queue, runner), media_vocab.py (the ONLY file that draws text), media_scene.py (one Chapter scene for all 18), media_mutate.py (hand-break sweep), media_html.py (M5), media_music.py (M6), media_walk.py / media_fidelity.py / media_recheck.py (voice), test_media_*.py. Queue files: /data/work/director-general-3-media/RENDERING (touch before a render's start test, remove after) and HOLD-GATES (touch after a chapter waited 1 h on the start test, tell SM, remove when done).

### commands (cwd ~/w-sg, python3 -B, nice 10, ONE heavy process at a time)
- start test: media_video.py start [PEAK_MIB] (anon+shmem<3500, MemAvailable>=3 GB, mem PSI full<2, io PSI some<50, no gate pytest, headroom; fail closed).
- one chapter: video/next.sh N (renders under flock + nice + /usr/bin/time -v + ulimit -v 2500000; a death at the ulimit = stop and ask), video/wait.sh N, video/sheet.sh N, LOOK at the 3 keyframes, then media_video.py publish N. Batch publishes (one partial join per batch, belam: the watcher takes a replaced file one pass after its size changed); NEVER backdate an mtime (council 3/3 NO).
- checks without a render: recheck N (file checks again), sync N (audio/video start + own-audio pauses vs stored ends), joinprobe JOINED.mp4 N (is chapter N inside the joined full file the animated one; exit 1 unless animated; NO CARD / NO FRAME are RED), offsets N (named timing exception), plan N, timing, lint FILE.., queue.
- hand-break: python3 -B extensions/agi/tests/media_mutate.py (58 rows, 1-2 h at load; prints at the end; DO NOT edit media_video.py while it runs: it mutates in place). Music: media_music.py clip FILE.. / clip-track FILE.. (clipped samples; a real track must have 0). Voice walk: media_walk.py TTSKEYFILE STTKEYFILE (keys only via SM from belam; never mint).
- tests: python3 -B -m pytest extensions/agi/tests/test_media_{video,mutate,html,recheck,walk,music}.py -q -p no:cacheprovider --basetemp=/data/work/director-general-3-media/season3/pt/NN (~145 tests, 4-6 min).

### open
1. The joined-file after-checks (belam, on the watcher's local join): duration 3226.3 s +-0.5 and joinprobe N=0..17 after the 18-chapter join; the join before it is partial by design for one pass.
2. YOUR FIRST ACT (council): one DG3 after-check on a published chapter GREEN and the same on a deliberately broken copy RED, before you own anything: e.g. joinprobe on a concat of deliver/ (all ANIMATED) vs a concat with deliver-static/ch02 (C2 STATIC, exit 1); sync N on the published file vs a copy remuxed with -itsoffset 1 (RED).
3. M5 inspector: node ~/.claude/skills/design-taste-frontend/scripts/inspect.mjs deliver/season3-explainer.html under the start test, screenshots viewed, FAILs reported as measured (its picture/motion floors are marketing-page gates: ask SM before --allow).
4. Owner (asleep) banked: the voice pick, 'sed' pronunciation, the music pick (existing sung Lyria songs lyria-three-of-three 2:59 and lyria-nothing-gets-deleted-here 2:23 in /data/work/belam-media are candidates; HOLD on any new music key/track), sung vs instrumental, the music video visuals (wait for the pick), four taste points with a keyframe each in video/banked/ (graph small top right, empty lower middle, chip over nodes, a line may break after a dollar sign).
5. C6 banked fault (council, no STT): beat 28 'So here we are.' shows 0.28 s (183.59-183.87 s), ~0.7 s early, once; a timestamped STT for C6 alone (one key via belam, cap <= $0.10 + the $0.50 floor) would fix it and cost a second partial join.
6. Walk edits that ride with the NEXT walk run only: percent-sign normalisation in media_fidelity, 429 retried like a 5xx (R1), key life via calendar.timegm (R2), 'r=' init hygiene.
7. For SM: R29a host act; the host-name history in a public commit.

FIRST ACT, before you own anything (council 3/3 10-21): run the DG3 after-check on one published chapter -> GREEN, and on a deliberately broken copy of it -> RED. Report both lines to SM.

## §2 Landed
M4 done 10-21 (DG3): 18 animated explainer mp4s published (batch of 15 at 15:51Z), joinprobe fix 94ee251c38, hand-over card.

## 🔴 Where it stops
Nothing is running. First command at first start: read this card, then `AGI_POST=director-review box read`.

## §4 Traps
- A timing or visual check cannot hear a dropped or swapped sentence (the timing DP re-fits around it, measured); the WER fidelity pass on the walk transcripts can.
- A threshold is calibrated on measured populations, never guessed (frame difference: same picture 0.00-0.18, real change 0.60-1.79, line 0.4).
- A hand-break harness: python3 -B, PYTHONDONTWRITEBYTECODE=1, delete the .pyc before and after, restore the file byte for byte, a byte-equal no-op mutant must SURVIVE.
- `box send TO` reads STDIN and prints nothing; verify with git log -1 refs/box/<you>/TO. Audio keys: limit >= planned + $0.50; usage lags hours.
- Drive: only the watcher touches it; the join key changes on a replaced chapter, so publish in few batches and say so in the README (line 3 of README-narration.txt).

## §5 Verification
The after-check on a chapter: GREEN on the published copy, RED on the broken copy (the §1 FIRST ACT).

## §6 BANKED
Owner (asleep): the voice pick, the word sed, the music pick (existing sung Lyria songs; HOLD on new music), sung vs instrumental, the music video visuals, four taste points (keyframes in video/banked/); the optional C6 timestamped STT. See §1 open 4-5.
