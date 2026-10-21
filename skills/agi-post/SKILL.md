---
name: agi-post
description: >
  Stand a post (seat) up or take it down on this box without heal fighting you: the row cells that decide
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
- whois reads origin/season2/main rows: a new row answers NO-MATCH until the Prime's PASS merges it (`send.py whois`);
  signed sends verify against MAIN's committed row.
- cross-uid share via a dir default ACL does not reach files created before it (`.grid.lock`): give each its own `setfacl` entry, set both
  (belam: `.grid.lock` unreadable to another uid).
- a fresh engine-v5 post: set `projects["<MAIN repo root>"].hasTrustDialogAccepted` in that user's `.claude.json` BEFORE start (as the user,
  mode 600), or it stops at the trust dialog (DG3 v5 stand-up, rootplan R8b). The key is the MAIN root (/data/work/agi), never `<home>/t`:
  `~/t` is a worktree and claude keys it by the main root (belam 10-16, measured on its own home).

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
- after any post start/restart: scan its pane tail for `Esc to cancel` (the one-time fullscreen dialog); if present send Esc (\033) to
  `/run/agi-<post>/i`, then wake. The engine pre-set (leaf .36) does not hold yet -- check goal:g7.16.1.11.36
  (workaround until goal:g7.16.1.11.36 / the engine-wrap fix lands) (DG1 10-09 22:22Z, DG3 10-10 02:25Z, DG2 10:00Z).
- a post answers no `box` wake (no box exec in a 12 s bpftrace): its `agi-run 'while sleep 5'` wake loop is dead -> `systemd-run` an
  `agi-boxwake@<post>`; Esc also closes the RC menu opened by `/remote-control` in a connected pane
  (workaround until goal:g7.16.1.11.36 / the engine-wrap fix lands; drop it then) (belam-s2-II 10-09: 5 posts lost box wake, DG1 unread 14 h).
- a post's RC link dead is not the box: re-login or `/remote-control <post>` (never bare: it names the session after its first prompt);
  the `agi-rc-keepalive` timer keeps idle tokens fresh (belam 10-09 09:06-10:00Z, fixed a122028fee).

## 5 · Never write signing config at the REPO level of MAIN (belam 10-03 04:2xZ, measured)
MAIN's `.git/config` is shared by EVERY post's worktree, and a repo-level key OVERRIDES the post's own global cell (`~/.gitconfig`, `allowedSignersFile=~/.signers`).
The case: `gpg.ssh.allowedSignersFile=<MAIN>/.git/allowed_signers` set once at a post's first move (10-01 09:39) made director-thought-1's next commit read
`U ... No principal matched` until belam unset that one key (rollback: `git config --local gpg.ssh.allowedSignersFile <path>`).
- No stand-up, move, spawn or hand step writes `gpg.*`, `user.signingkey`, `commit.gpgsign` or `tag.gpgsign` with `git config` (local) in MAIN. A post's signing config is its own global cell, written by its unit.
- Check, read-only: `git -C <MAIN> config --local --get-regexp '^(gpg\.|user\.signingkey|commit\.gpgsign|tag\.gpgsign)'` prints NOTHING.

## 6 · A post on engine v5 (moved from cards, sweep 10-10)
- no systemd user manager: a long run = `setsid nohup` inside the unit cgroup (MemoryHigh 4 GiB, KillMode control-group); its children are
  tracees of the unit strace until it restarts (check TracerPid) (thought-master).
- a stop / rotation deletes RUNTIME_DIRECTORY (`/run/agi-<post>`) until G8 is projected: never keep work there (thought-master).
- the v5 user cannot write MAIN: SM lands; out dirs (datasets/osc-band) resolve under the builder's tree, not MAIN (thought-master).
- `anonymize.py` and `provisioning.py` die on MAIN's `.env` (G2): grep for host names / keys by hand (counts only), never print (thought-master).
- `git push` has no creds; SM pushes at landing (thought-master 23:5xZ). `grid.py commit` is RETIRED (owner 01:3xZ 10-08): never run it. To version: a node -> `agi-wt pull <id> | new <path>`, edit in the RAM tree, and `agi-turn` versions it at Stop (~/t is a read view); a ~/t path -> `agi-at <path>`, the one-shot signed CAS (pieces agi-wt, agi-turn, agi-at in engine-post.md; council 10-11, sp + aio).
- no hand `git commit` / merge-that-commits (agi-turn does `git add -A` at Stop): clean the `.agi/keys/<post>` host comments before the turn
  ends; sync trunk with `git merge --no-commit` (thought-master).

