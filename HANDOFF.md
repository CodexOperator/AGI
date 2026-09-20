# SESSION HANDOFF — 2026-09-20: `belam-S2-L6-I` gen 3 LIVE on **box local-town** (seated 04:2xZ 09-20, Belam, prime, **Opus 5 (1M)**, remote-control `agi-season2`, no tmux window; predecessor gen 2 `belam-S2-L5-II` was on core-town) — **Texas two-step with NAMED posts: Prime + thought-master (POINT, Opus max) + director-thought (HELPER, Sonnet max)**, owner order 04:0xZ verbatim: *"assume the role of prime director and stand up your own post, then stand up thought master and director-thought as well. We are doing the Texas two-step but with specific posts activated not just random directors."* 🔴 **Stamp every line from `date -u`.** 🔴 **AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER THE MESSAGE — `config:posts` at HEAD.** 🔴 **THE MAIN TIP MOVES BETWEEN TWO OF YOUR OWN COMMANDS (thought-master shares MAIN) — measure, never infer.** 🔴 **READ THIS FILE IN RANGES (`sed -n 'A,Bp'`), NEVER WHOLE.**

**Owner's instructions:** carried in the graph (`doc:l4-owner-decisions`, `doc:l5-owner-decisions`, `goal:g14`, `goal:g17.1`), never here. Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). Prior handoffs: `grid.py payload build:HANDOFF.md --version N`.

## §0 State block

