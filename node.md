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

## §1 Plan (written by director-general-3 at the hand-over, council 14:44Z 10-21; paths re-cut to the trunk 16:3xZ, council 16:24Z)

### paths
- DATA DIR (the chown target, not a home): /data/work/media/season3. In it: deliver/ = what the Drive watcher uploads (18 season3-CN-narration.mp3, 18 explainer-chNN-<slug>.mp4 h264 1280x720 25 fps yuv420p + aac 44100 mono, season3-explainer.html, README-narration.txt with rows + 3 header lines, README-music.txt, music-sample-a/b/c); deliver-static/ = the 18 static cards (undo = one rename back); deliver-tmp/ = rendered, not yet published (sibling of deliver/, same filesystem, NEVER inside deliver/); video/ = venv (manim 0.22.0, pip-freeze.txt), chNN-plan.json, chNN-drawn.json, checks/chNN.report.json + chNN.json, keyframes-chNN-1..3.png, banked/ (taste keyframes), media-chNN (manim cache, deletable); walk/ (voice walk chunks + transcripts), music/ (run.log + request log), m2/ (script copy). Queue files: /data/work/media/RENDERING (touched by `render`) and HOLD-GATES (touch after a chapter waited 1 h on the start test, tell SM, remove when done).
- CODE, on the trunk (repo-relative, run from YOUR OWN worktree, never another post's): extensions/agi/tests/media_video.py (beats, timing, checks, start test, watcher, publish/undo/queue, runner, joinprobe), media_vocab.py (the ONLY file that draws text), media_scene.py (one Chapter scene for all 18), media_mutate.py (hand-break sweep), media_html.py (M5), media_music.py (M6), media_walk.py / media_fidelity.py / media_recheck.py (voice), test_media_*.py. The script of record: .agi/context/media/season3-explainer-script.md at sha 6432bf88d5; the run doc: .agi/nodes/doc/season3-media-run.md. The data dir is named in ONE module, extensions/agi/tests/media_base.py (env MEDIA_BASE overrides; the queue files' dir: MEDIA_QUEUE_DIR). The code finds its repo from its own location (env MEDIA_REPO overrides); a COPY of the walk (season3/walk/walk.py) needs MEDIA_REPO.

### commands (cwd = the root of your worktree, python3 -B, nice 10, ONE heavy process at a time)
- start test: python3 -B extensions/agi/tests/media_video.py start [PEAK_MIB] (anon+shmem<3500, MemAvailable>=3 GB, mem PSI full<2, io PSI some<50, no gate pytest, headroom; fail closed).
- one chapter: python3 -B extensions/agi/tests/media_video.py render N, in the background with its log in video/, then poll for video/checks/chNN.report.json (it touches RENDERING, waits for the start test, renders under flock + nice + /usr/bin/time -v + ulimit -v 2500000 (a death at the ulimit = stop and ask), muxes into deliver-tmp/, runs every check, writes the keyframes). LOOK at the 3 keyframes, then python3 -B extensions/agi/tests/media_video.py publish N. Publish in few batches (one partial join per batch; belam: the watcher takes a replaced file one pass after its size changed); NEVER backdate an mtime (council 3/3 NO). Do NOT run the old helper scripts next.sh, wait.sh, sheet.sh, smoke.sh in video/: they cd into DG3's worktree.
- checks without a render: recheck N, sync N, joinprobe JOINED.mp4 N (is chapter N inside the joined full file the animated one; exit 1 unless animated; NO CARD / NO FRAME are RED), offsets N, plan N, timing, lint FILE.., queue.
- hand-break: python3 -B extensions/agi/tests/media_mutate.py (58+ rows, 1-2 h at load; prints only at the end; DO NOT edit media_video.py while it runs: it mutates in place). Music: media_music.py clip FILE.. / clip-track FILE.. (a real track must have 0 clipped samples). Voice walk: media_walk.py TTSKEYFILE STTKEYFILE (key files in your own keys directory, only via SM from belam; never mint).
- tests (the media lane sets MEDIA_LANE=1: a test that needs the data dir FAILS there when it is missing; any other suite SKIPS it): python3 -B -m pytest extensions/agi/tests/test_media_{video,mutate,html,recheck,walk,music,paths}.py -q -p no:cacheprovider --basetemp=<a dir under the data dir> (about 190 tests, 7 min at load).

### open
1. The joined-file after-checks (belam, on the watcher's local join): duration 3226.3 s +-0.5 and joinprobe N=0..17 after the 18-chapter join; the join before it is partial by design for one pass.
2. YOUR FIRST ACT (council 16:24Z), from your OWN checkout, no home path: in the data dir make a concat list of deliver/explainer-ch*.mp4 (ffmpeg -f concat -safe 0 -i LIST -c copy good.mp4) and a second list with deliver-static/explainer-ch02-*.mp4 in place of the C2 line (stale.mp4); then `python3 -B extensions/agi/tests/media_video.py joinprobe good.mp4 2` -> ANIMATED, exit 0, and the same on stale.mp4 -> STATIC, exit 1. Report both lines to SM. (sync N on the published file vs an -itsoffset 1 remux is the second pair.)
3. M5 inspector: BELAM'S STEP FIRST: install the design-taste-frontend skill for agi-director-review; then run its inspect.mjs on deliver/season3-explainer.html under the start test, view the screenshots, report FAILs as measured (its picture/motion floors are marketing-page gates: ask SM before --allow). Not run yet.
4. Owner (asleep) banked: the voice pick, the word sed, the music pick (existing sung Lyria songs lyria-three-of-three 2:59 and lyria-nothing-gets-deleted-here 2:23 in /data/work/belam-media are candidates; HOLD on any new music key/track), sung vs instrumental, the music video visuals (wait for the pick), four taste points with a keyframe each in video/banked/ (graph small top right, empty lower middle, chip over nodes, a line may break after a dollar sign).
5. C6 banked fault (council, no STT): beat 28 'So here we are.' shows 0.28 s (183.59-183.87 s), about 0.7 s early, once; a timestamped STT for C6 alone (one key via belam, cap <= $0.10 + the $0.50 floor) would fix it and cost a second partial join.
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
