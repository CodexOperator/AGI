#!/bin/sh
# k2a-kid.t.sh: goal:g7.16.1.11.18 K2(a) no-root half (Z4.11). sh + git + a stub pi + a stub runuser.
# Z4.k (EACCES on caller ssh / id -G / update-ref) is ROOT and is NOT this file.
# PIECE files default: sect from ROOT's engine*.md. One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0
R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
G=/data/work/agi/.git
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect agi-kid@.service>$T/unit;sect agi-kid-run>$T/run;sect agi-kid-out>$T/out
ok "extract-unit agi-kid@.service is 443 B ($(wc -c<$T/unit) B)" '[ $(wc -c<$T/unit) -eq 443 ]'
ok "extract-run agi-kid-run is 583 B ($(wc -c<$T/run) B)" '[ $(wc -c<$T/run) -eq 583 ]'
ok "extract-out agi-kid-out is 319 B ($(wc -c<$T/out) B)" '[ $(wc -c<$T/out) -eq 319 ]'
ok "sg-0 the unit has 0 SupplementaryGroups" '! grep -q SupplementaryGroups $T/unit'
ok "dyn DynamicUser=yes" 'grep -qx DynamicUser=yes $T/unit'
ok "binds BindsTo=agi-mint@%i.service" 'grep -qx BindsTo=agi-mint@%i.service $T/unit'
ok "hide TemporaryFileSystem hides /data and /var/lib/agi" 'grep -q "TemporaryFileSystem=/data:ro /var/lib/agi:ro" $T/unit'
ok "gitro BindReadOnlyPaths is the shared .git" 'grep -qx BindReadOnlyPaths=/data/work/agi/.git $T/unit'
ok "run-sh POSIX sh" 'dash -n $T/run'
ok "out-sh POSIX sh" 'dash -n $T/out'
# --- run: id must be a FULL commit sha (short / branch / blob / unknown = rc 2, no out)
export RUNTIME_DIRECTORY=$T/rt CREDENTIALS_DIRECTORY=$T/cred
mkdir -p $T/rt $T/cred $T/bin
printf canary>$T/cred/key
printf '#!/bin/sh\necho STUBPI "$@"\necho ran>>%s/pi.log\n' $T>$T/bin/pi;chmod +x $T/bin/pi
PATH=$T/bin:$PATH
H=$(git --git-dir=$G rev-parse HEAD)
short=$(git --git-dir=$G rev-parse --short=7 HEAD)
blob=$(printf x|git --git-dir=$G hash-object --stdin)
unk=0000000000000000000000000000000000000000
runid(){ rm -rf $T/rt;mkdir $T/rt;sh $T/run "p--$1" >/dev/null 2>&1;echo $?;}
ok "run-short a 7-char sha exits 2, writes no out (rc=$(runid $short))" '[ $(runid $short) -eq 2 ]&&[ ! -e $T/rt/out ]'
ok "run-branch HEAD as the id exits 2 (rc=$(runid HEAD))" '[ $(runid HEAD) -eq 2 ]'
ok "run-blob a blob sha exits 2 (rc=$(runid $blob))" '[ $(runid $blob) -eq 2 ]'
ok "run-unk an unknown 40-hex exits 2 (rc=$(runid $unk))" '[ $(runid $unk) -eq 2 ]'
# dangling IN commit (no ref): tree = .kid/prompt + .kid/model
export GIT_AUTHOR_NAME=k2a GIT_AUTHOR_EMAIL=k2a@agi GIT_COMMITTER_NAME=k2a GIT_COMMITTER_EMAIL=k2a@agi
mkdir -p $T/in/.kid
printf 'PROMPT-K2A'>$T/in/.kid/prompt;printf 'MODEL-K2A'>$T/in/.kid/model
tin=$(git --git-dir=$G hash-object -w -t tree --stdin </dev/null)
# build tree via index in T
GIT_INDEX_FILE=$T/ix GIT_DIR=$G git read-tree --empty
GIT_INDEX_FILE=$T/ix GIT_DIR=$G git update-index --add --cacheinfo 100644,$(printf 'PROMPT-K2A'|git --git-dir=$G hash-object -w --stdin),.kid/prompt
GIT_INDEX_FILE=$T/ix GIT_DIR=$G git update-index --add --cacheinfo 100644,$(printf 'MODEL-K2A'|git --git-dir=$G hash-object -w --stdin),.kid/model
tr=$(GIT_INDEX_FILE=$T/ix GIT_DIR=$G git write-tree)
c=$(git --git-dir=$G commit-tree $tr -m k2a-in)
ok "in-sha the IN id is a full 40-hex commit" '[ ${#c} -eq 40 ]&&[ "$(git --git-dir=$G rev-parse -q --verify $c^{commit})" = $c ]'
rm -rf $T/rt;mkdir $T/rt
PATH=$T/bin:$PATH RUNTIME_DIRECTORY=$T/rt CREDENTIALS_DIRECTORY=$T/cred sh $T/run "aio--$c" >/dev/null 2>&1;rc=$?
ok "run-full a full-sha IN unpacks and the stub pi runs (rc=$rc)" '[ $rc -eq 0 ]&&grep -q ran $T/pi.log'
ok "run-slice .kid/prompt and .kid/model are the IN tree" '[ "$(cat $T/rt/s/.kid/prompt)" = PROMPT-K2A ]&&[ "$(cat $T/rt/s/.kid/model)" = MODEL-K2A ]'
ok "run-out the stub wrote ./out" '[ -s $T/rt/out ]'
ok "run-key the canary is not in out" '! grep -q canary $T/rt/out'
# --- out: regular file handed to stub runuser; a symlink is not followed
printf '#!/bin/sh\ncat >%s/handed\n' $T>$T/bin/runuser;chmod +x $T/bin/runuser
export RUNTIME_DIRECTORY=$T/rt
printf 'RESULT-K2A'>$T/rt/out
rm -f $T/handed
PATH=$T/bin:$PATH sh $T/out 'alive--deadbeef' >/dev/null 2>&1;rc=$?
ok "out-file a regular ./out is handed byte for byte (rc=$rc)" '[ $rc -eq 0 ]&&[ "$(cat $T/handed)" = RESULT-K2A ]'
rm -f $T/handed $T/rt/out
ln -s /etc/passwd $T/rt/out
PATH=$T/bin:$PATH sh $T/out 'alive--deadbeef' >/dev/null 2>&1;rc=$?
ok "out-link a symlink ./out hands nothing (rc=$rc)" '[ $rc -eq 0 ]&&[ ! -e $T/handed ]'
rm -f $T/rt/out
PATH=$T/bin:$PATH sh $T/out 'alive--deadbeef' >/dev/null 2>&1;rc=$?
ok "out-absent missing ./out is silent rc 0" '[ $rc -eq 0 ]&&[ ! -e $T/handed ]'
ok "no-python the three pieces need no python" '! grep -qi python $T/unit $T/run $T/out'
echo "k2a-kid: $f FAIL"
exit $f
