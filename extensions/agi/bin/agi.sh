#!/bin/sh
# agi.sh status | stop [--pack OUT] | answer KEY VALUE | host | start: the town's stop (goal:g7.16.1.11.44.8, S1; council 3/3 10-15 19:36Z + 19:41Z) and the host fold (S2a: `host`, the root act of a box).
# The step order is READ from the matrix row `town<TAB>start<TAB>main host posts crons units blast<TAB>agi.sh` (engine.md ### matrix, at the pin): START runs the names left to right, STOP right to
# left (blast, units, crons, posts, host and main: no-ops on STOP); every name is one function pair, ck_<name> (met?) and dn_<name> (the down arm). A re-run resumes at the first unmet check.
# Captive: ONE `[ask] KEY: question` per run (rc 20, answered with `answer KEY VALUE`), `[owner-do] command` (rc 21) for what only the owner can type; answers go to town.env (root 600, no secret, never in git); town.state is root-written 644: no secret in it, and sanctuary-watch (a user timer) reads its `stopped` line.
# Cells (env; a test points them at stubs; with ROOT set every /etc default below lies under $ROOT): AGI_MAIN (/data/work/agi) · AGI_TOWN_ENV (/etc/agi/town.env) · AGI_TOWN_STATE (/etc/agi/town.state) · AGI_CARRY_ENV (/etc/agi/carry.env: the pin) · AGI_WANTS_DIR ·
# AGI_TOWN_BOXBIN (belam's box). start adds: PIN · AGI_BOX · PRIME_USER (answers or env) · ROOT=<scratch> (the host check reads its files under it) · AGI_TOWN_STARTING (/etc/agi/town.starting) · AGI_ORIGIN (the public clone) · AGI_SUDOERS ·
# AGI_SYSGITCONFIG · AGI_GUARD_INIT · AGI_LOADAVG · AGI_PSI_IO. Config: .agi/config.json values.local_maxxing.agi_town = {keep_units, ack_wait_s, carry_fetch, sudoers_line}, read at the pin. No credential here; no git write except through `box town` (uid agi-belam), the clone (as PRIME_USER) and agi-belam's own gitconfig.
D=$(cd "$(dirname "$0")" && pwd)
MAIN=${AGI_MAIN:-/data/work/agi};ENVF=${AGI_TOWN_ENV:-$ROOT/etc/agi/town.env};STATE=${AGI_TOWN_STATE:-$ROOT/etc/agi/town.state}
CARRY=${AGI_CARRY_ENV:-/etc/agi/carry.env};WANTS=${AGI_WANTS_DIR:-/etc/systemd/system/multi-user.target.wants}
die(){ echo "$*" >&2;exit 1;}
ask(){ echo "[ask] $1: $2";exit 20;}
owner_do(){ echo "[owner-do] $1";exit 21;}
g(){ git -c safe.directory="$MAIN" -C "$MAIN" "$@";}
cell(){ g show "$PIN:.agi/config.json" 2>/dev/null|jq -r ".values.local_maxxing.agi_town$1" 2>/dev/null;}
getv(){ sed -n "s/^$1=//p" "$ENVF" 2>/dev/null|tail -1;}
# the unit lists: every agi-* unit that is up (active, activating = auto-restart or a oneshot mid-run, reloading), minus the keep-list
act_units(){ systemctl list-units 'agi-*' --plain --no-legend --state=active,activating,reloading 2>/dev/null|awk '{print $1}';}
kept(){ for k in $KEEP;do case $1 in $k)return 0;;esac;done;return 1;}
others(){ for u in $(act_units);do case $u in agi-post@*|agi-boxwake@*|agi-boot.service)continue;;esac;kept $u||echo $u;done;}   # the posts step owns agi-post@*, agi-boxwake@* and agi-boot.service
posts_up(){ act_units|grep -E '^agi-(post|boxwake)@';}
links(){ ls "$WANTS" 2>/dev/null|grep '^agi-post@.*\.service$';}
uids(){ getent passwd|cut -d: -f1|grep '^agi-';}
CR="python3 $D/crons.py"
marked(){ n=0;for u in $(uids);do c=$($CR marked --root "$MAIN" --user $u 2>/dev/null)||{ echo "[crons] cannot read the crontab of $u" >&2;c=1;};n=$((n+c));done;echo $n;}
need(){ for t in git jq systemctl getent;do command -v $t >/dev/null||owner_do "sudo apt-get install -y $([ $t = systemctl ]&&echo systemd||([ $t = getent ]&&echo libc-bin||echo $t))";done;}
# prep: the pin, MAIN readable (git's own refusal is shown, e.g. "dubious ownership" as root on belam's repo), the cells: read before anything is touched. status stops here;
# pstop adds what only a STOP needs and refuses on (the box, the matrix row, a leftover /etc wants link, a stale town.state, a foreign cron block).
prep(){ need
 PIN=$(sed -n 's/^AGI_TRUNK=//p' "$CARRY" 2>/dev/null|tail -1);case $PIN in *[!0-9a-f]*|"")die "[pin] $CARRY holds no 40-hex AGI_TRUNK: nothing stopped";;esac;[ ${#PIN} = 40 ]||die "[pin] AGI_TRUNK in $CARRY is not 40 hex: nothing stopped"
 g rev-parse HEAD >/dev/null||die "[git] cannot read $MAIN as $(id -un) (git said the above): nothing stopped"
 KEEP=$(cell .keep_units'[]?');[ -n "$KEEP" ]||KEEP="agi-carry@*.path agi-memguard* agi-ram-main*";WAIT=$(cell .ack_wait_s);case $WAIT in ""|null|*[!0-9]*)WAIT=600;;esac;}
pstop(){ BOX=${AGI_BOX:-$(getv AGI_BOX)};[ -n "$BOX" ]||ask AGI_BOX "the town's seat-set name (the box cell of its posts rows)"
 case $BOX in *[!A-Za-z0-9._-]*)die "[box] AGI_BOX '$BOX' is not a name: nothing stopped";; esac
 ROW=$(g show "$PIN:.agi/nodes/.geometry/engine.md" 2>/dev/null|sed -n '/^### matrix /,/^### /{/^~~~/,/^~~~/{//!p}}'|awk -F'\t' '$1=="town"&&$2=="start"{print $3}')
 [ -n "$ROW" ]||die "[matrix] no 'town start' row in engine.md at $PIN: nothing stopped"
 [ -z "$(links)" ]||die "[links] $(links|wc -l|tr -d ' ') agi-post@ wants link(s) under $WANTS: the boot set is the rows (agi-boot projects /run links); belam's host act removes these first: nothing stopped"
 [ ! -e "$STARTING" ]||die "[start-in-progress] a start is in progress since $(cat "$STARTING" 2>/dev/null): finish it with agi.sh start (town.state is the record it resumes from); nothing stopped"
 if grep -q '^stopped ' "$STATE" 2>/dev/null&&[ -n "$(posts_up)$(others)" ];then die "[stale-state] $STATE says stopped but $(posts_up|wc -l|tr -d ' ') post unit(s) and $(others|wc -l|tr -d ' ') other unit(s) are up (the town was brought back without start): move the file aside; nothing stopped";fi
 for u in $(uids);do f=$($CR marked --root "$MAIN" --user $u --foreign 2>/dev/null)||die "[crons] cannot read the crontab of $u: nothing stopped";[ -z "$f" ]||die "[crons] $u holds a managed block installed from ANOTHER root ($(echo "$f"|cut -f1|head -1)): stop removes MAIN's only; remove that block by hand first: nothing stopped";done;}
