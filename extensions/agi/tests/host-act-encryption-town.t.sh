#!/bin/sh
# host-act-encryption-town.t.sh: the REHEARSAL of extensions/agi/guard/host-act-encryption-town.sh (ROOT=<scratch>, no systemd, no root): step 0 + the act + the rollback + the per-post move, on a scratch MAIN holding the REAL geometry. One ok/FAIL line per case; exit = FAIL count. ACT=<script copy> runs a mutant.
umask 022;T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=$(cd "$(dirname "$0")/../../.." && pwd);ACT=${ACT:-$R0/extensions/agi/guard/host-act-encryption-town.sh};GEO=$R0/.agi/nodes/.geometry
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_AUTHOR_NAME GIT_COMMITTER_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_EMAIL;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
mk(){ X=$T/$1;rm -rf $X;mkdir -p $X/data/work/agi/.agi/nodes/.geometry $X/opt/agi/bin $X/etc/systemd/system $X/etc/polkit-1/rules.d $X/usr/local $X/mnt $X/var/lib;M=$X/data/work/agi;cp $GEO/engine*.md $M/.agi/nodes/.geometry/
 { printf '%s\n' '---' 'posts:';printf '  - {"name":"xp","box":"encryption-town","engine":{"v":4,"name":"xp","harness":"claude-code","model":"m","effort":"low"}}\n  - {"name":"lp","box":"local-town","engine":{"v":4,"name":"lp","harness":"claude-code","model":"m","effort":"low"}}\n';printf '%s\n' '---';} >$M/.agi/nodes/.geometry/posts.md
 [ -z "$CFG" ]||printf '%s\n' "$CFG">$M/.agi/config.json
 [ -n "$NOCOMMS" ]||{ mkdir -p $M/.agi/comms/season-2/dm;echo x>$M/.agi/comms/season-2/dm/a--b.md;}
 git init -q $M;git -C $M add -A;git -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm fx;PIN=$(git -C $M rev-parse HEAD);printf '#!/bin/sh\n' >$X/opt/agi/bin/pi;chmod +x $X/opt/agi/bin/pi;}
