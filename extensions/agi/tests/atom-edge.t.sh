#!/bin/sh
# atom-edge.t.sh [ROOT]: goal:g7.16.1.11.46.14 (M7) falsifier 1 + 2: one lane per row R1-R5, each with its MUTANT read RED; the council's G2 amendment (14:1xZ) for falsifier 2
# sh + git + jq + python3 on a scratch HOME, a scratch engine repo and a scratch card; the REAL agi-mem / agi-atom / agi-notice pieces and the real success_metrics intake reader; no network, no root, 0 USD. ROOT = the tree whose engine-post.md carries the pieces. exit = the FAIL count.
# G2: the store is 0700 under the facing post's uid, so the derive lane runs on a PLANTED store under THIS uid (a hand-labelled ask + an ack naming the id) and asserts >= 1 ask+ack row; the live line `done-when(4): <k> rows ask+ack, <q> owner chunks ?` is open while the stub stands in and RED once credits_live is true (the atomizer's turn-over point) and k = 0; a card with no chunks: field prints `chunks: 0 listed`, never a bare ok.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'chmod -R u+w "${D:?}" 2>/dev/null;rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_MINT AGI_MEM_BATCH AGI_ATOM_COMMIT
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;for x in agi-mem agi-atom agi-notice;do sect $x engine-post.md>$D/bin/$x;done;chmod +x $D/bin/*
for x in agi-mem agi-atom agi-notice;do [ -s $D/bin/$x ]||{ echo "FAIL inputs: no $x piece";exit 99;};done
E=$D/eng;mkdir -p $E/.agi/nodes/.geometry $E/.agi/nodes/goal;ln -s $R0/extensions $E/extensions
printf -- '---\nid: config:posts\nparents:\n  - goal:g7\nposts:\n  - {"name": "p", "mem": "full", "faces": "owner"}\n---\n'>$E/.agi/nodes/.geometry/posts.md
printf -- '---\nid: goal:g1.2\nstatus: active\n---\n# g\n'>$E/.agi/nodes/goal/g1.2.md
printf -- 'credits_live: false\n'>$E/.agi/nodes/.geometry/secrets.md
(cd $E&&git init -q .&&git config core.hooksPath /dev/null&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x)
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"%s","message":{"content":%s}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
AL(){ printf '{"type":"assistant","uuid":"%s","timestamp":"%s","message":{"content":[{"type":"text","text":%s}]}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
# nh <n>: a fresh HOME, store, card (G/sessions/quorum/p.md, the shape the board reads) and transcript
nh(){ H=$D/h$1;rm -rf "${H:?}";G=$D/g$1;rm -rf "${G:?}";mkdir -p $H/.claude/projects/x $G/sessions/quorum;X=$H/.claude/projects/x/S1.jsonl;: >$X;echo S1>$H/.session;S=$H/.mem/p.git;CARD=$G/sessions/quorum/p.md
 printf '# card\n\n## §0 x\nhi\n\n## §7 ATOMS\n\n| # | atom (verbatim slice) | source | state | lap |\n|---|---|---|---|---|\n| a1 | "fix the widget" | src:doc | leaf:goal:g1.2 | lap1 |\n| a2 | "other thing" | src:doc | target:x | lap5 |\n| 10.2 | "legacy ask" | src:doc | target:y | lap5 |\n\n## §8 after\n' >$CARD;}
EV(){ env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_T=$E AGI_TRUNK=HEAD AGI_ATOM_CARD=$CARD AGI_LAP=${LAP:-5} PATH=$D/bin:$PATH "$@";}
TAP(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_T=$E AGI_TRUNK=HEAD AGI_ATOM_CARD=$CARD AGI_LAP=${LAP:-5} PATH=$D/tb:$D/bin:$PATH sh ${1:-$D/bin/agi-mem} tap 2>&1;}
TAPF(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|EV sh ${1:-$D/bin/agi-mem} tap 2>&1;}
LB(){ EV sh ${1:-$D/bin/agi-mem} label 2>&1;}
WK(){ EV sh ${1:-$D/bin/agi-mem} walk 2>&1;}
field(){ f1=$(git -C $S grep -l -F -- "$1" refs/heads/mem|sed 's/^[^:]*://'|head -1);git -C $S show refs/heads/mem:$f1|awk -v k="$2" '/^---$/{n++}n<2&&index($0,k": ")==1{print substr($0,length(k)+3);exit}';}
PL(){ x=$(git -C $S grep -l -F -- "$1" refs/heads/mem|sed 's/^[^:]*://'|head -1);git -C $S show refs/heads/mem:$x|awk -v k="$2" '/^---$/{n++}n<2&&/^kind: /{print "kind: " k;next}{print}'>$D/pl;b=$(git -C $S hash-object -w $D/pl);GIT_INDEX_FILE=$D/pli;export GIT_INDEX_FILE;git -C $S read-tree refs/heads/mem;git -C $S update-index --cacheinfo 100644,$b,$x;t=$(git -C $S write-tree);c=$(git -C $S -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit-tree $t -p refs/heads/mem -m plant);git -C $S update-ref refs/heads/mem $c;unset GIT_INDEX_FILE;}
SA(){ x=$(git -C $S grep -l -F -- "$1" refs/heads/mem|sed 's/^[^:]*://'|head -1);git -C $S show refs/heads/mem:$x|awk -v a="$2" '/^---$/{n++}n<2&&/^atom: /{print "atom: " a;next}{print}'>$D/pl;b=$(git -C $S hash-object -w $D/pl);GIT_INDEX_FILE=$D/pli git -C $S read-tree refs/heads/mem;GIT_INDEX_FILE=$D/pli git -C $S update-index --cacheinfo 100644,$b,$x;c=$(git -C $S -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit-tree $(GIT_INDEX_FILE=$D/pli git -C $S write-tree) -p refs/heads/mem -m hand);git -C $S update-ref refs/heads/mem $c;}
MUT(){ sed "$1" $D/bin/$2>$D/mut_$2;cmp -s $D/bin/$2 $D/mut_$2&&{ echo "FAIL inputs: mutant edit '$1' changed nothing in $2";exit 99;};}
# TAP sweeps WITHOUT the label/derive/walk that a real tap ends with (so a lane can run each step, and its mutant, alone); TAPF is the full real tap
mkdir $D/tb;printf '#!/bin/sh\ncase $1 in label|walk) exit 0;; esac\nexec sh %s/bin/agi-mem "$@"\n' $D>$D/tb/agi-mem;printf '#!/bin/sh\ncase $1 in derive) exit 0;; esac\nexec sh %s/bin/agi-atom "$@"\n' $D>$D/tb/agi-atom;chmod +x $D/tb/*
T0=2026-10-24T10:00:00.000Z;T1=2026-10-24T10:00:05.000Z;T2=2026-10-24T10:00:09.000Z

# ---- R1 each chunk carries atom: <id>|none|?; the grammar resolves the card's real row ids, <n>.<m> and a<n>
nh r1;AL p1 "On it: a1 and 10.2 are mine" $T0>>$X;AL p2 "Nothing to see, a99 is no row" $T1>>$X;UL o1 "what became of a2 please" $T2>>$X;UL o2 "build a brand new thing" 2026-10-24T10:00:10.000Z>>$X;TAP>/dev/null;LB>/dev/null
ok "r1-post-naming-ids-gets-them a post chunk naming a row id of each form gets 'atom: 10.2 a1' (sorted) and kind: ack (got '$(field 'are mine' atom)' / '$(field 'are mine' kind)')" '[ "$(field "are mine" atom)" = "10.2 a1" ]&&[ "$(field "are mine" kind)" = ack ]'
ok "r1-unresolved-id-is-not-an-atom a99 names no card row, so the post chunk reads atom: none (got '$(field 'a99 is no row' atom)')" '[ "$(field "a99 is no row" atom)" = none ]'
ok "r1-owner-naming-an-id-gets-it an owner chunk naming a2 gets atom: a2 and keeps kind: ? (got '$(field 'became of a2' atom)' / '$(field 'became of a2' kind)')" '[ "$(field "became of a2" atom)" = a2 ]&&[ "$(field "became of a2" kind)" = "?" ]'
# ---- R4 tier 0 runs first; until C1-C3 the stub labels an owner chunk `?`, never `none`
ok "r4-stub-labels-owner-question-mark an owner chunk that names no row id stays 'atom: ?' after the label pass (got '$(field 'brand new thing' atom)'), a post chunk with none reads none" '[ "$(field "brand new thing" atom)" = "?" ]'
MUT 's/|\[0-9\]+\\.\[0-9\]+)/)/' agi-mem;nh r1m;AL p1 "On it: 10.2 is mine" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1-mutant-10.2-does-not-resolve-RED a grammar that knows only a<n> leaves 'atom: 10.2' unresolved ($(field 'is mine' atom)): the lane wants it" '[ "$(field "is mine" atom)" != "10.2" ]'


MUT 's/else continue;fi/else v=none;k=;fi/' agi-mem;nh r4m;UL o2 "build a brand new thing" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r4-mutant-stub-returns-none-RED a labeler that answers none for an owner chunk writes 'atom: $(field 'brand new' atom)': the lane wants ?" '[ "$(field "brand new" atom)" = none ]'

# ---- R2 the card row's chunks: list is DERIVED from the chunks, never hand-kept
nh r2;UL o1 "please fix the widget now" $T0>>$X;AL p1 "Opened a1 for it" $T1>>$X;TAP>/dev/null;LB>/dev/null;PL "please fix the widget now" ask
sed -i 's/^| a1 | "fix the widget" | src:doc | leaf:goal:g1.2 | lap1 |$/| a1 | "fix the widget" | src:doc | leaf:goal:g1.2 | lap1 | chunks: c:zzzzzzzzzzzz |/' $CARD;cp $CARD $D/card0
# the ask chunk names no id yet: label it a1 by hand (what tier 1 / M2's atomizer will do), the way a planted store would
SA "please fix the widget now" a1
o=$(EV agi-atom derive 2>$D/derr);ok "r2-derive-rewrites-a-hand-kept-list the hand-kept 'chunks: c:zzzzzzzzzzzz' is replaced by the two real chunk ids and REPORTED ('$(cat $D/derr)'; summary '$o')" '! grep -q zzzz $CARD&&grep -qE "^\| a1 \|.*\| lap1 \| chunks: c:[0-9a-f]{12} c:[0-9a-f]{12} \|$" $CARD&&grep -q "^\[derive\] a1: the chunks list was \[chunks: c:zzzzzzzzzzzz\], rewritten" $D/derr&&[ "$o" = "chunks: 2 listed" ]'
cp $CARD $D/card1;o=$(EV agi-atom derive 2>$D/derr);ok "r2-derive-is-idempotent a second derive changes nothing and reports nothing (cmp: $(cmp -s $CARD $D/card1&&echo same||echo differs); '$(cat $D/derr)')" 'cmp -s $CARD $D/card1&&[ ! -s $D/derr ]'
ok "r2-rows-without-chunks-are-untouched a2 and 10.2 (no chunk names them) keep their exact bytes" 'grep -qxF "| a2 | \"other thing\" | src:doc | target:x | lap5 |" $CARD&&grep -qxF "| 10.2 | \"legacy ask\" | src:doc | target:y | lap5 |" $CARD'
MUT 's/cmp -s $M.n "$C"||put <$M.n;;/:;;/' agi-atom;cp $D/card0 $CARD;o=$(EV sh $D/mut_agi-atom derive 2>/dev/null)
ok "r2-mutant-a-hand-edit-survives-RED a derive that never writes leaves the hand-kept list in the card (zzzz kept: $(grep -c zzzz $CARD)): the lane wants it gone" 'grep -q zzzz $CARD'

# ---- R3 agi-atom where <words> = chunk -> atom -> exit -> leaf status, no model; no hit = `no chunk`, rc 1
cp $D/card1 $CARD;EV agi-atom derive >/dev/null 2>&1;o=$(EV agi-atom where "fix the widget" 2>&1);rc=$?;id=$(git -C $S grep -h '^id: c:' refs/heads/mem|sed 's/^id: //'|head -1)
ok "r3-where-answers-from-the-chain a planted ask returns chunk id, atom id, exit and the leaf's status in one line: '$o'" '[ $rc = 0 ]&&echo "$o"|grep -qE "^asked 2026-10-24 10:00Z \(c:[0-9a-f]{12}\) · a1 · leaf:goal:g1.2 · active$"'
o2=$(EV agi-atom where "no such words anywhere" 2>&1);rc2=$?;ok "r3-no-hit-is-no-chunk-rc-1 words that match nothing print 'no chunk' with rc 1, never a nearest guess (got '$o2' rc $rc2)" '[ "$o2" = "no chunk" ]&&[ $rc2 = 1 ]'
MUT 's/echo "no chunk";exit 1;/echo "no chunk";exit 0;/' agi-atom;o3=$(EV sh $D/mut_agi-atom where "no such words" 2>&1);rc3=$?;ok "r3-mutant-a-miss-returns-rc-0-RED an agi-atom whose miss exits 0 fails the rc 1 lane (rc $rc3)" '[ $rc3 = 0 ]'

# ---- R5 a post reply to a planted `kind: ask` chunk that names no atom id is a red at the next turn; a reply naming the id is green
red(){ AGI_LAP=${LAP:-5} python3 -c "import sys;sys.path.insert(0,'$R0/extensions/agi/bin');import success_metrics as m;from pathlib import Path;print(m.intake_segment(Path('$G')))" 2>&1;}
nh r5;UL o1 "refactor the router please" $T0>>$X;AL p1 "Sure, on it." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;before=$(LAP=5 red);WK>/dev/null;after=$(LAP=5 red)
h=$(EV agi-mem map|awk -F'	' '$4=="ask"{print substr($1,3,8)}')
ok "r5-unnamed-reply-is-red an ask + a reply naming no id adds ONE r<8hex> row 'red:unnamed-reply' to the card, ONE notice '[unnamed-reply] <8hex> ...', and the board's intake red count rises ($before -> $after)" 'grep -qE "^\| r$h \| \"refactor the router please\" \| src:chunk:c:[0-9a-f]{12} \| red:unnamed-reply \| lap5 \|$" $CARD&&[ "$(cat $H/.notice 2>/dev/null|grep -c "^\[unnamed-reply\] $h ")" = 1 ]&&echo "$before"|grep -q "p=2/1/0"&&echo "$after"|grep -q "p=3/1/1"'
WK>/dev/null;WK>/dev/null;ok "r5-walk-is-idempotent running the walk again adds no second row and no second notice (rows $(grep -c '^| r' $CARD))" '[ "$(grep -c "^| r" $CARD)" = 1 ]'
EV agi-atom close r$h out:named;ok "r5-a-red-row-closes-like-any-atom agi-atom close r<8hex> out:named closes the born-red row and the red count falls back ($(LAP=5 red))" 'grep -q "^| r$h .*| out:named |" $CARD&&LAP=5 red|grep -q "p=2/2/0"'
nh r5g;UL o1 "refactor the router please" $T0>>$X;AL p1 "Opened a1 for the router." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK>/dev/null
ok "r5-named-reply-is-green the same ask answered with a reply that names a1 adds no row ($(grep -c '^| r' $CARD)) and the red count stays 0 ($(LAP=5 red))" '[ "$(grep -c "^| r" $CARD)" = 0 ]&&LAP=5 red|grep -q "p=2/1/0"'
MUT 's/print (\$5=="none"||\$5=="?"?"RED":"OK"),q\[i\],\$1/print "OK",q[i],$1/' agi-mem;nh r5m;UL o1 "refactor the router please" $T0>>$X;AL p1 "Sure, on it." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK $D/mut_agi-mem>/dev/null
ok "r5-mutant-unnamed-reply-reads-green-RED a walk that never calls a reply red leaves no r-row ($(grep -c '^| r' $CARD)): the lane wants one" '[ "$(grep -c "^| r" $CARD)" = 0 ]'
MUT 's/print (\$5=="none"||\$5=="?"?"RED":"OK"),q\[i\],\$1/print "RED",q[i],$1/' agi-mem;nh r5n;UL o1 "refactor the router please" $T0>>$X;AL p1 "Opened a1 for the router." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK $D/mut_agi-mem>/dev/null
ok "r5-mutant-named-reply-reads-red-RED a walk that calls every reply red writes an r-row for a reply that DID name the id ($(grep -c '^| r' $CARD)): the lane wants none" '[ "$(grep -c "^| r" $CARD)" = 1 ]'
# the M4 reader: a red: row is open AND red at once; the derived chunks: cell is not part of the row's shape
mkdir -p $D/gm/sessions/quorum;printf '## §7 ATOMS\n\n| # | atom | source | state | lap |\n|---|---|---|---|---|\n| a1 | "x" | src:doc | target:t | lap5 | chunks: c:aaaaaaaaaaaa |\n| rdeadbeef | "y" | src:chunk:c:bbbbbbbbbbbb | red:unnamed-reply | lap5 |\n| a2 | "z" | src:doc | leaf:goal:g1.2 | lap4 | chunks: c:cccccccccccc c:dddddddddddd |\n'>$D/gm/sessions/quorum/q.md
ok "r5-the-board-reads-the-new-shapes the intake reader counts a row with a derived chunks: cell by its state/lap and a red: row as open + red: '$(AGI_LAP=5 python3 -c "import sys;sys.path.insert(0,'$R0/extensions/agi/bin');import success_metrics as m;from pathlib import Path;print(m.intake_segment(Path('$D/gm')))")' (want q=2/1/1)" '[ "$(AGI_LAP=5 python3 -c "import sys;sys.path.insert(0,\"$R0/extensions/agi/bin\");import success_metrics as m;from pathlib import Path;print(m.intake_segment(Path(\"$D/gm\")))")" = "intake: q=2/1/1" ]'

# ---- falsifier 2 (G2): the derive lane on a planted store asserts >= 1 ask+ack row; the live line; the negative
nh f2;UL o1 "please fix the widget now" $T0>>$X;AL p1 "Opened a1 for it" $T1>>$X;TAP>/dev/null;PL "please fix the widget now" ask;SA "please fix the widget now" a1;LB>/dev/null
cp $CARD $D/cardp;EV agi-atom derive >/dev/null 2>&1;cp $CARD $D/cardf;o=$(EV agi-atom derive check 2>&1);rc=$?
ok "f2a-derive-lane-holds-an-ask-and-ack-row on a planted store the derive makes >= 1 row hold an ask AND its ack chunk: '$(echo "$o"|tr '\n' '|')'" '[ $rc = 0 ]&&echo "$o"|grep -q "^chunks: 2 listed$"&&echo "$o"|grep -q "^done-when(4): 1 rows ask+ack, 0 owner chunks ? (open: the stub stands in until C1-C3)$"'
cp $D/cardp $CARD;o2=$(EV agi-atom derive check 2>&1)
ok "f2a-mutant-zero-chunks-fields-RED a card with no chunks: field prints 'chunks: 0 listed' (never a bare ok), which is not the lane's >= 1: '$(echo "$o2"|tr '\n' '|')'" 'echo "$o2"|grep -q "^chunks: 0 listed$"&&! echo "$o2"|grep -q "^chunks: 2 listed$"'
cp $D/cardf $CARD;sed -i 's/chunks: c:[0-9a-f]\{12\}/chunks: c:zzzzzzzzzzzz/' $CARD;o3=$(EV agi-atom derive check 2>&1);rc3=$?
ok "f2c-negative-every-listed-chunk-id-resolves a chunks: id that no chunk names (c:zzzzzzzzzzzz) is a named line and rc != 0: '$(echo "$o3"|head -1)' rc $rc3" '[ $rc3 != 0 ]&&echo "$o3"|grep -q "^\[chunks\] a1: c:zzzzzzzzzzzz names a1 in no chunk$"'
nh f2l;printf 'credits_live: true\n'>$E/.agi/nodes/.geometry/secrets.md;(cd $E&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm live);UL o1 "an owner ask with no label" $T0>>$X;TAP>/dev/null;o4=$(EV agi-atom derive check 2>&1);rc4=$?
ok "f2b-red-once-the-atomizer-is-live with credits_live true and no row holding an ask+ack the live line is RED and rc != 0: '$(echo "$o4"|tail -1)' rc $rc4" '[ $rc4 != 0 ]&&echo "$o4"|grep -q "^done-when(4): 0 rows ask+ack, 1 owner chunks ? RED"'
echo "atom-edge: $f FAIL";exit $f
