#!/bin/sh
# post-move-checks.sh -- belam's per-move proof for a post rename (goal:g7.16.1.11.45 S2, design B: the agent keeps its OWN uid). Run as root.
#   post-move-checks.sh pre OLD NEW              BEFORE the usermod: prints the agent's uid (feed it to `check`) and proves NEW is a free name
#   post-move-checks.sh check OLD NEW UID T [--first-start]   AFTER the move: one line per check, `ok|FAIL|wait <name>: <detail>`; rc 1 if any FAIL
# OLD, NEW = post names (agi-<name> is the unix user and group); UID = what `pre` printed; T = the move's stamp, YYYYmmddHHMMSSZ (the dir
# /var/lib/agi/retired/keys/OLD-T and the allowed_signers valid-before). `wait` = not yet checkable (NEW's key line exists only once agi-out
# has run at the first start): not a FAIL, unless --first-start says that start has happened.
# Checks: uid · gid (name = agi-NEW, gid = uid) · old-name-free (passwd AND group) · key-held (retired dir root 700 holds the key) · key-unreadable
# (runuser -u agi-NEW -- test -r <retired key> fails, after a positive control so a runuser that cannot run is a FAIL, never a pass) ·
# key-not-in-home (no file under NEW's ~/.ssh is the retired key) · ring-old (every OLD@agi line closed, the last at T) · ring-new (no stale open
# NEW@agi line from an earlier holder of the name; after the first start exactly one open line, from T on, with a key OLD never held) ·
# grep-old (over sudoers.d polkit-1 /etc/systemd /run/systemd/system /etc/agi /var/spool/cron: nothing holds the word agi-OLD, nothing is NAMED agi-OLD, and nothing
# is a unit INSTANCE of OLD, `*@OLD.*`: every per-post unit is <unit>@<name>, so the wants links, the .service.d drop-ins and agi-carry@OLD.path are all caught; every
# scan dir must exist, a missing one is a FAIL naming it) · new-carry-path (agi-carry@NEW.path is enabled AND active: nothing else enables the new name's mail wake) ·
# old-post-inactive, old-boxwake-inactive (council addendum 15:26Z: AFTER the pin bump no agi-post@OLD / agi-boxwake@OLD is active; `systemctl is-active` must say
# inactive or failed, an empty answer or activating is a FAIL). Run it right after the move, before the name OLD is reused by a later move: old-name-free reads
# "empty" as the proof that no projection between the usermod and the bump minted a fresh agi-OLD.
# Env (defaults are the box's; a test sets them to stubs): ROOT (prefix of every default path) ID GETENT RUNUSER SYSTEMCTL ROOTUSER RET RING SCAN.
ROOT=${ROOT-};ID=${ID:-id};GETENT=${GETENT:-getent};RUNUSER=${RUNUSER:-runuser};SYSTEMCTL=${SYSTEMCTL:-systemctl};ROOTUSER=${ROOTUSER:-root}
RET=${RET:-$ROOT/var/lib/agi/retired/keys};RING=${RING:-$ROOT/var/lib/agi/allowed_signers}
SCAN=${SCAN-"$ROOT/etc/sudoers.d $ROOT/etc/polkit-1 $ROOT/etc/systemd $ROOT/run/systemd/system $ROOT/etc/agi $ROOT/var/spool/cron"}
f=0
say(){ _s=$1;_n=$2;shift 2;echo "$_s $_n: $*";[ "$_s" = FAIL ]&&f=$((f+1));:;}
t(){ _n=$1;_d=$2;shift 2;if "$@";then say ok "$_n" "$_d";else say FAIL "$_n" "$_d";fi;}
nm(){ case $1 in ""|*[!a-z0-9-]*)echo "post-move-checks: bad name '$1'" >&2;exit 2;;esac;}
mode=$1;OLD=$2;NEW=$3;nm "$OLD";nm "$NEW"
free(){ [ -z "$($GETENT passwd "agi-$1")" ]&&[ -z "$($GETENT group "agi-$1")" ];}
case $mode in
pre)u=$($ID -u "agi-$OLD" 2>/dev/null);g=$($ID -g "agi-$OLD" 2>/dev/null)
 t pre-old-user "agi-$OLD uid=${u:--} gid=${g:--} (the design keeps gid = uid)" test -n "$u" -a "$u" = "$g"
 t pre-new-free "no passwd and no group entry agi-$NEW yet" free "$NEW"
 echo "uid $u";[ $f = 0 ];exit $?;;
check)UID_=$4;T=$5;case $UID_ in ""|*[!0-9]*)echo "post-move-checks: UID '$UID_'" >&2;exit 2;;esac
 case $T in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]Z);;*)echo "post-move-checks: T '$T' is not YYYYmmddHHMMSSZ" >&2;exit 2;;esac;FIRST=$6;;
