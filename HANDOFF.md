# SESSION HANDOFF — 2026-09-20: `belam-S2-L5-I` gen 1 LIVE on **box local-town** (seated 05:19Z by rotate-self `--force` into the prime slot: tmux `agi-rc` window @4, pid 430845, session `da7cd23f-…`; Belam, prime, **Opus 5 (1M)**; remote-control watched from claude.ai) — **Modified Texas two-step (owner 05:4xZ, verbatim on goal:g14): Prime + thought-master + director-thought, who free-floats UNDER thought-master. No point, no helper the Prime tasks — the Prime reviews merge-ups into the trunk and keeps the box unblocked; it never queues work into the town.** 🔴 **Stamp every line from `date -u`.** 🔴 **AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER THE MESSAGE — `config:posts` at HEAD.** 🔴 **THE MAIN TIP MOVES BETWEEN TWO OF YOUR OWN COMMANDS (thought-master shares MAIN) — measure, never infer.** 🔴 **READ THIS FILE IN RANGES (`sed -n 'A,Bp'`), NEVER WHOLE.**

**Owner's instructions:** carried in the graph (`doc:l4-owner-decisions`, `doc:l5-owner-decisions`, `goal:g14`, `goal:g17.1`), never here. Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). Prior handoffs: `grid.py payload build:HANDOFF.md --version N`.

## §0 State block

| | value |
|---|---|
| box | **local-town** (`AGI_BOX` in `/data/work/agi/.env`). MAIN = `/data/work/agi`, user `belam`, tmux `agi-rc`, logs `~/logs/agi-crons-agi-3fbc6951.log`. GPU 8 GiB, 16 cores. `sudo -n` works (unused). |
| branch | **`local-maxxing/season2/main`** = the town trunk, **in sync with origin @e3549ff29 (05:3xZ)**. core/season2/main merged @cc4c087cd (701ac93bc). **core-town is DOWN** (thought-master 05:15Z: unreachable on overlay + public 22). director-thought on `local-maxxing/season2/posts/director-thought/main` in `.agi/worktrees/post-director-thought`; thought-master runs IN MAIN. |
| push | 🟢 UP (`gh auth login` CodexOperator + `gh auth setup-git`, 05:2xZ). Origin answers "repository moved → https://github.com/CodexOperator/AGI.git"; the redirect works — `git remote set-url` only if a push starts failing. |
| nodes | at wake (STARTUP verify): links **0 broken**, GOALS **186 byte-identical**, smoke **active 3520 / deprecated 223 / total 3743** — the session baseline; active never drops. |
| tests | 5804 / 18 / 26 at 701ac93bc; the 18 are box-env (10 no global git identity, 4 no `node` — node is present since 05:22Z, re-measure; 2 ws_raw; 1 provisioning, now available). `bin-suite-fresh` FAIL = no suite timestamp ever recorded on this box. `node-count` NOT STAMPED: the integration-branch names are `season2/main`/`season/s2`, this trunk is `local-maxxing/season2/main` (config gap, §6). |
| posts live | **belam gen 1** @4 pid 430845 (row 0899a142e; gen 3→1 on the `--force` rotate, §4). **thought-master gen 8** @2 pid 415733 (independent research; reports nothing to the Prime — owner relay). **director-thought gen 12** @3 pid 416745 (free-floats under thought-master). All three rows `box: local-town`; every other row in config:posts is core-town's. |
| spend | `provisioning: available keys_visible=2 engine_minted=1` (Doppler agi/dev key in MAIN `.env` since 05:1xZ, 0600, untracked; ~14 USD left of 192); floor 1.6; `OPENROUTER_API_KEY` empty by design (L4.98). budget 0/25 live. |
| harness | node 24.21.0; **pi 0.67.68 at `/home/belam/.npm-global/bin/pi`** (installed 05:22Z); `PI_BIN` + `PATH` exported in `~/.profile`, `~/.bashrc`, `tmux -g`. `dispatch.py --dry-run` resolves the live path WITH `PI_BIN` (measured), the dead `/home/ubuntu/…` path without. Sessions seated before 05:22Z (all three) prefix `PI_BIN=` inline. **`workflow.py run … --harness pi` launches the dead config path here — a FINDING on goal:g14, thought-master's to take or not.** |
| meter | belam pin `.agi/sessions/belam.meter` → this transcript; **f=0.09 at 05:22Z**; rotate at 0.47 with plain `rotate` (F23). |

## §1 Plan (this session)

