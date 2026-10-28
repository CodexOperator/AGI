#!/bin/sh
# recompose.t.sh: goal:g7.16.1.11.46.17 (G1b-1) -- posts/P recomposed as a VIEW from refs/grid/node tips, read-only, diff 0 against posts/P.
# sh + git + python3 on a SCRATCH repo. The fixture trunk refs/heads/posts/belam carries:
#   carried README.md src/a.txt | n1 idea (plain) | n2 idea DEPRECATED (deprecated/idea/) | b3 build + payload src/p3.txt | b4 build DEPRECATED, payload retired
#   (absent on both sides) | t5 a LEGACY path (.agi/nodes/task/t-005-long-name.md for task:t-005, placed by the map) | the map config:legacy-paths
# and the grid also holds g6 (a GHOST: a second ref carrying idea:n1, named never-composed by the map) and n7 (never landed: no live path,
# named by the map's '<mint> never-landed' row: goal:g7.16.1.11.46.18 T11, membership from the grid). Rows 5-7 of .46.18 (T11-T13, U2) are
# the t11*/t12*/t13*/u2* rows below. Every mutant (m-*) must read RED.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;nrows=0;G=/usr/bin/git;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};BIN=${BIN:-$R0/extensions/agi/bin}
ok(){ nrows=$((nrows+1));if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
printf '[user]\n\tname=t\n\temail=t@t\n[commit]\n\tgpgsign=false\n[safe]\n\tdirectory=*\n' >$T/gitconfig;export GIT_CONFIG_GLOBAL=$T/gitconfig GIT_CONFIG_SYSTEM=/dev/null PYTHONDONTWRITEBYTECODE=1
TR=refs/heads/posts/belam;NS=refs/grid/node;VIEW=refs/view/posts/belam
mut(){ python3 - "$1" "$2" "$3" <<'PY'
import sys
s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3]
assert s.count(a)==1,("mutant anchor",a)
open(sys.argv[1],"w").write(s.replace(a,b))
PY
}
mn(){ printf '%032x' $1;}
nd(){ printf -- '---\nid: %s\nmint_id: %s\ntype: %s\nstatus: %s\n%s---\n# node\n%s\n' "$1" "$2" "$3" "$4" "$5" "$6";}   # id mint type status extra-fm body
blob(){ $G -C $P hash-object -w --stdin;}
gc(){ tr_=$1;shift;echo "v $*"|$G -C $P commit-tree $tr_ ${1:+-p $1};}                          # a grid commit: tree [parent]
gt(){ b=$(printf '%s' "$1"|blob);if [ -n "$2" ];then pb=$(printf '%s' "$2"|blob);printf '100644 blob %s\tnode.md\n100644 blob %s\tpayload\n' $b $pb;else printf '100644 blob %s\tnode.md\n' $b;fi|$G -C $P mktree;}
put(){ mkdir -p $P/$(dirname $1);printf '%s' "$2" >$P/$1;}
rc(){ (cd $P&&python3 extensions/agi/bin/recompose.py --trunk $TR "$@");}
mkfix(){ P=$1;rm -rf $P;mkdir -p $P/extensions/agi;$G init -q $P;cp -r $BIN $P/extensions/agi/bin;cp -r ${SRC:-$R0/extensions/agi/src} $P/extensions/agi/src;find $P/extensions/agi -name __pycache__ -prune -exec rm -rf {} +
 N1=$(nd idea:n1 $(mn 1) idea active '' one);N2=$(nd idea:n2 $(mn 2) idea deprecated '' two);B3=$(nd build:b3 $(mn 3) build active 'payload_ref: src/p3.txt\n' three)
 B4=$(nd build:b4 $(mn 4) build deprecated 'payload_ref: gone.txt\n' four);T5=$(nd task:t-005 $(mn 5) task active '' five);G6=$(nd idea:n1 $(mn 6) idea active '' ghost)
 N7=$(nd idea:n7 $(mn 7) idea active '' never);MAP=$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
$(mn 7) never-landed")
 B3=$(printf '%b' "$B3");B4=$(printf '%b' "$B4")
 put README.md readme;put src/a.txt aaa;put src/p3.txt PAY3;put .agi/nodes/idea/n1.md "$N1";put .agi/nodes/deprecated/idea/n2.md "$N2";put .agi/nodes/build/b3.md "$B3"
 put .agi/nodes/deprecated/build/b4.md "$B4";put .agi/nodes/task/t-005-long-name.md "$T5";put .agi/nodes/.geometry/legacy-paths.md "$MAP"
 $G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm trunk;$G -C $P update-ref $TR HEAD
 for i in 1 2 4 5 6 7 8;do eval "x=\$$(echo N1 N2 _ B4 T5 G6 N7 MAP|cut -d' ' -f$i)";$G -C $P update-ref $NS/$(mn $i) $(gc $(gt "$x"));done
 $G -C $P update-ref $NS/$(mn 3) $(gc $(gt "$B3" PAY3));}
