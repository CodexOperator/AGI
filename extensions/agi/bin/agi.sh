#!/bin/sh
# agi.sh status | stop [--pack OUT] | answer KEY VALUE | start (S2, not yet): the town's stop (goal:g7.16.1.11.44.8, S1; council 3/3 10-15 19:36Z + 19:41Z).
# The step order is READ from the matrix row `town<TAB>start<TAB>posts crons units blast<TAB>agi.sh` (engine.md ### matrix, at the pin): START runs the names left to right, STOP right to
# left (blast, units, crons, posts); every name is one function pair, ck_<name> (met?) and dn_<name> (the down arm). A re-run resumes at the first unmet check.
# Captive: ONE `[ask] KEY: question` per run (rc 20, answered with `answer KEY VALUE`), `[owner-do] command` (rc 21) for what only the owner can type; answers go to town.env (root 600, no secret, never in git); town.state is root-written 644: no secret in it, and sanctuary-watch (a user timer) reads its `stopped` line.
# Cells (env; a test points them at stubs): AGI_MAIN (/data/work/agi) · AGI_TOWN_ENV (/etc/agi/town.env) · AGI_TOWN_STATE (/etc/agi/town.state) · AGI_CARRY_ENV (/etc/agi/carry.env: the pin) · AGI_WANTS_DIR ·
# AGI_TOWN_BOXBIN (belam's box). Config: .agi/config.json values.local_maxxing.agi_town = {keep_units, ack_wait_s}, read at the pin. No credential here; no git write except through `box town` (uid agi-belam).
D=$(cd "$(dirname "$0")" && pwd)
MAIN=${AGI_MAIN:-/data/work/agi};ENVF=${AGI_TOWN_ENV:-/etc/agi/town.env};STATE=${AGI_TOWN_STATE:-/etc/agi/town.state}
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
 case $v in /*);;*)for w in $(echo "$v"|tr './:@+=' ' ');do [ ${#w} -lt 32 ]||die "[secret] a segment of 32+ token chars (between . : / @ + =) is refused: town.env holds no secret (a value starting with / is a path)";done;;esac
 { grep -v "^$k=" "$ENVF" 2>/dev/null;echo "$k=$v";} >"$ENVF.tmp"&&chmod 600 "$ENVF.tmp"&&mv "$ENVF.tmp" "$ENVF"||die "[answer] cannot write $ENVF";echo "answered $k";}
r=${1:-};[ $# = 0 ]||shift
case $r in
status)prep;status;;
stop)cmd_stop "$@";;
answer)cmd_answer "$@";;
start)die "start: S2, not yet";;
*)die "usage: agi.sh status | stop [--pack OUT] | answer KEY VALUE";;
esac