| | value |
|---|---|
| box | **local-town** (`AGI_BOX` in `/data/work/agi/.env`; alias only). GPU 8 GiB, 16 GiB RAM, 243 GB free. MAIN = `/data/work/agi`. tmux `agi-rc`. Logs `~/logs/agi-crons-agi-3fbc6951.log`. |
| branch | **`local-maxxing/season2/main`** in MAIN = the town trunk. core/season2/main **@cc4c087cd merged in at 701ac93bc** (04:1xZ). Posts: director-thought on `local-maxxing/season2/posts/director-thought/main` in `.agi/worktrees/post-director-thought` (from refs/agi/posts/director-thought @43b4810f1 — TM.74 round NOT yet in the trunk). thought-master runs IN MAIN (row worktree '' here: a second checkout of the trunk cannot exist). |
| push | 🟢 **UP since 05:2xZ** — `gh auth login` (CodexOperator) + `gh auth setup-git`; trunk pushed 87ff547ec..07b336503. Was DOWN on this box — no GitHub credential: every push (cron + hand) fails `could not read Username for 'https://github.com'`, since the clone (cron log). MAIN is **ahead 46+** of origin. Fix = owner: `gh auth login` or a credential helper for `https://github.com/CodexOperator/agi.git` on this box. Commits are safe locally; nothing is lost, nothing is published. |
| nodes | links **3721 resolved / 0 broken** (18 retired payloads); GOALS **186 goals round-trip byte-identical** (re-rendered after the core sync: g17.14, g17.16-19 arrived unrendered). Node count: measure with `driver.sh --smoke --max-iters 1` before any merge-up; not measured this session. |
| tests | **5804 passed / 18 failed / 26 skipped** at 701ac93bc (575 s). All 18 are box-environment, not tree defects: 10× test_season TestMergeUp + test_cli (no **global** git identity → "Committer identity unknown" in tmp repos); 4× graphweb (no `node` binary); 2× ws_raw --help; 1× provisioning unavailable (no provisioning key issued here). pytest installed `--user` this session (QUICKSTART 2b). |
| crons | 🟢 applied 04:4xZ, `status: up to date` (11 lines): branch_push :07, mail_poll */5 (+ `migrate --receive`), wake */2, grid_sync + town mirrors (all pushes fail until creds land). |
| posts live | **belam** gen 3 pid 217736 (this session, `710907bf-…`), key re-minted (`.agi/sessions/seats/belam.key`, pubkey 016186c6…, key_history 19). **thought-master** gen 8 @2 pid 415733, session `90eec9d0-…`, seated 04:41:19Z — opened with the prayer, read the [seating] dm, working. **director-thought** gen 12 @3 pid 416688/416745, session `ec9e18a6-…`, seated 04:43:41Z — first reply orienting (no prayer; noted). Both rows carry `box: local-town` (the banked cell (b), now written on the owner's word). Everything else in config:posts is core-town's and foreign here. |
| spend | Prime + point on Opus max, helper on Sonnet max — subscription. pi parents: `OPENROUTER_API_KEY` present in .env; provisioning key present but `provisioning.py status` = unavailable (verify before a `--cap` dispatch). pi-local endpoint 127.0.0.1:18080 not probed this session. |
| meter | all three pins written by the Prime (`.agi/sessions/<post>.meter`, seat_status shows `meter`): thought-master 0.13, director-thought 0.13 at 04:5xZ. belam pin `.agi/sessions/belam.meter` → this transcript; **0.15 at 04:48Z**; rotate at 0.47 (`rotate.py meter --post belam --check`). |

## §1 Plan (this session)

1. ✅ Sync trunk with core (701ac93bc) + GOALS re-render (its own commit).
2. ✅ Stand up the Prime post: box cell + identity cells + gen 3 (580d735f7), meter pin, key re-mint (2cf1044cb).
3. ✅ Stand up thought-master (point): box cell, worktree '' (67affed24), [seating] dm (c22f32fe8), `rotate.py spawn --post thought-master --tier director --prompt-file .agi/sessions/quorum/thought-master.md` → @2.
4. ✅ Stand up director-thought (helper): worktree on its season2 post branch, same dm, same spawn shape → @3 (row ce1734476).
5. ✅ Crons applied. ✅ This card.
6. ✅ Meter pins for both seats. ⏳ NEXT: the point's first numbers line / [decision] on the belam--thought-master dm; the helper's reply to the point.

## §2 What landed (one line each)
- 701ac93bc merge core @cc4c087cd · GOALS.md render · 580d735f7 rows (box ×3, belam gen 3) · 67affed24 thought-master worktree '' · 2cf1044cb belam key · c22f32fe8 seating dms · 8ac7c6b98 thought-master seating row · ce1734476 director-thought seating row · worktree `.agi/worktrees/post-director-thought` created.

## §3 🔴 Where it stops
```
05:1xZ 09-20 LIVE (gen 3, f≈0.22): three posts seated; belam row is quiet (settings 'ultracode quiet'); thought-master told (owner relay) it is in independent research mode and reports nothing to the Prime. SKILL.md gained 'Entering prime state' (32dffa39f). NEXT = step 6 of that section, rotate self INTO the prime slot properly:
  touch .agi/sessions/quorum/belam.md && git commit -q -m 'belam card' -- .agi/sessions/quorum/belam.md   # clears 'card older than last commit'
  AGI_SEAT=belam AGI_POST=belam python3 extensions/agi/bin/rotate.py rotate --force --stops-file .agi/sessions/belam.stops
Push credential landed 05:2xZ (gh, CodexOperator); trunk in sync; rotating NOW — the successor (belam gen 4, tmux agi-rc) is the Prime; this bg session ends at its `continue`.
```

## §4 Traps hit this session
1. First Claude Code launch in a folder on a fresh box throws THREE TUI dialogs (folder trust → bypass-permissions accept → renderer offer) before the brief runs; the seat sits on them silently. Answer with `tmux send-keys -t agi-rc:<post> Down Enter` (trust, accept) and `Escape` for the renderer offer — Escape did NOT interrupt the running turn. Second launch (worktree under the trusted folder) showed none.
2. STARTUP's `[inbox] send.py read <seat>` runs with identity 'unknown' (no AGI_AGENT_ID in first_turn) — thought-master re-read by hand. Template fix candidate: `--from {seat}`.
3. `send.py send` from belam reports `[undelivered-yet]` when the target window is gone; the dm IS written and the seat reads it on its first turn.
4. The seats' cards (`.agi/sessions/quorum/*.md`, copied from core 04:00Z) carry core-town paths (`/home/ubuntu/work/agi`, `local-maxxing/season1/*`) — corrected in the [seating] dm, not in the cards.
5. The prime's own first reply this session did not open with the prayer (the skill was loaded after the reply began). Close with it.

## §5 Known-good verification sequence
```bash
git -C /data/work/agi branch --show-current                      # local-maxxing/season2/main
python3 extensions/agi/bin/links.py links | tail -1               # 0 broken
python3 extensions/agi/bin/snapshot-goals.py --render --check     # byte-identical
python3 extensions/agi/bin/seat_status.py --list | grep -E '^(belam|thought-master|director-thought)'
python3 extensions/agi/bin/crons.py show | grep ^status           # up to date
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q   # 5804 pass / 18 box-env fails at 701ac93bc
```

## §6 BANKED (owner-only)
- **GitHub credential on local-town** — without it nothing this box does reaches origin (branch, refs/agi/posts mirrors, refs/grid). Recommend `gh auth login` as user belam, or a PAT via `git credential-store` scoped to CodexOperator/agi.
- **The belam row now says `box: local-town`** — on core-town the Prime row is foreign to that box's guard until a core Prime re-seats it (or the owner says the Prime lives here now). Recommendation: leave it; one Prime, on the box the owner is on.
- **Global git identity + `node` on this box** would turn 15 of the 18 red tests green; not set (box-level config is the owner's).
- **Provisioning key**: `provisioning.py status` reports unavailable here — pi parents dispatch with the plain OPENROUTER_API_KEY only until the owner mints this box its own workspace key (Remote NOW step 1: spend isolation per box).
