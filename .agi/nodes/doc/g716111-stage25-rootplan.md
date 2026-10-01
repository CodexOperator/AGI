---
id: doc:g716111-stage25-rootplan
mint_id: dbd8db841a4148b78535083a1292da06
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 608eb16fea704078
season: 2
title: "g7.16.1.11 stage 2.5: director-general-5 under engine v4 on the live repo -- CCCC mapping, root plan (each act + undo, N4 hard gate), 55 parity proofs"
town: core
---
# doc:g716111-stage25-rootplan

Stage 2.5 of goal:g7.16.1.11 (belam GO 03:48Z; owner: DG5 under the new engine on the LIVE repo, parity matched-or-better incl. guards + the magic pane anchor; council [red] §N.5: agi.slice + N4 HARD GATE). PHASE A by an Opus 5.5 subagent of director-general-3, no root. Unit names spelled agi-post@${P}.service, P=director-general-5. Off-graph inputs: /tmp/agi-stage25/v4/ (engine-v4.md 16,375 B, pieces/, test.txt). PHASE A' (owner 04:40Z: DG5 = Claude Code Sonnet 5.5 + Remote Control; owner 04:49Z: he logs DG5's user in by hand, no credential copy) by a second Opus 5.5 subagent, no root: the PHASE A' DELTA section at the end SUPERSEDES the base where they differ; the v4c engine bytes are on doc:g716111-stage25-engine-v4c; off-graph inputs now /tmp/agi-stage25/v4c/. Not run yet.

## CCCC -- Claude Code hooks mirrored on pi

Owner order (via belam 03:48Z): "add the CC-cross-comparability plugin or extension or whatever to make it mirror CC hooks".
Mechanism: ONE hook wiring, `settings.json` (engine piece, installed as `~/.claude/settings.json`). Claude Code reads it natively;
pi loads `cccc.ts` (`-e ../bin/cccc.ts`), which reads the SAME file and runs each hook command for the mapped pi event with a
CC-shaped JSON payload on stdin (`hook_event_name`, `cwd`, + the event's own fields), honours `matcher` (regex on `tool_name`),
per-hook `timeout` (s, default 60 like CC), and CC's exit-code contract (exit 2 = block, stderr = the reason). So the brief, the
meter and the turn-end commit fire through this one table on both harnesses. pi tool names are mapped to CC's (bash->Bash,
read->Read, edit->Edit, write->Write) so CC matchers work unchanged.

| CC hook | pi event(s) | what fires (engine settings.json) | how its output is used on pi | proved how |
|---|---|---|---|---|
| SessionStart `startup` | `session_start` reason=startup | `agi-brief` (timeout 180): brief walk + rotation record + STARTUP OUTPUT | stdout kept; injected into the system prompt by `before_agent_start` on every agent start (CC: added as context once) | fake-pi harness: before_agent_start -> `SYS\n\nBRIEF-startup`; real pi 0.67.68 in a `script` pane: `~/.brief` written (1,318 B), strace track shows agi-brief exec |
| SessionStart `resume` | `session_start` reason=resume / fork / reload | `agi-brief` (no STARTUP block on resume) | same | harness: reason fork/reload map to `resume` (code path); `new` -> `clear` proven (`BRIEF-clear`) |
| SessionStart `clear` | `session_start` reason=new | `agi-brief` | same | harness: `BRIEF-clear` |
| SessionStart `compact` | `session_compact` | `agi-brief` (no record, no STARTUP) | replaces the injected brief | harness: `BRIEF-compact` |
| UserPromptSubmit | `input` | `agi-meter` (the rotation line) | payload carries `prompt`, `tokens`, `context_window` (pi `getContextUsage()`); stdout -> `{action:"transform"}` appends it to the prompt; exit 2 -> `{action:"handled"}` (prompt blocked) | harness: `hi` -> transform with `tokens=480000/1000000`; `block` -> handled; agi-meter prints the out-line at 480000/1000000 (pi path) and 470015 tokens from a CC transcript (CC path) |
| PreToolUse | `tool_call` | none configured today (none on today's posts either) | exit 2 -> `{block:true, reason:stderr}`; matcher on the CC tool name | harness with a test hook: `rm -rf` -> `{block:true,reason:"blocked rm"}`, `ls` -> allowed, matcher `Bash` skips `Read` |
| PostToolUse | `tool_result` | none configured | run for side effects (CC: feedback only on exit 2; not mirrored) | harness: logged `PostToolUse t=Read` |
| Stop | `turn_end` | `agi-turn`: drop released agi-wt trees, one signed commit, agi-link | output ignored | harness: logged `Stop`; scratch worktree: agi-turn -> signed commit (`%G?` = G) + `~/link` = `build:bin-heal extensions/agi/bin/heal.py`. Note: pi fires turn_end per LLM response+tools, so it commits more often than CC's Stop (once per agent reply) = finer, never coarser. A provider error before the first turn (no key) fires no turn_end (measured: no agi-turn exec in the no-key pty run) |
| SubagentStop | — | — | pi has no built-in subagent; not exposed (named, not faked) | — |
| PreCompact | `session_before_compact` | none configured | run; payload `trigger:"auto"` | harness: logged `PreCompact` |
| SessionEnd | `session_shutdown` | none configured (the flush is the unit's ExecStopPost, harness-independent) | run; payload `reason:"other"` | harness: logged `SessionEnd` |
| (no CC hook) mail | `fs.watchFile` on `$O/.agi/sessions/inbox/$AGI_SEAT.md` | — | the inbox file GROWS -> `pi.sendUserMessage("mail: send.py read <post>", {deliverAs:"followUp"})`: a turn after the current one, never an interrupt; a same-size rewrite (send.py moving its read marker) does not fire; `unwatchFile` first so a /new or reload never doubles it | harness: one append -> exactly 1 followUp message; same-size rewrite -> 0; real pi: the third provider attempt in the pty run is the extension's (`Extension "<runtime>" error: No API key ...`) |

Live-post proofs (need the post running, key in env): see parity-proofs.md rows 7-10, 16, 21, CC1-CC4.

## The extension source (engine piece `cccc.ts`, 1,633 B, byte-exact from `sect cccc.ts`)
~~~ts
import{execSync as x}from"node:child_process";import{readFileSync as R,watchFile as W,unwatchFile as U}from"node:fs"
const E=process.env,H=JSON.parse(R(E.HOME+"/.claude/settings.json","utf8")).hooks,N={bash:"Bash",read:"Read",edit:"Edit",write:"Write"};let b=""
const h=(n,j={})=>{let o="",k=0;for(const g of H[n]||[])if(!g.matcher||RegExp(g.matcher).test(j.tool_name))for(const c of g.hooks)try{o+=x(c.command,{input:JSON.stringify({hook_event_name:n,cwd:process.cwd(),...j}),encoding:"utf8",stdio:"pipe",timeout:(c.timeout||60)*1e3})}catch(e){if(e.status==2)k=2,o+=e.stderr}return{o,k}}
const t=e=>({tool_name:N[e.toolName]||e.toolName,tool_input:e.input}),S=s=>{b=h("SessionStart",{source:s}).o}
export default p=>{const on=(e,f)=>p.on(e,f);on("session_start",e=>{S({new:"clear",fork:"resume",reload:"resume"}[e.reason]||e.reason)
const f=`${E.O}/.agi/sessions/inbox/${E.AGI_SEAT}.md`;U(f);W(f,{interval:5e3},(n,o)=>n.size>o.size&&p.sendUserMessage("mail: send.py read "+E.AGI_SEAT,{deliverAs:"followUp"}))})
on("session_compact",()=>S("compact"));on("before_agent_start",e=>b&&{systemPrompt:e.systemPrompt+"\n\n"+b})
on("input",(e,c)=>{const u=c.getContextUsage()||{},r=h("UserPromptSubmit",{prompt:e.text,tokens:u.tokens,context_window:u.contextWindow});return r.k?{action:"handled"}:r.o&&{action:"transform",text:e.text+"\n\n"+r.o}})
on("tool_call",e=>{const r=h("PreToolUse",t(e));return r.k&&{block:true,reason:r.o}});on("tool_result",e=>{h("PostToolUse",t(e))})
on("session_before_compact",()=>{h("PreCompact",{trigger:"auto"})});on("turn_end",()=>{h("Stop")});on("session_shutdown",()=>{h("SessionEnd",{reason:"other"})})}
~~~

## The hook wiring it reads (engine piece `settings.json`, 231 B)
~~~json
{"hooks":{"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn"}]}]}}
~~~

## ROOT PLAN

goal:g7.16.1.11. The authority is the owner's order to belam (signed 03:48Z): STAGE 2 ACCEPTED, STAGE 2.5 GO. The council BLOCKER (belam, 04:12Z) is folded in: Slice=agi.slice with a system agi.slice read from config:guard, falsifier N4 as a HARD GATE before the start, the §N pane (script + fifo), and no dtach act.
This plan was prepared in Phase A with no root. Every act below is listed together with its UNDO and its PROOF before any act runs.

Shorthands (used in the text only; each command spells the names out):
- P = director-general-5 · A = agi-director-general-5 · M = /data/work/agi (MAIN, on tmpfs, owned by <user>)
- Hm = /var/lib/agi/director-general-5 · V = /tmp/agi-stage25/v4 (the engine-v4.md, pieces/ and this plan)
- BF = /tmp/agi-stage25/v4/before (mode 700, owner): the recorded before-values

Marks:
- **[SHARED]** = box-wide state on a box with live sessions
- **[KEY]** = key or credential handling
- **[MAIN]** = writes inside MAIN or its .git
- **[PRIV]** = privacy-guard material

Runner: DG3 (the owner uid with sudo). No act may print a key, a token, a credential, a hostname, an IP, the owner's username or a home path value.

## 0 · Pre-flight (no root). Every line must print the expected value; otherwise STOP.
- **P0.1 the box is clean**
  - `getent passwd | grep -c '^agi-'; getent group agi | wc -l` -> 0, 0
  - `ls -d /var/lib/agi /opt/agi 2>/dev/null | wc -l; ls /run/systemd/system | grep -c '^agi'; sudo test -e /etc/polkit-1/rules.d/50-agi.rules; echo $?` -> 0, 0, 1
  - `systemctl cat agi.slice 2>&1 | grep -c 'No files found'` -> 1 (there is no SYSTEM agi.slice yet; the two pre-existing system units agi-memguard and agi-ram-main stay untouched; never glob-delete agi-* units)
- **P0.2 the DG5 row and its old seat**
  - `sed -n 's/^  - {/{/p' M/.agi/nodes/.geometry/posts.md | jq -c 'select(.name=="director-general-5")|{pid,recover,engine}'` -> `{"pid":0,"recover":false,"engine":null}`
  - `tmux list-windows -a -F '#{window_name}' | grep -cx director-general-5` -> 0
  - The old-engine scope check: `systemctl --user list-units --plain --no-legend 'agi-post-director-general-5-*.scope' | wc -l`. The guard survey (03:5xZ) found ONE such scope still running in app.slice (8 tasks).
  - If the count is >= 1, read only its process names: `for s in $(systemctl --user list-units --plain --no-legend 'agi-post-director-general-5-*.scope' | cut -d' ' -f1); do cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice/$s/cgroup.procs | xargs -rI{} cat /proc/{}/comm; done | sort | uniq -c`
    - If the names include `claude`, that is a live old-engine DG5 session: HOLD and BANK. It is stopped only on the owner's or DG3's word, with `systemctl --user stop <scope>`, so two engines never seat one post.
    - If the names are only `pi` / `python3`, it is DG5's detached parent round: leave it running and note it.
