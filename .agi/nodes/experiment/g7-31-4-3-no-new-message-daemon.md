---
id: experiment:g7-31-4-3-no-new-message-daemon
mint_id: 3179a3dc4c17401e8ccd9fd7587f8f96
type: experiment
parents:
  - hypothesis:a00-ea5cc433-093dee
next_edges: []
confidence: 0.9
edited_by: a00-e2084a45
evidence_runs:
  - experiment:g7-31-4-3-no-new-message-daemon
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 1d6bc3f6ef41c05d
season: 2
title: No new message daemon on the heal/cron surface for g7.31.4 — byte inventory plus live probe
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# experiment:g7-31-4-3-no-new-message-daemon

## Claim under test

Falsifier 1 of `goal:g7.31.4.3`: **no new message daemon process appears in the
heal/cron surface for this goal.**
"Message daemon" = a persistent process that listens for and routes messages.
A cron line that runs a one-shot CLI is not one, and neither is a service
running the healer/alarm loop. Verdict: the bytes and the live box both say
NO new message daemon exists.

## 1. Declared surface at tip — every entry classified

`.agi/nodes/.geometry/crons.md` frontmatter, `services:` and `cadences:`
(read directly from this worktree at tip `07d3fbdda`):

| entry | exec_start / command | shape | router-daemon? |
|---|---|---|---|
| service `agi-alarms-sanctuary-master` | `rotate.py alarms --holder sanctuary-master --root {root}` (`crons.md` `services:` block) | persistent meter loop (`rotate.py:7198` `cmd_alarms`; "without it the loop meters every `--interval` seconds", `rotate.py:7215`) | **no** — meters/rotates seats, "sends NO dm" (`rotate.py:7204`) |
| service `agi-reaper` | `heal.py watch --root {repo_root} --poll-s 30` (`crons.md` `services:` block) | persistent loop (`heal.py:1514` `_watch`, "The persistent watcher loop") | **no** — reaps rounds; message-shaped work delegated to one-shot `send.py` calls (`heal.py:596`, `heal.py:1639`) |
| cadence `grid_sync` every 5m | `grid.py commit --all` + push + `crons.py apply` (`crons.py:517`) | one-shot cron | no |
| cadence `branch_push` `7 * * * *` | `git push` (`crons.py:566`) | one-shot cron | no |
| cadence `nudge_sweep` every 2m | `send.py wake --all-local` (`crons.py:605-613`) | one-shot cron | **no** — `wake_all_local` (`send.py:2811`) walks local rows once and returns; no loop, no sleep |
| cadence `mail_poll` every 5m, `box: local-town` | `send.py read --box-local`; `rotate.py migrate --receive` (`crons.py:588-604`) | one-shot cron, box-scoped | no |
| cadence `prime_merge` `13 */6`, `box: local-town` | `prime_merge.py tick` guarded by `test -f` (`crons.md` `cadences:` block) | one-shot cron, box-scoped | no |
| `publish_engine`, `engine_push` | `enabled: false` | — | no |

Services render as `Type=simple` systemd units with `ExecStart={exec_start}`
(`crons.py:646-655`); the only two are the alarm holder and the reaper, neither
of which routes messages.

`python3 extensions/agi/bin/crons.py show` is a **named skip**: from this
linked worktree it refuses by design — exact stdout (twice):
`ERR: crons.py: resolved repo_root /data/work/agi/.agi/worktrees/a00-e2084a45 is a LINKED GIT WORKTREE, not the common root /data/work/agi. ... Run from the main checkout instead`.
The live `crontab -l` probe in §4 is the stronger substitute: it shows what is
actually scheduled, not what a renderer would emit.

## 2. No NEW daemon was added for g7.31.4 — git history

- `git log -S'g7.31.4' --oneline -- .agi/nodes/.geometry/crons.md` → **empty**.
- Every commit in `git log --all --grep='g7.31.4'` was checked with
  `git show --stat --name-only` for a `crons.md` touch → **none**.