ids(){ g show "$TRK:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$BOX" 'select(has("harness") and .box==$x and .name!="belam")|.name';}
# --- blast: `box town down <sha>` as agi-belam; the ack of a post = the down commit's own sha reached refs/held/<p>/belam (held), else a card commit after t0 (card)
ck_blast(){ [ -s "$STATE" ]||[ -e "$SCR/ack" ];}   # sent: a town.state exists (an earlier run blasted) or this run did
dn_blast(){ BOXB=${AGI_TOWN_BOXBIN:-$(getent passwd agi-belam|cut -d: -f6)/bin/box};SHA=$(g rev-parse HEAD)||die "[blast] MAIN has no HEAD"
 (cd "$MAIN"&&sudo -H -u agi-belam env AGI_POST=belam AGI_BOX=$BOX AGI_TRUNK=$TRK $BOXB town down $SHA)||die "[blast] box town down $SHA failed: nothing stopped"
 : >$SCR/ack;t=0;while :;do pend=;for p in $(ids);do grep -q " $p " $SCR/ack 2>/dev/null&&continue;c=$(g rev-parse -q --verify refs/box/belam/$p)||{ pend="$pend $p";continue;}
   [ "$(g log -1 --format=%B $c)" = "[town] down $SHA" ]||{ pend="$pend $p";continue;};t0=$(g log -1 --format=%ct $c)
   if g merge-base --is-ancestor $c refs/held/$p/belam 2>/dev/null;then echo "ack $p held">>$SCR/ack
   elif [ "$(g log -1 --format=%ct refs/heads/posts/$p -- .agi/nodes/doc/card-$p.md 2>/dev/null)" -gt $t0 ] 2>/dev/null;then echo "ack $p card">>$SCR/ack
   else pend="$pend $p";fi;done
  [ -z "$pend" ]&&break;[ $t -ge $WAIT ]&&break;sleep 2;t=$((t+2));done
 for p in $pend;do echo "noack $p">>$SCR/ack;echo "[blast] noack $p: listed, the stop goes on" >&2;done;}
