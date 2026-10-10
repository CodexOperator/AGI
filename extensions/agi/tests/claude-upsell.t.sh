#!/bin/sh
# claude-upsell.t.sh: goal:g7.16.1.11.36 -- every claude post start pre-answers Claude Code's one-time "fullscreen renderer" dialog by setting fullscreenUpsellSeenCount to 3 in the post home's .claude.json.
# sh + jq on a SCRATCH HOME, no claude, no network. The step is the ONE line of the agi-run piece (sect agi-run of ROOT's .geometry/engine*.md; AGIRUN=<file> tests another piece) that names the key, run as the post's start would: env -i, HOME=<scratch>, H=<harness>.
# Cases: a fresh home -> the file holds only the key, 3, mode 600 · b a second run leaves it byte-identical · c other keys + count 1 -> 3, every other key survives (jq -S del equal) · c2 an absent key beside other keys · c3 a non-number count -> 3 ·
#   d count 3 and 5 -> bytes AND mtime unchanged (not rewritten) · e an unparsable file / a non-object -> byte-identical, step exits 0 · f a pi harness (H=node) touches nothing · g no temp file left behind · h the step names no other .claude.json key (falsifier 3).
# One ok/FAIL line per case; exit = FAIL count.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
[ -n "$AGIRUN" ]||{ sect agi-run>$T/agi-run;AGIRUN=$T/agi-run;}
grep -F fullscreenUpsellSeenCount $AGIRUN>$T/step;n=$(wc -l<$T/step|tr -d ' ')
[ "$n" = 1 ]||{ echo "FAIL extract: $n lines of agi-run name fullscreenUpsellSeenCount (want exactly 1)";exit 99;}
K=fullscreenUpsellSeenCount
# step HOME H: run the piece's line the way the start does
step(){ env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=$1 H=${2:-claude-x} sh -c "$(cat $T/step)";}
mk(){ rm -rf $T/h;mkdir $T/h;[ -n "$1" ]&&printf '%s' "$1">$T/h/.claude.json;:;}
cj=$T/h/.claude.json;mt(){ stat -c '%Y.%y' $cj;}
mk;step $T/h;rc=$?
ok "a-fresh-home-creates-only-the-key no .claude.json -> the step (rc $rc) leaves $(cat $cj 2>/dev/null) (want exactly {\"$K\":3}), mode $(stat -c %a $cj 2>/dev/null) (want 600)" '[ $rc = 0 ]&&[ "$(jq -cS . $cj)" = "{\"$K\":3}" ]&&[ "$(stat -c %a $cj)" = 600 ]'
cp $cj $T/b4;step $T/h
ok "b-second-run-byte-identical a second run leaves the file byte-identical" 'cmp -s $T/b4 $cj'
mk '{"hasCompletedOnboarding":true,"projects":{"/x":{"a":1}},"'$K'":1,"z":[1,2]}';jq -S 'del(.'$K')' $cj>$T/c.before;step $T/h;rc=$?;jq -S 'del(.'$K')' $cj>$T/c.after
ok "c-count-1-becomes-3-others-survive count 1 -> $(jq .$K $cj) (want 3), rc $rc, every other key identical (jq -S del before == after)" '[ $rc = 0 ]&&[ "$(jq .'$K' $cj)" = 3 ]&&cmp -s $T/c.before $T/c.after'
mk '{"hasCompletedOnboarding":true,"oauthAccount":{"u":1}}';jq -S . $cj>$T/c2.before;step $T/h;jq -S 'del(.'$K')' $cj>$T/c2.after
ok "c2-absent-key-added-others-survive the key is absent beside other keys -> $(jq .$K $cj) (want 3), the rest identical" '[ "$(jq .'$K' $cj)" = 3 ]&&cmp -s $T/c2.before $T/c2.after'
mk '{"'$K'":"x","k":1}';step $T/h
ok "c3-non-number-count-becomes-3 a string count -> $(jq .$K $cj) (want 3), k kept: $(jq .k $cj)" '[ "$(jq .'$K' $cj)" = 3 ]&&[ "$(jq .k $cj)" = 1 ]'
for v in 3 5;do mk '{"'$K'":'$v',"a": 1}';cp $cj $T/d.b;m0=$(mt);sleep 1.1;step $T/h;rc=$?
 ok "d-count-$v-not-rewritten a count of $v: rc $rc, bytes unchanged and mtime unchanged ($m0 -> $(mt))" '[ $rc = 0 ]&&cmp -s $T/d.b $cj&&[ "$m0" = "$(mt)" ]';done
for bad in '{"a":1' 'not json at all' '[1,2]' '';do mk "$bad";[ -n "$bad" ]||: >$cj;cp $cj $T/e.b;step $T/h;rc=$?
 ok "e-unparsable-left-alone [$bad] -> rc $rc (want 0), bytes unchanged" '[ $rc = 0 ]&&cmp -s $T/e.b $cj';done
mk;step $T/h node
ok "f-pi-harness-touches-nothing H=node (a pi post has no Claude Code): $(ls -A $T/h|tr '\n' ' ')(want an empty home)" '[ -z "$(ls -A $T/h)" ]'
mk '{"a":1}';step $T/h;mk '{"a":1';step $T/h;mk;step $T/h
ok "g-no-temp-left-behind after the writing and refusing cases above the home holds [$(ls -A $T/h|tr '\n' ' ')] (want only .claude.json)" '[ "$(ls -A $T/h)" = .claude.json ]'
ok "h-no-other-key-named the step names none of hasCompletedOnboarding / oauthAccount / projects (falsifier 3)" '! grep -q -E "hasCompletedOnboarding|oauthAccount|projects" $T/step'
echo "claude-upsell: $f FAIL";exit $f
