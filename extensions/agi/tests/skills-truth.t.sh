#!/bin/sh
# skills-truth.t.sh: goal:g1.41 H (DG1 21:46Z; hypothesis:g141-h-five-skills-say-what-is-true-write-py-is-the-old-setups-writer-and-workflow-py-is-legacy): five skills stop teaching two things the owner overruled and invent no replacement: (H1) agi-goal, agi-dispatch and agi-corrective name write.py as the OLD setup's node writer (a post whose row has engine.v 4 edits node files with plain Write/Edit and agi-turn commits, owner 10-01 23:3xZ) and none says write.py is "the only writer"; (H2) agi, agi-workflow, agi-corrective and agi-dispatch mark the workflow.py route LEGACY with the owner order (retire it, 10-02 14:01Z) and goal:g5.33, and none calls it "the only sanctioned" route; the routing itself is unchanged: agi-master-gate and agi-merge-pass still run every mur through the live workflow.py.
# sh + git + grep on a git tree, no network, no root, 0 USD. Usage: sh skills-truth.t.sh [ROOT [CUT [TIP]]] (or ROOT= CUT= TIP=): ROOT = a git tree whose skills/ is read AS CHECKED OUT (the tip); CUT..TIP = the range the NEGATIVE rows diff (default HEAD..HEAD: EMPTY, and a NEGATIVE row over no commits proves nothing, so on an empty range every n-* row prints `SKIP <name> ...` and counts as a SKIP, never as ok; STRICT=1 makes it a FAIL; goal:g1.42 row 6). The same file runs on the trunk (NEG) and on a reference commit.
# Lanes: h1-* the old-writer wording (no "(the only writer)", engine.v 4 and "old setup" in agi-goal / agi-dispatch / agi-corrective); h2-* the LEGACY banner (no "only sanctioned" route; LEGACY, g5.33 and the owner order date 10-02 in agi, agi-workflow, agi-corrective, agi-dispatch); n-* the NEGATIVE: the diff adds no dispatched-round / dispatch.py run replacement, agi-master-gate and agi-merge-pass are not touched and keep their `workflow.py run` line, no routing line (workflow.py run / --harness pi-free) is removed from the four, nothing under skills/ or .claude changes but the five SKILL.md (the round's own experiment node elsewhere is fine).
# Honest limits: greps over text, not a reading of whether a banner is true; the wording of the banner is free (the lane pins the tokens the hypothesis names); whether mur should move OFF workflow.py is goal:g5.33's schedule (DG1's banked note), so no row pins a replacement route either way except its ABSENCE from the added lines.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};CUT=${CUT:-${2:-HEAD}};TIP=${TIP:-${3:-HEAD}};f=0;sk=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
S=$R0/skills;g="git -C $R0"
[ -f $S/agi/SKILL.md ]&&[ -f $S/agi-master-gate/SKILL.md ]&&$g rev-parse --verify -q $CUT^{commit} >/dev/null&&$g rev-parse --verify -q $TIP^{commit} >/dev/null||{ echo "FAIL inputs: skills $S, cut $CUT, tip $TIP";exit 99;}
# neg: a NEGATIVE row diffs CUT..TIP; with no commit in that range it checks nothing -> SKIP by name (STRICT=1: FAIL), never an ok
nr=$($g rev-list --count $CUT..$TIP)
neg(){ if [ "$nr" -gt 0 ];then ok "$@";elif [ -n "$STRICT" ];then echo "FAIL $1 (the range $CUT..$TIP is empty: a NEGATIVE row over no commits proves nothing; pass CUT and TIP)";f=$((f+1));else echo "SKIP $1 (the range $CUT..$TIP is empty: a NEGATIVE row over no commits proves nothing; pass CUT and TIP)";sk=$((sk+1));fi;}
n=$(grep -rnE 'only sanctioned workflow dispatch route|\(the only writer\)' $S --include=SKILL.md|wc -l|tr -d ' ')
ok "h-no-only-sanctioned-route-and-no-only-writer $n line(s) of 'only sanctioned workflow dispatch route' or '(the only writer)' in skills/ (want 0; the trunk has 2)" '[ $n = 0 ]'
for k in agi agi-goal agi-dispatch agi-corrective;do F=$S/$k/SKILL.md
 e=$(grep -c 'engine\.v 4' $F);o=$(grep -ci 'old[ -]setup' $F);w=$(grep -ci 'only writer' $F)
 ok "h1-$k-names-the-engine-v-4-rule $k has $e line(s) with 'engine.v 4' (want >= 1)" '[ $e -ge 1 ]'
 ok "h1-$k-names-write-py-as-the-old-setups-writer $k has $o line(s) with 'old setup' (want >= 1), $w with 'only writer' (want 0)" '[ $o -ge 1 ]&&[ $w = 0 ]';done
for k in agi agi-workflow agi-corrective agi-dispatch;do F=$S/$k/SKILL.md
 l=$(grep -c 'LEGACY' $F);g5=$(grep -c 'g5\.33' $F);d=$(grep -c '10-02' $F);one=$(grep -cE 'LEGACY.*g5\.33|g5\.33.*LEGACY' $F)
 ok "h2-$k-marks-workflow-py-LEGACY $k has $l line(s) with LEGACY (want >= 1)" '[ $l -ge 1 ]'
 ok "h2-$k-names-goal-g5-33 $k has $g5 line(s) with g5.33 (want >= 1), $one of them also with LEGACY (want >= 1)" '[ $g5 -ge 1 ]&&[ $one -ge 1 ]'
 ok "h2-$k-names-the-owner-order $k has $d line(s) with the order date 10-02 (want >= 1)" '[ $d -ge 1 ]';done
