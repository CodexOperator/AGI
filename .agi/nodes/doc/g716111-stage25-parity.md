---
id: doc:g716111-stage25-parity
mint_id: 05fcb1c04f11497f9d0d2ed3b5d1dd4d
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: aa60178499b80f68
season: 2
title: "g7.16.1.11 stage 2.5 prep: the capability parity table (42 rows), the node-code auto-link and the per-node RAM worktree designs, the candidate post"
town: core
---
# doc:g716111-stage25-parity

Stage 2.5 PREP of goal:g7.16.1.11 (owner 02:55Z: one live post on the live repo, capabilities matched or exceeded). Read-only research by an Opus 5.5 subagent of director-general-3, 03:1xZ 10-01. The (a) agi-link and (b) agi-wt drafts were run on a throwaway clone; their bytes live off-graph until a stage-2.5 build lands them in config:engine.

## Stage 2.5 candidate — ONE live local-town post on the live repo

**director-general-6.** (1) STOOD DOWN on the owner's order since 09-30 06:2xZ, its handover done, no live parent, round or mur
named on its card (DG5 still has a detached parent; DG4 handed leftovers back 5 h ago; DG1-DG3 are mid-work; stream-master owns the
public stream; the Prime and the councils are excluded). (2) Its row already reads `recover: false`, so today's heal.py names it and
never respawns it — the two engines cannot both seat it. (3) Smallest history to carry (1 rotation record, a 6 KB card).

