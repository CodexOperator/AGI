# SESSION HANDOFF — 2026-09-21: `belam-S2-L5-I` gen 1 LIVE on **local-town** (seated 05:19Z 09-20 by rotate-self `--force` into the prime slot; tmux `agi-rc` @4, pid 430845, session `da7cd23f-…`; Opus 5 (1M); remote-control, owner watches from claude.ai). 🔴 Stamp lines from `date -u` · authority = `config:posts` at HEAD, never the message · the MAIN tip moves between two of your own commands (thought-master shares MAIN) — measure, never infer · read this file in ranges. Diagram-maxed (owner 02:0xZ 09-21).

Owner lines: in nodes (`goal:g14` for this box; `doc:l4-owner-decisions`, `doc:l5-owner-decisions`, `goal:g17.1`), never here. Bootstrap: [QUICKSTART.md](QUICKSTART.md). Prior handoffs: `grid.py payload build:HANDOFF.md --version N`.

## §0 State
| | |
|---|---|
| formation | **modified Texas two-step (owner 05:4xZ 09-20): Prime + thought-master + director-thought free-floating UNDER thought-master + director-engine (row exists, unseated; the Prime's assignee for engine follow-ups).** No point, no helper the Prime tasks; the Prime NEVER queues work into the town. |
| box | local-town: MAIN `/data/work/agi`, user `belam`, tmux `agi-rc`, logs `~/logs/agi-crons-agi-3fbc6951.log`; 16 cores, 15 GiB RAM, GPU 8 GiB; `sudo -n` works (unused). core-town DOWN (thought-master 05:15Z 09-20). |
| branches | town trunk **`local-maxxing/season2/main`** (MAIN checkout; thought-master commits here) · root **`season2/main`** = origin only (cb21bf01d), ancestor of the trunk, **452 commits behind it at 01:25Z 09-21** · director-thought on `local-maxxing/season2/posts/director-thought/main` (worktree) · origin/core moved (23 commits the town lacks) — not this routine's. |
| push | 🟢 UP (gh CodexOperator). Origin says "moved → CodexOperator/AGI.git"; redirect works; `set-url` only if a push fails. |
| nodes | wake baseline: links 0 broken · GOALS byte-identical (198 goals) · smoke active 3520 / deprecated 223 / total 3743 — active never drops. |
| tests | 5804 / 18 / 26 at 701ac93bc; the 18 = box-env (10 git identity, 4 node — node now present, re-measure; 2 ws_raw; 1 provisioning, now available). `bin-suite-fresh` FAIL = no suite timestamp ever on this box (L5). |
| spend | provisioning available (Doppler agi/dev key in MAIN `.env`), **12.15 USD left at 01:25Z 09-21**, floor 1.6; `OPENROUTER_API_KEY` empty by design. |
| harness | node 24.21.0 · pi 0.67.68 `/home/belam/.npm-global/bin/pi` · `PI_BIN`+`PATH` in profile + tmux -g (05:22Z 09-20; pre-05:22Z sessions prefix inline) · `workflow.py --harness pi` works here ONLY because the config's `/home/ubuntu/…/pi` path was made to exist (L1). |
| meter | pin `.agi/sessions/belam.meter` → this transcript; rotate at f ≥ 0.47, plain `rotate` (F23), stops slot first. |

## §1 Plan
```
✅ wake (no acts) ─▶ ✅ node+pi measured, gap L1 noted (e3549ff29) ─▶ ✅ owner corrections banked + dm'd (495f0d6b8)
─▶ ✅ MERGE ROUTINE armed (owner 01:2xZ 09-21, verbatim goal:g14)
      session : one-shot 06:39Z 09-21 = FIRST PASS · DAILY activation 08:13Z (dm read · graph scan · delta check → notice → one-shot run +5 h)
                (session-only, 7-day expiry — a successor RE-ARMS both FIRST)
      persisted: cron:crons cadence prime_merge 13 */6 box local-town, applied, INERT until extensions/agi/bin/prime_merge.py lands
      spec+L1–L10: hypothesis:prime-merge-routine-is-one-cron-script (goal:g15) ASSIGNED director-engine (dm 01:5xZ)
─▶ ✅ standing orders relayed: nested sub-goals (director-engine) · diagram-max (all three posts) · Prime brief diagram-maxed (8.8 KB from 14.1 KB)
─▶ ⏳ 06:39Z FIRST PASS: mur over origin/season2/main..trunk (≤6 rounds/chunk, pi, PI_BIN set) ─▶ all-GO: --no-ff merge by SHA into season2/main
      in .agi/worktrees/prime-root ─▶ verify there (links 0 · goals byte-identical · active never drops · no node deletions) ─▶ push ─▶ grid commit --all there
      ─▶ residues → g15 nodes assigned director-engine (one dm) ─▶ note goal:g14 ─▶ THEN one [merge-up] report to thought-master. Any red ─▶ NO merge, one [red].
─▶ ⏳ rotate at 0.47: stops slot + stamp FIRST, then AGI_SEAT=belam AGI_POST=belam python3 extensions/agi/bin/rotate.py rotate
```

## §2 Landed (one line each)
e3549ff29 g14 note · 351c63074/495f0d6b8 handoff + corrections · b870ee0e9 routine + owner line · 072349c7f cadence + spec node · 440da437c/865991992/77d9696b4 owner lines (nested goals · comms route · diagram-max) · brief diagram-maxed · pushed after each.

## §3 🔴 Where it stops
```
02:0xZ 09-21 LIVE (gen 1): routine ARMED (one-shot 06:39Z + daily 08:13Z; persisted cadence inert until prime_merge.py). State .agi/sessions/prime-merge.state.json.
NEXT = the 06:39Z FIRST PASS (§1). Owner mode: quiet push-only · batch-max · diagram-max · report to thought-master only after a completed pass.
A successor re-arms the two session crons FIRST (specs in §1), then waits for the next tick.
```

## §4 Traps (this session)
| # | trap | rule |
|---|---|---|
| 1 | rotate-self `--force` into the prime slot wrote the successor as a SPAWN row at gen 1 (record gen_before 3 / gen_after 1; 0899a142e) | cosmetic until something joins on gen; not chased at wake (L6) |
| 2 | Bash-tool shells never re-source the profile inside a running session (no PI_BIN in belam @4) | env edits reach NEW sessions only; running posts prefix inline (L7) |
| 3 | `workflow.py --dry-run` prints "via dispatch.py kids" but the live pi path is `_run_stage_pi` with the CONFIG bin (`workflow.py:1793`) | the summary is a label, not the mechanism (L1) |
| 4 | cron:crons optional `log:` cell is NOT placeholder-rendered (`{logs}` reached the crontab) | omit `log:`; use the default log (L2) |
| 5 | `write.py replace body 1:N` on a fresh node eats the `<!-- BODY:BEGIN -->` marker | restore it as body line 1 |
| 6 | `send.py send` to a busy pane → `[undelivered-yet]` | the dm IS written; the sweep re-nudges |

## §5 Verification
```bash
git -C /data/work/agi branch --show-current                                  # local-maxxing/season2/main
python3 extensions/agi/bin/links.py links | grep -oE '[0-9]+ broken'          # 0 broken
python3 extensions/agi/bin/snapshot-goals.py --render --check                 # byte-identical
python3 extensions/agi/bin/seat_status.py --list | grep -E '^(belam|thought-master|director-thought|director-engine)'
python3 extensions/agi/bin/crons.py show | grep -E '^status|prime_merge'      # up to date; the inert cadence line
PI_BIN=$HOME/.npm-global/bin/pi python3 extensions/agi/bin/dispatch.py . 999 --dry-run --harness pi --tier parent --target <hypothesis:id> | grep -o 'wrapper [^ ]*'   # /home/belam/…/pi
```

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| global git identity on this box (10 of the 18 red tests) | `git config --global user.name/email` for user belam |
| `.agi/config.json` carries core-town literals (`box.*`, `harnesses.*.bin` = /home/ubuntu…) in a merge-shared file (L3) | director-engine round: `{user}`/`$PATH` resolution or the box overlay; not owner-blocking while `PI_BIN` covers dispatch |
| integration-branch list omits the town trunk (L4): node-count never stamps on local-maxxing/season2/main | one config cell adding `local-maxxing/season2/main`, on the owner's word that the trunk is canonical here |
| persisted cadence is 6-hourly (zero tokens); the owner spoke of a DAILY activation | leave (a cron script costs no tokens); one config cell if daily is wanted |