1. ✅ Wake with no acts (ack answered by the predecessor); orient.
2. ✅ node+pi measured live; `dispatch.py` resolves with `PI_BIN`; the workflow.py precedence gap found, noted on `goal:g14` (e3549ff29). The 05:3xZ dm framed it as an order to director-thought — **WITHDRAWN 05:4xZ** on the owner's correction (a finding; thought-master decides); note reworded in place, correction dm sent.
3. ⏳ If the town takes that fix, review its merge-up **by bytes** (`workflow.py:1381` env-over-config, `heal.py:3113` default, one test) — the review path is the thing it fixes; verify on the trunk after landing; push.
4. ⏳ Any other `[merge-up]` from the town: report + bytes → accept/demote; verify (links 0 · goals byte-identical · active ≥ 3520 · guard silent); push after every landing.
5. ⏳ Rotate at 0.47: write + stamp the stops slot FIRST, then `AGI_SEAT=belam AGI_POST=belam python3 extensions/agi/bin/rotate.py rotate`.

## §2 What landed (one line each)
- e3549ff29 goal:g14 note (box facts + gap) + GOALS · 351c63074 handoff replaced, card trimmed · 05:4xZ: owner's three lines banked verbatim on goal:g14, note 153 reworded in place, correction dm → thought-master, this doc pass · pushed after each.

## §3 🔴 Where it stops
```
05:4xZ 09-20 LIVE (gen 1, f≈0.11): box blockers cleared (push up, provisioning up, node+pi up). The town runs its own rounds (owner GO 05:32Z in the thought-master pane: 6g on pi with deepseek); the workflow.py precedence gap is a noted finding, NOT queued. Owner 05:4xZ: slow down. Prime NEXT = one `send.py read belam` when nudged (never peek) -> review any [merge-up] by bytes -> verify on the trunk (links 0 · goals byte-identical · active >= 3520 · guard silent) -> push. Nothing else is owed by the Prime now.
```

## §4 Traps hit this session
1. `rotate-self --force` into the prime slot wrote the successor as a SPAWN row at **gen 1** (record `gen_before 3 / gen_after 1`, commit 0899a142e): the gen counter reset and the derived name reads L5 where the predecessor wrote L6. Cosmetic until something joins on gen; not chased at wake.
2. Bash-tool shells do not re-source `~/.bashrc`/`~/.profile` inside a running session (flags `hmtBc`; belam @4 has no `PI_BIN` although the profile has carried it since 05:22Z) — env edits reach NEW sessions only; running posts prefix inline.
3. `workflow.py run … --dry-run` prints "via dispatch.py kids", but the live pi path is `_run_stage_pi` launching `_pi_harness_cfg`'s CONFIG bin directly (`workflow.py:1793`) — the summary is a label, not the mechanism.
4. `send.py send` from belam to a busy pane reports `[undelivered-yet]`: the dm IS written; the sweep re-nudges.

## §5 Known-good verification sequence
```bash
git -C /data/work/agi branch --show-current                      # local-maxxing/season2/main
python3 extensions/agi/bin/links.py links | tail -1               # 0 broken
python3 extensions/agi/bin/snapshot-goals.py --render --check     # byte-identical
python3 extensions/agi/bin/seat_status.py --list | grep -E '^(belam|thought-master|director-thought)'
python3 extensions/agi/bin/crons.py show | grep ^status           # up to date
PI_BIN=$HOME/.npm-global/bin/pi python3 extensions/agi/bin/dispatch.py . 999 --dry-run --harness pi --tier parent --target <hypothesis:id> | grep wrapper   # /home/belam/... = live pi
```

## §6 BANKED (owner-only)
- **Global git identity on this box** (10 of the 18 red tests). Box-level; recommend `git config --global user.name/email` for user belam.
- **`.agi/config.json` carries core-town literals in a tracked, merge-shared file** (`box.root/user` = /home/ubuntu…, `harnesses.pi.bin`, `harnesses.copilot.bin`): SM.124's box cells were meant to be per-box. The fix (`harnesses.*.bin` resolving `{user}`/`$PATH`, and `_pi_harness_cfg` env-over-config) is thought-master's town's to take when it has a slot — not owner-blocking while `PI_BIN` covers dispatch.
- **Integration-branch list** (`season2/main`, `season/s2`) omits this town's trunk, so the node-count stamp and the suite window never land on local-town. Recommend one config cell adding `local-maxxing/season2/main`; the Prime applies it on the owner's word that the trunk is canonical here.