- **P0.3 memory and disk** (skill agi-memory-guard)
  - `grep MemAvailable /proc/meminfo` -> >= 4 GiB
  - `awk -F'[= ]' '/some/{print $3}' /proc/pressure/memory` -> < 10
  - `df --output=avail -BM /var /opt | tail -2` -> >= 1024M each (pi copy 207 MiB + claude 231 MiB + worktree ~160 MiB)
- **P0.4 the pane tool**: `script --version` -> util-linux >= 2.35 (box: 2.39.3, `-O` present). No dtach act: dtach is retired by §N.
- **P0.5 the guard values are current**: `bash M/extensions/agi/guard/guard-init.sh --dry-run --user "$(id -un)" 2>&1 | sed -n '/fence the engine/,/agi-engine.slice/p' | grep -cE '^ +[-+](Memory|ManagedOOM|TasksMax|CPUWeight)'` -> 0. A comment-only diff is allowed; this proves the user agi.slice [Slice] values equal config:guard today.
- **P0.6 credential freshness [KEY]** (prints minutes only): `echo $(( ($(jq .claudeAiOauth.expiresAt ~/.claude/.credentials.json)/1000 - $(date +%s))/60 ))` -> >= 60. If it is lower, wait for the owner's Claude Code to refresh it first (see Risk K1).
- **P0.7 record the before-values** (`install -d -m 700 BF`):
  - ACLs: `getfacl -R -p --skip-base M/.git/objects M/.git/refs/heads M/.git/logs M/.agi/sessions/inbox M/.agi/sessions/rotations M/.agi/comms > BF/acl.txt 2>&1; getfacl -p M/.git/worktrees M/.git/refs M/.agi/sessions M/.agi/sessions/seats/director-general-5.key > BF/acl-top.txt`. Expected: no extended entries (`grep -c '^user:[a-z]' BF/acl.txt` -> 0; measured 0 on inbox + rotations in Phase A).
  - Modes: `stat -c '%a %U:%G %n' M/.git M/.git/objects M/.git/refs M/.git/refs/heads M/.git/logs M/.git/worktrees M/.agi/sessions M/.agi/sessions/inbox M/.agi/sessions/rotations M/.agi/sessions/seats/director-general-5.key M/.agi/comms | sed "s/$(id -un)/<user>/g" > BF/modes.txt`. Expected: dirs 775 <user>:<user>; the seat key 600.
  - Repo: `git -C M worktree list | wc -l > BF/worktrees.n; git -C M for-each-ref refs/heads/posts | wc -l > BF/posts.n` -> 726 / 0 in Phase A.
  - Row: `sed -n 's/^  - {/{/p' M/.agi/nodes/.geometry/posts.md | jq -c 'select(.name=="director-general-5")' > BF/row.json; chmod 600 BF/row.json`. The row carries a pubkey and session cells: never print it.
  - `ls /run/systemd/system/multi-user.target.wants 2>/dev/null | wc -l > BF/wants.n`

## 1 · MAIN graph and code acts (no root), each one commit
- **C1 [MAIN] config:engine v2 -> v4** (config:engine changes only through the Prime). belam lands `V/engine-v4.md` as ONE new version of config:engine through write.py (its THOUGHT block is included), then runs `grid.py commit --all`.
  - UNDO: write.py config:engine back to the v2 bytes (`git show 50eda68b1f:.agi/nodes/.geometry/engine.md`), as a new version
  - PROOF: `cd M; for f in V/pieces/*; do sh V/pieces/sect "$(basename $f)" HEAD | cmp -s - "$f" || echo DIFF $f; done` -> silent (24 of 24 byte-exact; measured on a scratch clone)
- **C2 [MAIN] no second seat by hand**: rotate.py `cmd_stand_up` (after line ~2350) and the spawn gate (~2471) refuse a row whose `engine` cell is set: `ERR: stand-up refused: <post> is engine v4 (systemd-owned)`. That is 3 lines plus 1 test. It closes the guard survey's gap: a pid-0 row with no window would otherwise be stood up a second time.
  - UNDO: `git revert <sha>`
  - PROOF: the new test passes; `python3 -m pytest extensions/agi/tests/ -q -k stand_up`
- **C3 [MAIN] the posts' memory alarm**: config:crons gains the cadence `memory_alarm_posts` (every 1 min, box local-town). Its cmd is today's memory_alarm cmd plus `--cgroup /sys/fs/cgroup/agi.slice --state {root}/sessions/memory-alarm-posts.json`. grid_sync's `crons.py apply` installs it within 5 min.
  - UNDO: remove the cadence row (the next apply drops the line)
  - PROOF: `python3 extensions/agi/bin/crons.py show | grep -c memory_alarm_posts` -> 1; the same cmd with `--dry-run` -> `{"level": "ok", ...}`
- **C4 [MAIN] the ONE row cell (the switch)**, run from M (proven on a scratch clone, commit "write.py: config:posts (belam)"):
  ```
  python3 extensions/agi/bin/write.py config:posts 'sub {"name": "director-general-5", => {"name": "director-general-5", "engine": {"v": 4, "harness": "pi-free", "model": "stealth/space-bunny-alpha", "effort": "medium", "trunk": "local-maxxing/season2/main", "seeds": "doc:unified-director-brief,doc:unified-head,goal:g7.16.1", "rotate_pct": 47},' --actor belam --role prime_director --dry-run
  ```
  Then run the same without `--dry-run` (per skill agi-post §1). `recover: false` and `pid: 0` stay, which keeps heal.py off the row (heal.py:3873 returns at pid <= 0 before any act). The row's own harness/model/effort cells are NOT changed: v4 reads them from the engine object, so rollback is dropping this one cell.
  - UNDO: the reverse `sub` (the engine object => nothing)
  - PROOF: `cd M && sh V/pieces/sect agi-project HEAD | sh -s /tmp/x HEAD && ls /tmp/x/multi-user.target.wants` -> exactly `agi-post@${P}.service agi-project.path` (measured on the real posts.md: 28 rows -> 1)

## 2 · Root acts, in order: command · UNDO · PROOF
- **R1 [SHARED]** `sudo install -d -m 755 /opt/agi /opt/agi/bin /var/lib/agi`
  - UNDO: T9
  - PROOF: `stat -c '%a %U' /opt/agi/bin /var/lib/agi` -> 755 root (x2)
