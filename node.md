---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-XV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 15: the owner-GO move off / (M) ran steps 1-6 except ~/.pi (a pi parent was live). Deviations, each for a property of THIS box: (a) the card said "crons reopen per run" -- the reaper + alarms services hold the crons log via systemd `append:`, so a cross-fs move alone would strand their writes in an unlinked inode; copy + rename + symlink + restart both instead. (b) the card said TMPDIR=/data/tmp/<post> -- a systemd --user env var is ONE value for every service, so a per-post path cannot be expressed there; one sticky /data/tmp (1777) keeps /tmp semantics, per-post subdirs need the spawn to set them (engine). (c) ~/.cache moved per subdir (uv, pip = 5.3 GB of 5.34), not whole: xfwm4 + xfce4-notifyd hold sqlite/GL files there.
<!-- THOUGHT:END -->

## §0 State (22:3xZ 09-28)
| | |
|---|---|
| post | belam-S2-L5-XV gen 15 · woke 22:1xZ 09-28 · Opus 5.5 · owner asleep (delegated authority) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root **`/mnt/agi-flash/worktrees/prime-root`** (symlink at `.agi/worktrees/prime-root`) · stream DOWN (HELD) |
| DISK | `/` 11.3 GB free 22:3xZ (was 6.2) · `/data` 54 GB free (card XIV said 110 at 20:4xZ -- unexplained, not falling now) · flash 114 GB · sda ~3 MiB/s writes to / |
| moved | ~/logs -> /data/home-belam/logs · ~/.cache/{uv,pip} -> /data/home-belam/cache · TMPDIR=/data/tmp (new spawns) · 41 closed ~/.claude/projects dirs -> /data/home-belam/claude-projects |
| merge | **PASS B2 HELD 03:59Z 09-29** (state `held`, pass_started_at -> null so the next CHECK case (d) re-runs it from step 2): BASE ed34f49532 · TIP pinned 0628fb4afc (trunk sync of origin 156797702e, clean) · 12 rounds (5 hyp SAMPLED + 7 engine-delta) in /tmp/belam-passB2 · RED checks clean (0 D, 0 secret hits / 23,079 added lines, 0 broken) · MUST p2: test_boxkit_probe 28 passed |
| crons | CHECK da6f2ed6 "13 */4 * * *" · PASS B2 one-shot fca674bb 01:43Z 09-29 (both session-only: RE-ARM at wake) |
| spend | credits 0.606 USD -> PASS B2 is SAMPLED (build.py SAMPLE + MUST env) on --harness pi-free |

## §1 Plan
```
done   M. move off / steps 1,2,4,5,6 + 3 for uv/pip (22:1x-22:3xZ) · notice to DE + TM (both read) · board note
now    PASS B2 HELD (🔴 P) -- next CHECK re-runs it; owner [owner] 22:26Z: workflows retire over time (goal:g5.33) -- agi-merge-up-review is belam's call: kept until a dispatched replacement runs green
owed   M3b ~/.pi -> /data/home-belam/pi when NO pi runs (check /proc comm) · M4b live seats' ~/.claude/projects dirs after they rotate
owed   FACTS WINDOW on TM's ping (🔴 F) · TM (a) counting rule -> skills/agi-merge-pass 4 · town note grant lines (🔴 G)
HELD   OWNER 21:1xZ 09-27: stream · encryption-town config · sanctuary-master activation -- until messaging is done
```

## §2 Landed (gen 15): 6e31f798a card re-link · 8f891b8cd path move + board note · 0628fb4af PASS B2 trunk sync · 599cf3b07 config:rotations stale agi-corrective clause (DE flag)

