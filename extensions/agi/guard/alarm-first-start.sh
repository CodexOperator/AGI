#!/bin/sh
# alarm-first-start.sh -- belam's host act, ONCE, as root, after the installs of goal:g7.16.1.11.20.2 (council 3/3 23:0xZ item 5).
# It proves the alarm path on the box before the first real alarm does:
#   (1) r1 over the INSTALLED scripts (/usr/local/sbin + /opt/agi/bin): 0 lines that `box` + `send` or `ssh-keygen -Y sign`, COMMENT lines
#       skipped (agi-signers-repoint:4 and box:2 are comments). A hit = rc 1, file:line printed. Root signs nothing and holds no key.
#   (2) per drain row ONE hand-spooled test line reaches its reader G-SIGNED with Alarm-job + Alarm-id: the line is appended AS the sending
#       seat (a plain append, exactly what a root source does), then the seat's own drain runs once AS the seat (what the alarm_drain /
#       alarm_drain_belam cron row runs), then the seat's out-ref refs/box/<seat>/<reader> must carry a commit with the marker, both
#       trailers, and a signature "for <seat>@agi with" (what box read checks). A miss = rc 2.
# The reader then sees it with: AGI_POST=<reader> box read.
# Env (defaults are the box's): SBIN OPTBIN STORES AS RUNUSER BOXBIN VERIFY ROWS ("seat:reader seat:reader"; an EMPTY ROWS skips the drain rows, only r1 runs).
SBIN=${SBIN:-/usr/local/sbin};OPTBIN=${OPTBIN:-/opt/agi/bin};STORES=${STORES:-/var/lib/agi};AS=${AS:-/opt/agi/bin/alarm_spool.py}
RUNUSER=${RUNUSER:-runuser};ROWS=${ROWS-"sanctuary-master:belam belam:sanctuary-master"};VERIFY=${VERIFY:-"git verify-commit --raw"}
rc=0
# (1) the root scripts carry no signing and no mail send
hits=$(grep -rInE 'box[[:space:]]+send|ssh-keygen[[:space:]]+-Y[[:space:]]+sign' "$SBIN" "$OPTBIN" 2>/dev/null | grep -vE '^[^:]*:[0-9]+:[[:space:]]*#')
if [ -n "$hits" ];then echo "RED r1: a root script signs or sends:";echo "$hits";rc=1;else echo "ok r1: 0 uncommented signing or send lines in $SBIN and $OPTBIN";fi
# (2) one hand-spooled line per drain row, sent by the seat's own drain, signed by the seat
now=$(date +%s)
for row in $ROWS;do
 seat=${row%%:*};reader=${row#*:};marker="first-start-$now-$seat"
 as(){ "$RUNUSER" -u "agi-$seat" -- env HOME="$STORES/$seat" AGI_POST="$seat" "$@"; }
 as python3 "$AS" append --job first-start --to "$reader" --text "$marker" --max-lines 500 --spool "$STORES/$seat/alarm.spool" \
  || { echo "RED $seat: the plain append failed";rc=2;continue;}
 if [ -n "$BOXBIN" ];then as python3 "$AS" drain --seat "$seat" --max-tries 60 --box-bin "$BOXBIN";else as python3 "$AS" drain --seat "$seat" --max-tries 60;fi \
  || { echo "RED $seat: the drain failed";rc=2;continue;}
 h=$(as sh -c 'cd ~/t && git log "refs/box/$0/$1" -n 50 --grep="$2" --format=%H | head -1' "$seat" "$reader" "$marker" 2>/dev/null)
 [ -n "$h" ] || { echo "RED $seat -> $reader: no commit with $marker on refs/box/$seat/$reader";rc=2;continue;}
 msg=$(as sh -c 'cd ~/t && git log -1 --format=%B "$0"' "$h" 2>/dev/null)
 sig=$(as sh -c 'cd ~/t && $0 "$1" 2>&1' "$VERIFY" "$h")
 case $msg in *"Alarm-job: first-start"*"Alarm-id: "*) ;; *) echo "RED $seat -> $reader: $h lacks the Alarm-job / Alarm-id trailers";rc=2;continue;; esac
 case $sig in *"for $seat@agi with"*) echo "ok $seat -> $reader: $h is signed by $seat with its trailers (reader: AGI_POST=$reader box read)";; *) echo "RED $seat -> $reader: $h is not signed by $seat";rc=2;; esac
done
exit $rc
