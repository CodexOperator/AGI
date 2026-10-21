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
# inactive or failed, an empty answer or activating is a FAIL) · projected (council 17:58Z 10-21: agi-project.path was NEVER active on this box, so a carry.env write projects nothing;
# the projection is EXPLICIT, `systemctl start agi-project.service` right after 4b's `agi.sh host`: its last start (ExecMainStartTimestamp, whole seconds) is >= the mtime of
# carry.env and its Result is success; never started, started before the write, a failed run or an unreadable stamp is a FAIL) · refs-left (council 18:13Z R7: nothing left at refs/heads/posts/OLD,
# refs/box/OLD/*, refs/box/*/OLD, refs/held/OLD/*, refs/held/*/OLD; refs/retired and refs/remotes are outside the scan; a repo git cannot read is a FAIL) · outbox-signer (every tip under
# refs/box/NEW/* verifies `for NEW@agi` against the ring: `box send` refuses to append to a tip not signed for its sender, so an outbox MOVED from OLD is FAIL; none yet = ok) · flags (R10, belam
# measured: ~/.claude.json of NEW has projects["/data/work/agi"].hasTrustDialogAccepted true, else the first start stops at the trust dialog) · sweep (R11: every file under NEW's home that
# still names the OLD home path is NAMED; a hit in a file the post EXECUTES, ~/.gitconfig ~/.config/git ~/bin ~/.claude/settings*.json or any hooks/ file, is a FAIL; ~/.claude/projects and the
# dead project keys of .claude.json are not hits) · new-boxwake (R12: agi-boxwake@NEW is the live wake, started WITH agi-post@NEW by its Wants=; `wait` before the start, FAIL after it unless
# active; agi-carry@.path watches a g.git no post has, so new-carry-path does NOT prove the wake) · stays-up (council 20:00Z, G3's red: run 2 printed 18 ok over a post that exited ~3 s after each start and
# restarted every 30 s; ONLY with --first-start, so run 1 keeps its 18 rows: two `systemctl show` reads of agi-post@NEW >= STAYS_S (default 60) seconds apart, ActiveState active and SubState running at both, NRestarts
# present and equal; a post that exits (NRestarts moves, or auto-restart/activating), an unreadable answer or no answer is a FAIL). Run it right after the move, before the name OLD is reused by a later move: old-name-free reads
# "empty" as the proof that no projection between the usermod and the bump minted a fresh agi-OLD.
# Env (defaults are the box's; a test sets them to stubs): ROOT (prefix of every default path) ID GETENT RUNUSER SYSTEMCTL ROOTUSER RET RING SCAN CARRY MAINKEY MAIN STAYS_S.
ROOT=${ROOT-};ID=${ID:-id};GETENT=${GETENT:-getent};RUNUSER=${RUNUSER:-runuser};SYSTEMCTL=${SYSTEMCTL:-systemctl};ROOTUSER=${ROOTUSER:-root}
RET=${RET:-$ROOT/var/lib/agi/retired/keys};RING=${RING:-$ROOT/var/lib/agi/allowed_signers};CARRY=${CARRY:-$ROOT/etc/agi/carry.env};MAINKEY=${AGI_REPO:-/data/work/agi};MAIN=${MAIN:-$ROOT$MAINKEY}
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
# 11. the pin was PROJECTED: agi-project.path never runs here, so 4b's carry.env write alone changes nothing in /run; the start of agi-project.service after it does
proj(){ ps=$($SYSTEMCTL show --timestamp=utc -p ExecMainStartTimestamp --value agi-project.service 2>/dev/null);[ -n "$ps" ]||return 1;ps=$(date -u -d "$ps" +%s 2>/dev/null)||return 1
 pc=$(stat -c %Y "$CARRY" 2>/dev/null)||return 1;[ "$ps" -ge "$pc" ]&&[ "$($SYSTEMCTL show -p Result --value agi-project.service 2>/dev/null)" = success ]; }