Cost note to BANK, not decide: re-seating a post the owner stood down "to conserve tokens" spends tokens; the 2.5 run should be
budgeted (one goal leaf, Sonnet 5.5 per the owner's 02:27Z order) and the harness login for its new uid is unresolved (parity row 31).

## The switch (one row cell)
config:posts row director-general-6 gains `"engine": "v3"`; agi-project's selector becomes `select(.engine=="v3")` (parity row 1).
`recover: false` stays (keeps heal.py off it).

## Rollback to today's engine — one command, from MAIN
```
sudo systemctl stop agi-post@director-general-6 && sudo rm -f /run/systemd/system/multi-user.target.wants/agi-post@<director-general-6>.service && python3 extensions/agi/bin/rotate.py stand-up --post director-general-6
```
preceded by the row edit that drops `"engine"` (write.py config:posts, committed) so agi-project does not relink it on the next
trunk move. The work survives: everything the v3 post did is on `refs/posts/director-general-6/head` (agi-flush pushed it at stop),
left for the master to gate and land like any merge-up (never merged straight into MAIN's checked-out town trunk); its `agi-director-general-6` user and /var/lib/agi home stay
(retire, never delete). With parity row 3 fixed (agi-project unlinks dropped rows) the `rm -f` leg disappears.

## Stage 2.5 PARITY TABLE — today's local-town director post vs config:engine (v2 committed + proposed v3)

Read from the bytes, 10-01: skills/agi-*/SKILL.md frontmatter, doc:unified-director-brief (§0-§3), config:rotations
`templates.director.startup.first_turn` + `after_join`, config:posts row cells, extensions/agi/hooks/, config:crons,
config:guard RAM cells; new side = .agi/nodes/.geometry/engine.md (v2) + /tmp/agi-stage2/pieces/engine.diff (v3).
Status: MATCH = works as-is · PARTIAL = piece exists, bytes or a root act missing · MISSING = no piece · EXCEEDS = better than today.
MAIN = the live repo checkout. `<c>` = the candidate post (candidate.md). No value of a key, id or path-secret is printed by any proof.

| # | capability | today's mechanism | new mechanism | status · gap / bytes to add | proof on the live post |
|---|---|---|---|---|---|
| 1 | post identity = one row | config:posts row; rotate.py spawn/stand-up reads it | agi-project (row -> unit, user, H drop-in) | PARTIAL · selector is `recover!=false` = 10 rows today; stage 2.5 needs ONE: `select(.engine=="v3")` (~20 B) | `sect agi-project \| sh -s /tmp/x HEAD; ls /tmp/x/multi-user.target.wants` = only agi-post@<c> + agi-project.path |
| 2 | stand up / seat | skill agi-post §4: `rotate.py stand-up --post`; tmux window | agi-post@.service + agi-seed (v3: system manager, sysusers) | MATCH · 3 root acts (sysusers, agi.rules, daemon-reload) | `systemctl is-active agi-post@<c>` |
| 3 | take down / no double seat | heal.py `recover` cell (false = named, never respawned) | agi-project selector | PARTIAL · agi-project never UNlinks a dropped row (`ln -sf` only): add `rm -f $w/agi-post@*` before relinking (~25 B); keep `recover:false` on <c> so heal.py never respawns it in parallel | drop the cell, re-run agi-project: the wants link is gone |
| 4 | harness + model cells | harness_template.py via rotate.py spawn | v3 h.conf drop-in `H=claude --model <m> -c` / pi line | MATCH | `systemctl show -p Environment agi-post@<c> \| grep -c -- --model` = 1 |
| 5 | effort cell | harness_template.py passes effort | pi only (`--thinking`); claude-code drops it | PARTIAL · project effort for claude-code (env or settings line, ~40 B) | the session's first transcript line names the effort |
| 6 | settings cell (`quiet` / "") | harness_template.py settings variants | ONE settings.json for all | PARTIAL · a per-row variant merge (~40 B jq) or accept one | `jq -c .hooks ~agi-<c>/.claude/settings.json` |
| 7 | the brief (HEAD + template + card) | rotate.py `brief_file`; doc:unified-head + doc:unified-director-brief + doc:card-<p> | agi-brief + brief.py (walk from card + claims) | **BLOCKER** · brief.py walks `.agi/n/<mint>/p/*` symlinks; MAIN has no `.agi/n/` (5,385 nodes in `.agi/nodes/<type>/`) -> `os.listdir('n')` fails -> EMPTY brief. Adapter: build A from `parents:` frontmatter (~300 B); seed the row's `template` + doc:unified-head too (~60 B) | `B=0 agi-brief \| sed -n 2,6p` lists doc:unified-director-brief and doc:card-<c> |
| 8 | first-turn STARTUP OUTPUT | config:rotations `first_turn`: rotation-record, facts, prime-authority, git-state, predecessor-log, inbox, live-spawns, send-verbs, skills (byte_cap 8000) | none | MISSING · agi-brief runs each `cmd` of the role's first_turn under byte_cap (~150 B sh) | `agi-brief \| grep -c '^## STARTUP OUTPUT'` = 1 |
| 9 | the meter (rotate at the line) | hooks/rotation_alert.py (UserPromptSubmit) + `rotate.py meter --pin <pin_ref>`; `rotate_at` 0.47 | settings.json UserPromptSubmit hook, 470000 tokens hard-coded | PARTIAL · line not read from the row's `rotate_at` x window (~60 B) | feed the hook a synthetic transcript over the line: it prints the out-line |
| 10 | rotation = fresh successor | `rotate.py rotate`: card, out-line, new window, fresh session | `kill $PPID` -> Restart=always -> `${H} go` | **BUG** · H carries `claude ... -c`: the restart RESUMES the over-the-line context (meter fires again at once), and a first start has no conversation to continue. Fix: hook `touch ~/.fresh`; ExecStart drops `-c` when it exists (~70 B) | after a line-kill the new session's first usage line is < 50k tokens |
| 11 | rotation record / ack / telemetry | rotation_record.py -> .agi/sessions/rotations/<p>.<ts>.json (seed, model, effort, window, ack, meter, generation) | journal only | MISSING · ExecStartPre appends one record line (~100 B); the ack is the unit reaching active | `ls .agi/sessions/rotations/ \| grep -c <c>` grows by 1 per restart |
| 12 | after_join (join, pin, reap-proof) | rotate.py service tail: tmux list-windows, meter --pin, ps grep | one unit = one cgroup; a restart reaps the whole tree | EXCEEDS · 0 B | `systemctl show -p NRestarts --value agi-post@<c>` increments; TasksCurrent > 0 |
| 13 | card (one scratch, replaced whole) | write.py doc:card-<p> + .agi/sessions/quorum/<p>.md symlink | card in the post's checkout, seeded by agi-brief | MATCH · the quorum symlink is not needed (sessions/ is gitignored) | `git -C ~agi-<c>/t log -1 --format=%s -- .agi/nodes/doc/card-<c>.md` after a turn |
| 14 | inbox read (exactly once, VERIFIED header) | send.py read -> MAIN `.agi/sessions/inbox/<p>.md` (gitignored) | agi-inbox@.path on /var/spool/agi/<p> | PARTIAL · the inbox lives in MAIN, ignored by git, so the clone never sees it: <c> must run `send.py read` from MAIN (group write on MAIN `.agi/sessions` + `.agi/comms` = root act), 0 B code | as agi-<c>, `cd MAIN && send.py read <c>` prints the unread dm |
| 15 | send dm / room / report / escalate | send.py send: comms file + inbox append + sign line | refs/mail/<to>/<id> designed in doc:radically-simple-engine B.1, NOT a piece | PARTIAL · bridge = run send.py from MAIN (row 14); refs/mail stays future | `send.py send <c> <master> ...` from MAIN; the master's inbox file grows |
| 16 | wake / nudge | send.py wake/nudge (tmux send-keys + Enter); cron nudge_sweep | agi-inbox@.path -> `echo mail \| dtach -p` | PARTIAL · agi-project never enables agi-inbox@<p>.path (~70 B); nothing writes /var/spool/agi/<p>: send.py `touch` for engine:v3 rows (~150 B Py) + a tmpfiles spool line (~40 B, root); nudge_sweep must skip v3 rows (~40 B); `echo` sends LF, not CR — submit UNPROVEN | `touch /var/spool/agi/<c>` -> a `mail` user turn appears in the transcript |
| 17 | whois / authority verify | send.py whois --claim; row `pubkey`, `sig_scheme`; private key `.agi/sessions/seats/<p>.key` (MAIN) | per-user ssh key + `signers` | PARTIAL · two keys for one post: send.py signs with the seat key in MAIN (unreadable by agi-<c> without a key-handling root act) and the row pubkey is not the ssh key -> BANK (Prime: keys) | `send.py whois <c>` reads VERIFIED after <c>'s first send |
| 18 | key rotation / key_history | rotate.py `.key.pending` swap, `key_history` cell | key minted once at first start, never rotated | MISSING · acceptable for 2.5; ~80 B later | — |
| 19 | signed commits | none (dm lines only are signed; grid commits unsigned) | gitconfig `gpgsign` (ssh) + signers | EXCEEDS · gitconfig lacks `gpg.ssh.allowedSignersFile` so nothing can VERIFY (~45 B) | `git -C ~agi-<c>/t verify-commit HEAD` rc 0 |
| 20 | write a node (spawn gate, schemas) | skill agi-node-write: write.py | plain paths in the clone; write.py runs unchanged there | MATCH | `write.py goal:g7.16.1.11 'read body 1:5'` in the clone |
| 21 | commit at turn end | write.py commits by exact path; card committed by hand | Stop hook `git add -A .agi; git commit` | PARTIAL · `-A .agi` sweeps every tracked .agi change (comms, other nodes) into <c>'s commit: scope to a `commit_paths` cell (~25 B) | `git -C ~agi-<c>/t show --stat HEAD` touches only <c>'s paths |
| 22 | hand up the work (merge-up) | §1: post branch LOCAL-ONLY, one [merge-up] line; master lands | agi-flush: `pull origin trunk && push refs/posts/<p>/head` | **BLOCKER** · MAIN has no `trunk` branch: the pull fails, the `&&` skips the push -> work never leaves the clone. Cell `trunk` = the town trunk (~25 B); agi-master-gate reads refs/posts/<c>/head (skill text, 0 B) | `git -C MAIN rev-parse --verify refs/posts/<c>/head` after a stop |
| 23 | master gate / land | skill agi-master-gate: merge-tree / commit-tree onto the town trunk | pre-receive + agi-gate on refs/heads/trunk | PARTIAL · NOT installed on MAIN for 2.5 (it would gate every post's push); today's master gate lands refs/posts/<c>/head unchanged | `git merge-base --is-ancestor refs/posts/<c>/head <town trunk>` after a landing |
| 24 | path ownership | write_guard.py + the "never touch another post's worktree/row" rules | pre-receive `owner` attribute check | MISSING data · no `owner` attrs in MAIN's .gitattributes (~1 line per group) | `git check-attr owner -- .agi/nodes/doc/card-<c>.md` |
| 25 | grid versions | grid.py commit --all on season2/main (Prime), refs/grid/<ns>/node/<mint> (9,444 refs) | `git log -- <node>` (grid retires) | MATCH for 2.5 · keep today's Prime grid commit at land, 0 B | `grid.py log <a node <c> edited>` shows the landed version |
| 26 | node <-> code-file pairing | level3.py (git ls-files -> one build node, `payload_ref`); grid.py: node + payload = ONE version | none ("the node IS the file" covers engine pieces only) | MISSING · `agi-link` 359 B (design-ab.md (a)) | `agi-link HEAD` names build:<x> for every code path HEAD touched |
| 27 | per-node tiny worktree, RAM, purged | dispatch.py `ram_worktrees_dir` (GUARD_RAM_WORKTREES: WHOLE-repo round worktrees) + heal.py `_sweep_finished_worktrees` | none | MISSING · `agi-wt` 705 B + cells (design-ab.md (b)) | `agi-wt pull <mint>` = 2 files; `drop` -> dir gone, worktree list back |
| 28 | the post's checkout | `worktree` cell: git worktree of MAIN (shared objects) | v3 `git clone $O t` into /var/lib/agi/<p> | PARTIAL · MAIN is on tmpfs, /var/lib on ext4: a plain clone copies the pack (338 MiB) + 9.4k grid refs. `--shared --single-branch -b <trunk>` measured 1.8 MB (~30 B); trap: MAIN's gc may prune an object only the clone uses -> agi-flush keeps refs/posts/<p>/head reachable | `du -sk ~agi-<c>/t/.git` < 10 MiB |
| 29 | claims | `owning_goal` cell + board (sanctuary-master); spawn_budget leases | refs/claims/<mint> create-only CAS; agi-brief seeds from claim ref FILES | PARTIAL · MAIN `refs/claims/` must be a group-agi sticky dir and `gc.packRefs=false` on MAIN (a packed claim is invisible to `find`) = MAIN config change; `owning_goal` not seeded (~40 B) | `git -C MAIN update-ref refs/claims/<mint> HEAD 0000…` (2nd = "reference already exists"); brief rank moves |
| 30 | dispatch parents / kids | skill agi-dispatch: dispatch.py (ladder tier, --branch worktree, spawn bound, behind-origin refusal, rebrief) | refs/posts/<me>/kids/<k> designed, NOT a piece | PARTIAL · run dispatch.py from MAIN as agi-<c> (bound + leases live in MAIN); from the clone the tree-wide bound is per-clone = unbounded. 0 B code; perms + env (row 31) | `spawn_budget.py status` (MAIN) lists <c>'s parent |
| 31 | per-spawn keys / spend floor | provisioning.py, MAIN .env, envfile.py --check | EnvironmentFile /var/lib/agi/<p>.env (secrets, root-owned) | PARTIAL · root act per post; the harness LOGIN for agi-<c> is unsolved (no credential in the new home): copy the owner's harness credential (key handling -> Prime) or an API key (spend the owner has not named) -> BANK | `envfile.py --check` as agi-<c> = pass |
| 32 | kid/parent commit guard | hooks/agent-git pre-commit/pre-push (AGI_TIER) in MAIN .git/hooks | pre-receive owner groups | PARTIAL · the clone has no hooks: `core.hooksPath` line in gitconfig (~40 B) | `git -C ~agi-<c>/t config core.hooksPath` |
| 33 | review (mur) / workflows | skill agi-workflow: workflow.py run ... --harness pi-free, detached via `systemd-run --user` | runs in the clone if pi + key are present | PARTIAL · `systemd-run --user` needs agi-<c>'s own user manager (`loginctl enable-linger`, root act) or a system transient unit | a mur run key appears and its verdict file lands |
| 34 | judge / corrective / goal edits | season.py judge; skills agi-corrective, agi-goal | the same Python, in the clone | MATCH | `season.py status` in the clone |
| 35 | crash heal | heal.py `_watch_seats` (pid, recover, PSI admission, one launch per pass) | Restart=always + tick.sh | PARTIAL · no timer runs tick.sh (agi-tick.timer + .service ~150 B); no PSI admission on restart (StartLimit/RestartSec cells ~40 B) | `systemctl kill agi-post@<c>`; active again, a drift commit if projected != observed |
| 36 | memory caps | mem_cap.py scopes; agi.slice / ramdisk.slice; ManagedOOM; memory_alarm cron | `MemoryHigh=4G` in the unit | PARTIAL · no `Slice=` (lands in system.slice, outside agi.slice's oomd domain) ~20 B; MemoryMax / MemorySwapMax cells ~40 B | `systemctl show -p Slice,MemoryHigh agi-post@<c>` |
| 37 | box reads / stop a runaway | skill agi-memory-guard | uid isolation: <c> can stop only its own processes | MATCH (reads) · stop is narrower by design | the guard's reading command as agi-<c> |
| 38 | verify + suite lock | skill agi-verify: commands.py run verify; verification.py window lock in MAIN | "no suite lock" (CALM) | PARTIAL · a per-clone lock is no box-wide single runner; box memory still needs one: point the lock at MAIN (cell, ~30 B) or run the suite only from MAIN | `verification.py window` from the clone names MAIN's lock |
| 39 | stream / desktop / live view | viewport.py --live; skill agi-stream; agi-desktop-check screenshots tmux panes | dtach socket + strace file track `~/r` | MISSING (view) · no pane to screenshot; home 0700 hides the transcript from the dashboard: an owner-readable view (`dtach -a` read-only, or a group-read transcript dir) ~60 B + perms | `viewport.py --live` shows <c>'s last act |
| 40 | crons (grid_sync, branch_push, mail_poll, nudge_sweep) | config:crons + crons.py apply (owner crontab) | tick + agi-frontier, no timers | MATCH for 2.5 · owner crons keep running; nudge_sweep skip = row 16 | `crons.py show` unchanged |
| 41 | file-access trace (what a session opened) | none | strace `-e%file` -> `~/r`, agi-flush -> `~/track` | EXCEEDS · 0 B | `wc -l ~agi-<c>/track` > 0 after a session |
| 42 | anonymize | anonymize.py + §2 rule | ident `agi-<p>` / `agi@agi` | MATCH | `git log -1 --format='%an %ae'` = agi-<c> agi@agi |

## Counts
42 rows = **MATCH 9** (2, 4, 13, 20, 25, 34, 37, 40, 42) + **EXCEEDS 3** (12, 19, 41) + **PARTIAL 20** (1, 3, 5, 6, 9, 14, 15, 16, 17, 21,
23, 28, 29, 30, 31, 32, 33, 35, 36, 38) + **MISSING 7** (8, 11, 18, 24, 26, 27, 39) + **BLOCKER/BUG 3** (7 brief, 10 rotation `-c`, 22 flush/trunk).
Matched or better today: 12 of 42.

## Bytes to parity (code only, excl. root acts)
brief adapter 360 · agi-wt 705 · agi-link 359 · startup first_turn 150 · tick timer 150 · send.py spool touch 150 · record 100 ·
fresh-sentinel 70 · inbox path enable 70 · meter cell 60 · view 60 · small cells (selector, unlink, effort, settings, signers file,
commit scope, trunk, clone flags, owning_goal, hooksPath, Slice, caps, lock, nudge skip, StartLimit) ~520 -> **~2.9 KB**.

## Root acts the 2.5 run needs (the owner's / Prime's call)
sysusers + agi.rules + daemon-reload (v3) · group write for agi-<c> on MAIN `.git` + `.agi/sessions` + `.agi/comms` ·
refs/claims sticky dir + `gc.packRefs=false` on MAIN · /var/spool/agi/<c> · /var/lib/agi/<c>.env · the harness credential ·
linger for agi-<c> (detached workflows) · /mnt/agi-ram/wt/<c> (tmpfiles line, design-ab.md).

## Stage 2.5 — designs (a) auto-link node <-> code file(s) and (b) the per-node tiny worktree on the RAM disk

Both are engine pieces in config:engine's style: a small sh template over raw git, parameters as cells, extracted with
`sect <name>`. Both drafts were RUN on a throwaway `git clone --shared --single-branch` of MAIN under /tmp/agi-stage25
(1.8 MB .git; removed after), never on MAIN. Files: /tmp/agi-stage25/bin/agi-link, /tmp/agi-stage25/bin/agi-wt.

## What exists today (the thing to match)
- The link IS a frontmatter cell: a build node carries `payload_ref: <repo path>` (293 nodes in .agi/nodes/build/).
  level3.py mints one build node per tracked file passing payload_boundary.classify() (`--mint-missing-only`).
- A version = ONE grid commit of node + payload (grid.py `build_tree`, ref `refs/grid/<ns>/node/<mint>`), written by the
  Prime's `grid.py commit --all` on season2/main.
- Round worktrees are WHOLE-repo: dispatch.py `ram_worktrees_dir` (cell `GUARD_RAM_WORKTREES_<box>` = /mnt/agi-ram/worktrees,
  `.agi/worktrees/<agent>` symlinked to it), held at `GUARD_RAM_WT_HOLD_PCT_<box>` (60), reaped by heal.py
  `_sweep_finished_worktrees` (lease gone, archived if unmerged/dirty, grace). RAM pages charged via mem_cap.py ram-exec to ramdisk.slice.

## (a) agi-link — 359 B
The link stays the `payload_ref` cell (one writer, already on 293 nodes); the piece READS it both ways and flags the gap.
~~~sh
#!/bin/sh
r=${1:-HEAD};git diff --name-only $r~ $r -- ${AGI_LINK_ROOTS:-extensions skills src}|while read f;do n=$(git grep -lE "^payload_ref: \"?$f\"?$" $r -- .agi/nodes/build|head -1)
[ "$n" ]&&echo "$(git show $n|sed -n 's/^id: //p;/^id:/q') $f"||{ echo "unlinked $f";[ "$AGI_LINK_MINT" ]&&python3 extensions/agi/bin/level3.py --mint-missing-only;};done;:
~~~
- Cells (config:engine frontmatter, projected into the h.conf drop-in as Environment=): `link_roots: extensions skills src`,
  `link_mint: ""` (empty = report only; non-empty = mint the missing node through today's level3.py — the spawn gate stays its job).
- Node -> files is the same cell read the other way: `sed -n 's/^payload_ref: *//p' <node>`; agi-wt (b) uses it to know what to pull.
- History of the pair (replaces the grid's ONE-version read for a post that never runs grid.py): `git log -- <node> <payload>`;
  a drop commit from (b) touches both together, so one commit = one version of the pair.
- Plugs into: the turn-end commit (settings.json Stop hook / agi.ts `turn_end`) — `agi-link HEAD >>.agi/drift/$USER` after the
  commit (~30 B), and agi-flush before the push; optionally agi-gate refuses a tip with an `unlinked` line under link_roots (~40 B).
- Proven (measured on the shared clone, a real MAIN commit that touched rotate.py):
  `build:bin-heal extensions/agi/bin/heal.py` · `build:bin-rotate extensions/agi/bin/rotate.py` · `unlinked extensions/agi/tests/test_rotate_stranded_window.py`.
  Live proof on <c>: edit a linked file in the post's checkout, end the turn, `tail -3 .agi/drift/agi-<c>` names its build node;
  add a new file under extensions/: it reads `unlinked`, and with `link_mint` set the next commit carries its new build node.

## (b) agi-wt — 705 B
A node's version is authored in a SPARSE worktree holding only the node file + its `payload_ref` file(s), on the RAM disk,
pulled in when the node is taken up for a new version and purged when that version is committed.
~~~sh
#!/bin/sh
set -e;r=${3:-HEAD};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};mkdir -p $w;f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);m=$(git show $r:$f|sed -n 's/^mint_id: //p');d=$w/$m
case $1 in pull)[ -d $d ]&&{ echo $d;exit;};[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;}
git worktree add -q --no-checkout --detach $d $r;git -C $d sparse-checkout set --no-cone /$f $(git show $r:$f|sed -n 's|^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$|/\1|p');git -C $d checkout -q;echo $d;;
drop)git -C $d add -A;git -C $d commit -qm"$USER: $2"||:;git merge -q --no-edit $(git -C $d rev-parse HEAD);git worktree remove $d;git worktree prune;;esac
~~~
- **Location cell**: `wt_root` (config:engine frontmatter; a posts row may override). agi-project writes it into the post's
  h.conf drop-in as `Environment=AGI_WT=<wt_root>/<p>` (~45 B in agi-project). Unset = `$RUNTIME_DIRECTORY/wt`
  (= /run/agi-<p>/wt, the unit's own RuntimeDirectory: tmpfs, ZERO root acts, removed by systemd when the unit stops).
  Recommended value on local-town: `/mnt/agi-ram/wt` (the dedicated RAM disk, already budgeted by GUARD_RAM_BUDGET).
- **Hold cell**: `wt_hold_pct` (default 60 = today's GUARD_RAM_WT_HOLD_PCT_local_town) -> AGI_WT_HOLD; pull exits 3 "hold".
- **Age cell**: `wt_age` (default 1d) — agi-project emits one tmpfiles line per row, like sysusers:
  `d /mnt/agi-ram/wt/<p> 0700 agi-<p> agi <wt_age>` (~50 B in agi-project; ONE root act at install). `systemd-tmpfiles --clean`
  is the orphan reaper (a worktree left by a crash), replacing heal.py's sweep for these trees.
- **Pull-in trigger** (a node is being versioned): the claim. The claim act becomes
  `git update-ref refs/claims/<mint> HEAD 0000… && agi-wt pull <mint>` (one line in the director skill / agi-brief's STARTUP:
  every claim the post owns is pulled at wake, ~40 B). A session may also `agi-wt pull <id>` on demand before an edit.
- **Purge trigger** (done): (1) turn end — the Stop hook / agi.ts `turn_end` commits inside every `$AGI_WT/*` (the version is
  recorded each turn) and runs `agi-wt drop <mint>` for each whose claim ref is gone (released = done) (~120 B);
  (2) session end — agi-flush drops every remaining tree before its push (~40 B), so a rotation never strands one;
  (3) the age line above for anything a crash left.
- **RAM accounting**: tmpfs pages are charged to the cgroup that WROTE them — here the post's own `agi-post@<p>` unit — so each
  post pays for its own trees inside its MemoryHigh (honest per-post accounting, no ram-exec hop needed); the RAM disk's total
  stays under GUARD_RAM_BUDGET; the hold line refuses a pull at `wt_hold_pct`. Size per tree = node + payload, not the repo.
- **Proven** (measured on the shared clone): `agi-wt pull build:bin-rotate` -> a tree named by the mint with exactly 2 files
  (`.agi/nodes/build/bin-rotate.md`, `extensions/agi/bin/rotate.py`, 1,204 KiB — the payload's own size); an edit + `agi-wt drop`
  -> one commit on the post head touching the payload, the tree dir gone, `git worktree list` back to 1 line.
  Live proof on <c>: `agi-wt pull <mint>`; `findmnt -no FSTYPE -T $AGI_WT` = tmpfs; `find $AGI_WT/<mint> -type f -not -path '*/.git*' | wc -l` = 2;
  edit, release the claim, end the turn: `test ! -e $AGI_WT/<mint>` and `git log -1 --stat` names node + payload; `df` of the RAM disk returns to its before value.
- Limits, said plainly: a node with no `payload_ref` gets a node-only tree (extra files via a `wt_paths` frontmatter cell, ~30 B);
  `drop` merges into the post's checkout, so a conflicting edit made there in parallel stops the drop (set -e) and leaves the tree
  in place for the next turn — never a lost edit.

## Where they plug in (config:engine pieces touched)
agi-project (+~95 B: AGI_WT / AGI_WT_HOLD / link cells into h.conf, one tmpfiles line per row) · settings.json Stop + agi.ts
`turn_end` (+~150 B: agi-link, per-tree commit, released-claim drop) · agi-flush (+~40 B: drop all) · agi-post@.service
ExecStartPre tool list (+~16 B: `agi-link agi-wt`) · two new `### agi-link` / `### agi-wt` file sections (1,064 B).
Total ≈ 1.4 KB onto a body already over its 12,288 B budget in v3 (12,819 B) -> the budget cell needs the Prime's call.
