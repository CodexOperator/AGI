# AB.6: G1-G7, B1-B2, W1-W2 on the r3 fixture; seal.yml extracted by the runner
S=$1;K=$S/k;export AGI_CKPT=$S/ckpt;cd $S/r3;git checkout -q --detach trunk
sub(){ git ls-tree -r --name-only $1|LC_ALL=C sort|while read f;do printf '%s %s\n' "$(git show $1:$f|sha256sum|cut -c1-64)" "$f";done|sha256sum|cut -c1-64; }
pl(){ c=$1;echo "$(git show $c:tip) $(git show $c:time) $(git show $c:hash)"|sha256sum|cut -c1-64; }
ok(){ [ "$2" = "$3" ]&&r=PASS||r=FAIL;printf '%-4s %s (%s)\n' $r "$1" "$2"; }
B=$(git for-each-ref --format='%(objectname)' refs/agi/block);n=$(echo "$B"|wc -l)
ok "G1 the signed-payload digest is SHARED across blocks over one tip+time (distinct < blocks)" "$([ $(for c in $B;do pl $c;done|sort -u|wc -l) -lt $n ]&&echo shared||echo distinct)" shared
ok "G2 AGI_SUBJECT is distinct per block" "$([ $(for c in $B;do sub $c;done|sort -u|wc -l) -eq $n ]&&echo distinct||echo shared)" distinct
c=$(git rev-parse refs/agi/block/L3);rm -rf $S/o;git init -q $S/o;git -C $S/o fetch -q $S/r3 "+refs/agi/block/L3:refs/agi/block/L3"
ok "G3 an OUTSIDER who fetched only the block recomputes AGI_SUBJECT" "$([ "$(sub $c)" = "$(cd $S/o&&sub refs/agi/block/L3)" ]&&echo equal||echo differ)" equal
L=$(sub $c);mkdir -p $S/stub;printf '#!/bin/sh\ncase "$2" in *%s) exit 0;; esac; exit 1\n' $L>$S/stub/gh;chmod +x $S/stub/gh
m=$(for b in $B;do d=$(sub $b);PATH=$S/stub:$PATH gh api "x/sha256:$d">/dev/null 2>&1||echo $d;done|wc -l)
ok "G4 the sweep lists every subject but the attested one" "$m" "$((n-1))"
ok "G5 seal.yml parses with schedule + workflow_dispatch and the three permissions" "$(python3 -c "import yaml;d=yaml.safe_load(open('$S/seal.yml'));o=d[True];p=d['permissions'];print('ok' if 'schedule' in o and 'workflow_dispatch' in o and p=={'contents':'read','id-token':'write','attestations':'write'} else 'bad')")" ok
ok "G6 git archive tar bytes differ across tar.umask 0002/0022/0077" "$(for u in 0002 0022 0077;do git -c tar.umask=$u archive --format=tar $c|sha256sum;done|sort -u|wc -l)" 3
ok "G7 AGI_SUBJECT is one value across the same three umasks" "$(for u in 0002 0022 0077;do git -c tar.umask=$u ls-tree $c>/dev/null;sub $c;done|sort -u|wc -l)" 1
i=$(mktemp);git ls-tree $c>$i;printf '100644 blob %s\t%s\n' $(echo x|git hash-object -w --stdin) 'evil name'>>$i;git update-ref refs/agi/block/ODD $(echo odd|git commit-tree $(git mktree<$i) -p refs/agi/block/L1 2>/dev/null||echo odd|git commit-tree $(git mktree<$i))
ok "B1 a signed block plus one stray file does not hold" "$(sh $S/ckpt check|grep -c " $(git rev-parse refs/agi/block/ODD)$")" 0;git update-ref -d refs/agi/block/ODD
ok "B2 the same block without it holds" "$(sh $S/ckpt check|grep -c " $c$")" 1
mkdir -p .github/workflows;echo "on: push">.github/workflows/zz.yml;git add -A;git -c user.signingKey=$K/dg1b.pub commit -q -S -m wf
ok "W1 DG1 lands a workflow on the trunk" "$(sh $S/ring-gate trunk HEAD>/dev/null 2>&1&&echo admitted||echo refused)" refused;git checkout -q --detach trunk
mkdir -p .github/workflows;echo "on: push">.github/workflows/zz.yml;git add -A;git -c user.signingKey=$K/by-cert.pub commit -q -S -m wf2
ok "W2 the owner (cert on belam's current key) lands it" "$(sh $S/ring-gate trunk HEAD>/dev/null 2>&1&&echo admitted||echo refused)" admitted;git checkout -q --detach trunk