mkfix $T/base;P=$T/base
cp_(){ rm -rf $T/$1;cp -a $T/base $T/$1;P=$T/$1;}
# --- g0: the whole view, diff 0
cp_ g0;tr0=$($G -C $P rev-parse $TR);rc --write >$T/g0.out 2>&1;g0=$?
ok "g0-the-view-is-diff-0-and-written rc $g0; the view ref holds the trunk's tree, posts/belam unmoved: $(grep 'sets:\|diff vs' $T/g0.out|tr '\n' '|'|cut -c1-220)" '[ $g0 = 0 ]&&grep -q "diff vs the trunk [0-9a-f]*: 0 path(s)" $T/g0.out&&[ "$($G -C $P rev-parse $VIEW^{tree})" = "$($G -C $P rev-parse $TR^{tree})" ]&&[ "$($G -C $P rev-parse $TR)" = "$tr0" ]'
# T1: the three sets named, each with its size; a trunk node path no ref composes is unread BY NAME, never filled from the trunk
ok "t1a-the-sets-are-named-with-sizes node 6 composed of 6 trunk node paths, payload 1 (+1 retired), carried 2 (README.md, src/a.txt; recompose.py's own files ride as carried in the fixture too)" 'grep -q "sets: node 6 composed of 6 trunk node paths, payload 1 (+1 retired, absent on both sides), carried" $T/g0.out'
cp_ t1;$G -C $P update-ref -d $NS/$(mn 1);rc >$T/t1.out 2>&1;t1=$?
ok "t1b-a-node-path-with-no-grid-ref-is-unread n1's ref deleted: rc $t1, 'unread .agi/nodes/idea/n1.md (no grid ref composes' and NO diff 0" '[ $t1 = 1 ]&&grep -q "unread .agi/nodes/idea/n1.md (no grid ref composes this node path" $T/t1.out'
cp_ t1m;mut $P/extensions/agi/bin/recompose.py '    carried = [p for p in ptree if not is_node_path(p) and p not in pay]' '    carried = [p for p in ptree if (not is_node_path(p) or p not in composed) and p not in pay]
    unread = [u for u in unread if "no grid ref composes" not in u]';$G -C $P update-ref -d $NS/$(mn 1);rc >$T/t1m.out 2>&1;t1m=$?
