# R1-R7: revoke on the r3 fixture left by blk-cases.sh (DG1 gen1 handed off and sealed by L3b)
S=$1;K=$S/k;G=.agi/nodes/.geometry;export AGI_CKPT=$S/ckpt AGI_TRUNK=trunk;cd $S/r3;git checkout -q --detach trunk
pub(){ k=$(mktemp -d);printf '%s\n' "$1">$k/post;cp $K/$2 $k/key;tr=$(printf '100644 blob %s\tkey\n100644 blob %s\tpost\n' $(git hash-object -w $k/key) $(git hash-object -w $k/post)|git mktree);git update-ref refs/revoked $(echo "revoke $1"|git commit-tree $tr);rm -rf $k; }
v(){ o=$(timeout 30 sh $S/revoke 2>&1 </dev/null|head -1);case "$o" in revoked*)r=HOLDS;;*)r=REFUSED;;esac;[ $r = $2 ]&&x=PASS||x=FAIL;printf '%-4s %-8s %s\n' $x $r "$1"; }
pub director-general-1 dg1;  v "R1 DG1 gen1's key after the level-3 block sealed its hand-off" HOLDS
pub director-general-1 dg1b; v "R2 DG1 gen2's LIVE key" REFUSED
pub director-general-1 alive1; v "R3 a key that was never DG1's line" REFUSED
pub sanctuary-master dg1;    v "R3b DG1's retired key under ANOTHER post's name" REFUSED
pub director-general-1 enc;  v "R7 a passphrase-ENCRYPTED key (no prompt, no hang)" REFUSED
sed -i "s|^alive .*|alive $(cut -d' ' -f1,2 $K/alive2.pub)|" $G/ring;git add -A;git -c user.signingKey=$K/alive1.pub commit -q -S -m "alive hands off";sh $S/ring-gate trunk HEAD >/dev/null&&git branch -f trunk HEAD
pub alive alive1; v "R4 alive gen1 handed off, NO block seals it (grace)" REFUSED
x=$(git rev-parse trunk);y=$(date +%s);i=$(mktemp);j=0;for a in alive:alive2 all-is-one:aio1;do j=$((j+1));p=${a%%:*};f=${a#*:};b=$(sh $S/ckpt sign $p $K/$f $x $y|git hash-object -w --stdin);printf '100644 blob %s\t%s.%s\n' $b $p $j;done>$i
st=$(git mktree<$i);tr=$(printf '100644 blob %s\thash\n040000 tree %s\tsigs\n100644 blob %s\ttime\n100644 blob %s\ttip\n' $(echo "sha256 $(git archive --format=tar $x|sha256sum|cut -d' ' -f1)"|git hash-object -w --stdin) $st $(echo $y|git hash-object -w --stdin) $(echo $x|git hash-object -w --stdin)|git mktree);git update-ref refs/agi/block/L2b $(echo b|git commit-tree $tr -p refs/agi/block/L2)
v "R5 the same after alive + all-is-one cut a level-2 block over it" HOLDS
git -c user.signingKey=$K/alive1.pub commit -q -S --allow-empty -m forged;sh $S/ring-gate trunk HEAD >/dev/null 2>&1&&echo "FAIL ADMIT   R6 a commit signed with the PUBLISHED key"||echo "PASS REFUSED R6 a commit signed with the PUBLISHED key, any date";git checkout -q --detach trunk
