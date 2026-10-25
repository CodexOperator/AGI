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
# empty boot set = rc 1; a post whose ~/o or unit start time cannot be read is NAMED `unread: ...`.
# Cells (a test points them at fixtures): --repo (MAIN) STORES WANTS STATE SELF TO AS SPOOL U W G GAP NOW DRY=1 (print, no spool).
R=;while [ $# -gt 0 ];do case $1 in --repo)R=$2;shift 2;;*)echo "stall_watch: unknown arg $1">&2;exit 2;;esac;done
R=${R:-/data/work/agi};STORES=${STORES:-/var/lib/agi};WANTS=${WANTS:-/run/systemd/system/multi-user.target.wants}
STATE=${STATE:-$HOME/.stall-watch};SELF=${SELF:-belam};TO=${TO:-sanctuary-master}
AS=${AS:-$R/extensions/agi/bin/alarm_spool.py};SPOOL=${SPOOL:-$STORES/$SELF/alarm.spool}
U=${U:-1200};W=${W:-600};G=${G:-300};GAP=${GAP:-3600};now=${NOW:-$(date +%s)}
mkdir -p "$STATE"||{ echo "stall_watch: STATE $STATE not writable">&2;exit 1;}
[ -d "$WANTS" ]||{ echo "stall_watch: unread: no wants dir $WANTS (the boot set)">&2;exit 1;}
git -C "$R" rev-parse -q --git-dir >/dev/null 2>&1||{ echo "stall_watch: unread: $R is not a git repo (mail refs)">&2;exit 1;}
[ -n "$(git -C "$R" for-each-ref --count=1 refs/box)" ]||{ echo "stall_watch: unread: no refs/box in $R">&2;exit 1;}   # (3) sp: no mail refs would read every post k = 0
PS=$(ls "$WANTS"|sed -n 's/^agi-post@\([a-z0-9-]*\)\.service$/\1/p');[ -n "$PS" ]||{ echo "stall_watch: unread: boot set empty ($WANTS)">&2;exit 1;}   # (4) sp
m(){ echo $(($1/60))m;}
out=;n=0
for x in $PS;do
 p=$x;[ "$p" = "$SELF" ]&&continue;c=
 st=$(systemctl show "agi-post@$p.service" -p ActiveState --value 2>/dev/null)
 if [ "$st" != active ];then c="down: unit ${st:-unknown}"
 elif ! pgrep -u "agi-$p" -x claude >/dev/null 2>&1;then
  ts=$(systemctl show "agi-post@$p.service" -p ActiveEnterTimestamp --value 2>/dev/null);t=   # (2) aio: date -d "" is today's midnight, rc 0
  [ -n "$ts" ]&&t=$(date -d "$ts" +%s 2>/dev/null)
  if [ -z "$t" ];then c="unread: unit start time not readable (no claude process)"
  elif [ $((now-t)) -ge "$G" ];then c="no-claude: unit active $(m $((now-t))), no claude process";fi
 else
  k=0;o=
  for r in $(git -C "$R" for-each-ref --format='%(refname)' refs/box|grep "/$p\$");do
   f=${r#refs/box/};f=${f%/*};h=$(git -C "$R" rev-parse -q --verify "refs/held/$p/$f")
   for ct in $(git -C "$R" log --format=%ct "$r" ${h:+--not "$h"});do k=$((k+1));[ -z "$o" ]||[ "$ct" -lt "$o" ]&&o=$ct;done
  done
  s=$(stat -c %Y "$STORES/$p/o" 2>/dev/null)
  if [ "$k" -gt 0 ]&&[ $((now-o)) -ge "$U" ];then
   if [ -z "$s" ];then c="unread: screen log not readable (mail $k unread, oldest $(m $((now-o))))"   # (1) alive
   elif [ $((now-s)) -ge "$W" ];then c="mail: $k unread, oldest $(m $((now-o))), screen still $(m $((now-s)))";fi
  fi
 fi
 if [ -z "$c" ];then rm -f "$STATE/$p";continue;fi
 kind=${c%%:*};read -r lk lt 2>/dev/null <"$STATE/$p"||{ lk=;lt=0;}
 [ "$kind" = "$lk" ]&&[ $((now-lt)) -lt "$GAP" ]&&continue
 echo "$kind $now">"$STATE/$p";out="$out${out:+ · }$p: $c";n=$((n+1))
done
[ "$n" -gt 0 ]||exit 0
msg="[stall] stall-watch $(date -u -d @"$now" +%H:%MZ) -> $TO: $n post(s) look stalled: $out. Read the screen (sudo tail -c 4000 /var/lib/agi/<post>/o), then wake it, answer its dialog or restart it; this watch acts on nothing. Stop it: cadences.stall_watch enabled: false in config:crons + crons.py apply --sudo."
echo "$msg"
[ -n "$DRY" ]&&exit 0
python3 "$AS" append --job stall-watch --to "$TO" --text "$msg" --max-lines 500 --spool "$SPOOL"||{ echo "stall_watch: spool append FAILED: $msg">&2;for x in $(ls "$STATE");do rm -f "$STATE/$x";done;exit 1;}