ok "m-filled-from-the-trunk-reads-RED a node path with no ref filled from the trunk reads diff 0, rc $t1m (want rc 1 + unread, so rc 0 = caught)" '[ $t1m = 0 ]'
# T2: a grid tip AHEAD of the trunk: the tip is composed, the mint printed
cp_ t2;x=$($G -C $P rev-parse $NS/$(mn 1));$G -C $P update-ref $NS/$(mn 1) $(gc $(gt "$(nd idea:n1 $(mn 1) idea active '' one-v2)") $x);rc >$T/t2.out 2>&1;t2=$?
ok "t2-a-tip-ahead-composes-the-tip-and-names-its-mint rc $t2: $(grep AHEAD $T/t2.out|cut -c1-120)" '[ $t2 = 1 ]&&grep -q "AHEAD $(mn 1) .agi/nodes/idea/n1.md: the grid tip" $T/t2.out&&grep -q "M	.agi/nodes/idea/n1.md" $T/t2.out'
cp_ t2m;mut $P/extensions/agi/bin/recompose.py '        entries.append(("100644", nodesha[p], p))' '        nodesha[p] = ptree[p][1]; entries.append(("100644", nodesha[p], p))';x=$($G -C $P rev-parse $NS/$(mn 1));$G -C $P update-ref $NS/$(mn 1) $(gc $(gt "$(nd idea:n1 $(mn 1) idea active '' one-v2)") $x);rc >$T/t2m.out 2>&1;t2m=$?
ok "m-node-bytes-from-the-trunk-reads-RED composing node bytes from the trunk hides the tip ahead: rc $t2m, no AHEAD line (want both, so rc 0 = caught)" '[ $t2m = 0 ]&&! grep -q AHEAD $T/t2m.out'
# T3: a ref at a missing object is unread by name, rc 1
cp_ t3;mkdir -p $P/.git/$NS;echo 1234567890abcdef1234567890abcdef12345678 >$P/.git/$NS/$(mn 2);rc >$T/t3.out 2>&1;t3=$?
ok "t3-a-ref-at-a-missing-object-is-unread n2's ref names an absent object: rc $t3, 'unread $(mn 2) (its grid ref ... not a readable commit)'" '[ $t3 = 1 ]&&grep -q "unread $(mn 2) (its grid ref $NS/$(mn 2) names 1234567890ab, not a readable commit)" $T/t3.out'
cp_ t3m;mut $P/extensions/agi/bin/recompose.py '        if not k.endswith("missing") and k.split()[1:2] == ["commit"]:' '        if True:';mkdir -p $P/.git/$NS;echo 1234567890abcdef1234567890abcdef12345678 >$P/.git/$NS/$(mn 2);rc >$T/t3m.out 2>&1
ok "m-ref-kind-check-cut-reads-RED without the object check the missing ref is never named as one (want 'not a readable commit', so its absence = caught)" '! grep -q "not a readable commit" $T/t3m.out'
# T4: a retired node recomposes into .agi/nodes/deprecated/<type>/ (g0 holds n2 and b4 there); mutant: the deprecated/ prefix dropped
cp_ t4m;mut $P/extensions/agi/bin/recompose.py '    return live.replace(".agi/nodes/", ".agi/nodes/deprecated/", 1) if fm.get("status") == "deprecated" else live' '    return live';rc >$T/t4m.out 2>&1;t4m=$?
ok "m-deprecated-into-the-live-dir-reads-RED a retired node composed into the live type dir: rc $t4m, n2's deprecated/ path unread (want diff 0, so rc 1 = caught)" '[ $t4m = 1 ]&&grep -q "unread .agi/nodes/deprecated/idea/n2.md" $T/t4m.out'
# T6 (falsifier 1's mutant): one node's grid commit dropped, its blob differing from its parent's -> the tree differs, RED, the mint printed
cp_ t6;x=$($G -C $P rev-parse $NS/$(mn 1));y=$(gc $(gt "$(nd idea:n1 $(mn 1) idea active '' one)") $(gc $(gt "$(nd idea:n1 $(mn 1) idea active '' one-v0)")));$G -C $P update-ref $NS/$(mn 1) $y;rc >/dev/null 2>&1;g6a=$?
$G -C $P update-ref $NS/$(mn 1) $($G -C $P rev-parse $y^);rc >$T/t6.out 2>&1;t6=$?
ok "t6-a-dropped-grid-commit-reads-RED with its own blob in place rc $g6a (GREEN); its last commit dropped (the trunk's blob is on no version of the ref: BEHIND, .46.18 T12) rc $t6, the path and mint named: $(grep -E 'BEHIND|M	' $T/t6.out|head -1|cut -c1-90)" '[ $g6a = 0 ]&&[ $t6 = 1 ]&&grep -q "BEHIND $(mn 1) .agi/nodes/idea/n1.md (trunk bytes not on the grid)" $T/t6.out'
# T7: the view ref lives outside refs/heads/posts/, refs/box/, refs/held/ and refs/grid/
cp_ t7;for v in refs/heads/posts/x refs/box/a/b refs/held/a/b refs/grid/v/node/x;do rc --view $v --write >$T/t7.$$.out 2>&1||echo "$v $?";done >$T/t7.out
ok "t7-the-view-ref-is-refused-in-the-four-namespaces each of refs/heads/posts/, refs/box/, refs/held/, refs/grid/<v>/node/ refused rc 1, nothing written; the default $VIEW matches none" '[ $(grep -c " 1$" $T/t7.out) = 4 ]&&[ -z "$($G -C $P for-each-ref refs/grid/v refs/box refs/held refs/heads/posts/x)" ]'
cp_ t7m;mut $P/extensions/agi/bin/recompose.py 'VIEW_FORBIDDEN = ("refs/heads/posts/", "refs/box/", "refs/held/", "refs/grid/")' 'VIEW_FORBIDDEN = ()';rc --view refs/grid/v/node/x --write >/dev/null 2>&1
ok "m-view-namespace-check-cut-reads-RED the check cut writes the view under refs/grid/v/node/ (want refused, so the ref = caught)" '[ -n "$($G -C $P for-each-ref refs/grid/v)" ]'
# T8: the trunk read once and printed; refs with no live path counted and named, never written; the ghost never composed
ok "t8-one-trunk-sha-orphans-counted-ghost-named the trunk sha printed once, 1 ref with no live path ($(mn 7)) named, 1 never-composed, 1 placed by the map, and none in the tree" '[ $(grep -c "^recompose: trunk $TR = $tr0$" $T/g0.out) = 1 ]&&grep -q "1 with no live path, 1 never-composed (map), 1 placed by the legacy map" $T/g0.out&&grep -q "no live path $(mn 7)" $T/g0.out&&v8=$($G -C $T/g0 ls-tree -r --name-only $VIEW)&&[ -n "$v8" ]&&! echo "$v8"|grep -q n7'
# T9: a build node's payload is NODE-owned: dropped from its tip -> unread by mint
cp_ t9;$G -C $P update-ref $NS/$(mn 3) $(gc $(gt "$(printf '%b' "$(nd build:b3 $(mn 3) build active 'payload_ref: src/p3.txt\n' three)")"));rc >$T/t9.out 2>&1;t9=$?
ok "t9-a-payload-dropped-from-its-tip-is-unread b3's tip without its payload, the trunk holding src/p3.txt: rc $t9, unread $(mn 3)" '[ $t9 = 1 ]&&grep -q "unread $(mn 3) (its tip carries no payload, but the trunk has src/p3.txt)" $T/t9.out'
cp_ t9m;mut $P/extensions/agi/bin/recompose.py '            if ref in ptree:' '            if False:';$G -C $P update-ref $NS/$(mn 3) $(gc $(gt "$(printf '%b' "$(nd build:b3 $(mn 3) build active 'payload_ref: src/p3.txt\n' three)")"));rc >$T/t9m.out 2>&1
ok "m-payload-carried-from-the-trunk-reads-RED a dropped payload counted as retired: no unread line on $(mn 3) (want one, so none = caught)" '! grep -q "unread $(mn 3)" $T/t9m.out'
# the legacy map: read from ITS grid tip; a ghost with no map row, a duplicate row, a needless row, a new non-derivable node -> unread
cp_ k1;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md")"));rc >$T/k1.out 2>&1;k1=$?
ok "k1-a-ghost-the-map-does-not-name-is-unread without g6's never-composed row: rc $k1, n1's path claimed by 2 refs, unread by name" '[ $k1 = 1 ]&&grep -q "unread .agi/nodes/idea/n1.md (claimed by 2 grid refs: $(mn 1) $(mn 6))" $T/k1.out'
cp_ k2;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 5) never-composed")"));rc >$T/k2.out 2>&1;k2=$?
ok "k2-a-map-naming-one-mint-twice-is-unread rc $k2" '[ $k2 = 1 ]&&grep -q "names mint $(mn 5) twice" $T/k2.out'
cp_ k3;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
$(mn 1) .agi/nodes/idea/n1.md")"));rc >$T/k3.out 2>&1;k3=$?
ok "k3-a-map-row-at-the-derived-path-is-unread a row the derivation already gives (n1) is refused: rc $k3" '[ $k3 = 1 ]&&grep -q "row $(mn 1): .agi/nodes/idea/n1.md is the derived path" $T/k3.out'
cp_ k4;put .agi/nodes/task/t-009-another-long-name.md "$(nd task:t-009 $(mn 9) task active '' nine)";$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm new;$G -C $P update-ref $TR HEAD
$G -C $P update-ref $NS/$(mn 9) $(gc $(gt "$(nd task:t-009 $(mn 9) task active '' nine)"));rc >$T/k4.out 2>&1;k4=$?
ok "k4-a-NEW-non-derivable-node-is-unread a node minted after the map at a non-derivable path is never placed: rc $k4, its path unread, its ref with no live path" '[ $k4 = 1 ]&&grep -q "unread .agi/nodes/task/t-009-another-long-name.md (no grid ref composes" $T/k4.out'
cp_ k5;put .agi/nodes/.geometry/legacy-paths.md "$(nd config:legacy-paths $(mn 8) config active '' 'map (the trunk edit)')";$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm edit;$G -C $P update-ref $TR HEAD;rc >$T/k5.out 2>&1;k5=$?
ok "k5-the-map-is-read-from-its-grid-tip a trunk edit of the map file (no grid version): the view composes the grid's map, so the trunk's file differs (rc $k5), BEHIND (its bytes are on no grid version, .46.18 T12), and t5 is still placed" '[ $k5 = 1 ]&&grep -q "BEHIND $(mn 8) .agi/nodes/.geometry/legacy-paths.md (trunk bytes not on the grid)" $T/k5.out&&grep -q "1 placed by the legacy map" $T/k5.out'
# a map row is never skipped: an unparseable body line is unread; a mint that is not 32 hex (31-hex mints exist) is placed like any other
cp_ k6;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
a stray line in the body")"));rc >$T/k6.out 2>&1;k6=$?
ok "k6-an-unparseable-map-line-is-unread rc $k6 (never skipped)" '[ $k6 = 1 ]&&grep -q "body line .a stray line in the body. is not" $T/k6.out'
cp_ k6m;mut $P/extensions/agi/bin/recompose.py "            return [], f\"{LEGACY_MAP_ID} body line" "            continue
            return [], f\"{LEGACY_MAP_ID} body line";$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
