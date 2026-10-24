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
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"%s","origin":{"kind":"human"},"message":{"content":%s}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
AL(){ printf '{"type":"assistant","uuid":"%s","timestamp":"%s","message":{"content":[{"type":"text","text":%s}]}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
# nh <n>: a fresh HOME, store, card (G/sessions/quorum/p.md, the shape the board reads) and transcript
nh(){ H=$D/h$1;rm -rf "${H:?}";G=$D/g$1;rm -rf "${G:?}";mkdir -p $H/.claude/projects/x $G/sessions/quorum;X=$H/.claude/projects/x/S1.jsonl;: >$X;echo S1>$H/.session;S=$H/.mem/p.git;CARD=$G/sessions/quorum/p.md
 printf '# card\n\n## §0 x\nhi\n\n## §7 ATOMS\n\n| # | atom (verbatim slice) | source | state | lap |\n|---|---|---|---|---|\n| a1 | "fix the widget" | src:doc | leaf:goal:g1.2 | lap1 |\n| a2 | "other thing" | src:doc | target:x | lap5 |\n| 10.2 | "legacy ask" | src:doc | target:y | lap5 |\n| 5.5 | "model row" | src:doc | target:z | lap5 |\n\n## §8 after\n' >$CARD;}
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

# ---- R1 each chunk carries atom: <id>|none|?; a<n> is bare-safe, a dotted <n>.<m> counts only MARKED (`atom 10.2`, `atoms: 10.2 5.5`, `[10.2]`) and never with a version tail (council 15:4xZ L-GRAMMAR)
nh r1;AL p1 "On it: atoms: a1 10.2 are mine" $T0>>$X;AL p2 "Nothing to see, a99 is no row" $T1>>$X;AL p3 "f=0.47, model 5.5 on pi@1.4.0 and atom 10.2.1" $T2>>$X;AL p4 "Done [10.2] today" 2026-10-24T10:00:07.000Z>>$X;AL p5 "Both atoms: 10.2 5.5 shipped" 2026-10-24T10:00:08.000Z>>$X;UL o1 "what became of a2 please" 2026-10-24T10:00:09.000Z>>$X;UL o2 "build a brand new thing" 2026-10-24T10:00:10.000Z>>$X;UL o3 "use Haiku 5.5 for it" 2026-10-24T10:00:11.000Z>>$X;TAP>/dev/null;LB>/dev/null
ok "r1-post-naming-ids-gets-them a post chunk naming a1 and 10.2 marked gets 'atom: 10.2 a1' (sorted) and kind: ack (got '$(field 'are mine' atom)' / '$(field 'are mine' kind)')" '[ "$(field "are mine" atom)" = "10.2 a1" ]&&[ "$(field "are mine" kind)" = ack ]'
ok "r1-unresolved-id-is-not-an-atom a99 names no card row, so the post chunk reads atom: none (got '$(field 'a99 is no row' atom)')" '[ "$(field "a99 is no row" atom)" = none ]'
ok "r1-bare-decimals-and-version-tails-link-nothing 'f=0.47, model 5.5 on pi@1.4.0 and atom 10.2.1' links no row (got '$(field 'model 5.5 on pi' atom)'): 5.5 is a row, but bare" '[ "$(field "model 5.5 on pi" atom)" = none ]'
ok "r1-marked-forms-resolve '[10.2]' and 'atoms: 10.2 5.5' link their rows (got '$(field 'Done [10.2]' atom)' / '$(field 'atoms: 10.2 5.5' atom)')" '[ "$(field "Done [10.2]" atom)" = "10.2" ]&&[ "$(field "atoms: 10.2 5.5" atom)" = "10.2 5.5" ]'
ok "r1-owner-chunks-stay-question-mark tier 0 labels POST chunks only: an owner chunk naming a2, one with no id and one with 'Haiku 5.5' (a real row id) all stay 'atom: ?' (got '$(field 'became of a2' atom)' '$(field 'brand new thing' atom)' '$(field 'Haiku 5.5' atom)')" '[ "$(field "became of a2" atom)" = "?" ]&&[ "$(field "brand new thing" atom)" = "?" ]&&[ "$(field "Haiku 5.5" atom)" = "?" ]'
MUT 's/atoms?):?\[\[:space:\]\]/atomsZ?):?[[:space:]]/' agi-mem;nh r1m;AL p1 "Done atom 10.2 today" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1-mutant-10.2-does-not-resolve-RED a grammar whose marker form is broken leaves 'atom 10.2' unresolved ($(field 'Done atom' atom)): the lane wants 10.2" '[ "$(field "Done atom" atom)" != "10.2" ]'
MUT 's/\[ \$p = post \]||{ \[ "\$R" = redo \]&&{ y=\${x##\*c-};echo "label --redo: c:\${y%.md} is an owner chunk";miss=1;};continue;};//' agi-mem;nh r4m;UL o2 "build a brand new thing" $T0>>$X;UL o1 "what became of atom a2 please" $T1>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r4-mutant-stub-labels-an-owner-RED a labeler that also labels owner chunks writes 'atom: $(field 'brand new' atom)' for no id and '$(field 'became of atom a2' atom)' for a marked a2: the lanes want ? and ?" '[ "$(field "brand new" atom)" = none ]&&[ "$(field "became of atom a2" atom)" = a2 ]'

# ---- R2 the card row's chunks: list is DERIVED from the chunks, never hand-kept
nh r2;UL o1 "please fix the widget now" $T0>>$X;AL p1 "Opened atom a1 for it" $T1>>$X;TAP>/dev/null;LB>/dev/null;PL "please fix the widget now" ask
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
ok "r5-unnamed-reply-is-red an ask + a reply naming no id adds ONE r<8hex> row 'red:unnamed-reply' to the card, ONE notice '[unnamed-reply] <8hex> ...', and the board's intake red count rises ($before -> $after)" 'grep -qE "^\| r$h \| \"refactor the router please\" \| src:chunk:c:[0-9a-f]{12} \| red:unnamed-reply \| lap5 \|$" $CARD&&[ "$(cat $H/.notice 2>/dev/null|grep -c "^\[unnamed-reply\] $h ")" = 1 ]&&echo "$before"|grep -q "p=3/1/0"&&echo "$after"|grep -q "p=4/1/1"'
WK>/dev/null;WK>/dev/null;ok "r5-walk-is-idempotent running the walk again adds no second row and no second notice (rows $(grep -c '^| r' $CARD))" '[ "$(grep -c "^| r" $CARD)" = 1 ]'
EV agi-atom close r$h out:named;ok "r5-a-red-row-closes-like-any-atom agi-atom close r<8hex> out:named closes the born-red row and the red count falls back ($(LAP=5 red))" 'grep -q "^| r$h .*| out:named |" $CARD&&LAP=5 red|grep -q "p=3/2/0"'
nh r5g;UL o1 "refactor the router please" $T0>>$X;AL p1 "Opened atom a1 for the router." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK>/dev/null
ok "r5-named-reply-is-green the same ask answered with a reply that names a1 adds no row ($(grep -c '^| r' $CARD)) and the red count stays 0 ($(LAP=5 red))" '[ "$(grep -c "^| r" $CARD)" = 0 ]&&LAP=5 red|grep -q "p=3/1/0"'
MUT 's/print (\$5=="none"||\$5=="?"?"RED":"OK"),q\[i\],\$1/print "OK",q[i],$1/' agi-mem;nh r5m;UL o1 "refactor the router please" $T0>>$X;AL p1 "Sure, on it." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK $D/mut_agi-mem>/dev/null
ok "r5-mutant-unnamed-reply-reads-green-RED a walk that never calls a reply red leaves no r-row ($(grep -c '^| r' $CARD)): the lane wants one" '[ "$(grep -c "^| r" $CARD)" = 0 ]'
MUT 's/print (\$5=="none"||\$5=="?"?"RED":"OK"),q\[i\],\$1/print "RED",q[i],$1/' agi-mem;nh r5n;UL o1 "refactor the router please" $T0>>$X;AL p1 "Opened atom a1 for the router." $T1>>$X;TAP>/dev/null;PL "refactor the router please" ask;WK $D/mut_agi-mem>/dev/null
ok "r5-mutant-named-reply-reads-red-RED a walk that calls every reply red writes an r-row for a reply that DID name the id ($(grep -c '^| r' $CARD)): the lane wants none" '[ "$(grep -c "^| r" $CARD)" = 1 ]'
# the M4 reader: a red: row is open AND red at once; the derived chunks: cell is not part of the row's shape
mkdir -p $D/gm/sessions/quorum;printf '## §7 ATOMS\n\n| # | atom | source | state | lap |\n|---|---|---|---|---|\n| a1 | "x" | src:doc | target:t | lap5 | chunks: c:aaaaaaaaaaaa |\n| rdeadbeef | "y" | src:chunk:c:bbbbbbbbbbbb | red:unnamed-reply | lap5 |\n| a2 | "z" | src:doc | leaf:goal:g1.2 | lap4 | chunks: c:cccccccccccc c:dddddddddddd |\n'>$D/gm/sessions/quorum/q.md
ok "r5-the-board-reads-the-new-shapes the intake reader counts a row with a derived chunks: cell by its state/lap and a red: row as open + red: '$(AGI_LAP=5 python3 -c "import sys;sys.path.insert(0,'$R0/extensions/agi/bin');import success_metrics as m;from pathlib import Path;print(m.intake_segment(Path('$D/gm')))")' (want q=2/1/1)" '[ "$(AGI_LAP=5 python3 -c "import sys;sys.path.insert(0,\"$R0/extensions/agi/bin\");import success_metrics as m;from pathlib import Path;print(m.intake_segment(Path(\"$D/gm\")))")" = "intake: q=2/1/1" ]'

# Q (council 16:3xZ): a quoted id is not an ack (> line, backtick span, double-quoted span); REDO recomputes named chunks (a report that QUOTED the bad label was read as an ack)
nh r1q;AL q1 'The bad label was `atom 10.2` in my report' $T0>>$X;AL q2 'He wrote "atom 10.2" there' $T1>>$X;AL q3 '> atom 10.2
and my reply under it' $T2>>$X;AL q4 'atom 10.2 is mine' 2026-10-24T10:00:07.000Z>>$X;TAP>/dev/null;LB>/dev/null
ok "r1q-a-quoted-id-is-not-an-ack a backtick span, a double-quoted span and a > line naming atom 10.2 link nothing (got '$(field 'bad label was' atom)' '$(field 'He wrote' atom)' '$(field 'my reply under it' atom)'); the same words in prose link 10.2 (got '$(field 'is mine' atom)')" '[ "$(field "bad label was" atom)" = none ]&&[ "$(field "He wrote" atom)" = none ]&&[ "$(field "my reply under it" atom)" = none ]&&[ "$(field "is mine" atom)" = 10.2 ]'
MUT "s/|sed ':a;\$!{N;ba};s\/\`\[^\`\]\*\`\/\/g;s\/\"\[^\"\]\*\"\/\/g'//" agi-mem;nh r1qm;AL q1 'The bad label was `atom 10.2` in my report' $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1q-mutant-quotes-count-RED a label that strips no quotes reads a backtick-quoted 'atom 10.2' as an ack ($(field 'bad label was' atom)): the lane wants none" '[ "$(field "bad label was" atom)" = 10.2 ]'
# Q' (SM GATE224): a FENCED block (``` or ~~~) and a double-quoted span that runs across lines count no id either
FQ='Pasted from the report:
```
atom: 10.2 5.5
```
and nothing else'
TQ='Pasted from the report:
~~~
atoms: 10.2
~~~
done'
UQ='Opened a block and never closed it:
```
atom: 10.2
and the rest of the reply'
MQ='She wrote "see
atom 10.2 here" and left'
nh r1f;AL f1 "$FQ" $T0>>$X;AL f2 "$TQ" $T1>>$X;AL f3 "$MQ" $T2>>$X;AL f4 'atom 10.2 is mine again' 2026-10-24T10:00:07.000Z>>$X;TAP>/dev/null;LB>/dev/null
ok "r1f-fenced-and-multiline-quotes-are-not-acks a triple-backtick block, a ~~~ block and a double-quoted span across two lines naming marked ids link nothing (got '$(field 'Pasted from the report:' atom)' / '$(field 'She wrote' atom)'); the same id in prose links 10.2 (got '$(field 'is mine again' atom)')" '[ "$(git -C $S grep -h -A0 "^atom: none" refs/heads/mem|wc -l|tr -d " ")" -ge 3 ]&&[ "$(field "She wrote" atom)" = none ]&&[ "$(field "is mine again" atom)" = 10.2 ]'
MUT "s/|awk -v m=s \"\$FZ\"//" agi-mem;nh r1fm;AL f2 "$TQ" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1f-mutant-fence-not-stripped-RED a label with no fence stage reads the ~~~ fenced 'atoms: 10.2' as an ack ($(field 'Pasted from the report:' atom)): the lane wants none" '[ "$(field "Pasted from the report:" atom)" = "10.2" ]'
nh r1fu;AL u1 "$UQ" $T0>>$X;TAP>/dev/null;LB>/dev/null;ua=$(field 'Opened a block' atom);MUT "s/|awk -v m=s \"\$FZ\"//" agi-mem;nh r1fv;AL u1 "$UQ" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1f-an-unmatched-fence-fails-closed an opening triple-backtick with no close counts no id to the end of the chunk (got '$ua'); MUTANT: with no fence stage the same chunk reads '$(field 'Opened a block' atom)' (RED if 10.2)" '[ "$ua" = none ]&&[ "$(field "Opened a block" atom)" = 10.2 ]'
MUT "s/sed ':a;\$!{N;ba};s\/\`/sed 's\/\`/" agi-mem;nh r1fn;AL f3 "$MQ" $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1f-mutant-quotes-line-by-line-RED a label that strips quotes one line at a time reads the two-line quoted span as an ack ($(field 'She wrote' atom)): the lane wants none" '[ "$(field "She wrote" atom)" = 10.2 ]'

# N (council 18:4xZ, aio's gap): a block closes only on a fence of the opener's character at >= its length; a ~~~ / shorter fence inside it is text
N1='Block A:
~~~
```
atom: 10.2
~~~
and nothing else'
N2='Block B:
````
```
atom: 10.2
```
````
done'
N3='Block C:
```
~~~
atom: 10.2
```
done'
N4='Block D:
~~~
```
x
~~~
atom 5.5 is mine'
N5='Block E:
~~~
```
atom: 10.2
and the rest'
nn(){ nh $1;AL n1 "$N1" $T0>>$X;AL n2 "$N2" $T1>>$X;AL n3 "$N3" $T2>>$X;AL n4 "$N4" 2026-10-24T10:00:11.000Z>>$X;AL n5 "$N5" 2026-10-24T10:00:12.000Z>>$X;AL n6 "$FQ" 2026-10-24T10:00:13.000Z>>$X;UL n7 "Owner pasted:
~~~
\`\`\`
atom: 10.2
~~~" 2026-10-24T10:00:14.000Z>>$X;TAP>/dev/null;}
nn r1n;LB>/dev/null;g="$(field 'Block A:' atom)/$(field 'Block B:' atom)/$(field 'Block C:' atom)/$(field 'Block E:' atom)"
ok "r1n-a-nested-fence-is-text a tilde block holding a backtick pair (A), a 4-backtick block holding a 3-backtick pair (B) and a backtick block holding a tilde line (C), each naming 'atom: 10.2' inside, and an unmatched nested block (E) link nothing (got '$g'); prose after a closed outer fence still acks (D: '$(field 'Block D:' atom)')" '[ "$g" = none/none/none/none ]&&[ "$(field "Block D:" atom)" = 5.5 ]'
nm(){ MUT "$1" agi-mem;nn r1nm;LB $D/mut_agi-mem>/dev/null;h=$(field "Block $3:" atom)
 if [ $3 = D ];then ok "r1n-mutant-$4-RED $2 reads Block D's prose ack as '$h': the lane wants 5.5" '[ "$h" != 5.5 ]';else ok "r1n-mutant-$4-RED $2 reads Block $3 as '$h': the lane wants none" '[ "$h" = 10.2 ]';fi;}
nm 's/c==ch&&n>=len/n>=len/' "a closer of any character" A closer-of-any-character
nm 's/&&n>=len&&r~/\&\&r~/' "a closer of any length" B closer-of-any-length
nm 's/if(o&&c==ch&&n>=len&&r~\/^\[\[:space:\]\]\*\$\/)f=0/if(o)f=0/' "a toggle (the old behaviour)" A toggle
nm 's/)f=0;else/)f=1;else/' "a block that never closes" D never-closes
# S (council sp): the host sweep. nested [fix] lists the live POST chunks with a fence inside a fence; an unreadable store prints mem: unread, never 0
nn r1s;LB>/dev/null;o=$(EV agi-mem nested 2>&1);rc=$?
ok "r1s-nested-lists-the-post-chunks-with-a-fence-in-a-fence the sweep prints '$(echo "$o"|head -1)' and ids $(echo "$o"|sed 1d|wc -l|tr -d ' ') (want 5: A B C D E; not the plain fenced chunk, not the owner chunk), rc $rc" '[ $rc = 0 ]&&[ "$(echo "$o"|head -1)" = "nested-fence chunks: 5" ]&&[ "$(echo "$o"|sed 1d|grep -c "^c:[0-9a-f]\{12\}$")" = 5 ]'
SA 'Block A:' 10.2;EV agi-mem nested fix>/dev/null 2>&1;rc=$?;k2=$(field 'Block A:' atom)
ok "r1s-nested-is-a-report-only nested fix relabels nothing now (the recompute is label --all): Block A stays '$k2', rc $rc (want 10.2, 0)" '[ "$k2" = 10.2 ]&&[ $rc = 0 ]'
nh r1u;o=$(EV agi-mem nested 2>&1);rc=$?
ok "r1s-an-unreadable-store-is-never-zero a post with no store prints '$o' and rc $rc (want 'mem: unread', rc 1)" '[ "$o" = "mem: unread" ]&&[ $rc = 1 ]'
MUT 's/echo "mem: unread";exit 1;};: >/echo "nested-fence chunks: 0";exit 0;};: >/' agi-mem;o=$(EV sh $D/mut_agi-mem nested 2>&1)
ok "r1s-mutant-unreadable-reads-zero-RED a nested that prints 0 for a store it could not read says '$o': the lane wants mem: unread" '[ "$o" = "nested-fence chunks: 0" ]'
# F2 (alive): label --redo c:X that matches no chunk prints one line and exits 1; the chunks it did match are still recomputed
nn r1x;LB>/dev/null;SA 'Block A:' 10.2;ida=$(EV agi-mem find 'Block A:'|cut -f1);o=$(EV agi-mem label --redo c:000000000000 $ida 2>&1);rc=$?;k4=$(field 'Block A:' atom)
ok "f2-redo-of-a-missing-chunk-is-loud label --redo c:000000000000 $ida prints '$o' and rc $rc (want 'label --redo: no chunk c:000000000000', rc 1) and still recomputes the real one ($k4 -> none)" '[ "$o" = "label --redo: no chunk c:000000000000" ]&&[ $rc = 1 ]&&[ "$k4" = none ]'
o=$(EV agi-mem label --redo 2>&1);rc=$?
ok "f2-redo-with-no-id-is-loud label --redo with no id prints '$o' and rc $rc (want 'label --redo: no chunk named', rc 1)" '[ "$o" = "label --redo: no chunk named" ]&&[ $rc = 1 ]'
MUT 's/exit $miss;;/exit 0;;/' agi-mem;EV sh $D/mut_agi-mem label --redo c:000000000000 >/dev/null 2>&1;rc=$?
ok "f2-mutant-redo-miss-exits-0-RED a label that always exits 0 returns rc $rc for a missing chunk: the lane wants 1" '[ $rc = 0 ]'

# A (council 19:0xZ, belam's live a1/a2): an id counts only MARKED, a<n> as much as a dotted one; a bare a1 in prose is nothing
nh r1b;AL b1 'Rows 10.2, 5.5, a1 and a2 are still open on the card' $T0>>$X;AL b2 'Closing a1 and a2 on the router' $T1>>$X;AL b3 'Shipped it, atom a1 done' $T2>>$X;AL b4 'Both [a1, a2] shipped' 2026-10-24T10:00:07.000Z>>$X;AL b5 'And atoms: a2 shipped' 2026-10-24T10:00:08.000Z>>$X;TAP>/dev/null;LB>/dev/null
g="$(field 'Rows 10.2' atom)/$(field 'Closing a1' atom)/$(field 'atom a1 done' atom)/$(field 'Both [a1' atom)/$(field 'And atoms' atom)"
ok "r1b-a-bare-a<n>-is-not-an-ack belam's sentence listing rows bare and a bare 'closing a1 and a2' link nothing; 'atom a1', '[a1, a2]' and 'atoms: a2' link their rows (got '$g', want none/none/a1/a1 a2/a2)" '[ "$g" = "none/none/a1/a1 a2/a2" ]'
MUT 's/(?i:atoms?):?\[\[:space:\]\]+\\\\K/(?:(?i:atoms?):?[[:space:]]+)?\\\\K/' agi-mem;nh r1bm;AL b1 'Rows 10.2, 5.5, a1 and a2 are still open on the card' $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "r1b-mutant-bare-ids-count-RED a label whose marker is optional reads belam's bare list as '$(field 'Rows 10.2' atom)': the lane wants none" '[ "$(field "Rows 10.2" atom)" != none ]'
# R (council 19:0xZ): ONE recompute over EVERY live post chunk, then derive: k = m; an unreadable store is mem: unread, never 0
nn r1a;AL n8 'closing a1 and a2 on the router' 2026-10-24T10:00:15.000Z>>$X;TAP>/dev/null;LB>/dev/null;SA 'Block A:' 10.2;SA 'closing a1' 'a1 a2';o=$(EV agi-mem label --all 2>&1);rc=$?
ok "r1a-label-all-recomputes-every-live-post-chunk the recompute prints '$(echo "$o"|head -1)' rc $rc (want 'relabelled 7/7 post chunks', 0; 7 post chunks, the owner chunk is not one); a mislabelled Block A reads '$(field 'Block A:' atom)' and the old bare ack '$(field 'closing a1' atom)' (want none, none)" '[ "$(echo "$o"|head -1)" = "relabelled 7/7 post chunks" ]&&[ $rc = 0 ]&&[ "$(field "Block A:" atom)" = none ]&&[ "$(field "closing a1" atom)" = none ]'
SA 'Block A:' 10.2;MUT 's/ls-tree -r --name-only $tip -- mem|grep -v retired>$D\/rl;elif/ls-tree -r --name-only $tip -- mem|grep -v retired|grep -v c->$D\/rl;elif/' agi-mem;o=$(EV sh $D/mut_agi-mem label --all 2>&1)
ok "r1a-mutant-recompute-reads-no-chunk-RED a label --all whose list is empty prints '$(echo "$o"|head -1)' and leaves Block A at '$(field 'Block A:' atom)': the lane wants 7/7 and none" '[ "$(field "Block A:" atom)" = 10.2 ]'
nh r1au;o=$(EV agi-mem label --all 2>&1);rc=$?
ok "r1a-an-unreadable-store-is-never-zero label --all on a post with no store prints '$o' rc $rc (want 'mem: unread', 1)" '[ "$o" = "mem: unread" ]&&[ $rc = 1 ]'
MUT 's/{ \[ "$1" = --all \]&&{ echo "mem: unread";exit 1;};exit 0;};/{ exit 0;};/' agi-mem;o=$(EV sh $D/mut_agi-mem label --all 2>&1);rc=$?
ok "r1a-mutant-unreadable-exits-0-RED a label --all that says nothing and exits $rc for a store it could not read: the lane wants mem: unread, 1" '[ -z "$o" ]&&[ $rc = 0 ]'
# alive's small row: --redo on an OWNER chunk prints one line, rc 1 (was a silent rc 0)
nn r1o;oid=$(EV agi-mem map|awk -F'	' '$2=="owner"{print $1}'|head -1);o=$(EV agi-mem label --redo $oid 2>&1);rc=$?
ok "r1o-redo-of-an-owner-chunk-is-loud label --redo $oid prints '$o' rc $rc (want 'label --redo: $oid is an owner chunk', 1)" '[ "$o" = "label --redo: $oid is an owner chunk" ]&&[ $rc = 1 ]'
MUT 's/is an owner chunk";miss=1;}/is an owner chunk";}/' agi-mem;EV sh $D/mut_agi-mem label --redo $oid >/dev/null 2>&1;rc=$?
ok "r1o-mutant-owner-redo-exits-0-RED a label that prints the line but exits $rc: the lane wants 1" '[ $rc = 0 ]'

# the three small rows + two (council 20:31Z / 21:0xZ)
# (sp) m is counted from the store LISTING (speaker: post): a chunk the sweep cannot read leaves k < m, rc 1; no post chunk = one line, rc 1
mkdir -p $D/gw;printf '#!/bin/sh\ncase "$*" in *" show "*"$BADX"*) exit 128;; esac\nexec /usr/bin/git "$@"\n'>$D/gw/git;chmod +x $D/gw/git
nn r1m;LB>/dev/null
bx=$(git -C $S grep -l '^speaker: post$' refs/heads/mem -- mem|sed 's/^[^:]*://'|head -1);o=$(EV env PATH=$D/gw:$PATH BADX=${bx##*/} sh $D/bin/agi-mem label --all 2>&1);rc=$?
ok "m1-a-post-chunk-that-cannot-be-read-is-k-below-m the post chunk ${bx##*/} unreadable: '$(echo "$o"|head -1)' rc $rc (want k < m, rc 1)" 'n=$(echo "$o"|head -1);a1=${n#relabelled };k0=${a1%%/*};m0=${a1#*/};m0=${m0%% *};[ "$k0" -lt "$m0" ]&&[ $rc = 1 ]'
MUT 's/nm=$(git -C $S grep -n .^speaker: post$. $tip -- mem .:!mem\/retired.|awk -F: .\$3==3.|wc -l|tr -d . .);/nm=0;/;s/continue;};a=;/continue;};nm=$((nm+1));a=;/' agi-mem;o=$(EV env PATH=$D/gw:$PATH BADX=${bx##*/} sh $D/mut_agi-mem label --all 2>&1);rc=$?
ok "m1-mutant-m-counted-from-the-chunks-read-RED a recompute that counts m from the chunks it could read prints '$(echo "$o"|head -1)': the lane wants k < m" 'n=$(echo "$o"|head -1);a1=${n#relabelled };k0=${a1%%/*};m0=${a1#*/};m0=${m0%% *};[ "$k0" = "$m0" ]'
nh r1n0;mkdir -p $D/n0;(umask 077;git init -q --bare $H/.mem/p.git;cd $H/.mem/p.git&&git config core.hooksPath /dev/null);UL o1 "an owner line only" $T0>>$X;TAP>/dev/null;o=$(EV agi-mem label --all 2>&1);rc=$?
ok "m1-no-post-chunk-is-one-loud-line a store holding only an owner chunk prints '$(echo "$o"|head -1)' rc $rc (want 'mem: no post chunks', 1)" '[ "$(echo "$o"|head -1)" = "mem: no post chunks" ]&&[ $rc = 1 ]'
# (alive) label --all keeps agi-atom derive's rc AND its stderr
mkdir -p $D/ad;printf '#!/bin/sh\ncase $1 in derive) echo "derive-boom" >&2;exit 1;; esac\nexec sh %s/bin/agi-atom "$@"\n' $D>$D/ad/agi-atom;chmod +x $D/ad/agi-atom
nn r1d;o=$(EV env PATH=$D/ad:$PATH sh $D/bin/agi-mem label --all 2>&1);rc=$?
ok "d1-a-failed-derive-fails-the-recompute label --all with a derive that exits 1 prints '$(echo "$o"|tr '\n' '|')' rc $rc (want rc 1 and the derive-boom line kept)" '[ $rc = 1 ]&&echo "$o"|grep -q derive-boom'
MUT 's/agi-atom derive 2>&3||miss=1;/agi-atom derive 2>\/dev\/null;/' agi-mem;o=$(EV env PATH=$D/ad:$PATH sh $D/mut_agi-mem label --all 2>&1);rc=$?
ok "d1-mutant-derive-rc-dropped-RED a recompute that drops derive's rc and stderr exits $rc with '$(echo "$o"|tr '\n' '|')': the lane wants 1 and the line" '[ $rc = 0 ]&&! echo "$o"|grep -q derive-boom'
# (aio) the marker is case-insensitive; the ids stay lower-case
nh r1c;AL c1 'Atom a1 done' $T0>>$X;AL c2 'ATOMS: a2 shipped' $T1>>$X;AL c3 'Atomic a1 is not a marker' $T2>>$X;TAP>/dev/null;LB>/dev/null
g="$(field 'Atom a1 done' atom)/$(field 'ATOMS: a2' atom)/$(field 'Atomic a1' atom)"
ok "c1-the-marker-is-case-insensitive 'Atom a1 done' and 'ATOMS: a2 shipped' link a1 and a2; 'Atomic a1' is no marker (got '$g', want a1/a2/none)" '[ "$g" = a1/a2/none ]'
MUT 's/(?i:atoms?)/atoms?/' agi-mem;nh r1cm;AL c1 'Atom a1 done' $T0>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null
ok "c1-mutant-case-sensitive-marker-RED a label whose marker is case-sensitive reads 'Atom a1 done' as '$(field 'Atom a1 done' atom)': the lane wants a1" '[ "$(field "Atom a1 done" atom)" = none ]'
# (alive) derive check on a credits_live it cannot read is 'unread', never 'open'; (aio + sp) a live atomizer that leaves owner chunks ? is RED
nh u1;UL o1 "an owner line" $T0>>$X;AL p1 "Opened atom a1" $T1>>$X;TAP>/dev/null;LB>/dev/null;o=$(EV env AGI_TRUNK=no-such-ref agi-atom derive check 2>&1);rc=$?
ok "u1-an-unreadable-credits-live-is-unread-not-open derive check with a trunk that has no secrets.md prints '$(echo "$o"|tail -1)' rc $rc (want 'done-when(4): unread (credits_live unreadable)', rc 1)" '[ "$(echo "$o"|tail -1)" = "done-when(4): unread (credits_live unreadable)" ]&&[ $rc = 1 ]'
MUT 's/||echo UNREAD)/)/' agi-atom;o=$(EV sh $D/mut_agi-atom derive check 2>&1 </dev/null);o=$(EV env AGI_TRUNK=no-such-ref sh $D/mut_agi-atom derive check 2>&1);rc=$?
ok "u1-mutant-failed-read-reads-open-RED a derive that lets a failed read through prints '$(echo "$o"|tail -1)' rc $rc: the lane wants the unreadable line" '! echo "$o"|tail -1|grep -q "credits_live unreadable"'
# (sp) credits_live is exactly true or false: anything else is unread (rc 1), never open
SEC(){ printf '%s\n' "$1">$E/.agi/nodes/.geometry/secrets.md;(cd $E&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm sec);}
nh v1;UL o1 "an owner line" $T0>>$X;AL p1 "Opened atom a1" $T1>>$X;TAP>/dev/null;LB>/dev/null;g=
for v in 'credits_live: true # x' 'credits_live: yes' 'credits_lives: true' 'credits_live: False'; do SEC "$v";o=$(EV agi-atom derive check 2>&1);rc=$?;g="$g[$(echo "$o"|tail -1|sed 's/^done-when(4): //')/$rc]";done
ok "v1-a-credits-live-that-is-not-exactly-true-or-false-is-unread each of a trailing comment, 'yes', a misspelled key and 'False' reads unread with rc 1: $g" '[ "$g" = "[unread (credits_live: true # x)/1][unread (credits_live: yes)/1][unread (credits_live: no key)/1][unread (credits_live: False)/1]" ]'
SEC 'credits_live: false   ';o=$(EV agi-atom derive check 2>&1);rc=$?
ok "v1-trailing-blanks-are-not-a-comment 'credits_live: false' with trailing blanks still reads open (rc $rc): '$(echo "$o"|tail -1)'" '[ $rc = 0 ]&&echo "$o"|tail -1|grep -q "(open: the stub stands in"'
SEC 'credits_live: true # x';MUT 's/if(live!="true"&&live!="false")/if(0)/' agi-atom;o=$(EV sh $D/mut_agi-atom derive check 2>&1);rc=$?
ok "v1-mutant-no-value-check-RED a derive that does not check the value reads 'credits_live: true # x' as '$(echo "$o"|tail -1)' rc $rc: the lane wants unread" '[ $rc != 1 ]'
# (alive) the red on owner chunks still ? bites only after an atomize pass (a chunk older than ~/.atomize.last); a fresh chunk in the same turn is not red
SEC 'credits_live: true'
nh l3;UL o1 "please fix the widget now" $T0>>$X;UL o2 "and an owner line the stub never labelled" $T1>>$X;AL p1 "Opened atom a1 for it" $T2>>$X;TAP>/dev/null;PL "please fix the widget now" ask;SA "please fix the widget now" a1;LB>/dev/null;EV agi-atom derive>/dev/null 2>&1
LST=$D/last_l3;rm -f $LST
dc(){ o=$(EV env AGI_ATOMIZE_LAST=$LST $1 derive check 2>&1);rc=$?;}
dc agi-atom;ok "l3-no-atomize-pass-yet-is-not-red credits_live true, one ask+ack row, one owner chunk still ?, no atomize stamp: '$(echo "$o"|tail -1)' rc $rc (want no RED, rc 0)" '[ $rc = 0 ]&&! echo "$o"|tail -1|grep -q RED'
echo 2026-10-24T09:00:00Z>$LST;dc agi-atom;ok "l3-a-fresh-owner-chunk-in-the-same-turn-is-not-red the chunk is NEWER than the last atomize pass: '$(echo "$o"|tail -1)' rc $rc (want no RED, rc 0)" '[ $rc = 0 ]&&! echo "$o"|tail -1|grep -q RED'
echo 2026-10-24T11:00:00Z>$LST;dc agi-atom;ok "l3-a-chunk-still-open-after-an-atomize-pass-is-red the same chunk is OLDER than the last atomize pass: '$(echo "$o"|tail -1)' rc $rc (want RED naming the owner chunks, rc 1)" '[ $rc = 1 ]&&echo "$o"|tail -1|grep -q "RED: the atomizer is live and owner chunks are still ?"'
echo 2026-10-24T09:00:00Z>$LST;MUT 's/if(last!=""&&f\[3\]<last)qo++/qo++/' agi-atom;dc "sh $D/mut_agi-atom"
ok "l3-mutant-every-open-owner-chunk-counts-RED a derive that counts a fresh owner chunk reads '$(echo "$o"|tail -1)' rc $rc: the lane wants no RED" '[ $rc = 1 ]'
SA "and an owner line" none;echo 2026-10-24T11:00:00Z>$LST;dc agi-atom
ok "l3-all-owner-chunks-labelled-with-an-ask-ack-row-is-green credits_live true, the owner chunk labelled, one ask+ack row, an atomize pass after it: '$(echo "$o"|tail -1)' rc $rc (want no RED, rc 0)" '[ $rc = 0 ]&&! echo "$o"|tail -1|grep -q RED'
SEC 'credits_live: false'
# (aio) m is counted from a chunk's HEADER line: an owner chunk that QUOTES 'speaker: post' adds nothing
nh h1;AL p1 "Opened atom a1" $T0>>$X;UL o1 "I typed this:
speaker: post
and moved on" $T1>>$X;TAP>/dev/null;o=$(EV agi-mem label --all 2>&1);rc=$?
ok "h1-a-quoted-speaker-line-adds-nothing-to-m an owner chunk whose body holds 'speaker: post' leaves the recompute at '$(echo "$o"|head -1)' rc $rc (want relabelled 1/1 post chunks, 0)" '[ "$(echo "$o"|head -1)" = "relabelled 1/1 post chunks" ]&&[ $rc = 0 ]'
MUT 's/|awk -F: .\$3==3.//' agi-mem;o=$(EV sh $D/mut_agi-mem label --all 2>&1)
ok "h1-mutant-m-counts-any-matching-line-RED an m taken from any line says '$(echo "$o"|head -1)': the lane wants 1/1" '[ "$(echo "$o"|head -1)" != "relabelled 1/1 post chunks" ]'

# REDO: the chunk the mutant mislabelled is recomputed by the real label, and derive drops it from the row; a chunk NOT named is left alone
MUT "s/|sed ':a;\$!{N;ba};s\/\`\[^\`\]\*\`\/\/g;s\/\"\[^\"\]\*\"\/\/g'//" agi-mem;nh r1r;AL q1 'The bad label was `atom 10.2` in my report' $T0>>$X;AL q2 'atom a1 is mine' $T1>>$X;TAP>/dev/null;LB $D/mut_agi-mem>/dev/null;cp $CARD $D/cardr;EV agi-atom derive>/dev/null 2>&1;l0=$(grep -c 'chunks: c:' $CARD);id1=$(EV agi-mem map|awk -F'	' '$3 ~ /10:00:00/{print $1}');LB>/dev/null;k1=$(field 'bad label was' atom);EV agi-mem label --redo $id1 >/dev/null 2>&1;k2=$(field 'bad label was' atom);EV agi-atom derive>/dev/null 2>&1
ok "r1r-redo-recomputes-only-the-named-chunks the mislabelled chunk reads '$k1' (a plain label pass leaves it, it is no longer atom: ?), then '$k2' after label --redo; its link is gone from the card (rows with a chunks: cell $l0 -> $(grep -c 'chunks: c:' $CARD)), and the unnamed chunk keeps its atom ($(field 'is mine' atom))" '[ "$k1" = 10.2 ]&&[ "$k2" = none ]&&[ "$l0" = 2 ]&&[ "$(grep -c "chunks: c:" $CARD)" = 1 ]&&[ "$(field "is mine" atom)" = a1 ]'

# the live knock-on (belam 15:4xZ): a misattributed owner chunk naming card ids was LABELLED and DERIVED onto rows. Owner chunks now link nothing, and scrub takes the chunk out
MUT 's/<\[a-z\]\[a-z-\]\*\[ >\]|//' agi-mem;nh r6k;cp $CARD $D/cardk;UL c1 '<cross-session-message from="x">hand-off: see a1 and a2 and atom 10.2</cross-session-message>' $T0>>$X;TAP $D/mut_agi-mem>/dev/null;LB>/dev/null;EV agi-atom derive >/dev/null 2>&1;n0=$(grep -c 'chunks: c:' $CARD);s0=$(git -C $S grep -c '^id: c:' refs/heads/mem -- mem ':!mem/retired'|awk -F: '{n+=$NF}END{print n+0}');EV agi-mem scrub;EV agi-atom derive >/dev/null 2>&1;s1=$(git -C $S grep -c '^id: c:' refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|awk -F: '{n+=$NF}END{print n+0}')
ok "r6k-owner-chunks-link-nothing-and-scrub-clears-the-store a cross-session text stored as an owner chunk by an old tap links $n0 card rows (want 0, the card is byte-for-byte the pristine one: $(cmp -s $CARD $D/cardk&&echo yes||echo no)); scrub takes the chunk out of the store ($s0 -> $s1)" '[ "$n0" = 0 ]&&cmp -s $CARD $D/cardk&&[ "$s0" = 1 ]&&[ "$s1" = 0 ]'

# retired chunks (REPAIR'): a chunk under mem/retired/ is never derived into a chunks: cell
RT(){ x=$(git -C $S grep -l -F -- "$1" refs/heads/mem|sed 's/^[^:]*://'|head -1);rm -f $D/rti;b=$(git -C $S rev-parse refs/heads/mem:$x);printf '0 %040d\t%s\n100644 %s\tmem/retired/%s\n' 0 $x $b ${x#mem/}|GIT_INDEX_FILE=$D/rti git -C $S update-index --index-info;c=$(git -C $S -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit-tree $(GIT_INDEX_FILE=$D/rti git -C $S write-tree) -p refs/heads/mem -m ret);git -C $S update-ref refs/heads/mem $c;}
MUT 's/ -- mem .:!mem\/retired. 2>\/dev\/null|awk/ 2>\/dev\/null|awk/' agi-mem;mkdir -p $D/mp;cp $D/mut_agi-mem $D/mp/agi-mem;chmod +x $D/mp/agi-mem
nh r6x;cp $CARD $D/cardx;AL p1 "Done atom a1 and moving on" $T0>>$X;TAP>/dev/null;LB>/dev/null;EV agi-atom derive>/dev/null 2>&1;w1=$(grep -c 'chunks: c:' $CARD);cp $D/cardx $CARD;RT "Done atom a1 and moving on";EV agi-atom derive>/dev/null 2>&1;w2=$(grep -c 'chunks: c:' $CARD);env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_T=$E AGI_TRUNK=HEAD AGI_ATOM_CARD=$CARD AGI_LAP=5 PATH=$D/mp:$D/bin:$PATH agi-atom derive>/dev/null 2>&1;w3=$(grep -c 'chunks: c:' $CARD);cp $D/cardx $CARD
ok "r6x-a-retired-chunk-is-never-derived the live post chunk naming a1 links $w1 row; once moved to mem/retired/ the derive links $w2 (want 1 then 0); a map that does not exclude mem/retired/ links $w3 (the mutant: RED if 1)" '[ "$w1" = 1 ]&&[ "$w2" = 0 ]&&[ "$w3" = 1 ]'

# ---- falsifier 2 (G2): the derive lane on a planted store asserts >= 1 ask+ack row; the live line; the negative
nh f2;UL o1 "please fix the widget now" $T0>>$X;AL p1 "Opened atom a1 for it" $T1>>$X;TAP>/dev/null;PL "please fix the widget now" ask;SA "please fix the widget now" a1;LB>/dev/null
cp $CARD $D/cardp;EV agi-atom derive >/dev/null 2>&1;cp $CARD $D/cardf;o=$(EV agi-atom derive check 2>&1);rc=$?
ok "f2a-derive-lane-holds-an-ask-and-ack-row on a planted store the derive makes >= 1 row hold an ask AND its ack chunk: '$(echo "$o"|tr '\n' '|')'" '[ $rc = 0 ]&&echo "$o"|grep -q "^chunks: 2 listed$"&&echo "$o"|grep -q "^done-when(4): 1 rows ask+ack, 0 owner chunks ? (open: the stub stands in until C1-C3)$"'
cp $D/cardp $CARD;o2=$(EV agi-atom derive check 2>&1)
ok "f2a-mutant-zero-chunks-fields-RED a card with no chunks: field prints 'chunks: 0 listed' (never a bare ok), which is not the lane's >= 1: '$(echo "$o2"|tr '\n' '|')'" 'echo "$o2"|grep -q "^chunks: 0 listed$"&&! echo "$o2"|grep -q "^chunks: 2 listed$"'
cp $D/cardf $CARD;sed -i 's/chunks: c:[0-9a-f]\{12\}/chunks: c:zzzzzzzzzzzz/' $CARD;o3=$(EV agi-atom derive check 2>&1);rc3=$?
ok "f2c-negative-every-listed-chunk-id-resolves a chunks: id that no chunk names (c:zzzzzzzzzzzz) is a named line and rc != 0: '$(echo "$o3"|head -1)' rc $rc3" '[ $rc3 != 0 ]&&echo "$o3"|grep -q "^\[chunks\] a1: c:zzzzzzzzzzzz names a1 in no chunk$"'
nh f2l;printf 'credits_live: true\n'>$E/.agi/nodes/.geometry/secrets.md;(cd $E&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm live);UL o1 "an owner ask with no label" $T0>>$X;TAP>/dev/null;o4=$(EV agi-atom derive check 2>&1);rc4=$?
ok "f2b-red-once-the-atomizer-is-live with credits_live true and no row holding an ask+ack the live line is RED and rc != 0: '$(echo "$o4"|tail -1)' rc $rc4" '[ $rc4 != 0 ]&&echo "$o4"|grep -q "^done-when(4): 0 rows ask+ack, 1 owner chunks ? RED"'
echo "atom-edge: $f FAIL";exit $f