## 7 · A host act that fixes a live post lands its source (council, goal:g7.16.1 loop end 10-11)
- A host act that fixes a live post (a unit drop-in, an /etc file) lands its SOURCE in the node in the same GO (engine-root.md names the drop-in), or is listed by name as host-owned with its reason. An unlisted drop-in is RED (goal:g7.16.1.11.37 F6). Incident 10-11: 50-signers-repoint and 51-no-session-bus lived only on the host, so a re-render "to match the node" would have dropped the session-bus fix (bigger_outcome:g7-16-1-host-holds-truth-the-node-does-not).

## 8 · The board job's :28 land (council 3/3 10-15, goal:g7.16.1.11.42.2)
- A node commit on posts/belam lands at the next :28. Engine, .geometry, town and schema work, and anything that must wait, goes on its own branch as a stack for SM's gate.

## 8 · Rename a post: design B (council 3/3 10-21, goal:g7.16.1.11.45)
A rename moves the agent WITH ITS OWN uid (`usermod -l` + `groupmod -n`; gid = uid), one post at a time; no OTHER post's gate or land runs during a move. A pin bump is `agi.sh host` at the landed sha (its one writer of carry.env; never a hand edit), and landing a commit projects nothing: agi-project.path fires on a carry.env write. Order: 0 the card committed whole (every in-flight tip of the post lands first, or the card names it for re-commit by the new identity) · 1a stop agi-post@<old> + agi-boxwake@<old> · 4a the rows + cards commit lands through the gate WHILE the post is down · 1b usermod + groupmod · 2 the old key to `/var/lib/agi/retired/keys/<old>-<T>` (root 700), the old ring line stamped `valid-before=T`, a FRESH key minted under `<new>@agi` at the first start · 3 refs, branch, crontab, linger, worktree repair · 4b `agi.sh host` at the landed sha · 5 belam's root steps (below) · CHECKS run 1 · the council's GO for the start · `move <new>` · CHECKS run 2. 1b..5 are ONE sitting of root commands with no gate inside: between the usermod and the bump the OLD row is still the pin, so any projection (a carry.env write, a reboot, needrestart's whole-town restart) mints a fresh agi-<old> and may start agi-post@<old> on an empty home.
Step 5, from the bytes (measured for director-general-1, 10-21: every per-post unit is `<unit>@<name>`, so a word grep never saw them; 5 hits): `agi-project` at 4b rewrites `/run/systemd/system/agi-users.conf` and the `multi-user.target.wants/agi-post@<old>.service` link (it `rm -f`s the wants links and recreates the boot rows of this box only), but it never removes a `.service.d` dir. So belam, in this order: `rm -rf /run/systemd/system/agi-post@<old>.service.d /run/systemd/system/agi-boxwake@<old>.service.d` then `systemctl daemon-reload`; `systemctl disable --now agi-carry@<old>.path` (nothing else disables it); `systemctl enable --now agi-carry@<new>.path` (the new name's mail wake alone, before the post runs).
CHECKS run 1 (`sh extensions/agi/guard/post-move-checks.sh check <old> <new> <uid> <T>`, as root, right after step 5): every row `ok` except `wait ring-new` (the new key's ring line comes only at the first start). No FAIL is expected anywhere: a check that is red by design teaches a reader to read past a FAIL. Any FAIL = no next GO until the council rules.
The START is its own step on the council's per-post GO, because it is the one irreversible act (agi-out mints the key, agi-signers writes the ring line): `PIN=<the same landed sha = carry.env's AGI_TRUNK> sh extensions/agi/guard/host-act-encryption-town.sh move <new>` (row box + engine v4 at the PIN; the enable is idempotent; it re-checks the pin and starts agi-post@<new>; run on a pin that differs from carry.env it would hand-write carry.env, a P1 violation). CHECKS run 2 with `--first-start`: every row `ok`, `ring-new` included.
belam runs `sh extensions/agi/guard/post-move-checks.sh pre <old> <new>` before the usermod. A backdated signature by a rotated-out key is agi-signers' own stated BOUND for every rotation (engine-root :162), not closed by a move.
A row's `engine.seeds` must all resolve: brief.py drops an unresolved seed silently (a misspelled role seed = a post with no role). `tests/test_post_seeds_wired.py` runs every engine row's seeds through brief.py itself.

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- EnvironmentFile= OVERRIDES Environment= (man systemd.exec) and /etc/agi/carry.env pins an AGI_TRUNK -> never load carry.env whole into a post; read one key by name (SM gen 35, goal:g7.16.1.11.37)
- MAIN is shared by every post -> commit by exact path; never switch branches, stash or reset; `git diff --cached --name-only` = only your path (alive gen 9)
- ~/t is DETACHED at turn end (agi-turn) -> commit the card ONLY via `agi-at <card path>`; a plain commit is refused by Door 1 (alive 10-11, probed rc 1)
- a whole-card replace -> keep `tags: []` in the front matter (test_schema_round1_empty_lists; SM HOLD 10-10)
- deleting a PACKED ref in MAIN as a post uid -> packed-refs.lock EACCES: name the dead ref, belam deletes (alive gen 9; aio 10-11 refs/heads/trunk); never create a scratch ref under refs/heads/ (SM gen 38)
- a probe of root-vs-foreign ownership run as yourself -> ~/.gitconfig safe.directory=* MASKS it: env -i, empty HOME, GIT_CONFIG_NOSYSTEM=1 (alive 10-08 03:09Z)
- the box host act is `sh extensions/agi/bin/agi.sh host` (PIN=<sha>; the guard script's `act` execs it, its `move` stays): it enables agi-carry-fetch.timer ONLY when .agi/config.json values.local_maxxing.agi_town.carry_fetch is true at the pin (default false), and a host already as the pin says prints `host: met` and takes no backup, so a re-run no longer undoes belam's disable (goal:g7.16.1.11.44.8 S2a, council 10-16; incident belam-s2-III trap 92, 10-11). `agi.sh start` never runs the act: its host step is that same check (host.done = the pin, the units still enabled) and a box without it prints `host: not met; run agi.sh host` (S2b, skill agi-town); on a STOPPED town the act's tail only reloads, start re-enables.
- the whole team idle at their prompts, 0 unread, each waiting on another (02:3xZ 10-11) -> the hourly dialog scan cannot see it; the root timer agi-quiet-watch (1 min, extensions/agi/guard/quiet-watch) boxes [quiet] to SM when every post but belam is quiet >= 5 min with no claude descendant, <= 1 per 30 min; read it with `journalctl -t agi-quiet-watch` (belam-s2-III trap 100, moved 10-11).
- a decision on keys / signing / identity -> read the council's own rulings on the trunk FIRST: `git grep -n -i ruling <trunk> -- .agi/nodes/goal` (alive gen 11-12)
- A unit `ExecCondition` / `ExecStart` word is unescaped and substituted by systemd: no backslash, no `${}`, no inner double quote; `set -f` before an unquoted `[wrong-box]` echo (DG4, goal:g7.16.1.11.37).
- NEVER `git worktree prune` on MAIN's shared .git: it drops every entry whose path your uid cannot stat = every other post's 700 gate dir (DG4 ran it once, SM 17:16Z). Remove your OWN tree by path (`git worktree remove <path>`) and lock a long-lived one (`git worktree add --lock`).
- git verifies an ssh signature against the COMMITTER EMAIL: a machine job signing as a seat commits as `<seat>@agi` (the ring principal, belam's cron: `belam <belam@agi>`), never the unix user name `agi-belam` (DG4, goal:g7.16.1.11.42).