# --- units: town.state FIRST (tmp + mv), then every active agi-* unit outside the keep-list and outside the posts' own (agi-post@*, agi-boxwake@*, agi-boot.service)
ck_units(){ [ -s "$STATE" ]&&[ -z "$(others)" ]&&[ -z "$(en_left)" ];}
en_left(){ for u in $(sed -n 's/^unit \(.*\) enabled$/\1/p' "$STATE" 2>/dev/null);do systemctl is-enabled $u >/dev/null 2>&1&&echo $u;done;}
wstate(){ [ -s "$STATE" ]&&return 0;{ echo "boot $(systemctl is-enabled agi-boot.service 2>/dev/null|grep -qx enabled&&echo enabled||echo disabled)"
   for u in $(act_units|grep '^agi-post@');do u=${u#agi-post@};echo "running ${u%.service}";done
   for u in $(others);do systemctl is-enabled $u >/dev/null 2>&1&&echo "unit $u enabled"||echo "unit $u";done
   cat $SCR/ack 2>/dev/null||:;} > $STATE.tmp&&chmod 644 $STATE.tmp&&mv $STATE.tmp $STATE||die "[state] cannot write $STATE: nothing stopped";}
# a unit that is enabled would come back at the next boot: it is stopped AND disabled (`unit NAME enabled` in town.state; start re-enables it)
dn_units(){ wstate
 for u in $(others|grep -E '\.(timer|path|socket)$') $(others|grep -vE '\.(timer|path|socket)$');do systemctl stop $u||die "[units] cannot stop $u";done
 for u in $(en_left);do systemctl disable $u||die "[units] cannot disable $u";done;}
# --- crons: crons.py remove for every uid holding the marked block (crons_live and the graph are untouched)
ck_crons(){ [ "$(marked)" = 0 ];}
dn_crons(){ for u in $(uids);do c=$($CR marked --root "$MAIN" --user $u)||die "[crons] cannot read the crontab of $u";[ "$c" = 0 ]||$CR remove --root "$MAIN" --user $u||die "[crons] remove failed for $u";done;}
# --- posts: the posts' own units and agi-boot (disabled; start re-enables it). The /etc agi-post@ wants links are belam's host act (prep refuses while any is left). Refused while heal (agi-reaper*) is up: it would relaunch a stopped post. `stopped <box> <UTC>` LAST.
ck_posts(){ [ -z "$(posts_up)" ]&&[ -z "$(links)" ]&&! systemctl is-enabled agi-boot.service >/dev/null 2>&1&&grep -q '^stopped ' "$STATE" 2>/dev/null;}
dn_posts(){ [ -z "$(act_units|grep '^agi-reaper')" ]||die "[reaper] agi-reaper* is active: heal would relaunch a stopped post (the units step runs first): nothing stopped"
 systemctl disable agi-boot.service||die "[posts] cannot disable agi-boot.service"
 for u in $(posts_up);do systemctl stop $u||die "[posts] cannot stop $u";done
 grep -q '^stopped ' "$STATE"||echo "stopped $BOX $(date -u +%Y-%m-%dT%H:%M:%SZ)">>$STATE;}
status(){ ou=$(others|wc -l|tr -d ' ');pu=$(posts_up|wc -l|tr -d ' ');lk=$(links|wc -l|tr -d ' ');cl=$(marked);be=0;systemctl is-enabled agi-boot.service >/dev/null 2>&1&&be=1
 echo "units-outside-keep $((ou+pu))";echo "posts-running $pu";echo "wants-links $lk";echo "agi-boot-enabled $be";echo "cron-lines $cl";[ $((ou+pu+lk+be+cl)) = 0 ];}
cmd_stop(){ pack=;while [ $# -gt 0 ];do case $1 in --pack)[ $# -ge 2 ]||die "stop: --pack wants OUT";pack=$2;shift 2;;*)die "stop: unknown argument '$1'";;esac;done
 [ -z "$pack" ]||die "stop --pack: S3, not yet (nothing stopped)"
 need;[ "$(id -u)" = 0 ]||die "[root] stop needs root: nothing stopped"
 prep;pstop;TRK=$(g branch --show-current);[ -n "$TRK" ]||die "[trunk] MAIN has no checked-out branch: nothing stopped"
 for s in $ROW;do command -v dn_$s >/dev/null 2>&1||die "[step] '$s' (matrix row) has no down arm in this agi.sh: nothing stopped";done
 SCR=$(mktemp -d)||die "[tmp] no scratch dir";trap 'rm -rf "$SCR"' 0;rev=;for s in $ROW;do rev="$s $rev";done
 for s in $rev;do ck_$s||{ dn_$s;ck_$s||die "[step] $s: still unmet after its down arm";};done
 status >/dev/null&&echo "stopped $BOX: $(sed -n 's/^stopped //p' "$STATE")"||{ status;die "[status] the stop left the town up (see above)";};}
cmd_answer(){ [ $# = 2 ]||die "answer KEY VALUE";k=$1;v=$2
 case $k in [A-Z]*)case $k in *[!A-Z0-9_]*)k=;;esac;;*)k=;;esac;[ -n "$k" ]&&[ ${#k} -le 64 ]||die "[answer] KEY is [A-Z][A-Z0-9_]*, up to 64"
 case $v in ""|*[!A-Za-z0-9._:/@+-]*)die "[answer] VALUE is 1-128 of [A-Za-z0-9._:/@+-] (an answer, never a secret)";;esac;[ ${#v} -le 128 ]||die "[answer] VALUE is 1-128 of [A-Za-z0-9._:/@+-]"
 [ -e "$v" ]||for w in $(echo "$v"|tr './:@+=' ' ');do [ ${#w} -lt 32 ]||die "[secret] a segment of 32+ token chars (between . : / @ + =) is refused: town.env holds no secret (only a value that IS an existing path is exempt)";done
 { grep -v "^$k=" "$ENVF" 2>/dev/null;echo "$k=$v";} >"$ENVF.tmp"&&chmod 600 "$ENVF.tmp"&&mv "$ENVF.tmp" "$ENVF"||die "[answer] cannot write $ENVF";echo "answered $k";}
# --- host (S2a, council 09:20Z 10-16): the root host act, folded in from guard/host-act-encryption-town.sh (whose `act` is now ONE line that execs `agi.sh host`; its `move` stays there until S3).
#   PIN=<40-hex commit of AGI_REPO> [ROOT=<scratch>] [AGI_REPO AGI_BOX E_MEM_HIGH E_MEM_MAX E_OOM_LIMIT SKIP_PREREQ PRIME_USER] sh agi.sh host
# hostmet (every piece / unit / polkit rule byte-equal to the PIN via sect, carry.env, the ram unit, the slice, the MAIN ACLs) runs BEFORE STEP 0: met -> "host: met", rc 0, NO backup; else STEP 0 backs the before-state up and writes ONE rollback, then the act.
# agi-carry-fetch.timer is enabled only when .agi/config.json values.local_maxxing.agi_town.carry_fetch is true at the PIN (default false: the hub route is out). NO sudoers file is written here (S2b). The pieces are ONE list (PC) read by the writer AND by hostmet.
# /etc/agi/host.done = the PIN is the act's LAST write (cleared before the first): hostmet requires it, so an act that died at verify / enable re-runs. STOP leaves the host installed and never touches it: ck_host / dn_host are met / no-op (S2b: start's host check is hostmet).
up_host(){ (
R=${ROOT:-};M=${AGI_REPO:-/data/work/agi};PIN=${PIN:-};BOX=${AGI_BOX:-encryption-town}
PU=${PRIME_USER:-belam};[ -z "$R" ]||PU=${PRIME_USER:-$(id -un)}
die(){ echo "host-act: $*">&2;exit 1;}
case $PIN in ""|*[!0-9a-f]*)die "PIN must be a 40-hex commit sha";esac;[ ${#PIN} = 40 ]||die "PIN must be a 40-hex commit sha"
export GIT_NO_REPLACE_OBJECTS=1 GIT_NO_LAZY_FETCH=1;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
G(){ git -c safe.directory=$R$M -C $R$M "$@";}
G cat-file -e $PIN^{commit} 2>/dev/null||die "$PIN is not a commit of $R$M"
[ -n "$R" ]||[ "$(id -u)" = 0 ]||die "run as root (sudo), or set ROOT= for a rehearsal"
S(){ G ls-tree --full-tree --name-only $PIN .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$PIN:|"|G cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
OWN="-o root -g root";[ -z "$R" ]||OWN=
put(){ t=$(mktemp)||exit 1;S $1>$t;[ -s $t ]||{ rm -f $t;die "no ### $1 at $PIN";};case $4 in sh)sh -n $t||{ rm -f $t;die "### $1 does not parse";};esac;install -D -m $3 $OWN $t $R$2||{ rm -f $t;die "cannot write $2";};echo "  $2  $(sha256sum<$t|cut -c1-16)  $(wc -c<$t) B";rm -f $t;}
AG=agi;[ -z "$R" ]||AG=$(id -gn)
TS=${AGI_TOWN_STATE:-$R/etc/agi/town.state};TG=${AGI_TOWN_STARTING:-$R/etc/agi/town.starting}
CF=$(G show $PIN:.agi/config.json 2>/dev/null|jq -r ".values.local_maxxing.agi_town.carry_fetch==true" 2>/dev/null)
PC="agi-vstore:/usr/local/libexec/agi-vstore:755:sh sect:/opt/agi/bin/sect:755:sh box:/opt/agi/bin/box:755:sh box-carry:/opt/agi/bin/box-carry:755:sh agi-signers:/opt/agi/bin/agi-signers:755:sh $(for u in agi-carry@.service agi-carry@.path agi-carry-fetch.service agi-carry-fetch.timer agi-boot.service;do printf '%s:/etc/systemd/system/%s:644:unit ' $u $u;done)agi.rules:/etc/polkit-1/rules.d/50-agi.rules:644:unit"
each(){ for x in $PC;do n=${x%%:*};r=${x#*:};d=${r%%:*};r=${r#*:};m=${r%%:*};k=${r#*:};"$@"||return 1;done;}
put1(){ put $n $d $m $k;}
pmet(){ S $n|cmp -s - $R$d&&[ "$(stat -c %a $R$d)" = $m ];}
carry_env(){ printf 'AGI_BOX=%s\nAGI_HUB=\nAGI_REPO=%s\nAGI_TRUNK=%s\nGIT_CONFIG_VALUE_0=%s\n' $BOX $M $PIN $M;}
ramunit(){ printf '%s\n' '# encryption-town ONLY: MAIN is a plain directory on the internal drive; this satisfies the pinned agi-boot.service Requires/After' '[Unit]' 'Description=encryption-town: no RAM disk, MAIN on the internal drive' '[Service]' 'Type=oneshot' 'RemainAfterExit=yes' 'ExecStart=/bin/true';}
sliceunit(){ printf '%s\n' '# encryption-town: typed here (config:guard has no E line); 7.8 GB box' '[Slice]' "MemoryHigh=${E_MEM_HIGH:-5G}" "MemoryMax=${E_MEM_MAX:-6G}" 'ManagedOOMMemoryPressure=kill' "ManagedOOMMemoryPressureLimit=${E_OOM_LIMIT:-40%}";}
acl1(){ getfacl -p "$1" 2>/dev/null|grep -qx "$2";}
aclmet(){ for d in objects refs logs worktrees;do acl1 $R$M/.git/$d "group:$AG:rwx"&&acl1 $R$M/.git/$d "user:$PU:rwx"||return 1;done;for d in $R$M/.agi/sessions $R$M/.agi/sessions/inbox $R$M/.agi/comms;do acl1 $d "group:$AG:rwx"||return 1;done;acl1 $R$M/.agi/comms "user:$PU:rwx";}
# R-c (council 10-21): host.done proves the tail ran ONCE, not that it holds. Live (or a rehearsal ONLY through AGI_HOST_UNITS=<stub dir>) the units must still be enabled: `systemctl is-enabled agi-boot.service` prints exactly `enabled` with rc 0 (and agi-carry-fetch.timer the same iff the cell is true); any other output, a non-zero rc or no systemctl is NOT met (fail closed). A plain rehearsal skips it.
# A STOPPED town (town.state has its `stopped` line; council 10-21 R-c on a stopped town): stop disabled agi-boot, and the carry-fetch timer if town.state records `unit agi-carry-fetch.timer enabled`, by design. There unitsmet wants exactly `disabled` for those (masked, static, empty, no systemctl: NOT met),
# the act's tail runs daemon-reload ONLY (no enable / start: start's own steps re-enable from town.state and read each back as exactly `enabled`). A start IN PROGRESS (town.starting) has begun enabling them, so either exact word is met there.
stp(){ grep -q '^stopped ' "$TS" 2>/dev/null;}
unitsmet(){ [ -n "$R" ]&&[ -z "$AGI_HOST_UNITS" ]&&return 0
 o=$(systemctl is-enabled agi-boot.service 2>/dev/null);rc=$?
 if ! stp;then [ $rc = 0 ]&&[ "$o" = enabled ]||return 1;elif [ -e "$TG" ];then [ "$o" = enabled ]||[ "$o" = disabled ]||return 1;else [ "$o" = disabled ]||return 1;fi
 tw=;[ "$CF" != true ]||tw=enabled;if stp&&grep -qx 'unit agi-carry-fetch.timer enabled' "$TS" 2>/dev/null;then tw=disabled;fi;[ -n "$tw" ]||return 0
 o=$(systemctl is-enabled agi-carry-fetch.timer 2>/dev/null);rc=$?
 if [ $tw = enabled ];then [ $rc = 0 ]&&[ "$o" = enabled ];elif [ -e "$TG" ];then [ "$o" = enabled ]||[ "$o" = disabled ];else [ "$o" = disabled ];fi;}
hostmet(){ each pmet&&carry_env|cmp -s - $R/etc/agi/carry.env&&ramunit|cmp -s - $R/etc/systemd/system/agi-ram-main.service&&sliceunit|cmp -s - $R/etc/systemd/system/agi.slice&&[ -d $R/mnt/agi-ram/state ]&&[ -d $R/var/lib/agi ]&&[ "$(cat $R/etc/agi/host.done 2>/dev/null)" = $PIN ]&&unitsmet&&aclmet;}
tm(){ [ "$CF" = true ]||return 0;stp&&return 0;if [ -n "$R" ]&&[ -z "$AGI_HOST_UNITS" ];then echo "rehearsal: systemctl enable --now agi-carry-fetch.timer";else systemctl enable --now agi-carry-fetch.timer;fi;}
# ---- preflight (nothing written yet) ----
for c in git jq setfacl sed;do command -v $c>/dev/null||die "missing tool: $c";done
[ -n "$R" ]||{ command -v systemctl>/dev/null||die "missing tool: systemctl";getent group agi>/dev/null||die "group agi is absent (the agi-* users are the owner's act)";}
# R-b (council 10-21): AGI_HOST_UNITS=<stub dir> (a rehearsal's switch for the live tail): with ROOT set, systemctl AND systemd-analyze must resolve INSIDE that dir, else nothing runs; a rehearsal never reaches the real systemctl
[ -z "$R" ]||[ -z "$AGI_HOST_UNITS" ]||for c in systemctl systemd-analyze;do case $(command -v $c 2>/dev/null) in "$AGI_HOST_UNITS"/*);;*)die "AGI_HOST_UNITS needs stubs: $c does not resolve inside $AGI_HOST_UNITS (nothing written)";;esac;done
G show $PIN:.agi/nodes/.geometry/posts.md>/dev/null||die "no posts.md at $PIN"
# B3 (alive/aio 10-21): `up_host check` writes nothing: met -> rc 0, else rc 1 with the line start prints. The live box has no host.done until ONE `sudo PIN=<pin> sh agi.sh host` has run (owner / SM GO); start never runs the act itself.
if [ "$1" = check ];then hostmet&&{ echo "host: met";exit 0;};echo "host: not met; run agi.sh host" >&2;exit 1;fi
id $PU>/dev/null 2>&1||die "PREREQ: user $PU (the comms ACL's second entry) is absent: PRIME_USER=<user> to name another"
[ -n "$SKIP_PREREQ" ]||{ [ -x $R/opt/agi/bin/pi ]||[ -x $R/usr/local/bin/pi ]||die "PREREQ: no pi at /opt/agi/bin/pi (agi-project exits 3 without it while a pi row has box $BOX): install it first, SKIP_PREREQ=1 to override";}
hostmet&&{ echo "host: met";exit 0;}
# ---- STEP 0 (root, BEFORE anything else): back the before-state up and write ONE rollback command ----
B=$R/var/backups/agi-act-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p $R/var/backups&&mkdir $B||die "$B exists or cannot be made: refusing to overwrite a before-state";mkdir $B/files
L="/etc/agi/host.done /etc/agi/carry.env /etc/systemd/system/agi-boot.service /etc/systemd/system/agi-ram-main.service /etc/systemd/system/agi-carry@.service /etc/systemd/system/agi-carry@.path /etc/systemd/system/agi-carry-fetch.service /etc/systemd/system/agi-carry-fetch.timer /etc/systemd/system/agi.slice /etc/polkit-1/rules.d/50-agi.rules /opt/agi/bin/agi-signers /opt/agi/bin/box /opt/agi/bin/box-carry /opt/agi/bin/sect /usr/local/libexec/agi-vstore"
for f in $L;do if [ -e $R$f ];then (cd $R/&&cp -a --parents ${f#/} $B/files/)||exit 1;else echo $f>>$B/absent;fi;done
for d in $M/.git/worktrees $M/.agi/comms $M/.agi/sessions/inbox $M/.agi/sessions /mnt/agi-ram/state /mnt/agi-ram /opt/agi/bin /opt/agi /usr/local/libexec /etc/agi /var/lib/agi;do [ -d $R$d ]||echo $d>>$B/absentdirs;done
for f in $L;do [ -e $R$f ]&&stat -c '%a %U:%G %n' $R$f;done>$B/before.stat
AD=;for d in objects refs logs worktrees;do [ -d $R$M/.git/$d ]&&AD="$AD $R$M/.git/$d";done
[ -z "$AD" ]||getfacl -R -p $AD>$B/acl.before 2>/dev/null||exit 1
[ ! -d $R$M/.agi/sessions ]||getfacl -p $R$M/.agi/sessions>>$B/acl.before 2>/dev/null||exit 1
[ ! -e $R$M/.agi/sessions/.grid.lock ]||getfacl -p $R$M/.agi/sessions/.grid.lock>>$B/acl.before 2>/dev/null||exit 1
[ ! -d $R$M/.agi/sessions/inbox ]||getfacl -p $R$M/.agi/sessions/inbox>>$B/acl.before 2>/dev/null||exit 1
[ ! -d $R$M/.agi/comms ]||getfacl -R -p $R$M/.agi/comms>>$B/acl.before 2>/dev/null||exit 1
U=$R/run/systemd/system;( cd $U 2>/dev/null&&ls -d agi-* agi.slice multi-user.target.wants/agi-* 2>/dev/null )>$B/run.list
if [ -s $B/run.list ];then tar -C $U -cpf $B/run.tar -T $B/run.list||exit 1;(cd $U&&find $(cat $B/run.list) |sort)>$B/run.before;else : >$B/run.before;fi
(cd $B/files&&find . -type f|sort|xargs -r sha256sum)>$B/before.sha256
printf '%s\n' '#!/bin/sh' "B=$B;R=$R" 'U=$R/run/systemd/system' '[ -n "$R" ]||systemctl disable --now agi-carry-fetch.timer 2>/dev/null' '[ -n "$R" ]||systemctl disable agi-boot.service 2>/dev/null' '[ ! -d $B/files ]||cp -a $B/files/. ${R:-/}||exit 1' '[ ! -s $B/acl.before ]||setfacl --restore=$B/acl.before||echo "rollback: acl restore rc $? (vanished paths skipped)">&2' 'if [ -d $U ];then ( cd $U;find agi-* agi.slice multi-user.target.wants/agi-* 2>/dev/null|while read p;do grep -qxF "$p" $B/run.before||rm -rf "$p";done );fi' '[ ! -s $B/run.tar ]||tar -C $U -xpf $B/run.tar' '[ ! -s $B/absent ]||while read f;do rm -f $R$f;done<$B/absent' '[ ! -s $B/absentdirs ]||while read d;do rmdir $R$d 2>/dev/null;done<$B/absentdirs' '[ -n "$R" ]||systemctl daemon-reload' 'echo rolled back from $B "(an act-made dir that posts have filled since stays: rmdir removes only empty ones)"'>$B/rollback.sh
echo "backup $B: $(wc -l <$B/before.sha256) files, $(wc -l <$B/run.before) /run paths, $(wc -l <$B/absent 2>/dev/null||echo 0) absent files; rollback: sh $B/rollback.sh"
# ---- the act: the pieces and units, carry.env, the E no-op ram unit, the slice, reload, enable ----
rm -f $R/etc/agi/host.done||exit 1   # an act that dies below leaves NO marker: the re-run is not met
echo "installing from $PIN:"
each put1||exit 1
install -d -m 755 $OWN $R/etc/agi||exit 1
carry_env>$R/etc/agi/carry.env||exit 1;chmod 644 $R/etc/agi/carry.env
install -d -m 755 $OWN $R/mnt/agi-ram $R/mnt/agi-ram/state||exit 1
ramunit>$R/etc/systemd/system/agi-ram-main.service||exit 1;chmod 644 $R/etc/systemd/system/agi-ram-main.service
sliceunit>$R/etc/systemd/system/agi.slice||exit 1;chmod 644 $R/etc/systemd/system/agi.slice
install -d -m 755 $OWN $R/var/lib/agi||exit 1
# MAIN ACL: the post users (group agi) create refs, objects, logs and worktrees in MAIN's .git; L carries this, nothing in the repo made it
install -d $R$M/.git/worktrees||exit 1
for d in objects refs logs worktrees;do setfacl -R -m g:$AG:rwX,u:$PU:rwX $R$M/.git/$d&&find $R$M/.git/$d -type d -exec setfacl -d -m g:$AG:rwX,u:$PU:rwX {} +||die "cannot set the MAIN ACL on .git/$d: sh $B/rollback.sh";done
echo "  MAIN ACL g:$AG:rwX + u:$PU:rwX (+default) on .git/{objects,refs,logs,worktrees}"
IB=$R$M/.agi/sessions/inbox;NS=;[ -d $R$M/.agi/sessions ]||NS=$R$M/.agi/sessions
mkdir -p $IB||exit 1;[ -n "$R" ]||chown --reference=$R$M/.agi $NS $IB||exit 1
# G5: grid.py commit --all takes sessions/.grid.lock as a post user, so .agi/sessions needs the group too (not recursive: the files in it keep their owners)
setfacl -m g:$AG:rwx $R$M/.agi/sessions&&setfacl -d -m g:$AG:rwx $R$M/.agi/sessions||die "cannot set the sessions ACL on .agi/sessions: sh $B/rollback.sh"
echo "  sessions ACL g:$AG:rwx + default g:$AG:rwx on .agi/sessions"
# a file made BEFORE the default has no group entry (belam, hand-set 01:0xZ): the grid lock gets its own
[ ! -e $R$M/.agi/sessions/.grid.lock ]||{ setfacl -m g:$AG:rw $R$M/.agi/sessions/.grid.lock||die "cannot set the ACL on .agi/sessions/.grid.lock: sh $B/rollback.sh";echo "  lock ACL g:$AG:rw on .agi/sessions/.grid.lock";}
setfacl -m g:$AG:rwx $IB&&setfacl -d -m g:$AG:rw- $IB||die "cannot set the inbox ACL on .agi/sessions/inbox: sh $B/rollback.sh"
echo "  inbox ACL g:$AG:rwx + default g:$AG:rw- on .agi/sessions/inbox"
CM=$R$M/.agi/comms;[ -d $CM ]||{ mkdir -p $CM&&{ [ -n "$R" ]||chown --reference=$R$M/.agi $CM;};}||exit 1
setfacl -R -m g:$AG:rwX,u:$PU:rwX $CM&&find $CM -type d -exec setfacl -d -m g:$AG:rwX,u:$PU:rwX {} +||die "cannot set the comms ACL on .agi/comms: sh $B/rollback.sh"
echo "  comms ACL g:$AG:rwX + u:$PU:rwX (+default on every dir) on .agi/comms"
if [ -z "$R" ];then
 U=$(G show $PIN:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b $BOX 'select(.box==$b and .engine.v==4)|.name'|head -1)
 if [ -n "$U" ]&&id agi-$U>/dev/null 2>&1;then
  for d in objects refs logs worktrees;do t=$(setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups mktemp -d $M/.git/$d/.act-probe.XXXXXX)&&setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups rmdir $t||die "agi-$U cannot create under $M/.git/$d (the MAIN ACL): sh $B/rollback.sh";done
  t=$(setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups mktemp $M/.agi/sessions/inbox/.act-probe.XXXXXX)&&setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups rm $t||die "agi-$U cannot create a file in $M/.agi/sessions/inbox (the inbox ACL): sh $B/rollback.sh"
  sd=$(find "$M/.agi/comms" -mindepth 1 -type d|head -1)
  for d in "$M/.agi/sessions" "$M/.agi/comms" ${sd:+"$sd"};do t=$(setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups mktemp "$d/.act-probe.XXXXXX")&&setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups rm $t||die "agi-$U cannot create a file in $d (the sessions / comms ACL): sh $B/rollback.sh";done
  [ ! -e $M/.agi/sessions/.grid.lock ]||setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups sh -c ': >>"$0"' $M/.agi/sessions/.grid.lock||die "agi-$U cannot open $M/.agi/sessions/.grid.lock for writing (the lock ACL): sh $B/rollback.sh"
  echo "  probe: agi-$U creates and removes a dir in .git/{objects,refs,logs,worktrees} and a file in .agi/sessions, .agi/sessions/inbox and .agi/comms"
 else echo "  probe SKIPPED: no agi-<post> user for a box $BOX row yet">&2;fi
fi
if [ -z "$R" ]||[ -n "$AGI_HOST_UNITS" ];then   # AGI_HOST_UNITS=<stub dir>: a rehearsal runs this tail too, against the systemctl / systemd-analyze stubs IN that dir (R-b: refused otherwise)
 systemd-analyze verify $R/etc/systemd/system/agi-ram-main.service $R/etc/systemd/system/agi-boot.service $R/etc/systemd/system/agi-carry@.service $R/etc/systemd/system/agi-carry-fetch.service $R/etc/systemd/system/agi.slice||die "systemd-analyze verify refused a unit: sh $B/rollback.sh"
 if stp;then systemctl daemon-reload||die "daemon-reload failed: sh $B/rollback.sh";echo "stopped town: start's steps re-enable"
 else systemctl daemon-reload&&tm&&systemctl enable agi-boot.service||die "enable failed: sh $B/rollback.sh";fi   # (2) council 10-21: ENABLE only, no start: start (S5) writes the flags with no post up, then its restart of agi-boot starts the posts
 echo "slice:";systemctl show agi.slice -p MemoryHigh -p MemoryMax -p ManagedOOMMemoryPressure
else tm||exit 1;fi
echo "act done; next: per post, PIN=$PIN sh $D/../guard/host-act-encryption-town.sh move <post> (after its row has box $BOX at that pin)"
printf '%s\n' $PIN>$R/etc/agi/host.done&&chmod 644 $R/etc/agi/host.done||exit 1   # the LAST line (council R1): only a completed act is met
);}
# ===== start (S2b; council 3/3 10-15 19:36Z + 10-16 09:20Z + 10-21): the town up on a box, captive and idempotent =====
# ONE TABLE (council cond 6): every S-step -> the matrix-row name whose up arm runs it. `steps` is that table; the lane checks it against the row, the sk_/su_ arms and the dn_/ck_ arms.
#   S0 preflight and S1 inputs run BEFORE the row (cmd_start). S2 main -> main · S3 host + S4 credentials -> host · S5 posts + S6 logins -> posts · S7 crons -> crons · S8 units -> units · S9 box town up + read-back + town.state moved aside -> blast
# Every name has sk_<name> (met? read from LIVE state: units, crontab, refs, files; never town.state alone: cond 4) and su_<name> (the up arm). START runs the row left to right: sk_ || { su_; sk_ || die }.
steps(){ printf '%s\n' 'S0 pre' 'S1 pre' 'S2 main' 'S3 host' 'S4 host' 'S5 posts' 'S6 posts' 'S7 crons' 'S8 units' 'S9 blast';}
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ;}
STARTING=${AGI_TOWN_STARTING:-$ROOT/etc/agi/town.starting};ORIGIN=${AGI_ORIGIN:-https://github.com/CodexOperator/AGI.git}
SUDOERS=${AGI_SUDOERS:-$ROOT/etc/sudoers.d/90-agi-belam};SYSGIT=${AGI_SYSGITCONFIG:-$ROOT/etc/gitconfig}
phome(){ getent passwd "$1"|cut -d: -f6;}
au(){ u=$1;shift;sudo -n -u "$u" "$@";}
apt1(){ case $1 in setfacl)echo acl;; script)echo bsdutils;; *)echo $1;;esac;}
guard_ok(){ GI=${AGI_GUARD_INIT:-$MAIN/extensions/agi/guard/guard-init.sh};[ -f "$GI" ]||return 0;sh "$GI" --status >/dev/null 2>&1||owner_do "sudo sh $GI apply   # guard-init.sh --status is absent or degraded; agi.sh never runs it";}
# S0: the deps (one [owner-do] per run), no <MAIN>/bin/*.py (CLAUDE.md: driver.sh prefers a shadow copy), the guard layers
s0(){ for t in git jq setfacl python3 strace script gh claude;do command -v $t >/dev/null 2>&1&&continue
  case $t in claude)owner_do "npm install -g @anthropic-ai/claude-code   # claude is absent";; esac;owner_do "sudo apt-get install -y $(apt1 $t)";done
 [ -x "$ROOT/opt/agi/bin/pi" ]||[ -x "$ROOT/usr/local/bin/pi" ]||command -v pi >/dev/null 2>&1||owner_do "install pi at /opt/agi/bin/pi   # agi-project exits 3 without it while a pi row has this box"
 python3 -c 'import yaml' 2>/dev/null||owner_do "sudo apt-get install -y python3-yaml"
 ls "$MAIN"/bin/*.py >/dev/null 2>&1&&die "[shadow] $MAIN/bin/*.py exists: driver.sh prefers it over the engine's and a stale copy once wiped nodes/ (CLAUDE.md): remove it by hand; nothing started"
 guard_ok;}
# S1: the inputs, ONE [ask] per run: AGI_BOX, then the pin; PRIME_USER defaults to belam
deftip(){ if [ -d "$MAIN/.git" ];then g rev-parse HEAD 2>/dev/null;else git ls-remote "$ORIGIN" HEAD 2>/dev/null|cut -f1;fi;}
inputs(){ BOX=${AGI_BOX:-$(getv AGI_BOX)};[ -n "$BOX" ]||ask AGI_BOX "the town's seat-set name (the box cell of its posts rows)"
 case $BOX in *[!A-Za-z0-9._-]*)die "[box] AGI_BOX '$BOX' is not a name: nothing started";; esac
 PU=${PRIME_USER:-$(getv PRIME_USER)};PU=${PU:-belam}
 PIN=${PIN:-$(getv PIN)};[ -n "$PIN" ]||ask PIN "the commit to start, 40 hex (the tip now: $(deftip))"
 case $PIN in *[!0-9a-f]*)die "[pin] '$PIN' is not 40 hex: nothing started";; esac;[ ${#PIN} = 40 ]||die "[pin] '$PIN' is not 40 hex: nothing started";}
# --- main (S2): present -> the pin must be an ancestor of HEAD; absent -> the public clone, then the pin checked out on the origin branch that holds it. (The ring, capsule in and --from are S3.)
sk_main(){ [ -d "$MAIN/.git" ]&&g cat-file -e "$PIN^{commit}" 2>/dev/null&&g merge-base --is-ancestor "$PIN" HEAD 2>/dev/null;}
su_main(){ if [ -e "$MAIN" ]&&[ -n "$(ls -A "$MAIN" 2>/dev/null)" ];then [ -d "$MAIN/.git" ]||die "[main] $MAIN exists and is not a git repo: nothing started"
  die "[main] the pin $PIN is not an ancestor of $MAIN's HEAD (or not a commit of it): fetch it or name another pin; nothing started";fi
 d=$(dirname "$MAIN");o=;[ -z "$ROOT" ]&&[ "$(id -u)" = 0 ]&&o="-o $PU";install -d $o "$d"||die "[main] cannot make $d: nothing started"
 au $PU git clone -q "$ORIGIN" "$MAIN"||die "[main] the clone of $ORIGIN failed: nothing started"
 br=$(g for-each-ref --contains "$PIN" --format='%(refname)' refs/remotes/origin 2>/dev/null|grep -v '/HEAD$'|head -1);br=${br#refs/remotes/};[ -n "$br" ]||die "[main] the pin $PIN is on no branch of $ORIGIN: nothing started"
 au $PU git -C "$MAIN" checkout -q -B "${br#origin/}" "$PIN"||die "[main] cannot check out the pin: nothing started"
 guard_ok;echo "main: cloned $ORIGIN, $PIN on ${br#origin/}";}
# --- host (S3 + S4). S3's check is hostmet (B2: host.done included); NOT met -> the line and rc 1, never the act (B3: the act is root's own, once). S4 credentials: agi.sh holds none.
hl(){ printf '[credential "https://github.com"]\n\thelper = \n\thelper = !sudo -n -u %s /usr/bin/gh auth git-credential\n' "$PU";}
narrow(){ printf 'agi-belam ALL=(%s) NOPASSWD: /usr/bin/gh auth git-credential' "$PU";}
cr_gh(){ au $PU gh auth status >/dev/null 2>&1;}
cr_sudo(){ [ -f "$SUDOERS" ]&&{ { narrow;echo;}|cmp -s - "$SUDOERS"||{ sl=$(cell .sudoers_line);[ -n "$sl" ]&&[ "$sl" != null ]&&printf '%s\n' "$sl"|cmp -s - "$SUDOERS";};};}
cr_reach(){ for u in $(uids|grep -vx agi-belam);do sudo -n -l -U $u 2>/dev/null|grep -qE "\((ALL|$PU)[ :)]"&&{ echo $u;return 1;};done;return 0;}
gcfgs(){ echo "$SYSGIT";for u in $(uids);do echo "$(phome $u)/.gitconfig";done;}
ngit(){ n=0;for f in $(gcfgs);do [ -f "$f" ]&&grep -q 'git-credential' "$f"&&n=$((n+1));done;echo $n;}
cr_helper(){ bf=$(phome agi-belam)/.gitconfig;[ "$(ngit)" = 1 ]&&[ -f "$bf" ]&&grep -q 'git-credential' "$bf"&&[ "$(awk '/^\[credential "https:\/\/github.com"\]$/{p=1;print;next} p&&/^\t/{print;next} {p=0}' "$bf")" = "$(hl)" ];}
creds_ok(){ cr_sudo&&cr_reach >/dev/null&&cr_helper&&cr_gh;}
sudo_note(){ case $(cat "$SUDOERS" 2>/dev/null) in *ALL*ALL*)echo "[sudoers] present, byte-equal to the cell; BROAD grant (ALL), owner ruling pending";; esac;}
sk_host(){ up_host check||return 1;creds_ok||return 1;sudo_note;}
su_host(){ up_host check >/dev/null 2>&1||exit 1
 if [ -f "$SUDOERS" ];then cr_sudo||{ sl=$(cell .sudoers_line);[ -n "$sl" ]&&[ "$sl" != null ]||die "[sudoers] $SUDOERS exists and the cell values.local_maxxing.agi_town.sudoers_line is absent at $PIN: its bytes cannot be checked, nothing written"
   die "[sudoers] $SUDOERS differs from the cell sudoers_line and from the narrow line: nothing written";};sudo_note
 else command -v visudo >/dev/null 2>&1||owner_do "sudo apt-get install -y sudo   # visudo is absent: then put this ONE line in $SUDOERS (0440 root): $(narrow)"
  t=$(mktemp "$SUDOERS.XXXXXX")||die "[sudoers] cannot make a temp file beside $SUDOERS: nothing written"
  { narrow;echo;}>"$t"&&visudo -cf "$t" >/dev/null 2>&1||{ rm -f "$t";die "[sudoers] visudo refused the line: $SUDOERS not written";}
  chmod 0440 "$t"&&{ [ -n "$ROOT" ]||chown root:root "$t";}&&mv "$t" "$SUDOERS"||{ rm -f "$t";die "[sudoers] cannot install $SUDOERS: nothing written";};echo "[sudoers] wrote the narrow one-command line to $SUDOERS";fi
 u=$(cr_reach)||die "[sudoers] $u holds a sudo grant that runs as $PU (only agi-belam may): remove it by hand; nothing written"
 if [ "$(ngit)" != 0 ]&&! cr_helper;then die "[creds] the gh credential helper is in $(ngit) global git config(s) or differs from belam's order (an empty helper first, then the sudo line): want exactly one, agi-belam's; nothing written";fi
 [ "$(ngit)" != 0 ]||{ bf=$(phome agi-belam)/.gitconfig;hl|au agi-belam sh -c 'cat >>"$1"' x "$bf"||die "[creds] cannot write $bf";echo "[creds] wrote the gh helper lines to $bf";}
 cr_gh||owner_do "sudo -u $PU gh auth login   # the token stays in uid $PU";}
# --- posts (S5 + S6)
rows(){ g show "$PIN:.agi/nodes/.geometry/posts.md"|sed -n 's/^  - {/{/p'|jq -r --arg x "$BOX" 'select(has("harness") and .box==$x)|.name';}
pset(){ if grep -q '^stopped ' "$STATE" 2>/dev/null;then sed -n 's/^running //p' "$STATE";else rows;fi;}   # a stopped town: its recorded set; a fresh box: the AGI_BOX rows
isup(){ systemctl is-active -q "agi-post@$1.service";}
nostart(){ for p in $(pset);do isup $p||echo $p;done;}
nologin(){ for p in $(pset);do [ -s "$(phome agi-$p)/.claude/.credentials.json" ]||echo $p;done;}
bootok(){ [ "$(systemctl is-enabled agi-boot.service 2>/dev/null)" = enabled ];}
# the four first-run flags (belam's measure): folder trust (.claude.json projects[MAIN]), the bypass offer (settings.json), the renderer offer + fullscreen (settings.json tui + .claude.json fullscreenUpsellSeenCount>=3), onboarding
flags_ok(){ h=$(phome agi-$1);[ -n "$h" ]&&jq -e --arg m "$AGI_REPO" '.hasCompletedOnboarding==true and (.fullscreenUpsellSeenCount//0)>=3 and .projects[$m].hasTrustDialogAccepted==true' "$h/.claude.json" >/dev/null 2>&1&&jq -e '.skipDangerousModePermissionPrompt==true and .tui=="default"' "$h/.claude/settings.json" >/dev/null 2>&1&&[ "$(stat -c %a "$h/.claude.json")" = 600 ]&&[ "$(stat -c %a "$h/.claude/settings.json")" = 600 ];}
noflags(){ for p in $(pset);do flags_ok $p||echo $p;done;}
flags_do(){ h=$(phome agi-$1);[ -n "$h" ]||die "[posts] no user agi-$1 (the agi-* users are the owner's act)"
 au agi-$1 sh -c 'umask 077;f=$1;shift;mkdir -p "$(dirname "$f")";[ -s "$f" ]||echo "{}" >"$f";jq "$@" "$f" >"$f.new"&&mv "$f.new" "$f"&&chmod 600 "$f"' x "$h/.claude.json" --arg m "$AGI_REPO" '.hasCompletedOnboarding=true|.fullscreenUpsellSeenCount=(if (.fullscreenUpsellSeenCount//0)<3 then 3 else .fullscreenUpsellSeenCount end)|.projects[$m].hasTrustDialogAccepted=true'||die "[posts] cannot write $h/.claude.json"
 au agi-$1 sh -c 'umask 077;f=$1;shift;mkdir -p "$(dirname "$f")";[ -s "$f" ]||echo "{}" >"$f";jq "$@" "$f" >"$f.new"&&mv "$f.new" "$f"&&chmod 600 "$f"' x "$h/.claude/settings.json" '.skipDangerousModePermissionPrompt=true|.tui="default"'||die "[posts] cannot write $h/.claude/settings.json";}
# agi-boot's own load gate, read from the same cells at the pin, for a post it does not start (not boot:true)
gate_ok(){ l=;read l _ <${AGI_LOADAVG:-/proc/loadavg};i=$(sed -n 's/^some .*avg60=\([0-9.]*\).*/\1/p' ${AGI_PSI_IO:-/proc/pressure/io} 2>/dev/null);[ -n "$l" ]&&[ -n "$i" ]&&awk -v l=$l -v i=$i -v L=$GL -v P=$GP 'BEGIN{exit !(l<L&&i<P)}';}
gate_wait(){ c(){ g show "$PIN:.agi/config.json"|jq -r ".values.local_maxxing.$1";};GL=$(c de_live_parents.ceiling_if.loadavg1_lt);GP=$(c de_live_parents.ceiling_if.io_psi_some_avg60_lt);GN=$(c agi_boot.poll_s);GM=$(c agi_boot.wait_max_s)
 for v in "$GL" "$GP" "$GN" "$GM";do case $v in ""|*[!0-9.]*)die "[gate] a load-gate cell is not a plain number at $PIN: nothing started";; esac;done
 gs=$(date +%s);until gate_ok;do [ $(($(date +%s)-gs)) -ge "$GM" ]&&return 1;sleep "$GN";done;}
# S5 reads the ring row at the pin (.agi/nodes/.geometry/ring; ABSENT at the pin = the one line `[ring] no ring at <pin>: the old gate, nothing to verify`, i.e. ring: unverified) against each post's own ~/.ssh/id_ed25519.pub and writes NO commit (council 10-21: the post's own unit mints its key and commits its row). An unreadable read (git show fails, no key file, no permission) is LISTED, never a match and never skipped; a differing key is listed and start goes on.
ringcheck(){ m=0;c=0
 if ro=$(g ls-tree --name-only "$PIN" .agi/nodes/.geometry/ring 2>/dev/null)&&[ -z "$ro" ];then echo "[ring] no ring at $PIN: the old gate, nothing to verify";return 0;fi   # (3) council 10-21: the ring is absent until an agi-out ring commit has run: ONE line, not M `unread`
 rg=$(g show "$PIN:.agi/nodes/.geometry/ring" 2>&1)&&rok=1||rok=
 for p in $(pset);do m=$((m+1));h=$(phome agi-$p)
  [ -n "$rok" ]||{ echo "[ring] $p: unread (git show $PIN:.agi/nodes/.geometry/ring: $(echo "$rg"|head -1|cut -c1-90))" >&2;continue;}
  k=$(cut -d' ' -f2 "$h/.ssh/id_ed25519.pub" 2>/dev/null)&&[ -n "$k" ]||{ echo "[ring] $p: unread (no readable key file $h/.ssh/id_ed25519.pub)" >&2;continue;}
  c=$((c+1));r=$(echo "$rg"|awk -v p=$p '$1==p&&$2=="ssh-ed25519"{print $3}'|tail -1)
  if [ -z "$r" ];then echo "[ring] $p: no ssh-ed25519 row at $PIN" >&2;elif [ "$r" != "$k" ];then echo "[ring] $p: key differs" >&2;fi;done
 echo "[ring] checked $c of $m posts";[ "$m" = 0 ]||[ "$c" != 0 ]||echo "[ring] WARNING: 0 of $m posts could be checked: the ring is UNVERIFIED" >&2;}
sk_posts(){ [ -z "$(nostart)$(noflags)$(nologin)" ]&&bootok;}
su_posts(){ if [ ! -e "$STARTING" ];then (umask 077;utc >"$STARTING.tmp")&&mv "$STARTING.tmp" "$STARTING"&&chmod 600 "$STARTING"||die "[posts] cannot write $STARTING: nothing started";fi   # cond 7: before the first unit
 nf=$(noflags)
 for p in $nf;do isup $p&&{ systemctl stop "agi-post@$p.service"||die "[posts] cannot stop $p before its flags";};done   # (2) council 10-21: Claude Code writes its in-memory ~/.claude.json back on exit, so a post lacking flags is stopped FIRST (its SIGTERM write lands now); the flags are written with NO post of theirs up, then the starts below bring them up
 for p in $nf;do flags_do $p;done                                                  # FIRST the flags, each written as that user, 600 (B1: before any agi-boot call)
 bootok||systemctl enable agi-boot.service||die "[posts] cannot enable agi-boot.service";bootok||die "[posts] agi-boot.service reads '$(systemctl is-enabled agi-boot.service 2>/dev/null)' after its enable, want exactly 'enabled': nothing more started"   # THEN agi-boot (unchanged); a stopped town's unit is still active (exited), so a restart re-runs it
 [ -z "$(nostart)" ]||systemctl restart agi-boot.service||die "[posts] agi-boot.service failed"
 bad=;for p in $(nostart);do gate_wait&&systemctl start "agi-post@$p.service"||bad="$bad $p";done
 [ -z "$bad" ]||die "[posts] cannot start:$bad (listed; a re-run retries them)"
 ringcheck
 np=$(nologin);if [ -n "$np" ];then for p in $np;do echo "[owner-do] AGI_MOVE_TO=$BOX sh $MAIN/extensions/agi/guard/box-move.sh url $p   # open the URL, then: printf %s CODE | AGI_MOVE_TO=$BOX sh $MAIN/extensions/agi/guard/box-move.sh login $p";done;exit 21;fi;}   # S6: rc 21, AFTER S5 started the posts, BEFORE S9
# --- crons (S7): apply, then apply --sudo, as agi-belam (the uid that holds the main block)
sk_crons(){ au agi-belam $CR show --root "$MAIN" 2>/dev/null|grep -q '^status: up to date';}
su_crons(){ au agi-belam $CR apply --root "$MAIN"||die "[crons] apply failed";au agi-belam $CR apply --sudo --root "$MAIN"||die "[crons] apply --sudo failed";}
# --- units (S8): the agi-* units town.state recorded (`unit NAME enabled|plain`): enable the enabled ones, start all
ulines(){ sed -n 's/^unit //p' "$STATE" 2>/dev/null;}
sk_units(){ ulines|while read n m;do [ "$m" != enabled ]||[ "$(systemctl is-enabled "$n" 2>/dev/null)" = enabled ]||exit 1;case $(systemctl is-active "$n" 2>/dev/null) in active|activating);;*)exit 1;;esac;done;}   # B-6 (council 10-21): every recorded unit must be UP too, else start's last line would lie
su_units(){ ulines|while read n m;do if [ "$m" = enabled ];then systemctl enable "$n"||exit 1;[ "$(systemctl is-enabled "$n" 2>/dev/null)" = enabled ]||{ echo "[units] $n reads '$(systemctl is-enabled "$n" 2>/dev/null)' after its enable, want exactly 'enabled'" >&2;exit 1;};fi;systemctl start "$n"||echo "[units] cannot start $n" >&2;case $(systemctl is-active "$n" 2>/dev/null) in active|activating);;*)echo "[units] $n is not active after its start (town.state and town.starting are kept: fix it, re-run start)" >&2;;esac;done||die "[units] a unit town.state recorded as enabled did not come back enabled: re-run start after fixing it";}
# --- blast (S9): `box town up <pin>` as agi-belam, the read-back, and LAST town.state moved aside whole (R6: never edited) with town.starting removed in the same act
sent_all(){ for p in $(pset);do c=$(g rev-parse -q --verify "refs/box/belam/$p" 2>/dev/null)||return 1;[ "$(g log -1 --format=%B $c)" = "[town] up $PIN" ]||return 1;done;}
# ONLY 'Try the new fullscreen renderer' is a MEASURED title (belam saw it in a pane); the other five are Claude Code's known texts, UNMEASURED (no login in a scratch HOME reaches them): a constant, not a cell. S3 BIND (council 10-21): a post counts up only at the measured ready marker (the prompt), an unknown dialog in ~/o makes blast unmet.
TITLES='Try the new fullscreen renderer|Quick safety check|Do you trust the files in this folder|Bypass Permissions mode|Select login method|Choose the text style';MEASURED='Try the new fullscreen renderer'
stuck(){ for p in $(pset);do t=$(tail -c 6000 "$(phome agi-$p)/o" 2>/dev/null|sed -E 's/\x1b\[[0-9;?]*[a-zA-Z]//g;s/\x1b\][^\a]*\a//g'|tr -d ' \r\n');
   echo "$TITLES"|tr '|' '\n'|while read -r ti;do case $t in *"$(printf %s "$ti"|tr -d ' ')"*)printf '%s\t%s\n' "$p" "$ti";break;; esac;done;done;}   # post name + dialog title only, never the tail bytes
sk_blast(){ sent_all&&[ -z "$(stuck)" ]&&[ ! -e "$STARTING" ]&&! grep -q '^stopped ' "$STATE" 2>/dev/null;}
su_blast(){ echo "[blast] dialog probe: $(echo "$TITLES"|tr '|' '\n'|grep -vxF "$MEASURED"|wc -l|tr -d ' ') of $(echo "$TITLES"|tr '|' '\n'|wc -l|tr -d ' ') titles unmeasured"
 if ! sent_all;then BOXB=${AGI_TOWN_BOXBIN:-$(phome agi-belam)/bin/box};TB=$(g branch --show-current);[ -n "$TB" ]||die "[trunk] MAIN has no checked-out branch: nothing sent"
  (cd "$MAIN"&&sudo -H -u agi-belam env AGI_POST=belam AGI_BOX=$BOX AGI_TRUNK=$TB $BOXB town up $PIN)||die "[blast] box town up $PIN failed";fi
 st=$(stuck);if [ -n "$st" ];then echo "$st"|while IFS="$(printf '\t')" read -r p ti;do echo "[dialog] $p is stuck at: $ti" >&2;done;die "[blast] $(echo "$st"|wc -l|tr -d ' ') post(s) are stuck at a first-run dialog (listed above): town.state kept, re-run start";fi
 [ ! -e "$STATE" ]||mv "$STATE" "$STATE.$(utc)"||die "[state] cannot move $STATE aside";rm -f "$STARTING";}
ck_main(){ return 0;}
dn_main(){ return 0;}   # S3 adds the pack / ring down arm
cmd_start(){ [ $# = 0 ]||die "start: unknown argument '$1' (--from PACK is S3)"
 # R-d (council 10-21): a ROOT rehearsal of start must not reach the live box: AGI_HOST_UNITS=<stub dir> must hold the tools it calls
 [ -z "$ROOT" ]||{ [ -n "$AGI_HOST_UNITS" ]||die "[root] ROOT is set: AGI_HOST_UNITS=<stub dir> must hold systemctl sudo visudo gh crontab (a rehearsal never reaches the real ones): nothing written"
  for c in systemctl sudo visudo gh crontab;do case $(command -v $c 2>/dev/null) in "$AGI_HOST_UNITS"/*);;*)die "[root] AGI_HOST_UNITS needs stubs: $c does not resolve inside $AGI_HOST_UNITS: nothing written";; esac;done;}
 need;[ -n "$ROOT" ]||[ "$(id -u)" = 0 ]||die "[root] start needs root: nothing started"
 s0;inputs;SCR=$(mktemp -d)||die "[tmp] no scratch dir";trap 'rm -rf "$SCR"' 0
 AGI_REPO=$MAIN;if [ -n "$ROOT" ];then case $MAIN in "$ROOT"/*)AGI_REPO=${MAIN#"$ROOT"};;*)die "[root] ROOT is set but MAIN ($MAIN) is not inside it";; esac;fi
 export PIN AGI_BOX=$BOX AGI_REPO PRIME_USER=$PU
 sk_main||su_main;sk_main||die "[main] still unmet after its up arm"   # the clone comes first: the row is read from MAIN at the pin
 ROW=$(g show "$PIN:.agi/nodes/.geometry/engine.md" 2>/dev/null|sed -n '/^### matrix /,/^### /{/^~~~/,/^~~~/{//!p}}'|awk -F'\t' '$1=="town"&&$2=="start"{print $3}')
 [ -n "$ROW" ]||die "[matrix] no 'town start' row in engine.md at $PIN: nothing started"
 for s in $ROW;do { command -v sk_$s >/dev/null 2>&1&&command -v su_$s >/dev/null 2>&1;}||die "[step] '$s' (matrix row) has no up arm in this agi.sh: nothing started";done
 TRK=$PIN
 for s in $ROW;do sk_$s||{ su_$s;sk_$s||die "[step] $s: still unmet after its up arm";};echo "start: $s met";done
 echo "started $BOX at $PIN";}
ck_host(){ return 0;}
dn_host(){ return 0;}
r=${1:-};[ $# = 0 ]||shift
case $r in
status)prep;status;;
stop)cmd_stop "$@";;
answer)cmd_answer "$@";;
host)up_host "$@";;
start)cmd_start "$@";;
*)die "usage: agi.sh status | stop [--pack OUT] | start | answer KEY VALUE | host";;
esac
