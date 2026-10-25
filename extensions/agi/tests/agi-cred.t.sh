#!/bin/sh
# agi-cred.t.sh: goal:g7.16.1.11.46.6 (C1) falsifier 1: the root timer agi-cred on STUBS, run as a plain user: a stub doppler on PATH, a temp credstore, a stub systemctl, a fixture /proc + cgroup tree, a scratch git repo
# for the cells. No root, no network, no Doppler, no real key (the "key" is a canary assembled here). One ok/FAIL line per case; exit = number of FAILs. PIECE=<file> tests an edited copy; a MUTANT is ONE edit of the piece (rep)
# and its row passes only when the matching clean row is RED on it. The root leg (agi-cred check on the live posts; a post started with a key in its env makes it exit non-zero) is belam's at install.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};G=/usr/bin/git
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-cred>$T/piece;PIECE=$T/piece;}
[ -s $PIECE ]||{ echo "FAIL extract: agi-cred $(wc -c<$PIECE) B";exit 99;}
[ -n "$UNIT" ]||{ sect agi-cred.service>$T/unit;UNIT=$T/unit;}   # run() takes HOME from the unit's own Environment= line: the stub doppler refuses an empty HOME as the real one does
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
[ -n "$HOME" ]||{ printf '%s\n' 'Unable to determine home directory' 'Doppler Error: $HOME is not defined' >&2;exit 1;}   # doppler v3.76.5, both lines (belam 10-25: the live unit had no HOME, rc 5)
[ -z "$STUB_DOP_ERR" ]||{ echo "Doppler Error: token $DOPPLER_TOKEN rejected; last value $STUB_KEY" >&2;exit 1;}   # an error that echoes the token and a key (council L127 Row 1')
[ -z "$STUB_DOP_FAIL" ]||exit 1
echo "$STUB_KEY"
EOF
cat >$SH/systemctl<<'EOF'
#!/bin/sh
case $1 in cat)cat $STUB_LOG/units/$2 2>/dev/null;;try-restart)echo "$2">>$STUB_LOG/sd.log;[ "$2" != "$STUB_SD_FAIL" ];;list-units)cat $STUB_LOG/active 2>/dev/null;;show)echo /system.slice/$5;;esac
EOF
# the stub git: records the safe.directory set THIS call sees (its env + its -c pairs; run from / so no repo config is listed) and the GIT_* names in
# its env, then runs the real git. The log path is BAKED IN: the piece's read runs under env -i (council L127 S1, 20:52Z), so no STUB_LOG reaches it
printf '%s\n' '#!/bin/sh' 'a=;while [ "$1" = -c ];do a="$a -c $2";shift 2;done' "(cd / && /usr/bin/git \$a config --get-all safe.directory) >$T/sdcfg 2>/dev/null" "env|sed -n 's/^\\(GIT_[A-Z_]*\\)=.*/\\1/p'|sort|tr '\\n' ' ' >$T/gitenv" 'exec /usr/bin/git $a "$@"' >$SH/git
cat >$SH/tr<<'EOF'
#!/bin/sh
# the race, deterministically: when stdin is the environ of $STUB_TR_RM the pid exits DURING the read (its proc dir is removed, nothing comes out)
[ -z "$STUB_TR_RM" ]||[ "$(readlink /proc/self/fd/0)" != "$STUB_TR_RM/environ" ]||{ rm -rf "$STUB_TR_RM";exec cat >/dev/null;}
exec /usr/bin/tr "$@"
EOF
printf '[safe]\n\tdirectory = *\n' >$T/hostile.gc   # a hostile system AND global value; run() also exports a hostile env pair (VALUE_0='*')
DC=$T/decoy;mkdir -p $DC/.agi/nodes/.geometry;$G -C $DC init -q;sed 's/^credits_live: .*/credits_live: false/' $R0/.agi/nodes/.geometry/secrets.md>$DC/.agi/nodes/.geometry/secrets.md;$G -C $DC add -A;$G -C $DC -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm decoy
# EVERY run() is hostile (council 20:52Z): GIT_CONFIG_PARAMETERS '*', the env pair '*', GIT_DIR + GIT_OBJECT_DIRECTORY at a decoy whose cell reads credits_live: false, GIT_NAMESPACE, hostile system + global files
chmod +x $SH/*;printf '[Service]\nLoadCredential=claude-sp:/etc/credstore/claude-sp\n'>$T/units/agi-batch.service;cp $T/units/agi-batch.service $T/units/agi-kids.service;printf '[Service]\nExecStart=/bin/true\n'>$T/units/agi-council.service
run(){ env -i PATH=$SH:/usr/bin:/bin HOME=$(sed -n 's/^Environment=HOME=//p' $UNIT|tail -1) AGI_REPO=$M AGI_TRUNK=${TRUNK:-$TR} AGI_CREDSTORE=$T/cs AGI_PROC=$T/proc AGI_CGROUP=$T/cg STUB_LOG=$T STUB_KEY="${KEY:-$K}" STUB_DOP_FAIL=$DFAIL STUB_DOP_ERR=$DERR STUB_SD_FAIL=$SDF STUB_TR_RM=$TRRM GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' GIT_CONFIG_GLOBAL=$T/hostile.gc GIT_CONFIG_SYSTEM=$T/hostile.gc GIT_CONFIG_PARAMETERS="'safe.directory'='*'" GIT_DIR=$DC/.git GIT_OBJECT_DIRECTORY=$DC/.git/objects GIT_NAMESPACE=x sh ${PIECE} "$@" >$T/o 2>$T/e;rc=$?;}
fresh(){ rm -rf $T/cs/* $T/cs/.[a-z]* $T/sd.log $T/dop.log $T/active $T/proc $T/cg;mkdir -p $T/proc $T/cg;: >$T/sd.log;printf 'TOKVALUE9' >$T/cs/doppler-token;TRUNK=;DFAIL=;DERR=;SDF=;KEY=;TRRM=;}
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
rep "grep -q '^LoadCredential=claude-sp:'||continue;" ':;';fresh;cells true prd;run tick
ok "m4-MUTANT-no-LoadCredential-test-restarts-the-council-unit-RED council restarts $(nsd agi-council) (clean: 0)" '[ "$(nsd agi-council)" = 1 ]'
rep 'cmp -s $n $F' 'false';fresh;cells true prd;run tick;: >$T/sd.log;run tick
ok "m5-MUTANT-no-change-test-restarts-on-the-same-key-RED restarts $(wc -l <$T/sd.log|tr -d ' ') (clean: 0)" '[ -s $T/sd.log ]'
rep '[ -e $F ]&&rm -f $F&&echo' '[ -e $F ]&&echo';fresh;cells true prd;run tick;cells false prd;run tick
ok "m6-MUTANT-the-kill-without-the-rm-leaves-the-file-RED file $([ -e $T/cs/claude-sp ]&&echo THERE||echo gone) (clean: gone)" '[ -e $T/cs/claude-sp ]'
rep 'printf %s "$k">$n;' 'printf %s "$k">$n;chmod 644 $n;';fresh;cells true prd;run tick
ok "m7-MUTANT-a-world-readable-file-RED mode $(stat -c %a $T/cs/claude-sp) (clean: 600)" '[ "$(stat -c %a $T/cs/claude-sp)" != 600 ]'
PIECE=$P0
# ================= UNREAD (belam 10-25): the live unit's git read was refused (dubious ownership: carry.env has GIT_CONFIG_VALUE_0 but the
# unit had no COUNT/KEY_0), the cell read empty, and tick passed SILENTLY as "not live". Now an unreadable cell is a named unread, rc 3, fail closed.
printf x >$T/cs/claude-sp;TRUNK=refs/heads/no-such-ref run tick
ok "u1-an-unreadable-secrets-cell-is-unread-rc3-and-the-key-file-goes rc $rc (want 3), file $([ -e $T/cs/claude-sp ]&&echo present||echo gone)" '[ $rc = 3 ] && [ ! -e $T/cs/claude-sp ] && grep -q "\[cred\] unread" $T/e'
u2(){ grep -c '^Environment=.*GIT_CONFIG' $1;}
ok "u2-the-service-carries-no-git-config-pair (the piece scopes its own read; carry.env VALUE_0 is inert without COUNT/KEY_0) $(u2 $UNIT)" '[ "$(u2 $UNIT)" = 0 ]'
{ cat $UNIT;echo 'Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory';}>$T/unit.pair
ok "u2m-MUTANT-the-pair-restored-in-the-unit-RED $(u2 $T/unit.pair) (clean: 0)" '[ "$(u2 $T/unit.pair)" != 0 ]'
rep '[ -n "$s" ]||{' 'true||{';printf x >$T/cs/claude-sp;TRUNK=refs/heads/no-such-ref run tick;PIECE=$P0
ok "u1m-mutant-guard-dropped-reads-silent-rc0-RED rc $rc" '[ $rc = 0 ] && ! grep -q "\[cred\] unread" $T/e'
rm -f $T/cs/claude-sp
# ================= HOME (belam 10-25): the first live start after the pin move (L124) exited 5 "doppler gave no key": systemd gives the unit no HOME and doppler refuses without one
ok "u3-the-service-sets-HOME-for-doppler $(sect agi-cred.service|grep -c "^Environment=HOME=/root$")" '[ "$(sect agi-cred.service|grep -c "^Environment=HOME=/root$")" = 1 ]'
U0=$UNIT;grep -v '^Environment=HOME=' $U0>$T/unit.mut;UNIT=$T/unit.mut;fresh;cells true prd;run tick;UNIT=$U0
ok "u3m-MUTANT-the-unit-without-HOME-writes-no-key-RED rc $rc (clean: 0), file $([ -e $T/cs/claude-sp ]&&echo THERE||echo none)" '[ $rc = 5 ]&&[ ! -e $T/cs/claude-sp ]&&grep -q "doppler gave no key" $T/e'
rm -f $T/cs/claude-sp
# ================= ROW 1 + 1' (council L127): the rc-5 line names doppler's cause (its 'Doppler Error' line, else its first) and never a token or key
U0=$UNIT;UNIT=$T/unit.mut;fresh;cells true prd;run tick;UNIT=$U0
ok "r1-the-rc5-line-names-the-cause rc $rc, say: $(cut -c1-110 $T/e)" '[ $rc = 5 ]&&grep -qF "(doppler: Doppler Error: \$HOME is not defined)" $T/e'
fresh;cells true prd;printf 'dp.st.TOKSECRET9abc' >$T/cs/doppler-token;DERR=1;run tick
ok "r2-a-dp-token-and-a-key-in-the-error-are-redacted-the-cause-kept rc $rc, token bytes $(grep -c TOKSECRET9 $T/e), key bytes $(grep -c TESTCANARY $T/e), say: $(cut -c1-110 $T/e)" '[ $rc = 5 ]&&grep -qF "(doppler: Doppler Error: token [redacted] rejected; last value [redacted])" $T/e&&! grep -q -e TOKSECRET9 -e TESTCANARY $T/e'
fresh;cells true prd;DERR=1;run tick
ok "r3-a-token-of-no-known-shape-blanks-the-whole-line rc $rc, token bytes $(grep -c TOKVALUE9 $T/e), say: $(cut -c1-110 $T/e)" '[ $rc = 5 ]&&grep -qF "(doppler: [redacted])" $T/e&&! grep -q TOKVALUE9 $T/e'
# OBSERVED copy, ONE line differs (checked): the read's env -i gets the stub dir on PATH (the real read finds git only on /usr/bin:/bin), plus GIT_CONFIG_SYSTEM=<hostile>
# standing in for a hostile /etc/gitconfig (a plain user cannot write it) and HOME=<a dir whose .gitconfig is hostile> standing in for a kept HOME: NOSYSTEM and GLOBAL=/dev/null must hold against both
mkdir -p $T/hh;cp $T/hostile.gc $T/hh/.gitconfig
obs(){ sed "s|env -i PATH=/usr/bin:/bin |env -i PATH=$SH:/usr/bin:/bin GIT_CONFIG_SYSTEM=$T/hostile.gc HOME=$T/hh |" $1 >$T/obs;PIECE=$T/obs;}
obs $P0;nd=$(diff $P0 $T/obs|grep -c '^>')
fresh;cells true prd;rm -f $T/sdcfg $T/gitenv;run tick
ok "s1-under-a-hostile-env-the-read-sees-ONLY-AGI_REPO-the-REAL-cell-and-3-GIT-names-plus-the-observed-SYSTEM rc $rc, observed lines changed $nd, effective: $(tr '\n' ' ' <$T/sdcfg 2>/dev/null), file $([ -e $T/cs/claude-sp ]&&echo written||echo NONE), GIT_* seen: $(cat $T/gitenv 2>/dev/null)" '[ $nd = 1 ]&&[ $rc = 0 ]&&[ "$(cat $T/sdcfg)" = "$M" ]&&[ -e $T/cs/claude-sp ]&&[ "$(cat $T/gitenv)" = "GIT_CONFIG_GLOBAL GIT_CONFIG_NOSYSTEM GIT_CONFIG_SYSTEM GIT_NO_REPLACE_OBJECTS " ]'
ok "s1p-the-real-read-keeps-only-the-system-PATH $(grep -c 'env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 git ' $P0)" '[ "$(grep -c "env -i PATH=/usr/bin:/bin GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_REPLACE_OBJECTS=1 git " $P0)" = 1 ]'
rep 'env -i PATH=/usr/bin:/bin ' '';fresh;cells true prd;rm -f $T/sdcfg;run tick
ok "m23-MUTANT-no-env-i-the-hostile-env-reaches-the-read-RED rc $rc, effective: $(tr '\n' ' ' <$T/sdcfg 2>/dev/null), file $([ -e $T/cs/claude-sp ]&&echo written||echo none) (clean: only AGI_REPO, written)" 'grep -qx "\*" $T/sdcfg||[ ! -e $T/cs/claude-sp ]'
for x in 'GIT_CONFIG_NOSYSTEM=1 :m20-system' 'GIT_CONFIG_GLOBAL=/dev/null :m21-global';do e=${x%%:*};rep "$e" '';obs $PIECE;fresh;cells true prd;rm -f $T/sdcfg;run tick
 ok "${x#*:}-MUTANT-that-config-file-read-admits-*-RED effective: $(tr '\n' ' ' <$T/sdcfg 2>/dev/null)" 'grep -qx "\*" $T/sdcfg';done
rep '-c safe.directory="$AGI_REPO" ' '';obs $PIECE;fresh;cells true prd;rm -f $T/sdcfg;run tick
ok "m22-MUTANT-no-scoped-value-the-effective-set-is-not-AGI_REPO-RED effective: [$(tr '\n' ' ' <$T/sdcfg 2>/dev/null)]" '[ "$(cat $T/sdcfg 2>/dev/null)" != "$M" ]'
PIECE=$P0
rpl(){ b=$($G -C $M rev-parse $TR:.agi/nodes/.geometry/secrets.md);nb=$(sed 's/^credits_live: .*/credits_live: false/' $M/.agi/nodes/.geometry/secrets.md|$G -C $M hash-object -w --stdin);$G -C $M replace -f $b $nb;}
fresh;cells true prd;rpl;run tick;$G -C $M replace -d $b >/dev/null
ok "s2-a-replace-object-over-the-cell-is-ignored rc $rc, file $([ -e $T/cs/claude-sp ]&&echo written||echo NONE)" '[ $rc = 0 ]&&[ -e $T/cs/claude-sp ]'
rep '2>$e)' '2>/dev/null)';fresh;cells true prd;UNIT=$T/unit.mut;run tick;UNIT=$U0
ok "m13-MUTANT-doppler-stderr-dropped-names-no-cause-RED say: $(cut -c1-90 $T/e)" '! grep -qF "\$HOME is not defined" $T/e'
rep 's/dp\.(st|sa|ct|pt|scim|audit)\.[A-Za-z0-9]+/[redacted]/g;' '';fresh;cells true prd;printf 'dp.st.TOKSECRET9abc' >$T/cs/doppler-token;DERR=1;run tick
ok "m14-MUTANT-no-dp-redaction-loses-the-cause-to-the-blanket-RED say: $(cut -c1-90 $T/e)" '! grep -qF "token [redacted] rejected" $T/e'
rep ';s/$P-[A-Za-z0-9_-]+/[redacted]/g' '';fresh;cells true prd;printf 'dp.st.TOKSECRET9abc' >$T/cs/doppler-token;DERR=1;run tick
ok "m16-MUTANT-no-key-redaction-leaks-the-key-RED key bytes $(grep -c TESTCANARY $T/e) (clean: 0)" 'grep -q TESTCANARY $T/e'
rep "case \$l in *\"\$tk\"*)l='[redacted]';;esac" ':';fresh;cells true prd;DERR=1;run tick
ok "m15-MUTANT-no-token-guard-leaks-a-shapeless-token-RED token bytes $(grep -c TOKVALUE9 $T/e) (clean: 0)" 'grep -q TOKVALUE9 $T/e'
rep 'GIT_NO_REPLACE_OBJECTS=1 ' '';fresh;cells true prd;rpl;run tick;$G -C $M replace -d $b >/dev/null
ok "m17-MUTANT-replace-objects-honoured-reads-the-forged-cell-RED file $([ -e $T/cs/claude-sp ]&&echo written||echo none) (clean: written)" '[ ! -e $T/cs/claude-sp ]'
PIECE=$P0;rm -f $T/cs/claude-sp
# ================= K' (council 10-25): the live start said 'lane units restarted' with 0 lane units present; the line now carries k/m
fresh;cells true prd;run tick
ok "k1-the-write-line-counts-the-restarts $(cut -c1-90 $T/o)" 'grep -q "written (0600): lane units restarted 2/2$" $T/o'
fresh;cells true prd;SDF=agi-kids.service;run tick
ok "k2-a-failed-restart-is-counted-not-hidden $(cut -c1-90 $T/o)" 'grep -q "lane units restarted 1/2$" $T/o'
nou(){ for x in batch kids;do printf '[Service]\nExecStart=/bin/true\n'>$T/units/agi-$x.service;done;}
reu(){ for x in batch kids;do printf '[Service]\nLoadCredential=claude-sp:/etc/credstore/claude-sp\n'>$T/units/agi-$x.service;done;}
nou;fresh;cells true prd;run tick;a=$(cat $T/o);cells false prd;run tick;b=$(cat $T/o)
ok "k3-no-lane-unit-reads-0-hold-and-no-bare-restarted write: $(printf %s "$a"|cut -c30-90); kill: $(printf %s "$b"|cut -c30-110)" 'printf "%s\n%s\n" "$a" "$b"|grep -c "0 lane units hold the credential$"|grep -qx 2&&! printf "%s\n%s\n" "$a" "$b"|grep -q restarted'
rep '[ $m = 0 ]&&echo "0 lane units hold the credential"||' '';fresh;cells true prd;run tick
ok "m18-MUTANT-no-zero-branch-says-restarted-with-no-unit-RED $(cut -c30-90 $T/o)" 'grep -q restarted $T/o'
reu;PIECE=$P0;rm -f $T/cs/claude-sp
# ================= NEGATIVE (leaf falsifier 3): the pieces and units name no key and no ANTHROPIC_API_KEY environment
n=$(for g in agi-cred agi-cred.service agi-cred.timer;do sect $g;done|grep -c -e "Environment=.*ANTHROPIC_API_KEY" -e "$KP-")
ok "n-the-three-pieces-hold-no-key-prefix-and-no-ANTHROPIC_API_KEY-environment hits $n (want 0)" '[ "$n" = 0 ]'
ok "n-the-service-carries-no-LoadCredential-or-key-env (it is root's own) $(sect agi-cred.service|grep -c -e LoadCredential -e ANTHROPIC)" '[ "$(sect agi-cred.service|grep -c -e LoadCredential -e ANTHROPIC)" = 0 ]'
echo "agi-cred: $f FAIL";exit $f