run(){ ( cd $T;env -i PATH=$PATH HOME=$T ROOT=$X PIN=${PIN} AGI_REPO=/data/work/agi STUB_X=$X STUB_M=$X/data/work/agi "$@" );}
# one line per getfacl record, sorted: readdir order differs between filesystems (tmpfs moves .git/index when it is rewritten), the content does not
acls(){ { getfacl -R -p $X/data/work/agi/.git $X/data/work/agi/.agi/comms;getfacl -p $X/data/work/agi/.agi/sessions;} 2>/dev/null|awk 'BEGIN{RS=""}{gsub(/\n/,"|");print}'|sort;}
tree(){ (cd $X&&find . -path ./data -prune -o -path ./var/backups -prune -o -print|sort|xargs -I{} stat -c '%a %n' {});}
# ---- a clean E: the act installs exactly the pinned bytes ----
PU=agi-post@;GG=$(id -gn);mk a;before=$(tree);acl0=$(acls);run sh $ACT act>$T/a.out 2>$T/a.err;ra=$?
ok a1-act-exits-0-and-names-the-backup "[ $ra = 0 ]&&grep -q '^backup .*rollback: sh ' $T/a.out"
ok a2-carry-env-is-exactly-the-five-cells "[ \"\$(cat $X/etc/agi/carry.env)\" = \"\$(printf 'AGI_BOX=encryption-town\nAGI_HUB=\nAGI_REPO=/data/work/agi\nAGI_TRUNK=%s\nGIT_CONFIG_VALUE_0=/data/work/agi\n' $PIN)\" ]"
for p in agi-vstore:usr/local/libexec/agi-vstore sect:opt/agi/bin/sect box:opt/agi/bin/box box-carry:opt/agi/bin/box-carry agi-signers:opt/agi/bin/agi-signers;do n=${p%%:*};d=${p#*:}
 ok "a3-$n-is-the-pinned-section-byte-for-byte" "sect $n|cmp -s - $X/$d&&[ \$(stat -c %a $X/$d) = 755 ]";done
for u in agi-carry@.service agi-carry@.path agi-carry-fetch.service agi-carry-fetch.timer agi-boot.service;do ok "a4-unit-$u-is-the-pinned-section" "sect $u|cmp -s - $X/etc/systemd/system/$u&&[ \$(stat -c %a $X/etc/systemd/system/$u) = 644 ]";done
ok a5-polkit-rule-is-the-pinned-section "sect agi.rules|cmp -s - $X/etc/polkit-1/rules.d/50-agi.rules"
ok a6-the-boot-unit-keeps-its-pinned-ram-lines-and-no-dropin-exists "sect agi-boot.service|cmp -s - $X/etc/systemd/system/agi-boot.service&&grep -q '^Requires=agi-ram-main.service' $X/etc/systemd/system/agi-boot.service&&[ ! -e $X/etc/systemd/system/agi-boot.service.d ]"
ok a7-ram-is-a-plain-directory-and-agi-ram-main-is-a-noop-oneshot "[ -d $X/mnt/agi-ram/state ]&&U=$X/etc/systemd/system/agi-ram-main.service&&grep -qx 'Type=oneshot' \$U&&grep -qx 'RemainAfterExit=yes' \$U&&grep -qx 'ExecStart=/bin/true' \$U&&grep -q '^Description=encryption-town: no RAM disk, MAIN on the internal drive' \$U&&! grep -v '^#' \$U|grep -q 'mount\|^Requires\|^After'"
ok a7b-systemd-analyze-verifies-the-root-copies-when-present "(command -v systemd-analyze>/dev/null||exit 0;V=\$(mktemp -d);cp $X/etc/systemd/system/agi-*.service $X/etc/systemd/system/agi-*.path $X/etc/systemd/system/agi-*.timer $X/etc/systemd/system/agi.slice \$V/;systemd-analyze verify \$V/agi-ram-main.service \$V/agi-boot.service 2>\$T/v.err;rv=\$?;rm -rf \$V;[ \$rv = 0 ])"
ok a8-slice-has-finite-memory-and-oom-kill "grep -qx 'MemoryHigh=5G' $X/etc/systemd/system/agi.slice&&grep -qx 'MemoryMax=6G' $X/etc/systemd/system/agi.slice&&grep -qx 'ManagedOOMMemoryPressure=kill' $X/etc/systemd/system/agi.slice"
ok a9-no-engine-byte-changed-in-main "[ -z \"\$(git -C $X/data/work/agi status --porcelain)\" ]"
ok a10-no-crontab-and-nothing-outside-the-scratch "[ ! -e $X/var/spool/cron ]&&[ \$(grep -c 'crontab' $T/a.out) = 0 ]"
# ---- the MAIN ACL (belam G2 10-08 22:3xZ): the post users must create refs, objects, logs and worktrees in MAIN's .git ----
GD=$X/data/work/agi/.git
ok f1-main-acl-group-rwx-and-default-on-the-four-dirs "(for d in objects refs logs worktrees;do getfacl -p $GD/\$d 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p $GD/\$d 2>/dev/null|grep -qx \"default:group:$GG:rwx\"||exit 1;done;getfacl -p $GD/refs/heads/* 2>/dev/null|grep -qx \"group:$GG:rw-\")"
mkdir $GD/refs/heads/zz $GD/objects/zz
ok f2-a-dir-made-later-inherits-the-group-acl "getfacl -p $GD/refs/heads/zz 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p $GD/objects/zz 2>/dev/null|grep -qx \"default:group:$GG:rwx\""
ok f3-main-acl-names-the-prime-user-with-defaults-and-a-later-dir-inherits-it "(for d in objects refs logs worktrees;do getfacl -p $GD/\$d 2>/dev/null|grep -qx \"user:$(id -un):rwx\"&&getfacl -p $GD/\$d 2>/dev/null|grep -qx \"default:user:$(id -un):rwx\"||exit 1;done;getfacl -p $GD/refs/heads/zz 2>/dev/null|grep -qx \"user:$(id -un):rwx\")"
rmdir $GD/refs/heads/zz $GD/objects/zz
SS=$X/data/work/agi/.agi/sessions
ok g2-sessions-has-group-rwx-and-default-rwx "getfacl -p $SS 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p $SS 2>/dev/null|grep -qx \"default:group:$GG:rwx\"&&grep -q 'sessions ACL g:$GG:rwx' $T/a.out"
IB=$X/data/work/agi/.agi/sessions/inbox
ok g1-inbox-has-group-rwx-default-rw-and-mode-775 "getfacl -p $IB 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p $IB 2>/dev/null|grep -qx \"default:group:$GG:rw-\"&&[ \$(stat -c %a $IB) = 775 ]"
CD=$X/data/work/agi/.agi/comms;PUN=$(id -un)
ok h1-comms-acl-group-and-prime-user-rwx-with-defaults-on-every-dir "(for d in $CD $CD/season-2 $CD/season-2/dm;do getfacl -p \$d 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p \$d 2>/dev/null|grep -qx \"user:$PUN:rwx\"&&getfacl -p \$d 2>/dev/null|grep -qx \"default:group:$GG:rwx\"&&getfacl -p \$d 2>/dev/null|grep -qx \"default:user:$PUN:rwx\"||exit 1;done;getfacl -p $CD/season-2/dm/a--b.md 2>/dev/null|grep -qx \"group:$GG:rw-\")"
mkdir $CD/season-2/zz
ok h2-a-comms-dir-made-later-inherits-both-entries "getfacl -p $CD/season-2/zz 2>/dev/null|grep -qx \"group:$GG:rwx\"&&getfacl -p $CD/season-2/zz 2>/dev/null|grep -qx \"user:$PUN:rwx\"&&getfacl -p $CD/season-2/zz 2>/dev/null|grep -qx \"default:user:$PUN:rwx\""
rmdir $CD/season-2/zz
ok h3-the-act-names-the-comms-acl "grep -q 'comms ACL g:$GG:rwX + u:$PUN:rwX' $T/a.out"
# ---- the rollback: back to the before-state, modes included ----
rb=$(sed -n 's/.*rollback: sh //p' $T/a.out);sh $rb>$T/rb.out 2>&1;rr=$?
ok b1-rollback-restores-an-untouched-E "[ $rr = 0 ]&&[ \"\$(tree)\" = \"$before\" ]"
ok b2-rollback-restores-the-main-acl-and-drops-the-worktrees-dir "[ \"\$(acls)\" = \"\$acl0\" ]&&[ ! -e $GD/worktrees ]&&[ ! -e $IB ]&&[ ! -e $SS ]"
ok b3-rollback-leaves-the-comms-bytes-and-no-acl-on-them "[ \"\$(cat $CD/season-2/dm/a--b.md)\" = x ]&&! getfacl -R -p $CD 2>/dev/null|grep -q '^default:\\|^user:[a-z]\\|^group:[a-z]'"
# ---- an E with an old file of non-default mode: restored with its bytes and mode ----
mk c;mkdir -p $X/data/work/agi/.agi/sessions/inbox;chmod 750 $X/data/work/agi/.agi/sessions/inbox;mkdir -p $X/etc/agi;echo OLD>$X/etc/agi/carry.env;chmod 640 $X/etc/agi/carry.env;before=$(tree);echo x>$X/data/work/agi/.agi/sessions/f.tsv;echo 7 >$X/data/work/agi/.agi/sessions/.grid.lock;run sh $ACT act>$T/c.out 2>$T/c.err;rc=$?;getfacl -p $X/data/work/agi/.agi/sessions/.grid.lock 2>/dev/null|grep -qx "group:$GG:rw-"&&gl=1||gl=0;getfacl -p $X/data/work/agi/.agi/sessions/f.tsv 2>/dev/null|grep -q '^[a-z:]*group:[a-z]'&&gf=1||gf=0;rb=$(sed -n 's/.*rollback: sh //p' $T/c.out);sh $rb>/dev/null 2>&1
ok c2-an-old-inbox-comes-back-with-its-mode-and-no-group-acl "[ \$(stat -c %a $X/data/work/agi/.agi/sessions/inbox) = 750 ]&&! getfacl -p $X/data/work/agi/.agi/sessions/inbox 2>/dev/null|grep -q '^[a-z:]*group:[a-z]'"
ok c3-an-old-sessions-dir-comes-back-without-the-group-acl "! getfacl -p $X/data/work/agi/.agi/sessions 2>/dev/null|grep -q '^[a-z:]*group:[a-z]'&&[ \$(stat -c %a $X/data/work/agi/.agi/sessions) = 755 ]"
ok c5-an-existing-grid-lock-gets-its-own-group-rw-entry "[ $gl = 1 ]&&grep -q 'lock ACL g:$GG:rw on' $T/c.out"
ok c6-the-grid-lock-comes-back-without-the-group-entry-and-with-its-bytes "! getfacl -p $X/data/work/agi/.agi/sessions/.grid.lock 2>/dev/null|grep -q '^[a-z:]*group:[a-z]'&&[ \"\$(cat $X/data/work/agi/.agi/sessions/.grid.lock)\" = 7 ]"
ok c4-the-sessions-acl-is-not-recursive-a-file-in-it-keeps-its-acl "[ $gf = 0 ]"
ok c1-an-old-carry-env-comes-back-with-its-bytes-and-mode "[ $rc = 0 ]&&[ \"\$(cat $X/etc/agi/carry.env)\" = OLD ]&&[ \$(stat -c %a $X/etc/agi/carry.env) = 640 ]&&[ \"\$(tree)\" = \"$before\" ]"
# ---- a MAIN with no comms dir: the act makes it, the rollback removes it; an absent prime user is refused with nothing written ----
NOCOMMS=1 mk h;[ ! -e $X/data/work/agi/.agi/comms ];run sh $ACT act>$T/h.out 2>$T/h.err;rh=$?;rb=$(sed -n 's/.*rollback: sh //p' $T/h.out);sh $rb>/dev/null 2>&1
ok h4-an-absent-comms-dir-is-made-and-rolled-back "[ $rh = 0 ]&&grep -q 'comms ACL' $T/h.out&&[ ! -e $X/data/work/agi/.agi/comms ]"
mk i;before=$(tree);run env PRIME_USER=nosuchuser-zz sh $ACT act>/dev/null 2>$T/i.err;ri=$?
ok h5-an-absent-prime-user-is-refused-and-nothing-is-written "[ $ri != 0 ]&&grep -q 'PREREQ: user nosuchuser-zz' $T/i.err&&[ ! -e $X/var/backups ]&&[ \"\$(tree)\" = \"$before\" ]"
# ---- a recorded path that vanished before the rollback (a loose object gc'd, a comms file renamed): the ACL restore warns and the later undo steps STILL run ----
mk j;mkdir -p $X/run/systemd/system;run sh $ACT act>$T/j.out 2>$T/j.err;rb=$(sed -n 's/.*rollback: sh //p' $T/j.out)
: >$X/run/systemd/system/agi-junk.service;rm -f $X/data/work/agi/.git/logs/HEAD
sh $rb>$T/j.rb 2>$T/j.rberr;rj=$?
ok j1-a-vanished-recorded-path-warns-and-the-rollback-finishes "[ $rj = 0 ]&&grep -q 'rollback: acl restore rc' $T/j.rberr&&grep -q '^rolled back from' $T/j.rb"
ok j2-the-later-undo-steps-ran-run-list-absent-files-and-act-made-dirs "[ ! -e $X/run/systemd/system/agi-junk.service ]&&[ ! -e $X/etc/agi/carry.env ]&&[ ! -e $X/data/work/agi/.agi/sessions ]&&[ ! -e $X/data/work/agi/.git/worktrees ]"
ok j3-the-rollback-echo-says-a-filled-act-made-dir-stays "grep -q 'act-made dir that posts have filled since stays' $T/j.rb"
# ---- refusals write NOTHING ----
mk d;before=$(tree);run env PIN=zz sh $ACT act>/dev/null 2>$T/d1.err;r1=$?;run env PIN=0000000000000000000000000000000000000000 sh $ACT act>/dev/null 2>$T/d2.err;r2=$?;rm $X/opt/agi/bin/pi;run sh $ACT act>/dev/null 2>$T/d3.err;r3=$?
ok d1-a-bad-pin-is-refused-by-name "[ $r1 != 0 ]&&grep -q 'PIN must be' $T/d1.err"
ok d2-a-pin-that-is-no-commit-is-refused "[ $r2 != 0 ]&&grep -q 'is not a commit' $T/d2.err"
ok d3-no-pi-is-refused-and-nothing-is-written "[ $r3 != 0 ]&&grep -q 'PREREQ: no pi' $T/d3.err&&[ ! -e $X/var/backups ]&&[ ! -e $X/etc/agi ]&&[ \"\$(tree)\" = \"\$(echo \"$before\"|grep -v opt/agi/bin/pi)\" ]"
# ---- the per-post move ----
mk e;run sh $ACT act>/dev/null 2>&1;echo "AGI_TRUNK=$PIN">/dev/null
M=$X/data/work/agi;sed -i 's/"effort":"low"}}/"effort":"high"}}/' $M/.agi/nodes/.geometry/posts.md;git -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qam bump;PIN2=$(git -C $M rev-parse HEAD)
mkdir -p $X/run/systemd/system/${PU}xp.service.d;: >$X/run/systemd/system/${PU}xp.service.d/h.conf;mkdir -p $X/run/systemd/system/multi-user.target.wants
run env PIN=$PIN2 sh $ACT move xp>$T/e.out 2>$T/e.err;re=$?
ok e1-move-bumps-the-pin-and-keeps-the-old-env "[ $re = 0 ]&&grep -qx \"AGI_TRUNK=$PIN2\" $X/etc/agi/carry.env&&grep -qx \"AGI_TRUNK=$PIN\" $X/etc/agi/carry.env.before-xp&&grep -q 'moved: xp' $T/e.out"
ok e5-move-names-the-agi-box-a-shell-on-E-needs "grep -q 'needs AGI_BOX=encryption-town' $T/e.out"
cp $X/etc/agi/carry.env $T/env.keep;run env PIN=$PIN2 sh $ACT move lp>/dev/null 2>$T/e2.err;re2=$?
ok e2-a-post-whose-row-is-another-box-is-refused-and-nothing-changes "[ $re2 != 0 ]&&grep -q 'is not box encryption-town' $T/e2.err&&cmp -s $X/etc/agi/carry.env $T/env.keep"
rm -rf $X/run/systemd/system/${PU}xp.service.d;ln -s ../agi-post@.service $X/run/systemd/system/multi-user.target.wants/${PU}xp.service;run env PIN=$PIN2 sh $ACT move xp>/dev/null 2>$T/e4.err;re4=$?
ok e4-projection-is-the-hconf-dropin-not-the-wants-link "[ $re4 != 0 ]&&grep -q 'not projected (no h.conf' $T/e4.err"
run env PIN=$PIN2 sh $ACT move 'bad name'>/dev/null 2>$T/e3.err;ok e3-a-bad-post-name-is-refused "[ \$? != 0 ]"
# ---- S2a (goal:g7.16.1.11.44.8, council 09:20Z 10-16): the act lives in `agi.sh host`; the old script's `act` is ONE delegating line. Each row has its mutant (one edit on the code under test; the row passes only when the clean property BREAKS) ----
AGI=${AGI:-$R0/extensions/agi/bin/agi.sh}
rep(){ A=$1 B=$2 awk '{o="";r=$0;while((i=index(r,ENVIRON["A"]))>0){o=o substr(r,1,i-1) ENVIRON["B"];r=substr(r,i+length(ENVIRON["A"]))}print o r}' $AGI>$T/mut.sh;cmp -s $AGI $T/mut.sh&&echo "# NO EDIT for [$1]";}
backups(){ ls -d $X/var/backups/agi-act-* 2>/dev/null|wc -l|tr -d ' ';}
# the `act)` branch of the old script (condition 1): exactly the one exec line, no step of its own left in it
onebranch(){ b=$(sed -n '/^act)/,/^move)/p' $1|sed '$d');[ "$(echo "$b"|wc -l|tr -d ' ')" = 1 ]&&echo "$b"|grep -qx 'act)exec sh "$(dirname "$0")/../bin/agi.sh" host;;'&&! echo "$b"|grep -q 'setfacl\|install\|put\|systemctl\|printf\|mkdir';}
unitread(){ env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory $(grep '^GIT_CONFIG_VALUE_0=' $X/etc/agi/carry.env 2>/dev/null) git config --get safe.directory 2>/dev/null;}
ok k1-the-old-act-branch-is-one-exec-line-and-no-step-of-its-own "onebranch $ACT"
sed '/^act)/a setfacl -m g:x:rwx /nonexistent' $ACT>$T/act.mut;cmp -s $ACT $T/act.mut&&echo "# NO EDIT in the act mutant"
ok k1-mutant-an-act-branch-that-runs-its-own-step-is-RED "! onebranch $T/act.mut"
mk k;run sh $AGI host>$T/k.out 2>$T/k.err;rk=$?
ok k2-carry-env-keeps-GIT_CONFIG_VALUE_0-and-the-stub-unit-read-prints-the-repo "[ $rk = 0 ]&&grep -qx 'GIT_CONFIG_VALUE_0=/data/work/agi' $X/etc/agi/carry.env&&[ \"\$(unitread)\" = /data/work/agi ]"
rep '\nGIT_CONFIG_VALUE_0=%s\n'"'"' $BOX $M $PIN $M' '\n'"'"' $BOX $M $PIN';mk k;run sh $T/mut.sh host>/dev/null 2>&1
ok k2-mutant-carry-env-without-VALUE_0-is-RED "[ \"\$(unitread)\" != /data/work/agi ]&&! grep -q GIT_CONFIG_VALUE_0 $X/etc/agi/carry.env"
# condition 8: the check runs BEFORE step 0, so a host that is already as the pin says gets no second backup
mk m;run sh $AGI host>$T/m1.out 2>&1;n1=$(backups);run sh $AGI host>$T/m2.out 2>&1;r2=$?;n2=$(backups)
ok k3-a-second-run-is-met-and-takes-no-backup "[ $n1 = 1 ]&&[ $r2 = 0 ]&&[ $n2 = 1 ]&&grep -qx 'host: met' $T/m2.out&&[ \"\$(grep -c '^backup ' $T/m2.out)\" = 0 ]"
rep 'hostmet(){ ' 'hostmet(){ return 1;';mk m;run sh $T/mut.sh host>/dev/null 2>&1;sleep 1;run sh $T/mut.sh host>$T/mm2.out 2>&1
ok k3-mutant-hostmet-false-is-RED "[ \$(backups) = 2 ]"   # a check that never says met: 2 backups after two runs (the clean row keeps 1)
# a piece that drifted, an ACL that was removed: NOT met; the act re-runs (a new backup) and puts the pinned bytes back
mk q;run sh $AGI host>/dev/null 2>&1;echo drift>>$X/opt/agi/bin/sect;sleep 1;run sh $AGI host>$T/q.out 2>&1;rq=$?
ok k3-a-drifted-piece-is-not-met-and-is-restored "[ $rq = 0 ]&&! grep -qx 'host: met' $T/q.out&&[ $(backups) = 2 ]&&sect sect|cmp -s - $X/opt/agi/bin/sect"
mk q;run sh $AGI host>/dev/null 2>&1;setfacl -x g:$GG $X/data/work/agi/.agi/sessions/inbox;sleep 1;run sh $AGI host>$T/q2.out 2>&1;rq2=$?
ok k3-a-removed-inbox-acl-is-not-met-and-is-restored "[ $rq2 = 0 ]&&! grep -qx 'host: met' $T/q2.out&&getfacl -p $X/data/work/agi/.agi/sessions/inbox 2>/dev/null|grep -qx \"group:$GG:rwx\""
mk q;run sh $AGI host>/dev/null 2>&1;sed -i 's/^MemoryMax=6G/MemoryMax=9G/' $X/etc/systemd/system/agi.slice;sleep 1;run sh $AGI host>$T/q3.out 2>&1
ok k3-an-edited-slice-is-not-met-and-is-restored "grep -qx 'MemoryMax=6G' $X/etc/systemd/system/agi.slice&&! grep -qx 'host: met' $T/q3.out"
# the hub's fetch timer: enabled only when the cell is true at the pin (default false)
ok k4-cell-absent-no-enable-line "! grep -q 'rehearsal: systemctl enable --now agi-carry-fetch.timer' $T/m1.out"
CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":false}}}}';mk n;CFG=;run sh $AGI host>$T/n0.out 2>&1
CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":true}}}}';mk n;CFG=;run sh $AGI host>$T/n1.out 2>&1
ok k4-cell-false-no-line-cell-true-the-line "! grep -q 'rehearsal: systemctl enable --now agi-carry-fetch.timer' $T/n0.out&&grep -qx 'rehearsal: systemctl enable --now agi-carry-fetch.timer' $T/n1.out"
rep 'tm(){ [ "$CF" = true ]||return 0;' 'tm(){ ';CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":false}}}}';mk n;CFG=;run sh $T/mut.sh host>$T/n2.out 2>&1
ok k4-mutant-the-ungated-enable-is-RED "grep -qx 'rehearsal: systemctl enable --now agi-carry-fetch.timer' $T/n2.out"
mk r;run env PIN=zz sh $AGI host>/dev/null 2>$T/r.err;rr=$?
ok k5-agi-sh-host-refuses-a-bad-pin-by-name "[ $rr != 0 ]&&grep -q 'PIN must be' $T/r.err&&[ ! -e $X/var/backups ]"
ok k6-the-row-is-in-the-matrix-and-the-act-writes-no-sudoers "sect matrix|grep -qP '^town\\tstart\\tmain host posts crons units blast\\tagi.sh\$'&&[ ! -e $X/etc/sudoers.d ]&&! sed -n '/^up_host()/,/^);}\$/p' $AGI|grep -q 'sudoers\\|visudo'"
# ---- council RETURN R1 (11:22Z 10-16): a FAILED act must not re-run as "host: met". /etc/agi/host.done = the PIN is the act's LAST write (cleared before its first); hostmet requires it; stop never touches it.
# AGI_HOST_UNITS=<stub dir> makes the rehearsal run the live tail (verify, daemon-reload, timer, enable agi-boot: ENABLE only, council 10-21 (2)) against these stubs.
# council 17:58Z 10-21: agi-project.path never runs on the box, so `start agi-project.service` is the ONLY projection. The stubs' `proj` helper runs the REAL agi-project piece of carry.env's pin the way the unit's ExecStart does, into $STUB_X/run/systemd/system; STUB_NOPROJ=1 = a start that returns 0 and projects nothing
PROJ='#!/bin/sh
[ -z "$STUB_NEEDUNIT" ]||[ -e $STUB_X/run/systemd/system/agi-project.service ]||{ echo "Unit agi-project.service not found." >&2;exit 5;}
[ -z "$STUB_NOPROJ" ]||exit 0
pin=$(sed -n "s/^AGI_TRUNK=//p" $STUB_X/etc/agi/carry.env 2>/dev/null);[ -n "$pin" ]||exit 1;U=$STUB_X/run/systemd/system;mkdir -p $U;f=$(mktemp)||exit 1
git -C $STUB_M ls-tree --full-tree --name-only $pin .agi/nodes/.geometry/|grep "/engine[^/]*\.md\$"|sed "s|^|$pin:|"|git -C $STUB_M cat-file --batch --follow-symlinks|sed -n "/^###* agi-project /,/^###* /{/^~~~/,/^~~~/{//!p}}">$f;[ -s $f ]||{ rm -f $f;exit 1;}
(cd $STUB_M&&AGI_BOX=${STUB_BOX:-encryption-town} sh $f $U $pin);r=$?;rm -f $f;exit $r'
SHD=$T/shd;mkdir -p $SHD;printf '%s\n' "$PROJ" >$SHD/proj;printf '#!/bin/sh\n[ "$STUB_FAIL" = verify ]&&exit 1;exit 0\n' >$SHD/systemd-analyze
cat >$SHD/systemctl <<'XEOF'
#!/bin/sh
pin=;[ "$1 $2" = "start agi-project.service" ]&&pin=" pin=$(sed -n 's/^AGI_TRUNK=//p' $STUB_X/etc/agi/carry.env 2>/dev/null)"
echo "$*$pin">>$STUB_LOG
case $1 in is-enabled)case $2 in agi-carry-fetch.timer)echo "${STUB_IS_T-enabled}";exit ${STUB_IS_T_RC:-0};;esac;echo "${STUB_IS-enabled}";exit ${STUB_IS_RC:-0};;esac
[ "$STUB_FAIL" = "$1" ]&&exit 1
[ "$1 $2" = "start agi-project.service" ]&&{ sh "$(dirname "$0")/proj"||exit 1;}
exit 0
XEOF
chmod +x $SHD/*
hu(){ run env PATH=$SHD:$PATH AGI_HOST_UNITS=$SHD AGI_TOWN_STATE=$T/ts STUB_LOG=$T/sc.log STUB_FAIL=$1 STUB_NOPROJ=$NOPROJ STUB_NEEDUNIT=$NEEDUNIT sh ${2:-$AGI} host;}
HD=etc/agi/host.done
mk s;: >$T/sc.log;hu "">$T/s1.out 2>&1;rs1=$?
ok r1-a-completed-act-writes-host-done-pin-mode-644-and-runs-the-tail-enabling-agi-boot-without-starting-it "[ $rs1 = 0 ]&&[ \"\$(cat $X/$HD)\" = $PIN ]&&[ \$(stat -c %a $X/$HD) = 644 ]&&grep -qx 'daemon-reload' $T/sc.log&&grep -qx 'enable agi-boot.service' $T/sc.log&&! grep -q 'start agi-boot.service' $T/sc.log&&! grep -q 'carry-fetch' $T/sc.log"
sleep 1;hu "">$T/s2.out 2>&1;rs2=$?
ok r1-a-the-second-run-is-met-and-no-new-backup "[ $rs2 = 0 ]&&grep -qx 'host: met' $T/s2.out&&[ \$(backups) = 1 ]"
for F in verify enable;do mk t;: >$T/sc.log;hu $F>$T/t1.out 2>$T/t1.err;rt1=$?;sleep 1;hu "">$T/t2.out 2>&1;rt2=$?;hu "">$T/t3.out 2>&1
 ok "r1-b-a-stub-failing-at-$F-leaves-no-marker-and-the-re-run-is-NOT-met" "[ $rt1 != 0 ]&&grep -q 'rollback.sh' $T/t1.err&&[ $rt2 = 0 ]&&! grep -qx 'host: met' $T/t2.out&&[ \$(backups) = 2 ]&&[ \"\$(cat $X/$HD)\" = $PIN ]&&grep -qx 'host: met' $T/t3.out";done
mk t;hu verify>/dev/null 2>&1;ok r1-b-after-a-failed-act-there-is-no-host-done "[ ! -e $X/$HD ]"
# the old marker must not survive a re-run that dies: drift a piece, re-run with a failing enable, the next run must not be met
mk u;hu "">/dev/null 2>&1;echo drift>>$X/opt/agi/bin/sect;sleep 1;hu enable>/dev/null 2>&1;sleep 1;hu "">$T/u3.out 2>&1
ok r1-c-a-re-run-that-dies-clears-the-old-marker-so-the-next-run-is-not-met "! grep -qx 'host: met' $T/u3.out&&sect sect|cmp -s - $X/opt/agi/bin/sect"
mk u;hu "">/dev/null 2>&1;echo 0000000000000000000000000000000000000000>$X/$HD;sleep 1;hu "">$T/u4.out 2>&1
ok r1-c-a-marker-holding-another-pin-is-not-met "! grep -qx 'host: met' $T/u4.out&&[ \"\$(cat $X/$HD)\" = $PIN ]"
mk u;hu "">/dev/null 2>&1;echo drift>>$X/opt/agi/bin/sect;sleep 1;hu "">/dev/null 2>&1;sh $(ls -d $X/var/backups/agi-act-*|tail -1)/rollback.sh>/dev/null 2>&1
ok r1-c-the-rollback-of-a-re-run-restores-the-old-marker "[ \"\$(cat $X/$HD)\" = $PIN ]"
# MUTANTS: each is one edit on agi.sh, and the clean row above must BREAK
rep '&&[ "$(cat $R/etc/agi/host.done 2>/dev/null)" = $PIN ]' '';mk t;hu enable $T/mut.sh>/dev/null 2>&1;sleep 1;hu "" $T/mut.sh>$T/m1.out 2>&1   # a failed act that got past the projection (since 17:58Z a verify failure leaves nothing projected, so projmet alone would say not met)
ok r1-mutant-hostmet-without-host-done-says-met-after-a-failed-act-is-RED "grep -qx 'host: met' $T/m1.out"
rep 'rm -f $R/etc/agi/host.done||exit 1' ':';mk u;hu "">/dev/null 2>&1;echo drift>>$X/opt/agi/bin/sect;sleep 1;hu enable $T/mut.sh>/dev/null 2>&1;sleep 1;hu "" $T/mut.sh>$T/m2.out 2>&1
ok r1-mutant-an-old-marker-kept-through-a-dying-re-run-says-met-RED "grep -qx 'host: met' $T/m2.out"
rep 'printf '"'"'%s\n'"'"' $PIN>$R/etc/agi/host.done&&chmod 644 $R/etc/agi/host.done||exit 1' ':';mk t;hu "" $T/mut.sh>$T/m3.out 2>&1;sleep 1;hu "" $T/mut.sh>$T/m3b.out 2>&1
ok r1-mutant-no-host-done-write-never-becomes-met-RED "[ ! -e $X/$HD ]&&! grep -qx 'host: met' $T/m3b.out"
# stop never touches it: every host.done in agi.sh sits inside up_host
ok r1-stop-never-touches-host-done "[ \$(grep -v '^#' $AGI|grep -c 'host[.]done') -gt 0 ]&&[ \$(awk '/^up_host\\(\\)/{i=1}/^ck_host\\(\\)/{i=0}i&&/host[.]done/&&!/^#/{n++}END{print n+0}' $AGI) = \$(grep -v '^#' $AGI|grep -c 'host[.]done') ]"
sed 's|^dn_host(){ return 0;}|dn_host(){ rm -f /etc/agi/host.done;}|' $AGI>$T/mut.sh;cmp -s $AGI $T/mut.sh&&echo "# NO EDIT for dn_host mutant"
ok r1-mutant-dn_host-removing-it-is-RED "! [ \$(awk '/^up_host\\(\\)/{i=1}/^ck_host\\(\\)/{i=0}i&&/host[.]done/&&!/^#/{n++}END{print n+0}' $T/mut.sh) = \$(grep -v '^#' $T/mut.sh|grep -c 'host[.]done') ]"
# the timer on the live tail: a cell true enables it, false does not (the stub log)
CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":true}}}}';mk n;CFG=;: >$T/sc.log;hu "">/dev/null 2>&1
ok r1-d-carry-fetch-true-enables-the-timer-on-the-live-tail "grep -qx 'enable --now agi-carry-fetch.timer' $T/sc.log"
# ---- S2b FIRST COMMIT (council 10-21 residues R-a, R-b, R-c, B3): each k-row has its one-edit mutant ----
# R-a: the rollback row could not fail (old and new marker were both $PIN). A first act on a clean tree then rollback.sh leaves NO marker; an old marker of a second pin comes back byte-equal.
P2=2222222222222222222222222222222222222222
lastrb(){ ls -d $X/var/backups/agi-act-*|tail -1;}
rbrow(){ AX=${1:-$AGI}   # prints "gone-old" for the act that ran from the script $AX
 mk v;hu "" $AX>/dev/null 2>&1;RB1=$(lastrb);sh $RB1/rollback.sh>/dev/null 2>&1;[ ! -e $X/$HD ]&&echo -n gone-||echo -n kept-
 mk v;hu "" $AX>/dev/null 2>&1;printf '%s\n' $P2>$X/$HD;sleep 1;hu "" $AX>/dev/null 2>&1;sh $(lastrb)/rollback.sh>/dev/null 2>&1;[ "$(cat $X/$HD 2>/dev/null)" = $P2 ]&&echo old||echo lost;}
ok k7-a-first-act-then-rollback-leaves-no-marker-and-a-second-pins-marker-comes-back-byte-equal "[ \"\$(rbrow)\" = gone-old ]"
rep '/etc/agi/host.done ' '';ok k7-mutant-host-done-dropped-from-the-backup-list-is-RED "[ \"\$(rbrow $T/mut.sh)\" != gone-old ]"
# R-b: AGI_HOST_UNITS=<stub dir> with ROOT set needs systemctl AND systemd-analyze INSIDE that dir; stubs elsewhere on PATH (or the real systemctl) are refused before any call, no backup
EMP=$T/emptyd;mkdir -p $EMP
rbb(){ mk w;: >$T/sc.log;run env PATH=$SHD:$PATH AGI_HOST_UNITS=$EMP STUB_LOG=$T/sc.log STUB_FAIL= sh ${1:-$AGI} host>$T/w.out 2>$T/w.err;RC=$?;}
rbb;ok k8-stubs-elsewhere-on-PATH-are-refused-with-nothing-called-and-no-backup "[ $RC != 0 ]&&grep -q 'AGI_HOST_UNITS needs stubs' $T/w.err&&[ ! -s $T/sc.log ]&&[ ! -e $X/var/backups ]&&[ ! -e $X/etc/agi/carry.env ]"
mk w;run env PATH=/usr/bin:/bin AGI_HOST_UNITS=$EMP sh $AGI host>$T/w2.out 2>$T/w2.err;rw2=$?
ok k8-the-real-systemctl-is-refused-too "[ $rw2 != 0 ]&&grep -q 'AGI_HOST_UNITS needs stubs' $T/w2.err&&[ ! -e $X/var/backups ]"
rep '[ -z "$R" ]||[ -z "$AGI_HOST_UNITS" ]||for c in systemctl systemd-analyze;do' '[ -z "$R" ]||[ -z "$AGI_HOST_UNITS" ]||for c in ;do'
rbb $T/mut.sh;ok k8-mutant-the-resolve-check-dropped-reaches-the-stub-RED "grep -qx 'daemon-reload' $T/sc.log"
# R-c: hostmet is met only while agi-boot.service (and the timer iff the cell) still reads exactly `enabled` with rc 0; fail closed. Live, or a rehearsal ONLY through the stub dir.
rcrow(){ mk x;: >$T/sc.log;hu "">/dev/null 2>&1;sleep 1;run env PATH=$SHD:$PATH AGI_HOST_UNITS=$SHD AGI_TOWN_STATE=$T/ts STUB_LOG=$T/sc.log "$@" sh ${AGIX:-$AGI} host>$T/x.out 2>&1;}
for v in masked static linked "" disabled;do rcrow STUB_IS=$v;ok "k9-agi-boot-reading-'$v'-is-NOT-met" "! grep -qx 'host: met' $T/x.out&&[ \$(backups) = 2 ]";done
rcrow STUB_IS=enabled STUB_IS_RC=1;ok k9-an-enabled-text-with-rc-1-is-NOT-met "! grep -qx 'host: met' $T/x.out"
rcrow;ok k9-enabled-rc-0-is-met "grep -qx 'host: met' $T/x.out&&[ \$(backups) = 1 ]"
CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":true}}}}';mk x;CFG=;hu "">/dev/null 2>&1;sleep 1;run env PATH=$SHD:$PATH AGI_HOST_UNITS=$SHD AGI_TOWN_STATE=$T/ts STUB_LOG=$T/sc.log STUB_IS_T=masked sh $AGI host>$T/x2.out 2>&1
ok k9-the-timer-masked-with-the-cell-true-is-NOT-met "! grep -qx 'host: met' $T/x2.out"
mk x;: >$T/sc.log;hu "">/dev/null 2>&1;sleep 1;run env PATH=$SHD:$PATH AGI_HOST_UNITS=$SHD AGI_TOWN_STATE=$T/ts STUB_LOG=$T/sc.log STUB_IS_T=masked sh $AGI host>$T/x3.out 2>&1
ok k9-the-timer-masked-with-the-cell-false-is-still-met "grep -qx 'host: met' $T/x3.out"
mk y;: >$T/sc.log;run env PATH=$SHD:$PATH STUB_LOG=$T/sc.log STUB_IS=masked sh $AGI host>/dev/null 2>&1;sleep 1;run env PATH=$SHD:$PATH STUB_LOG=$T/sc.log STUB_IS=masked sh $AGI host>$T/y.out 2>&1
ok k9-a-plain-rehearsal-second-run-is-still-met-and-the-stub-log-is-empty "grep -qx 'host: met' $T/y.out&&[ ! -s $T/sc.log ]"
# a STOPPED town has agi-boot disabled by its own stop: exactly `disabled` is met there, and only there
printf 'stopped encryption-town 2026-10-21T00:00:00Z\n'>$T/ts;rcrow STUB_IS=disabled STUB_IS_RC=1;ok k9-stopped-town-with-agi-boot-disabled-is-met "grep -qx 'host: met' $T/x.out"
rcrow STUB_IS=enabled;ok k9-stopped-town-with-agi-boot-enabled-is-NOT-met "! grep -qx 'host: met' $T/x.out"
rcrow STUB_IS=masked;ok k9-stopped-town-with-agi-boot-masked-is-NOT-met "! grep -qx 'host: met' $T/x.out";rm -f $T/ts
rep '&&unitsmet&&aclmet' '&&aclmet';AGIX=$T/mut.sh;rcrow STUB_IS=masked;AGIX=
ok k9-mutant-hostmet-without-the-enabled-check-says-met-on-masked-RED "grep -qx 'host: met' $T/x.out"
# (2) council 10-21: the fresh-box tail ENABLES agi-boot and never STARTS it; the mutant puts the start back
rep 'systemctl enable agi-boot.service||die "enable failed' 'systemctl enable agi-boot.service&&systemctl start agi-boot.service||die "enable failed';mk s;: >$T/sc.log;hu "" $T/mut.sh>/dev/null 2>&1
ok k11-mutant-the-act-tail-that-starts-agi-boot-is-RED "grep -qx 'start agi-boot.service' $T/sc.log"
# ---- council 08:37Z 10-21 R-c ON A STOPPED TOWN: a STATEFUL stub systemctl (enable / disable state in a file, is-enabled answered from it). act (CF true) -> stop's posts + units arms -> drift sect -> `agi.sh host` -> `agi.sh host`:
# the 2nd prints `host: met`, backups = 2, the stub log has no `enable agi-boot.service` / `start agi-boot.service` / `enable --now agi-carry-fetch.timer` AFTER the stop, and `agi.sh host check` is rc 0.
SHS=$T/shs;mkdir -p $SHS;printf '#!/bin/sh\nexit 0\n' >$SHS/systemd-analyze
cat >$SHS/systemctl <<'EOF'
#!/bin/sh
echo "$*">>$STUB_LOG;E=$STUB_EN;touch $E
case $1 in
start)[ "$2" = agi-project.service ]&&{ sh "$(dirname "$0")/proj"||exit 1;};;
is-enabled)grep -qx "$2" $E&&{ echo enabled;exit 0;};echo ${STUB_WORD:-disabled};exit 1;;
enable)shift;[ "$1" = --now ]&&shift;case ",$STUB_NOOP," in *,$1,*)exit 0;;esac;echo "$1">>$E;;
disable)grep -vxF "$2" $E>$E.n;mv $E.n $E;;
esac
exit 0
EOF
printf '%s\n' "$PROJ" >$SHS/proj;chmod +x $SHS/*
sx(){ run env PATH=$SHS:$PATH AGI_HOST_UNITS=$SHS AGI_TOWN_STATE=$T/ts2 STUB_LOG=$T/sl.log STUB_EN=$T/en STUB_WORD=${WORD:-disabled} sh ${1:-$AGI} host $2;}
# the stop's own arms, as agi.sh stop does them: posts arm = `systemctl disable agi-boot.service`; units arm = disable the recorded `enabled` unit; town.state written FIRST (the stopped line LAST)
stopsim(){ printf 'boot enabled\nunit agi-carry-fetch.timer enabled\nstopped encryption-town 2026-10-21T00:00:00Z\n'>$T/ts2;$SHS/systemctl disable agi-boot.service;$SHS/systemctl disable agi-carry-fetch.timer;}
stopped_run(){ CFG='{"values":{"local_maxxing":{"agi_town":{"carry_fetch":true}}}}';mk f;CFG=;rm -f $T/en $T/ts2;: >$T/sl.log;sx $1>/dev/null 2>&1;export STUB_LOG=$T/sl.log STUB_EN=$T/en;stopsim;n0=$(wc -l <$T/sl.log);echo drift>>$X/opt/agi/bin/sect;sleep 1;sx $1>$T/f1.out 2>&1;sleep 1;sx $1>$T/f2.out 2>&1;sx "$1" check>$T/f3.out 2>&1;RC3=$?;}
stopped_run;ok r2-stopped-town-act-then-re-act-is-met-with-no-enable-after-the-stop "[ $RC3 = 0 ]&&grep -qx 'host: met' $T/f2.out&&[ \$(backups) = 2 ]&&! sed -n \"$((n0+1)),\\\$p\" $T/sl.log|grep -qE '^(enable agi-boot.service|start agi-boot.service|enable --now agi-carry-fetch.timer|enable agi-carry-fetch.timer)'&&grep -q \"stopped town: start's steps re-enable\" $T/f1.out&&sed -n \"$((n0+1)),\\\$p\" $T/sl.log|grep -qx daemon-reload"
# MUTANTS (each RED): the act enables agi-boot on a stopped town; unitsmet wants the timer enabled while stopped; masked accepted while stopped; a drifted piece is left unrepaired
rep 'if stp;then systemctl daemon-reload' 'if false;then systemctl daemon-reload';stopped_run $T/mut.sh;ok r2-mutant-the-act-enables-agi-boot-on-a-stopped-town-is-RED "sed -n \"$((n0+1)),\\\$p\" $T/sl.log|grep -qE '^(enable agi-boot.service|start agi-boot.service)'"
rep 'then tw=disabled;fi;' 'then tw=enabled;fi;';stopped_run $T/mut.sh;ok r2-mutant-unitsmet-wants-the-timer-enabled-while-stopped-is-RED "! grep -qx 'host: met' $T/f2.out"
rep '[ "$o" = disabled ]||return 1;fi' '[ -n "$o" ]||return 1;fi';mk f;rm -f $T/en;printf 'stopped x y\n'>$T/ts2;: >$T/sl.log;sx >/dev/null 2>&1;WORD=masked sx $T/mut.sh>/dev/null 2>&1;WORD=masked sx $T/mut.sh>$T/f4.out 2>&1
ok r2-mutant-masked-accepted-while-stopped-is-RED "grep -qx 'host: met' $T/f4.out"
mk f;rm -f $T/en;printf 'stopped x y\n'>$T/ts2;: >$T/sl.log;sx >/dev/null 2>&1;sleep 1;WORD=masked sx >$T/f5.out 2>&1
ok r2-stub-masked-on-a-stopped-town-is-NOT-met "! grep -qx 'host: met' $T/f5.out"
rm -f $T/ts2
# ---- council 17:58Z 10-21 (3): `host: met` was a FALSE GREEN while /run held an older pin's projection (agi-project.path never ran on the box). The act's tail now STARTS agi-project.service after the carry.env write,
# and hostmet reads the live projection (agi-users.conf bytes + the agi-post@* wants links) against the pin's OWN, built by the pinned piece. The stubs' `proj` runs the real piece; STUB_NOPROJ=1 = a start that returns 0 and projects nothing.
NOPROJ=;NEEDUNIT=
pj_commit(){ git -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qam "$1";git -C $M rev-parse HEAD;}
pj_row(){ sed -i '/"name":"lp"/a\  - {"name":"zp","box":"encryption-town","boot":true,"engine":{"v":4,"name":"zp","harness":"claude-code","model":"m","effort":"low"}}' $M/.agi/nodes/.geometry/posts.md;}
mk p;: >$T/sc.log;hu "">$T/p1.out 2>&1;rp1=$?
ok p1-the-act-starts-agi-project-after-the-carry-env-write-and-the-run-projection-is-the-pins "[ $rp1 = 0 ]&&grep -qx 'start agi-project.service pin=$PIN' $T/sc.log&&grep -q 'agi-xp' $X/run/systemd/system/agi-users.conf&&! grep -q 'agi-lp' $X/run/systemd/system/agi-users.conf&&[ \"\$(grep -B1 -x 'start agi-project.service pin=$PIN' $T/sc.log|head -1)\" = 'daemon-reload' ]"
# the false green: the pin moves to B and the start returns 0 WITHOUT projecting; host.done = B, carry.env = B, /run is still A's
PA=$PIN;pj_row;PB=$(pj_commit zp);PIN=$PB;sleep 1;NOPROJ=1;hu "">$T/p2a.out 2>&1;NOPROJ=;sleep 1;hu "">$T/p2b.out 2>&1;rp2b=$?;sleep 1;hu "">$T/p2c.out 2>&1
ok p2-carry-env-at-the-pin-but-run-from-an-older-pin-is-NOT-met-and-the-re-act-projects "! grep -qx 'host: met' $T/p2b.out&&[ $rp2b = 0 ]&&[ \$(backups) = 3 ]&&grep -q 'agi-zp' $X/run/systemd/system/agi-users.conf&&[ -L $X/run/systemd/system/multi-user.target.wants/agi-post@zp.service ]&&grep -qx 'host: met' $T/p2c.out"
# MUTANT: hostmet without the projection read says met at the older pin's projection
rep '&&aclmet&&projmet;}' '&&aclmet;}';mk p;hu "">/dev/null 2>&1;pj_row;PIN=$(pj_commit zp);sleep 1;NOPROJ=1;hu "" $T/mut.sh>/dev/null 2>&1;NOPROJ=;sleep 1;hu "" $T/mut.sh>$T/p3.out 2>&1
ok p3-mutant-hostmet-without-the-projection-read-says-met-at-an-older-pins-run-is-RED "grep -qx 'host: met' $T/p3.out&&! grep -q 'agi-zp' $X/run/systemd/system/agi-users.conf"
# drift in the live projection: an extra user line, then a stale wants link
mk q;hu "">/dev/null 2>&1;printf 'u agi-ghost - - -\n'>>$X/run/systemd/system/agi-users.conf;sleep 1;hu "">$T/p4a.out 2>&1;sleep 1;hu "">$T/p4b.out 2>&1
ok p4-an-extra-user-line-in-the-live-agi-users-conf-is-NOT-met-and-is-re-projected "! grep -qx 'host: met' $T/p4a.out&&! grep -q ghost $X/run/systemd/system/agi-users.conf&&grep -qx 'host: met' $T/p4b.out"
mk q;hu "">/dev/null 2>&1;mkdir -p $X/run/systemd/system/multi-user.target.wants;ln -s ../agi-post@.service $X/run/systemd/system/multi-user.target.wants/agi-post@ghost.service;sleep 1;hu "">$T/p4c.out 2>&1
ok p4-a-stale-agi-post-wants-link-in-run-is-NOT-met-and-is-removed "! grep -qx 'host: met' $T/p4c.out&&[ ! -e $X/run/systemd/system/multi-user.target.wants/agi-post@ghost.service ]"
# MUTANT: a tail that never starts the projection (the else arm). On a box that HAS the unit (so the fresh-box fallback stays out) the pin moves, /run stays the old pin's, and the next run is not met
rep '{ systemctl start agi-project.service||die "$PJ";}&&tm' 'tm';mk r;hu "">/dev/null 2>&1;pj_row;PIN=$(pj_commit zp);sleep 1;: >$T/sc.log;hu "" $T/mut.sh>$T/p5a.out 2>&1;n5=$(grep -c 'start agi-project.service' $T/sc.log);z5=$(grep -c 'agi-zp' $X/run/systemd/system/agi-users.conf);sleep 1;hu "">$T/p5.out 2>&1
ok p5-mutant-a-tail-that-never-starts-agi-project-is-RED "[ $n5 = 0 ]&&[ $z5 = 0 ]&&! grep -qx 'host: met' $T/p5.out"
# a failing start dies by name with the rollback line and leaves no host.done
mk s;: >$T/sc.log;hu start>$T/p6.out 2>$T/p6.err;rp6=$?
ok p6-a-failing-projection-start-dies-naming-it-with-the-rollback-line-and-no-marker "[ $rp6 != 0 ]&&grep -q 'agi-project.service did not run at $PIN' $T/p6.err&&grep -q 'rollback.sh' $T/p6.err&&[ ! -e $X/$HD ]"
# ---- council 19:46Z 10-21 FRESH-BOX DEADLOCK: a box whose agi-boot never ran has no agi-project.service in /run, so the explicit start dies, a re-run dies the same way and a reboot does not help (agi-boot is installed by this act but not enabled).
# STUB_NEEDUNIT=1 makes the stub start answer like systemd for a missing unit. The tail runs the SAME pinned piece into /run when the unit is absent (one code, two callers).
mk w;: >$T/sc.log;NEEDUNIT=1;hu "">$T/f1.out 2>$T/f1.err;rf1=$?;sleep 1;hu "">$T/f1b.out 2>&1;NEEDUNIT=
ok f1-a-fresh-box-act-completes-writes-the-unit-and-the-second-run-is-met "[ $rf1 = 0 ]&&[ -e $X/run/systemd/system/agi-project.service ]&&grep -q 'agi-xp' $X/run/systemd/system/agi-users.conf&&[ -s $X/$HD ]&&grep -qx 'host: met' $T/f1b.out&&[ \$(backups) = 1 ]"
rep 'fresh(){ [ -e $R/run/systemd/system/agi-project.service ]&&return 0;' 'fresh(){ return 0;';mk w;: >$T/sc.log;NEEDUNIT=1;hu "" $T/mut.sh>$T/f2.out 2>$T/f2.err;rf2=$?;NEEDUNIT=
ok f2-mutant-the-tail-without-the-fresh-box-fallback-dies-at-the-start-RED "[ $rf2 != 0 ]&&grep -q 'agi-project.service did not run at $PIN' $T/f2.err&&[ ! -e $X/$HD ]"
mk w;sed -i '/^### agi-project /,/^### /s|^#!/bin/sh$|#!/bin/sh\nexit 4|' $M/.agi/nodes/.geometry/engine.md;PIN=$(pj_commit brokenpiece);: >$T/sc.log;NEEDUNIT=1;hu "">$T/f3.out 2>$T/f3.err;rf3=$?;NEEDUNIT=
ok f3-a-pinned-piece-that-itself-fails-dies-by-name-with-the-rollback-line-and-no-marker "[ $rf3 != 0 ]&&grep -q 'the pinned agi-project piece failed at $PIN' $T/f3.err&&grep -q 'rollback.sh' $T/f3.err&&[ ! -e $X/$HD ]&&! grep -q 'start agi-project' $T/sc.log"
echo "host-act-encryption-town: $f FAIL";exit $f