a stray line in the body")"));rc >$T/k6m.out 2>&1;k6m=$?
ok "m-unparseable-map-line-skipped-reads-RED skipping the line names no body line and reads the map as placed (want the unread line, so its absence = caught; rc $k6m is the map tip AHEAD of the trunk, as in k5)" '! grep -q "body line" $T/k6m.out&&grep -q "1 placed by the legacy map" $T/k6m.out'
cp_ k7;s31=a00dc51bea8483af1000000000000ff;T31=$(nd task:t-031 $s31 task active '' thirtyone);put .agi/nodes/task/t-031-short-mint.md "$T31";$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm m31;$G -C $P update-ref $TR HEAD
$G -C $P update-ref $NS/$s31 $(gc $(gt "$T31"));$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
$(mn 7) never-landed
$s31 .agi/nodes/task/t-031-short-mint.md")"));rc >$T/k7.out 2>&1;k7=$?
ok "k7-a-31-hex-mint-row-is-placed the live repo carries 31-hex mints (a00dc51bea8483af1000000000000ff): its row places its path: 2 placed by the map, no unread line (rc $k7 = the map tip AHEAD of the trunk only)" 'grep -q "2 placed by the legacy map" $T/k7.out&&! grep -q "^  unread" $T/k7.out&&[ "$(grep -c "^recompose:   [ADM]	" $T/k7.out)" = 1 ]&&grep -q "M	.agi/nodes/.geometry/legacy-paths.md" $T/k7.out'
# (i) aio 05:20:25Z: a PATH row is LIVE-form; deprecated/ comes from status. Retire the mapped t5 THROUGH node_writer.retire_node -> it composes at
# deprecated/<the same path>, diff 0, the map unchanged
rt(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/recompose.py "$1" "$2";shift 2;done
 (cd $P/extensions/agi/bin&&python3 -c "import sys,node_writer as w;from pathlib import Path;r=w.retire_node(Path('$P/.agi'),'task:t-005',note='lane');print(r.status,r.reason)") >$T/$OUT.rt 2>&1
 $G -C $P add -A .agi/nodes >/dev/null 2>&1;$G -C $P commit -qm retire;$G -C $P update-ref $TR HEAD
 x=$($G -C $P rev-parse $NS/$(mn 5));$G -C $P update-ref $NS/$(mn 5) $(gc $($G -C $P rev-parse HEAD:.agi/nodes/deprecated/task/t-005-long-name.md|xargs -I{} printf '100644 blob {}\tnode.md\n'|$G -C $P mktree) $x);rc >$T/$OUT.out 2>&1;}
