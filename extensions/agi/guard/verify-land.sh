#!/bin/sh
# verify-land.sh N LANDSHA BASE GATETIP -- held, tree, parents, G, D, anonymize, home, gpu
N=$1 L=$2 B=$3 G=$4; S=$(dirname $0); cd $HOME/t || exit 2
git fetch -q origin 2>/dev/null
H=$(git -C /data/work/agi rev-parse -q --verify refs/held/sanctuary-master/$N 2>/dev/null || git rev-parse -q --verify refs/held/sanctuary-master/$N)
L=$(git rev-parse $L); echo "held=$(echo $H|cut -c1-10) land=$(echo $L|cut -c1-10) $( [ "$H" = "$L" ] && echo OK || echo MISMATCH)"
echo "parents: $(git log -1 --format=%P $L | awk '{print substr($1,1,10), substr($2,1,10)}') want $(git rev-parse --short=10 $B) $(git rev-parse --short=10 $G)"
echo "tree $(git rev-parse --short=10 $L^{tree}) merge-tree $(git merge-tree --write-tree $B $G | head -1 | cut -c1-10)"
echo "sigs: $(git log --format=%G? $B..$L | sort | uniq -c | tr '\n' ' ')"
echo "D: $(git diff --name-status $B $L | grep -c '^D')  files: $(git diff --name-status $B $L | tr '\t\n' ' ')"
git diff $B $L > $S/$N.diff; git log --format=%B $B..$L > $S/$N.msg
python3 extensions/agi/bin/anonymize.py check --diff-file $S/$N.diff; echo "anon-diff=$?"
python3 extensions/agi/bin/anonymize.py check --text "$(cat $S/$N.msg)" >/dev/null; echo "anon-msg=$? emails: $(grep -o -E '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' $S/$N.msg | sort -u | tr '\n' ' ')"
python3 -I - $S/$N.diff $S/$N.msg <<'P'
import pwd,sys
homes={p.pw_dir for p in pwd.getpwall() if len(p.pw_dir)>5 and p.pw_dir not in ('/nonexistent','/var/empty','/usr/sbin')}
print('home hits', [h for f in sys.argv[1:] for h in homes if h+'/' in open(f,errors='replace').read()])
P
echo "gpu: $(grep -c -i -E 'nvidia|cuda|gpu' $S/$N.diff)"