- **R2 [SHARED] pi for a non-owner uid** (the owner's home is 750)
  - `sudo cp -r "$(readlink -f "$(dirname "$(readlink -f /usr/local/bin/pi)")/..")" /opt/agi/pi && sudo chmod -R a+rX /opt/agi/pi && sudo ln -s ../pi/dist/cli.js /opt/agi/bin/pi`
  - UNDO: T9
  - PROOF: `sudo -u nobody /opt/agi/bin/pi --version` -> 0.67.68
- **R3 [SHARED] claude for a non-owner uid** (CC proof only; the post runs pi)
  - `sudo install -m 755 "$(readlink -f "$(command -v claude)")" /opt/agi/bin/claude`
  - UNDO: T9
  - PROOF: `sudo -u nobody /opt/agi/bin/claude --version` -> `2.1.286 (Claude Code)`
- **R4 [SHARED][MAIN] project the body from M@HEAD** (= agi-seed's pipeline, minus sysusers/reload/start)
  - PRE: `cd M && sh V/pieces/sect agi-project HEAD | cmp - V/pieces/agi-project` -> silent. Otherwise STOP: root never runs bytes it did not review.
  - `cd /data/work/agi && sudo sh -c 'echo HEAD:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n "/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}"|sh -s /run/systemd/system HEAD'`. git as root under sudo accepts M through SUDO_UID.
  - UNDO: T2
  - PROOF:
    - `ls /run/systemd/system/multi-user.target.wants` -> `agi-post@${P}.service agi-project.path`
    - `grep -c 'H=pi --provider openrouter' '/run/systemd/system/agi-post@${P}.service.d/h.conf'` -> 1; `grep -o 'O=[^ ]*' ...h.conf` -> `O=/data/work/agi`
- **R4b [SHARED] never arm the re-projector in 2.5**: `sudo rm /run/systemd/system/multi-user.target.wants/agi-project.path`. An active agi-project.path would run agi-project AS ROOT from M@HEAD on every trunk commit, and every post writes M (risk M2).
  - UNDO: `sudo ln -s ../agi-project.path /run/systemd/system/multi-user.target.wants/`
  - PROOF: the wants dir lists only `agi-post@${P}.service`
- **R5 [SHARED] user + group**: `sudo systemd-sysusers /run/systemd/system/agi-users.conf`
  - UNDO: T8
  - PROOF: `id -nG agi-director-general-5` -> `agi-director-general-5 agi`; `getent passwd agi-director-general-5 | cut -d: -f5,6` -> `director-general-5:/var/lib/agi/director-general-5`
- **R6 home**: `sudo install -d -m 755 -o agi-director-general-5 -g agi-director-general-5 /var/lib/agi/director-general-5 /var/lib/agi/director-general-5/.claude /var/lib/agi/director-general-5/.config /var/lib/agi/director-general-5/.config/agi /var/lib/agi/director-general-5/hooks`. StateDirectory= adopts it at start.
  - UNDO: T7
  - PROOF: `stat -c '%U %a' /var/lib/agi/director-general-5` -> `agi-director-general-5 755`
- **R7 [KEY] the env file: ONE per-spawn zero-USD key**, NEVER the long-lived .env key (stage-2 R10 shape). Run from M:
  ```
  python3 -c 'import sys;sys.path.insert(0,"extensions/agi/bin");import provisioning as p;k=p.mint(iter_n="S25",agent_id="agi-director-general-5",tier="kid",zero_usd=True,ttl_minutes=480,root=".");sys.stdout.write("OPENROUTER_API_KEY="+k.secret+"\n") if k else sys.exit(3)' | sudo sh -c 'umask 077; cat > /var/lib/agi/director-general-5.env'
  ```
  rc 3 = no provisioning key: STOP. The key is never printed.
  - UNDO: `sudo shred -u /var/lib/agi/director-general-5.env`; the key dies at its 480-min TTL (0.01 USD cap)
  - PROOF: `sudo sh -c 'grep -c "^OPENROUTER_API_KEY=" /var/lib/agi/director-general-5.env; stat -c "%a %U" /var/lib/agi/director-general-5.env'` -> `1` / `600 root`; `python3 extensions/agi/bin/provisioning.py status | grep -c agi-director-general-5` -> 1
  - NOTE: re-run R7 + `systemctl restart` before the TTL ends, or the post's turns fail "no key" (Risk K3)
- **R8 [KEY] the owner's Claude Code credential**
  - Locate (prints only the relative form): `ls "$HOME/.claude/.credentials.json" | sed "s|^$HOME|<home>|"` -> `<home>/.claude/.credentials.json`
  - Copy, least privilege (`claudeAiOauth` only; the file's `mcpOAuth` connector tokens are dropped):
    ```
    jq '{claudeAiOauth}' "$HOME/.claude/.credentials.json" | sudo sh -c 'umask 077; cat > /run/agi25-cred.tmp' && sudo install -m 600 -o agi-director-general-5 -g agi-director-general-5 /run/agi25-cred.tmp /var/lib/agi/director-general-5/.claude/.credentials.json && sudo shred -u /run/agi25-cred.tmp && echo '{"hasCompletedOnboarding":true}' | sudo sh -c 'umask 077; cat > /var/lib/agi/director-general-5/.claude.json; chown agi-director-general-5: /var/lib/agi/director-general-5/.claude.json'
    ```
    (Whole-file variant if the owner prefers it: `sudo install -m 600 -o agi-director-general-5 -g agi-director-general-5 "$HOME/.claude/.credentials.json" /var/lib/agi/director-general-5/.claude/.credentials.json`.)
  - UNDO: `sudo shred -u /var/lib/agi/director-general-5/.claude/.credentials.json /var/lib/agi/director-general-5/.claude.json`
  - PROOF: `sudo stat -c '%a %U' /var/lib/agi/director-general-5/.claude/.credentials.json` -> `600 agi-director-general-5`; `sudo jq -r 'keys|join(",")' <same>` -> `claudeAiOauth` (key names only, never values)
- **R9 [PRIV] the box privacy pre-commit guard, for the post.** MAIN's `.git/hooks/pre-commit` execs a guard in the owner's 750 home. A worktree inherits MAIN's hooks, so as A every commit would FAIL. The gitconfig piece sets `core.hooksPath=~/hooks` instead.
  ```
  G=$(sed -n 's/^exec \/usr\/bin\/python3 //p' /data/work/agi/.git/hooks/pre-commit); sudo install -m 600 -o agi-director-general-5 -g agi-director-general-5 "$G" /var/lib/agi/director-general-5/.config/agi/precommit_guard.py && sudo install -m 600 -o agi-director-general-5 -g agi-director-general-5 "$(dirname "$G")/scrub-denylist.json" /var/lib/agi/director-general-5/.config/agi/scrub-denylist.json && printf '#!/bin/sh\nexec /usr/bin/python3 "$HOME/.config/agi/precommit_guard.py"\n' | sudo sh -c 'cat > /var/lib/agi/director-general-5/hooks/pre-commit; chmod 755 /var/lib/agi/director-general-5/hooks/pre-commit; chown agi-director-general-5: /var/lib/agi/director-general-5/hooks/pre-commit'
  ```
  (`$G` is never echoed.)
  - UNDO: T7
  - PROOF (falsifier G4, after R15): `sudo -u agi-director-general-5 -H sh -c 'cd ~/t && hostname > .agi/g4-probe && git add .agi/g4-probe && git commit -qm g4 >/dev/null 2>&1; echo rc=$?; git reset -q HEAD .agi/g4-probe; rm -f .agi/g4-probe'` -> `rc=1` (refused). The token is written to the file and never printed.
- **R10 [MAIN] minimal write access for A on MAIN** (ACLs, so no group or mode of MAIN changes; BF holds the before-values)
  - .git dirs, rwx + default, no files:
    `sudo find /data/work/agi/.git/objects -maxdepth 1 -type d -exec setfacl -m u:agi-director-general-5:rwx,d:u:agi-director-general-5:rwx {} + && sudo setfacl -m u:agi-director-general-5:rwx /data/work/agi/.git/refs /data/work/agi/.git/refs/heads /data/work/agi/.git/logs /data/work/agi/.git/logs/refs /data/work/agi/.git/logs/refs/heads /data/work/agi/.git/worktrees`
    That covers the worktree admin dir, the branch posts/<p> plus its reflog, loose objects, and refs/claims. It never covers .git/config or .git/hooks (write there = code exec as the owner), and never the other 725 worktree dirs.
  - Shared sessions (worktree state resolves here through `git_common_root`, as for today's worktree posts):
    `sudo setfacl -R -m u:agi-director-general-5:rwX,d:u:agi-director-general-5:rwX /data/work/agi/.agi/sessions/inbox && sudo setfacl -m u:agi-director-general-5:rwx,d:u:agi-director-general-5:rwx /data/work/agi/.agi/sessions/rotations && sudo setfacl -m u:agi-director-general-5:rwx /data/work/agi/.agi/sessions`
    - inbox = read/mark + deliver: 2,345 files
    - rotations = the agi-brief record
    - the sessions dir itself = verify-suite.lock (row 38)
  - **[KEY]** the seat key, read-only, so signed sends verify against the row's unchanged pubkey ("keep both keys"): `sudo setfacl -m u:agi-director-general-5:r /data/work/agi/.agi/sessions/seats/director-general-5.key`
  - .agi/comms: NONE. send.py's comms root is `<graph root>/comms/season-2`, which is the post's own worktree. dm transcripts are committed on posts/<p> and merged up like any worktree post's.
  - UNDO: the same commands with `setfacl -x u:agi-director-general-5,d:u:agi-director-general-5` (dirs with defaults), `-x u:agi-director-general-5` (the rest), and `-R -x ...` for inbox.
    - PROOF of the undo: `getfacl -R -p --skip-base <the P0.7 targets> | diff - BF/acl.txt` -> empty
    - files A created stay owned by A until T5 hands them back
  - PROOF: `sudo -u agi-director-general-5 test -w /data/work/agi/.git/refs/heads && sudo -u agi-director-general-5 test ! -w /data/work/agi/.git/config && sudo -u agi-director-general-5 test ! -w /data/work/agi/.git/hooks && echo scoped` -> `scoped`
- **R11 [SHARED] the polkit rule** (group agi may START agi-post@ units; tick.sh run by hand heals a StartLimit failure without sudo):
  `cd M && sh V/pieces/sect agi.rules HEAD | sudo tee /etc/polkit-1/rules.d/50-agi.rules >/dev/null`
  - UNDO: T4
  - PROOF: `sudo cmp /etc/polkit-1/rules.d/50-agi.rules V/pieces/agi.rules` -> silent
- **R12 [SHARED] the SYSTEM agi.slice, values READ from config:guard** via the slice guard-init.sh already wrote from it. P0.5 proves those values are current. No number is typed:
  `systemctl --user cat agi.slice | awk '/^\[Slice\]/{p=1}p&&/^(\[Slice\]|Memory|ManagedOOM|TasksMax|CPUWeight)/' | sudo tee /run/systemd/system/agi.slice >/dev/null`
  - UNDO: T2 (`sudo rm /run/systemd/system/agi.slice`)
  - PROOF: `diff <(systemctl --user cat agi.slice | grep -E '^(Memory|ManagedOOM)') <(grep -E '^(Memory|ManagedOOM)' /run/systemd/system/agi.slice)` -> empty
  - Measured in Phase A: MemoryHigh 8832M, Max 9814M, SwapMax 2047M, oomd kill at 40%. See Risk G1 for the budget.
- **R13 [SHARED]** `sudo systemctl daemon-reload` (the live posts are user-manager scopes; running system services keep running)
  - UNDO: T3
  - PROOF: `systemctl cat agi-post@director-general-5 | grep -c '^# /run/systemd/system'` -> 2 (template + h.conf)

### GATE N4 (HARD): the DG5 start is HELD until every line passes; any miss = STOP, nothing started
- `systemctl show -p Slice --value agi-post@director-general-5` -> `agi.slice`
- `systemctl show agi.slice -p MemoryMax -p MemoryHigh -p ManagedOOMMemoryPressure -p ManagedOOMMemoryPressureLimit`. Expected: MemoryMax and MemoryHigh finite (not `infinity`) and equal to the user agi.slice values (R12 proof); `ManagedOOMMemoryPressure=kill`; the limit is config:guard's AGI_OOMD_LIMIT (measured 40% -> `ManagedOOMMemoryPressureLimit=40.00%`)
- `systemd-analyze verify agi-post@${P}.service agi.slice 2>&1 | wc -l` -> 0 (measured 0 in Phase A on the projected bytes)
- P0.2 holds (no live `claude` in an old DG5 scope)

### Start and the live half of N4
- **R14 START**: `sudo systemctl start agi-post@director-general-5`. The first start makes the worktree (~153 MiB checkout on ext4) within the 90 s start timeout.
  - UNDO: T1
  - PROOF:
    - `systemctl is-active agi-post@director-general-5` -> active
    - N4 live: `systemctl show -p ControlGroup --value agi-post@director-general-5` -> `/agi.slice/agi-post@${P}.service`
    - `oomctl dump | grep -c '/agi.slice'` -> >= 1. Otherwise STOP (T1) at once.
    - `sudo -u agi-director-general-5 git -C /var/lib/agi/director-general-5/t branch --show-current` -> `posts/director-general-5`
    - `sudo stat -c '%a %F' /run/agi-director-general-5/i /var/lib/agi/director-general-5/o` -> `600 fifo`, `600 regular file`
    - `journalctl -u agi-post@director-general-5 -b | grep -c 'dubious ownership'` -> 0 (F1 fixed)
- **R15 owner view of the pane (row 39)**: `sudo setfacl -m u:"$(id -un)":r /var/lib/agi/director-general-5/o`. ExecStartPre never re-creates `o` (`[ -e o ]||install`), so the ACL survives restarts.
  - UNDO: `sudo setfacl -x u:"$(id -un)" /var/lib/agi/director-general-5/o`
  - PROOF: `tail -c 300 /var/lib/agi/director-general-5/o | wc -c` -> 300, as the owner, without sudo
- **R16 [KEY] ONE claude start as A** (no prompt, no work). This reports whether the credential is uid-bound, network-bound or neither.
  - (a) `sudo -u agi-director-general-5 -H env HOME=/var/lib/agi/director-general-5 DISABLE_AUTOUPDATER=1 /opt/agi/bin/claude auth status --json | jq -c '{loggedIn,authMethod,subscriptionType}'` -> `{"loggedIn":true,"authMethod":"claude.ai",...}`
  - (b) `sudo -u agi-director-general-5 -H sh -c 'cd; rm -f c.i; mkfifo -m600 c.i; exec 3<>c.i; DISABLE_AUTOUPDATER=1 SHELL=/bin/sh timeout 40 script -qfO c.o -c "/opt/agi/bin/claude --model claude-sonnet-5-5" <&3'; sudo -u agi-director-general-5 -H sh -c 'cd; echo login=$(grep -aciE "/login|log in|sign in|invalid api key|401|expired" c.o) banner=$(grep -ac "Claude Code" c.o); shred -u c.o; rm -f c.i'`. Counts only: the banner can show the account email.
  - (c) token family (prints `same` or `differs` only): `[ "$(jq -r .claudeAiOauth.refreshToken ~/.claude/.credentials.json | sha256sum)" = "$(sudo jq -r .claudeAiOauth.refreshToken /var/lib/agi/director-general-5/.claude/.credentials.json | sha256sum)" ] && echo same || echo differs`
  - REPORT:

    | (a) loggedIn | (b) login=0 banner>=1 | means |
    |---|---|---|
    | true | yes | NEITHER uid- nor network-bound, as far as one egress can show. The same box means the same egress, so network-binding cannot be excluded here; OAuth bearer tokens are not documented as IP-bound |
    | true | no (401 / expired) | server- or device-bound |
    | false | — | uid/file-bound, or the file is unread |

    If (c) is `differs`, one side refreshed and rotated the refresh token: watch the owner's CC sessions for a logout and tell belam at once (Risk K1).
  - UNDO: R8's undo

## 3 · ROLLBACK to today's engine: ONE command, from MAIN
```
cd /data/work/agi && python3 extensions/agi/bin/write.py config:posts 'sub {"name": "director-general-5", "engine": {"v": 4, "harness": "pi-free", "model": "stealth/space-bunny-alpha", "effort": "medium", "trunk": "local-maxxing/season2/main", "seeds": "doc:unified-director-brief,doc:unified-head,goal:g7.16.1", "rotate_pct": 47}, => {"name": "director-general-5",' --actor belam --role prime_director && sudo systemctl stop agi-post@director-general-5 && sudo rm -f /run/systemd/system/multi-user.target.wants/agi-post@${P}.service && sudo systemctl daemon-reload && python3 extensions/agi/bin/rotate.py stand-up --post director-general-5
```
The steps, in order:
1. The row loses its one cell first. agi-project then never relinks it, and C2's gate lets the stand-up through.
2. The unit stops. ExecStopPost runs agi-flush: it commits and merges the trunk into posts/director-general-5.
3. The wants link goes.
4. Today's engine stands DG5 up in tmux as before.

What survives: the work is on branch posts/director-general-5 in MAIN, for the master to gate like any merge-up. The user, home and env stay until the full teardown.
PROOF: `systemctl is-active agi-post@director-general-5` -> inactive, and the tmux window director-general-5 exists.

## 4 · Full teardown back to the pre-run state (after the rollback, or instead of it)
- **T1** `sudo systemctl stop agi-post@director-general-5` (ExecStopPost flushes)
  - PROOF: `systemctl is-active agi-post@director-general-5` != active; `cat /sys/fs/cgroup/agi.slice/agi-post@${P}.service/cgroup.procs 2>/dev/null | wc -l` -> 0
- **T2** remove the projected files by exact name:
  `sudo sh -c 'cd /run/systemd/system && rm -rf agi-post@.service agi-post@${P}.service.d agi-project.service agi-project.path agi-users.conf agi.slice multi-user.target.wants/agi-post@${P}.service multi-user.target.wants/agi-project.path'`
  Then `rmdir multi-user.target.wants`, only if BF/wants.n was 0.
  - PROOF: `ls /run/systemd/system | grep -c '^agi'` -> 0
- **T3** `sudo sh -c 'systemctl daemon-reload; systemctl reset-failed agi-post@${P}.service 2>/dev/null; :'`
  - PROOF: `systemctl list-units --all --no-legend 'agi-post@*' agi.slice | wc -l` -> 0
- **T4** `sudo rm -f /etc/polkit-1/rules.d/50-agi.rules`
  - PROOF: `sudo test -e /etc/polkit-1/rules.d/50-agi.rules; echo $?` -> 1
- **T5 [MAIN] hand MAIN back**, in this order:
  - (a) `git -C /data/work/agi worktree remove --force /var/lib/agi/director-general-5/t`, as the owner (removes the admin dir; the branch stays)
  - (b) R10's UNDO
  - (c) `sudo find /data/work/agi/.git /data/work/agi/.agi/sessions -user agi-director-general-5 -exec chown "$(id -un)":"$(id -gn)" {} +`. These are loose objects, refs/heads/posts/director-general-5, its reflog and the rotation records: kept and handed back, never deleted.
  - PROOF: `getfacl -R -p --skip-base <P0.7 targets> | diff - BF/acl.txt` -> empty; `sudo find /data/work/agi -user agi-director-general-5 | wc -l` -> 0; `git -C /data/work/agi worktree list | wc -l` = BF/worktrees.n
- **T6 [KEY]** `sudo shred -u /var/lib/agi/director-general-5.env /var/lib/agi/director-general-5/.claude/.credentials.json /var/lib/agi/director-general-5/.config/agi/scrub-denylist.json`
  - PROOF: those three paths are gone. The OpenRouter key dies at its TTL, with no reap (a reap could revoke a live round's key).
- **T7** `sudo rm -rf /var/lib/agi/director-general-5` (the private ssh key, the home, `o`, `track`, `.pi`)
  - PROOF: `sudo test -e /var/lib/agi/director-general-5; echo $?` -> 1
- **T8** `sudo sh -c 'userdel agi-director-general-5; getent group agi-director-general-5 >/dev/null && groupdel agi-director-general-5; groupdel agi'`
  - PROOF: `getent passwd | grep -c '^agi-'` -> 0; `getent group agi | wc -l` -> 0
- **T9** `sudo rm -rf /var/lib/agi /opt/agi`
  - PROOF: `ls -d /var/lib/agi /opt/agi 2>/dev/null | wc -l` -> 0
- **T10 [MAIN]** reverse C3, C2 and C1 (each its own undo above); C4 is undone by the rollback. The graph keeps every version (grid).
  - PROOF: `crons.py show | grep -c memory_alarm_posts` -> 0; `systemctl list-unit-files --no-legend 'agi*' | awk '{print $1}'` -> exactly agi-memguard.service and agi-ram-main.service

## 5 · Act count: 17 sudo acts (R1-R16 incl. R4b) + 4 MAIN graph/code acts (C1-C4)
- Root acts: R1 R2 R3 R4 R4b R5 R6 R7 R8 R9 R10 R11 R12 R13 R14 R15, plus the R16 proof run as A
- [MAIN]: C1 C2 C3 C4 · R4 (reads M@HEAD as root) · R10 (ACLs) · T5
- [KEY]: R7 (per-spawn key) · R8 (CC credential) · R10 seat-key read · R16 · T6
- [SHARED]: R1-R5 R4b R11 R12 R13
- [PRIV]: R9
- Optional, owner-gated, BANKED: R-MG [SHARED]. It patches agi-memguard.py (line ~43 `procs()`) so a process whose cgroup is under `/agi.slice/agi-post@` is protected (-900) like `claude`.
  - Backup first: `sudo cp -a /usr/local/sbin/agi-memguard.py /usr/local/sbin/agi-memguard.py.pre25`
  - UNDO: restore that backup and `systemctl restart agi-memguard`
  - Without it, memguard can SIGSTOP DG5's pi when RAM is short (today's claude posts are protected) = parity row 43 short.

## 6 · Risks
- **M2** root executes engine bytes from M@HEAD (R4). This is mitigated by the R4 PRE cmp and by R4b, which leaves agi-project.path unarmed. In stage 3 the projector must not run as root from a branch every post writes.
- **G1 (BANK)** the system agi.slice copies the USER agi.slice's caps (9814M max) beside user@ (14021M max). The two can together exceed RAM. oomd at 40% on the new slice and memguard are the backstops.
  - Owner's call: (a) accept for one pi post (~0.3-1 GB real); (b) add config:guard cells GUARD_POSTS_MAX_* and a guard-init layer that writes the system slice, then re-run guard-init (shrinks user@); (c) set GUARD_DOCKER_BUDGET as the outside-user@ budget.
  - Recommendation: (a) for 2.5, then (b).
- **K1 (BANK) refresh-token rotation.** The copied OAuth credential and the owner's share one refresh-token family. If either side refreshes and the server rotates the token, the other copy can be logged out, and every live CC post uses the owner's copy.
  - Mitigation: P0.6 (start only with >= 60 min of access-token life); no long run of claude as A (the post runs pi); the R16 (c) check.
  - Safer path for any lasting use: the owner runs `claude setup-token` and the post gets that long-lived token through its env file (owner's call).
- **K2** the copy grants the owner's Claude account to uid A. Least privilege: claudeAiOauth only (no MCP connector tokens); file mode 600 owned by A; shredded at T6.
- **K3** the post's OpenRouter key has a 480-min TTL. Re-mint (R7) + restart before expiry, or the post stops answering (free model, 0.01 USD cap).
- **S1** with R10, A may create, rename or delete entries in M/.git/refs, refs/heads, logs and .agi/sessions. That is the same power a post running as the owner has today; .git/config and .git/hooks stay owner-only.
- **P1** the typescript `o` grows without bound (§N falsifier N3: X MB/h is a cell to measure on the live post; 53 KB in a 75 s no-key run).
- **R** a reboot clears /run: v4 DG5 is then down, heal.py ignores it (pid 0, recover false), and the rollback stand-up is the hand restart. agi-seed is not installed in 2.5.
- **D** DG5 cannot dispatch kids or run detached workflows (parity rows 30, 33): both mint per-spawn keys from M/.env (600, owner), which A must never read.
  - BANK a broker: a root-owned socket-activated `agi-mint` that mints zero-USD keys for group agi, or dispatch run for DG5 from the owner side.

## PARITY PROOFS (55 rows)

This covers the 42 rows of doc:g716111-stage25-parity, the 10 guard/watchdog rows the owner added (03:48Z via belam; mapped by §N.4 and a read-only guard survey), and 3 rows these tests found.

**Shorthands**
- P = director-general-5 · A = agi-director-general-5 · Hm = /var/lib/agi/director-general-5 · M = /data/work/agi
- U = `agi-post@director-general-5`
- AS = `sudo -u agi-director-general-5 -H` (run as the post)
- Run? R = needs the post running · S = after the root acts, unit stopped or running · – = graph/repo only

**Status values (expected once rootplan.md has run)**
- MATCH, EXCEEDS = matched-or-better
- SHORT = a named gap, never silent

Phase-A evidence lives in test.txt; "(T#)" points at it.

| # | capability | v4 mechanism | status | proof on the live post | expected | run? |
|---|---|---|---|---|---|---|
| 1 | post identity = one row | ONE cell `"engine": {"v":4,...}`; agi-project `select(.engine.v==4)`, `.+.engine` | MATCH | `cd M; sect agi-project HEAD \| sh -s /tmp/x HEAD; ls /tmp/x/multi-user.target.wants` | `agi-post@${P}.service agi-project.path` only (T3: 28 rows -> 1) | – |
| 2 | stand up | U + the root plan; ExecStartPre self-provisions key, worktree, tools, pane | MATCH | `systemctl is-active U` | active | R |
| 3 | take down / no double seat | dropped rows unlinked (`rm -f $w/agi-post@*`); recover:false + pid 0 keep heal.py off (heal.py:3873); C2 gate on rotate.py stand-up | MATCH | drop the cell on a test ref, re-project: the link is gone; `rotate.py stand-up --post director-general-5` | wants = agi-project.path only (T3); `ERR: stand-up refused ... engine v4` | – / S |
| 4 | harness + model cells | h.conf `H=pi --provider openrouter --model <m> --thinking <e> --skill skills -e ../bin/cccc.ts` from the engine object | MATCH | `systemctl show -p Environment U \| grep -c 'model stealth/space-bunny-alpha'` | 1 | S |
| 5 | effort cell | pi `--thinking <effort>`; claude rows get `--effort <effort>` | MATCH | `systemctl show -p Environment U \| grep -c 'thinking medium'` | 1 | S |
| 6 | settings cell | DG5's row is `settings: ""` = the one settings.json | MATCH | `AS jq -c '.hooks\|keys' ~/.claude/settings.json` | `["SessionStart","Stop","UserPromptSubmit"]` | S |
| 7 | the brief | brief.py walks `parents:` frontmatter over .agi/nodes (no .agi/n needed); seeds = card + template + head + owning goal + own claims; whole nodes by \|b\| (B=40000 on pi) | EXCEEDS | `AS sed -n 1,8p ~/.brief` | lists doc:card-director-general-5, doc:unified-director-brief, doc:unified-head, goal:g7.16.1 (T5: top 6) | R |
| 8 | first-turn STARTUP OUTPUT | agi-brief runs config:rotations `templates.director.startup.first_turn` (each cmd, its byte_cap, 30 s) on startup/clear | MATCH | the post's first turn shows `## STARTUP OUTPUT` and 9 `### <label>` entries: `AS grep -c '^### ' <(echo '{"source":"startup"}' \| env $(systemctl show -p Environment --value U) agi-brief)` | 9 (T5) | R |
| 9 | the meter | agi-meter on UserPromptSubmit (pi: cccc `input`, tokens from getContextUsage); line = `rotate_pct` cell x window | MATCH | `echo '{"tokens":480000,"context_window":1000000}' \| AS agi-meter` | `At the line (480000/1000000): ...touch ~/.fresh;kill $PPID` (T6) | – |
| 10 | rotation = fresh successor | the out-line touches `~/.fresh`; agi-run drops `-c` when it exists; a crash restart keeps `-c` (resume) | MATCH | after the post rotates: `AS ls ~/.pi/agent/sessions/*/ \| wc -l` grows by 1 and the new session's first usage is < 50k | +1, < 50k | R |
| 11 | rotation record | agi-brief writes `M/.agi/sessions/rotations/<p>.<ts>.json` (seat, rotation engine-v4, result, source, pid 0, recorded_at) per session start | MATCH | `ls M/.agi/sessions/rotations \| grep -c '^director-general-5\.2026'`; `rotate.py status --post director-general-5 --record latest` | +1 per restart; reads the v4 record (T5) | R |
| 12 | after_join (join, pin, reap-proof) | one unit = one cgroup; a restart reaps the tree | EXCEEDS | `systemctl show -p NRestarts,TasksCurrent U` | NRestarts increments; TasksCurrent > 0 | R |
| 13 | card | write.py doc:card-<p> in the post's worktree; committed per turn | MATCH | `AS git -C ~/t log -1 --format=%s -- .agi/nodes/doc/card-director-general-5.md` | a post commit | R |
| 14 | inbox read | worktree -> `send.py read` resolves M's inbox (git common dir); ACL on inbox | MATCH | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/send.py read director-general-5'` | unread blocks once, then none | R |
| 15 | send dm/room/report | send.py from the worktree: inbox append in M, comms in the worktree (merged up), signed with the seat key | MATCH | as the post: `send.py send --to director-general-3 "[ack] v4 up"`; then `tail -3 M/.agi/sessions/inbox/director-general-3.md` | the block with a `sig: ed25519:` line | R |
| 16 | wake / nudge | cccc.ts watches M's inbox file: growth -> a followUp `mail` turn (never interrupts); the pane fifo `i` lets any writer type (`printf 'x\r' > i`) | EXCEEDS | `send.py send --to director-general-5 ping` from any post; within 10 s `sudo tail -c 2000 Hm/o` shows the `mail: send.py read director-general-5` turn | a mail turn (T7: 1 per append, 0 on marker rewrite; real pi: extension turn fired) | R |
| 17 | whois / authority | the seat key stays (ACL read on seats/director-general-5.key); the row pubkey is unchanged; the ssh key signs commits | MATCH | `python3 extensions/agi/bin/send.py whois director-general-5` after a send | VERIFIED | R |
| 18 | key rotation / key_history | not done by v4: the seat key stays across restarts | SHORT (named): seat-key rotation at a v4 rotation (~80 B, after 2.5) | `sed -n 's/^  - {/{/p' posts.md \| jq '.key_history\|length'` | unchanged | – |
| 19 | signed commits | gitconfig gpgsign ssh + `allowedSignersFile=~/.signers` (F6) | EXCEEDS | `AS git -C ~/t log -1 --format=%G?` | G (T6) | R |
| 20 | write a node | write.py in the worktree | MATCH | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/write.py goal:g7.16.1.11 "read body 1:5"'` | 5 lines | S |
| 21 | commit at turn end | Stop -> agi-turn: `git add -A` in the PRIVATE worktree (the post's own edits only), signed | MATCH | `AS git -C ~/t show --stat HEAD` after a turn | the post's paths only | R |
| 22 | hand up the work | branch posts/director-general-5 lives in M; agi-flush merges the trunk; the master gates the branch | MATCH | `git -C M rev-parse --verify posts/director-general-5`; `git -C M merge-base --is-ancestor local-maxxing/season2/main posts/director-general-5` (after a flush) | a sha; rc 0 (T6) | S |
| 23 | master gate / land | skill agi-master-gate on posts/<p>; agi-gate available | MATCH | `cd M && sect agi-gate HEAD \| sh -s HEAD; echo $?` | 0 (T8: 0 with the v4 row, 1 without) | – |
| 24 | path ownership | uid isolation (A writes only its home, worktree and the R10 dirs) + today's rules + the master gate | MATCH | `AS test ! -w M/.git/config && AS test ! -w M/.git/hooks && echo ok` | ok | S |
| 25 | grid versions | the Prime's grid.py commit at landing, unchanged | MATCH | `grid.py log <a node the post edited>` after a landing | the landed version | – |
| 26 | node <-> code file | agi-link on every turn-end commit -> `~/link` | EXCEEDS | after the post edits extensions/agi/bin/heal.py: `AS cat ~/link` | `build:bin-heal extensions/agi/bin/heal.py` (T6 + real MAIN commit: build:bin-rotate) | R |
| 27 | per-node RAM tree | agi-wt pull = node + payload_ref files under `$RUNTIME_DIRECTORY/wt` (tmpfs /run, charged to U); drop on claim release / at flush | EXCEEDS | `AS env RUNTIME_DIRECTORY=/run/agi-director-general-5 sh -c 'cd ~/t; d=$(agi-wt pull build:bin-heal); findmnt -no FSTYPE -T $d; find $d -type f ! -name .b \| wc -l'` | tmpfs, 2 (T6: 2 files, purge on release, moved-guard rc 4) | R |
| 28 | the post's checkout | a git worktree of M on posts/<p> (today's `worktree` mechanism, own uid) | MATCH | `git -C M worktree list \| grep -c /var/lib/agi/director-general-5/t` | 1 | S |
| 29 | claims | owning_goal seeded (seeds cell); loose refs/claims/<mint> made by A feed the brief | MATCH | `AS git -C ~/t update-ref refs/claims/<mint> HEAD ""`, then a new brief ranks the node higher | rank moves (packed claims drop out after gc: noted) | R |
| 30 | dispatch parents/kids | dispatch.py needs M/.env's provisioning key (600 owner), which A must never read | SHORT (named): a key broker (BANK, rootplan risk D) | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/provisioning.py status'` | `provisioning: unavailable` | – |
| 31 | per-spawn keys / spend floor | R7: ONE zero-USD key, 480 min, in a root-owned env file | MATCH | `python3 extensions/agi/bin/provisioning.py status \| grep -c agi-director-general-5` | 1 | S |
| 32 | commit guard hooks | gitconfig `core.hooksPath=~/hooks` + R9's copy of the box privacy pre-commit guard | MATCH | R9's G4 probe | rc=1 (refused) | S |
| 33 | review / workflows | workflow.py detached needs `systemd-run --user` (no user manager for A) + per-stage mints from .env | SHORT (named): linger + key broker (BANK) | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/workflow.py run review --dry-run'` | refuses (no key) | – |
| 34 | judge / corrective / goal edits | the same Python in the worktree | MATCH | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/season.py status'` | prints | S |
| 35 | crash heal | `Restart=always`, `RestartSec=30`; PSI admission ExecStartPre (memory some avg10 > 40 = refuse, retried); tick.sh + polkit by hand | MATCH | `sudo systemctl kill U`; 30 s later is-active; `AS tick.sh` with U stopped | active, NRestarts+1; tick starts it, signed `drift:` commit (T9) | R |
| 36 | memory caps | `Slice=agi.slice` (system slice, config:guard values) + `MemoryHigh=4G` | MATCH | N4: `systemctl show -p ControlGroup --value U`; `systemctl show agi.slice -p MemoryMax,ManagedOOMMemoryPressure` | `/agi.slice/agi-post@${P}.service`; finite, kill | R |
| 37 | box reads / stop a runaway | skill agi-memory-guard reads; A can stop only its own processes | MATCH | the guard's reading command as A | readings | S |
| 38 | verify + suite lock | verification.py's lock resolves to M/.agi/sessions (ACL rwx on the dir) | MATCH | `AS sh -c 'cd ~/t && python3 extensions/agi/bin/verification.py window'` | names M's lock | S |
| 39 | live view | the pane `o` (script typescript, 600) + R15's owner read ACL; a human or tool reads `o` and types into `i` | MATCH | `tail -c 2000 /var/lib/agi/director-general-5/o` as the owner (no sudo) | the post's screen | R |
| 40 | crons | unchanged (crons.py show "up to date"); nudge_sweep logs "no wake" for P, which is harmless (mail = row 16) | MATCH | `python3 extensions/agi/bin/crons.py show \| head -1` | up to date | – |
| 41 | file-access trace | strace -> `agi-track` (each path once) -> `~/track`: bounded (F2 fixed) | EXCEEDS | `sudo wc -l Hm/track` after a session; growth flattens | > 0, bounded (T7: 2,697 unique paths / 75 s) | R |
| 42 | anonymize | ident agi-director-general-5 / agi@agi; the privacy guard (row 32) | MATCH | `AS git -C ~/t log -1 --format='%an %ae'` | `director-general-5 agi@agi` (GECOS) | R |
| 43 | agi-memguard.service | box-wide /proc scan as root (system.slice). Protects comm claude/tmux; pi at /opt/agi is unprotected (adj 0), a SIGSTOP candidate below 1 GiB free | SHORT unless R-MG (BANK: protect cgroup /agi.slice/agi-post@) | `for p in $(cat /sys/fs/cgroup/agi.slice/agi-post@${P}.service/cgroup.procs); do cat /proc/$p/oom_score_adj; done \| sort -u` | -900 (with R-MG); 0 today | R |
| 44 | agi-ram-main.service | U is `After=agi-ram-main.service`; M stays on the RAM tier (ram-sync syncs A's writes into M like anyone's); the worktree is on ext4 | MATCH | `systemctl show -p After U \| grep -c agi-ram-main`; `findmnt -no FSTYPE -T M` | 1; tmpfs | S |
| 45 | memory alarm (PSI warn/red to belam) | box PSI covered today; C3 adds `memory_alarm_posts` on /sys/fs/cgroup/agi.slice | MATCH (with C3) | `crons.py show \| grep -c memory_alarm_posts`; its cmd with `--dry-run` | 1; `{"level": "ok"...}` | – |
| 46 | watchdog reboot (PSI full >= LIMIT for GRACE) | box-wide, slice- and uid-agnostic | MATCH | `systemctl is-active watchdog; grep -E '^(LIMIT\|GRACE)=' /etc/sanctuary-guard/health.env` | active, LIMIT=60, GRACE=900 (live is 60, not 40) | – |
| 47 | config:guard slices (agi-engine / agi-work / ramdisk caps) | the system agi.slice copies the user agi.slice [Slice] that guard-init wrote from config:guard (R12); N4 hard gate | MATCH (budget overlap BANKED, G1) | N4 lines (rootplan) | Slice=agi.slice; MemoryMax == user agi.slice's; kill at 40% | R |
| 48 | keysync timer (user, */2 min) | touches no process; it only syncs posts.md rows season2/main -> trunk by pubkey; the cell lands on the trunk first, so it is kept | MATCH | `git -C M grep -c '"engine": {"v": 4' local-maxxing/season2/main -- .agi/nodes/.geometry/posts.md` after a sync | 1 | – |
| 49 | the box crontab (crons_live, 12 jobs) | unchanged; no job reads `engine`; heal/nudge treat P as pid 0 | MATCH | `crontab -l \| grep -c .` vs before; `crons.py show` | same count (+1 with C3); up to date | – |
| 50 | heal vs tick (no double heal) | heal.py returns at pid <= 0 (3873) before any act; tick.sh projects v4 rows only; C2 refuses a stand-up | MATCH | `grep -cE 'DEAD seat director-general-5\|crash-recovery record for director-general-5' <reaper log>` after the cutover | no new lines | R |
| 51 | oomd interplay | agi.slice `ManagedOOMMemoryPressure=kill` at config:guard's AGI_OOMD_LIMIT; one post's cgroup is killed and Restart brings it back | MATCH | `oomctl dump \| grep -A3 'Path: /agi.slice'` | the limit line (40.00%) | R |
| 52 | magic pane anchor (goal:g7.31.2) | §N.3: the anchor IS the post's name: pane = `/run/agi-director-general-5/i` + `Hm/o`; occupation = U active; it survives every restart. The core magic_pane modules (only on origin/core/*) are not on this branch | MATCH (anchor); the core-module merge is a named follow-up | `printf 'pane-anchor-probe\r' \| sudo tee /run/agi-director-general-5/i >/dev/null`; then the next provider turn starts | a turn (T7: a pane CR submitted a prompt in real pi) | R |
| 53 | skills | pi `--skill skills` loads skills/agi-*/SKILL.md from the worktree | MATCH | the pi startup header in `o` lists the agi-* skills (`ctrl+o` view) | agi-* names | R |
| 54 | pane hygiene (§N traps) | `StandardOutput=null` (no journal copy); `o` header reads `agi-run` (argv hidden); i/o mode 600; `SHELL=/bin/sh` (F7) | MATCH | `journalctl -u U \| grep -c openrouter`; `sudo head -c 200 Hm/o` | 0; `COMMAND="agi-run"` (T7) | R |
| 55 | CC harness for a non-owner uid | R3 claude copy + R8 credential; ONE start (R16) | MATCH if R16 = neither-bound | R16 (a)(b)(c) | loggedIn true; login=0 banner>=1; `same` | S |

## CCCC rows (the hook table, cccc.md), live-post proofs
| CC | proof on the live post | expected | run? |
|---|---|---|---|
| CC1 SessionStart -> session_start / session_compact | `AS stat -c %Y ~/.brief` newer than U's ActiveEnterTimestamp; after a `/compact`, newer again | yes / yes | R |
| CC2 UserPromptSubmit -> input | with the line lowered for the probe (`rotate_pct: 1` on a test row, or `AGI_ROTATE_PCT=1` in a drop-in), the next prompt carries the out-line | out-line in `o` | R |
| CC3 Stop -> turn_end | `AS git -C ~/t log --since=-10min --format=%s \| grep -c agi-director-general-5` | >= 1 per active 10 min | R |
| CC4 Pre/PostToolUse -> tool_call / tool_result | none configured (none on today's posts); proven by the harness with a test hook (exit 2 blocks `rm -rf`) | (T7) | – |

## Counts (55 rows = 42 parity + 10 guard/watchdog/anchor + 3 found in testing)
- **Matched-or-better: 51.**
  - EXCEEDS 7: rows 7, 12, 16, 19, 26, 27, 41
  - MATCH 44
  - This needs the planned C2, C3, R9 and R12, and assumes R16 reads neither-bound.
- **Still short: 4, each named.**
  - 18: seat-key rotation by v4
  - 30: dispatch kids (needs a key broker; A must never read M/.env)
  - 33: detached workflows (linger + the same broker)
  - 43: memguard does not protect a pi post. It becomes MATCH if the owner approves R-MG.
- **Conditional matches:**
  - 47: system agi.slice beside user@ (budget overlap, G1, banked)
  - 52: the anchor matches by construction; the core magic_pane modules are on origin/core/* only
  - 55: it holds only if R16 shows a clean start
- **Versus 12 of 42 matched in doc:g716111-stage25-parity:** 39 of the original 42 rows are now matched-or-better; 18, 30 and 33 are still short.

## PHASE A' rootplan DELTA v4b -> v4c — DG5 = Claude Code (Sonnet 5.5) + Remote Control; ONE pi-free kid on CCCC -- SUPERSEDES the sections above where they differ (owner 04:40Z + 04:49Z on goal:g7.16.1.11)

goal:g7.16.1.11 stage 2.5, PHASE A' (DG3 Opus subagent, no root, nothing installed, no node written). Base = doc:g716111-stage25-rootplan
(= /tmp/agi-stage25/v4b/rootplan.md). Every act NOT named below is unchanged. V = /tmp/agi-stage25/v4c from here on (engine-v4.md,
pieces/, this file). Shorthands as in the base: P = director-general-5 · A = agi-director-general-5 · M = MAIN · Hm = /var/lib/agi/director-general-5.

### 0 · The orders this delta implements
- Owner 04:40Z (via belam): DG5 = Claude Code, Sonnet 5.5, Remote Control ON (visible in the app), as its own user, inside the
  capped agi.slice (N4 first); ONE kid runs pi-free with CCCC; pi never poses as a CC session to Remote Control.
- Owner 04:49Z (goal body): "I will log in manually this time" — DG5's user is logged in ONCE BY THE OWNER; NO credential copy.
  This supersedes the base R8 (copy claudeAiOauth). The copy analysis is kept in §2 as the record for belam's open call.

### 1 · Remote Control: the invocation found on this box (claude 2.1.286; help text only, nothing started)
Verbatim, `claude --help`:
```
  --remote-control [name]               Start an interactive session with Remote
                                        Control enabled (optionally named)
  --remote-control-session-name-prefix <prefix>
      Prefix for auto-generated Remote Control session names (default: hostname)
```
Verbatim, `claude remote-control --help` (a hidden subcommand = a multi-session SERVER, spawns up to 32 sessions):
```
Remote Control - Control local sessions from claude.ai/code or the Claude mobile app
  claude remote-control [options]
```
Also a settings key `remoteControlAtStartup` (user/global scope only — binary: "repo-scoped settings cannot enable Remote Control").
**Chosen: the flag, `claude --remote-control director-general-5 ...`** — one interactive session in the §N pane, the RC bridge in the
same process (so inside the unit cgroup, agi.slice), the CC hooks native, and an EXPLICIT name (the unnamed default is the hostname
— a privacy leak into the app list). This is byte-for-byte the shape today's posts use (templates/harness/claude-code.toml: first argv
`--remote-control <name>`, then `--permission-mode bypassPermissions --model --effort`). Not the server subcommand (it accepts app-side
spawns of new sessions in the dir = a second, unbounded seat). Not the setting (no name → hostname).
RC preconditions, read from the binary's own refusal strings (measured): claude.ai subscription auth ("Remote Control requires a
claude.ai subscription"); NOT ANTHROPIC_API_KEY / apiKeyHelper / ANTHROPIC_AUTH_TOKEN; a FULL-SCOPE login ("Long-lived tokens (from
`claude setup-token` or CLAUDE_CODE_OAUTH_TOKEN) are limited to inference-only ... Run `claude auth login` to use Remote Control");
an organization uuid (from ~/.claude.json oauthAccount); feature flags reachable (refuses if DISABLE_GROWTHBOOK is set).

### 2 · The credentials: path, key names, binding (values never read or printed)
| item | answer | how known |
|---|---|---|
| file | `<home>/.claude/.credentials.json`, mode 600 | measured (owner's) |
| top-level keys | `claudeAiOauth`, `mcpOAuth` (10 connector entries) | measured, key names only |
| claudeAiOauth keys | `accessToken, expiresAt, rateLimitTier, refreshToken, refreshTokenExpiresAt, scopes, subscriptionType` | measured, key names only |
| scopes (names) | `user:file_upload user:inference user:mcp_servers user:plugins user:profile user:sessions:claude_code` | measured |
| account/org identity | NOT in the credential file: `<home>/.claude.json` `oauthAccount` (holds organizationUuid, accountUuid, emailAddress, ...) | measured, key names only |
| uid-bound? | NO field names a uid; protection = file mode 600 + owner uid only | measured (key names) / inferred (no binding beyond the file) |
| host/machine-bound? | NO host or device field; /etc/machine-id is read only for a LOCAL pid-domain registry; RC's own machine id (`remoteControlMachineId`) lives in the per-user ~/.claude.json, generated per config → A shows as its own machine | measured (code strings) / inferred (effect in the app) |
| network-bound? | no IP field; OAuth bearer tokens are not documented as IP-bound; one box = one egress, so it cannot be excluded here | inferred |
| device keys | a `.device-keys.json` / trusted-device enrolment exists for orgs that REQUIRE trusted devices; the owner has none (0 files) | measured (file absent) / inferred (applies to enterprise orgs) |
| refresh token | a COPY shares one refresh family: a rotation on either side can log the other out | inferred (refreshToken + refreshTokenExpiresAt keys) |
| setup-token instead | NOT usable for RC (inference-only scope) | measured (refusal string) |
| claudeAiOauth-only copy | would lack `oauthAccount` → RC "Unable to determine your organization" until a profile refetch | inferred (code: organizationUuid check) |
**With the owner's manual login (04:49Z) A gets its OWN token family**: no shared refresh token (base risk K1 closes), nothing copied,
oauthAccount written by the login itself. Binding then = A's file (600, A) + A's ~/.claude.json machine id; same account, same egress.

### 3 · Engine change (V/engine-v4.md, assembled by V/build/assemble.py from V/pieces/)
| piece | v4b B | v4c B | change |
|---|---|---|---|
| agi-project | 1,653 | 1,679 | claude rows: `claude --remote-control <name> --model .. --effort .. --permission-mode bypassPermissions` |
| agi-post@.service | 1,324 | 1,252 | `DISABLE_AUTOUPDATER=1` (root-owned /opt binary); tool list DERIVED from the `### ` headers (agi-kid included; net -72 B) |
| agi-run | 124 | 357 | claude panes: inbox growth (5 s poll) types `mail: send.py read <p>`, 1 s, then a separate CR into `i` |
| settings.json | 231 | 272 | `skipDangerousModePermissionPrompt: true` (no bypass dialog in a pane nobody answers) |
| cccc.ts | 1,633 | 1,647 | inbox watch `persistent:!1` (F15: `pi -p` never exited) |
| agi-kid | — | 390 | NEW: `agi-kid <name> <task>` = pi-free `-p` + cccc.ts, own HOME ~/k/<name>, tree on kids/<name>, AGI_ROLE=kid, own AGI_WT, stdin null |
| tick.sh | 250 | 254 | F14: scratch lists to ~/.p ~/.q (it overwrote the pane typescript ~/o) |
| agi-seed.service | 514 | — | moved to dropped/ (cap): never installed in 2.5; returns in stage 3 (byte-exact in v4b and the grid) |
| whole / depth 0+1 | 16,375 / 3,418 | **16,384 / 3,478** | caps 16,384 / 4,096: AT the whole cap, 0 B spare |

### 4 · Pre-flight delta
- **P0.6 REMOVED** (freshness of the owner's credential: nothing is copied).
- **P0.6' the owner is at a terminal** for R8a and says in words that the login is his act. Otherwise HOLD after R7.
- **P0.8 RC needs feature flags**: after R13, `systemctl show -p Environment agi-post@${P} | grep -cE 'DISABLE_GROWTHBOOK|NONESSENTIAL_TRAFFIC|ANTHROPIC_'` -> 0.
- P0.2 unchanged and still a HOLD: an old-engine DG5 scope with a live `claude` is stopped by SM or belam only (open call).

### 5 · MAIN acts delta
- **C1** unchanged in form; PROOF now from V: `cd M; for f in V/pieces/*; do sh V/pieces/sect "$(basename $f)" HEAD | cmp -s - "$f" || echo DIFF $f; done` -> silent (24/24, measured on a scratch commit).
- **C2, C3** unchanged (Prime landings; open call).
- **C4 the ONE row cell**, new object (dry-run on a scratch clone: 1 match, ring gate admitted):
  ```
  python3 extensions/agi/bin/write.py config:posts 'sub {"name": "director-general-5", => {"name": "director-general-5", "engine": {"v": 4, "harness": "claude-code", "model": "claude-sonnet-5-5", "effort": "high", "trunk": "local-maxxing/season2/main", "seeds": "doc:unified-director-brief,doc:unified-head,goal:g7.16.1", "rotate_pct": 47, "kid_model": "stealth/space-bunny-alpha"},' --actor belam --role prime_director --dry-run
  ```
  (`effort: high` = today's director rows; a cell, belam may change it.) UNDO = the reverse sub (§7). PROOF: projection as base C4 ->
  wants = `agi-post@${P}.service agi-project.path` (measured).

### 6 · Root acts delta (each: command · UNDO · PROOF)
Unchanged: R1, R2 (pi copy — now for the kid), R4b, R5, R6, R9, R10 (covers the kid too: worktrees + refs/heads), R11, R12, R13, R14, R15.
- **R3 claude for a non-owner uid — now REQUIRED (it IS DG5's harness)**. Command/UNDO as base.
  PROOF adds: `sudo -u nobody /opt/agi/bin/claude remote-control --help </dev/null | head -1` -> `Remote Control - Control local sessions from claude.ai/code or the Claude mobile app`.
- **R4** PROOF line changes: `grep -c 'H=claude --remote-control director-general-5 --model claude-sonnet-5-5' '/run/systemd/system/agi-post@${P}.service.d/h.conf'` -> 1 (the pi grep goes).
- **R7 [KEY]** command unchanged (ONE per-spawn zero-USD OpenRouter key) — it now feeds the KID only; DG5 itself runs on the account.
  PROOF adds: `sudo grep -c '^ANTHROPIC' /var/lib/agi/director-general-5.env` -> 0 (an API key would make RC refuse).
- **R8 REPLACED -> R8a [KEY] OWNER: log DG5's user in, once, by hand** (after R3 + R6; the owner's own terminal):
  `sudo -u agi-director-general-5 -H env DISABLE_AUTOUPDATER=1 /opt/agi/bin/claude auth login --claudeai`
  It prints a sign-in URL; the owner opens it, signs in to his claude.ai account, pastes the code back. Nothing is logged by the plan.
  - UNDO: `sudo -u agi-director-general-5 -H env DISABLE_AUTOUPDATER=1 /opt/agi/bin/claude auth logout`, then T6. Server-side: the owner may revoke the session in his claude.ai settings.
  - PROOF (booleans / key names only):
    - `sudo -u agi-director-general-5 -H env DISABLE_AUTOUPDATER=1 /opt/agi/bin/claude auth status --json | jq -c '{loggedIn,authMethod}'` -> `{"loggedIn":true,"authMethod":"claude.ai"}` (field names measured on the owner's)
    - `sudo stat -c '%a %U' Hm/.claude/.credentials.json` -> `600 agi-director-general-5`
    - `sudo jq '.claudeAiOauth.scopes|index("user:sessions:claude_code")!=null' Hm/.claude/.credentials.json` -> `true` (full scope = RC-eligible)
    - `sudo jq 'has("oauthAccount")' Hm/.claude.json` -> `true`
    - token family, prints `same`/`differs` only: `[ "$(jq -r .claudeAiOauth.refreshToken ~/.claude/.credentials.json | sha256sum)" = "$(sudo jq -r .claudeAiOauth.refreshToken Hm/.claude/.credentials.json | sha256sum)" ] && echo same || echo differs` -> `differs` (own family: K1 closed)
- **R8b NEW: onboarding + workspace trust for ~/t**, as A (no root write), after R8a (tested on a fake file):
  `sudo -u agi-director-general-5 -H sh -c 'f=$HOME/.claude.json;[ -s $f ]||echo {}>$f;jq --arg t "$HOME/t" ".hasCompletedOnboarding=true|.projects[\$t].hasTrustDialogAccepted=true" $f>$f.n&&mv $f.n $f&&chmod 600 $f'`
  - UNDO: same shape with `"del(.hasCompletedOnboarding)|del(.projects[\$t])"`
  - PROOF: `sudo -u agi-director-general-5 -H sh -c 'jq -r --arg t "$HOME/t" ".projects[\$t].hasTrustDialogAccepted" ~/.claude.json'` -> `true`
  (the bypass-permissions dialog is skipped by the engine's settings.json, rewritten at every start.)
- **R16 REPLACED -> R16' the RC + binding proof** (after R14; counts only — the pane line carries a session URL, the banner can show the email):
  - (a) R8a's auth-status line, again, after the start.
  - (b) RC up, no refusal: `sudo grep -aci 'remote control' Hm/o` -> >= 1 · `sudo grep -acE 'Remote Control (requires|cannot start|is disabled|is not available)|verify Remote Control|/login' Hm/o` -> 0
  - (c) uid + slice of the RC client: `for p in $(cat /sys/fs/cgroup/agi.slice/agi-post@${P}.service/cgroup.procs); do echo "$(cat /proc/$p/comm) $(stat -c %U /proc/$p)"; done | grep -c '^claude agi-director-general-5$'` -> 1 (comm + owner, never argv)
  - (d) **APP PROOF (the owner reads)**: in the Claude app / claude.ai/code session list, a session named `director-general-5` is listed and live; the owner types `app-ping` there and `sudo grep -ac app-ping Hm/o` -> >= 1. The owner answers: **DG5 visible in the app: yes / no.**
  - (e) REPORT row: uid binding = A's own file (600 A), own refresh family (R8a `differs`); machine = A's own RC machine id (inferred); network = the box's one egress, not separable (inferred).
  - UNDO: T1 (the session leaves the app list when the unit stops).
- **R17 NEW: the pi-free kid proves CCCC** (not a root act; DG3 orders DG5 in one line, so the kid runs INSIDE the unit/slice):
  DG5 runs `agi-kid cccc-probe "<one small committed edit>"` (uses R7's key).
  - PROOF: `sudo test -s Hm/k/cccc-probe/.brief && echo brief` (SessionStart via cccc) · `git -C M log -1 --format=%G? kids/cccc-probe` -> `G` (Stop -> turn_end -> agi-turn) · `ls M/.agi/sessions/rotations | grep -c '^cccc-probe\.'` -> >= 1 · `sudo grep -c '/k/cccc-probe/' Hm/track` -> >= 1 (traced under DG5's strace = in the cgroup)
  - UNDO: `git -C M worktree remove --force Hm/k/cccc-probe/t` (after T5c, as the owner); branch kids/cccc-probe is kept for the master.
- **R-MG** (memguard patch): no longer needed for DG5 — the live memguard protects comm `claude` (-900) for any uid (measured: PROTECT_COMM). The kid's pi gets +500 like today's pi workers. Stays BANKED, optional.

### 7 · Rollback (ONE command) — the engine string changes
```
cd /data/work/agi && python3 extensions/agi/bin/write.py config:posts 'sub {"name": "director-general-5", "engine": {"v": 4, "harness": "claude-code", "model": "claude-sonnet-5-5", "effort": "high", "trunk": "local-maxxing/season2/main", "seeds": "doc:unified-director-brief,doc:unified-head,goal:g7.16.1", "rotate_pct": 47, "kid_model": "stealth/space-bunny-alpha"}, => {"name": "director-general-5",' --actor belam --role prime_director && sudo systemctl stop agi-post@${P} && sudo rm -f /run/systemd/system/multi-user.target.wants/agi-post@${P}.service && sudo systemctl daemon-reload && python3 extensions/agi/bin/rotate.py stand-up --post director-general-5
```

### 8 · Teardown delta
- **T5** adds, after (a): `git -C M worktree prune` (kid trees under Hm/k go with T7); kids/* branches are handed back by (c) like posts/*.
- **T6 [KEY]**: first R8a's UNDO (`claude auth logout` as A), then `sudo shred -u /var/lib/agi/director-general-5.env Hm/.claude/.credentials.json Hm/.claude.json Hm/.config/agi/scrub-denylist.json`.
- T7 also removes Hm/k (kid homes, their .pi tool downloads).

### 9 · Parity delta (base: 55 rows, 51 matched-or-better)
| # | was | v4c | why / proof change |
|---|---|---|---|
| 4 harness+model | MATCH (pi) | MATCH | h.conf `H=claude --remote-control director-general-5 --model claude-sonnet-5-5 ...` (measured); proof greps `model claude-sonnet-5-5` |
| 5 effort | MATCH | MATCH | `--effort high`; proof greps `effort high` |
| 6 settings | MATCH | MATCH | keys `["hooks","skipDangerousModePermissionPrompt"]` (measured); hooks unchanged |
| 7 brief | EXCEEDS | **MATCH** | claude gets the ranked list + STARTUP (B=0); pi inlined node bodies |
| 9 meter | MATCH | MATCH | CC path: transcript_path tail (v4b T6: 470015 tokens -> out-line) |
| 10 rotation | MATCH | MATCH (inferred) | `kill $PPID` from CC's Bash tool = claude (inferred); proof counts `Hm/.claude/projects/*/*.jsonl` +1 |
| 16 wake | EXCEEDS | **MATCH** | typed mail into `i` (= today's typed nudge, send.py's pause rule); measured 1 append -> 1 line, rewrite -> 0 |
| 30 dispatch kids | SHORT | SHORT (partial) | pi-free kids via agi-kid on the unit's ONE key; per-spawn keys still need the broker (stage 3) |
| 39 live view | MATCH | **EXCEEDS** | the pane `o` AND the owner's app (read + type), R16'(d) |
| 43 memguard | SHORT | **MATCH** | comm `claude` is protected -900 for any uid (measured); R-MG not needed for DG5 |
| 53 skills | MATCH | MATCH | CC loads `~/t/.claude/skills` natively; proof `AS ls ~/t/.claude/skills | grep -c agi-` |
| 54 pane hygiene | MATCH | MATCH | o header `agi-run` (measured, RC name absent); RC line carries a URL: o stays 600 + owner ACL |
| 55 CC as non-owner uid | MATCH (cond. R16) | MATCH (cond. R8a + R16') | the post IS claude; own login, own token family |
| 56 NEW Remote Control in the app | — | MATCH (cond. R16') | today's posts run `--remote-control <name>`; R16'(b)(c)(d) |
| 57 NEW pi-free kid on CCCC | — | MATCH (cond. R17) | both harnesses proven in one post: R17 |
| CC1-CC3 | on DG5 | on the kid | native on DG5; the CCCC proofs move to R17 |
**Count, the original 55: 52 matched-or-better** (EXCEEDS 6: 12, 19, 26, 27, 39, 41 · MATCH 46), **short 3**: 18 (seat-key rotation),
30 (broker; partial now), 33 (detached workflows). With the 2 new rows: 54 of 57, rows 55-57 conditional on the live proofs.

### 10 · Risks (new or changed) and the open calls kept
- **RC1** the app can drive DG5 (prompts typed in the app run with bypassPermissions) — the same surface as today's RC posts.
- **RC2** RC refuses silently-ish if flags are unreachable / an API key is set / the token is inference-only: P0.8, R7 proof, R16'(b).
- **RC3** an unnamed session would show the HOSTNAME in the app: the name is always passed (agi-project).
- **K1 closed** by the manual login (own refresh family). **K1'** A holds a full-scope token of the owner's account (600, A; root and DG5's own Bash tool can read it — as today's posts can read the owner's).
- **U1** DG5 draws on the owner's subscription limits shared by every CC post (as today).
- **S2** strace -f on claude: heavier than on pi, and the kid's pi is traced too (track grows faster; base P1).
- **Q1** typed mail while claude is busy: queued by CC (inferred; today's nudge relies on it); `kill $PPID` reaching claude: inferred. Both are live proofs (rows 10, 16).
- **KID** the kid shares DG5's uid, ssh key, cgroup and ONE zero-USD key; its identity is the branch kids/<k> + its rotation record (named, not faked); its first provider call came after 30-66 s in scratch (brief walk + pi's own fd/rg fetch from GitHub into Hm/k/<k>/.pi).
- **B0** engine at exactly 16,384 B: any 2.5 fix must trim elsewhere; agi-seed.service is out until stage 3 (a reboot leaves DG5 down, as in v4b).
- **Open calls (NOT decided here)**: copied-creds shared refresh token — superseded by the owner's 04:49Z manual login (belam confirms) · agi.slice + user@ overcommit G1 (accept for ONE post) · memguard R-MG (now optional) · key broker = stage 3 · the old-engine DG5 scope stopped by SM or belam (P0.2) · C1/C2 = Prime landings.

### 11 · Act count v4c
Root acts: R1 R2 R3 R4 R4b R5 R6 R7 R9 R10 R11 R12 R13 R14 R15 = 15 sudo acts, + R8a (OWNER, sudo -u), R8b (sudo -u, no root write),
R16' (proofs), R17 (DG5's own turn). MAIN: C1-C4 (C4's object changed). [KEY]: R7 R8a R10-seat-key R16' T6.

## V-L1 (DG3) -- ML-KEM-768 for the council's §P.7 escrow wrap (owner GO 05:35Z, verbatim on goal:g7.16.1.11 @c53548ae2)
Terms: user-level, no root, no apt, the smallest MAINTAINED route doing real ML-KEM-768 (FIPS 203), proved by round-trip + the hybrid wrap on a throwaway share. Done 05:4xZ by an Opus 5.5 subagent of DG3; proof re-run by DG3 (rc 0, RESULT: PASS).

| | |
|---|---|
| route | Node's built-in node:crypto -- NOTHING INSTALLED |
| package + version | node v24.21.0 (/usr/local/bin/node) with its bundled OpenSSL 3.5.8: generateKeyPairSync('ml-kem-768'), crypto.encapsulate / decapsulate; X25519, HKDF-SHA256, ChaCha20-Poly1305 from the same module |
| bytes on disk | 0 (no install location created) |
| why | the smallest route is the one already present and maintained (Node 24 LTS; OpenSSL 3.5 = OpenSSL's LTS line, FIPS 203 final, not draft Kyber) |
| candidates checked | system OpenSSL 3.0.13: no ML-KEM (root to upgrade) · system python cryptography 41.0.7: no mlkem (50.0.2 has it: a user venv, 4.75 MB wheel + cffi) · @noble/post-quantum 0.7.1 (745 KB) + curves/hashes/ciphers (~2.8 MB more) · liboqs-python 0.16.0.1: needs the C library built |
| KDF binding | HKDF-SHA256, salt empty, info "agi-escrow-hybrid-v1", IKM = ss_mlkem ‖ ss_x25519 ‖ ct_mlkem ‖ eph_x25519_pub ‖ rcpt_x25519_pub |
| AEAD | ChaCha20-Poly1305, random 12 B nonce, AAD = label ‖ eph_pub ‖ ct_mlkem; envelope = eph_pub(32) ‖ ct(1088) ‖ nonce(12) ‖ tag(16) ‖ body |
| caveats | escrow tooling must use node:crypto, never shell openssl (3.0.13 here) · ML-KEM is as current as Node's bundled OpenSSL · no published KAT run · implicit rejection: a tampered ML-KEM ct yields a pseudo-random secret; the AEAD tag is what refuses it (by design) · Python callers would need the cryptography >= 50 venv |

Proof output (DG3 re-run, secret prefixes masked):
```
node v24.21.0 openssl 3.5.8
[1] ML-KEM-768 ek=1184 B ct=1088 B ss=32 B equal=true
[2] hybrid wrap: share=32 B envelope=1180 B (32 eph + 1088 ct + 12 nonce + 16 tag + 32 body) unwrap_equal=true
[3] flip byte in mlkem_ct / eph_pub / nonce / tag / aead_body, and a wrong x25519 key: all 6 rejected (Unsupported state or unable to authenticate data)
RESULT: PASS
```
The proof script (4,424 B, sha256 prefix 5461de863c829243), byte-exact; run with `node proof.mjs`; keys are throwaway, in memory only:
~~~~~javascript
// V-L1 proof (goal:g7.16.1.11): hybrid X25519 + ML-KEM-768 escrow wrap, Node built-in crypto only.
// All keys are THROWAWAY, in memory only; nothing is written to disk. Only lengths / short hex prefixes print.
import crypto from 'node:crypto';

const LABEL = Buffer.from('agi-escrow-hybrid-v1');            // domain separation
const hex8 = (b) => Buffer.from(b).toString('hex').slice(0, 16) + '...';
const x25519Raw = (pub) => Buffer.from(pub.export({ format: 'jwk' }).x, 'base64url');

console.log('node', process.version, 'openssl', process.versions.openssl);

// (1) ML-KEM-768 keygen -> encapsulate -> decapsulate
const kem = crypto.generateKeyPairSync('ml-kem-768');
const ek = kem.publicKey.export({ format: 'raw-public' });
const { sharedKey: ssA, ciphertext: ct0 } = crypto.encapsulate(kem.publicKey);
const ssB = crypto.decapsulate(kem.privateKey, ct0);
console.log(`[1] ML-KEM-768 ek=${ek.length} B ct=${ct0.length} B ss=${ssA.length} B equal=${crypto.timingSafeEqual(ssA, ssB)} ss~${hex8(ssA)}`);

// Recipient (escrow holder) long-term keys: X25519 static + ML-KEM-768
const rcptX = crypto.generateKeyPairSync('x25519');
const rcptK = kem;

function deriveKey(ssK, ssX, ctK, ephPub, rcptXPub) {
  // KDF binds: ss_mlkem || ss_x25519 || ct_mlkem || eph_x25519_pub || rcpt_x25519_pub ; info = LABEL
  const ikm = Buffer.concat([ssK, ssX, ctK, ephPub, rcptXPub]);
  return Buffer.from(crypto.hkdfSync('sha256', ikm, Buffer.alloc(0), LABEL, 32));
}

// Envelope: eph_pub(32) || ct_mlkem(1088) || nonce(12) || tag(16) || aead_ct(len(share))
function wrap(share, rcptXPub, rcptEk) {
  const eph = crypto.generateKeyPairSync('x25519');
  const ephPub = x25519Raw(eph.publicKey);
  const ssX = crypto.diffieHellman({ privateKey: eph.privateKey, publicKey: rcptXPub });
  const { sharedKey: ssK, ciphertext: ctK } = crypto.encapsulate(rcptEk);
  const key = deriveKey(ssK, ssX, ctK, ephPub, x25519Raw(rcptXPub));
  const nonce = crypto.randomBytes(12);
  const c = crypto.createCipheriv('chacha20-poly1305', key, nonce, { authTagLength: 16 });
  c.setAAD(Buffer.concat([LABEL, ephPub, ctK]));
  const body = Buffer.concat([c.update(share), c.final()]);
  return Buffer.concat([ephPub, ctK, nonce, c.getAuthTag(), body]);
}

function unwrap(env, rcptXPriv, rcptXPub, rcptDk) {
  const ephPub = env.subarray(0, 32), ctK = env.subarray(32, 1120);
  const nonce = env.subarray(1120, 1132), tag = env.subarray(1132, 1148), body = env.subarray(1148);
  const ephKey = crypto.createPublicKey({ key: { kty: 'OKP', crv: 'X25519', x: ephPub.toString('base64url') }, format: 'jwk' });
  const ssX = crypto.diffieHellman({ privateKey: rcptXPriv, publicKey: ephKey });
  const ssK = crypto.decapsulate(rcptDk, ctK);           // implicit rejection: bad ct -> pseudo-random ss
  const key = deriveKey(ssK, ssX, ctK, ephPub, x25519Raw(rcptXPub));
  const d = crypto.createDecipheriv('chacha20-poly1305', key, nonce, { authTagLength: 16 });
  d.setAAD(Buffer.concat([LABEL, ephPub, ctK]));
  d.setAuthTag(tag);
  return Buffer.concat([d.update(body), d.final()]);    // throws on tag mismatch
}

// (2) hybrid wrap / unwrap of a throwaway 32-byte share
const share = crypto.randomBytes(32);
const env = wrap(share, rcptX.publicKey, rcptK.publicKey);
const back = unwrap(env, rcptX.privateKey, rcptX.publicKey, rcptK.privateKey);
console.log(`[2] hybrid wrap: share=${share.length} B envelope=${env.length} B (32 eph + 1088 ct + 12 nonce + 16 tag + 32 body) unwrap_equal=${crypto.timingSafeEqual(share, back)} share~${hex8(share)}`);

// (3) negatives: one flipped byte in each region must fail to unwrap
let allFail = true;
for (const [name, off] of [['mlkem_ct', 32 + 500], ['eph_pub', 5], ['nonce', 1125], ['tag', 1140], ['aead_body', 1150]]) {
  const bad = Buffer.from(env); bad[off] ^= 0x01;
  let ok;
  try { unwrap(bad, rcptX.privateKey, rcptX.publicKey, rcptK.privateKey); ok = 'UNWRAPPED (BAD)'; allFail = false; }
  catch (e) { ok = `rejected (${e.message})`; }
  console.log(`[3] flip byte in ${name.padEnd(9)} @${off}: ${ok}`);
}
// wrong recipient X25519 key must also fail
try { unwrap(env, crypto.generateKeyPairSync('x25519').privateKey, rcptX.publicKey, rcptK.privateKey); allFail = false; console.log('[3] wrong x25519 key: UNWRAPPED (BAD)'); }
catch (e) { console.log(`[3] wrong x25519 key        : rejected (${e.message})`); }
console.log(allFail ? 'RESULT: PASS' : 'RESULT: FAIL');
process.exit(allFail ? 0 : 1);
~~~~~

## PHASE C RUN (DG3, 05:2xZ-08:4xZ 10-01): DG5 UP on engine v4c, PI-FREE (owner night plan: no owner login tonight)
| act | result |
|---|---|
| P0.1-P0.5 + P0.7 | PASS (before-values in /tmp/agi-stage25/v4c/before) |
| R1 R2 R3 | PASS (R3's rc-help as nobody printed 'must be logged in': equivalent) |
| C1 | belam e1e0dbaaf (config:engine = v4c byte-exact) |
| C2 | belam aa2f2e28a (rotate.py refuses an engine-owned row; built by DG3's Opus subagent bf5fb95c82) |
| C4 | belam 81ed274fc (the DG5 row engine {v 4, harness pi-free, model stealth/space-bunny-alpha, effort medium}; the ring gate refuses a director on another row) |
| pre-R4 | all 24 pieces at HEAD == /tmp/agi-stage25/v4c/pieces (sect | cmp) |
| R4 + R4b | projected: wants = agi-post@${P}.service (agi-project.path removed); h.conf H=pi --provider openrouter, O=MAIN |
| R5 R6 R7 | user + groups (agi existed: belam's post users); home 755; ONE per-spawn zero-USD key, 600 root, never printed |
| R8 R16 | SKIPPED tonight (pi-free: no Claude credential) |
| R9 R10 R11 | privacy guard for the post; scoped ACLs (refs writable, .git/config + hooks NOT); polkit rule cmp-equal |
| R12 R13 | system agi.slice values == the user agi.slice (from config:guard); daemon-reload; 2 unit fragments |
| GATE N4 | PASS: Slice agi.slice · MemoryHigh 9,261,023,232 / MemoryMax 10,290,724,864 (finite, == user slice) · ManagedOOMMemoryPressure kill, limit 40% · systemd-analyze verify 0 lines · 0 old DG5 scopes |
| R14 START | active, NRestarts 0, cgroup /agi.slice/agi-post@${P}.service, oomd watches agi.slice; processes as A: pi, script, agi-brief, agi-track/strace, sh; worktree branch posts/director-general-5; i = 600 fifo, o = 600 file; 0 dubious ownership |
| R15 | the owner reads the pane without sudo (300 B) |
| FIRST TURN | pi working; the first turn commit on posts/director-general-5 (adds .agi/keys/director-general-5), SIGNED: git verify-commit as A = Good ed25519 signature (%G? G); MAIN cannot verify it (no allowedSignersFile in MAIN's config) |
| SEEN BY THE MAP | the map script (DG2's hypothesis) is not landed; its inputs show DG5: git worktree list (1) and git log --graph --all (posts/director-general-5) |
UNDO = §3 ROLLBACK / §4 teardown; units live in /run (gone at reboot).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PHASE A' (v4c): DG5 moves from pi-free to Claude Code Sonnet 5.5 with Remote Control (owner 04:40Z) and the owner logs DG5's user in by hand (04:49Z), so the credential copy R8 becomes R8a (owner login) + R8b (onboarding/trust); RC proof R16' + app proof; R17 = the ONE pi-free kid on CCCC; engine-v4 at 16,384/16,384 B (agi-seed.service dropped for stage 3); parity 52/55 matched-or-better + rows 56-57 pending live proof. First Phase A' run died at the 04:45Z rotation (only assemble.py touched); this is the relaunch.
<!-- THOUGHT:END -->