*)echo "usage: post-move-checks.sh pre OLD NEW | check OLD NEW UID T [--first-start]" >&2;exit 2;;
esac
n=agi-$NEW
# 1. the agent keeps its uid
got=$($ID -u "$n" 2>/dev/null);t uid "id -u $n = ${got:--}, the agent's old uid $UID_" test "$got" = "$UID_"
# 2. group renamed with the user, gid = uid
gn=$($ID -gn "$n" 2>/dev/null);gi=$($ID -g "$n" 2>/dev/null)
t gid "id -gn $n = ${gn:--} (want $n), gid ${gi:--} (want $UID_)" test "$gn" = "$n" -a "$gi" = "$UID_"
# 3. the old name is free, user AND group, before anything reuses it
t old-name-free "getent passwd agi-$OLD '$($GETENT passwd "agi-$OLD")', group '$($GETENT group "agi-$OLD")' (want both empty: no projection minted a fresh one)" free "$OLD"
# 4. the retired key is held by root alone
rk=$RET/$OLD-$T;pub=$(cut -d' ' -f1,2 "$rk/id_ed25519.pub" 2>/dev/null)
held(){ [ -f "$rk/id_ed25519" ]&&[ -n "$pub" ]&&[ "$(stat -c '%a %U' "$rk")" = "700 $ROOTUSER" ]; }
t key-held "$rk holds id_ed25519 + .pub, mode 700 owner $ROOTUSER (is $(stat -c '%a %U' "$rk" 2>/dev/null || echo absent))" held
# 5. the new uid cannot read it; the control proves runuser really acts as $n, else a failing runuser would pass this
home=$($GETENT passwd "$n"|cut -d: -f6)
cannot(){ "$RUNUSER" -u "$n" -- test -r "$home" || return 1;[ -f "$rk/id_ed25519" ]||return 1;! "$RUNUSER" -u "$n" -- test -r "$rk/id_ed25519"; }
t key-unreadable "runuser -u $n -- test -r $rk/id_ed25519 fails (control: it can read its own home $home)" cannot
# 6. no copy of the retired key stays under the new home
left=;if [ -n "$pub" ]&&[ -d "$home/.ssh" ];then for k in "$home"/.ssh/*;do [ -f "$k" ]||continue
  [ "$(head -n1 "$k"|cut -d' ' -f1,2)" = "$pub" ]||cmp -s "$k" "$rk/id_ed25519"&&left="$left $k";done;fi
t key-not-in-home "no file under $home/.ssh is the retired key${left:+ (found:$left)}" test -n "$pub" -a -z "$left"
# 7. the ring: OLD closed at T, NEW has no stale open line and (after its first start) one fresh one
ol=$(grep "^$OLD@agi " "$RING" 2>/dev/null)
oldok(){ [ -n "$ol" ]&&[ -z "$(echo "$ol"|grep -v 'valid-before=')" ]&&case $(echo "$ol"|tail -n1) in *valid-before=\"$T\"*)true;;*)false;; esac; }
t ring-old "every $OLD@agi line in $RING carries valid-before and the last is \"$T\"" oldok
op=$(grep "^$NEW@agi " "$RING" 2>/dev/null|grep -v 'valid-before='|sed 's/.*valid-after="\([0-9]*\)Z".*/\1/')
tn=${T%Z};stale=0;fresh=0;for a in $op;do if [ "$a" -lt "$tn" ];then stale=$((stale+1));else fresh=$((fresh+1));fi;done
nk=$(grep "^$NEW@agi " "$RING" 2>/dev/null|grep -v 'valid-before='|sed 's/^[^ ]* [^ ]* //'|cut -d' ' -f1,2|tail -n1)
if [ $stale -gt 0 ];then say FAIL ring-new "$NEW@agi has $stale open line(s) older than $T: an earlier holder's key still signs for the name"
elif [ $fresh -gt 1 ];then say FAIL ring-new "$NEW@agi has $fresh open lines from $T on (want 1)"
elif [ $fresh = 0 ];then if [ "$FIRST" = --first-start ];then say FAIL ring-new "$NEW@agi has no open line after the first start";else say wait ring-new "$NEW@agi has no line yet (agi-signers adds it at the first start; re-run with --first-start)";fi
elif [ -n "$pub" ]&&[ "$nk" = "$pub" ];then say FAIL ring-new "$NEW@agi signs with the retired key"
else say ok ring-new "$NEW@agi: no stale line, one open line from $T on, a key $OLD never held";fi
# 8. nothing in the host config still names the old user
miss=;for d in $SCAN;do [ -d "$d" ]||miss="$miss $d";done
hits=$({ grep -rlw "agi-$OLD" $SCAN;find $SCAN -name "agi-$OLD";find $SCAN -name "*@$OLD.*";} 2>/dev/null|sort -u|tr '\n' ' ')
t grep-old "agi-$OLD over $SCAN: hits '${hits% }' (want none)${miss:+, MISSING scan dir(s):$miss}" test -z "$miss" -a -z "$hits"
# 9. nothing of the old name runs (AFTER the pin bump: a projection in the window could have started agi-post@OLD on an empty home)
idle(){ case $($SYSTEMCTL is-active "$1" 2>/dev/null) in inactive|failed)return 0;;esac;return 1;}
for u in agi-post agi-boxwake;do t "old-${u#agi-}-inactive" "systemctl is-active $u@$OLD = '$($SYSTEMCTL is-active "$u@$OLD" 2>/dev/null)' (want inactive or failed)" idle "$u@$OLD";done
# 10. the new name's mail wake: nothing but `systemctl enable --now agi-carry@NEW.path` makes it (host-act-encryption-town.sh move NEW, after 4b)
carry(){ [ "$($SYSTEMCTL is-enabled "agi-carry@$NEW.path" 2>/dev/null)" = enabled ]&&[ "$($SYSTEMCTL is-active "agi-carry@$NEW.path" 2>/dev/null)" = active ]; }
t new-carry-path "systemctl is-enabled agi-carry@$NEW.path = '$($SYSTEMCTL is-enabled "agi-carry@$NEW.path" 2>/dev/null)', is-active '$($SYSTEMCTL is-active "agi-carry@$NEW.path" 2>/dev/null)' (want enabled, active)" carry
[ $f = 0 ]
