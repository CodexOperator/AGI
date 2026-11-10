---
id: goal:g7.31.1.2
mint_id: fb589b44ed9f46eaa6c0b4c4323bba0f
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.9
edited_by: director-general-1
goal_id: G7.31.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 67eb4b9e47d1ff69
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - adapter
  - tmux
  - pane
thought_session: magic-pane-2026-09-21
title: "G7.31.1.2: Durable named tmux pane restart/reattach hold"
town: core
---
# goal:g7.31.1.2

## Why this exists

**Parent `goal:g7.31.1`.** Falsifiers on the parent were multi-headed. This leaf owns **durable named tmux pane hold** — kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name the seat keeps.

## Target end-state

- Adapter `restart` (or documented true impossibility) re-attaches to the same named tmux pane.
- Pane name is stable across adapter restarts; seat occupation is visible independently of process pid churn.
- Precursor to magic pane — durable hold first; magic UX later.

## Invariants

- One named pane per seat; no anonymous fire-and-forget for persistent grok seats.
- Restart goes through the same adapter/template seam as first spawn (`goal:g7.27` / `goal:g7.28`).
- Measured CLI argv shape is OOS here (`goal:g7.31.1.1`).
- Does not special-case `grok` inside `dispatch.py` / `rotate.py`.

## Falsifier

1. Kill the seat process; `restart` (or persistent-dispatch restart) reattaches to the **same** tmux pane name; `tmux list-panes` / capture shows the seat still there.