## 🔴 Where it stops
04:0xZ 09-29 belam-S2-L5-XV: PASS B2 HELD -- free lane dead, 0/12 rounds reviewed, nothing merged; the next CHECK re-runs it
```
P. PASS B2 HELD: 6 chunks (01:47-01:52Z) + 6 paced re-retries (02:13-03:59Z) all died on 'Provider returned an empty response'; a 1-file diag round
   (engine-delta-7) hung 25 min with no reply -> NOT prompt size. DE runs 4 merge-up-review workflows on the same pi-free lane. The model is still listed ($0).
   Next CHECK (case d): re-fetch; if origin/season2/main moved, trunk sync (/tmp/belam-trunk-sync/sync.sh, target = OS); re-pin TIP; rebuild with build.py
   (SAMPLE=5, PER=2) into /tmp/belam-passB2 (clear chunk*/rr* first), launch. Die on empty in < 1 min again -> hold again, one line to the owner.
M3b. ~/.pi (935 MB, pi agent state): ONLY while no process with comm `pi` runs. cp -a to /data/home-belam/pi, mv ~/.pi ~/.pi.old-on-root,
     ln -s, a `pi --version` smoke, then rm the old. PI_BIN stays ~/.npm-global/bin/pi (not moved).
M4b. live seats' project dirs (-data-work-agi, post-director-engine, post-director-thought, -data-work): after each seat rotates; `ln -s --` (names start with '-').
T.   TMPDIR follow-ups: crontab jobs still use /tmp (crons.py owns the crontab -- a hand edit is overwritten in 5 min); per-post /data/tmp/<post> = engine (spawn env), not systemd.
F. FACTS WINDOW -- PREP DONE: branch belam/facts-window @ a1ccc2dee (worktree .agi/worktrees/belam-facts, still on /data). When TM pings with the chain tip, in ONE window land a1ccc2dee with it, then: F13 line -> 'Spend by hand, from any worktree:' · cell templates.director.startup.facts_pointer_target_bytes = 2000 · RE-MEASURE the 2009 B region · config:posts:102 + goal:g4.18.2:34 drop the DEFAULT_CC_ROLES ultracode residue ONLY once EG.5 removes it from rotate.py:120.
G. TOWN NOTE GRANT (TM option a): DE builds a verb-scoped actor_rows note grant (goal:g7.33 round); at landing add ONE [town] schema grant line per post (DE, TM, DT) and drop the interim clause from agi-dispatch 5.
D. DISK: if / < 200 MiB, stop launching anything; regenerable scratch only (skill agi-memory-guard 4); never du /tmp; never delete another post's tree.
R. RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window. NEVER a bare `systemctl --user import-environment`.
5. RAM + per-role roots (owner 06:2xZ, DH.499): kids tmpfs · DE + parents /data · belam + TM /mnt/agi-flash (belam: prime-root DONE) · tmpfs GO = TMM.313.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push is thought-master's alone | belam pushes only `season2/main` + `local-maxxing/main` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 40 | F13's home-path .env does not exist here | the MAIN .env is `/data/work/agi/.env` |
| 43 | `send.py read` shows EMPTY while blocks sit in `.agi/sessions/inbox/belam.md` | read the inbox FILE by ts at every CHECK |
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3 |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm | `git worktree list`; `find /tmp -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 47 | a seat key row can carry a pubkey whose seed was never written | prove by sign+verify before any re-key |
| 48 | `~/.claude/projects/*` names start with '-': `ln`/`du` read them as options (gen 15 lost 41 links for a minute) | always `--` or a `./` prefix |
| 49 | a systemd `append:` log holder keeps its fd across a move | restart the unit after the symlink swap |

## §5 Verification: `links.py links` 0 broken (22:3xZ) · `snapshot-goals.py --render --check` · `df -B1M / /data` · `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-` (22:24Z WARN landed in the new path)

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| MERGE LANE: pi-free (stealth/space-bunny-alpha) empty since ~20:0xZ 09-28; PASS B2 held; credits 0.606 USD rule out a paid pass | (a) wait -- CHECK re-runs every 4 h (recommended while the owner sleeps) · (b) a credit top-up -> paid sampled pass · (c) the owner names another :free model for the pi-free lane |
| docker data-root still on / (owner: -> /data or flash when models are redownloaded) | a stop-the-daemon window; owner's word |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` for usb/reset |
| memory crits (PSI full peaks 51.2% 04:44Z 09-28) | the idle predecessor belam sessions hold RAM: reap on the owner's word; or GUARD_DOCKER_BUDGET 2048M |
| seat rows in config:posts still claude-opus-5 (adv-*, masters) | move on the owner's word |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
