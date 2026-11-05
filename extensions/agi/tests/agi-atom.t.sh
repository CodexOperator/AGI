#!/bin/sh
# agi-atom.t.sh [ROOT]: goal:g7.16.1.11.46.2 (M1) falsifier 1: `agi-atom add|close|grandfather` on a scratch card -- add-verbatim-ok, add-one-word-changed REFUSED, add-no-src REFUSED, close-to-real-id ok, close-to-absent-id REFUSED, close-outside-set REFUSED; mutants m1 (no substring check) m2 (close without the id check) m3 (close of a terminal row) must read RED.
# sh + awk + git on a scratch repo, no network, no root, 0 USD. ROOT = the tree whose engine-post.md carries the piece; PIECE=<file> tests a candidate instead. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf $D' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_ATOM_CARD AGI_ATOM_COMMIT
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
PC=${PIECE:-};[ -n "$PC" ]||{ awk '/^### agi-atom /{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/engine-post.md>$D/agi-atom;PC=$D/agi-atom;};[ -s "$PC" ]||{ echo "FAIL inputs: no agi-atom piece";exit 99;}
G="git -c user.name=t -c user.email=t@t -c commit.gpgsign=false"
mk(){ T=$D/$1/t;rm -rf $D/$1;mkdir -p $T/.agi/nodes/goal $T/.agi/nodes/doc $T/.agi/nodes/idea $T/.agi/sessions/quorum;cd $T;git init -q .
 printf -- '---\nid: goal:g1.2\n---\n# g\n' >.agi/nodes/goal/g1.2.md;printf -- '---\nid: doc:dd\n---\nl1\nl2\nl3\n' >.agi/nodes/doc/dd.md;printf -- '---\nid: idea:ii\n---\n# i\n' >.agi/nodes/idea/ii.md
 printf -- '---\nid: goal:g9\n---\n## OWNER 2026-10-23, verbatim\n> "Trajectory holds the momentum data"\nplain line two\n\n## Other\nnot owner words\n' >.agi/nodes/goal/g9.md
 printf '# card\n\n## §0 x\nhi\n\n## §7 ATOMS old\n\n**throw 1 (10-22) -- x**\n| # | atom (owner ask, short) | state |\n|---|---|---|\n| 1.1 | button down | target:§0 |\n| 1.2 | simplify | leaf:goal:g1.2 |\n' >.agi/sessions/quorum/p.md
 printf '# card2\n\n## §0 x\nhi\n' >.agi/sessions/quorum/q.md;$G add -A;$G commit -qm 'the owner said: build the thing now' ;H=$(git rev-parse HEAD);C=$T/.agi/sessions/quorum/p.md;}
A(){ (cd $T;env AGI_T=$T AGI_POST=${AP:-p} AGI_LAP=5 HOME=$D sh ${PIECE_RUN:-$PC} "$@") 2>$D/err;}
st(){ awk -F'|' -v i=$1 '{y=$2;gsub(/ /,"",y)}y==i&&NF==7{s=$5;gsub(/^ +| +$/,"",s);print s}' $C;}
# --- add
mk a;A grandfather;A add 'plain line two' src:goal:g9#OWNER>$D/o;ok "add-verbatim-ok a slice inside the node's OWNER verbatim section lands as a1 (got $(cat $D/o))" '[ "$(cat $D/o)" = a1 ]&&grep -qF "| a1 | \"plain line two\" | src:goal:g9#OWNER | target:? | lap5 |" $C'
A add 'Trajectory holds the momentum data' src:goal:g9#OWNER>$D/o;ok "add-second-row-increments the next row is a2 and the old rows are untouched" '[ "$(cat $D/o)" = a2 ]&&grep -qF "| 1.1 | \"button down\" | src:doc | target:§0 | lap5 |" $C'
A add 'Trajectory holds the momentum date' src:goal:g9#OWNER;rc=$?;ok "add-one-word-changed-REFUSED one word changed: refused (rc $rc), no a3 row" '[ $rc != 0 ]&&! grep -q "| a3 |" $C&&grep -q "^agi-atom: \[verbatim\]" $D/err'
A add 'not owner words' src:goal:g9#OWNER;rc=$?;ok "add-outside-owner-section-REFUSED a line of the node OUTSIDE its OWNER verbatim section: refused (rc $rc)" '[ $rc != 0 ]'
A add 'plain line two';rc=$?;ok "add-no-src-REFUSED no source argument: refused (rc $rc)" '[ $rc != 0 ]'
A add 'build the thing' foo;rc=$?;ok "add-bad-src-REFUSED a source that is neither src:<sha> nor src:<node>#OWNER: refused (rc $rc)" '[ $rc != 0 ]'
A add 'build the thing' src:$H>$D/o;ok "add-box-commit-ok a slice of a commit's message, src:<sha>: lands (got $(cat $D/o))" 'grep -qF "| \"build the thing\" | src:$H |" $C'
A add 'author' src:$H;rc=$?;ok "add-commit-headers-not-source a word that is only in the commit HEADERS (tree/author), not its message: refused (rc $rc)" '[ $rc != 0 ]'
A add 'plain | line' src:goal:g9#OWNER;rc=$?;ok "add-pipe-refused a slice with | would break the row: refused (rc $rc)" '[ $rc != 0 ]'
A add 'plain line two' src:goal:g9#OWNER;rc=$?;ok "add-duplicate-refused the same slice from the same source twice: refused (rc $rc)" '[ $rc != 0 ]'
mk b;AP=q A add 'plain line two' src:goal:g9#OWNER>$D/o;ok "add-creates-section a card with no §7 gets one with its header, then the row (got $(cat $D/o))" 'grep -q "^## §7" $T/.agi/sessions/quorum/q.md&&grep -q "^| a1 | " $T/.agi/sessions/quorum/q.md&&grep -q "^|---|---|---|---|---|" $T/.agi/sessions/quorum/q.md'
# --- close
mk c;A grandfather;A add 'plain line two' src:goal:g9#OWNER>/dev/null;A add 'Trajectory holds' src:goal:g9#OWNER>/dev/null;A add 'momentum data' src:goal:g9#OWNER>/dev/null;A add 'plain' src:goal:g9#OWNER>/dev/null
A close a1 leaf:g1.2;ok "close-to-real-id-ok a goal that exists: a1 -> leaf:g1.2 (state $(st a1))" '[ "$(st a1)" = leaf:g1.2 ]'
A close a2 idea:ii;ok "close-idea-ok an idea that exists (state $(st a2))" '[ "$(st a2)" = idea:ii ]'
A close a3 decision:dd#3;ok "close-decision-ok a doc line that exists (state $(st a3))" '[ "$(st a3)" = decision:dd#3 ]'
A close a4 out:not-wanted;ok "close-out-ok out:<reason> (state $(st a4))" '[ "$(st a4)" = out:not-wanted ]'
mk d;A grandfather;for w in 'plain line two' 'Trajectory holds' 'momentum data' 'plain' 'verbatim';do A add "$w" src:goal:g9#OWNER>/dev/null;done
A close a1 leaf:g777;rc=$?;ok "close-to-absent-leaf-REFUSED a goal id with no node: refused (rc $rc), a1 still $(st a1)" '[ $rc != 0 ]&&[ "$(st a1)" = target:? ]'
A close a1 idea:idea:nope;rc=$?;ok "close-to-absent-idea-REFUSED (rc $rc)" '[ $rc != 0 ]&&[ "$(st a1)" = target:? ]'
A close a1 decision:dd#99;rc=$?;ok "close-decision-line-past-the-end-REFUSED doc:dd has 7 lines, #99: refused (rc $rc)" '[ $rc != 0 ]&&[ "$(st a1)" = target:? ]'
A close a1 decision:nodoc#1;rc=$?;ok "close-to-absent-doc-REFUSED (rc $rc)" '[ $rc != 0 ]'
A close a1 done:yes;rc=$?;ok "close-outside-set-REFUSED a state outside the closed set: refused (rc $rc)" '[ $rc != 0 ]&&[ "$(st a1)" = target:? ]'
A close a1 moved:flow;rc=$?;ok "close-moved-is-moves-alone moved:<flow> by close: refused (rc $rc)" '[ $rc != 0 ]&&[ "$(st a1)" = target:? ]'
A close a1 out:;rc=$?;ok "close-empty-out-REFUSED out: with no reason: refused (rc $rc)" '[ $rc != 0 ]'
A close a9 out:x;rc=$?;ok "close-absent-row-REFUSED a row that is not there: refused (rc $rc)" '[ $rc != 0 ]'
A close a1 out:first;A close a1 leaf:g1.2;rc=$?;ok "close-terminal-REFUSED a closed row does not move again: refused (rc $rc), stays $(st a1)" '[ $rc != 0 ]&&[ "$(st a1)" = out:first ]'
A close 1.1 out:legacy;ok "close-grandfathered-row a src:doc row closes through the same state check (state $(st 1.1))" '[ "$(st 1.1)" = out:legacy ]'
# --- grandfather
mk e;A grandfather;cp $C $D/g1;A grandfather;ok "grandfather-idempotent the second run changes nothing" 'cmp -s $C $D/g1'
n=$(awk '/^## §7/,0' $C|grep -E '^\| (a[0-9]+|[0-9]+\.[0-9]+) \|'|grep -vc 'src:');ok "grandfather-every-row-has-a-source every §7 data row carries src: (rows without: $n)" '[ "$n" = 0 ]'
# --- mutants (each must be caught: the lane it breaks reads RED)
# FIX-FORWARD 2 (L93 council): grandfather stamps src:doc ONLY rows under a **throw ..** heading; a legacy N.N row elsewhere is refused by name and nothing is written
mk h;printf '# card\n\n## §7 ATOMS\n\n**throw 1 (10-22) -- x**\n| # | atom (owner ask, short) | state |\n|---|---|---|\n| 1.1 | button down | target:§0 |\n\n**throws 4-7 (10-23)**\n| 4.1 | four | target:§1 |\n\n**added 10-23 (council V10a decision)**\n| 8.1 | seat_status.py retire | target:§9 |\n' >$C;cp $C $D/h0;A grandfather;rc=$?
ok "grandfather-refuses-a-row-not-under-a-throw an N.N row under an 'added ...' heading is refused with the NAMED line, rc 2, the card unchanged (rc $rc, err: $(head -1 $D/err))" '[ "$rc" = 2 ]&&grep -qF "[src] 8.1 is not under a throw: give it its real src" $D/err&&cmp -s $C $D/h0'
mk i;printf '# card\n\n## §7 ATOMS\n\n**throw 1 (10-22) -- x**\n| # | atom (owner ask, short) | state |\n|---|---|---|\n| 1.1 | button down | target:§0 |\n\n**throws 4-7 (10-23)**\n| 4.1 | four | target:§1 |\n' >$C;A grandfather;rc=$?
ok "grandfather-stamps-throw-rows rows under **throw 1** and **throws 4-7** are stamped src:doc (rc $rc, rows $(grep -c '| src:doc |' $C))" '[ "$rc" = 0 ]&&[ "$(grep -c "| src:doc |" $C)" = 2 ]'
M=$D/m4;sed 's/;\[ -z "\$r" \]||d "\$r"$//' $PC>$M;mk j;printf '# card\n\n## §7 ATOMS\n\n**added 10-23 (x)**\n| 8.1 | seat_status.py retire | target:§9 |\n' >$C;PIECE_RUN=$M A grandfather;rc=$?
ok "m4-no-throw-scope-RED the mutant without the scope check STAMPS the 'added' row src:doc (rc $rc, stamped $(grep -c '| src:doc |' $C)): the refuse lane catches it" '[ "$rc" = 0 ]&&[ "$(grep -c "| src:doc |" $C)" = 1 ]&&! cmp -s $M $PC'
M=$D/m1;sed '/\[verbatim\]/d' $PC>$M;mk f;A grandfather;PIECE_RUN=$M A add 'Trajectory holds the momentum date' src:goal:g9#OWNER>/dev/null;rc=$?
ok "m1-no-substring-check-RED a piece without the substring check ACCEPTS the changed word (rc $rc): the add-one-word-changed lane catches it" '[ $rc = 0 ]'
M=$D/m2;sed 's/n "\$v"||d "\[state\] no goal node \$v";//' $PC>$M;mk g;A grandfather;A add 'plain line two' src:goal:g9#OWNER>/dev/null;PIECE_RUN=$M A close a1 leaf:g777;rc=$?
ok "m2-no-id-check-RED a piece without the goal-id check closes a1 to an absent goal (rc $rc): the close-to-absent-leaf lane catches it" '[ $rc = 0 ]'
M=$D/m3;awk '!z{k="*\"| target:\"*|*\"| red:\"*);;";i=index($0,k);if(i){$0=substr($0,1,i-1)"*);;"substr($0,i+length(k));z=1}}1' $PC>$M;mk h;A grandfather;A add 'plain line two' src:goal:g9#OWNER>/dev/null;A close a1 out:first;PIECE_RUN=$M A close a1 out:second;rc=$?
ok "m3-terminal-reopens-RED a piece that lets a closed row move again (answers rc $rc, want 0): the close-terminal lane catches it" '[ $rc = 0 ]'
echo "agi-atom.t.sh: $f FAIL";exit $f