OUT=r1;rt r1;r1=$?;m8=$($G -C $T/base rev-parse $NS/$(mn 8))
ok "i-a-retired-mapped-node-composes-at-deprecated-same-path retire_node moved t5 ($(head -c60 $T/r1.rt)) and the view composes it at deprecated/task/t-005-long-name.md: diff 0, 1 placed by the map, the map ref unchanged" 'grep -q "^recompose: diff vs the trunk [0-9a-f]*: 0 path(s)" $T/r1.out&&grep -q "1 placed by the legacy map" $T/r1.out&&[ "$($G -C $T/r1 rev-parse $NS/$(mn 8))" = "$m8" ]&&$G -C $T/r1 cat-file -e $TR:.agi/nodes/deprecated/task/t-005-long-name.md'
OUT=r1m;rt r1m '        p = placed(lmap[m], fm) if m in lmap else derived_path(fm)' '        p = lmap[m] if m in lmap else derived_path(fm)'
ok "m-prefix-from-the-row-reads-RED the mapped path taken from the row as is: the retired t5's path unread by name (want diff 0, so the unread = caught)" 'grep -q "unread .agi/nodes/deprecated/task/t-005-long-name.md (no grid ref composes" $T/r1m.out'
# T10 alive: ONE path rule (node_writer.node_dir, NODE_HOME config -> .geometry): a config node minted after the map composes at .geometry/<slug>.md with NO row
tn(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/recompose.py "$1" "$2";shift 2;done;C9=$(nd config:c9 $(mn 9) config active '' nine)
 put .agi/nodes/.geometry/c9.md "$C9";$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm c9;$G -C $P update-ref $TR HEAD;$G -C $P update-ref $NS/$(mn 9) $(gc $(gt "$C9"));rc >$T/$OUT.out 2>&1;}