PROVISIONAL and UNMEASURED, ACT 2c (council: alive [decision] 11-06 19:49:54Z (A)(3) and 11-09 10:56:03Z; none of this is ever read as a pass of 1, which only the live kill + reattach run decides, on the owner's or belam's GO):
- grok-bot's resume proof is `session_id` (grok-bot.toml `[session] resume_proof`): heal resumes when the row carries an id, and logs 'resume proof PROVISIONAL (session_id present; UNMEASURED)' on every use.
- The session store's path is UNREAD: the help names the grok home `~/.grok` (doc:grok-bot-help-measured :175) and that sessions live 'under the target session directory' (:140-141), but no store was seen (belam's `~/.grok` read empty, 11-09). grok-bot.toml declares no `[session] store`, so heal's pre-launch read is UNREAD on every resume and the resume is launched.
- heal reads as uid `agi-reaper` (crons.md, `heal.py watch`), not the seat's uid: a store under the seat's home may be unreadable to it, and that also reads UNREAD, never 'absent'.
- A failed -r that keeps its process up (so the join reads the dead id back from its own argv) is invisible to the join alone; the first live run measures it once.
- A failed -r (2c-3, council 3/3 11:22Z-11:25Z 11-09, DG1's pick (b)): heal reads the pane join at the END of a 30 s window after its -r launch. `absent` or `no-pane` (the common exit: the launch-file bash ends with the harness and the window closes; the repo sets no remain-on-exit, the live tmux server's setting NOT read) = FAILED: the id leaves the row, the row keeps its dead pid (heal scans only pid > 0), NO in-pass fresh launch; the next heal cycle's ordinary spawn is the fresh launch (2b's new uuid, read back by the after-join pass). `ambiguous`, or a different pid at the end than at the launch = the id kept, pid EMPTY, nothing launched. On `absent` the failed window is still OPEN, so the row's window is written EMPTY (2c-4, R6): with its @id the next pass's (1b) would read the seat alive, a silent stall; empty, the next pass reaches _recover_seat and its same-name refusal, loud each pass, until the window closes (no window is killed). LIMIT (aio 11:46:05Z): that refusal holds for a NON-chain seat (it respawns under its own name); a chain seat (role prime_director) respawns as base-<gen+1>, a NEW name, so it would pass the refusal and open a SECOND window beside the failed one. Latent today: the one prime_director row is belam's, on claude-code, so the session_id path never reaches it. So a chain seat KEEPS its @id on an absent read (2c-5, sp's NIT): fail-closed, a stall, never a second window; its FAILED line says heal reads it alive until that window closes (alive's addition), so the stall is named once. Before any chain seat runs on a session_id-proof harness, it needs its own open-window check. The same-name refusal logs its own line each pass (2c-5, alive's NIT 1). NAMED, not changed (alive's NIT 2): a failed -r reads respawned False, so the pass's one launch slot stays unspent although a launch happened; a second seat can launch in the same pass. The dead id and what the join read are in heal's crash-recovery record, `resume_failed`; from the seat name: `python3 extensions/agi/bin/heal.py resume-failed --post <seat>` (2c-5; `rotate.py status --record` skips crash-recovery records, so it never shows one). A refusal pass that rewrites the deduped detected record carries the prior `resume_failed` over (2c-5); the heal log's FAILED line keeps the id too. A row cell for it is one banked line for the owner's batch (council 10:56:03Z (C)). Which of no-pane / absent a live failed -r gives is read by the first live run.
- NOT YET (alive's NIT 1, at the touch that declares a `[session] store`): `~` in a store path expands in the home of heal's uid, not the seat's; resolve it against the seat's home then, with a row.

## F1 script: the throwaway run

OWNER (c:175d1f09df76, 03:56:36Z 11-10, via belam): "you are go for grok-bot check and integration pass I can log in as needed/when needed". Council [decision] alive 04:09:00Z 11-10, road (S), 3/3: F1 runs on a THROWAWAY grok seat under terms T1-T3; this script is that run. ORDER (belam 04:10Z, corrected 04:11Z): it runs as uid agi-plan-master (971), before any posts.md row names plan-master; the host side is the owner's one `grok login` as that uid, then the run. Nothing else starts before the script.

- ROUTE, named (T1): the first spawn is `rotate.py stand-up` (the one stand-up verb; fresh, 2b's `-s` uuid). Each restart is heal: `heal.py watch --root R --once`, i.e. `_watch_seats` -> `_recover_seat` -> `-r <row session_id>` -> the 30 s pane-join window. R is a throwaway root: the trunk's bytes at the given sha, its own git repo with no remote, its `sessions/` emptied, and posts.md cut to ONE scratch row (`f1-grok`, harness grok-bot, role director, recover true). Every heal pass prints its number, rc and heal's uid. Section 5 lists each 2c branch as REACHED or NOT RUN from heal's own log; a branch it does not reach is NOT RUN in the CLOSE, never a pass.
- uid (T2): heal's uid reads MEASURED only as agi-reaper (the production uid). Run as agi-plan-master, the line reads NOT MEASURED. A hand spawn (no heal) would leave the three UNMEASURED reads NOT RUN, and the goal does not close on them.
- READS (T3): one line per read; an empty read prints READ NOTHING and fails the run (rc 1). The reads are: the pane before/after; the seat pid before/after (ENFORCED, alive's TERM 04:23:59Z: an after-pid that is empty, 0, the same, or not alive under kill -0 sets FAIL and the line names which; a killed pid still ALIVE fails too; and 'yes' needs a before-pid > 0 whose kill read 'gone', so a run where no kill ran never reads as a proof, self-perpetuating 04:41:00Z); the row session_id before/after; the capture's byte count (non-whitespace; 0 = READ NOTHING); the comm and cwd grok runs under; its -s/-r argv; the session store (paths only, under the uid's home); the failed -r's join kind and whether grok stays up on a dead id; and the `resume-failed` route's rc and line (`--post` first, `--seat` if `--post` is not yet on the trunk; a last rc > 1 fails the run). Section 4's dead-id write is checked as row session_id == the dead id; if the write fails or the check misses, the run fails and section 4 stops (sp 04:26:28Z). The resume proof is a MEASURED line beside the reads, never one of them.
- MEASURED by DG1's dry setup (11-10, F1_SETUP_ONLY=1, uid 979, trunk a23333068e): config.json `harnesses.grok-bot.bin` = `~/.npm-global/bin/grok-bot` REFUSES on this box (the adapter raises FileNotFoundError: no such file in the uid's home), so a live launch would die at its first spawn. The script exports the adapter's own override, `GROK_BOT_BIN`, from PATH (`/usr/local/bin/grok-bot` -> grok 1.0.46) and prints it. The config cell is a finding for the plan-master leaf (an engine unit hits the same refusal). Also measured: the dry build is `rotate.py launch-wrapper --seat f1-grok -- grok-bot --model grok-4 -s <uuid> <prompt>` (rc 0), and one heal pass in R scans 0 pid rows and touches nothing outside R.

- THE CREDENTIAL (all-is-one [word] 04:12:03Z + 04:25:21Z, self-perpetuating [note] 04:13:14Z, SM [review] R1 04:22:55Z, 11-10; section 0 runs after the setup and BEFORE the stand-up; the listing is uncapped, and a find error fails the run): the token is the owner's xAI account, and the home is 755. `f1.sh mark` touches a marker BEFORE the login. The run's section 0 lists every file under the WHOLE home whose status changed after that marker (`find -cnewer`, which no utimes call can set back; sp 04:28:55Z), each with its mode. An empty or failed mode read is READ NOTHING and fails the run, never 'owner-only'. Any file with a group or other bit is cleared with `chmod go-rwx` (the owner's bits kept; aio 04:29:35Z) before anything launches, and the line names it with its mode after. 0 files = READ NOTHING: the token is stored outside the home, UNREAD and never 'safe', and the run stops (rc 1) until it is found. The script grants heal's uid no read; if T2 shows agi-reaper needs the session store, that grant covers the store alone, never a token file.

RUN (belam, on encryption-town), in this order. The mktemp path must be readable to uid 971: a /tmp mktemp file at 644 is; a file under a 700 scratch dir is not (belam 08:38Z 11-10). The scratch row's model is `F1_MODEL`, default grok-4.6, the box's grok default; `grok models` on this box lists only grok-4.6 and grok-4.5 (belam 08:4xZ). A setup-only pass as the uid comes first (SM NIT 2: whether 971 can read SRC is UNMEASURED, and a refusal there should cost no login). Then the marker, then the owner's login, then the run. The script goes to a mktemp path (SM NIT 1: never a fixed name in /tmp):
```
F=$(mktemp) && sed -n '/^```bash f1.sh$/,/^```$/p' .agi/nodes/goal/g7.31.1.2.md | sed '1d;$d' > "$F" && chmod 644 "$F"
sudo -u agi-plan-master -H env AGI_BOX=encryption-town SHELL=/bin/bash F1_SETUP_ONLY=1 bash "$F" <trunk sha>
sudo -u agi-plan-master -H bash "$F" mark
  (the owner's grok login as agi-plan-master)
sudo -u agi-plan-master -H env AGI_BOX=encryption-town SHELL=/bin/bash bash "$F" <trunk sha>
```
The output stays in `~agi-plan-master/f1-<stamp>/f1.out` with heal.log beside it. Its readings come back to this leaf, and the CLOSE cites them.

```bash f1.sh
#!/usr/bin/env bash
# goal:g7.31.1.2 F1 -- the owner's 'grok-bot check' (c:175d1f09df76), on a THROWAWAY grok seat.
# Council [decision] alive 04:09:00Z 11-10, T1-T3. Run ON encryption-town, AS agi-plan-master, after the
# owner's one `grok login` as that uid (belam asks the owner at that moment):
#   sudo -u agi-plan-master -H env AGI_BOX=encryption-town SHELL=/bin/bash bash f1.sh <trunk-sha> [src-repo]
# Nothing here is a pass. One line per read; an EMPTY read prints READ NOTHING and fails the run (rc 1).
# The resume proof is a MEASURED line beside the reads, never part of them.
# Order (the leaf's RUN block): F1_SETUP_ONLY=1 as the uid (a refusal costs no login), then `f1.sh mark`, then the
# owner's login, then the run.
set -u
LM=$HOME/.f1-login-marker
if [ "${1-}" = mark ]; then touch "$LM" && echo "login marker set: $(stat -c '%y' "$LM")"; exit 0; fi
TIP=${1:?usage: f1.sh mark | f1.sh <trunk-sha> [src-repo]}; SRC=${2:-/data/work/agi}
SEAT=f1-grok; STAMP=$(date -u +%Y%m%dT%H%M%SZ); R=$HOME/f1-$STAMP; FAIL=0
mkdir -p "$R"; exec > >(tee "$R/f1.out") 2>&1
rd() { if [ -n "${2-}" ]; then echo "READ $1: $2"; else echo "READ $1: READ NOTHING"; FAIL=1; fi; }
row() { (cd "$R/extensions/agi/bin" && python3 -c "import sys,rotate
r=[x for x in rotate._load_seats(__import__('pathlib').Path(sys.argv[1]+'/.agi')) if x.get('name')==sys.argv[2]]
print(r[0].get(sys.argv[3],'') if r else '')" "$R" "$SEAT" "$1"); }
panes() { tmux list-windows -a -F '#{session_name}:#{window_id} #{window_name} pane_pid=#{pane_pid}' 2>/dev/null | grep -F "$SEAT" || true; }
HEALN=0; KILLED=
heal() { HEALN=$((HEALN+1)); local a; a=$(wc -l < "$AGI_REAPER_LOG" 2>/dev/null || echo 0)
  echo "HEAL PASS $HEALN: heal.py watch --root $R --once (uid $(id -un))"
  (cd "$R" && python3 extensions/agi/bin/heal.py watch --root "$R" --once); echo "HEAL PASS $HEALN rc $?"
  tail -n +"$((a+1))" "$AGI_REAPER_LOG" 2>/dev/null | grep -F -e "$SEAT" -e 'seat-dead scan' | sed "s/^/  heal[$HEALN] /"; }
proc() { local p=$1; rd "$2 comm (heal finds a seat by comm + cwd)" "$(ps -o comm= -p "$p" 2>/dev/null)"
  rd "$2 cwd" "$(readlink "/proc/$p/cwd" 2>/dev/null)"
  rd "$2 argv -s/-r" "$(tr '\0' '\n' < "/proc/$p/cmdline" 2>/dev/null | grep -A1 -x -e -s -e -r | paste -sd' ')"; }
killseat() { local p=$1; kill -TERM "$p" 2>/dev/null; for _ in $(seq 20); do kill -0 "$p" 2>/dev/null || break; sleep 1; done
  kill -0 "$p" 2>/dev/null && { kill -KILL "$p"; sleep 2; }; if kill -0 "$p" 2>/dev/null; then echo "READ pid $p after the kill: FAIL: ALIVE"; FAIL=1; else echo "READ pid $p after the kill: gone"; KILLED=$p; fi; }

echo "== F1 goal:g7.31.1.2 (c:175d1f09df76) $STAMP; R=$R (a throwaway root: its own repo, no remote, ONE row)"
rd "uid" "$(id -un) ($(id -u))"; rd "HOME" "$HOME"; rd "SHELL (tmux's default-shell; the uid's login shell is nologin)" "${SHELL-}"
rd "AGI_BOX" "${AGI_BOX-}"; rd "grok-bot on PATH" "$(command -v grok-bot)"
# config.json harnesses.grok-bot.bin = '~/.npm-global/bin/grok-bot' REFUSES on this box (no such file in any post home;
# DG1 dry build 11-10): the adapter's own override names the PATH binary, read here, never guessed.
export GROK_BOT_BIN=${GROK_BOT_BIN:-$(command -v grok-bot)}; rd "GROK_BOT_BIN (the adapter override)" "$GROK_BOT_BIN";
# the scratch row's model (belam 08:4xZ 11-10: grok models on this box lists only grok-4.6 (default) and grok-4.5)
F1_MODEL=${F1_MODEL:-grok-4.6}; rd "F1_MODEL (the scratch row's model)" "$F1_MODEL"; rd "grok-bot --version" "$(grok-bot --version 2>&1 | head -1)"
if [ "$(id -un)" = agi-reaper ]; then echo "MEASURED heal uid: agi-reaper (production's)"
else echo "NOT MEASURED heal uid: heal runs here as $(id -un), production heal as agi-reaper; every 'store readable to heal' read below is $(id -un)'s"; fi

# --- the throwaway root: the trunk's bytes at TIP, its own repo, posts.md cut to ONE scratch row
git -c safe.directory="$SRC" -C "$SRC" archive "$TIP" | tar -x -C "$R" || { echo "ABORT: archive of $TIP from $SRC failed"; exit 1; }
# R's sessions/ (old rotation records, rounds) out: heal's late-reap and round passes in R must see the scratch seat only
rm -rf "$R/.agi/sessions"; mkdir -p "$R/.agi/sessions"
export AGI_REAPER_LOG=$R/heal.log; : > "$AGI_REAPER_LOG"
python3 - "$R" "$SEAT" "${AGI_BOX-}" "$F1_MODEL" <<'PY'
import json, re, sys
from pathlib import Path
R, seat, box, model = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
p = R / ".agi/nodes/.geometry/posts.md"; t = p.read_text()
row = {"name": seat, "role": "director", "tier": 1, "harness": "grok-bot", "model": model, "effort": "",
       "settings": "", "session_kind": "", "personality_ref": "", "handoff_file": "", "pin_ref": "",
       "rotated_by": seat, "template": "doc:f1-scratch-brief", "worktree": "", "session_ref": "",
       "session_id": "", "window": "", "town": "core", "box": box, "pubkey": "", "pid": 0,
       "generation": 0, "recover": True}
t, n = re.subn(r"(?m)^posts:\n(?:  - .*\n)+", "posts:\n  - " + json.dumps(row) + "\n", t)
assert n == 1, "posts: block not found"
p.write_text(t)
txt = ("F1 THROWAWAY seat (goal:g7.31.1.2). Reply with the one word: ready. Run NO tool, read no file. "
       "When asked to continue, reply: ready.")
for nid, slug in (("doc:f1-scratch-brief", "f1-scratch-brief"), (f"doc:card-{seat}", f"card-{seat}")):
    (R / f".agi/nodes/doc/{slug}.md").write_text(
        f"---\nid: {nid}\ntype: doc\nparents:\n  - goal:g7.31.1.2\ntitle: F1 scratch\n---\n{txt}\n")
PY
[ $? = 0 ] || { echo "ABORT: the scratch row write failed"; exit 1; }
git -C "$R" init -q && git -C "$R" -c user.name=f1 -c user.email=f1@local add -A && \
  git -C "$R" -c user.name=f1 -c user.email=f1@local commit -qm "F1 throwaway root at $TIP" || { echo "ABORT: R repo"; exit 1; }
NR=$(cd "$R/extensions/agi/bin" && python3 -c "import rotate,sys;print(len(rotate._load_seats(__import__('pathlib').Path(sys.argv[1]+'/.agi'))))" "$R")
rd "R's rows (must be 1)" "$( [ "$NR" = 1 ] && echo "1: $(row harness) $(row box)")"
# alive NIT 08:44:36Z: the stand-up builds its launch from the ROW's model (rotate.py :5555), so read it back from the row
RM=$(row model); if [ "$RM" = "$F1_MODEL" ]; then echo "READ the row's model: $RM"; else echo "READ the row's model: FAIL: '${RM:-empty}', not $F1_MODEL"; FAIL=1; fi
rd "the launch argv heal builds (dry, prompt elided)" "$(cd "$R/extensions/agi/bin" && python3 -c "import rotate,re,sys
from pathlib import Path
rc,c=rotate.spawn_window(name=sys.argv[2],tier='director',prompt_file=None,model=sys.argv[3],effort='',settings=rotate._normalize_settings(''),root=Path(sys.argv[1]+'/.agi'),dry_run=True,seat=sys.argv[2],harness='grok-bot',resume=None,card_file=sys.argv[1]+'/.agi/nodes/doc/card-'+sys.argv[2]+'.md')
print('rc', rc, (c or '').split(' --',1)[-1].split(\" '\",1)[0], '<PROMPT>')" "$R" "$SEAT" "$RM" 2>&1 | tail -1)"
[ "${F1_SETUP_ONLY-}" = 1 ] && { echo "== setup only (F1_SETUP_ONLY=1): nothing launched; FAIL=$FAIL"; exit $FAIL; }
# --- 0. the owner's grok credential (aio NIT 04:12:03Z + sp ADD 04:13:14Z, 11-10): every file the login wrote under
# the WHOLE home whose status changed after the marker (-cnewer), with its mode; any group/other bit -> chmod go-rwx
# BEFORE the run, said per file with the mode after; an empty mode read or a find error fails the run.
# 0 files = READ NOTHING (the token is stored outside the home, UNREAD, never 'safe'): the run stops and waits.
echo "== 0 the credential (files the login wrote, modes)"
[ -e "$LM" ] || { echo "READ login marker: READ NOTHING (run 'f1.sh mark' BEFORE the login); the run waits"; exit 1; }
CRED=$(find "$HOME" -xdev -cnewer "$LM" -type f -not -path "$HOME/f1-*" 2>"$R/cred.err")
[ -s "$R/cred.err" ] && { sed 's/^/READ cred find ERROR (an unreadable path is never a silent 0): /' "$R/cred.err"; FAIL=1; }
echo "READ files the login wrote under HOME (uncapped): $(printf '%s' "$CRED" | grep -c .)"
[ -n "$CRED" ] || { echo "READ files the login wrote under HOME: READ NOTHING (token outside the home, UNREAD, never safe); the run waits"; exit 1; }
rd "the .grok dir mode" "$(stat -c '%a %U' "$HOME/.grok" 2>/dev/null || echo 'no .grok dir')"
while IFS= read -r f; do m=$(stat -c '%a' "$f" 2>&1)
  # sp ADD (2): an empty or failed mode read is READ NOTHING, never 'owner-only'
  case "$m" in ''|*[!0-7]*) echo "READ cred file ${f#$HOME/}: mode READ NOTHING (${m:-empty}); the run waits"; FAIL=1; continue;; esac
  # aio NIT 04:29:35Z: clear group/other only (chmod go-rwx), the owner's bits kept
  if [ $((0$m & 077)) -ne 0 ]; then chmod go-rwx "$f"; echo "READ cred file ${f#$HOME/}: mode $m -> TIGHTENED to $(stat -c '%a' "$f") before the run"
  else echo "READ cred file ${f#$HOME/}: mode $m (owner-only, unchanged)"; fi
done <<< "$CRED"
[ "$FAIL" = 0 ] || { echo "ABORT: the credential reads failed; nothing launched"; exit 1; }
echo "NOTE no read is granted to heal's uid by this script; if T2 shows agi-reaper needs the session store, the grant is on the store alone, never a token file"

# sp NIT 08:46:07Z: F1_MODEL against the list grok itself gives, after the login and BEFORE the stand-up
GM=$("$GROK_BOT_BIN" models 2>&1 | awk '/^Available models:/{a=1;next} a&&/^[[:space:]]+[*-][[:space:]]/{print $2}')
if [ -z "$GM" ]; then echo "READ grok models: READ NOTHING (an empty list); nothing launched"; exit 1
elif printf '%s\n' "$GM" | grep -qxF -- "$F1_MODEL"; then echo "READ grok models: $(printf '%s' "$GM" | paste -sd' '); F1_MODEL $F1_MODEL listed"
else echo "READ grok models: $(printf '%s' "$GM" | paste -sd' '); FAIL: F1_MODEL $F1_MODEL not listed; nothing launched"; exit 1; fi
MARK=$R/.marker; touch "$MARK"; sleep 1

# --- 1. the first spawn: the ONE stand-up verb (fresh, 2b's -s uuid), then a heal pass for the after-join
echo "== 1 stand-up (fresh)"; (cd "$R" && python3 extensions/agi/bin/rotate.py stand-up --post "$SEAT"); echo "stand-up rc $?"
sleep 20; heal
P0=$(row pid); W0=$(row window); S0=$(row session_id)
rd "row pid before" "$P0"; rd "row window before" "$W0"; rd "row session_id before" "$S0"; rd "pane before" "$(panes)"
[ -n "$P0" ] && [ "$P0" != 0 ] && proc "$P0" "seat before"

# --- 2. kill the harness; heal's route (the ROUTE, T1): _watch_seats -> _recover_seat -> -r <row session_id> -> 30 s join
echo "== 2 kill + heal resume (the good id)"
[ -n "$P0" ] && [ "$P0" != 0 ] && killseat "$P0"; rd "pane after the kill" "$(panes || true)$( [ -z "$(panes)" ] && echo 'none (the window closed with the harness)')"
heal; sleep 5; heal
P1=$(row pid); S1=$(row session_id)
rd "row pid after" "$P1"; rd "row session_id after" "$S1"; rd "pane after" "$(panes)"
# alive's TERM: ENFORCED, not only printed: empty, 0, the same pid, or an after-pid not alive -> FAIL, the line says which
# sp 04:41:00Z: 'yes' needs P0 > 0, a 'gone' line from killseat for P0, and P1 alive and different
if [ -z "$P0" ] || [ "$P0" = 0 ]; then echo "READ pid differs (the kill's proof): FAIL: no seat before the kill (before-pid ${P0:-empty}): the kill never ran"; FAIL=1
elif [ "$KILLED" != "$P0" ]; then echo "READ pid differs (the kill's proof): FAIL: no 'gone' read for $P0: the kill did not complete"; FAIL=1
elif [ -z "$P1" ] || [ "$P1" = 0 ]; then echo "READ pid differs (the kill's proof): FAIL: the after-pid is ${P1:-empty}"; FAIL=1
elif [ "$P1" = "$P0" ]; then echo "READ pid differs (the kill's proof): FAIL: NO, $P0 -> $P1"; FAIL=1
elif ! kill -0 "$P1" 2>/dev/null; then echo "READ pid differs (the kill's proof): FAIL: the after-pid $P1 is not alive"; FAIL=1
else echo "READ pid differs (the kill's proof): yes $P0 -> $P1, alive"; fi
[ -n "$P1" ] && [ "$P1" != 0 ] && proc "$P1" "seat after"
W1=$(row window); CB=$( [ -n "$W1" ] && tmux capture-pane -p -t "$W1" -S -200 2>/dev/null | tr -d '[:space:]' | wc -c)
rd "capture bytes (non-whitespace; 0 = READ NOTHING)" "$( [ "${CB:-0}" -gt 0 ] && echo "$CB")"
echo "MEASURED resume proof (beside the reads, never a pass): session_id $S0 -> $S1; heal's PROVISIONAL line: $(grep -c 'resume proof PROVISIONAL' "$AGI_REAPER_LOG") time(s)"

# --- 3. where grok keeps a session: every file grok wrote under this uid's home since the marker (paths only)
echo "== 3 the session store"
ST=$(find "$HOME" -xdev -newer "$MARK" -type f -not -path "$R/*" 2>"$R/store.err")
[ -s "$R/store.err" ] && { sed 's/^/READ store find ERROR: /' "$R/store.err"; FAIL=1; }
rd "files written under HOME since the start, outside R (paths only; total $(printf '%s' "$ST" | grep -c .), first 40 shown)" "$(printf '%s' "$ST" | head -40 | paste -sd' ')"
SN=$(find "$HOME" -xdev -newer "$MARK" -not -path "$R/*" 2>"$R/store2.err" | grep -F -- "${S0:-@@none}")
[ -s "$R/store2.err" ] && { sed 's/^/READ store find ERROR: /' "$R/store2.err"; FAIL=1; }
rd "of them naming the session id (total $(printf '%s' "$SN" | grep -c .), first 5 shown)" "$(printf '%s' "$SN" | head -5 | paste -sd' ')"

# --- 4. a failed -r: a never-used id on the row, kill, heal: which of no-pane / absent / ambiguous, and does grok stay up
echo "== 4 failed -r (a dead id)"
DEAD=$(python3 -c 'import uuid;print(uuid.uuid4())')
(cd "$R/extensions/agi/bin" && python3 -c "import sys,re;from pathlib import Path
p=Path(sys.argv[1])/'.agi/nodes/.geometry/posts.md';t=p.read_text()
t2=re.sub(r'(\"name\": \"'+sys.argv[2]+r'\".*?\"session_id\": \")[^\"]*',lambda m:m.group(1)+sys.argv[3],t,count=1);assert t2!=t;p.write_text(t2)" "$R" "$SEAT" "$DEAD") \
  && git -C "$R" -c user.name=f1 -c user.email=f1@local commit -qam "F1: dead id $DEAD" || { echo "READ dead-id row write: FAILED; section 4 stops"; FAIL=1; }
SD=$(row session_id); if [ "$SD" = "$DEAD" ]; then echo "READ row session_id set to the dead id: $SD"
else echo "READ row session_id set to the dead id: FAIL: the row reads '${SD:-empty}', not $DEAD; section 4 stops"; FAIL=1; fi
if [ "$SD" = "$DEAD" ]; then
P2=$(row pid); [ -n "$P2" ] && [ "$P2" != 0 ] && killseat "$P2"
heal
rd "heal's FAILED / ambiguous line for the dead id" "$(grep -F "$DEAD" "$AGI_REAPER_LOG" | grep -e FAILED -e ambiguous | tail -1)"
rd "a grok still up on the dead id (the stay-alive case)" "$(pgrep -u "$(id -u)" -af -- "-r $DEAD" | cut -c1-120 || true)$(pgrep -u "$(id -u)" -f -- "-r $DEAD" >/dev/null || echo 'none')"
rd "pane after the failed -r" "$(panes)$( [ -z "$(panes)" ] && echo none)"
for f in --post --seat; do OUT=$(cd "$R" && python3 extensions/agi/bin/heal.py resume-failed $f "$SEAT" --root "$R" 2>&1); RC=$?
  echo "READ resume-failed $f: rc $RC: $OUT"; [ $RC -le 1 ] && break; done
[ -n "$OUT" ] || { echo "READ resume-failed: READ NOTHING"; FAIL=1; }
[ "$RC" -gt 1 ] && { echo "READ resume-failed: FAIL: the last rc is $RC (neither --post nor --seat parsed)"; FAIL=1; }
heal   # the next cycle: the fresh spawn (or the same-name refusal while an absent window is open)
rd "row pid/session_id after the next cycle" "$(row pid) / $(row session_id)"
fi

# --- 5. every 2c branch, REACHED or NOT RUN (T1): only what heal's own log shows was reached
echo "== 5 the 2c branches"
br() { if grep -qE "$2" "$AGI_REAPER_LOG"; then echo "REACHED $1"; else echo "NOT RUN $1"; fi; }
br "resume launched on the session_id proof" "seat $SEAT resume proof PROVISIONAL"
br "failed -r, absent" "resume of .* FAILED: the pane join read absent"
br "failed -r, no-pane" "resume of .* FAILED: the pane join read no-pane"
br "ambiguous (id kept, pid empty)" "seat $SEAT resume of .*ambiguous"
br "same-name refusal pass" "seat $SEAT recovery refused"
echo "NOT RUN chain seat (role prime_director) on a session_id proof: the scratch row is role director"
echo "NOT RUN the store pre-launch read: grok-bot.toml declares no [session] store (heal reads UNREAD)"

# --- cleanup: the scratch row off, its windows closed; R kept for the readings
P3=$(row pid); [ -n "$P3" ] && [ "$P3" != 0 ] && kill -TERM "$P3" 2>/dev/null
for w in $(tmux list-windows -a -F '#{window_id} #{window_name}' 2>/dev/null | awk -v s="$SEAT" 'index($2,s)==1{print $1}'); do tmux kill-window -t "$w"; done
pgrep -u "$(id -u)" -f -- "$DEAD" >/dev/null && pkill -u "$(id -u)" -f -- "$DEAD"
echo "== done: R=$R (f1.out, heal.log kept); FAIL=$FAIL"; exit $FAIL
```

## Out of scope

- Measuring CLI flags / retiring stub argv (`goal:g7.31.1.1`).
- Magic-pane product chrome.
- Pane ↔ post/pin (`goal:g7.31.2`).

## Agent Notes

Split from `goal:g7.31.1` by director-belam (point) 2026-09-21 ET — multi-headed falsifier. Launch pi parent; diagram-max; batch-max; merge-up to Belam; blockers to owner only via director-belam.

**Related:** `goal:g7.28`, `goal:g7.31.1.1`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version adds the F1 script, the owner's 'grok-bot check' (c:175d1f09df76), which the council bound to T1-T3 (alive [decision] 04:09:00Z 11-10, road (S) 3/3). The Falsifier's text is unchanged: the script is the run that decides it, and its readings are not here yet. Near miss, measured by DG1's dry setup before any launch: config.json's grok-bot bin cell names a file that exists in no post home, so the first live spawn would have died with FileNotFoundError. The script names the adapter's override (GROK_BOT_BIN) and prints its value. SM returned the first tip (R1, 04:22:55Z): no credential reads. aio's NIT and sp's ADD had been sent before it and the tip missed them. Section 0 now runs after the setup and before the stand-up. Its listing is uncapped and keeps stderr, so an unreadable path fails the run and never reads as a silent 0 (aio 04:25:21Z); the owner's token must not stay world-readable under a 755 home. alive's TERM (04:23:59Z): the kill proof is ENFORCED, not only printed (a row pid of 0 used to read 'yes P0 -> 0'). Section 3 prints its total beside its 40-line cap. The third cut (SM 04:27:15Z, list 1-9) adds sp's three T3 reads (capture bytes, the dead-id row check, the resume-failed rc), `find -cnewer` (a backdated mtime was missed), an empty mode = READ NOTHING, and `chmod go-rwx` in place of 600. A second near miss: R inherited the trunk's committed rotation records, and heal's late-reap pass acted on one of them inside R. The script now empties R's sessions/, so heal sees only the scratch seat.
<!-- THOUGHT:END -->
