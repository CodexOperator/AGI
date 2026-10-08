#!/bin/sh
# engine-sizes.t.sh: goal:g1.41 B1 + B4 (DG1 22:12Z; hypothesis:g141-b-engine-grow-and-post-pieces-...): (B1) every size the engine states is the MEASURED size: the pieces map in engine.md (## pieces) and every ### heading of the .geometry/engine*.md equal the byte count of their fenced body, and the map lists every piece, agi-boot, agi-boot.service and matrix included; (B4) the engine-grow.md LIMITS line stops saying 'DG1 to rule' and records the ruling (no ring: cell on engine*.md) and the owner-only alternative.
# sh + awk + grep on a TREE, no git, no network, no root, 0 USD. ROOT=<tree> (or $1) = the tree whose .agi/nodes/.geometry/engine*.md is read as checked out; it runs on any tree. The measure is DG1's: the bytes of the lines of the FIRST fenced body (~~~ ... ~~~) under a ### heading, each line plus its newline (it reproduces A1's 447 / 1477 for agi-boot.service / agi-boot).
# Lanes: b1-measure-* the measure finds the pieces (non-vacuous); b1-headings-* every heading states its measured size; b1-map-* every map row is the measured size, no row names an absent piece, every piece is in the map, the three named pieces are; b4-* the LIMITS line: no `DG1 to rule`, the exact ruling text + its pointer, and the pointer RESOLVES to the hypothesis node whose `## DG1 RULING on B4` section names the owner-sign alternative.
# Honest limits: bytes, not meaning; engine.md's railed totals (fenced <= 8,192, whole <= 12,288) are the builder's own re-measure and are NOT asserted here (their measure is a convention the ceiling names, not this lane's); a heading whose first fence is not its piece body is not a case the lane can know.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};G=$R0/.agi/nodes/.geometry;f=0;T=$(mktemp -d);trap 'rm -rf $T' 0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
ls $G/engine*.md >/dev/null 2>&1&&[ -f $G/engine.md ]||{ echo "FAIL inputs: $G/engine*.md";exit 99;}
# heads: "name stated measured" for every ### heading that has a fenced body, across engine*.md
for F in $G/engine*.md;do LC_ALL=C awk '
function emit(){ print name, (st==""?"-":st), n }
/^### /{ if(name!=""&&fz==2) emit(); name=$2; st=""; if(match($0,/\([0-9]+ B\)/)) st=substr($0,RSTART+1,RLENGTH-4); fz=0; n=0; next }
/^## /{ if(name!=""&&fz==2) emit(); name=""; fz=0; next }
name!=""{ if(fz==0&&/^~~~/){fz=1;next} if(fz==1){ if(/^~~~/){fz=2;next} n+=length($0)+1 } }
END{ if(name!=""&&fz==2) emit() }' $F;done >$T/heads
# map: "name size" for each row of the ## pieces fence of engine.md
LC_ALL=C awk '/^## pieces/{m=1;next} /^## /{m=0} m&&/^~~~/{fz=!fz;next} m&&fz&&match($0,/^[^ ]+ +[0-9]+ B/){split($0,a," ");print a[1],a[2]}' $G/engine.md >$T/map
nh=$(wc -l <$T/heads|tr -d ' ');nm=$(wc -l <$T/map|tr -d ' ')
ok "b1-measure-finds-the-pieces the measure found $nh fenced pieces under ### headings (want >= 40) and $nm rows in the ## pieces map (want >= 30)" '[ $nh -ge 40 ]&&[ $nm -ge 30 ]'
stale=$(awk '$2!=$3{printf "%s(%s/%s) ",$1,$2,$3}' $T/heads);ns=$(awk '$2!=$3' $T/heads|wc -l|tr -d ' ')
ok "b1-headings-state-the-measured-size $ns stale heading(s) of $nh (want 0): [${stale% }]" '[ $ns = 0 ]'
off=$(awk 'NR==FNR{m[$1]=$3;next} ($1 in m)&&$2!=m[$1]{printf "%s(%s/%s) ",$1,$2,m[$1]}' $T/heads $T/map);no=$(echo "$off"|wc -w|tr -d ' ')
ok "b1-map-rows-equal-the-measured-size $no map row(s) whose size differs from the measured piece (want 0): [${off% }]" '[ $no = 0 ]'
ghost=$(awk 'NR==FNR{m[$1]=1;next} !($1 in m){printf "%s ",$1}' $T/heads $T/map);ng=$(echo "$ghost"|wc -w|tr -d ' ')
ok "b1-map-names-no-absent-piece $ng map row(s) naming a piece with no ### heading + fenced body (want 0): [${ghost% }]" '[ $ng = 0 ]'
miss=$(awk 'NR==FNR{m[$1]=1;next} !($1 in m){printf "%s ",$1}' $T/map $T/heads);nx=$(echo "$miss"|wc -w|tr -d ' ')
ok "b1-map-lists-every-piece $nx measured piece(s) absent from the map (want 0): [${miss% }]" '[ $nx = 0 ]'
for p in agi-boot agi-boot.service matrix;do ok "b1-map-lists-$p the map has a row for $p: $(awk -v p=$p '$1==p' $T/map|wc -l|tr -d ' ') (want 1)" '[ "$(awk -v p=$p "\$1==p" $T/map|wc -l|tr -d " ")" = 1 ]';done
# RB-2: the map is counted, not just measured row by row: the row count equals the `###` block count, no piece is named twice, and the stated "map of N pieces" in engine.md's title equals both
nblk=$(cat $G/engine*.md|grep -c '^### ');nrow=$nm;ndup=$(awk '{c[$1]++} END{for(k in c)if(c[k]>1)n++; print n+0}' $T/map);dups=$(awk '{c[$1]++} END{for(k in c)if(c[k]>1)printf "%s(x%s) ",k,c[k]}' $T/map)
ntitle=$(grep -m1 -o 'map of [0-9]* pieces' $G/engine.md|grep -o '[0-9]*');nt=$(grep -c 'map of [0-9]* pieces' $G/engine.md)
ok "b1-map-row-count-equals-the-block-count the ## pieces map has $nrow row(s), engine*.md has $nblk ### block(s) (want equal, both >= 40)" '[ "$nrow" = "$nblk" ]&&[ "$nblk" -ge 40 ]'
ok "b1-map-names-no-piece-twice $ndup piece name(s) listed more than once in the map (want 0): [${dups% }]" '[ $ndup = 0 ]'
ok "b1-the-title-number-equals-the-map-and-the-blocks engine.md states 'map of N pieces' $nt time(s) (want 1): N = ${ntitle:-none} (want $nrow = $nblk)" '[ "$nt" = 1 ]&&[ "$ntitle" = "$nrow" ]&&[ "$ntitle" = "$nblk" ]'
# B4 (DG1 ruling (a), 13:36Z: the line carries `ruled: no ring cell, g141-b`; the why and the owner-sign alternative live on the hypothesis node's `## DG1 RULING on B4` section): the LIMITS line of engine-grow.md and its pointer. There is NO bare `owner` grep: the line already says 'a broken owner schema', so a word count could never go red when the ruling or its alternative was deleted (the old row was vacuous).
L=$(grep -m1 'LIMITS:' $G/engine-grow.md);dg=$(grep -c 'DG1 to rule' $G/engine-grow.md);ru=$(echo "$L"|grep -cF 'ruled: no ring cell, g141-b');rg=$(echo "$L"|grep -c 'ring:')
ok "b4-the-limits-line-no-longer-asks-DG1-to-rule 'DG1 to rule' appears $dg time(s) in engine-grow.md (want 0)" '[ $dg = 0 ]'
ok "b4-the-limits-line-carries-the-ruling-and-its-pointer the LIMITS line holds the EXACT text 'ruled: no ring cell, g141-b': $ru (want 1) and still says ring: $rg (want 1 line)" '[ "$ru" = 1 ]&&[ "$rg" = 1 ]'
ptr=$(echo "$L"|sed -n 's/.*ruled: no ring cell, \([A-Za-z0-9-]*\).*/\1/p'|head -1);hy=$(ls $R0/.agi/nodes/hypothesis/$ptr-*.md 2>/dev/null);nh=$(echo "$hy"|grep -c .)
hdr=0;os=0;[ "$nh" = 1 ]&&{ hdr=$(grep -c '^## DG1 RULING on B4' "$hy");os=$(awk '/^## DG1 RULING on B4/{s=1;next} /^## |^<!-- THOUGHT:BEGIN/{s=0} s' "$hy"|grep -c 'owner-sign');}
ok "b4-the-pointer-resolves the pointer in the line is [${ptr:-none}]: $nh hypothesis file(s) .agi/nodes/hypothesis/${ptr:-?}-*.md (want 1), its '## DG1 RULING on B4' heading $hdr time(s) (want 1), the section (up to the next ## or the THOUGHT block, which also says owner-sign) names the alternative ('owner-sign') on $os line(s) (want >= 1)" '[ -n "$ptr" ]&&[ "$nh" = 1 ]&&[ "$hdr" = 1 ]&&[ "$os" -ge 1 ]'
echo "engine-sizes: $f FAIL"
exit $f