t projected "agi-project.service last start '$($SYSTEMCTL show --timestamp=utc -p ExecMainStartTimestamp --value agi-project.service 2>/dev/null)', Result '$($SYSTEMCTL show -p Result --value agi-project.service 2>/dev/null)'; $CARRY written $(stat -c %y "$CARRY" 2>/dev/null|cut -c1-19) (want a start at or after the write, success: run \`systemctl start agi-project.service\` after \`agi.sh host\`)" proj
# 12. refs (R7): the INBOX moved with the agent (refs/box/*/OLD -> NEW, refs/held/OLD/* -> NEW, posts/OLD -> posts/NEW); the OUTBOX refs/box/OLD/* and the peers' marks refs/held/*/OLD were RETIRED to
# refs/retired/OLD-T/. `box send` appends only onto a tip signed `for <sender>@agi` and `box read` checks each commit against its sender, so a moved outbox is dead mail under the new name
GIT(){ git -c safe.directory="$MAIN" -c gpg.format=ssh -c gpg.ssh.allowedSignersFile="$RING" -C "$MAIN" "$@"; }
refs=$(GIT for-each-ref --format='%(refname)' refs/heads/posts refs/box refs/held 2>/dev/null)||refs=UNREADABLE
left=$(printf '%s\n' "$refs"|grep -E "^refs/heads/posts/$OLD(/|\$)|^refs/box/$OLD/|^refs/box/[^/]+/$OLD\$|^refs/held/$OLD/|^refs/held/[^/]+/$OLD\$"|tr '\n' ' ')
t refs-left "refs of $OLD left outside refs/retired + refs/remotes in $MAIN: '${left% }' (want none)$([ "$refs" != UNREADABLE ]||echo '; the repo is UNREADABLE as this user: root needs safe.directory')" test "$refs" != UNREADABLE -a -z "$left"
bad=;nb=0;for r in $(printf '%s\n' "$refs"|grep "^refs/box/$NEW/");do nb=$((nb+1));GIT verify-commit --raw "$r" 2>&1|grep -q "for $NEW@agi with"||bad="$bad ${r#refs/box/}";done
t outbox-signer "$nb tip(s) under refs/box/$NEW/*, each must verify 'for $NEW@agi'${bad:+ (NOT:$bad)}" test "$refs" != UNREADABLE -a -z "$bad"
# 13. the trust dialog (R10): claude keys trust by the project path the post runs in, MAIN's root; a fresh home has no entry
flags(){ [ -f "$home/.claude.json" ]&&jq -e --arg p "$MAINKEY" '.projects[$p].hasTrustDialogAccepted==true' "$home/.claude.json" >/dev/null 2>&1; }
t flags "$home/.claude.json projects[\"$MAINKEY\"].hasTrustDialogAccepted == true (else the first start sticks at the trust dialog)" flags
# 14. the sweep (R11): the old HOME path inside the new home. Named, never skipped; fatal only where the post EXECUTES it
oh=$(dirname "$home")/$OLD;pat="$(printf %s "$oh"|sed 's/[][\\.*^$\/]/\\&/g')([^a-z0-9-]|\$)"
hits=;for h in $(grep -rIlE -e "$pat" "$home" 2>/dev/null|sort);do case $h in "$home"/.claude/projects/*)continue;; "$home"/.claude.json)jq -e --arg p "$pat" '[del(.projects)|..|strings|select(test($p))]|length>0' "$h" >/dev/null 2>&1||continue;; esac;hits="$hits ${h#$home/}";done
run=;for h in $hits;do case $h in .gitconfig|.config/git/*|bin/*|.claude/settings.json|.claude/settings.local.json|*/hooks/*|hooks/*)run="$run $h";; esac;done
t sweep "$(echo $hits|wc -w) file(s) under $home name $oh:${hits:- none}${run:+; EXECUTED:$run}" test -z "$run"
# 15. the wake (R12): agi-boxwake@NEW starts and stops WITH agi-post@NEW (Wants= / PartOf=): `move NEW` or agi-boot starts it, no line of the sitting does
bw=$($SYSTEMCTL is-active "agi-boxwake@$NEW" 2>/dev/null)
if [ "$bw" = active ];then say ok new-boxwake "agi-boxwake@$NEW is active (the live wake)"
elif [ "$FIRST" = --first-start ];then say FAIL new-boxwake "systemctl is-active agi-boxwake@$NEW = '${bw:--}' after the first start (want active: no wake, no mail read)"
else say wait new-boxwake "agi-boxwake@$NEW = '${bw:--}': it starts with agi-post@$NEW at the start (re-run with --first-start); agi-carry@$NEW.path is NOT the wake";fi
# 16. the post STAYS up (council 20:00Z): the first start can be "active" for the 3 s before a crash, so look twice, a restart interval apart (RestartUSec is 30 s)
if [ "$FIRST" = --first-start ];then
 pst(){ $SYSTEMCTL show -p ActiveState -p SubState -p NRestarts "agi-post@$NEW" 2>/dev/null; }
 s1=$(pst);sleep "${STAYS_S:-60}";s2=$(pst)
 up(){ for r in "$s1" "$s2";do printf '%s\n' "$r"|grep -qx 'ActiveState=active'&&printf '%s\n' "$r"|grep -qx 'SubState=running'||return 1;done
  n1=$(printf '%s\n' "$s1"|sed -n 's/^NRestarts=//p');n2=$(printf '%s\n' "$s2"|sed -n 's/^NRestarts=//p');[ -n "$n1" ]&&[ "$n1" = "$n2" ]; }
 t stays-up "agi-post@$NEW read twice ${STAYS_S:-60} s apart: ActiveState/SubState '$(printf '%s' "$s1"|tr '\n' ' ')' then '$(printf '%s' "$s2"|tr '\n' ' ')' (want active, running and the same NRestarts both times)" up
fi
[ $f = 0 ]
