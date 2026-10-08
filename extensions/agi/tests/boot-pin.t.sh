#!/bin/sh
# boot-pin.t.sh: goal:g1.41 A1 (DG1 20:54Z; hypothesis:g141-a1-agi-boot-and-its-reprojection-read-only-a-root-pinned-sha): root's boot chain reads ONLY a 40-hex trunk sha pinned in /etc/agi/carry.env (AGI_TRUNK), never HEAD. engine-root.md only; engine.md is not touched.
# sh + git + jq on a SCRATCH repo, no systemd, no root, no /etc, no network, 0 USD. It runs the REAL pieces extracted with `sect` from the .geometry/engine*.md of ROOT: the agi-boot script and the agi-boot.service unit text (engine-root.md) and the agi-project block that agi-boot pipes in (engine.md), under the test_agi_boot.py fakes: setfacl / systemctl stubs that log, a git wrapper that logs every argv and execs the real git, AGI_RAM, AGI_BOOT_OUT, AGI_LOADAVG, AGI_PSI_IO, a scratch posts.md / config.json (the real engine*.md are copied in so the real agi-project block is there). ROOT=<repo> where the pieces are read (a mutant / the reference = another tree with the same .geometry layout). One ok/FAIL line per case; exit = FAIL count.
# Lanes: a1 the pin is good and HEAD is HOSTILE (a commit adding a boot row `evil` and a decoy engine-root.md): the projected units, the starts and the baked agi-project.service are BYTE-IDENTICAL to a boot before HEAD moved (agi-project.path is excluded on purpose: with a sha it degenerates to logs/, DG1 measured), no agi-post@evil, 0 HEAD in the baked ExecStart, the pinned sha baked in · a2 (x7) the pin unset / short (7) / 41 chars / uppercase hex / non-hex / empty / a trailing newline: the boot fails BEFORE any git read, any setfacl, any start (a git wrapper logs 0 argv, 0 setfacl, 0 start); set-but-malformed = rc 1 exactly, unset / empty = rc != 0 (`${AGI_TRUNK:?}` is rc 2 in dash) · a3 the unit text: EnvironmentFile=/etc/agi/carry.env present once, HEAD in no ExecStart line · a4 the ExecStart line, extracted and run under sh with AGI_TRUNK set in a repo whose HEAD carries a DECOY engine-root.md (its agi-boot touches a marker): the marker is NOT touched and the pinned boot ran (2 starts) · a5 control: the pinned boot with HEAD == the pin starts exactly the boot rows in order.
# Honest limits: this is the script and the unit TEXT, not systemd: whether the unit really loads /etc/agi/carry.env is read off its EnvironmentFile line, never run; systemd's own $VAR substitution in ExecStart is not modelled (the line is run under sh, where $AGI_TRUNK expands from the environment, as test_agi_boot.py runs it). The pin VALUE in /etc/agi/carry.env is host-held and never touched. The a2 cases stop at the gate by construction: a gate placed AFTER the first git read / setfacl is caught by the logs, a gate that accepts a bad value by the rc.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST AGI_RAM AGI_BOOT_OUT
sect agi-boot >$T/agiboot.sh;sect agi-boot.service >$T/unit.txt
[ -s $T/agiboot.sh ]&&[ -s $T/unit.txt ]||{ echo "FAIL extract: agi-boot $(wc -c <$T/agiboot.sh) unit $(wc -c <$T/unit.txt)";exit 99;}
mkdir -p $T/fk $T/hm
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig
printf '#!/bin/sh\necho "setfacl $*">>%s/log\n' $T >$T/fk/setfacl
printf '#!/bin/sh\necho "systemctl $*">>%s/log\n[ "$1" = start ]&&echo "b $2">>%s/log\nexit 0\n' $T $T >$T/fk/systemctl
printf '#!/bin/sh\necho "git $*">>%s/gitlog\nexec /usr/bin/git "$@"\n' $T >$T/fk/git
chmod +x $T/fk/*
echo "0.50 0.5 0.5 1/1 1" >$T/la;printf 'some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/io
row(){ printf '  - {"name": "%s", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' $1;}
# the scratch repo: commit GOOD (the real engine*.md, boot rows a b), then branch evil = HOSTILE (an extra boot row `evil` and a DECOY engine-root.md whose agi-boot touches a marker)
rm -rf $T/r;mkdir -p $T/r/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine*.md $T/r/.agi/nodes/.geometry/
{ printf -- '---\nposts:\n';row a;row b;} >$T/r/.agi/nodes/.geometry/posts.md
jq '.values.local_maxxing.agi_boot={"poll_s":0.1,"wait_max_s":1,"space_s":0.2}' $R0/.agi/config.json >$T/r/.agi/config.json
export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
$G init -q $T/r;$G -C $T/r add -A;$G -C $T/r commit -qm good;GOOD=$($G -C $T/r rev-parse HEAD)
$G -C $T/r checkout -q -b evil;row evil >>$T/r/.agi/nodes/.geometry/posts.md
printf '### agi-boot (1 B)\n~~~sh\n#!/bin/sh\ntouch %s/marker\n~~~\n' $T >$T/r/.agi/nodes/.geometry/engine-root.md
$G -C $T/r add -A;$G -C $T/r commit -qm hostile;EVIL=$($G -C $T/r rev-parse HEAD);$G -C $T/r checkout -q -B main $GOOD
# boot OUT [VAR=val ...]: the real agi-boot under the fakes; the extra args are env assignments (the pin). rc in $brc, output in $T/boot.out
boot(){ o=$1;shift;rm -rf $T/out.$o $T/ram;: >$T/log;: >$T/gitlog;(cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out.$o AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io "$@" sh -s <$T/agiboot.sh >$T/boot.out 2>&1);brc=$?;}
starts(){ grep '^b ' $T/log|tr '\n' ' ';}
# a5 control + the BEFORE snapshot: HEAD == the pin
boot m AGI_TRUNK=$GOOD;a0rc=$brc;a0s=$(starts);rm -rf $T/snap.a0;cp -a $T/out.m $T/snap.a0   # the SAME out dir name both times: the baked units embed their own output path
P=agi-post@
ok "a5-pinned-boot-with-head-at-the-pin-starts-the-boot-rows (control) the pinned boot, HEAD == the pin: rc $a0rc (want 0), starts '$a0s' (want exactly the boot rows a b in order), the units are projected ($(ls $T/snap.a0|tr '\n' ' '))" '[ $a0rc = 0 ]&&[ "$a0s" = "b ${P}a b ${P}b " ]&&[ -e $T/snap.a0/agi-project.service ]'
# a1: HEAD moves to the hostile commit, the pin stays: nothing changes
$G -C $T/r checkout -q -B main $EVIL
boot m AGI_TRUNK=$GOOD;a1rc=$brc;a1s=$(starts);rm -f $T/marker;rm -rf $T/snap.a1;cp -a $T/out.m $T/snap.a1
d=$(diff -r -x agi-project.path $T/snap.a0 $T/snap.a1 2>&1|wc -l|tr -d ' ');sv=$T/snap.a1/agi-project.service
ev=$(find $T/snap.a1 -name '*evil*'|wc -l|tr -d ' ');hx=$(grep '^ExecStart=' $sv 2>/dev/null|grep -c HEAD);gs=$(grep -c $GOOD $sv 2>/dev/null)
ok "a1-hostile-head-changes-nothing the pin is good and HEAD is the hostile commit (an extra boot row evil, a decoy engine-root.md): rc $a1rc (want 0), starts '$a1s' (want the same a b), the projected units differ from the pre-move boot by $d diff line(s) (want 0, agi-project.path excluded), $ev evil file(s) (want 0), the baked agi-project.service ExecStart holds HEAD $hx time(s) (want 0) and the pinned sha $gs time(s) (want >= 1)" '[ $a1rc = 0 ]&&[ "$a1s" = "$a0s" ]&&[ "$d" = 0 ]&&[ "$ev" = 0 ]&&[ "$hx" = 0 ]&&[ "$gs" -ge 1 ]'
# a2: a bad pin fails before ANY work
nl=$(printf '\n.');nl=${nl%.}
chk(){ nm=$1;shift;boot c$nm "$@";gl=$(wc -l <$T/gitlog|tr -d ' ');sf=$(grep -c '^setfacl' $T/log);st=$(grep -c '^b ' $T/log);od=$(ls $T/out.c$nm 2>/dev/null|wc -l|tr -d ' ')
 case $nm in unset|empty)want="!= 0";okrc='[ $brc != 0 ]';;*)want="= 1";okrc='[ $brc = 1 ]';;esac
 ok "a2-pin-$nm-fails-before-any-work the pin $nm: rc $brc (want $want), $gl git argv logged (want 0), $sf setfacl (want 0), $st start (want 0), $od unit file(s) written (want 0)" "$okrc&&[ \$gl = 0 ]&&[ \$sf = 0 ]&&[ \$st = 0 ]&&[ \$od = 0 ]";}
chk unset
chk empty AGI_TRUNK=
chk short7 AGI_TRUNK=$(printf %s $GOOD|cut -c1-7)
chk len41 AGI_TRUNK=${GOOD}0
chk upper AGI_TRUNK=$(printf %s $GOOD|tr a-f A-F)
chk nonhex AGI_TRUNK=$(printf %s $GOOD|sed 's/^./g/')
chk newline "AGI_TRUNK=$GOOD$nl"
chk headword AGI_TRUNK=HEAD
# a3: the unit text
ec=$(grep -c '^EnvironmentFile=/etc/agi/carry.env$' $T/unit.txt);xh=$(grep '^ExecStart=' $T/unit.txt|grep -c HEAD);xs=$(grep -c '^ExecStart=' $T/unit.txt)
ok "a3-unit-loads-the-carry-env-and-never-names-head agi-boot.service carries EnvironmentFile=/etc/agi/carry.env ($ec, want 1) and HEAD appears in $xh of its $xs ExecStart line(s) (want 0 of 1)" '[ "$ec" = 1 ]&&[ "$xh" = 0 ]&&[ "$xs" = 1 ]'
# a4: the ExecStart line run under sh, HEAD = the hostile commit with the decoy
cmd=$(grep '^ExecStart=' $T/unit.txt|sed 's/^ExecStart=//');rm -rf $T/out.x $T/ram;: >$T/log;rm -f $T/marker
(cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out.x AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io AGI_TRUNK=$GOOD sh -c "$cmd" >$T/x.out 2>&1);xrc=$?;xs2=$(starts)
ok "a4-execstart-reads-the-pinned-blob-not-head the ExecStart line extracted and run under sh with AGI_TRUNK=<good> while HEAD carries a decoy engine-root.md: the decoy marker is $([ -e $T/marker ]&&echo TOUCHED||echo untouched) (want untouched), rc $xrc (want 0), the pinned boot ran: starts '$xs2' (want a b)" '[ ! -e $T/marker ]&&[ $xrc = 0 ]&&[ "$xs2" = "b ${P}a b ${P}b " ]'
echo "boot-pin: $f FAIL"
exit $f
