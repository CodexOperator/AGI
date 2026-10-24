---
id: config:engine-capsule
mint_id: 37c93fa1308042e8af3e0070a154a78a
type: config
parents:
  - goal:g7.16.1.11.44
next_edges: []
edited_by: director-general-4
season: 2
town: core
---
# config:engine-capsule

EXPANSION of config:engine: the capsule verbs (goal:g7.16.1.11.44, doc:g716111-44-capsule-pack): ONE signed ref refs/capsule/CID carries a graph slice or a post's refs; its bundle moves it; pack · out · verify · in · regrow · repoint (capsule move is not built)
Read only through `sect capsule [REV] | sh -s -- VERB ARGS` (a post's extraction loop skips this node: its glob is engine.md engine-[pw]*.md, so no post gains or loses a piece when this file changes). Run it in the repo that holds the refs: AGI_POST packs as <post>@agi, AGI_ALLOWED is the ring, AGI_TRUNK the repo's trunk.
MANIFEST `atoms:` section (SPEC only, goal:g7.16.1.11.46.4; U3 in wave 2 fills it from the pack route, the capsule piece does not read it yet): a line `atoms:` then one line per moved atom, `  <atom id> <src> <slice sha12>`: the id, src and sha that `agi-atom move` wrote into the flow's ARGS json (`.atoms[]`), so a receiver re-derives each slice's sha12 from the ARGS and an atom is in the pack OR on a card, never both.

## pieces — depth 1, one line each (bytes on disk)
~~~
capsule           8041 B  signed slice ref <-> bundle: pack out verify in..
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### capsule (8041 B)
~~~sh
#!/bin/sh
# capsule pack ATTACH subtree MINT|post P|list MINT.. [--ref GLOB].. [--kind slice|secret] [--encrypt none|quorum] | out CID >FILE | verify FILE|CID | in FILE | regrow CID DIR | repoint CID MINT   (doc:g716111-44-capsule-pack)
# a capsule = ONE signed commit refs/capsule/CID (MANIFEST + members at their repo paths); its bundle = that ref + every ref its `ref` lines name. Run in the repo; AGI_POST packs as <post>@agi, AGI_ALLOWED = the ring, AGI_TRUNK = this repo's trunk (default HEAD); rc 2 refused at pack, 3 [attach-absent], 4 refused at verify, 128 git
set -f;export GIT_NO_REPLACE_OBJECTS=1;A=${AGI_ALLOWED:-/var/lib/agi/allowed_signers};T=${AGI_TRUNK:-HEAD};V=$1;shift
die(){ echo "$2">&2;exit $1;}
m32(){ case $1 in ""|*[!0-9a-f]*)return 1;;esac;[ ${#1} = 32 ];}
at(){ m32 $1&&git grep -q "^mint_id: $1\$" $T -- .agi/nodes;}
chk(){ g="git --git-dir=$1";t=$($g rev-parse -q --verify refs/capsule/$2^{commit})||die 4 "[none] $2";M=$($g show $t:MANIFEST)||die 4 "[manifest] $2";k=$(echo "$M"|sed -n 's/^packer //p')
 [ "$(echo "$M"|sed -n 1,3p|tr '\n' ' ')" = "capsule 1 cid $2 kind slice " ]||die 4 "[manifest] $2: not 'capsule 1 / cid / kind slice'"
 for x in $($g rev-list --first-parent $t);do [ "$($g -c gpg.ssh.allowedSignersFile=$A log -1 --format='%G? %GS' $x)" = "G $k" ]||die 4 "[sig] $x is not G by $k"
  q=$($g rev-parse -q --verify $x^)||continue;[ "$($g diff-tree -r --name-only $q $x)" = MANIFEST ]&&[ "$($g show $q:MANIFEST|grep -v '^attach ')" = "$($g show $x:MANIFEST|grep -v '^attach ')" ]||die 4 "[tree] $x differs from its parent beyond attach";done
 [ "$($g ls-tree -r --name-only $t|grep -vx MANIFEST|sort)" = "$(echo "$M"|sed -n 's/^member [0-9a-f]* //p'|sort)" ]||die 4 "[tree] $2: the tree is not exactly the member lines"
 w=$(echo "$M"|sed -n 's/^attach //p');at $w||die 3 "[attach-absent] $2 $w";}
vf(){ [ -f "$1" ]||{ m32 $1&&{ chk "$(git rev-parse --git-dir)" $1;return;};die 4 "[arg] $1";}
 git bundle verify "$1">/dev/null 2>&1||die 4 "[bundle] $1: not a bundle this repo can open";H=$(git bundle list-heads "$1"|sort);c=$(echo "$H"|sed -n 's|.* refs/capsule/\([0-9a-f]*\)$|\1|p');m32 $c&&[ $(echo "$H"|grep -c ' refs/capsule/') = 1 ]||die 4 "[heads] not exactly one refs/capsule/CID"
 s=$(mktemp -d);trap 'rm -rf $s' 0;git init -q --bare $s/s;echo "$(cd "$(git rev-parse --git-path objects)"&&pwd)">$s/s/objects/info/alternates;g="git --git-dir=$s/s";$g fetch -q "$1" refs/capsule/$c:refs/capsule/$c||die 4 "[fetch] $c";chk $s/s $c
 b=$($g show refs/capsule/$c:MANIFEST|sed -n 's/^base //p');[ "$H" = "$({ echo "$($g rev-parse refs/capsule/$c) refs/capsule/$c";$g show refs/capsule/$c:MANIFEST|sed -n 's/^ref \(.*\) \(.*\)$/\1 \2/p'|while read r n;do git cat-file -e $n^{commit} 2>/dev/null&&git merge-base --is-ancestor $n $b||echo "$n $r";done;}|sort)" ]||die 4 "[heads] the bundle's refs are not exactly the ref lines less the behind-base ones";}
case $V in
pack) a=$1;shift;W=;K=slice;E=none;L=;while [ $# -gt 0 ];do case $1 in --ref)L="$L $2";shift 2;;--kind)K=$2;shift 2;;--encrypt)E=$2;shift 2;;*)W="$W $1";shift;;esac;done;set -- $W;S=$1;shift
 [ $K = slice -a $E = quorum ]&&die 2 "[class] a slice is never quorum-popped";[ $K = secret -a $E != quorum ]&&die 2 "[class] a secret is always quorum-sealed";[ $K = slice ]||die 2 "[secret] capsule-pop packs a secret, not this verb";[ $E = none ]||die 2 "[seal] $E waits in the .11 HOLD"
 P=${AGI_POST:?};at $a||die 3 "[attach-absent] $a";d=$(mktemp -d);trap 'rm -rf $d' 0
 case $S in subtree|list)for x in "$@";do at $x||die 3 "[attach-absent] $x";done
  git ls-tree -r $T .agi/nodes|awk -F'\t' '$1~/ blob /&&$2~/\.md$/&&$2!~/ /{split($1,a," ");print a[3],$2}'|git cat-file --batch='@ %(rest)'|awk '/^@ /{p=$2;h=0;l=0;next} h>1{next} /^---$/{h++;next} h==1{if($0~/^id: /)i[p]=$2;else if($0~/^mint_id: /)n[p]=$2;else if($0~/^payload_ref: /)y[p]=$2;else if($0~/^parents:/){l=1;s=$0;if(s~/\[/){gsub(/parents: *\[|\]|,/," ",s);c=split(s,q," ");for(j=1;j<=c;j++)o[p]=o[p]" "q[j];l=0}}else if(l&&$0~/^ +- /){x=$0;sub(/^ +- /,"",x);o[p]=o[p]" "x}else l=0}END{for(p in n)print n[p],i[p],p,(y[p]==""?"-":y[p]),o[p]}'>$d/tab
  awk -v s=$S -v r="$*" 'BEGIN{split(r,R," ")}{m[$2]=$1;f[$2]=$3;y[$2]=$4;I[$1]=$2;for(j=5;j<=NF;j++)c[$j]=c[$j]" "$2}END{if(s=="list"){for(k in R)w[I[R[k]]]=1}else{q[1]=I[R[1]];w[q[1]]=1;t=1;for(h=1;h<=t;h++){n=split(c[q[h]],z," ");for(j=1;j<=n;j++)if(!(z[j] in w)){w[z[j]]=1;q[++t]=z[j]}}}for(k in w)if(k!=""){print m[k],f[k];if(y[k]!="-")print m[k],y[k]}}' $d/tab|sort -u>$d/m0;git ls-tree -r --name-only $T|sort>$d/all;awk 'NR==FNR{a[$0]=1;next}$2 in a' $d/all $d/m0>$d/mem;[ -s $d/mem ]||die 2 "[none] no members";;
 post)case $1 in ""|*[!a-z0-9-]*)die 2 "[post] $1";esac;: >$d/mem;L="refs/heads/posts/$1 refs/box/$1/ refs/held/$1/ refs/archive/posts/$1* $L";;*)die 2 "[sel] subtree MINT | post P | list MINT..";;esac
 { [ -z "$L" ]||git for-each-ref --format='%(refname) %(objectname)' $L;}|grep -v '^refs/capsule/'|sort -u>$d/ref;c=${CID:-$(tr -d - </proc/sys/kernel/random/uuid)}
 { echo capsule 1;echo cid $c;echo kind $K;echo attach $a;echo encrypt $E;echo packer $P@agi;echo base $(git rev-parse $T);sed 's/^/member /' $d/mem;sed 's/^/ref /' $d/ref;printf 'not %s\n' "ram-trees uncommitted" "untracked-mints no tree entry" "host-files outside the repo" "crontabs outside the repo" "refs/stash a two-part ref cannot ride a bundle" "refs/remotes the target fetches its own";}>$d/MANIFEST
 { printf '100644 %s\tMANIFEST\n' $(git hash-object -w $d/MANIFEST);while read m f;do printf '100644 %s\t%s\n' $(git rev-parse $T:$f) $f;done<$d/mem;}|GIT_INDEX_FILE=$d/x git update-index --add --index-info&&t=$(GIT_INDEX_FILE=$d/x git write-tree)&&\
 n=$(GIT_AUTHOR_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_NAME=$P GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S -m "capsule $c" $t)&&git update-ref refs/capsule/$c $n ""&&echo $c;;
