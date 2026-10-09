#!/bin/sh
# host-act-encryption-town.sh: the ONE root act that stands the agi root side up on encryption-town (E), and the per-post start (owner 2026-10-08 21:2xZ: every post moves TONIGHT; E's internal drive, NO RAM disk), in the shape of experiment:g141-a1b-host-act-before-state-and-rollback: STEP 0 copies the before-state aside and writes ONE rollback command, then the act.
#   PIN=<40-hex commit of AGI_REPO> sh host-act-encryption-town.sh act          step 0, then the act (root, on E)
#   PIN=<40-hex> sh host-act-encryption-town.sh move POST                       per post, after its row has box encryption-town AT PIN
#   ROOT=<scratch dir> ...                                                      rehearsal: every path is prefixed, no systemctl / ACL / chown / root check
# Cells (env): PIN (required) · AGI_REPO (default /data/work/agi) · AGI_BOX (default encryption-town) · E_MEM_HIGH / E_MEM_MAX / E_OOM_LIMIT (the E agi.slice; typed here because config:guard has no E line: belam's to confirm) · SKIP_PREREQ=1 (a rehearsal without pi / claude) · PRIME_USER (default belam: the user the comms ACL also names; a rehearsal defaults to the invoking user).
# What it installs, ALL from the pinned commit's bytes (`sect` over the geometry at PIN, never the moving checkout): agi-vstore, sect, box, box-carry, agi-signers, the carry units, agi-boot.service, the polkit rule; it writes /etc/agi/carry.env and, for E ONLY, a NO-OP agi-ram-main.service (Type=oneshot, ExecStart=/bin/true: E has no RAM disk, MAIN is a plain directory; a drop-in cannot reset a dependency list, so agi-boot.service keeps its pinned Requires / After text) plus a plain /mnt/agi-ram, and the MAIN ACL the posts need (g:agi:rwX + a default ACL, recursive, on .git/{objects,refs,logs,worktrees}, and on .agi/sessions/inbox g:agi:rwx + default g:agi:rw-, and on .agi/comms (recursive) g:agi:rwX + u:$PRIME_USER:rwX + a default ACL on every directory: L carries them, no code made them before). NO engine byte changes; local-town is untouched.
# PREREQUISITES it checks and does NOT install: pi at /opt/agi/bin/pi (or any PATH dir of the post unit) and claude for the claude rows, readable by the agi-* users; group agi and the agi-<post> users; setfacl; the clone at AGI_REPO holding PIN.
R=${ROOT:-};M=${AGI_REPO:-/data/work/agi};PIN=${PIN:-};BOX=${AGI_BOX:-encryption-town};mode=${1:-act}
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
case $mode in
act)
# ---- preflight (nothing written yet) ----
for c in git jq setfacl sed;do command -v $c>/dev/null||die "missing tool: $c";done
[ -n "$R" ]||{ command -v systemctl>/dev/null||die "missing tool: systemctl";getent group agi>/dev/null||die "group agi is absent (the agi-* users are the owner's act)";}
G show $PIN:.agi/nodes/.geometry/posts.md>/dev/null||die "no posts.md at $PIN"
id $PU>/dev/null 2>&1||die "PREREQ: user $PU (the comms ACL's second entry) is absent: PRIME_USER=<user> to name another"
[ -n "$SKIP_PREREQ" ]||{ [ -x $R/opt/agi/bin/pi ]||[ -x $R/usr/local/bin/pi ]||die "PREREQ: no pi at /opt/agi/bin/pi (agi-project exits 3 without it while a pi row has box $BOX): install it first, SKIP_PREREQ=1 to override";}
# ---- STEP 0 (root, BEFORE anything else): back the before-state up and write ONE rollback command ----
B=$R/var/backups/agi-act-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p $R/var/backups&&mkdir $B||die "$B exists or cannot be made: refusing to overwrite a before-state";mkdir $B/files
L="/etc/agi/carry.env /etc/systemd/system/agi-boot.service /etc/systemd/system/agi-ram-main.service /etc/systemd/system/agi-carry@.service /etc/systemd/system/agi-carry@.path /etc/systemd/system/agi-carry-fetch.service /etc/systemd/system/agi-carry-fetch.timer /etc/systemd/system/agi.slice /etc/polkit-1/rules.d/50-agi.rules /opt/agi/bin/agi-signers /opt/agi/bin/box /opt/agi/bin/box-carry /opt/agi/bin/sect /usr/local/libexec/agi-vstore"
for f in $L;do if [ -e $R$f ];then (cd $R/&&cp -a --parents ${f#/} $B/files/)||exit 1;else echo $f>>$B/absent;fi;done
for d in $M/.git/worktrees $M/.agi/comms $M/.agi/sessions/inbox $M/.agi/sessions /mnt/agi-ram/state /mnt/agi-ram /opt/agi/bin /opt/agi /usr/local/libexec /etc/agi /var/lib/agi;do [ -d $R$d ]||echo $d>>$B/absentdirs;done
for f in $L;do [ -e $R$f ]&&stat -c '%a %U:%G %n' $R$f;done>$B/before.stat
AD=;for d in objects refs logs worktrees;do [ -d $R$M/.git/$d ]&&AD="$AD $R$M/.git/$d";done
[ -z "$AD" ]||getfacl -R -p $AD>$B/acl.before 2>/dev/null||exit 1
[ ! -d $R$M/.agi/sessions/inbox ]||getfacl -p $R$M/.agi/sessions/inbox>>$B/acl.before 2>/dev/null||exit 1
[ ! -d $R$M/.agi/comms ]||getfacl -R -p $R$M/.agi/comms>>$B/acl.before 2>/dev/null||exit 1
U=$R/run/systemd/system;( cd $U 2>/dev/null&&ls -d agi-* agi.slice multi-user.target.wants/agi-* 2>/dev/null )>$B/run.list
if [ -s $B/run.list ];then tar -C $U -cpf $B/run.tar -T $B/run.list||exit 1;(cd $U&&find $(cat $B/run.list) |sort)>$B/run.before;else : >$B/run.before;fi
(cd $B/files&&find . -type f|sort|xargs -r sha256sum)>$B/before.sha256
printf '%s\n' '#!/bin/sh' "B=$B;R=$R" 'U=$R/run/systemd/system' '[ -n "$R" ]||systemctl disable --now agi-carry-fetch.timer 2>/dev/null' '[ -n "$R" ]||systemctl disable agi-boot.service 2>/dev/null' '[ ! -d $B/files ]||cp -a $B/files/. ${R:-/}||exit 1' '[ ! -s $B/acl.before ]||setfacl --restore=$B/acl.before||exit 1' 'if [ -d $U ];then ( cd $U;find agi-* agi.slice multi-user.target.wants/agi-* 2>/dev/null|while read p;do grep -qxF "$p" $B/run.before||rm -rf "$p";done );fi' '[ ! -s $B/run.tar ]||tar -C $U -xpf $B/run.tar' '[ ! -s $B/absent ]||while read f;do rm -f $R$f;done<$B/absent' '[ ! -s $B/absentdirs ]||while read d;do rmdir $R$d 2>/dev/null;done<$B/absentdirs' '[ -n "$R" ]||systemctl daemon-reload' 'echo rolled back from $B'>$B/rollback.sh
echo "backup $B: $(wc -l <$B/before.sha256) files, $(wc -l <$B/run.before) /run paths, $(wc -l <$B/absent 2>/dev/null||echo 0) absent files; rollback: sh $B/rollback.sh"
# ---- the act: vstore first, then carry.env, the pieces, the units, the E no-op ram unit, polkit, the slice, reload, enable ----
echo "installing from $PIN:"
put agi-vstore /usr/local/libexec/agi-vstore 755 sh
install -d -m 755 $OWN $R/etc/agi||exit 1
printf 'AGI_BOX=%s\nAGI_HUB=\nAGI_REPO=%s\nAGI_TRUNK=%s\nGIT_CONFIG_VALUE_0=%s\n' $BOX $M $PIN $M>$R/etc/agi/carry.env||exit 1;chmod 644 $R/etc/agi/carry.env
for p in sect box box-carry agi-signers;do put $p /opt/agi/bin/$p 755 sh;done
for u in agi-carry@.service agi-carry@.path agi-carry-fetch.service agi-carry-fetch.timer agi-boot.service;do put $u /etc/systemd/system/$u 644 unit;done
install -d -m 755 $OWN $R/mnt/agi-ram $R/mnt/agi-ram/state||exit 1
printf '%s\n' '# encryption-town ONLY: MAIN is a plain directory on the internal drive; this satisfies the pinned agi-boot.service Requires/After' '[Unit]' 'Description=encryption-town: no RAM disk, MAIN on the internal drive' '[Service]' 'Type=oneshot' 'RemainAfterExit=yes' 'ExecStart=/bin/true' >$R/etc/systemd/system/agi-ram-main.service||exit 1;chmod 644 $R/etc/systemd/system/agi-ram-main.service
put agi.rules /etc/polkit-1/rules.d/50-agi.rules 644 unit
printf '%s\n' '# encryption-town: typed here (config:guard has no E line); 7.8 GB box' '[Slice]' "MemoryHigh=${E_MEM_HIGH:-5G}" "MemoryMax=${E_MEM_MAX:-6G}" 'ManagedOOMMemoryPressure=kill' "ManagedOOMMemoryPressureLimit=${E_OOM_LIMIT:-40%}" >$R/etc/systemd/system/agi.slice||exit 1;chmod 644 $R/etc/systemd/system/agi.slice
install -d -m 755 $OWN $R/var/lib/agi||exit 1
# MAIN ACL: the post users (group agi) create refs, objects, logs and worktrees in MAIN's .git; L carries this, nothing in the repo made it
AG=agi;[ -z "$R" ]||AG=$(id -gn)
install -d $R$M/.git/worktrees||exit 1
for d in objects refs logs worktrees;do setfacl -R -m g:$AG:rwX $R$M/.git/$d&&find $R$M/.git/$d -type d -exec setfacl -d -m g:$AG:rwX {} +||die "cannot set the MAIN ACL on .git/$d: sh $B/rollback.sh";done
echo "  MAIN ACL g:$AG:rwX (+default) on .git/{objects,refs,logs,worktrees}"
IB=$R$M/.agi/sessions/inbox;NS=;[ -d $R$M/.agi/sessions ]||NS=$R$M/.agi/sessions
mkdir -p $IB||exit 1;[ -n "$R" ]||chown --reference=$R$M/.agi $NS $IB||exit 1
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
  for d in $M/.agi/comms $(find $M/.agi/comms -mindepth 1 -type d|head -1);do t=$(setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups mktemp $d/.act-probe.XXXXXX)&&setpriv --reuid=$(id -u agi-$U) --regid=$(id -g agi-$U) --init-groups rm $t||die "agi-$U cannot create a file in $d (the comms ACL): sh $B/rollback.sh";done
  echo "  probe: agi-$U creates and removes a dir in .git/{objects,refs,logs,worktrees} and a file in .agi/sessions/inbox and .agi/comms"
 else echo "  probe SKIPPED: no agi-<post> user for a box $BOX row yet">&2;fi
fi
if [ -z "$R" ];then
 systemd-analyze verify /etc/systemd/system/agi-ram-main.service /etc/systemd/system/agi-boot.service /etc/systemd/system/agi-carry@.service /etc/systemd/system/agi-carry-fetch.service /etc/systemd/system/agi.slice||die "systemd-analyze verify refused a unit: sh $B/rollback.sh"
 systemctl daemon-reload&&systemctl enable --now agi-carry-fetch.timer&&systemctl enable agi-boot.service&&systemctl start agi-boot.service||die "enable / start failed: sh $B/rollback.sh"
 echo "slice:";systemctl show agi.slice -p MemoryHigh -p MemoryMax -p ManagedOOMMemoryPressure
fi
echo "act done; next: per post, PIN=$PIN sh $0 move <post> (after its row has box $BOX at that pin)";;
move)
P=$2;case $P in ""|*[!a-z0-9-]*)die "usage: move POST";esac
G show $PIN:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -e --arg p $P --arg b $BOX 'select(.name==$p and .box==$b and .engine.v==4)'>/dev/null||die "row $P is not box $BOX with engine.v 4 at $PIN"
[ -f $R/etc/agi/carry.env ]||die "no /etc/agi/carry.env: run act first"
if ! grep -qx "AGI_TRUNK=$PIN" $R/etc/agi/carry.env;then cp -a $R/etc/agi/carry.env $R/etc/agi/carry.env.before-$P||exit 1;sed "s/^AGI_TRUNK=.*/AGI_TRUNK=$PIN/" $R/etc/agi/carry.env.before-$P>$R/etc/agi/carry.env.new&&cat $R/etc/agi/carry.env.new>$R/etc/agi/carry.env;rm -f $R/etc/agi/carry.env.new;echo "pin -> $PIN (the old carry.env is carry.env.before-$P)";fi
if [ -z "$R" ];then
 systemctl start agi-project.service||die "projection failed (agi-project.service)"
fi
[ -f $R/run/systemd/system/agi-post@$P.service.d/h.conf ]||die "agi-post@$P is not projected (no h.conf drop-in): the row's engine.v / box at $PIN"
if [ -z "$R" ];then
 id agi-$P>/dev/null||die "user agi-$P is absent"
 systemctl enable --now agi-carry@$P.path&&systemctl start agi-post@$P||die "start failed for agi-post@$P"
 systemctl is-active agi-post@$P;systemctl show agi-post@$P -p ControlGroup
fi
echo "moved: $P started on $BOX (a shell on E needs AGI_BOX=$BOX, or send.py refuses the E rows as FOREIGN); next: the owner logs it in (/login relay), it resumes from its card";;
*)die "usage: act | move POST";;
esac