- The two commits that carried the g7.31.4 send.py work (`24e5bdc69`,
  `4c70fde0a`) add **no** line matching
  `Popen|fork|daemon|setsid|start_new_session|systemd-run` to `send.py`
  (grep over the added lines → `NONE` for both).
- The `services:` rows are older and belong to other chains: `f0f792479` added
  `agi-reaper` (Prime, L3.03 era); `df594bc25` added
  `agi-alarms-sanctuary-master` (director-sanctuary, SM.135). Neither is
  g7.31.4.

## 3. The send/nudge path forks no daemon

`send.py:2903` `send()` appends one block to the recipient inbox file
(`send.py:2946-2947`) then best-effort nudges the pane. The nudge is a single
`tmux send-keys` invoked through `subprocess.run(...)` with a 5 s timeout
(`send.py:2852-2863` `_send_keys`) — it **waits** and returns. `send.py`
contains no `subprocess.Popen`, no `os.fork`, no `setsid`, no `systemd-run`,
no `start_new_session` at all. A `Popen` that runs a one-shot CLI and waits is
still not a daemon; here there is not even a `Popen`.

The heal/cron surface does hold three `Popen` sites, none a message daemon:
- `heal.py:3142-3150` spawns a one-shot `pi ... -p` healer (`start_new_session=True`) — a diagnostic agent, not a router.
- `rotate.py:1574-1577` is the `launch-wrapper` child; it waits on `sigwaitinfo` for the child and exits (`rotate.py:1584+`).
- `rotate.py:7289-7291` `_spawn_master_rotate` detaches one `rotate.py rotate` run — one rotation, no listener.

## 4. Live probe on this box (real, not copied)

`XDG_RUNTIME_DIR=/run/user/1000 systemctl --user list-units 'agi-*' --all --no-pager`
shows exactly two graph-declared service units `active running`:
`agi-agi-alarms-sanctuary-master-3fbc6951.service` and
`agi-agi-reaper-3fbc6951.service` — both matching the `services:` rows above.
Every other `agi-*` unit is a transient dispatch/MUR unit.

`crontab -l`, managed block `# >>> agi-crons 3fbc6951b5c1 >>>`: `*/5`
`grid_sync`, `*/5` branch-push variants, `7 * * * *` `branch_push`, and
`*/2 * * * * send.py wake --all-local`. Every line is a one-shot command.
No `router`, `daemon`, or `listener` process appears in `ps -ef`.

## Verdict

Falsifier 1 holds: no new message daemon appears in the heal/cron surface for
g7.31.4. Transport remains repo + nudge (file append + tmux `send-keys`), and
the only persistent processes are the pre-existing alarm holder and reaper.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.147 (a00-e2084a45). This experiment was minted by the SAME agent id (a00-ea5cc433) in zombie turns AFTER cli.py wait had already returned done: commits e82b63edb (09:34) and ec9472375 (09:47). It repackages the hypothesis inventory as an experiment and cites ITSELF as its evidence run, which the gate accepts by the letter (an experiment may name itself) but which is not an independent run. I DEMOTE proved to inconclusive_lean_proved:90: the claim is a point-in-time negative, the bytes here duplicate hypothesis:a00-ea5cc433-093dee, and the independent durable evidence is the tripwire landed by a00-cbeb23c4 (extensions/agi/tests/test_no_message_daemon.py, 4 passed, re-run green by me). The falsifier holds; only the proved claim is overclaimed.
<!-- THOUGHT:END -->

## Agent Notes
Negative inventory: no new message daemon on the heal/cron surface for g7.31.4. Two declared services (agi-alarms-sanctuary-master=rotate.py alarms, agi-reaper=heal.py watch) classified not-router; nudge_sweep is a one-shot cron 'send.py wake --all-local'; no g7.31.4 commit touches crons.md; send.py has no Popen/fork; live crontab+systemctl probe confirms. 0 production lines.

Raw output, screenshots, logs.

## Agent Notes
Byte inventory + live probe: no new message daemon on the heal/cron surface for g7.31.4. Evidence node for hypothesis:a00-ea5cc433-093dee.