OUT=t10;tn t10;t10=$?
ok "t10-a-new-config-node-derives-under-node_dir config:c9 at .geometry/c9.md composes with no map row: rc $t10, diff 0" '[ $t10 = 0 ]&&grep -q "diff vs the trunk [0-9a-f]*: 0 path(s)" $T/t10.out'
OUT=t10m;tn t10m "    return f\"{node_dir('.agi', typ).as_posix()}/{nid.split(':', 1)[1]}.md\"" "    return f\".agi/nodes/{typ}/{nid.split(':', 1)[1]}.md\""
ok "m-derivation-without-NODE_HOME-reads-RED the type dir spelled a second time (no NODE_HOME): c9's path unread and its mint with no live path (want diff 0, so both = caught)" 'grep -q "unread .agi/nodes/.geometry/c9.md" $T/t10m.out&&grep -q "no live path $(mn 9)" $T/t10m.out'
# ref names after refs/grid/node/ are taken VERBATIM, a slash included (refs/grid/node/hyp/a00-1467544f-chain-600hop is live): a slashed ghost row is admitted, a slashed never-landed ref printed whole
cp_ sl;$G -C $P update-ref $NS/hyp/g-slash $(gc $(gt "$(nd idea:n1 hyp/g-slash idea active '' slashghost)"));$G -C $P update-ref $NS/hyp/n-slash $(gc $(gt "$(nd idea:n-slash hyp/n-slash idea active '' slashnever)"))
$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$($G -C $P show $TR:.agi/nodes/.geometry/legacy-paths.md)
hyp/g-slash never-composed
hyp/n-slash never-landed"));printf '%s\nhyp/g-slash never-composed\nhyp/n-slash never-landed\n' "$($G -C $P show $TR:.agi/nodes/.geometry/legacy-paths.md)" >$P/.agi/nodes/.geometry/legacy-paths.md;$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm sl;$G -C $P update-ref $TR HEAD
$G -C $P update-ref $NS/$(mn 8) $(gc $($G -C $P rev-parse HEAD:.agi/nodes/.geometry/legacy-paths.md|xargs -I{} printf '100644 blob {}\tnode.md\n'|$G -C $P mktree));rc >$T/sl.out 2>&1;sl=$?
ok "s1-slashed-ref-names-are-taken-verbatim rc $sl: the slashed ghost row admitted (2 never-composed), the slashed never-landed ref printed whole as 'no live path hyp/n-slash'" '[ $sl = 0 ]&&grep -q "2 never-composed (map)" $T/sl.out&&grep -q "no live path hyp/n-slash$" $T/sl.out'
# sp 05:21:35Z: the trunk's one QUOTED id + mint_id node composes at its derived path
qq(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/recompose.py "$1" "$2";shift 2;done;Q=$(printf -- '---\nid: "idea:q1"\nmint_id: "%s"\ntype: idea\nstatus: active\n---\n# quoted\n' $(mn 10))
 put .agi/nodes/idea/q1.md "$Q";$G -C $P add -A >/dev/null 2>&1;$G -C $P commit -qm q;$G -C $P update-ref $TR HEAD;$G -C $P update-ref $NS/$(mn 10) $(gc $(gt "$Q"));rc >$T/$OUT.out 2>&1;}
