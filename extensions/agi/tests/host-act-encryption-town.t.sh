#!/bin/sh
# host-act-encryption-town.t.sh: the REHEARSAL of extensions/agi/guard/host-act-encryption-town.sh (ROOT=<scratch>, no systemd, no root): step 0 + the act + the rollback + the per-post move, on a scratch MAIN holding the REAL geometry. One ok/FAIL line per case; exit = FAIL count. ACT=<script copy> runs a mutant.
umask 022;T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=$(cd "$(dirname "$0")/../../.." && pwd);ACT=${ACT:-$R0/extensions/agi/guard/host-act-encryption-town.sh};GEO=$R0/.agi/nodes/.geometry
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_AUTHOR_NAME GIT_COMMITTER_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_EMAIL;export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
sect(){ cat $GEO/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
mk(){ X=$T/$1;rm -rf $X;mkdir -p $X/data/work/agi/.agi/nodes/.geometry $X/opt/agi/bin $X/etc/systemd/system $X/etc/polkit-1/rules.d $X/usr/local $X/mnt $X/var/lib;M=$X/data/work/agi;cp $GEO/engine*.md $M/.agi/nodes/.geometry/
 { printf '%s\n' '---' 'posts:';printf '  - {"name":"xp","box":"encryption-town","engine":{"v":4,"name":"xp","harness":"pi","model":"m","effort":"low"}}\n  - {"name":"lp","box":"local-town","engine":{"v":4,"name":"lp","harness":"pi","model":"m","effort":"low"}}\n';printf '%s\n' '---';} >$M/.agi/nodes/.geometry/posts.md
 [ -n "$NOCOMMS" ]||{ mkdir -p $M/.agi/comms/season-2/dm;echo x>$M/.agi/comms/season-2/dm/a--b.md;}
 git init -q $M;git -C $M add -A;git -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm fx;PIN=$(git -C $M rev-parse HEAD);printf '#!/bin/sh\n' >$X/opt/agi/bin/pi;chmod +x $X/opt/agi/bin/pi;}
run(){ ( cd $T;env -i PATH=$PATH HOME=$T ROOT=$X PIN=${PIN} AGI_REPO=/data/work/agi "$@" );}
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
echo "host-act-encryption-town: $f FAIL";exit $f
