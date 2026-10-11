#!/bin/sh
# run.sh [REV]: §AB's measured cases (C, L/T/E/H, X, P/N, S, R, G/B/W) against the pieces EXTRACTED from doc:radically-simple-engine at REV (default HEAD) -- no second copy of any piece.
# HERMETIC: the caller's global + system git config are ignored (SM 04:0xZ: a global allowedSignersFile once hid a revoke bug). Every key is a THROWAWAY generated here (no private key is ever committed: the trunk refuses one). Needs git >= 2.34, OpenSSH >= 8.9, jq, python3 + cryptography + pyyaml. No root, no network.
R=${1:-HEAD};D=$(cd "$(dirname "$0")"&&pwd);top=$(git -C $D rev-parse --show-toplevel);S=$(mktemp -d);trap 'rm -rf $S' EXIT
doc(){ git -C $top show $R:.agi/nodes/doc/radically-simple-engine.md; }
ex(){ doc|awk -v n="$1" -v f="$2" 'index($0,"`" n "` whole")==1{a=1;next} a&&$0=="```" f{g=1;next} g&&$0=="```"{exit} g'>$S/$1; }
ex ring-gate sh;ex ckpt sh;ex revoke sh;ex pq.py python;ex seal.yml yaml;cp $D/*.sh $D/*.py $S/;mkdir $S/k
for n in ca belam1 belam2 alive1 alive2 sm1 dg1 dg1b dg2 aio1;do ssh-keygen -q -t ed25519 -N '' -f $S/k/$n -C $n;done
for n in belam1pq alive2pq dg1pq dg2pq sm1pq aio1pq;do ssh-keygen -q -t ecdsa -b 256 -N '' -f $S/k/$n -C $n;done
ssh-keygen -q -t ed25519 -N pw -f $S/k/enc -C enc
for n in belam1 belam2;do ssh-keygen -q -s $S/k/ca -I owner-window -n owner@agi -V -1m:+4h -z 7 $S/k/$n.pub;done
unset AGI_TRUNK AGI_SIGN AGI_HASHES AGI_CKK AGI_RULES;export AGI_CKPT=$S/ckpt GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
{ sh $S/cases.sh $S;sh $S/blk-cases.sh $S;sh $S/rev-cases.sh $S;sh $S/g-cases.sh $S;(cd $S&&python3 x.py&&python3 seal-test.py&&timeout 120 python3 -u pq-test.py </dev/null); } 2>/dev/null|tee $S/out|grep -E '^(PASS|FAIL)'
while IFS= read -r l;do grep -qxF "$l" $S/out&&echo "PASS $l"||echo "FAIL missing: $l";done<$D/py.expected>>$S/out
grep -E '^(PASS|FAIL) [A-Za-z0-9]' $S/out|grep -vE '^(PASS|FAIL) +(ADMIT|REFUSE|NO|HOLDS|HOLDS +|REFUSED)'|tail -13
echo "--- $(grep -c '^PASS' $S/out) PASS, $(grep -c '^FAIL' $S/out) FAIL";grep -q '^FAIL' $S/out&&exit 1;exit 0
