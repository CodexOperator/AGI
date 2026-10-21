#!/bin/sh
# host-act-encryption-town.sh: the per-post `move` of the box host act (owner 2026-10-08 21:2xZ: every post moves TONIGHT; E's internal drive, NO RAM disk). Its `act` (STEP 0 before-state + rollback, the pieces, units, ACLs) moved to `agi.sh host` (goal:g7.16.1.11.44.8 S2a, council 09:20Z 10-16): here it is ONE line that execs it. `move` stays until S3.
#   PIN=<40-hex commit of AGI_REPO> sh host-act-encryption-town.sh act          = exec sh ../bin/agi.sh host (step 0, then the act; root, on E; ROOT=<scratch> rehearses)
#   PIN=<40-hex> sh host-act-encryption-town.sh move POST                       per post, after its row has box encryption-town AT PIN
# Cells (env) for move: PIN (required) · AGI_REPO (default /data/work/agi) · AGI_BOX (default encryption-town) · ROOT=<scratch dir> (every path prefixed, no systemctl / root check). The act's cells (E_MEM_*, SKIP_PREREQ, PRIME_USER, carry_fetch) are agi.sh's.
R=${ROOT:-};M=${AGI_REPO:-/data/work/agi};PIN=${PIN:-};BOX=${AGI_BOX:-encryption-town};mode=${1:-act}
die(){ echo "host-act: $*">&2;exit 1;}
case $PIN in ""|*[!0-9a-f]*)die "PIN must be a 40-hex commit sha";esac;[ ${#PIN} = 40 ]||die "PIN must be a 40-hex commit sha"
export GIT_NO_REPLACE_OBJECTS=1 GIT_NO_LAZY_FETCH=1;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
G(){ git -c safe.directory=$R$M -C $R$M "$@";}
G cat-file -e $PIN^{commit} 2>/dev/null||die "$PIN is not a commit of $R$M"
[ -n "$R" ]||[ "$(id -u)" = 0 ]||die "run as root (sudo), or set ROOT= for a rehearsal"
case $mode in
act)exec sh "$(dirname "$0")/../bin/agi.sh" host;;
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
