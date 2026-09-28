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
thought_session: belam-S2-L5-XIV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 14 late card: PASS 12 + PASS B1 closed, DE key row fixed, root fs full. Landed history is on the board + commit log (owner 06:4xZ 09-28); §2 keeps only one-liners.
<!-- THOUGHT:END -->

## §0 State (17:2xZ 09-28)
| | |
|---|---|
| post | belam-S2-L5-XIV gen 14 · woke 03:5xZ 09-28 · Opus 5.5 · owner asleep from 06:5xZ (delegated authority) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · stream DOWN (HELD) |
| DISK | **`/` 100% (447 MiB free 17:2xZ)** -- /tmp holds 9,669 entries, 5,584 > 24 h (DE's round trees; [red] to DE 17:2xZ) · `/data` 110 GB free · `/mnt/agi-flash` 112 GB free · sda ~35 ms/op (§6) |
| merge | **PASS B1 CLOSED 17:1xZ**: season2/main 1bb6aa5a9 · local-maxxing/main -> ed34f4953 · next BASE = ed34f49532 · residues goal:g1.29 (PASS 12: goal:g1.28) |
| crons | CHECK **372dc32f** "13 */4 * * *" (session-only: re-arm at wake; fires can be late or dropped -- run by hand if > 30 min late) |
| spend | credits 0.606 USD; pi-free 0 USD; a pass with credits < 4 USD is SAMPLED (step 1 rule; build.py SAMPLE + MUST env) |
| models | claude-code kid + parent = claude-opus-5-5, max_live 4 · ladder roles[5] director tier-0 = pi-free (a577c160a) · pi-free model stays stealth/space-bunny-alpha (owner 15:5xZ: "let's hammer it") |

## §1 Plan
```
done   PASS 12 + PASS B1 · clean prune (144 removed) · DE key row re-keyed (e42433aa1) · skills index += agi-corrective (ee82066ec) · board-row interim (abf58770f)
next   CHECK 20:13Z: N = rev-list ed34f49532..local-maxxing/season2/main; landed > 0 -> ONE [owner] 5 h notice to TM -> PASS B2 (tag pb2chunk, /tmp/belam-passB2 from /tmp/belam-passB1, BASE ed34f49532)
owed   FACTS WINDOW on TM's ping (§🔴 F) · TM (a) counting rule -> skills/agi-merge-pass 4 (mur-eg-11; ask TM for the text) · town note grant lines when DE's verb-scoped grant lands (§🔴 G)
HELD   OWNER 21:1xZ 09-27: stream · encryption-town config · sanctuary-master activation -- until messaging is done
```

## §2 Landed (gen 14): b065c922c re-link · 44925a6b6 + 288513229 opus 5.5 · 968d19ca1 DH.499 note · 321a99b29 g7.32.6 · 39b942824 + abf58770f board row · 3e356eb7f g1.28 · 774e0b912 PASS 12 · b1aba8033 prune · a577c160a ladder · 1bb6aa5a9 PASS B1 · 89dd7038b g1.29 · e42433aa1 DE key · ee82066ec skills index

## 🔴 Where it stops
17:2xZ 09-28 belam-S2-L5-XIV: PASS B1 closed; next is the 20:13Z CHECK; / is full (DE sweeping)
```
F. FACTS WINDOW (TM 10:4xZ): when TM pings with DE's EG.5 facts-chain tip, in ONE window: F13 line -> 'Spend by hand, from any worktree:' · cell templates.director.startup.facts_pointer_target_bytes = 2000 · RE-MEASURE the 2009 B region (EG.05 parent: never re-derived) · config:posts:102 + goal:g4.18.2:34 drop the rotate.py DEFAULT_CC_ROLES ultracode residue ONLY once EG.5 removes it from rotate.py:120.
G. TOWN NOTE GRANT (TM option a, 08:4xZ): DE builds a verb-scoped actor_rows note grant inert (goal:g7.33 round); at landing add ONE [town] schema grant line per post (DE, TM, DT) and drop the interim clause from agi-dispatch 5 "progress -> board".
D. DISK: if / < 200 MiB, stop launching anything; regenerable scratch only (skill agi-memory-guard 4); never du /tmp (9 min timeout); never delete another post's tree -- list it for its owner.
R. RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window. NEVER a bare `systemctl --user import-environment`.
5. RAM + per-role worktree roots (owner 06:2xZ, on DH.499): kids tmpfs · DE + parents /data · belam + TM /mnt/agi-flash · mount check before any write · tmpfs GO = TMM.313 (EG.9 sweep chain merged + 24 h no memory crit).
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
| 43 | a send lands `pending=0` (no nudge) when others dm the same post; `send.py read` shows EMPTY while blocks sit in `.agi/sessions/inbox/belam.md` | read the inbox FILE by ts at every CHECK; for a send that matters, watch the addressee's file for `# read up to here` |
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3 |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm / never finishes | `git worktree list`; `find /tmp -maxdepth 1` |
| 46 | `pkill -f <pat>` / `pgrep -f` inside a Bash call kills or matches your OWN shell (exit 144) | match exact argv in python (`/proc/<p>/cmdline`) |
| 47 | a seat key row can be committed with a pubkey whose seed was never written | prove by sign+verify with the held seed before any re-key; never keygen over an existing key |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `df -B1M /` · `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| ROOT FS FULL: / 100% (447 MiB) at 17:2xZ; DE hit 1 MiB at 13:0xZ and tools blocked | move /tmp scratch off / (a tmpfiles.d age rule for /tmp, or TMPDIR=/data/... for every post); `sudo du -xh --max-depth=1 /` to find the rest. MEASURED 17:3xZ: model WEIGHTS are on /data (/data/ml/models, bind-mounted), NOT on /. On /: docker images 12.8 GB (llama.cpp:full-cuda 10.3 GB used by NO container; server-cuda 7.0 GB used) + 85 unattached volumes 3.4 GB (check for postgres data first) + home 8.2 GB. Owner idea 17:3xZ: docker data-root -> /data or /mnt/agi-flash (sequential image reads; flash = own io queue; needs sudo + RequiresMountsFor if flash) |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op, io PSI 68-90 | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` for usb/reset · port/cable/heat |
| memory crits (PSI full peaks 51.2% 04:44Z, 47.2% 06:41Z 09-28; watchdog line 40% for 5 min) | the 4 idle predecessor belam sessions (L5-X..XIII) still hold RAM: reap on the owner's word; or GUARD_DOCKER_BUDGET 2048M |
| seat rows in config:posts still claude-opus-5 (adv-*, masters) | move on the owner's word |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