OUT=q1;qq q1;q1=$?
ok "q1-a-quoted-id-and-mint-compose rc $q1, diff 0" '[ $q1 = 0 ]&&grep -q "diff vs the trunk [0-9a-f]*: 0 path(s)" $T/q1.out'
OUT=q1m;qq q1m "            fm[m.group(1)] = m.group(2).strip().strip('\"').strip(\"'\")" "            fm[m.group(1)] = m.group(2).strip()"
ok "m-quotes-kept-reads-RED quotes kept in the id: the quoted node's path unread by name (want diff 0, so the unread = caught)" 'grep -q "unread .agi/nodes/idea/q1.md" $T/q1m.out'
cp_ k8;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "prose with no rows heading
$(mn 5) .agi/nodes/task/t-005-long-name.md")"));rc >$T/k8.out 2>&1;k8=$?
ok "k8-a-map-without-ONE-rows-section-is-unread rc $k8: no '## rows' heading = unread, never 0 rows" '[ $k8 = 1 ]&&grep -q "carries 0 .## rows. sections" $T/k8.out'
# goal:g7.16.1.11.46.18 row 5, T11 (sp 05:17:22Z + 05:16:17Z): MEMBERSHIP from the grid. `git rm` one live node file on the trunk -> unread <its mint>,
# never a silent diff 0; mutant: membership read from the trunk listing (a ref with no live path tolerated) -> diff 0
t11(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/recompose.py "$1" "$2";shift 2;done
 $G -C $P rm -q .agi/nodes/idea/n1.md;$G -C $P commit -qm drop;$G -C $P update-ref $TR HEAD;rc >$T/$OUT.out 2>&1;}
