#!/bin/sh
# boot-cells.t.sh: goal:g1.41 A2 (DG1 21:49Z; hypothesis:g141-a2-a4-root-pieces-fail-closed-on-a-bad-cell-...): agi-boot reads its five cells (loadavg1_lt, io_psi_some_avg60_lt, poll_s, wait_max_s, space_s) and exits 1 NAMING THE CELL before any setfacl, unit write or start unless each is a plain non-negative number: a missing cell (jq prints null) or a typo no longer opens the load gate by awk STRING comparison.
# sh + git + jq on a SCRATCH repo, no systemd, no root, no /etc, no network, 0 USD. The REAL piece (`sect agi-boot` from the .geometry/engine*.md of ROOT, default the working tree) runs under fakes (setfacl, systemctl, sleep, git is real). The pin is passed as AGI_TRUNK=<good sha>, so the lane holds on the trunk, on trunk + A1 (the pin) and on the A2 reference.
# Lanes: c-<cell>-<variant> each of the five cells absent / "abc" / -1 / "" / "1 2" / "5s": rc 1, the cell named, 0 setfacl, 0 start, 0 unit files written. k-* controls: the LIVE values (16 / 50 / 20 / 600 / 120) boot both posts and sleep the space cell; a numeric CLOSED gate (load above the line) still starts nothing. The load / io fakes sit on the side that makes a NULL cell visible (load 9.5 for the load cell, io 99 for the io cell): on the trunk the gate opens and the posts START.
# A2b rows (u-*): the unit's ExecStart line with a pin that is 40 zeros / a tree sha / an absent sha.
# Honest limits: the lane reads the piece, not systemd; "plain non-negative number" is read as digits with at most one dot (the cells are 16 / 50 / 20 / 600 / 120 and the fixture 0.1 / 1 / 0.2); an exponent form is not asserted either way.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST AGI_RAM AGI_BOOT_OUT
sect agi-boot >$T/agiboot.sh;[ -s $T/agiboot.sh ]&&[ -s $R0/.agi/config.json ]||{ echo "FAIL extract: agi-boot $(wc -c <$T/agiboot.sh)";exit 99;}
# UE (DG1 04:15Z, belam 04:14Z: the lane runs the REAL ownership): the unit's own Environment= words are the ONLY thing that lets root read /data/work/agi (another uid owns it); the runs below use an empty git config + git's different-owner seam + UE, never a $T/gitconfig that grants safe.directory the unit does not
sect agi-boot.service|sed -n 's/^Environment=//p'|tr ' ' '\n' >$T/ue.txt;UE=$(cat $T/ue.txt)
# A1b (DG1 05:18Z, DG3's build 4915baf8e8): the boot unit carries ExecStartPre=/usr/local/libexec/agi-vstore and Environment=GIT_DIR=/run/agi-v.git, so root reads ONLY the verified store. The lane runs the chain the way the unit does: `pre WORDS && START`. pre = the REAL `### agi-vstore` piece builds a scratch store $T/vs from MAIN ($T/r) at the pin of THIS run (a pin the verifier refuses stops the chain: START is not reached, as systemd does); START = the run below, with the unit's Environment words and GIT_DIR rewritten to that store (UEG). Without the piece (a tree before A1b) every run below is a FAIL, not a skip.
sect agi-vstore >$T/vstore;GDW=$(printf '%s\n' "$UE"|grep -cx 'GIT_DIR=/run/agi-v.git');UEG=$({ printf '%s\n' "$UE"|sed "s#^GIT_DIR=/run/agi-v.git#GIT_DIR=$T/vs#"|grep -v '^GIT_CONFIG_VALUE_0=';echo "GIT_CONFIG_VALUE_0=${CV0:-$T/r}";})
# HOST MODEL (DG1 06:11Z): the unit's Environment= words, THEN /etc/agi/carry.env over them (systemd applies EnvironmentFile over Environment= for the same name): carry.env holds GIT_CONFIG_VALUE_0 = the PATH of AGI_REPO (measured 10-08: /data/work/agi), not the unit's inline `*`, so MAIN ($T/r here) is the ONE granted path. root owns its own stores on the host, so those are granted by the global file $T/own.cfg (the seam would make them foreign)
printf '[safe]\n\tdirectory=%s\n\tdirectory=%s\n\tdirectory=%s\n\tdirectory=%s\n' $T/vs $T/vs.n $T/vp $T/vp.n >$T/own.cfg
pre(){ rm -rf $T/vs $T/vs.n;[ -s $T/vstore ]||return 127;(set -f;cd $T/r&&env -i PATH=/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/own.cfg GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 $UEG AGI_VSTORE=$T/vs AGI_MAIN=$T/r "$@" timeout 60 sh $T/vstore >/dev/null 2>$T/pre.err);r=$?;cat $T/pre.err >$T/err;cat $T/pre.err >$T/boot.out;return $r;}
mkdir -p $T/fk $T/hm
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig
printf '#!/bin/sh\necho "setfacl $*">>%s/log\n' $T >$T/fk/setfacl
printf '#!/bin/sh\necho "systemctl $*">>%s/log\n[ "$1" = start ]&&echo "b $2">>%s/log\nexit 0\n' $T $T >$T/fk/systemctl
printf '#!/bin/sh\necho "sleep $*">>%s/log\nexec /bin/sleep 0.05\n' $T >$T/fk/sleep;chmod +x $T/fk/*
row(){ printf '  - {"name": "%s", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' $1;}
P=.values.local_maxxing;LP=$P.de_live_parents.ceiling_if.loadavg1_lt;IP=$P.de_live_parents.ceiling_if.io_psi_some_avg60_lt;NP=$P.agi_boot.poll_s;MP=$P.agi_boot.wait_max_s;SP=$P.agi_boot.space_s
# the base config: the live file with the five cells pinned to FAST plain numbers (load line 16, io line 50), committed with the real engine*.md and two boot rows
jq "($LP)=16|($IP)=50|($NP)=0.1|($MP)=1|($SP)=0.2" $R0/.agi/config.json >$T/base.json
rm -rf $T/r;mkdir -p $T/r/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine*.md $T/r/.agi/nodes/.geometry/
{ printf -- '---\nposts:\n';row a;row b;} >$T/r/.agi/nodes/.geometry/posts.md
export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
$G init -q $T/r;$G -C $T/r add -A
# cfg EXPR: the base config with EXPR applied, committed; CS = that commit
cfg(){ jq "$1" $T/base.json >$T/r/.agi/config.json;$G -C $T/r add -A;$G -C $T/r commit -qm "c" --allow-empty;CS=$($G -C $T/r rev-parse HEAD);}
# boot LOAD IO: the real agi-boot under the fakes, pinned to CS; rc in $brc, output in $T/boot.out
boot(){ rm -rf $T/out $T/ram;: >$T/log;echo "$1 0.5 0.5 1/1 1" >$T/la;printf 'some avg10=0.00 avg60=%s avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' $2 >$T/io
 pre AGI_TRUNK=$CS&&(set -f;cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/own.cfg GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 $UEG AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io AGI_TRUNK=$CS timeout 60 sh -s <$T/agiboot.sh >$T/boot.out 2>&1);brc=$?;sf=$(grep -c '^setfacl' $T/log);st=$(grep -c '^b ' $T/log);uf=$(ls $T/out 2>/dev/null|wc -l|tr -d ' ');}
# k: controls first, so a broken fixture shows before the lanes
cfg "($LP)=16|($IP)=50|($NP)=20|($MP)=600|($SP)=120";boot 0.50 1.00
ok "k-live-values-boot-both-posts the LIVE cells (16 / 50 / 20 / 600 / 120), gate open: rc $brc (want 0), $st start(s) (want 2), the space cell used: $(grep -c '^sleep 120$' $T/log) 'sleep 120' (want 1), $uf unit file(s) written (want > 0)" '[ $brc = 0 ]&&[ $st = 2 ]&&[ $(grep -c "^sleep 120$" $T/log) = 1 ]&&[ $uf -gt 0 ]'
cfg ".";boot 0.50 1.00
ok "k-fast-decimal-cells-boot-both-posts the fixture's cells (0.1 / 1 / 0.2: decimals) boot both posts: rc $brc (want 0), $st start(s) (want 2)" '[ $brc = 0 ]&&[ $st = 2 ]'
cfg "($LP)=4";boot 9.50 1.00
ok "k-a-numeric-closed-gate-still-closes load line 4, load 9.5: rc $brc (want != 0: the gate never opened), $st start(s) (want 0)" '[ $brc != 0 ]&&[ $st = 0 ]'
for cell in loadavg1_lt:$LP:9.50:1.00 io_psi_some_avg60_lt:$IP:0.50:99.00 poll_s:$NP:0.50:1.00 wait_max_s:$MP:0.50:1.00 space_s:$SP:0.50:1.00;do nm=${cell%%:*};r=${cell#*:};path=${r%%:*};r=${r#*:};ld=${r%%:*};io=${r#*:}
 for var in absent:"del($path)" abc:"($path)=\"abc\"" negative:"($path)=-1" empty:"($path)=\"\"" two-words:"($path)=\"1 2\"" unit:"($path)=\"5s\"";do vn=${var%%:*};ex=${var#*:};cfg "$ex";boot $ld $io;nmd=0;grep -q "$nm" $T/boot.out&&nmd=1
  ok "c-$nm-$vn the cell $nm ($vn): rc $brc (want 1), the cell named: $nmd (want 1), $sf setfacl (want 0), $st start (want 0), $uf unit file(s) written (want 0)" '[ $brc = 1 ]&&[ $nmd = 1 ]&&[ $sf = 0 ]&&[ $st = 0 ]&&[ $uf = 0 ]';done;done
# A2b (DG1 21:59Z, found judging A1): the pin gate checks FORMAT, not existence. The unit's own ExecStart line (agi-boot.service), run under sh from the repo: a pin that is 40 zeros, a TREE sha or a well-formed sha absent from the repo must fail LOUD (rc != 0, a git message on stderr, 0 starts); a real commit sha proceeds. The trunk's ExecStart reads HEAD and ignores the pin; A1's reads the pin but runs an empty script (rc 0, nothing booted) for a missing object.
cfg ".";GOODC=$CS;TREE=$($G -C $T/r rev-parse $CS^{tree});UCMD=$(sect agi-boot.service|sed -n 's/^ExecStart=//p')
bootu(){ rm -rf $T/out $T/ram;: >$T/log;echo "0.50 0.5 0.5 1/1 1" >$T/la;printf 'some avg10=0.00 avg60=1.00 avg300=0.00 total=1\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=1\n' >$T/io
 pre AGI_TRUNK=$1&&(set -f;cd $T/r&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=$T/own.cfg GIT_CONFIG_SYSTEM=/dev/null GIT_TEST_ASSUME_DIFFERENT_OWNER=1 $UEG AGI_RAM=$T/ram AGI_BOOT_OUT=$T/out AGI_LOADAVG=$T/la AGI_PSI_IO=$T/io AGI_TRUNK=$1 timeout 60 sh -c "$UCMD" >$T/boot.out 2>&1);brc=$?;st=$(grep -c '^b ' $T/log);ge=$(grep -ciE 'fatal|error|not a valid|unknown revision|bad object' $T/boot.out);}
[ -n "$UCMD" ]||echo "FAIL extract: no ExecStart line in agi-boot.service"
bootu $GOODC;ok "u-the-unit-execstart-with-a-real-commit-pin-boots-both-posts the ExecStart line with AGI_TRUNK=<a commit>: rc $brc (want 0), $st start(s) (want 2)" '[ $brc = 0 ]&&[ $st = 2 ]'
for pin in zeros:0000000000000000000000000000000000000000 tree:$TREE absent:1234567890abcdef1234567890abcdef12345678;do pn=${pin%%:*};bootu ${pin#*:}
 ok "u-the-unit-execstart-with-a-$pn-pin-fails-loud AGI_TRUNK=$pn: rc $brc (want != 0), a git message on stderr: $ge line(s) (want >= 1), $st start(s) (want 0)" '[ $brc != 0 ]&&[ $ge -ge 1 ]&&[ $st = 0 ]';done
# the unit text this lane relies on (NEG: GIT_DIR dropped / the verifier after ExecStart / a - prefix -> RED)
sect agi-boot.service >$T/unit.u;upre=$(grep -n '^ExecStartPre=/usr/local/libexec/agi-vstore$' $T/unit.u|cut -d: -f1);uxs=$(grep -n '^ExecStart=' $T/unit.u|cut -d: -f1);unp=$(grep -c '^ExecStartPre=' $T/unit.u)
ok "k0-the-unit-reads-the-verified-store agi-boot.service: ExecStartPre=/usr/local/libexec/agi-vstore on line ${upre:-none} before ExecStart on line ${uxs:-none}, $unp ExecStartPre line(s) (want 1), Environment GIT_DIR=/run/agi-v.git: $GDW (want 1)" '[ -n "$upre" ]&&[ -n "$uxs" ]&&[ "$upre" -lt "$uxs" ]&&[ "$unp" = 1 ]&&[ "$GDW" = 1 ]'
echo "boot-cells: $f FAIL"
exit $f