# the NEGATIVE: no invented replacement, the live route stays where it is used, nothing outside the five moves
add=$($g diff $CUT..$TIP -- skills|grep '^+'|grep -v '^+++'|grep -cE 'dispatched round|dispatch\.py run')
neg "n-no-dispatched-round-replacement-in-the-added-lines $add added line(s) in skills/ name a 'dispatched round' or 'dispatch.py run' (want 0)" '[ $add = 0 ]'
c0=$($g grep -h -c 'workflow\.py run' $CUT -- skills/agi-master-gate/SKILL.md skills/agi-merge-pass/SKILL.md|awk -F: '{s+=$NF}END{print s+0}');c1=$($g grep -h -c 'workflow\.py run' $TIP -- skills/agi-master-gate/SKILL.md skills/agi-merge-pass/SKILL.md|awk -F: '{s+=$NF}END{print s+0}')
neg "n-the-live-route-keeps-its-workflow-py-run-lines agi-master-gate + agi-merge-pass: 'workflow.py run' lines $c0 at the cut, $c1 at the tip (want equal and >= 1)" '[ "$c0" = "$c1" ]&&[ "$c0" -ge 1 ]'
t=$($g diff --name-only $CUT..$TIP -- skills/agi-master-gate skills/agi-merge-pass|wc -l|tr -d ' ')
neg "n-master-gate-and-merge-pass-are-untouched $t changed file(s) under agi-master-gate / agi-merge-pass (want 0)" '[ $t = 0 ]'
for kr in 'agi:workflow\.py run' 'agi-workflow:workflow\.py run' 'agi-corrective:workflow\.py run' 'agi-dispatch:harness pi-free';do k=${kr%%:*};re=${kr#*:};a0=$($g show $CUT:skills/$k/SKILL.md|grep -c "$re");a1=$($g show $TIP:skills/$k/SKILL.md|grep -c "$re")
 neg "n-$k-keeps-its-routing-line lines matching '$re' (the line that routes a run): $a0 at the cut, $a1 at the tip (want tip >= cut >= 1: a banner labels the route, it does not remove it)" '[ $a1 -ge $a0 ]&&[ $a0 -ge 1 ]';done
odd=$($g diff --name-only $CUT..$TIP -- skills .claude|grep -vE '^skills/(agi|agi-workflow|agi-corrective|agi-dispatch|agi-goal)/SKILL\.md$'|tr '\n' ' ')
neg "n-only-the-five-skills-change files changed under skills/ or .claude outside the five SKILL.md: [${odd% }] (want none)" '[ -z "$odd" ]'
# RH1 (DG1 23:05Z/23:11Z): skills/agi/SKILL.md still teaches "write.py is the ONE writer" in four places without the old-setup label the owner order of 10-01 23:3xZ calls for. The heading text is a CONSUMER KEY (rolslice.py matches it verbatim to cut the role slices), so the rows keep it UNCHANGED and pin the label NEXT TO it: 'old setup' (case-insensitive) on the heading line or within the next 3 lines, and on (or within the 3 lines above) each of the three claim lines. A claim line that no longer exists passes: the rule is "labelled or gone".
A=$S/agi/SKILL.md;H='Every node edit goes through `write.py`'
RK=$($g show $TIP:extensions/agi/bin/rolslice.py 2>/dev/null|grep -o 'Every node edit goes through `write.py`'|head -1);[ -n "$RK" ]||RK=$H
hn=$(grep -nF "## $RK" $A|head -1|cut -d: -f1)
ok "rh1-the-section-heading-is-unchanged the heading line '## $RK' (the key rolslice.py cuts the role slices by): $(grep -cF "## $RK" $A) line(s) in skills/agi/SKILL.md (want 1)" '[ "$(grep -cF "## $RK" $A)" = 1 ]'
lab=0;[ -n "$hn" ]&&lab=$(sed -n "${hn},$((hn+3))p" $A|grep -ci 'old[ -]setup')
ok "rh1-the-heading-carries-the-old-setup-label 'old setup' on the heading line (at $hn) or the 3 lines after it: $lab line(s) (want >= 1)" '[ -n "$hn" ]&&[ $lab -ge 1 ]'
claim(){ nm=$1;pat=$2;ln=$(grep -nF "$pat" $A|head -1|cut -d: -f1)
 if [ -z "$ln" ];then ok "rh1-$nm-is-labelled-or-gone the line holding [$pat] is gone" 'true';return;fi
 lo=$((ln-3));[ $lo -ge 1 ]||lo=1;c=$(sed -n "${lo},${ln}p" $A|grep -ci 'old[ -]setup')
 ok "rh1-$nm-is-labelled-or-gone the line holding [$pat] (line $ln): 'old setup' on it or the 3 lines above: $c line(s) (want >= 1)" '[ $c -ge 1 ]';}
claim the-prime-row-line 'through the ONE writer (write.py'
claim the-one-way-in-line 'One way in'
claim the-anything-but-write-py-stop-line 'anything but `write.py`, stop'
echo "skills-truth: $f FAIL ($sk SKIP)"
exit $f
