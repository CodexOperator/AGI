---
name: agi-post
description: >
  Stand a post up or take it down on this box without heal fighting you: the row cells that decide
  crash-respawn (recover, pid), the one sanctioned spawn command and the row fields it reads, the card a new
  post's brief is built from, re-homing a row from another box, keys and whois, and a hand restart after a
  reboot. Use whenever a post is added, re-homed, stood up, taken down, or restarted by hand (rotate.py stand-up).
---

# agi-post — stand up · take down (owner 09-29: "Need a post stand up/takedown skill")

Source of truth: `heal.py _watch_seats` (crash-respawn) · `rotate.py cmd_spawn` (stand-up) · `brief.py render` (first turn) ·
`.agi/context/schemas/[config].md` (row fields). Mapped 09-29 by belam-S2-L5-XV — the cites below are by function name (no line numbers); re-verify after engine edits.

## 1 · Take a post DOWN, and keep it down
```
1. tell the post: finish the atomic step, write + commit its card, reply "[rotation] <post> down-ready"
2. its row in MAIN posts.md: "recover": false (a JSON boolean: the STRING "false" reads true) AND "pid": 0
   one write.py config:posts write (--actor belam --role prime_director, --dry-run first) -> commit by exact path
3. only then stop it: tmux kill-window -t agi-rc:<@window>        heal polls every 30 s: flags FIRST, kill second
```
- heal relaunches a row when pid > 0 and box == AGI_BOX and its pid, window and pinned session are all gone and no newer or
  in-flight rotation exists (pid > 0 + local box: `heal.py _watch_seats`; the newer/in-flight-rotation skip: `heal.py _watch_one_seat`);
  `recover: false` = logged, never relaunched (`heal.py _watch_one_seat`).
- a worktree post (director-thought, director-engine): heal reads its row from the WORKTREE's posts.md, identity cells from MAIN
  (`heal.py _live_seat_row`): `pid: 0` in MAIN excludes it outright; `recover: false` alone must also reach the worktree copy.
- a merge-up from the post's branch can restore cells (skill agi-master-gate): re-check both cells after any merge.

## 2 · Stand a post UP
```
0. its row in MAIN posts.md, committed BEFORE spawn: name · role (director | parent | …) · model · effort · settings · box = this box ·
   town (a ladder town; `all` is refused) · template (masters: doc:unified-master-brief) · worktree ("" = MAIN) ·
   identity cells EMPTY (pid 0, window "", session_*) · pubkey "" unless its key file is on this box
1. its card: write.py create doc card-<post> --parent goal:<g> --body-file <f>     the brief = HEAD + template + CARD (+ STARTUP)
2. python3 extensions/agi/bin/rotate.py spawn --seat <post> --dry-run   ->   the same without --dry-run     (from MAIN, never on master)
```
- spawn reads name/role/model/effort/settings/worktree/pid/generation/pubkey/template; `--model`/`--effort` must match the row
  (exit 3, `rotate.py _cmd_spawn`); the harness comes from the flag (default claude-code); the window lands in tmux agi-rc (`rotate.py spawn_window`).
- it starts FRESH (no --resume), mints a key if the row has none, writes pid/window/session cells, commits ONLY its own row and
  pushes the current branch: commit your own row edits first (a dirty posts.md refuses the later ack).
- never `seats-launch` for one post: it starts EVERY non-fire-and-forget row (council and other-box rows too) and writes no row,
  key or commit (`rotate.py cmd_seats_launch`).
- the role must be one config:brief has parts for: a `council` role has none (spawn crashes) — a council post keeps `role: director`.
- whois reads origin town-trunk rows: a new row answers NO-MATCH until the Prime's PASS merges it (identity via posts row);
  signed sends verify against MAIN's committed row.

## 3 · Re-home a row from another box
Formal route: `rotate.py migrate --post <p> --to <box>`, run ON the source box. From this box instead: ONE row write that sets box
and town, clears pid/window/session_*, the worktree (unless it exists here) and pubkey/key_history (no key file here = the post
cannot sign; spawn then mints one). Skip it and heal treats the old pid as a dead LOCAL post and retries it every pass.

## 4 · A hand restart (after a reboot) = the ONE stand-up verb
```
python3 extensions/agi/bin/rotate.py stand-up --post <p>        (from MAIN)
```
- = `rotate.stand_up(mode="restart")`: the post's launch lock -> heal's recover body -> `--resume <session_id>` when the row's
  transcript exists, fresh otherwise -> the row written (window now, pid at the join) -> a crash-recovery record (`probable_cause: hand-restart`)
  the after_join service joins, pins and acks.
- refuses a row with an `engine` cell by name (`stand-up refused: <post> is engine vN (systemd-owned)`: strip the cell first),
  a post whose row pid is alive or whose window @id is open, and a stand-up of the same post already in flight (lock
  held): never a second live session.
- spawn · rotate-self · heal recover · stand-up are the four callers of ONE verb (goal:g7.16.1.7.1.1.4): never start a post's
  `claude` by hand.

## 5 · Never write signing config at the REPO level of MAIN (belam 10-03 04:2xZ, measured)
MAIN's `.git/config` is shared by EVERY post's worktree, and a repo-level key OVERRIDES the post's own global cell (`~/.gitconfig`, `allowedSignersFile=~/.signers`).
The case: `gpg.ssh.allowedSignersFile=<MAIN>/.git/allowed_signers` set once at a post's first move (10-01 09:39) made director-thought-1's next commit read
`U ... No principal matched` until belam unset that one key (rollback: `git config --local gpg.ssh.allowedSignersFile <path>`).
- No stand-up, move, spawn or hand step writes `gpg.*`, `user.signingkey`, `commit.gpgsign` or `tag.gpgsign` with `git config` (local) in MAIN. A post's signing config is its own global cell, written by its unit.
- Check, read-only: `git -C <MAIN> config --local --get-regexp '^(gpg\.|user\.signingkey|commit\.gpgsign|tag\.gpgsign)'` prints NOTHING.

