#!/bin/sh
# agi-gate-priv.t.sh: goal:g1.41 B2 (DG1 22:12Z; hypothesis:g141-b-engine-grow-and-post-pieces-...): agi-gate never runs a candidate's agi-project, or the ExecStart text that genome generates, as uid 0. agi-land calls the gate as root, so when its effective uid is 0 it must re-execute itself as an unprivileged user (default nobody) BEFORE the first sect: a ring-signed commit that changes ### agi-project then executes no candidate code as root. The gate must still run the candidate's genome (that is its test): at euid != 0 it behaves as today (duplicate heading rc 2, no regrow rc 1, clean rc 0).
# sh + git on a SCRATCH repo, no real root, no systemd, no network, 0 USD. The REAL piece (`sect agi-gate` from the .geometry/engine*.md of ROOT, default the working tree) runs as an executable file under stubs on PATH: `id -u` prints $FAKE_UID (default 0 = "root"); runuser / setpriv / su / sudo LOG their argv and run the command after the drop with FAKE_UID=65534 (so the unprivileged half sees a non-zero uid) in the env the real `nobody` has: GIT_TEST_ASSUME_DIFFERENT_OWNER=1 (it owns neither the repo nor a safe.directory entry), GIT_CONFIG_GLOBAL=/dev/null, HOME an empty dir, so a piece that re-executes without carrying safe.directory (an exported GIT_CONFIG_COUNT/KEY_0/VALUE_0, or the like) dies `dubious ownership` on its first git read and is RED (DG1 22:34Z, B2 addendum); `sect` logs the uid it ran under and runs the real sect piece. A HOSTILE candidate tip adds `id -u >>MARK` to ITS agi-project: the marker holds the uid every candidate run saw, the direct run and the ExecStart replay alike.
# Lanes: p-* at fake root with the hostile candidate: the drop comes before any sect (0 `sect uid=0`), once, naming a non-root user and carrying the candidate arg, the marker holds only non-zero uids (>= 2 lines = the genome AND the replay); rc is carried through the drop for a clean tip / a duplicate heading / a no-regrow tip. u-* at fake uid 1000: no drop, the three fixtures as today.
# Honest limits: the privilege drop is read off stubs (no real uid change); the lane accepts runuser, setpriv, su or sudo and a re-exec of "$0" with the candidate arg; a gate that drops with another tool is not covered; the unprivileged user is checked as EXACTLY `nobody`, the argument of the tool's user option (an agi_gate_user cell is not read); nobody's read access to the repo path is a deploy fact, not a piece fact (not modelled: the scratch repo is readable); the lane models the ownership refusal with GIT_TEST_ASSUME_DIFFERENT_OWNER, not a real second uid.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};MARK=$T/mark;LOG=$T/log
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE AGI_TRUNK AGI_SEAT AGI_POST FAKE_UID
sect agi-gate >$T/gate;sect sect >$T/sect.real;[ -s $T/gate ]&&[ -s $T/sect.real ]||{ echo "FAIL extract: agi-gate $(wc -c <$T/gate) sect $(wc -c <$T/sect.real)";exit 99;};chmod +x $T/gate
mkdir -p $T/fk $T/hm $T/ho
printf '#!/bin/sh\n[ "$1" = -u ]&&{ echo ${FAKE_UID:-0};exit 0;}\nexec /usr/bin/id "$@"\n' >$T/fk/id
printf '#!/bin/sh\necho "sect uid=$(id -u) $*" >>%s\nexec sh %s "$@"\n' $LOG $T/sect.real >$T/fk/sect
cat >$T/drop<<XX
#!/bin/sh
tool=\${0##*/};echo "\$tool \$*" >>$LOG
has=0;for a in "\$@";do [ "\$a" = -- ]&&has=1;done
if [ \$has = 1 ];then while [ "\$1" != -- ];do shift;done;shift
else case \$tool in
 runuser|su|sudo)c=;prev=;for a in "\$@";do [ "\$prev" = -c ]&&c=\$a;prev=\$a;done
  if [ -n "\$c" ];then set -- sh -c "\$c";else case \$tool in
   runuser)while [ \$# -gt 0 ];do case \$1 in -u|-g|-G|-s)shift 2;;-*)shift;;*)break;;esac;done;;
   sudo)while [ \$# -gt 0 ];do case \$1 in -u|-g|-h|-p)shift 2;;-*)shift;;*)break;;esac;done;;
   su)shift;;esac;fi;;
 setpriv)while [ \$# -gt 0 ];do case \$1 in -*)shift;;*)break;;esac;done;;
esac;fi
exec env FAKE_UID=65534 GIT_TEST_ASSUME_DIFFERENT_OWNER=1 GIT_CONFIG_GLOBAL=/dev/null HOME=$T/ho "\$@"
XX
chmod +x $T/drop $T/fk/id $T/fk/sect;for t in runuser setpriv su sudo;do ln -s $T/drop $T/fk/$t;done
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null
row(){ printf '  - {"name": "%s", "boot": true, "engine": {"v": 4, "harness": "claude-code", "model": "m", "effort": "high"}, "role": "director", "tier": 1, "box": "local-town"}\n' $1;}
# the candidate repo: C0 clean; C1 hostile (its agi-project also writes `id -u` to MARK); C2 duplicate heading; C3 no regrow (an agi-project that projects nothing)
rm -rf $T/c;mkdir -p $T/c/.agi/nodes/.geometry;cp $R0/.agi/nodes/.geometry/engine*.md $T/c/.agi/nodes/.geometry/;{ printf -- '---\nposts:\n';row a;row b;} >$T/c/.agi/nodes/.geometry/posts.md
E=$T/c/.agi/nodes/.geometry/engine.md;$G init -q $T/c;$G -C $T/c add -A;$G -C $T/c commit -qm c0;C0=$($G -C $T/c rev-parse HEAD);cp $E $T/engine.c0
awk -v m="id -u >>$MARK" '/^### agi-project /{h=1} h&&/^~~~/{c++;if(c==2)print m} {print}' $T/engine.c0 >$E;$G -C $T/c commit -qam c1;C1=$($G -C $T/c rev-parse HEAD)
{ cat $T/engine.c0;printf '\n### agi-gate (1 B)\n~~~sh\nx\n~~~\n';} >$E;$G -C $T/c commit -qam c2;C2=$($G -C $T/c rev-parse HEAD)
awk '/^### agi-project /{h=1} h&&/^~~~/{c++;print;if(c==1)print "#!/bin/sh\nexit 0";next} h&&c==1{next} {print}' $T/engine.c0 >$E;$G -C $T/c commit -qam c3;C3=$($G -C $T/c rev-parse HEAD)
[ "$C0" != "$C1" ]&&[ "$C1" != "$C2" ]&&[ "$C2" != "$C3" ]||echo "FAIL fixture: the four candidates are not distinct"
# gate TIP [FAKE_UID]: the real gate piece, cwd = the candidate repo, stubs first on PATH; rc in $grc, logs in $LOG / $MARK
gate(){ rm -f $LOG $MARK;: >$LOG;(cd $T/c&&env -i PATH=$T/fk:/usr/bin:/bin HOME=$T/hm AGI_BOX=local-town GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null ${2:+FAKE_UID=$2} timeout 60 $T/gate $1 >$T/gate.out 2>&1);grc=$?;drops=$(grep -cE '^(runuser|setpriv|su|sudo) ' $LOG);sect0=$(grep -c '^sect uid=0 ' $LOG);sects=$(grep -c '^sect ' $LOG);mk=0;mz=0;[ -f $MARK ]&&{ mk=$(wc -l <$MARK|tr -d ' ');mz=$(grep -cx 0 $MARK||true);};true;}
# u: at an unprivileged uid nothing changes
gate $C0 1000;ok "u-clean-tip-at-uid-1000 a clean tip: rc $grc (want 0), $drops privilege drop(s) (want 0: it is not root), $sects sect call(s) (want >= 1: the candidate's genome still runs)" '[ $grc = 0 ]&&[ $drops = 0 ]&&[ $sects -ge 1 ]'
gate $C2 1000;ok "u-duplicate-heading-at-uid-1000 a tip with a duplicate ### heading: rc $grc (want 2), $drops drop(s) (want 0), $sects sect call(s) (want 0: refused before any sect)" '[ $grc = 2 ]&&[ $drops = 0 ]&&[ $sects = 0 ]'
gate $C3 1000;ok "u-no-regrow-at-uid-1000 a tip whose agi-project projects nothing: rc $grc (want 1), $drops drop(s) (want 0)" '[ $grc = 1 ]&&[ $drops = 0 ]'
gate $C1 1000;ok "u-the-hostile-genome-still-runs-at-uid-1000 the hostile tip at uid 1000: the genome ran and wrote $mk marker line(s) (want >= 2: the direct run and the ExecStart replay), uid 0 among them: $mz (want 0)" '[ $mk -ge 2 ]&&[ $mz = 0 ]'
# p: at fake root with the hostile candidate
gate $C1;first=$(head -1 $LOG|cut -d' ' -f1);dl=$(grep -E '^(runuser|setpriv|su|sudo) ' $LOG|head -1)
ok "p-the-drop-comes-before-any-sect the first thing the gate does at uid 0 is drop privilege: first logged call [$first] (want runuser/setpriv/su/sudo), $sect0 sect call(s) at uid 0 (want 0)" 'case $first in runuser|setpriv|su|sudo)true;;*)false;;esac&&[ $sect0 = 0 ]'
ok "p-the-drop-happens-once $drops privilege drop(s) (want 1: a re-exec, not a loop)" '[ $drops = 1 ]'
nn=0;echo "$dl"|grep -q nobody&&nn=1;ta=0;echo "$dl"|grep -qF "$C1"&&ta=1
ok "p-the-drop-names-a-non-root-user-and-carries-the-candidate argv [$dl]: names nobody $nn (want 1), carries the candidate tip $ta (want 1)" '[ $nn = 1 ]&&[ $ta = 1 ]'
# RB-3: the user is EXACTLY nobody (the argument of the user option of whichever tool), it comes BEFORE the re-exec'd gate path, and the candidate tip is the LAST argument (a `-u daemon -g nobody` or `-u nobodyx` drop used to pass the grep above)
dtool=$(echo "$dl"|cut -d' ' -f1);duser=$(echo "$dl"|awk '{for(i=2;i<=NF;i++){if($i=="-u"||$i=="--reuid"){print $(i+1);exit} if($i~/^--reuid=/){sub(/^--reuid=/,"",$i);print $i;exit}} if($1=="su"){for(i=2;i<=NF;i++){if($i=="-s"||$i=="-c"||$i=="-g"||$i=="-G"){i++;continue} if($i!~/^-/){print $i;exit}}}}')
pu=$(echo "$dl"|awk -v u="$duser" '{for(i=2;i<=NF;i++)if(($i==u||$i=="--reuid="u)&&u!=""){print i;exit}}');pg=$(echo "$dl"|awk -v g="$T/gate" '{for(i=2;i<=NF;i++)if($i==g){print i;exit}}');nf=$(echo "$dl"|awk '{print NF}');lastw=$(echo "$dl"|awk '{print $NF}')
ok "p-the-drop-user-is-exactly-nobody-and-comes-before-the-reexec the drop [$dtool] runs as [$duser] (want exactly nobody), the user is word ${pu:-none} and the re-exec'd gate word ${pg:-none} (want user < gate), the last word is the candidate tip: [$lastw] (want $C1)" '[ "$duser" = nobody ]&&[ -n "$pu" ]&&[ -n "$pg" ]&&[ "$pu" -lt "$pg" ]&&[ "$lastw" = "$C1" ]'
ok "p-the-hostile-genome-ran-only-unprivileged the hostile tip's own code (direct run + the replayed ExecStart) saw uids: $mk marker line(s) (want >= 2), $mz of them uid 0 (want 0)" '[ $mk -ge 2 ]&&[ $mz = 0 ]'
ok "p-the-gate-still-passes-the-clean-genome-at-root the hostile-but-valid tip run from root: rc $grc (want 0: the genome still regrows)" '[ $grc = 0 ]'
gate $C0;ok "p-rc-is-carried-clean-tip a clean tip from root: rc $grc (want 0), $sect0 sect call(s) at uid 0 (want 0)" '[ $grc = 0 ]&&[ $sect0 = 0 ]'
gate $C2;ok "p-rc-is-carried-duplicate-heading a duplicate heading from root: rc $grc (want 2), $sect0 sect call(s) at uid 0 (want 0; whether the drop precedes the heading check is the builder's)" '[ $grc = 2 ]&&[ $sect0 = 0 ]'
gate $C3;ok "p-rc-is-carried-no-regrow a no-regrow tip from root: rc $grc (want 1), $sect0 sect call(s) at uid 0 (want 0)" '[ $grc = 1 ]&&[ $sect0 = 0 ]'
echo "agi-gate-priv: $f FAIL"
exit $f