out) c=$1;m32 $c||die 2 "[cid] $c";chk "$(git rev-parse --git-dir)" $c;M=$(git show refs/capsule/$c:MANIFEST);b=$(echo "$M"|sed -n 's/^base //p');K=;R=$(echo "$M"|sed -n 's/^ref \(.*\) \(.*\)/\1/p')
 for r in $R;do [ "$(git rev-parse -q --verify $r)" = "$(echo "$M"|sed -n "s|^ref $r ||p")" ]||die 4 "[moved] $r is not at its ref line";git merge-base --is-ancestor $r $b||K="$K $r";done
 d=$(mktemp -d);trap 'rm -rf $d' 0;git bundle create $d/b refs/capsule/$c $K --not $b||exit;{ sed -n 1p $d/b;[ "$(sed -n 2p $d/b|cut -c1)" = - ]||echo "-$b base";tail -n +2 $d/b;};;
verify) vf "$1";;
in) [ -f "$1" ]||die 2 "[file] $1";vf "$1";git bundle unbundle "$1">/dev/null||die 4 "[unbundle] $1";Z=$(git hash-object --stdin </dev/null|tr 0-9a-f 0);: >$s/u
 { echo "$H";$g show refs/capsule/$c:MANIFEST|sed -n 's/^ref \(.*\) \(.*\)$/\2 \1/p';}|sort -u -k2|while read n r;do o=$(git rev-parse -q --verify $r);[ "$o" = $n ]&&continue;git worktree list --porcelain|grep -qx "branch $r"&&echo "[checked-out] $r">>$s/e;[ -z "$o" ]||git merge-base --is-ancestor $o $n||echo "[non-ff] $r">>$s/e;echo "update $r $n ${o:-$Z}">>$s/u;done
 [ ! -s $s/e ]||die 4 "$(cat $s/e)";{ echo start;cat $s/u;echo prepare;echo commit;}|git update-ref --stdin>/dev/null;;
