#!/bin/sh
# agi-cred.t.sh: goal:g7.16.1.11.46.6 (C1) falsifier 1: the root timer agi-cred on STUBS, run as a plain user: a stub doppler on PATH, a temp credstore, a stub systemctl, a fixture /proc + cgroup tree, a scratch git repo
# for the cells. No root, no network, no Doppler, no real key (the "key" is a canary assembled here). One ok/FAIL line per case; exit = number of FAILs. PIECE=<file> tests an edited copy; a MUTANT is ONE edit of the piece (rep)
# and its row passes only when the matching clean row is RED on it. The root leg (agi-cred check on the live posts; a post started with a key in its env makes it exit non-zero) is belam's at install.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};G=/usr/bin/git
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-cred>$T/piece;PIECE=$T/piece;}
[ -s $PIECE ]||{ echo "FAIL extract: agi-cred $(wc -c<$PIECE) B";exit 99;}
P0=$PIECE;ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
KP=sk-an;KP=${KP}t;K="${KP}-api03-TESTCANARY0123";K2="${KP}-api03-OTHERCANARY456"
rep(){ A=$1 B=$2 awk '{o="";r=$0;while((i=index(r,ENVIRON["A"]))>0){o=o substr(r,1,i-1) ENVIRON["B"];r=substr(r,i+length(ENVIRON["A"]))}print o r}' $P0>$T/mut;cmp -s $P0 $T/mut&&echo "# NO EDIT for [$1]";PIECE=$T/mut;}
# --- the scratch main repo with the cells
M=$T/main;mkdir -p $M/.agi/nodes/.geometry;$G -C $M init -q;cp $R0/.agi/nodes/.geometry/secrets.md $M/.agi/nodes/.geometry/secrets.md
cells(){ sed -e "s/^credits_live: .*/credits_live: $1/" -e "s/^doppler: .*/doppler: {\"project\": \"agi\", \"config\": \"$2\"}/" $R0/.agi/nodes/.geometry/secrets.md>$M/.agi/nodes/.geometry/secrets.md;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm c$$ >/dev/null 2>&1;TR=$($G -C $M rev-parse HEAD);}
# --- stubs
SH=$T/sh;mkdir -p $SH $T/units $T/cs $T/proc $T/cg
cat >$SH/doppler<<'EOF'
#!/bin/sh
echo "$*">>$STUB_LOG/dop.log;echo "token-len ${#DOPPLER_TOKEN}">>$STUB_LOG/dop.log
[ -z "$STUB_DOP_FAIL" ]||exit 1
echo "$STUB_KEY"
EOF
cat >$SH/systemctl<<'EOF'
#!/bin/sh
case $1 in cat)cat $STUB_LOG/units/$2 2>/dev/null;;try-restart)echo "$2">>$STUB_LOG/sd.log;;list-units)cat $STUB_LOG/active 2>/dev/null;;show)echo /system.slice/$5;;esac
EOF
cat >$SH/tr<<'EOF'
#!/bin/sh
# the race, deterministically: when stdin is the environ of $STUB_TR_RM the pid exits DURING the read (its proc dir is removed, nothing comes out)
[ -z "$STUB_TR_RM" ]||[ "$(readlink /proc/self/fd/0)" != "$STUB_TR_RM/environ" ]||{ rm -rf "$STUB_TR_RM";exec cat >/dev/null;}
exec /usr/bin/tr "$@"
EOF
chmod +x $SH/*;printf '[Service]\nLoadCredential=claude-sp:/etc/credstore/claude-sp\n'>$T/units/agi-batch.service;cp $T/units/agi-batch.service $T/units/agi-kids.service;printf '[Service]\nExecStart=/bin/true\n'>$T/units/agi-council.service
run(){ env -i PATH=$SH:/usr/bin:/bin AGI_REPO=$M AGI_TRUNK=${TRUNK:-$TR} AGI_CREDSTORE=$T/cs AGI_PROC=$T/proc AGI_CGROUP=$T/cg STUB_LOG=$T STUB_KEY="${KEY:-$K}" STUB_DOP_FAIL=$DFAIL STUB_TR_RM=$TRRM GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' sh ${PIECE} "$@" >$T/o 2>$T/e;rc=$?;}
fresh(){ rm -rf $T/cs/* $T/cs/.[a-z]* $T/sd.log $T/dop.log $T/active $T/proc $T/cg;mkdir -p $T/proc $T/cg;: >$T/sd.log;printf 'TOKVALUE9' >$T/cs/doppler-token;TRUNK=;DFAIL=;KEY=;TRRM=;}
nsd(){ grep -c "^$1.service\$" $T/sd.log;}
# ================= TICK
cells true prd;fresh;run tick
ok "t-a-live-true-writes-the-key-file-0600 rc $rc, mode $(stat -c %a $T/cs/claude-sp 2>/dev/null), same bytes as the doppler value: $(printf %s "$K"|cmp -s - $T/cs/claude-sp&&echo yes||echo NO)" '[ $rc = 0 ]&&[ "$(stat -c %a $T/cs/claude-sp)" = 600 ]&&printf %s "$K"|cmp -s - $T/cs/claude-sp'
ok "t-a-doppler-is-asked-for-the-key-by-name-and-the-token-is-env-not-argv log: $(sed -n 1p $T/dop.log|cut -c1-110); $(sed -n 2p $T/dop.log) (the token is 3 bytes)" 'grep -qx "secrets get CLAUDE_CONSOLE_SP_KEY --plain --project agi --config prd" $T/dop.log&&grep -qx "token-len 9" $T/dop.log&&! grep -q "TOKVALUE9" $T/dop.log'
ok "t-a-the-output-never-carries-the-key canary hits in stdout+stderr: $(cat $T/o $T/e|grep -c TESTCANARY) (want 0)" '[ "$(cat $T/o $T/e|grep -c TESTCANARY)" = 0 ]'
ok "t-a-no-temp-file-is-left $(ls -A $T/cs|tr '\n' ' ')" '[ "$(ls -A $T/cs|tr "\n" " ")" = "claude-sp doppler-token " ]'
ok "t-b-only-the-units-with-LoadCredential-restart batch $(nsd agi-batch) kids $(nsd agi-kids) council $(nsd agi-council) (want 1 1 0)" '[ "$(nsd agi-batch)" = 1 ]&&[ "$(nsd agi-kids)" = 1 ]&&[ "$(nsd agi-council)" = 0 ]'
: >$T/sd.log;run tick
ok "t-c-the-same-key-again-restarts-nothing rc $rc, restarts $(wc -l <$T/sd.log|tr -d ' ') (want 0)" '[ $rc = 0 ]&&[ ! -s $T/sd.log ]'
: >$T/sd.log;KEY=$K2;run tick
ok "t-d-a-new-key-replaces-the-file-and-restarts rc $rc, new bytes: $(printf %s "$K2"|cmp -s - $T/cs/claude-sp&&echo yes||echo NO), batch restarts $(nsd agi-batch)" '[ $rc = 0 ]&&printf %s "$K2"|cmp -s - $T/cs/claude-sp&&[ "$(nsd agi-batch)" = 1 ]'
# --- the kill cell
cells false prd;: >$T/sd.log;run tick
ok "t-e-credits-live-false-removes-the-file-and-restarts rc $rc, file $([ -e $T/cs/claude-sp ]&&echo STILL THERE||echo gone), batch restarts $(nsd agi-batch), say: $(cut -c1-60 $T/o)" '[ $rc = 0 ]&&[ ! -e $T/cs/claude-sp ]&&[ "$(nsd agi-batch)" = 1 ]&&grep -q "credits_live is not true" $T/o'
: >$T/sd.log;run tick
ok "t-f-and-again-is-a-no-op rc $rc, restarts $(wc -l <$T/sd.log|tr -d ' ') (want 0)" '[ $rc = 0 ]&&[ ! -s $T/sd.log ]'
# --- fail closed and fail safe
cells true prd;run tick;TRUNK=deadbeef;run tick
ok "t-g-an-unreadable-cell-removes-the-file-fail-closed rc $rc, file $([ -e $T/cs/claude-sp ]&&echo STILL THERE||echo gone)" '[ ! -e $T/cs/claude-sp ]'
fresh;cells true prd;run tick;DFAIL=1;KEY=$K2;run tick
ok "t-h-doppler-failing-keeps-the-last-file-and-says-so rc $rc (want 5), file still the old key: $(printf %s "$K"|cmp -s - $T/cs/claude-sp&&echo yes||echo NO), say: $(cut -c1-50 $T/e)" '[ $rc = 5 ]&&printf %s "$K"|cmp -s - $T/cs/claude-sp&&grep -q "nothing written" $T/e'
fresh;cells true "";run tick
ok "t-i-an-empty-doppler-config-cell-writes-nothing rc $rc (want 4), file $([ -e $T/cs/claude-sp ]&&echo THERE||echo none)" '[ $rc = 4 ]&&[ ! -e $T/cs/claude-sp ]'
fresh;cells true prd;rm -f $T/cs/doppler-token;run tick
ok "t-j-no-doppler-token-writes-nothing rc $rc (want 4), file $([ -e $T/cs/claude-sp ]&&echo THERE||echo none)" '[ $rc = 4 ]&&[ ! -e $T/cs/claude-sp ]'
# ================= CHECK: 2 posts, 3 pids, fixture proc + cgroup
mkpost(){ mkdir -p $T/cg/system.slice/agi-post@$1.service;: >$T/cg/system.slice/agi-post@$1.service/cgroup.procs;echo "agi-post@$1.service loaded active running x" >>$T/active;}
addpid(){ echo $2 >>$T/cg/system.slice/agi-post@$1.service/cgroup.procs;mkdir -p $T/proc/$2;printf 'PATH=/bin\0AGI_POST=%s\0HOME=/x\0' $1 >$T/proc/$2/environ;}
world(){ fresh;mkpost a;mkpost b;addpid a 101;addpid a 102;addpid b 201;}
unread(){ rm -f $T/proc/$1/environ;ln -s /nonexistent/environ $T/proc/$1/environ;}   # the pid EXISTS (its proc dir is there) but its environ cannot be read
notread(){ rm -f $T/proc/$1/environ;mkdir -p $T/proc/$1/environ;}   # -r PASSES (a directory) and the read FAILS (EISDIR), the pid is present: the kernel's ptrace-mode EACCES under a hardened unit looks the same to the check (reviewer finding 10-24)
gone(){ rm -rf $T/proc/$1;}   # the pid was listed in cgroup.procs and exited before the read
world;run check
ok "k-a-clean-posts-pass rc $rc, $(cut -c1-70 $T/o)" '[ $rc = 0 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 3 gone 0 key-hits 0" $T/o'
world;printf 'PATH=/bin\0ANTHROPIC_API_KEY=%s\0' "$K">$T/proc/102/environ;run check
ok "k-b-a-key-in-a-post-environ-fails rc $rc, $(cut -c1-70 $T/o), canary in output: $(cat $T/o $T/e|grep -c TESTCANARY)" '[ $rc = 1 ]&&grep -q "key-hits 1$" $T/o&&[ "$(cat $T/o $T/e|grep -c TESTCANARY)" = 0 ]'
fresh;run check
ok "k-c-an-empty-selector-fails-it-proves-nothing rc $rc, say: $(cut -c1-60 $T/e)" '[ $rc = 1 ]&&grep -q "nothing is proven" $T/e'
world;unread 201;run check
ok "k-d-a-pid-that-exists-and-cannot-be-read-fails rc $rc, $(cut -c1-60 $T/o)" '[ $rc = 1 ]&&grep -q "pids 3 read 2 gone 0 " $T/o'
world;gone 201;run check
ok "k-d2-a-pid-gone-before-its-read-is-not-counted (belam red 10-24: short-lived git/sh of a busy post) rc $rc (want 0), $(cut -c1-70 $T/o)" '[ $rc = 0 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 2 gone 1 key-hits 0" $T/o'
world;: >$T/proc/102/environ;run check
ok "k-g-a-live-pid-with-an-empty-environ-is-READ-not-red (env -i children; council 01:2x) rc $rc, $(cut -c1-80 $T/o)" '[ $rc = 0 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 3 gone 0 key-hits 0" $T/o'
world;TRRM=$T/proc/102;run check
ok "k-h-readable-then-emptied-and-removed-during-the-read-is-GONE-not-read rc $rc, $(cut -c1-80 $T/o)" '[ $rc = 0 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 2 gone 1 key-hits 0" $T/o'
world;gone 101;gone 102;gone 201;run check
ok "k-i-a-cgroup-whose-pids-all-vanished-proves-nothing rc $rc, $(cut -c1-80 $T/o), say: $(cut -c1-50 $T/e)" '[ $rc = 1 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 0 gone 3 key-hits 0" $T/o&&grep -q "nothing is proven" $T/e'
world;notread 201;run check
ok "k-j-a-read-that-FAILS-on-a-present-pid-is-RED-not-a-silent-green rc $rc, $(cut -c1-80 $T/o)" '[ $rc = 1 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 2 gone 0 key-hits 0" $T/o'
fresh;mkpost a;addpid a 101;notread 101;run check
ok "k-j-a-check-that-can-open-NO-environ-proves-nothing rc $rc, $(cut -c1-80 $T/o)" '[ $rc = 1 ]&&grep -qx "\[cred\] check: posts 1 pids 1 read 0 gone 0 key-hits 0" $T/o&&grep -q "nothing is proven" $T/e'
world;notread 201;TRRM=$T/proc/201;run check
ok "k-j-a-failed-read-then-the-pid-leaves-is-gone-not-red (the shim removes the dir while the read fails: the unreadable-environ pid is not present any more) rc $rc, $(cut -c1-80 $T/o)" '[ $rc = 0 ]&&grep -qx "\[cred\] check: posts 2 pids 3 read 2 gone 1 key-hits 0" $T/o'
world;cells true prd;printf 'ANTHROPIC_API_KEY=%s\0' "$K">$T/proc/101/environ;run
ok "k-e-the-bare-run-ticks-then-checks-and-takes-the-worse-rc rc $rc (want 1: the tick wrote, the check found the key), file $([ -e $T/cs/claude-sp ]&&echo written||echo none)" '[ $rc = 1 ]&&[ -e $T/cs/claude-sp ]'
ok "k-f-an-unknown-argument-is-refused rc $(PIECE=$P0 run bogus;echo $rc) (want 2)" '[ "$(PIECE=$P0 run bogus;echo $rc)" = 2 ]'
# ================= MUTANTS (one edit each; the matching clean row above is RED on it)
fresh;run;PIECE=$P0
rep '[ $rd -gt 0 ]&&[ $((tot' '[ $((tot';fresh;run check
ok "m1-MUTANT-the-count-skipped-passes-an-empty-selector-RED rc $rc (clean: 1)" '[ $rc = 0 ]'
rep '&&[ $hit = 0 ];}' ';}';world;printf 'KEY=%s\0' "$K">$T/proc/102/environ;run check
ok "m2-MUTANT-the-hit-count-ignored-passes-a-key-RED rc $rc (clean: 1)" '[ $rc = 0 ]'
rep '&&[ $((tot-gn)) = $rd ]' '';world;unread 201;run check
ok "m3-MUTANT-an-unread-pid-ignored-passes-RED rc $rc (clean: 1)" '[ $rc = 0 ]'
rep '{ [ -d "$R/$q" ]||gn=$((gn+1));continue;}' '{ continue;}';world;gone 201;run check
ok "m8-MUTANT-a-vanished-pid-counted-as-unread-fails-a-working-town-RED rc $rc (clean: 0), $(cut -c1-70 $T/o)" '[ $rc = 1 ]&&grep -q "pids 3 read 2 gone 0 " $T/o'
rep '{ [ -d "$R/$q" ]||gn=$((gn+1));continue;}' '{ gn=$((gn+1));continue;}';world;unread 201;run check
ok "m9-MUTANT-every-unread-pid-called-gone-passes-an-existing-unreadable-one-RED rc $rc (clean: 1), $(cut -c1-70 $T/o)" '[ $rc = 0 ]'
rep '[ -n "$d" ]||[ -d "$R/$q" ]||{ gn=$((gn+1));continue;}' '[ -n "$d" ]||{ gn=$((gn+1));continue;}';world;: >$T/proc/102/environ;run check
ok "m10-MUTANT-an-empty-environ-treated-as-gone-RED $(cut -c1-70 $T/o) (clean: read 3 gone 0)" '! grep -q "read 3 gone 0 " $T/o'
rep '[ -n "$d" ]||[ -d "$R/$q" ]||{ gn=$((gn+1));continue;}' ':';world;TRRM=$T/proc/102;run check
ok "m11-MUTANT-no-gone-test-after-the-read-counts-a-pid-that-left-as-read-RED $(cut -c1-70 $T/o) (clean: read 2 gone 1)" '! grep -q "read 2 gone 1 " $T/o'
rep '||{ [ -d "$R/$q" ]||gn=$((gn+1));continue;};[ -n "$d" ]' ';[ -n "$d" ]';world;notread 201;run check
ok "m12-MUTANT-the-read-rc-ignored-counts-a-failed-read-as-read-RED rc $rc (clean: 1), $(cut -c1-70 $T/o)" '[ $rc = 0 ]'
rep "grep -q '^LoadCredential=claude-sp:'&&" '';fresh;cells true prd;run tick
ok "m4-MUTANT-no-LoadCredential-test-restarts-the-council-unit-RED council restarts $(nsd agi-council) (clean: 0)" '[ "$(nsd agi-council)" = 1 ]'
rep 'cmp -s $n $F' 'false';fresh;cells true prd;run tick;: >$T/sd.log;run tick
ok "m5-MUTANT-no-change-test-restarts-on-the-same-key-RED restarts $(wc -l <$T/sd.log|tr -d ' ') (clean: 0)" '[ -s $T/sd.log ]'
rep '[ -e $F ]&&rm -f $F&&kick' '[ -e $F ]&&kick';fresh;cells true prd;run tick;cells false prd;run tick
ok "m6-MUTANT-the-kill-without-the-rm-leaves-the-file-RED file $([ -e $T/cs/claude-sp ]&&echo THERE||echo gone) (clean: gone)" '[ -e $T/cs/claude-sp ]'
rep 'printf %s "$k">$n;' 'printf %s "$k">$n;chmod 644 $n;';fresh;cells true prd;run tick
ok "m7-MUTANT-a-world-readable-file-RED mode $(stat -c %a $T/cs/claude-sp) (clean: 600)" '[ "$(stat -c %a $T/cs/claude-sp)" != 600 ]'
PIECE=$P0
# ================= UNREAD (belam 10-25): the live unit's git read was refused (dubious ownership: carry.env has GIT_CONFIG_VALUE_0 but the
# unit had no COUNT/KEY_0), the cell read empty, and tick passed SILENTLY as "not live". Now an unreadable cell is a named unread, rc 3, fail closed.
printf x >$T/cs/claude-sp;TRUNK=refs/heads/no-such-ref run tick
ok "u1-an-unreadable-secrets-cell-is-unread-rc3-and-the-key-file-goes rc $rc (want 3), file $([ -e $T/cs/claude-sp ]&&echo present||echo gone)" '[ $rc = 3 ] && [ ! -e $T/cs/claude-sp ] && grep -q "\[cred\] unread" $T/e'
ok "u2-the-service-sets-safe.directory-for-root-reads (carry.env holds VALUE_0) $(sect agi-cred.service|grep -c "^Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory$")" '[ "$(sect agi-cred.service|grep -c "^Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory$")" = 1 ]'
rep '[ -n "$s" ]||{' 'true||{';printf x >$T/cs/claude-sp;TRUNK=refs/heads/no-such-ref run tick;PIECE=$P0
ok "u1m-mutant-guard-dropped-reads-silent-rc0-RED rc $rc" '[ $rc = 0 ] && ! grep -q "\[cred\] unread" $T/e'
rm -f $T/cs/claude-sp
# ================= NEGATIVE (leaf falsifier 3): the pieces and units name no key and no ANTHROPIC_API_KEY environment
n=$(for g in agi-cred agi-cred.service agi-cred.timer;do sect $g;done|grep -c -e "Environment=.*ANTHROPIC_API_KEY" -e "$KP-")
ok "n-the-three-pieces-hold-no-key-prefix-and-no-ANTHROPIC_API_KEY-environment hits $n (want 0)" '[ "$n" = 0 ]'
ok "n-the-service-carries-no-LoadCredential-or-key-env (it is root's own) $(sect agi-cred.service|grep -c -e LoadCredential -e ANTHROPIC)" '[ "$(sect agi-cred.service|grep -c -e LoadCredential -e ANTHROPIC)" = 0 ]'
echo "agi-cred: $f FAIL";exit $f