OUT=t11;t11 t11;t11=$?
ok "t11-a-dropped-live-node-is-unread-by-mint n1's file git-rm'd on the trunk: rc $t11, 'unread $(mn 1) (no live path ...)', never diff 0 alone" '[ $t11 = 1 ]&&grep -q "unread $(mn 1) (no live path .agi/nodes/idea/n1.md and no .$(mn 1) never-landed. row" $T/t11.out'
OUT=t11m;t11 t11m '                          for m in ms if m not in never)' '                          for m in ms if False)';t11m=$?
ok "m-membership-from-the-trunk-listing-reads-RED the never-landed check cut: the dropped node reads diff 0, rc $t11m (want unread rc 1, so rc 0 = caught)" '[ $t11m = 0 ]&&grep -q "diff vs the trunk [0-9a-f]*: 0 path(s)" $T/t11m.out'
cp_ t11b;$G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$(nd config:legacy-paths $(mn 8) config active '' "## rows
$(mn 5) .agi/nodes/task/t-005-long-name.md
$(mn 6) never-composed
$(mn 7) never-landed
$(mn 2) never-landed")"));rc >$T/t11b.out 2>&1;t11b=$?
ok "t11b-a-never-landed-row-on-a-live-node-is-unread n2 (live, deprecated/) named never-landed: rc $t11b (as k3: the row is removed in the land that lands its node)" '[ $t11b = 1 ]&&grep -q "unread $(mn 2) (a .$(mn 2) never-landed. row in config:legacy-paths, but it composes the live path .agi/nodes/deprecated/idea/n2.md)" $T/t11b.out'
# row 6, T12 (sp 05:50:03Z): AHEAD only when the trunk's blob is an EARLIER version on the mint's ref (t2), else BEHIND (t6, k5); mutant: label by inequality alone
cp_ t12m;mut $P/extensions/agi/bin/recompose.py '        elif ptree[p][1] in set(batch_sha([f"{c}:node.md" for c in hist])):' '        elif True:';$G -C $P update-ref $NS/$(mn 1) $(gc $(gt "$(nd idea:n1 $(mn 1) idea active '' one-v0)"));rc >$T/t12m.out 2>&1
ok "m-ahead-by-inequality-alone-reads-RED n1's ref at a version that never held the trunk's bytes is labelled AHEAD (want BEHIND, so AHEAD = caught)" 'grep -q "AHEAD $(mn 1)" $T/t12m.out&&! grep -q BEHIND $T/t12m.out'
# row 7, T13 (sp 05:50:03Z) + U2 (sp 07:18:02Z): the map's PATH rows are frozen at its FIRST grid version; membership rows are not path rows.
# A second map version (parent = the first) adds ROW; n9 = a node minted after the map at a non-derivable path, with its ref.
mv(){ cp_ $1;shift;while [ $# -ge 2 ];do mut $P/extensions/agi/bin/recompose.py "$1" "$2";shift 2;done;x=$($G -C $P rev-parse $NS/$(mn 8))
 $G -C $P update-ref $NS/$(mn 9) $(gc $(gt "$(nd task:t-009 $(mn 9) task active '' nine)"))
 $G -C $P update-ref $NS/$(mn 8) $(gc $(gt "$($G -C $P show $x:node.md)
$ROW") $x);rc >$T/$OUT.out 2>&1;}
ROW="$(mn 9) .agi/nodes/task/t-009-late.md";OUT=t13;mv t13;t13=$?
ok "t13-a-path-row-added-after-the-freeze-is-unread a second map version adds one PATH row: rc $t13, 'row added after the freeze $(mn 9)'" '[ $t13 = 1 ]&&grep -q "unread $(mn 9) (row added after the freeze $(mn 9):" $T/t13.out'
OUT=t13m;mv t13m '        unread.extend(added)' '        pass';t13m=$?
ok "m-freeze-check-cut-reads-RED the added path row is admitted: no 'row added after the freeze' line, rc $t13m (want the unread line, so its absence = caught)" '! grep -q "row added after the freeze" $T/t13m.out'
ROW="$(mn 9) never-landed";OUT=u2;mv u2;u2=$?
ok "u2-a-membership-row-added-after-the-freeze-passes a second map version adds '$(mn 9) never-landed' (T11's freeze version): rc $u2, diff 0 besides the map's own AHEAD path, no unread" '! grep -q "^  unread" $T/u2.out&&grep -q "AHEAD $(mn 8)" $T/u2.out&&[ "$(grep -c "^recompose:   [ADM]	" $T/u2.out)" = 1 ]'
OUT=u2m;mv u2m '    at_first = {(m, w) for m, w in rows if w != "never-landed"}' '    at_first = {(m, w) for m, w in rows}' '        added, problem = frozen_problems(tips[map_mint], {**lmap, **{m: "never-composed" for m in ghosts}})' '        added, problem = frozen_problems(tips[map_mint], {**lmap, **{m: "never-composed" for m in ghosts}, **{m: "never-landed" for m in never}})';u2m=$?
ok "m-freeze-over-all-rows-reads-RED T13 over EVERY row: T11's own never-landed freeze row reads 'row added after the freeze' (want it admitted, so the line = caught)" 'grep -q "unread $(mn 9) (row added after the freeze $(mn 9)" $T/u2m.out'
# U2 as CORRECTED (sp [correction] 07:55:06Z, 3/3 alive 07:56:52Z): never-composed rows are frozen too (a ghost mint is dropped before any claim, so
# T11 never sees it): a later map version adding '<n9> never-composed' for a fresh no-live-path ref -> 'row added after the freeze'; mutant (2): T13 over path rows only -> it passes
ROW="$(mn 9) never-composed";OUT=u2b;mv u2b;u2b=$?
ok "u2b-a-ghost-row-added-after-the-freeze-is-unread a second map version adds '$(mn 9) never-composed' for a fresh ref with no live path: rc $u2b, 'row added after the freeze $(mn 9)'" '[ $u2b = 1 ]&&grep -q "unread $(mn 9) (row added after the freeze $(mn 9):" $T/u2b.out'
OUT=u2bm;mv u2bm '        added, problem = frozen_problems(tips[map_mint], {**lmap, **{m: "never-composed" for m in ghosts}})' '        added, problem = frozen_problems(tips[map_mint], lmap)';u2bm=$?
ok "m-freeze-over-path-rows-only-reads-RED T13 over PATH rows only: the added ghost row passes with no unread line, rc $u2bm (want 'row added after the freeze', so its absence = caught; T11 is bypassed)" '! grep -q "row added after the freeze" $T/u2bm.out&&! grep -q "^  unread" $T/u2bm.out'
echo "recompose: $nrows rows";echo "recompose: $f FAIL";[ $f = 0 ]