regrow) m32 $1&&[ -n "$2" ]||die 2 "[arg] regrow CID DIR";chk "$(git rev-parse --git-dir)" $1;mkdir -p "$2"&&git archive refs/capsule/$1|tar -x -C "$2";;
repoint) c=$1;a=$2;m32 $c||die 2 "[cid] $c";P=${AGI_POST:?};chk "$(git rev-parse --git-dir)" $c;at $a||die 3 "[attach-absent] $a";o=$(git rev-parse refs/capsule/$c);M=$(git show $o:MANIFEST);[ "$P@agi" = "$(echo "$M"|sed -n 's/^packer //p')" ]||die 2 "[packer] only $(echo "$M"|sed -n 's/^packer //p') re-points $c"
 d=$(mktemp -d);trap 'rm -rf $d' 0;echo "$M"|sed "s/^attach .*/attach $a/">$d/MF;export GIT_INDEX_FILE=$d/x;git read-tree $o&&git update-index --add --cacheinfo 100644,$(git hash-object -w $d/MF),MANIFEST&&n=$(GIT_AUTHOR_NAME=$P GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_NAME=$P GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S -p $o -m "re-point $c to $a" $(git write-tree))&&git update-ref refs/capsule/$c $n $o&&echo $n;;
*)die 2 "capsule pack|out|verify|in|regrow|repoint";;esac
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-4 10-11 22:xxZ, goal:g7.16.1.11.44.1-.6 (SM 21:06Z): ONE piece, one case arm per verb, so a leaf adds an arm, never a file; `sect capsule | sh -s -- VERB`. Built to the council's section 5 with FOUR deviations the bytes forced, each a lane row: (1) a ref BEHIND base cannot ride a thin bundle (git drops it from the heads; a fat bundle measured 21,122 commits / 287 MiB): FF1 (council 01:41Z) it rides as its MANIFEST ref line ONLY, out is always thin, verify = heads == the ref lines less the behind-base ones (each checked on the target by cat-file -e + merge-base --is-ancestor <sha> <base>), and `in` is `git bundle unbundle` (objects only) + ONE `update-ref --stdin` transaction over every ref (carried and behind), checking each ref is an ancestor of its new value first (`[non-ff]`), and refusing a branch a worktree has checked out (`[checked-out]`); (2) a capsule commit is a ROOT commit, so `--not base` alone leaves a bundle with no prerequisite and O1 could not fail: out writes `-<base>` into the header itself; (3) verify reads a bundle through a scratch bare repo whose alternates point at the repo, so it writes nothing to the repo (the byte-identical row is structural); (4) out refuses `[moved]` when a ref line's ref is no longer at its pinned sha. A sealed capsule (encrypt box/post) is refused `[seal]`: it waits in the .11 HOLD (Q2); a secret is refused `[secret]`: capsule-pop owns it (Q3). repoint is signed by the packer only (`[packer]`, rc 2): the chain rule reads every commit as G by the MANIFEST's packer. The landing lane over every refs/capsule/* is the `l` section of extensions/agi/tests/capsule.t.sh (LANDING_REPO, LAND_TRUNK, CAPSULE_FLOOR). Not built: `capsule move` (box-move.sh's carry; the design's section 6).
<!-- THOUGHT:END -->
