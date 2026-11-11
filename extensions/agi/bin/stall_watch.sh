#!/bin/sh
# stall_watch.sh (config:crons stall_watch; owner 01:1xZ 10-25: "Are we also checking to see if anyone is stalled out" ·
# "let's add it just make it graph native like the other scripts do it's easy to start and stop"). agi-quiet-watch sees the
# WHOLE town idle; nothing saw ONE post stuck while the rest work. Every run, for each post in the boot set (the agi-post@
# wants links) but SELF, read with NO root and NO screen bytes (a post's ~/o and transcripts are 0600 to its own uid):
#   down      its unit is not active
#   no-claude its unit has been active >= G s and runs no claude process
#   mail      it has unread box mail whose oldest message is >= U s old AND its screen log (~/o, mtime only) has not
#             changed for >= W s -- the mail wake did not land: a dialog, an error, a hung pane
# A post busy on a long tool redraws its spinner, so its ~/o is fresh and it is never flagged. All named posts go in ONE
# line appended to SELF's alarm spool; SELF's drain (config:crons alarm_drain_belam) signs and box-sends it to TO. It
# ACTS ON NOTHING: no keys typed, no restarts. A post's line repeats at most once per GAP s while the same condition
# holds; a new condition, or the condition clearing and coming back, re-alerts. Stop/start: the `enabled:` cell of
# cadences.stall_watch in .agi/nodes/.geometry/crons.md, then `crons.py apply --sudo` (the row names user agi-belam).
# A check that cannot read its input says `unread`, never "nobody stalled" (council 3/3 01:4xZ 10-25, rows 1-4): no refs/box or an
# empty boot set (besides SELF) = rc 1; a post whose ~/o or unit start time cannot be read is NAMED `unread-screen:` /
# `unread-start:`. The GAP key is the CAUSE (council 02:0xZ 10-25, N2), so a changed cause re-alerts inside GAP.
# HUB CAUSE (goal:g7.16.1.11.46.35; 14:22Z-19:34Z 11-10 hub A could not reach upstream, 20:53Z-06:01Z it sat in a 429
# cooldown, and this watch said `mail`, a symptom): a post that looks stalled (mail / unread-screen / no-claude) is read
# against two host-written files in HUBDIR (a root timer reads the hub's journal and the post's route; shape agreed
# DG2 + belam 06:5xZ 11-11), each with line 1 `written EPOCH`:
#   route  `POST HUB MODEL` (MODEL = the id the hub logs for that post) or `POST direct`
#   state  `HUB MODEL ok|quota|hub-down T LAST` and, while a hub is down, `HUB - hub-down T LAST` (T: quota = reset, 0 = none
#          given; hub-down = since; ok = the last 200. LAST = the hub's newest log line, any status: `written` proves the
#          timer fresh, LAST the state; LAST older than HUBMAX adds `, last seen HH:MMZ`; alive 06:50Z)
# In order: a file unreadable / without `written` / older than HUBMAX, no route row, or a hub route with no MODEL
# = `unread-hub:` (named, run rc 1, never quiet, never quota); `direct` = the symptom stands; the hub's `-` hub-down line
# FIRST = `hub-down: hub A (no upstream) since HH:MMZ`; then that HUB+MODEL's quota line = `quota: hub A (M) until
# HH:MMZ` (`until unknown` for T 0; `reset HH:MMZ passed, not confirmed` once T is past); ok or no line = the symptom.
# Cells (a test points them at fixtures): --repo (MAIN) STORES WANTS STATE SELF TO AS SPOOL U W G GAP NOW DRY=1 (print, no spool)
# HUBDIR HUBMAX.
R=;while [ $# -gt 0 ];do case $1 in --repo)R=$2;shift 2;;*)echo "stall_watch: unknown arg $1">&2;exit 2;;esac;done
R=${R:-/data/work/agi};STORES=${STORES:-/var/lib/agi};WANTS=${WANTS:-/run/systemd/system/multi-user.target.wants}
STATE=${STATE:-$HOME/.stall-watch};SELF=${SELF:-belam};TO=${TO:-sanctuary-master}
AS=${AS:-$R/extensions/agi/bin/alarm_spool.py};SPOOL=${SPOOL:-$STORES/$SELF/alarm.spool}
U=${U:-1200};W=${W:-600};G=${G:-300};GAP=${GAP:-3600};now=${NOW:-$(date +%s)}
HUBDIR=${HUBDIR:-/run/agi-hub};HUBMAX=${HUBMAX:-180}
mkdir -p "$STATE"||{ echo "stall_watch: STATE $STATE not writable">&2;exit 1;}
[ -d "$WANTS" ]||{ echo "stall_watch: unread: no wants dir $WANTS (the boot set)">&2;exit 1;}
git -C "$R" rev-parse -q --git-dir >/dev/null 2>&1||{ echo "stall_watch: unread: $R is not a git repo (mail refs)">&2;exit 1;}
[ -n "$(git -C "$R" for-each-ref --count=1 refs/box)" ]||{ echo "stall_watch: unread: no refs/box in $R">&2;exit 1;}   # (3) sp: no mail refs would read every post k = 0
PS=$(ls "$WANTS"|sed -n 's/^agi-post@\([a-z0-9-]*\)\.service$/\1/p'|grep -vx "$SELF");[ -n "$PS" ]||{ echo "stall_watch: unread: boot set empty besides $SELF ($WANTS)">&2;exit 1;}   # (4) sp; (N1) SELF dropped first
m(){ echo $(($1/60))m;}
hz(){ date -u -d @"$1" +%H:%MZ 2>/dev/null||echo "?";}
fresh(){ [ -f "$1" ]&&[ -r "$1" ]||return 1;read -r w1 w2 <"$1" 2>/dev/null||return 1   # $1 a host file: readable, `written` line 1, young
 [ "$w1" = written ]&&[ "$w2" -eq "$w2" ] 2>/dev/null&&[ $((now-w2)) -lt "$HUBMAX" ];}
num(){ [ -n "$1" ]&&[ "$1" -eq "$1" ] 2>/dev/null;}
ls1(){ [ $((now-$1)) -ge "$HUBMAX" ]&&echo ", last seen $(hz "$1")";}   # the state's own age, not the timer's
hub(){   # $1 post, $2 its symptom line -> prints the line to say
 for x in route state;do fresh "$HUBDIR/$x"||{ echo "unread-hub: $HUBDIR/$x not readable, unwritten or older than ${HUBMAX}s ($2)";return;};done
 set -- "$1" "$2" $(awk -v p="$1" 'NR>1&&$1==p{print $2,$3;exit}' "$HUBDIR/route")
 [ -n "$3" ]||{ echo "unread-hub: no route row for $1 ($2)";return;}
 [ "$3" = direct ]&&{ echo "$2";return;}
 [ -n "$4" ]||{ echo "unread-hub: $1 on hub $3 with no model id ($2)";return;}
 set -- "$1" "$2" "$3" "$4" $(awk -v h="$3" 'NR>1&&$1==h&&$2=="-"&&$3=="hub-down"{print $4,$5,"x";exit}' "$HUBDIR/state")
 if [ -n "$5" ];then num "$5"&&num "$6"||{ echo "unread-hub: hub $3 hub-down line not \`T LAST\` ($2)";return;}
  echo "hub-down: hub $3 (no upstream) since $(hz "$5")$(ls1 "$6"|sed 's/last seen/last failed dial/')";return;fi   # sp 07:05Z: LAST there is the newest FAILED dial
 set -- "$1" "$2" "$3" "$4" $(awk -v h="$3" -v md="$4" 'NR>1&&$1==h&&$2==md&&$3=="quota"{print $4,$5,"x";exit}' "$HUBDIR/state")
 [ -z "$5" ]||{ num "$5"&&num "$6";}||{ echo "unread-hub: hub $3 ($4) quota line not \`T LAST\` ($2)";return;}
 if [ -z "$5" ];then echo "$2"
 elif [ "$5" = 0 ];then echo "quota: hub $3 ($4) until unknown$(ls1 "$6")"
 elif [ "$5" -gt "$now" ];then echo "quota: hub $3 ($4) until $(hz "$5")$(ls1 "$6")"
 else echo "quota: hub $3 ($4) reset $(hz "$5") passed, not confirmed$(ls1 "$6")";fi
}
out=;n=0;uh=0
for x in $PS;do
 p=$x;c=
 st=$(systemctl show "agi-post@$p.service" -p ActiveState --value 2>/dev/null)
 if [ "$st" != active ];then c="down: unit ${st:-unknown}"
 elif ! pgrep -u "agi-$p" -x claude >/dev/null 2>&1;then
  ts=$(systemctl show "agi-post@$p.service" -p ActiveEnterTimestamp --value 2>/dev/null);t=   # (2) aio: date -d "" is today's midnight, rc 0
  [ -n "$ts" ]&&t=$(date -d "$ts" +%s 2>/dev/null)
  if [ -z "$t" ];then c="unread-start: unit start time not readable (no claude process)"
  elif [ $((now-t)) -ge "$G" ];then c="no-claude: unit active $(m $((now-t))), no claude process";fi
 else
  k=0;o=
  for r in $(git -C "$R" for-each-ref --format='%(refname)' refs/box|grep "/$p\$");do
   f=${r#refs/box/};f=${f%/*};h=$(git -C "$R" rev-parse -q --verify "refs/held/$p/$f")
   for ct in $(git -C "$R" log --format=%ct "$r" ${h:+--not "$h"});do k=$((k+1));[ -z "$o" ]||[ "$ct" -lt "$o" ]&&o=$ct;done
  done
  s=$(stat -c %Y "$STORES/$p/o" 2>/dev/null)
  if [ "$k" -gt 0 ]&&[ $((now-o)) -ge "$U" ];then
   if [ -z "$s" ];then c="unread-screen: screen log not readable (mail $k unread, oldest $(m $((now-o))))"   # (1) alive
   elif [ $((now-s)) -ge "$W" ];then c="mail: $k unread, oldest $(m $((now-o))), screen still $(m $((now-s)))";fi
  fi
 fi
 if [ -z "$c" ];then rm -f "$STATE/$p";continue;fi
 case ${c%%:*} in mail|unread-screen|no-claude)c=$(hub "$p" "$c");;esac
 [ "${c%%:*}" = unread-hub ]&&uh=$((uh+1))
 kind=${c%%:*};read -r lk lt 2>/dev/null <"$STATE/$p"||{ lk=;lt=0;}
 [ "$kind" = "$lk" ]&&[ $((now-lt)) -lt "$GAP" ]&&continue
 echo "$kind $now">"$STATE/$p";out="$out${out:+ · }$p: $c";n=$((n+1))
done
rc=0;[ "$uh" -gt 0 ]&&rc=1
[ "$n" -gt 0 ]||exit $rc
msg="[stall] stall-watch $(date -u -d @"$now" +%H:%MZ) -> $TO: $n post(s) look stalled: $out. Read the screen (sudo tail -c 4000 /var/lib/agi/<post>/o), then wake it, answer its dialog or restart it; this watch acts on nothing. Stop it: cadences.stall_watch enabled: false in config:crons + crons.py apply --sudo."
echo "$msg"
[ -n "$DRY" ]&&exit $rc
python3 "$AS" append --job stall-watch --to "$TO" --text "$msg" --max-lines 500 --spool "$SPOOL"||{ echo "stall_watch: spool append FAILED: $msg">&2;for x in $(ls "$STATE");do rm -f "$STATE/$x";done;exit 1;}
exit $rc
