#!/bin/sh
# agi-turn.t.sh [ROOT]: goal:g7.16.1.11.11 AA1.V (E2 round 2, DG1 06:07Z; doc:rse-aa1-boxes AA1.V G1-G9 rewritten as a committed lane): every turn is ONE signed commit PER CHANGED NODE, made from the node's tiny tree onto posts/<P> by `agi-turn`; ~/t is a DETACHED read view of that tip; `agi-wt` pulls / creates / drops the trees; `agi-link` is gone.
# sh + git + ssh-keygen on SCRATCH repos: a fixture trunk, branch posts/alive, a DETACHED ~/t worktree, a throwaway ssh key, a RING (allowedSignersFile with `alive@agi`: a post's own config resolves no principal, so its commits verify U, not G: the ring is what makes %G? = G), HOME / RUNTIME_DIRECTORY / AGI_WT in tmp. Nothing live is touched.
# The pieces come from `sect agi-turn|agi-wt|agi-flush|agi-link` of the .geometry/engine*.md of ROOT (default the working tree), or of PIECES=<file> (a candidate: any file holding `### name` headings with ~~~ fences). Never from ~/bin (a post's ~/bin copy is extracted by name at its restart).
# Rows: g1 pull (a doc node: .p = its path; a build node: node + payload) · g2 no edit = no commit · g3 two trees edited = EXACTLY two commits, `alive: <node path>`, one node each (V4: the node file, or its payload paths, nothing else), %G? = G against the ring, doc:b untouched · g4 ~/t HEAD = the new tip, detached, shows the edit, no stderr · g5 a stray ~/t edit = [out-of-tree] on stderr, not committed, kept · g6 a tip moved since pull = the tip's version kept, mine on refs/archive/alive/<mint>, [moved], tree dropped; a SECOND move never destroys the first archived version · g7 `agi-wt new` lands a new node · g8 edit then drop = versioned then purged · g9 trunk untouched, 0 refs/grid · x1 a raced CAS is [raced], not retried · x2 agi-link gone · x3 agi-flush leaves ~/t on the tip · x4 AGI_POST unset fails closed (agi-wt rc 5 + its message, agi-turn rc != 0), nothing committed, the tree kept · x4b folded into the standing no-retired-variable test (goal:g7.16.1.11.46.11) · x5 agi-flush archives a moved tree end to end · x6 agi-flush exits 5 when a drop does · x7 a racer on posts/<P> (a plain turn): [raced], the tree kept, .b UNCHANGED, the next turn archives mine and the racer's change stays · x7b a raced node does not stop the turn (the next tree still lands on the racer's tip) · x8 a racer on the ARCHIVE ref: [raced] only, no [moved], the tree kept, the archive is the racer's. x9 a RACED `agi-wt drop` (rc 4, [raced], the tree kept, the tip the racer's, 0 archive refs; the next drop archives it [moved]) · x10 agi-flush with a racer (rc 0, only 5 counts; the edit is never purged: with ONE racer the final turn archives it) · x10b two racers (the drop, then the archive ref): the tree kept. A racer is a git shim on PATH ($T/racespec = one line per racer, "REF NODE MINT LETTER").
# v5 (AA1.V v5, DG1 17:26Z + 17:27Z, SM mur residues R1-R5): THE RULE: no tree is purged unless its turn PROVED its commit (add, write-tree, commit-tree, update-ref all checked); every failure keeps the tree, exits != 0 and prints a bracketed label (never [raced] unless the CAS missed). `.p` = ONE PATH PER LINE (g1, n7, n8); x3 no longer expects an unchanged tip (agi-flush ends with a CAS merge of the trunk, n6); x14d fails when agi-at is absent. New rows n1-n8 sit under the v5 banner at the end; every v4 row is kept.
T=$(mktemp -d);trap 'rm -rf $T' 0;f=0;G=/usr/bin/git;R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_WT RUNTIME_DIRECTORY AGI_TRUNK
export HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $T/hm $T/bin $T/shim $T/run $T/k
ssh-keygen -q -t ed25519 -N '' -f $T/k/alive -C alive >/dev/null||{ echo "FAIL fixture: ssh-keygen";exit 99;}
echo "alive@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/alive.pub)" >$T/allowed
for n in agi-turn agi-wt agi-flush agi-link agi-at agi-out agi-meter agi-notice agi-sync tick.sh grow.py;do sect $n >$T/bin/$n;if [ -s $T/bin/$n ];then chmod +x $T/bin/$n;else rm -f $T/bin/$n;fi;done
cat >$T/shim/git<<XX
#!/bin/sh
G=/usr/bin/git
if [ "\$1" = commit-tree ]&&[ -e $T/raceflag ];then rm -f $T/raceflag;t=\$(\$G -C $T/g rev-parse posts/alive);n=\$(\$G -C $T/g commit-tree -m racer -p \$t \$t^{tree});\$G -C $T/g update-ref refs/heads/posts/alive \$n;fi
# racespec = one line per racer, "REF NODE-PATH MINT LETTER": on the first update-ref of REF a racer gets in first (its line is consumed) -- it advances REF with a commit that changes that node to 'racer edit' (the real update-ref then fails on the old value)
if [ "\$1" = update-ref ]&&[ -s $T/racespec ]&&l=\$(grep -m1 "^\$2 " $T/racespec)&&[ -n "\$l" ];then
 rref=\$2;rpath=\$(echo "\$l"|cut -d' ' -f2);rmint=\$(echo "\$l"|cut -d' ' -f3);rid=\$(echo "\$l"|cut -d' ' -f4);grep -vxF "\$l" $T/racespec >$T/racespec.n;mv $T/racespec.n $T/racespec
  rt=\$(\$G -C $T/g rev-parse posts/alive);rx=$T/idx.race
  ro=\$(printf -- '---\\nid: doc:%s\\nmint_id: %s\\ntype: doc\\n---\\nbody %s\\nracer edit\\n' \$rid \$rmint \$rid|\$G -C $T/g hash-object -w --stdin)
  env GIT_INDEX_FILE=\$rx \$G -C $T/g read-tree \$rt;env GIT_INDEX_FILE=\$rx \$G -C $T/g update-index --cacheinfo 100644,\$ro,\$rpath;rn=\$(env GIT_INDEX_FILE=\$rx \$G -C $T/g write-tree);rm -f \$rx
  rcur=\$(\$G -C $T/g rev-parse -q --verify \$rref||:);rc=\$(echo racer|\$G -C $T/g commit-tree -p \${rcur:-\$rt} \$rn);\$G -C $T/g update-ref \$rref \$rc
 fi
# n3: a failing `git archive` (flag $T/failarchive). n5: postrace = one line per racer, "REF NODE MINT LETTER": AFTER the real update-ref of REF succeeds a racer advances REF (the pulled-in R3 window between update-ref and the .b write)
if [ "\$1" = archive ]&&[ -e $T/failarchive ];then echo "fatal: simulated git archive failure" >&2;exit 128;fi
# w0: a failing read-tree (flag $T/failreadtree)
if [ "\$1" = read-tree ]&&[ -e $T/failreadtree ];then echo "fatal: simulated read-tree failure" >&2;exit 128;fi
# k6: chk reads the tree through `git --work-tree=D diff --name-only` and `ls-files -o` (flags $T/faildiff, $T/faills): a failing one must KEEP the tree
case " \$* " in *" diff --name-only "*)[ -e $T/faildiff ]&&{ echo "fatal: simulated diff failure" >&2;exit 128;};; *" ls-files -o "*)[ -e $T/faills ]&&{ echo "fatal: simulated ls-files failure" >&2;exit 128;};; esac
# go8/ga6: a failing git diff-index (flag $T/faildi): grow.py reads the turn's NEW nodes through it, so it must FAIL CLOSED
case " \$* " in *" diff-index "*)[ -e $T/faildi ]&&{ echo "fatal: simulated diff-index failure" >&2;exit 128;};; esac
# k7: the trunk moves while merge-tree runs (flag $T/movetrunk); the args merge-tree got are recorded in $T/mt.args
if [ "\$1" = merge-tree ]&&[ -e $T/movetrunk ];then unlink $T/movetrunk;echo "\$*" >$T/mt.args;o=\$(\$G "\$@")||exit \$?;tt=\$(\$G -C $T/g rev-parse trunk);nn=\$(\$G -C $T/g commit-tree -m moved-late -p \$tt \$tt^{tree});\$G -C $T/g update-ref refs/heads/trunk \$nn;echo "\$o";exit 0;fi
if [ "\$1" = update-ref ]&&[ -s $T/postrace ]&&l=\$(grep -m1 "^\$2 " $T/postrace)&&[ -n "\$l" ];then
 grep -vxF "\$l" $T/postrace >$T/postrace.n;mv $T/postrace.n $T/postrace;\$G "\$@"||exit \$?
 sh $T/racer.sh \$2 "\$(echo "\$l"|cut -d' ' -f2)" "\$(echo "\$l"|cut -d' ' -f3)" "\$(echo "\$l"|cut -d' ' -f4)";exit 0
 fi
exec \$G "\$@"
XX
chmod +x $T/shim/git
cat >$T/racer.sh<<'XX'
G=/usr/bin/git;d=@T@/g;ref=$1;path=$2;mint=$3;id=$4;rx=$d.race2
rt=$($G -C $d rev-parse $ref);ro=$(printf -- '---\nid: doc:%s\nmint_id: %s\ntype: doc\n---\nbody %s\nracer edit\n' $id $mint $id|$G -C $d hash-object -w --stdin)
env GIT_INDEX_FILE=$rx $G -C $d read-tree $rt;env GIT_INDEX_FILE=$rx $G -C $d update-index --cacheinfo 100644,$ro,$path;rn=$(env GIT_INDEX_FILE=$rx $G -C $d write-tree);rm -f $rx
rc=$(echo racer|$G -C $d commit-tree -p $rt $rn);$G -C $d update-ref $ref $rc
XX
sed -i "s#@T@#$T#" $T/racer.sh
# n3b: a failing tar (flag $T/failtar)
cat >$T/shim/tar<<XX
#!/bin/sh
if [ -e $T/failtar ];then echo "tar: simulated extraction failure" >&2;exit 2;fi
exec /usr/bin/tar "\$@"
XX
chmod +x $T/shim/tar
MA=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;MB=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;MC=cccccccccccccccccccccccccccccccc
NA=.agi/nodes/doc/a.md;NB=.agi/nodes/doc/b.md;NC=.agi/nodes/build/c.md
# mk: a fresh fixture (trunk with doc:a, doc:b, build:c + src/c.sh + README.md; posts/alive = trunk; ~/t = a detached worktree of it; no trees)
mk(){ rm -rf $T/g $T/hm/t $T/wt $T/raceflag $T/racespec $T/failarchive $T/failtar $T/postrace $T/failreadtree $T/faildiff $T/faills $T/faildi $T/movetrunk $T/mt.args;mkdir -p $T/wt;$G init -q -b trunk $T/g;g="$G -C $T/g";$g config user.name alive;$g config user.email alive@agi;$g config gpg.format ssh;$g config user.signingkey $T/k/alive;$g config commit.gpgsign true
 mkdir -p $T/g/.agi/nodes/doc $T/g/.agi/nodes/build $T/g/src
 for n in a:$MA b:$MB;do k=${n%:*};m=${n#*:};printf -- '---\nid: doc:%s\nmint_id: %s\ntype: doc\n---\nbody %s\n' $k $m $k >$T/g/.agi/nodes/doc/$k.md;done
 printf -- '---\nid: build:c\nmint_id: %s\ntype: build\npayload_ref: src/c.sh\n---\nbuild c\n' $MC >$T/g/$NC;printf '#!/bin/sh\necho c\n' >$T/g/src/c.sh;echo readme >$T/g/README.md
 $g add -A;$g commit -qm trunk;$g branch posts/alive trunk;$g worktree add -q --detach $T/hm/t posts/alive;TR0=$($g rev-parse trunk);}
run(){ (cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 "$@");}
run0(){ (cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 "$@");}
tip(){ $G -C $T/g rev-parse posts/alive;}
sig(){ $G -C $T/g -c gpg.ssh.allowedSignersFile=$T/allowed log -1 --format=%G? $1;}
sigx(){ $G -C $T/g log -1 --format=%G? $1;}
# src: the text the unit and the pieces come from (PIECES=<file>, else ROOT's engine*.md); unitenv: the words of the agi-post@.service `Environment=` line that carries AGI_POST=%i (goal:g7.16.1.11.37), %i = alive
src(){ if [ -n "$PIECES" ];then cat "$PIECES";else cat $R0/.agi/nodes/.geometry/engine*.md;fi;}
unitline(){ src|grep -m1 '^Environment=.*AGI_POST=%i'|sed 's/^Environment=//;s/%i/alive/g';}
# runu CMD...: a piece under EXACTLY the unit's environment (every word of the Environment= line but PATH, which must find the fixture's pieces) -- NO AGI_POST of ours
runu(){ (cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 $(unitline|tr ' ' '\n'|grep -v '^PATH=') "$@");}
# runh CMD...: from $HOME (agi-out's cd) with AGI_POST (the unit's one identity variable, goal:g7.16.1.11.37)
runh(){ (cd $T/hm&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm USER=agi-alive GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 AGI_POST=alive "$@");}
# mkr: mk + a ring (alive's three lines + bob's) committed on posts/alive, an old ~/.ssh key and a newer ~/.fresh: agi-out's out-line has work to do
mkr(){ mk;R=.agi/nodes/.geometry/ring;mkdir -p $T/hm/t/.agi/nodes/.geometry $T/hm/.ssh;printf 'alive ssh-ed25519 AAAAold\nalive pq-sha256 oldpq\nalive x25519 oldseal\nbob ssh-ed25519 AAAAbob\n' >$T/hm/t/$R;$G -C $T/hm/t add -A;$G -C $T/hm/t commit -qm ring;$G -C $T/g update-ref refs/heads/posts/alive $($G -C $T/hm/t rev-parse HEAD)
 ssh-keygen -q -t ed25519 -N '' -f $T/hm/.ssh/id_ed25519 -C old >/dev/null;touch -d '2026-01-01' $T/hm/.ssh/id_ed25519;touch $T/hm/.fresh;}
[ -s $T/bin/agi-turn ]&&[ -s $T/bin/agi-wt ]&&[ -s $T/bin/agi-at ]&&[ -s $T/bin/grow.py ]||{ echo "FAIL extract: agi-turn $(wc -c <$T/bin/agi-turn 2>/dev/null) B, agi-wt $(wc -c <$T/bin/agi-wt 2>/dev/null) B, agi-at $(wc -c <$T/bin/agi-at 2>/dev/null) B, grow.py $(wc -c <$T/bin/grow.py 2>/dev/null) B in ${PIECES:-ROOT}";exit 99;}
# mkgo (used by the rows that land a NEW node, and by the go rows at the end): mk + a scratch repo that carries the engine's own extensions/agi/{bin,src}, .agi/context/schemas and a tiny corpus, so the growth-order check can run from ~/t
mkgo(){ mk;mkdir -p $T/g/extensions/agi $T/g/.agi/context $T/g/.agi/nodes/goal $T/g/.agi/nodes/hypothesis $T/g/.agi/nodes/experiment;cp -r $R0/extensions/agi/bin $R0/extensions/agi/src $T/g/extensions/agi/;cp -r $R0/.agi/context/schemas $T/g/.agi/context/
 printf -- '---\nid: goal:g1\nmint_id: 000000000000000000000000000000a1\ntype: goal\nparents: []\n---\nroot goal\n' >$T/g/.agi/nodes/goal/g1.md
 printf -- '---\nid: hypothesis:h1\nmint_id: 000000000000000000000000000000b1\ntype: hypothesis\nparents:\n  - goal:g1\n---\na hypothesis\n' >$T/g/.agi/nodes/hypothesis/h1.md
 printf -- '---\nid: experiment:x1\nmint_id: 000000000000000000000000000000c1\ntype: experiment\nparents:\n  - goal:g1\n---\nlegacy experiment\n' >$T/g/.agi/nodes/experiment/x1.md
 mkdir -p $T/g/.agi/nodes/idea;printf -- '---\nid: idea:i1\nmint_id: 000000000000000000000000000000f1\ntype: idea\nparents:\n  - goal:g1\n---\nan idea\n' >$T/g/.agi/nodes/idea/i1.md
 $G -C $T/g add -A;$G -C $T/g commit -qm "engine + corpus";$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive;TR0=$($G -C $T/g rev-parse trunk);}
# --- g1 pull
mk;da=$(run agi-wt pull doc:a 2>$T/e1);dc=$(run agi-wt pull build:c 2>>$T/e1);pa=$(cat $da/.p 2>/dev/null);pc=$(tr "\n" "|" <$dc/.p 2>/dev/null);la=$(wc -l <$da/.p|tr -d " ");lc=$(wc -l <$dc/.p|tr -d " ")
ok "g1-pull-a-doc-node the tree of doc:a is $T/wt/<mint> (got [${da#$T/}]); .p = [$pa] (want exactly the node path); the node file is in it" '[ "$da" = $T/wt/$MA ]&&[ "$pa" = "$NA" ]&&[ "$la" = 1 ]&&[ -f $da/$NA ]'
ok "g1-pull-a-build-node the tree of build:c: .p = [$pc] (v5: ONE PATH PER LINE: want $NC|src/c.sh| over 2 lines); the node file and src/c.sh are in it" '[ "$dc" = $T/wt/$MC ]&&[ "$pc" = "$NC|src/c.sh|" ]&&[ "$lc" = 2 ]&&[ -f $dc/$NC ]&&[ -f $dc/src/c.sh ]'
# --- g2 no edit
b0=$(tip);run agi-turn 2>$T/e2;rc=$?
ok "g2-no-edit-no-commit a turn with two clean trees: rc $rc (want 0), tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no), stderr [$(cat $T/e2)] (want empty)" '[ $rc = 0 ]&&[ $(tip) = $b0 ]&&[ ! -s $T/e2 ]'
# --- g3 two trees edited
echo "edit a" >>$da/$NA;echo "# c2" >>$dc/src/c.sh;b0=$(tip);run agi-turn 2>$T/e3;rc3=$?;nc=$($G -C $T/g rev-list --count $b0..posts/alive);cs=$($G -C $T/g rev-list --reverse $b0..posts/alive)
sa=;sc=;fa=;fc=;for c in $cs;do s=$($G -C $T/g log -1 --format=%s $c);fl=$($G -C $T/g diff-tree --no-commit-id --name-only -r $c|tr '\n' ' ');case $s in "alive: $NA")sa=$c;fa=$fl;;"alive: $NC")sc=$c;fc=$fl;;esac;done
ok "g3-two-commits two trees edited in one turn: rc $rc3, $nc new commit(s) on posts/alive (want exactly 2), linear: $($G -C $T/g rev-list --merges $b0..posts/alive|wc -l|tr -d ' ') merge(s) (want 0)" '[ $rc3 = 0 ]&&[ $nc = 2 ]&&[ $($G -C $T/g rev-list --merges $b0..posts/alive|wc -l|tr -d " ") = 0 ]'
ok "g3-named-for-its-node the subjects are [alive: $NA] and [alive: $NC]: found a ${sa:+yes}${sa:-NO}, c ${sc:+yes}${sc:-NO}" '[ -n "$sa" ]&&[ -n "$sc" ]'
ok "g3-v4-one-node-each (V4) doc:a changed [${fa:-none}] (want only $NA); build:c changed [${fc:-none}] (want only src/c.sh: its payload, its node file is unchanged); doc:b untouched: $($G -C $T/g diff --quiet $b0 posts/alive -- $NB&&echo yes||echo NO)" '[ "$fa" = "$NA " ]&&[ "$fc" = "src/c.sh " ]&&$G -C $T/g diff --quiet $b0 posts/alive -- $NB'
ok "g3-signed-G both commits verify %G? = G against the ring fixture: a [$([ -n "$sa" ]&&sig $sa)], c [$([ -n "$sc" ]&&sig $sc)] (want G, G); with NO ring the same commits read [$([ -n "$sa" ]&&sigx $sa)] (the trap: U)" '[ -n "$sa" ]&&[ -n "$sc" ]&&[ "$(sig $sa)" = G ]&&[ "$(sig $sc)" = G ]'
# --- g4 the read view
ok "g4-read-view-is-the-tip after the turn ~/t HEAD = posts/alive: $([ "$($G -C $T/hm/t rev-parse HEAD)" = "$(tip)" ]&&echo yes||echo NO), DETACHED: $($G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&echo NO||echo yes), the edit is visible in ~/t: $(grep -c 'edit a' $T/hm/t/$NA) (want 1), g3 turn stderr [$(cat $T/e3)] (want empty)" '[ "$($G -C $T/hm/t rev-parse HEAD)" = "$(tip)" ]&&! $G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&[ "$(grep -c "edit a" $T/hm/t/$NA)" = 1 ]&&[ ! -s $T/e3 ]'
# --- g5 a stray edit in ~/t
echo stray >>$T/hm/t/README.md;b0=$(tip);run agi-turn 2>$T/e5
ok "g5-stray-edit-is-out-of-tree a direct edit in ~/t: stderr [$(cat $T/e5|cut -c1-90)] (want [out-of-tree]); tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no); the edit kept in ~/t: $(grep -c stray $T/hm/t/README.md) (want 1)" 'grep -q "\[out-of-tree\]" $T/e5&&[ $(tip) = $b0 ]&&[ "$(grep -c stray $T/hm/t/README.md)" = 1 ]'
# --- g9 (on the g3/g5 state)
ok "g9-trunk-untouched-no-refs-grid after g1-g5: trunk is $([ "$($G -C $T/g rev-parse trunk)" = "$TR0" ]&&echo unchanged||echo MOVED), refs/grid refs: $($G -C $T/g for-each-ref refs/grid|wc -l|tr -d ' ') (want 0)" '[ "$($G -C $T/g rev-parse trunk)" = "$TR0" ]&&[ -z "$($G -C $T/g for-each-ref refs/grid)" ]'
# --- g6 a tip moved since pull
mv_b(){ x=$T/idx.mv;t=$(tip);GIT_INDEX_FILE=$x $G -C $T/g read-tree $t;printf -- '---\nid: doc:b\nmint_id: %s\ntype: doc\n---\nbody b\nmerged %s\n' $MB $1 >$T/b.new;o=$($G -C $T/g hash-object -w $T/b.new);GIT_INDEX_FILE=$x $G -C $T/g update-index --cacheinfo 100644,$o,$NB;n=$(GIT_INDEX_FILE=$x $G -C $T/g write-tree);c=$(echo "merge $1"|$G -C $T/g commit-tree -p $t $n);$G -C $T/g update-ref refs/heads/posts/alive $c $t;rm -f $x;$G -C $T/hm/t checkout -q --detach posts/alive;}
mk;db=$(run agi-wt pull doc:b);mv_b one;echo "mine one" >>$db/$NB;b1=$(tip);run agi-turn 2>$T/e6;AR=refs/archive/alive/$MB;a1=$($G -C $T/g rev-parse -q --verify $AR||echo none)
ok "g6-moved-keeps-the-tip-archives-mine doc:b pulled, then changed on the tip, then edited in its tree: the tip is $([ $(tip) = $b1 ]&&echo kept||echo MOVED) (want kept), tip's b has 'mine': $($G -C $T/g show posts/alive:$NB|grep -c 'mine one') (want 0), $AR holds mine: $([ $a1 != none ]&&$G -C $T/g show $AR:$NB|grep -c 'mine one'||echo no-ref) (want 1)" '[ $(tip) = $b1 ]&&[ "$($G -C $T/g show posts/alive:$NB|grep -c "mine one")" = 0 ]&&[ $a1 != none ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine one")" = 1 ]'
ok "g6-moved-is-reported-and-the-tree-dropped stderr [$(cat $T/e6|cut -c1-80)] (want [moved] naming the node); the tree $db exists: $([ -d $db ]&&echo YES||echo no) (want no)" 'grep -q "\[moved\]" $T/e6&&[ ! -d $db ]'
db=$(run agi-wt pull doc:b);mv_b two;echo "mine two" >>$db/$NB;run agi-turn 2>$T/e6b;a2=$($G -C $T/g rev-parse -q --verify $AR||echo none)
ok "g6-second-move-never-overwrites-the-first the same node moved AGAIN: the first archived version $a1 is still reachable from $AR (now $a2): $($G -C $T/g rev-list $AR 2>/dev/null|grep -c "^$a1\$") (want 1); the second version is on it too: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'mine two') (want 1)" '[ $a1 != none ]&&[ "$($G -C $T/g rev-list $AR|grep -c "^$a1\$")" = 1 ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine two")" = 1 ]'
# --- g7 agi-wt new
mkgo;nd=$(run agi-wt new .agi/nodes/doc/n.md 2>$T/e7);mkdir -p $nd/.agi/nodes/doc;printf -- '---\nid: doc:n\nmint_id: nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\ntype: doc\nparents:\n  - goal:g1\n---\nnew\n' >$nd/.agi/nodes/doc/n.md;b0=$(tip);run agi-turn 2>$T/e7b;nc=$($G -C $T/g rev-list --count $b0..posts/alive)
ok "g7-new-node-lands agi-wt new + a node written in its tree: $nc new commit(s) (want 1), subject [$($G -C $T/g log -1 --format=%s posts/alive)] (want alive: .agi/nodes/doc/n.md), the node is on posts/alive: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/doc/n.md&&echo yes||echo NO), signed: [$(sig posts/alive)]" '[ $nc = 1 ]&&[ "$($G -C $T/g log -1 --format=%s posts/alive)" = "alive: .agi/nodes/doc/n.md" ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/doc/n.md&&[ "$(sig posts/alive)" = G ]'
# --- g8 edit then drop
mk;da=$(run agi-wt pull doc:a);echo "drop edit" >>$da/$NA;b0=$(tip);run agi-wt drop doc:a 2>$T/e8;rc=$?
ok "g8-edit-then-drop-versions-then-purges agi-wt drop: rc $rc (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1) with the edit: $($G -C $T/g show posts/alive:$NA|grep -c 'drop edit') (want 1), the tree exists: $([ -d $da ]&&echo YES||echo no) (want no), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0: a drop that lands on the tip archives nothing)" '[ $rc = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "drop edit")" = 1 ]&&[ ! -d $da ]&&[ -z "$($G -C $T/g for-each-ref refs/archive)" ]'
# --- g8b (V4, old test_agi_wt_archive f2) a CLEAN drop: the tree goes, no commit, NO refs/archive ref
mk;da=$(run agi-wt pull doc:a);b0=$(tip);run agi-wt drop doc:a 2>$T/e8b;rc=$?
ok "g8b-a-clean-drop-purges-and-makes-no-archive-ref pull then drop with no edit: rc $rc (want 0), the tree exists: $([ -d $da ]&&echo YES||echo no) (want no), the tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0), stderr [$(cat $T/e8b)] (want empty)" '[ $rc = 0 ]&&[ ! -d $da ]&&[ $(tip) = $b0 ]&&[ -z "$($G -C $T/g for-each-ref refs/archive)" ]&&[ ! -s $T/e8b ]'
# --- x1 a raced CAS
mk;da=$(run agi-wt pull doc:a);echo "race edit" >>$da/$NA;b0=$(tip);: >$T/raceflag;run agi-turn 2>$T/ex1;mine=$($G -C $T/g log --format=%s posts/alive|grep -c "alive: $NA")
ok "x1-raced-cas-is-reported-not-retried a second writer moves posts/alive between the read and the update: stderr [$(cat $T/ex1|cut -c1-60)] (want [raced]); the racer's commit is the tip: $([ "$($G -C $T/g log -1 --format=%s posts/alive)" = racer ]&&echo yes||echo NO) (want yes); my commit on the branch: $mine (want 0: no retry, no overwrite)" 'grep -q "\[raced\]" $T/ex1&&[ "$($G -C $T/g log -1 --format=%s posts/alive)" = racer ]&&[ $mine = 0 ]'
# --- x2 agi-link retired
nl=$(cat $T/bin/*|grep -c agi-link||true)
ok "x2-agi-link-is-gone the piece agi-link is $([ -f $T/bin/agi-link ]&&echo PRESENT||echo absent) (want absent) and the pieces agi-turn / agi-wt / agi-flush name it $nl time(s) (want 0)" '[ ! -f $T/bin/agi-link ]&&[ "$nl" = 0 ]'
# --- x3 agi-flush on the detached view: trunk diverged from the tip
mk;da=$(run agi-wt pull doc:a);echo "flush edit" >>$da/$NA;run agi-turn 2>/dev/null;g="$G -C $T/g";echo "trunk side" >$T/g/trunk-only.txt;$g add trunk-only.txt;$g commit -qm trunkside;t1=$(tip);run agi-flush 2>$T/ex3;rc=$?;h=$($G -C $T/hm/t rev-parse HEAD)
ok "x3-agi-flush-leaves-the-read-view-on-the-tip trunk has a commit the tip lacks; agi-flush: rc $rc (want 0), the tip is $([ $(tip) = $t1 ]&&echo unchanged||echo MOVED) (v5: MOVED, flush ends with the CAS merge of the trunk, see n6a), ~/t HEAD $([ $h = $(tip) ]&&echo = the tip||echo != the tip: a commit nobody references) (want = the tip), merge in progress: $([ -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&echo YES||echo no)" '[ $rc = 0 ]&&[ $h = $(tip) ]&&[ ! -e $T/g/.git/worktrees/t/MERGE_HEAD ]'
# --- x4 AGI_POST unset
mk;da=$(run agi-wt pull doc:a);echo "nopost edit" >>$da/$NA;b0=$(tip);run0 agi-wt drop doc:a 2>$T/ex4;rc=$?;run0 agi-turn 2>$T/ex4b;rt=$?
ok "x4-no-post-fails-closed AGI_POST unset: agi-wt drop rc $rc (want 5) and stderr [$(cat $T/ex4|cut -c1-70)] (want 'no AGI_POST ... not archived'); agi-turn rc $rt (want != 0); nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO); the tree and its edit kept: $(grep -c 'nopost edit' $da/$NA 2>/dev/null||echo 0) (want 1)" '[ $rc = 5 ]&&grep -q "no AGI_POST" $T/ex4&&[ $rt != 0 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "nopost edit" $da/$NA)" = 1 ]'
# --- x5 agi-flush archives a moved tree end to end (replaces test_agi_wt_archive m3)
mk;db=$(run agi-wt pull doc:b);mv_b one;echo "mine flush" >>$db/$NB;b1=$(tip);run agi-flush 2>$T/ex5;rc=$?;AR=refs/archive/alive/$MB
ok "x5-agi-flush-archives-a-moved-tree agi-flush with a tree whose node moved on the tip: rc $rc (want 0), the tip kept: $([ $(tip) = $b1 ]&&echo yes||echo NO), $AR holds mine: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'mine flush') (want 1), [moved] on stderr: $(grep -c '\[moved\]' $T/ex5) (want 1), the tree dropped: $([ -d $db ]&&echo NO||echo yes)" '[ $rc = 0 ]&&[ $(tip) = $b1 ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine flush")" = 1 ]&&[ "$(grep -c "\[moved\]" $T/ex5)" = 1 ]&&[ ! -d $db ]'
# --- x6 agi-flush carries rc 5 (replaces test_agi_wt_archive g83)
mk;da=$(run agi-wt pull doc:a);echo "flush nopost" >>$da/$NA;b0=$(tip);run0 agi-flush 2>$T/ex6;rc=$?
ok "x6-agi-flush-exits-5-when-a-drop-exits-5 AGI_POST unset: agi-flush rc $rc (want 5), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO), the tree and its edit kept: $(grep -c 'flush nopost' $da/$NA 2>/dev/null||echo 0) (want 1)" '[ $rc = 5 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "flush nopost" $da/$NA)" = 1 ]'
# --- x7 a racer on posts/<P> during a plain turn (DG1 12:43Z A): [raced], the tree kept, .b UNCHANGED, the racer's change survives the NEXT turn
mk;da=$(run agi-wt pull doc:a);echo "mine A" >>$da/$NA;b0=$(tip);echo "refs/heads/posts/alive $NA $MA a" >$T/racespec;run agi-turn 2>$T/ex7;t1=$(tip);bb=$(cat $da/.b 2>/dev/null)
ok "x7-a-racer-on-the-branch-is-raced-and-leaves-the-pull-marker-alone a racer advances posts/alive at the CAS: stderr [$(cat $T/ex7|cut -c1-50)] (want [raced] and no [moved]); the tip is the racer's: $($G -C $T/g show posts/alive:$NA|grep -c 'racer edit') (want 1, mine 0: $($G -C $T/g show posts/alive:$NA|grep -c 'mine A')); the tree $da kept: $([ -d $da ]&&echo yes||echo NO); .b is the pull tip $b0: [${bb:-none}] (want unchanged, NOT the racer's tip $t1)" 'grep -q "\[raced\]" $T/ex7&&! grep -q "\[moved\]" $T/ex7&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine A")" = 0 ]&&[ -d $da ]&&[ "$bb" = "$b0" ]&&[ "$bb" != "$t1" ]'
run agi-turn 2>$T/ex7b;AR=refs/archive/alive/$MA
ok "x7-the-next-turn-archives-mine-and-the-racers-change-stays the next turn (no racer): stderr [$(cat $T/ex7b|cut -c1-50)] (want [moved]); the tip still carries the racer's change: $($G -C $T/g show posts/alive:$NA|grep -c 'racer edit') (want 1) and not mine: $($G -C $T/g show posts/alive:$NA|grep -c 'mine A') (want 0); $AR holds mine: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine A') (want 1); the tree dropped: $([ -d $da ]&&echo NO||echo yes)" 'grep -q "\[moved\]" $T/ex7b&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine A")" = 0 ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine A")" = 1 ]&&[ ! -d $da ]'
# --- x7b a raced node does not stop the turn: the next tree in the same turn still lands, on top of the racer's tip
mk;da=$(run agi-wt pull doc:a);dc=$(run agi-wt pull build:c);echo "mine A2" >>$da/$NA;echo "# c3" >>$dc/src/c.sh;b0=$(tip);echo "refs/heads/posts/alive $NA $MA a" >$T/racespec;run agi-turn 2>$T/ex7c;t1=$(tip)
ok "x7b-a-raced-node-does-not-stop-the-turn doc:a is raced (racer first), build:c is the next tree: stderr [$(cat $T/ex7c|cut -c1-40)] (want [raced]); build:c landed: $($G -C $T/g log --format=%s $b0..posts/alive|grep -c "alive: $NC") commit (want 1) on the racer's tip: parent has 'racer edit': $($G -C $T/g show $t1~1:$NA|grep -c 'racer edit') (want 1); src/c.sh on the tip has the edit: $($G -C $T/g show posts/alive:src/c.sh|grep -c 'c3') (want 1); doc:a's tree kept: $([ -d $da ]&&echo yes||echo NO); .b of build:c = the new tip: $([ "$(cat $dc/.b 2>/dev/null)" = "$t1" ]&&echo yes||echo NO)" 'grep -q "\[raced\]" $T/ex7c&&[ "$($G -C $T/g log --format=%s $b0..posts/alive|grep -c "alive: $NC")" = 1 ]&&[ "$($G -C $T/g show $t1~1:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show posts/alive:src/c.sh|grep -c c3)" = 1 ]&&[ -d $da ]&&[ "$(cat $dc/.b)" = "$t1" ]'
# --- x8 a racer on the ARCHIVE ref (DG1 12:43Z B): [raced] only, no [moved], the tree kept, the archive is the racer's
mk;db=$(run agi-wt pull doc:b);mv_b one;echo "mine B" >>$db/$NB;b1=$(tip);AR=refs/archive/alive/$MB;echo "$AR $NB $MB b" >$T/racespec;run agi-turn 2>$T/ex8
ok "x8-a-racer-on-the-archive-ref-is-raced-not-moved the node moved on the tip since pull AND a racer creates $AR first: stderr [$(cat $T/ex8|cut -c1-50)] (want [raced] only), [moved] lines: $(grep -c '\[moved\]' $T/ex8) (want 0); the tree $db kept: $([ -d $db ]&&echo yes||echo NO) with its edit: $(grep -c 'mine B' $db/$NB 2>/dev/null||echo 0) (want 1); the archive is the racer's: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'racer edit') (want 1, mine: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'mine B')); the tip kept: $([ $(tip) = $b1 ]&&echo yes||echo NO)" 'grep -q "\[raced\]" $T/ex8&&[ "$(grep -c "\[moved\]" $T/ex8)" = 0 ]&&[ -d $db ]&&[ "$(grep -c "mine B" $db/$NB)" = 1 ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine B")" = 0 ]&&[ $(tip) = $b1 ]'
# --- x9 a RACED drop keeps the tree (DG1 13:15Z D): `agi-wt drop` = agi-turn && purge; agi-turn exits 4 after a [raced], so the purge does not run
mk;da=$(run agi-wt pull doc:a);echo "mine D" >>$da/$NA;b0=$(tip);echo "refs/heads/posts/alive $NA $MA a" >$T/racespec;run agi-wt drop doc:a 2>$T/ex9;rc9=$?;t1=$(tip);bb=$(cat $da/.b 2>/dev/null);na=$($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ');k1=$([ -d $da ]&&echo yes||echo NO);e1=$(grep -c 'mine D' $da/$NA 2>/dev/null||echo 0)
run agi-wt drop doc:a 2>$T/ex9b;rc9b=$?;AR=refs/archive/alive/$MA
ok "x9-a-raced-drop-keeps-the-tree-and-the-next-drop-archives-it a racer advances posts/alive during agi-wt drop: rc $rc9 (want 4), stderr [$(cat $T/ex9|cut -c1-40)] (want [raced]); the tree $da kept: $k1 with its edit: $e1 (want 1); the tip is the racer's: $([ $t1 != $b0 ]&&[ "$($G -C $T/g show $t1:$NA|grep -c 'racer edit')" = 1 ]&&echo yes||echo NO), untouched by mine: $($G -C $T/g show $t1:$NA|grep -c 'mine D') (want 0); archive refs: $na (want 0); .b unchanged: $([ "$bb" = "$b0" ]&&echo yes||echo NO). THEN drop again, no racer: rc $rc9b (want 0), [moved] $(grep -c '\[moved\]' $T/ex9b) (want 1), the tree gone: $([ -d $da ]&&echo NO||echo yes), $AR holds mine: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine D') (want 1), the tip still has the racer's change, not mine: $($G -C $T/g show posts/alive:$NA|grep -c 'racer edit')/$($G -C $T/g show posts/alive:$NA|grep -c 'mine D') (want 1/0)" '[ $rc9 = 4 ]&&grep -q "\[raced\]" $T/ex9&&[ $k1 = yes ]&&[ $e1 = 1 ]&&[ $t1 != $b0 ]&&[ "$($G -C $T/g show $t1:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show $t1:$NA|grep -c "mine D")" = 0 ]&&[ $na = 0 ]&&[ "$bb" = "$b0" ]&&[ $rc9b = 0 ]&&[ "$(grep -c "\[moved\]" $T/ex9b)" = 1 ]&&[ ! -d $da ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine D")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine D")" = 0 ]'
# --- x10 agi-flush with a racer: rc 0 and my edit is never purged
# one racer: the drop is raced (tree kept), flush's FINAL agi-turn (no racer left) archives it [moved]: the edit survives on the archive ref
mk;da=$(run agi-wt pull doc:a);echo "mine F" >>$da/$NA;echo "refs/heads/posts/alive $NA $MA a" >$T/racespec;run agi-flush 2>$T/ex10;rc10=$?;AR=refs/archive/alive/$MA
kept=$(grep -c 'mine F' $da/$NA 2>/dev/null||echo 0);arch=$($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine F')
ok "x10-agi-flush-with-a-racer-never-loses-the-edit one racer on posts/alive: agi-flush rc $rc10 (want 0: a raced 4 is ignored, only 5 counts), [raced] $(grep -c '\[raced\]' $T/ex10) (want 1); my edit survives: in the tree $kept, on $AR $arch (want exactly one of them 1: the tree kept, or archived by the final turn); the tip is the racer's, not mine: $($G -C $T/g show posts/alive:$NA|grep -c 'racer edit')/$($G -C $T/g show posts/alive:$NA|grep -c 'mine F') (want 1/0)" '[ $rc10 = 0 ]&&[ "$(grep -c "\[raced\]" $T/ex10)" = 1 ]&&[ $((kept+arch)) = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine F")" = 0 ]'
# archive racers: agi-flush's FINAL turn is tried up to THREE times (agi-turn||agi-turn||agi-turn). One racer on posts/alive takes the drop; each racer line on the ARCHIVE ref then costs the final turn one attempt. Lines differ (the 4th word) so the shim consumes ONE per update-ref.
AR=refs/archive/alive/$MA
fl(){ mk;da=$(run agi-wt pull doc:a);echo "mine $1" >>$da/$NA;{ echo "refs/heads/posts/alive $NA $MA a";[ $2 -ge 1 ]&&echo "$AR $NA $MA b";[ $2 -ge 2 ]&&echo "$AR $NA $MA c";[ $2 -ge 3 ]&&echo "$AR $NA $MA d";:;} >$T/racespec;run agi-flush 2>$T/exf;rcf=$?;}
# ONE archive racer: the 2nd attempt commits ([moved], the archive holds mine on top of the racer's), rc 0, the tree gone
fl F2 1
ok "x10b-agi-flush-retries-the-final-turn one racer on posts/alive (the drop) and one on $AR (the final turn's 1st attempt): agi-flush rc $rcf (want 0), [raced] $(grep -c '\[raced\]' $T/exf) (want 2), [moved] $(grep -c '\[moved\]' $T/exf) (want 1); the tree gone: $([ -d $da ]&&echo NO||echo yes); $AR holds mine on top: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine F2') (want 1), the racer's commit under it: $($G -C $T/g show $AR~1:$NA 2>/dev/null|grep -c 'racer edit') (want 1)" '[ $rcf = 0 ]&&[ "$(grep -c "\[raced\]" $T/exf)" = 2 ]&&[ "$(grep -c "\[moved\]" $T/exf)" = 1 ]&&[ ! -d $da ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine F2")" = 1 ]&&[ "$($G -C $T/g show $AR~1:$NA|grep -c "racer edit")" = 1 ]'
# TWO archive racers: the 3rd (last) attempt commits, rc 0 (pins that there ARE three attempts)
fl F3 2
ok "x10c-agi-flush-has-three-attempts two racers on $AR: agi-flush rc $rcf (want 0), [raced] $(grep -c '\[raced\]' $T/exf) (want 3), [moved] $(grep -c '\[moved\]' $T/exf) (want 1), the tree gone: $([ -d $da ]&&echo NO||echo yes), $AR holds mine: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine F3') (want 1)" '[ $rcf = 0 ]&&[ "$(grep -c "\[raced\]" $T/exf)" = 3 ]&&[ "$(grep -c "\[moved\]" $T/exf)" = 1 ]&&[ ! -d $da ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine F3")" = 1 ]'
# FOUR raced attempts (the drop-era count is kept: 1 + 3): exit 4, the tree KEPT with its edit, AND (v5d, DG1 ruling (2)) the leftover tree goes WHOLE onto the archive ref on top of the racer's: a kept tree is a ref, not only a RAM dir
fl F4 3
ok "x10d-agi-flush-exits-4-keeps-the-tree-and-saves-it-whole-when-every-attempt-is-raced all four attempts raced: agi-flush rc $rcf (want 4), [raced] $(grep -c '\[raced\]' $T/exf) (want 4), [moved] $(grep -c '\[moved\]' $T/exf) (want 0), [kept] $(grep -c '^\[kept\]' $T/exf) (want 1); the tree $da kept: $([ -d $da ]&&echo yes||echo NO) with its edit: $(grep -c 'mine F4' $da/$NA 2>/dev/null||echo 0) (want 1); $AR holds mine on top: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine F4') (want 1), the racer's commit under it: $($G -C $T/g show $AR~1:$NA 2>/dev/null|grep -c 'racer edit') (want 1)" '[ $rcf = 4 ]&&[ "$(grep -c "\[raced\]" $T/exf)" = 4 ]&&[ "$(grep -c "\[moved\]" $T/exf)" = 0 ]&&[ "$(grep -c "^\[kept\]" $T/exf)" = 1 ]&&[ -d $da ]&&[ "$(grep -c "mine F4" $da/$NA)" = 1 ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine F4")" = 1 ]&&[ "$($G -C $T/g show $AR~1:$NA|grep -c "racer edit")" = 1 ]'
# a drop that exits 5 wins over everything: agi-flush exit 5
mk;da=$(run agi-wt pull doc:a);echo "mine F5" >>$da/$NA;echo "refs/heads/posts/alive $NA $MA a" >$T/racespec;run0 agi-flush 2>$T/exf5;rcf5=$?
ok "x10e-agi-flush-exit-5-still-wins AGI_POST unset (the drop exits 5): agi-flush rc $rcf5 (want 5), the tree and its edit kept: $(grep -c 'mine F5' $da/$NA 2>/dev/null||echo 0) (want 1)" '[ $rcf5 = 5 ]&&[ "$(grep -c "mine F5" $da/$NA)" = 1 ]'
# --- x11 (V1) the UNIT's own Environment= line (engine-root.md, the one with AGI_POST=%i, %i = alive) is enough for the pieces: NO AGI_POST of ours
mk;ul=$(unitline);b0=$(tip)
da=$(runu agi-wt pull doc:a 2>$T/e11);prc=$?;echo "mine U1" >>$da/$NA;runu agi-turn 2>>$T/e11;trc=$?;c1=$($G -C $T/g rev-list --count $b0..posts/alive)
echo "mine U2" >>$da/$NA;runu agi-wt drop doc:a 2>>$T/e11;drc=$?;c2=$($G -C $T/g rev-list --count $b0..posts/alive)
db=$(runu agi-wt pull doc:b 2>>$T/e11);echo "mine U3" >>$db/$NB;runu agi-flush 2>>$T/e11;frc=$?;c3=$($G -C $T/g rev-list --count $b0..posts/alive)
ok "x11-the-units-own-environment-runs-the-pieces the unit's Environment= line (AGI_POST=%i, %i=alive) reads [$(echo "$ul"|tr ' ' '\n'|grep -v '^PATH='|tr '\n' ' ')] (want it to hold AGI_POST=alive: $(echo " $ul "|grep -c ' AGI_POST=alive ')); under exactly those words: agi-wt pull rc $prc (want 0), agi-turn rc $trc (want 0) -> $c1 commit(s) (want 1), agi-wt drop rc $drc (want 0) -> $c2 (want 2), agi-flush rc $frc (want 0) -> $c3 (want 3); the nodes landed: a $($G -C $T/g show posts/alive:$NA 2>/dev/null|grep -c 'mine U2') b $($G -C $T/g show posts/alive:$NB 2>/dev/null|grep -c 'mine U3') (want 1 1); stderr [$(head -c 80 $T/e11)]" '[ "$(echo " $ul "|grep -c " AGI_POST=alive ")" = 1 ]&&[ $prc = 0 ]&&[ $trc = 0 ]&&[ $c1 = 1 ]&&[ $drc = 0 ]&&[ $c2 = 2 ]&&[ $frc = 0 ]&&[ $c3 = 3 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine U2")" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NB|grep -c "mine U3")" = 1 ]'
# --- x12 (V2) agi-out's ring commit lands THROUGH agi-at: reachable from posts/P after the next agi-turn
mkr;b0=$(tip);runh sh $T/bin/agi-out 2>$T/e12;rc12=$?
c=$($G -C $T/hm/t log -1 --format=%H HEAD posts/alive -- $R);run agi-turn 2>>$T/e12
anc=$($G -C $T/g merge-base --is-ancestor $c posts/alive 2>/dev/null&&echo yes||echo NO);nc=$($G -C $T/g rev-list --count $b0..posts/alive)
ok "x12-the-ring-commit-is-reachable-after-the-next-turn agi-out (ExecStartPre, from \$HOME) rc $rc12 (want 0); the ring commit ${c:-none} is an ancestor of posts/alive after the next agi-turn: $anc (want yes); $nc new commit(s) on posts/alive (want 1); the tip's ring no longer holds the old key ($($G -C $T/g show posts/alive:$R 2>/dev/null|grep -c AAAAold), want 0) and still holds bob ($($G -C $T/g show posts/alive:$R 2>/dev/null|grep -c '^bob '), want 1); signed G: [$(sig posts/alive)]; stderr [$(head -c 100 $T/e12)]" '[ $rc12 = 0 ]&&[ -n "$c" ]&&[ $anc = yes ]&&[ $nc = 1 ]&&[ "$($G -C $T/g show posts/alive:$R|grep -c AAAAold)" = 0 ]&&[ "$($G -C $T/g show posts/alive:$R|grep -c "^bob ")" = 1 ]&&[ "$(sig posts/alive)" = G ]'
# --- x13 (V2) tick's drift commit lands THROUGH agi-at: reachable from posts/P after the next agi-turn
mk;printf '#!/bin/sh\ncase $1 in project.sh)echo "echo unit agi-post@alive";; observe.sh)echo "echo unit agi-post@gone";;esac\n' >$T/bin/sect;printf '#!/bin/sh\nexit 0\n' >$T/bin/systemctl;chmod +x $T/bin/sect $T/bin/systemctl;b0=$(tip)
runh sh $T/bin/tick.sh 2>$T/e13;rc13=$?;c=$($G -C $T/hm/t log -1 --format=%H HEAD posts/alive -- .agi/drift/agi-alive);run agi-turn 2>>$T/e13
anc=$($G -C $T/g merge-base --is-ancestor $c posts/alive 2>/dev/null&&echo yes||echo NO);nc=$($G -C $T/g rev-list --count $b0..posts/alive)
ok "x13-the-drift-commit-is-reachable-after-the-next-turn tick.sh rc $rc13 (want 0); the drift commit ${c:-none} is an ancestor of posts/alive after the next agi-turn: $anc (want yes); $nc new commit(s) (want 1); the tip carries .agi/drift/agi-alive: $($G -C $T/g cat-file -e posts/alive:.agi/drift/agi-alive 2>/dev/null&&echo yes||echo NO); signed G: [$(sig posts/alive)]; stderr [$(head -c 100 $T/e13)]" '[ $rc13 = 0 ]&&[ -n "$c" ]&&[ $anc = yes ]&&[ $nc = 1 ]&&$G -C $T/g cat-file -e posts/alive:.agi/drift/agi-alive&&[ "$(sig posts/alive)" = G ]'
# --- x14 agi-at itself: one signed commit by CAS on posts/P; no change = no commit; a miss = [raced], rc 4, the edit stays; no AGI_POST fails closed
mk;echo "agi-at edit" >>$T/hm/t/$NB;b0=$(tip);run agi-at $NB 2>$T/e14;rc14=$?;nc=$($G -C $T/g rev-list --count $b0..posts/alive);ht=$($G -C $T/hm/t rev-parse HEAD)
ok "x14-agi-at-commits-by-cas agi-at on an edited ~/t path: rc $rc14 (want 0), $nc new commit(s) (want 1) with the edit: $($G -C $T/g show posts/alive:$NB 2>/dev/null|grep -c 'agi-at edit') (want 1), signed G: [$(sig posts/alive)], ~/t HEAD = the tip: $([ $ht = $(tip) ]&&echo yes||echo NO), detached: $($G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&echo NO||echo yes), the edit kept in ~/t: $(grep -c 'agi-at edit' $T/hm/t/$NB) (want 1), status clean: $([ -z "$($G -C $T/hm/t status -s)" ]&&echo yes||echo NO)" '[ $rc14 = 0 ]&&[ $nc = 1 ]&&[ "$($G -C $T/g show posts/alive:$NB|grep -c "agi-at edit")" = 1 ]&&[ "$(sig posts/alive)" = G ]&&[ $ht = $(tip) ]&&! $G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&[ "$(grep -c "agi-at edit" $T/hm/t/$NB)" = 1 ]&&[ -z "$($G -C $T/hm/t status -s)" ]'
mk;b0=$(tip);run agi-at $NB 2>$T/e14b;rc14b=$?
ok "x14b-agi-at-with-no-change-commits-nothing agi-at on an unedited path: rc $rc14b (want 0), tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no)" '[ $rc14b = 0 ]&&[ $(tip) = $b0 ]'
mk;echo "mine AT" >>$T/hm/t/$NB;b0=$(tip);echo "refs/heads/posts/alive $NB $MB b" >$T/racespec;run agi-at $NB 2>$T/e14c;rc14c=$?;t1=$(tip)
ok "x14c-agi-at-cas-miss-is-raced-rc-4-and-the-edit-stays a racer advances posts/alive at the CAS: rc $rc14c (want 4), stderr [$(cat $T/e14c|cut -c1-40)] (want [raced]); the tip is the racer's: $($G -C $T/g show $t1:$NB|grep -c 'racer edit') (want 1) and not mine: $($G -C $T/g show $t1:$NB|grep -c 'mine AT') (want 0); exactly one new commit (the racer's): $($G -C $T/g rev-list --count $b0..posts/alive) (want 1); the edit stays in ~/t: $(grep -c 'mine AT' $T/hm/t/$NB) (want 1)" '[ $rc14c = 4 ]&&grep -q "\[raced\]" $T/e14c&&[ "$($G -C $T/g show $t1:$NB|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/g show $t1:$NB|grep -c "mine AT")" = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$(grep -c "mine AT" $T/hm/t/$NB)" = 1 ]'
mk;echo "mine NP" >>$T/hm/t/$NB;b0=$(tip);run0 agi-at $NB 2>$T/e14d;rc14d=$?
ok "x14d-agi-at-with-no-post-fails-closed the piece agi-at exists: $([ -s $T/bin/agi-at ]&&echo yes||echo NO) (want yes), AGI_POST unset: rc $rc14d (want != 0 and not 'command not found': [$(head -c 60 $T/e14d)]), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO), the edit kept: $(grep -c 'mine NP' $T/hm/t/$NB) (want 1)" '[ -s $T/bin/agi-at ]&&[ $rc14d != 0 ]&&! grep -qi "not found" $T/e14d&&[ $(tip) = $b0 ]&&[ "$(grep -c "mine NP" $T/hm/t/$NB)" = 1 ]'
# --- x14e agi-at commits ONLY the named path: a SECOND dirty tracked file and an UNTRACKED file sit in ~/t beside it, and neither is committed (the commit's tree differs from its parent by the one named path; the second file stays modified, the untracked one stays untracked)
mk;echo "agi-at named" >>$T/hm/t/$NB;echo "second dirty" >>$T/hm/t/$NA;echo "untracked" >$T/hm/t/untracked.txt;b0=$(tip);run agi-at $NB 2>$T/e14e;rc14e=$?;t1=$(tip);nc=$($G -C $T/g rev-list --count $b0..posts/alive);ch=$($G -C $T/g diff --name-only $b0 $t1|tr '\n' ' ');st=$($G -C $T/hm/t status --porcelain|tr '\n' '|')
ok "x14e-agi-at-commits-only-the-named-path a second dirty tracked file and an untracked file beside $NB: rc $rc14e (want 0), $nc new commit(s) (want 1), the commit's tree differs from its parent by [${ch% }] (want exactly $NB), the named edit is in it: $($G -C $T/g show $t1:$NB|grep -c 'agi-at named') (want 1), the second file is NOT: $($G -C $T/g show $t1:$NA|grep -c 'second dirty') (want 0) and stays modified in ~/t: $(grep -c 'second dirty' $T/hm/t/$NA) (want 1), the untracked file is NOT in the tip: $($G -C $T/g cat-file -e $t1:untracked.txt 2>/dev/null&&echo yes||echo no) (want no) and stays untracked: [$st] (want  M $NA|?? untracked.txt|)" '[ $rc14e = 0 ]&&[ $nc = 1 ]&&[ "${ch% }" = "$NB" ]&&[ "$($G -C $T/g show $t1:$NB|grep -c "agi-at named")" = 1 ]&&[ "$($G -C $T/g show $t1:$NA|grep -c "second dirty")" = 0 ]&&[ "$(grep -c "second dirty" $T/hm/t/$NA)" = 1 ]&&! $G -C $T/g cat-file -e $t1:untracked.txt 2>/dev/null&&[ "$st" = " M $NA|?? untracked.txt|" ]'
# --- x15 (V2) the agi-meter line sends the post through agi-flush, never `git commit`
hi=$(echo '{"tokens": 900000, "context_window": 1000000}'|run sh $T/bin/agi-meter 2>&1);lo=$(echo '{"tokens": 1000, "context_window": 1000000}'|run sh $T/bin/agi-meter 2>&1)
ok "x15-the-meter-line-names-agi-flush-and-no-git-commit at 90% of the window the meter prints [$(echo "$hi"|cut -c1-110)...]: names agi-flush $(echo "$hi"|grep -c agi-flush) (want 1), has 'git commit' $(echo "$hi"|grep -c 'git commit') (want 0); below the line it prints nothing: [$lo] (want empty)" '[ "$(echo "$hi"|grep -c agi-flush)" = 1 ]&&[ "$(echo "$hi"|grep -c "git commit")" = 0 ]&&[ -z "$lo" ]'
# ====================================================================================================================================================================
# v5 (goal:g7.16.1.11.11 AA1.V v5, SM mur residues R1-R5, DG1 17:26Z/17:27Z): THE RULE: no tree is purged unless its turn PROVED its commit (add + write-tree + commit-tree + update-ref ALL checked); every failure path KEEPS the tree and exits != 0 with a bracketed label that names the cause (never [raced] unless the CAS missed). `.p` is ONE PATH PER LINE.
# n1 an absent payload at pull · n2 an absent payload at turn (the edit is not lost) · n2b a failing tree does not stop the next · n3 a failed `git archive` / `tar` at pull · n4 no signer · n5 `.b` is the commit THIS turn wrote (R3) · n6 agi-flush ends with a CAS merge of the trunk onto posts/P (R4) · n7 a payload path with a space, the OLD one-line `.p` fails closed (R1/R5) · n8 `agi-wt new` writes one path per line
# ====================================================================================================================================================================
MG=gggggggggggggggggggggggggggggggg;MS=ssssssssssssssssssssssssssssssss;NG=.agi/nodes/build/g.md;NS=.agi/nodes/build/s.md
# mkn: mk + build:g (payload_ref extensions/gone.py, ABSENT from the repo: the live shape of build:tests-test-render-context) + build:s (payload_ref "src/s p.sh", a path with a space) committed on trunk AND posts/alive
mkn(){ mk;printf -- '---\nid: build:g\nmint_id: %s\ntype: build\npayload_ref: extensions/gone.py\n---\nbuild g\n' $MG >$T/g/$NG;printf -- '---\nid: build:s\nmint_id: %s\ntype: build\npayload_ref: "src/s p.sh"\n---\nbuild s\n' $MS >$T/g/$NS;printf '#!/bin/sh\necho s\n' >"$T/g/src/s p.sh";$G -C $T/g add -A;$G -C $T/g commit -qm nodes;$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive;TR0=$($G -C $T/g rev-parse trunk);}
lab(){ grep -E '^\[' "$1"|grep -vE '^\[(raced|moved|out-of-tree)\]';}
# --- n1 pull of a node whose payload is absent from the repo: rc != 0, NO tree left, a label naming the path
mkn;b0=$(tip);dn=$(run agi-wt pull build:g 2>$T/en1);rn1=$?;ls1=$(ls -A $T/wt|tr '\n' ' ')
ok "n1-pull-with-an-absent-payload-fails-and-leaves-no-tree agi-wt pull build:g (payload_ref extensions/gone.py is not in the repo): rc $rn1 (want != 0), stdout [$dn] (want empty: no tree path handed out), $T/wt holds [${ls1:-nothing}] (want nothing: no empty tree left as if fine), stderr [$(head -c 160 $T/en1|tr '\n' '|')] (want a line naming agi-wt or pull AND extensions/gone.py), the tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES)" '[ $rn1 != 0 ]&&[ -z "$dn" ]&&[ -z "$ls1" ]&&grep -iE "agi-wt|pull" $T/en1|grep -q extensions/gone.py&&[ $(tip) = $b0 ]'
# --- n2 a tree that holds an edit and an absent payload path (what a v4 pull left behind: the node file, edited, and .p naming the gone payload): the turn KEEPS it, rc != 0, a label names the path, nothing is committed, the edit is not lost
mkn;dg=$T/wt/$MG;mkdir -p $dg/.agi/nodes/build;$G -C $T/g show posts/alive:$NG >$dg/$NG;echo "MY EDIT" >>$dg/$NG;printf '%s\n%s\n' $NG extensions/gone.py >$dg/.p;$G -C $T/g rev-parse posts/alive >$dg/.b;b0=$(tip);run agi-turn 2>$T/en2;rn2=$?
ok "n2-turn-with-an-absent-payload-keeps-the-tree-and-the-edit a tree with 'MY EDIT' in $NG and .p = node + extensions/gone.py (absent at HEAD): agi-turn rc $rn2 (want != 0), the tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no), the tree kept: $([ -d $dg ]&&echo yes||echo NO) with the edit: $(grep -c 'MY EDIT' $dg/$NG 2>/dev/null||echo 0) (want 1), a bracketed label naming the path: [$(lab $T/en2|grep extensions/gone.py|head -1|cut -c1-110)] (want one, not [raced])" '[ $rn2 != 0 ]&&[ $(tip) = $b0 ]&&[ -d $dg ]&&[ "$(grep -c "MY EDIT" $dg/$NG)" = 1 ]&&lab $T/en2|grep -q extensions/gone.py'
mkn;dg=$T/wt/$MG;mkdir -p $dg/.agi/nodes/build;$G -C $T/g show posts/alive:$NG >$dg/$NG;echo "MY EDIT" >>$dg/$NG;printf '%s\n%s\n' $NG extensions/gone.py >$dg/.p;$G -C $T/g rev-parse posts/alive >$dg/.b;b0=$(tip);run agi-wt drop build:g 2>$T/en2d;rn2d=$?
ok "n2-drop-with-an-absent-payload-keeps-the-tree the same tree through agi-wt drop (agi-turn && purge): rc $rn2d (want != 0), the tree kept: $([ -d $dg ]&&echo yes||echo NO) with the edit: $(grep -c 'MY EDIT' $dg/$NG 2>/dev/null||echo 0) (want 1), the tip moved: $([ $(tip) = $b0 ]&&echo no||echo YES) (want no), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0)" '[ $rn2d != 0 ]&&[ -d $dg ]&&[ "$(grep -c "MY EDIT" $dg/$NG)" = 1 ]&&[ $(tip) = $b0 ]&&[ -z "$($G -C $T/g for-each-ref refs/archive)" ]'
# --- n2b a failing tree does not stop the next one: build:g (bad, sorts first) + build:s (good, a payload with a space)
mkn;dg=$T/wt/$MG;mkdir -p $dg/.agi/nodes/build;$G -C $T/g show posts/alive:$NG >$dg/$NG;echo "MY EDIT" >>$dg/$NG;printf '%s\n%s\n' $NG extensions/gone.py >$dg/.p;$G -C $T/g rev-parse posts/alive >$dg/.b
ds=$(run agi-wt pull build:s 2>/dev/null);echo "# s2" >>"$ds/src/s p.sh";b0=$(tip);run agi-turn 2>$T/en2b;rn2b=$?;nc=$($G -C $T/g rev-list --count $b0..posts/alive)
ok "n2b-a-failing-tree-does-not-stop-the-turn build:g (bad) and build:s (good, edited): rc $rn2b (want != 0), $nc new commit(s) (want 1: build:s), its subject [$($G -C $T/g log -1 --format=%s posts/alive)] (want alive: $NS), 's p.sh' on the tip has the edit: $($G -C $T/g show 'posts/alive:src/s p.sh'|grep -c s2) (want 1); build:g kept with its edit: $([ -d $dg ]&&grep -c 'MY EDIT' $dg/$NG||echo NO) (want 1), label: [$(lab $T/en2b|head -1|cut -c1-90)]" '[ $rn2b != 0 ]&&[ $nc = 1 ]&&[ "$($G -C $T/g log -1 --format=%s posts/alive)" = "alive: $NS" ]&&[ "$($G -C $T/g show "posts/alive:src/s p.sh"|grep -c s2)" = 1 ]&&[ -d $dg ]&&[ "$(grep -c "MY EDIT" $dg/$NG)" = 1 ]&&lab $T/en2b|grep -q .'
# --- n3 a failed `git archive` (the git side) and a failed `tar` (the extracting side) at pull: rc != 0 either way (a pipeline's status is its LAST command: v4 handed out an empty tree and exited 0)
mk;: >$T/failarchive;b0=$(tip);dn=$(run agi-wt pull doc:a 2>$T/en3);rn3=$?;ls3=$(ls -A $T/wt|tr '\n' ' ')
ok "n3-pull-with-a-failed-git-archive-fails git archive exits 128 (shim): agi-wt pull doc:a rc $rn3 (want != 0), stdout [$dn] (want empty), $T/wt holds [${ls3:-nothing}] (want nothing), stderr [$(head -c 100 $T/en3|tr '\n' '|')] (want a line)" '[ $rn3 != 0 ]&&[ -z "$dn" ]&&[ -z "$ls3" ]&&[ -s $T/en3 ]'
mk;: >$T/failtar;dn=$(run agi-wt pull doc:a 2>$T/en3b);rn3b=$?;ls3b=$(ls -A $T/wt|tr '\n' ' ')
ok "n3b-pull-with-a-failed-tar-fails tar exits 2 (shim): agi-wt pull doc:a rc $rn3b (want != 0), stdout [$dn] (want empty), $T/wt holds [${ls3b:-nothing}] (want nothing: no half-extracted tree), stderr [$(head -c 100 $T/en3b|tr '\n' '|')]" '[ $rn3b != 0 ]&&[ -z "$dn" ]&&[ -z "$ls3b" ]&&[ -s $T/en3b ]'
mk;da=$(run agi-wt pull doc:a 2>$T/en3c);rn3c=$?
ok "n3c-the-shims-are-inert-by-default the same pull with no failure flag: rc $rn3c (want 0), the tree $da has the node: $([ -f $da/$NA ]&&echo yes||echo NO) (so n3 / n3b fail because of the shim, not the fixture)" '[ $rn3c = 0 ]&&[ -f $da/$NA ]'
# --- n4 NO SIGNER: its OWN label (not [raced]), the tree kept with the edit, rc != 0, nothing committed
mk;da=$(run agi-wt pull doc:a);echo "mine S" >>$da/$NA;$G -C $T/g config --unset user.signingkey;b0=$(tip);run agi-turn 2>$T/en4;rn4=$?
ok "n4-no-signer-has-its-own-label-and-keeps-the-tree user.signingkey unset (commit-tree -S cannot sign): agi-turn rc $rn4 (want != 0), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO), the tree kept with the edit: $([ -d $da ]&&grep -c 'mine S' $da/$NA||echo NO) (want 1), [raced] lines: $(grep -c '\[raced\]' $T/en4) (want 0), a bracketed label that names the signer: [$(lab $T/en4|grep -i sign|head -1|cut -c1-100)] (want one)" '[ $rn4 != 0 ]&&[ $(tip) = $b0 ]&&[ -d $da ]&&[ "$(grep -c "mine S" $da/$NA)" = 1 ]&&[ "$(grep -c "\[raced\]" $T/en4)" = 0 ]&&lab $T/en4|grep -qi sign'
$G -C $T/g config user.signingkey $T/k/alive;run agi-turn 2>$T/en4b;rn4b=$?
ok "n4b-the-kept-tree-lands-once-the-signer-is-back the signer restored, the SAME tree: agi-turn rc $rn4b (want 0), the edit is on the tip: $($G -C $T/g show posts/alive:$NA|grep -c 'mine S') (want 1), signed G: [$(sig posts/alive)]" '[ $rn4b = 0 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine S")" = 1 ]&&[ "$(sig posts/alive)" = G ]'
# --- n5 R3: a racer between update-ref and the .b write. .b = the commit THIS turn wrote, so the NEXT turn sees the node moved (archives mine) and never commits over the racer
mk;da=$(run agi-wt pull doc:a);echo "mine P1" >>$da/$NA;b0=$(tip);echo "refs/heads/posts/alive $NA $MA a" >$T/postrace;run agi-turn 2>$T/en5;rn5=$?;t1=$(tip);bb=$(cat $da/.b 2>/dev/null);mc=$($G -C $T/g log --format='%H %s' $b0..posts/alive|grep " alive: $NA\$"|cut -d' ' -f1)
ok "n5-dot-b-is-the-commit-this-turn-wrote a racer advances posts/alive right AFTER my update-ref: rc $rn5 (want 0: my commit landed), my commit ${mc:-none}, the tip $t1 is the racer's: $($G -C $T/g show $t1:$NA|grep -c 'racer edit') (want 1), .b [${bb:-none}] (want = my commit, NOT the tip), the tree kept: $([ -d $da ]&&echo yes||echo NO)" '[ $rn5 = 0 ]&&[ -n "$mc" ]&&[ $t1 != $mc ]&&[ "$($G -C $T/g show $t1:$NA|grep -c "racer edit")" = 1 ]&&[ "$bb" = "$mc" ]&&[ -d $da ]'
echo "mine P2" >>$da/$NA;run agi-turn 2>$T/en5b;AR=refs/archive/alive/$MA
ok "n5b-the-next-turn-sees-the-racer-and-archives-mine the next turn on the same tree: [moved] $(grep -c '\[moved\]' $T/en5b) (want 1); the tip is still the racer's ($t1): $([ $(tip) = $t1 ]&&echo yes||echo NO), without mine P2: $($G -C $T/g show posts/alive:$NA|grep -c 'mine P2') (want 0); $AR holds mine P2: $($G -C $T/g show $AR:$NA 2>/dev/null|grep -c 'mine P2') (want 1); the tree dropped: $([ -d $da ]&&echo NO||echo yes)" '[ "$(grep -c "\[moved\]" $T/en5b)" = 1 ]&&[ $(tip) = $t1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "mine P2")" = 0 ]&&[ "$($G -C $T/g show $AR:$NA|grep -c "mine P2")" = 1 ]&&[ ! -d $da ]'
# --- n6 R4: agi-flush ends with a CAS merge of the trunk onto posts/P (the base ended with `git merge ${AGI_TRUNK:-trunk}`; v4 dropped it and nothing else advances posts/P from the trunk)
tmove(){ echo "trunk side" >$T/g/trunk-only.txt;$G -C $T/g add trunk-only.txt;$G -C $T/g commit -qm trunkside;}
# n6a a post whose trunk moved, with an edit to land: the trunk ends up in posts/P's history, signed, ~/t on the new tip
mk;da=$(run agi-wt pull doc:a);echo "flush merge" >>$da/$NA;tmove;run agi-flush 2>$T/en6;rn6=$?;t1=$(tip);np=$($G -C $T/g rev-list --parents -n1 $t1|wc -w|tr -d ' ');tf=$($G -C $T/g cat-file -e $t1:trunk-only.txt 2>/dev/null&&echo yes||echo NO);anc=$($G -C $T/g merge-base --is-ancestor trunk posts/alive&&echo yes||echo NO)
ok "n6a-flush-merges-the-moved-trunk-onto-the-tip trunk has a commit the post lacks and one tree holds an edit: agi-flush rc $rn6 (want 0); the trunk is an ancestor of posts/alive: $anc (want yes); the tip has $((np-1)) parent(s) (want 2: the post's tip and the trunk); trunk-only.txt on the tip: $tf (want yes); my edit on the tip: $($G -C $T/g show $t1:$NA|grep -c 'flush merge') (want 1); signed G: [$(sig $t1)]; ~/t HEAD = the tip: $([ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&echo yes||echo NO), detached: $($G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&echo NO||echo yes), merge in progress: $([ -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&echo YES||echo no); stderr [$(head -c 80 $T/en6)] (want empty)" '[ $rn6 = 0 ]&&[ $anc = yes ]&&[ $np = 3 ]&&[ $tf = yes ]&&[ "$($G -C $T/g show $t1:$NA|grep -c "flush merge")" = 1 ]&&[ "$(sig $t1)" = G ]&&[ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&! $G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&[ ! -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&[ ! -s $T/en6 ]'
# n6b no tree at all: a post merely BEHIND the trunk moves to the trunk tip by CAS (goal:g7.16.1.11.41: no commit, so board_job.py land sees no non-own commit)
mk;tmove;b0=$(tip);tt=$($G -C $T/g rev-parse trunk);run agi-flush 2>$T/en6b;rn6b=$?;t1=$(tip);np=$($G -C $T/g rev-list --parents -n1 $t1|wc -w|tr -d ' ')
ok "n6b-flush-with-no-trees-fast-forwards-a-behind-post trunk moved, no tree: agi-flush rc $rn6b (want 0), the tip is the trunk tip: $([ $t1 = $tt ]&&echo yes||echo NO), the tip has $((np-1)) parent(s) (want 1: no merge commit), ~/t HEAD = the tip: $([ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&echo yes||echo NO)" '[ $rn6b = 0 ]&&[ $t1 = $tt ]&&[ $np = 2 ]&&[ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]'
# n6c nothing to merge (the trunk is already in the post): no merge commit, rc unchanged
mk;da=$(run agi-wt pull doc:a);echo "flush plain" >>$da/$NA;b0=$(tip);run agi-flush 2>$T/en6c;rn6c=$?;t1=$(tip);np=$($G -C $T/g rev-list --parents -n1 $t1|wc -w|tr -d ' ')
ok "n6c-flush-with-nothing-to-merge-adds-no-merge-commit the trunk is already an ancestor: agi-flush rc $rn6c (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1: my edit), the tip has $((np-1)) parent(s) (want 1)" '[ $rn6c = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ $np = 2 ]'
# n6d a CONFLICTING trunk (same line of doc:a): posts/P is left exactly as the final turn made it, rc 0, no markers anywhere, ~/t on the tip, no merge in progress
mk;da=$(run agi-wt pull doc:a);sed -i 's/^body a$/body a MINE/' $da/$NA;$G -C $T/g checkout -q trunk;sed -i 's/^body a$/body a TRUNK/' $T/g/$NA;$G -C $T/g add $NA;$G -C $T/g commit -qm trunkconflict;run agi-flush 2>$T/en6d;rn6d=$?;t1=$(tip);np=$($G -C $T/g rev-list --parents -n1 $t1|wc -w|tr -d ' ')
ok "n6d-a-conflicting-trunk-leaves-posts-p-untouched trunk and the post edit the same line of $NA: agi-flush rc $rn6d (want 0), the tip is my turn's commit (1 parent: $((np-1)), want 1; subject [$($G -C $T/g log -1 --format=%s $t1)] want alive: $NA), the trunk is NOT an ancestor: $($G -C $T/g merge-base --is-ancestor trunk posts/alive&&echo YES||echo no) (want no), no conflict markers in the tip's $NA: $($G -C $T/g show $t1:$NA|grep -c '^[<>=]\{7\}') (want 0), MINE on the tip: $($G -C $T/g show $t1:$NA|grep -c MINE) (want 1), ~/t HEAD = the tip: $([ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&echo yes||echo NO), merge in progress: $([ -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&echo YES||echo no) (want no), ~/t status clean: $([ -z "$($G -C $T/hm/t status -s)" ]&&echo yes||echo NO)" '[ $rn6d = 0 ]&&[ $np = 2 ]&&[ "$($G -C $T/g log -1 --format=%s $t1)" = "alive: $NA" ]&&! $G -C $T/g merge-base --is-ancestor trunk posts/alive&&[ "$($G -C $T/g show $t1:$NA|grep -c "^[<>=]\{7\}")" = 0 ]&&[ "$($G -C $T/g show $t1:$NA|grep -c MINE)" = 1 ]&&[ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&[ ! -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&[ -z "$($G -C $T/hm/t status -s)" ]'
# n6e a raced CAS at the merge: a racer advances posts/P first: the racer's commit stays (nothing lost), the tree is not rewound, ~/t on the tip
mk;tmove;echo "refs/heads/posts/alive $NB $MB b" >$T/racespec;run agi-flush 2>$T/en6e;rn6e=$?;t1=$(tip)
ok "n6e-a-raced-merge-keeps-the-racer a racer advances posts/alive at the merge's update-ref: agi-flush rc $rn6e (want 0), the racer's commit is on posts/alive: $($G -C $T/g log --format=%s posts/alive|grep -c '^racer$') (want 1), the tip's $NB carries the racer's edit: $($G -C $T/g show $t1:$NB|grep -c 'racer edit') (want 1), ~/t HEAD = the tip: $([ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&echo yes||echo NO), merge in progress: $([ -e $T/g/.git/worktrees/t/MERGE_HEAD ]&&echo YES||echo no)" '[ $rn6e = 0 ]&&[ "$($G -C $T/g log --format=%s posts/alive|grep -c "^racer\$")" = 1 ]&&[ "$($G -C $T/g show $t1:$NB|grep -c "racer edit")" = 1 ]&&[ "$($G -C $T/hm/t rev-parse HEAD)" = $t1 ]&&[ ! -e $T/g/.git/worktrees/t/MERGE_HEAD ]'
# n6f AGI_TRUNK names the branch to merge: main2 merged, trunk (which also moved) NOT
mk;$G -C $T/g branch main2 trunk;$G -C $T/g checkout -q main2;echo m2 >$T/g/main2-only.txt;$G -C $T/g add main2-only.txt;$G -C $T/g commit -qm main2side;$G -C $T/g checkout -q trunk;tmove;run AGI_TRUNK=main2 agi-flush 2>$T/en6f;rn6f=$?;t1=$(tip)
ok "n6f-agi-trunk-names-the-branch-to-merge AGI_TRUNK=main2: agi-flush rc $rn6f (want 0), main2 is an ancestor of posts/alive: $($G -C $T/g merge-base --is-ancestor main2 posts/alive&&echo yes||echo NO) (want yes), main2-only.txt on the tip: $($G -C $T/g cat-file -e $t1:main2-only.txt 2>/dev/null&&echo yes||echo NO), the trunk is NOT an ancestor: $($G -C $T/g merge-base --is-ancestor trunk posts/alive&&echo YES||echo no) (want no), trunk-only.txt on the tip: $($G -C $T/g cat-file -e $t1:trunk-only.txt 2>/dev/null&&echo YES||echo no) (want no)" '[ $rn6f = 0 ]&&$G -C $T/g merge-base --is-ancestor main2 posts/alive&&$G -C $T/g cat-file -e $t1:main2-only.txt&&! $G -C $T/g merge-base --is-ancestor trunk posts/alive&&! $G -C $T/g cat-file -e $t1:trunk-only.txt 2>/dev/null'
# --- n7 .p is ONE PATH PER LINE: a payload path with a space round-trips (R5); the OLD one-line form "node payload" is ONE pathspec with a space and FAILS CLOSED (R1; no compat reader)
mkn;ds=$(run agi-wt pull build:s 2>$T/en7);ps=$(tr '\n' '|' <$ds/.p);nl7=$(wc -l <$ds/.p|tr -d ' ')
ok "n7-pull-writes-one-path-per-line a node whose payload_ref has a space (src/s p.sh): .p = [$ps] (want $NS|src/s p.sh| , $nl7 line(s), want 2); the payload is in the tree: $([ -f "$ds/src/s p.sh" ]&&echo yes||echo NO); stderr [$(cat $T/en7)] (want empty)" '[ "$ps" = "$NS|src/s p.sh|" ]&&[ "$nl7" = 2 ]&&[ -f "$ds/src/s p.sh" ]&&[ ! -s $T/en7 ]'
echo "# s3" >>"$ds/src/s p.sh";b0=$(tip);run agi-turn 2>$T/en7b;rn7=$?;t1=$(tip);ch=$($G -C $T/g diff --name-only $b0 $t1|tr '\n' '|')
ok "n7b-a-payload-path-with-a-space-lands the edit to 'src/s p.sh': agi-turn rc $rn7 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), changed [$ch] (want src/s p.sh|), subject [$($G -C $T/g log -1 --format=%s $t1)] (want alive: $NS), the edit is on the tip: $($G -C $T/g show "$t1:src/s p.sh"|grep -c s3) (want 1), .b = the tip: $([ "$(cat $ds/.b)" = $t1 ]&&echo yes||echo NO); a clean second turn commits nothing: tip moved $(run agi-turn 2>/dev/null;[ $(tip) = $t1 ]&&echo no||echo YES) (want no)" '[ $rn7 = 0 ]&&[ "$ch" = "src/s p.sh|" ]&&[ "$($G -C $T/g log -1 --format=%s $t1)" = "alive: $NS" ]&&[ "$($G -C $T/g show "$t1:src/s p.sh"|grep -c s3)" = 1 ]&&[ "$(cat $ds/.b)" = $t1 ]&&[ $(tip) = $t1 ]'
mk;dc=$(run agi-wt pull build:c);printf '%s %s\n' $NC src/c.sh >$dc/.p;echo "# old form" >>$dc/src/c.sh;b0=$(tip);run agi-turn 2>$T/en7c;rn7c=$?
ok "n7c-the-old-one-line-p-fails-closed a tree from a v4 piece (.p = one line '$NC src/c.sh'): agi-turn rc $rn7c (want != 0), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO) (the payload is NOT silently dropped), the tree kept with the edit: $([ -d $dc ]&&grep -c 'old form' $dc/src/c.sh||echo NO) (want 1), a bracketed label naming the path: [$(lab $T/en7c|grep src/c.sh|head -1|cut -c1-110)] (want one)" '[ $rn7c != 0 ]&&[ $(tip) = $b0 ]&&[ -d $dc ]&&[ "$(grep -c "old form" $dc/src/c.sh)" = 1 ]&&lab $T/en7c|grep -q src/c.sh'
# --- n8 agi-wt new writes .p the same way
mkgo;dn=$(run agi-wt new .agi/nodes/build/n.md src/n.sh 2>$T/en8);pn=$(tr '\n' '|' <$dn/.p);mkdir -p $dn/.agi/nodes/build $dn/src;printf -- '---\nid: build:n\nmint_id: nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\ntype: build\nbuild_kind: prose\npayload_ref: src/n.sh\nparents:\n  - goal:g1\n  - idea:i1\n---\nnew build\n' >$dn/.agi/nodes/build/n.md;echo 'echo n' >$dn/src/n.sh;b0=$(tip);run agi-turn 2>$T/en8b;rn8=$?;ch=$($G -C $T/g diff --name-only $b0 posts/alive|tr '\n' '|')
ok "n8-new-writes-one-path-per-line agi-wt new PATH PAYLOAD: .p = [$pn] (want .agi/nodes/build/n.md|src/n.sh|), the turn rc $rn8 (want 0) lands ONE commit [$($G -C $T/g rev-list --count $b0..posts/alive)] with both paths [$ch]" '[ "$pn" = ".agi/nodes/build/n.md|src/n.sh|" ]&&[ $rn8 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$ch" = ".agi/nodes/build/n.md|src/n.sh|" ]'
# ====================================================================================================================================================================
# v5 residues (DG1 order (C) 21:4xZ, SM's gate; DG3's design read 21:37Z): w0 agi-at exits != 0 when its `git add` or `git read-tree` FAILS (the base chained them with ';', an index equal to the tip exited 0 and agi-out saw success; a failed read-tree left an EMPTY index, so the add built a tree of the named paths only and COMMITTED it) · w1 agi-wt drop removes a tree ONLY when the WHOLE tree is clean against the commit its turn proved (not just the .p paths): a file outside .p, a payload_ref added after pull · w4 the quirk: drop runs agi-turn over ALL trees (the safe direction), so a failure in tree B keeps tree A · w5 the same whole-tree rule in agi-turn's [moved] arm. Each kept tree: rc != 0 and a bracketed label that NAMES THE FILE (one path per line: git status -uall).
# ====================================================================================================================================================================
# --- w0 agi-at: a failed add / a failed read-tree
mk;echo "w0 edit" >>$T/hm/t/$NB;b0=$(tip);run agi-at $NB .agi/nodes/doc/nope.md 2>$T/ew0a;rw0a=$?
ok "w0a-a-failed-add-exits-nonzero agi-at on an edited path AND a path git refuses (no such file): rc $rw0a (want != 0, and not 4: it is not a CAS miss), stderr [$(head -c 80 $T/ew0a|tr '\n' '|')] (want a line), [raced] lines: $(grep -c '\[raced\]' $T/ew0a) (want 0), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO), the edit kept in ~/t: $(grep -c 'w0 edit' $T/hm/t/$NB) (want 1)" '[ $rw0a != 0 ]&&[ $rw0a != 4 ]&&[ -s $T/ew0a ]&&[ "$(grep -c "\[raced\]" $T/ew0a)" = 0 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "w0 edit" $T/hm/t/$NB)" = 1 ]'
mk;echo "w0 edit" >>$T/hm/t/$NB;b0=$(tip);: >$T/failreadtree;run agi-at $NB 2>$T/ew0b;rw0b=$?;rm -f $T/failreadtree;nf=$($G -C $T/g ls-tree -r --name-only posts/alive|wc -l|tr -d ' ')
ok "w0b-a-failed-read-tree-exits-nonzero-and-commits-nothing git read-tree fails (shim): agi-at rc $rw0b (want != 0), the tip is $([ $(tip) = $b0 ]&&echo unchanged||echo "MOVED: a commit built on an EMPTY index, its tree holds $nf files") (want unchanged), stderr [$(head -c 80 $T/ew0b|tr '\n' '|')] (want a line), the edit kept in ~/t: $(grep -c 'w0 edit' $T/hm/t/$NB) (want 1)" '[ $rw0b != 0 ]&&[ $(tip) = $b0 ]&&[ -s $T/ew0b ]&&[ "$(grep -c "w0 edit" $T/hm/t/$NB)" = 1 ]'
mk;echo "w0 ok" >>$T/hm/t/$NB;b0=$(tip);run agi-at $NB 2>$T/ew0c;rw0c=$?
ok "w0c-the-fixture-is-inert-without-the-flag the same agi-at with no failure flag and a good path: rc $rw0c (want 0), one new commit: $($G -C $T/g rev-list --count $b0..posts/alive) (want 1) (so w0a / w0b fail because of the failure, not the fixture)" '[ $rw0c = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]'
# --- w1 agi-wt drop keeps a tree that is not clean as a WHOLE
mk;da=$(run agi-wt pull doc:a);echo "w1 edit" >>$da/$NA;echo stray >$da/extra.txt;b0=$(tip);run agi-wt drop doc:a 2>$T/ew1a;rw1a=$?
ok "w1a-a-new-file-outside-p-keeps-the-tree doc:a edited (in .p) and a NEW file extra.txt beside it (not in .p): agi-wt drop rc $rw1a (want != 0), the tree exists: $([ -d $da ]&&echo yes||echo NO) (want yes) with extra.txt: $([ -f $da/extra.txt ]&&echo yes||echo NO), a bracketed label naming extra.txt: [$(lab $T/ew1a|grep extra.txt|head -1|cut -c1-100)] (want one), the .p edit still landed: $($G -C $T/g rev-list --count $b0..posts/alive) commit (want 1) with 'w1 edit' on the tip: $($G -C $T/g show posts/alive:$NA|grep -c 'w1 edit'), extra.txt on the tip: $($G -C $T/g cat-file -e posts/alive:extra.txt 2>/dev/null&&echo YES||echo no) (want no)" '[ $rw1a != 0 ]&&[ -d $da ]&&[ -f $da/extra.txt ]&&lab $T/ew1a|grep -q extra.txt&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "w1 edit")" = 1 ]&&! $G -C $T/g cat-file -e posts/alive:extra.txt 2>/dev/null'
mk;da=$(run agi-wt pull doc:a);echo "w1b edit" >>$da/$NA;echo "not the repo's readme" >$da/README.md;b0=$(tip);run agi-wt drop doc:a 2>$T/ew1b;rw1b=$?
ok "w1b-a-modified-tracked-file-outside-p-keeps-the-tree README.md (tracked at the pulled commit, not in .p) written with other bytes in the tree: agi-wt drop rc $rw1b (want != 0), the tree exists: $([ -d $da ]&&echo yes||echo NO) (want yes), a bracketed label naming README.md: [$(lab $T/ew1b|grep README.md|head -1|cut -c1-100)] (want one), README.md on the tip is still the repo's: $($G -C $T/g show posts/alive:README.md|grep -c readme) (want 1)" '[ $rw1b != 0 ]&&[ -d $da ]&&lab $T/ew1b|grep -q README.md&&[ "$($G -C $T/g show posts/alive:README.md|grep -c readme)" = 1 ]'
mk;da=$(run agi-wt pull doc:a);sed -i 's#^type: doc#type: doc\npayload_ref: src/new.sh#' $da/$NA;mkdir -p $da/src;echo 'echo new' >$da/src/new.sh;b0=$(tip);run agi-wt drop doc:a 2>$T/ew2a;rw2a=$?
ok "w2a-a-payload-ref-added-after-pull-keeps-the-tree the node gains payload_ref src/new.sh and the file is written in the tree, but .p (fixed at pull) does not list it: agi-wt drop rc $rw2a (want != 0), the tree exists: $([ -d $da ]&&echo yes||echo NO) (want yes), a bracketed label naming src/new.sh: [$(lab $T/ew2a|grep src/new.sh|head -1|cut -c1-100)] (want one: the file, not just 'src/'), the node edit landed (payload_ref on the tip): $($G -C $T/g show posts/alive:$NA|grep -c 'payload_ref: src/new.sh') (want 1), src/new.sh on the tip: $($G -C $T/g cat-file -e posts/alive:src/new.sh 2>/dev/null&&echo YES||echo no) (want no)" '[ $rw2a != 0 ]&&[ -d $da ]&&lab $T/ew2a|grep -q src/new.sh&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "payload_ref: src/new.sh")" = 1 ]&&! $G -C $T/g cat-file -e posts/alive:src/new.sh 2>/dev/null'
echo src/new.sh >>$da/.p;run agi-wt drop doc:a 2>$T/ew2b;rw2b=$?
ok "w2b-listing-the-path-in-p-lets-it-land-and-the-tree-go the same tree with src/new.sh added to .p: agi-wt drop rc $rw2b (want 0), src/new.sh is on the tip: $($G -C $T/g cat-file -e posts/alive:src/new.sh 2>/dev/null&&echo yes||echo NO) (want yes), the tree exists: $([ -d $da ]&&echo YES||echo no) (want no), stderr [$(head -c 80 $T/ew2b)] (want empty)" '[ $rw2b = 0 ]&&$G -C $T/g cat-file -e posts/alive:src/new.sh&&[ ! -d $da ]&&[ ! -s $T/ew2b ]'
# --- w4 the quirk: `agi-wt drop A` runs agi-turn over ALL trees; a failure in tree B keeps tree A (the safe direction)
mkn;da=$(run agi-wt pull doc:a);echo "w4 edit" >>$da/$NA;dg=$T/wt/$MG;mkdir -p $dg/.agi/nodes/build;$G -C $T/g show posts/alive:$NG >$dg/$NG;echo "g edit" >>$dg/$NG;printf '%s\n%s\n' $NG extensions/gone.py >$dg/.p;$G -C $T/g rev-parse posts/alive >$dg/.b;b0=$(tip);run agi-wt drop doc:a 2>$T/ew4a;rw4a=$?
ok "w4a-a-failure-in-tree-b-keeps-tree-a doc:a (clean, edited) and build:g (a payload absent from the repo: its turn fails): agi-wt drop doc:a rc $rw4a (want != 0), doc:a's edit landed anyway: $($G -C $T/g show posts/alive:$NA|grep -c 'w4 edit') (want 1), doc:a's tree is KEPT: $([ -d $da ]&&echo yes||echo NO) (want yes: the quirk, safe direction), build:g's tree kept with its edit: $([ -d $dg ]&&grep -c 'g edit' $dg/$NG||echo NO) (want 1), a bracketed label: [$(lab $T/ew4a|head -1|cut -c1-90)] (want one)" '[ $rw4a != 0 ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "w4 edit")" = 1 ]&&[ -d $da ]&&[ -d $dg ]&&[ "$(grep -c "g edit" $dg/$NG)" = 1 ]&&lab $T/ew4a|grep -q .'
rm -rf $dg;run agi-wt drop doc:a 2>$T/ew4b;rw4b=$?
ok "w4b-once-b-is-gone-a-drops the failing tree removed by hand: agi-wt drop doc:a rc $rw4b (want 0), the tree exists: $([ -d $da ]&&echo YES||echo no) (want no), commits after the first drop: $($G -C $T/g rev-list --count $b0..posts/alive) (want 1: no second commit of the same edit)" '[ $rw4b = 0 ]&&[ ! -d $da ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]'
# --- w5 the same whole-tree rule in agi-turn's [moved] arm: the tip moved since pull, a file outside .p sits in the tree
mk;db=$(run agi-wt pull doc:b);mv_b one;echo "mine w5" >>$db/$NB;echo stray >$db/outside.txt;b1=$(tip);run agi-turn 2>$T/ew5a;rw5a=$?;AR=refs/archive/alive/$MB
ok "w5a-a-moved-turn-keeps-a-tree-with-a-file-outside-p doc:b moved on the tip since pull, edited in .p, and a file outside.txt beside it: agi-turn rc $rw5a (want != 0), the tip is $([ $(tip) = $b1 ]&&echo kept||echo MOVED) (want kept), $AR holds mine: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'mine w5') (want 1) and not outside.txt: $($G -C $T/g cat-file -e $AR:outside.txt 2>/dev/null&&echo YES||echo no) (want no), the tree is KEPT: $([ -d $db ]&&echo yes||echo NO) (want yes), a bracketed label naming outside.txt that is not [raced]: [$(lab $T/ew5a|grep outside.txt|head -1|cut -c1-100)] (want one)" '[ $rw5a != 0 ]&&[ $(tip) = $b1 ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine w5")" = 1 ]&&! $G -C $T/g cat-file -e $AR:outside.txt 2>/dev/null&&[ -d $db ]&&lab $T/ew5a|grep -q outside.txt'
rm -f $db/outside.txt;run agi-turn 2>$T/ew5b;rw5b=$?
ok "w5b-without-the-stray-file-the-moved-tree-is-dropped as before the same tree with outside.txt removed: agi-turn rc $rw5b (want 0), [moved] lines: $(grep -c '\[moved\]' $T/ew5b) (want >= 1), the tree exists: $([ -d $db ]&&echo YES||echo no) (want no), $AR holds mine: $($G -C $T/g show $AR:$NB 2>/dev/null|grep -c 'mine w5') (want 1)" '[ $rw5b = 0 ]&&grep -q "\[moved\]" $T/ew5b&&[ ! -d $db ]&&[ "$($G -C $T/g show $AR:$NB|grep -c "mine w5")" = 1 ]'
# ---- v5d (SM mur wf_78d269f2-b2b on 04c450c35e, DG1 ruling): ONE end-state invariant (rc 0 iff no tree remains), a kept tree is a REF and has a READER, ~/t is detached BY THE UNIT, a kid fails closed, chk fails closed, flush resolves the trunk once
sx(){ $G -C $T/g show "$@" 2>/dev/null;}
# k1 (R1) a pulled tree with a stray file outside .p through agi-flush: the edit lands, the tree is KEPT, rc != 0, [kept] names it, EVERY file is on refs/archive/alive/<mint>
mk;da=$(run agi-wt pull doc:a);echo "mine K1" >>$da/$NA;echo stray >$da/stray.txt;run agi-flush 2>$T/ek1;rk1=$?;AR=refs/archive/alive/$MA
ok "k1-flush-keeps-a-dirty-pulled-tree-whole-on-a-ref agi-flush with a stray file beside the edit: rc $rk1 (want != 0), [kept] lines $(grep -c "^\[kept\] $MA: " $T/ek1) (want 1, naming stray.txt: $(grep -c 'stray.txt' $T/ek1)); the tree exists: $([ -d $da ]&&echo yes||echo NO); the edit landed on posts/alive: $(sx posts/alive:$NA|grep -c 'mine K1') (want 1), stray.txt NOT on the tip: $(sx posts/alive:stray.txt|wc -l|tr -d ' ') (want 0); $AR holds stray.txt: $(sx $AR:stray.txt|grep -c stray) (want 1) and the node: $(sx $AR:$NA|grep -c 'mine K1') (want 1), the rest of the tip is there too (README.md $(sx $AR:README.md|grep -c readme), $NB $(sx $AR:$NB|grep -c 'body b'); want 1/1: --ignore-removal, not -A); subject [$($G -C $T/g log -1 --format=%s $AR 2>/dev/null)] (want alive: kept $MA), signed G: [$(sig $AR)]" '[ $rk1 != 0 ]&&[ "$(grep -c "^\[kept\] $MA: .*stray.txt" $T/ek1)" = 1 ]&&[ -d $da ]&&[ "$(sx posts/alive:$NA|grep -c "mine K1")" = 1 ]&&[ "$(sx posts/alive:stray.txt|wc -l|tr -d " ")" = 0 ]&&[ "$(sx $AR:stray.txt|grep -c stray)" = 1 ]&&[ "$(sx $AR:$NA|grep -c "mine K1")" = 1 ]&&[ "$(sx $AR:README.md|grep -c readme)" = 1 ]&&[ "$(sx $AR:$NB|grep -c "body b")" = 1 ]&&[ "$($G -C $T/g log -1 --format=%s $AR)" = "alive: kept $MA" ]&&[ "$(sig $AR)" = G ]'
# the kept ref carries NO .p / .b (the tree's own bookkeeping) and a second stop chains on the first (the archive entry is never overwritten)
a1k=$($G -C $T/g rev-parse $AR);run agi-flush 2>$T/ek1b;rk1b=$?
ok "k1b-a-second-stop-chains-on-the-first-kept-commit agi-flush again over the same kept tree: rc $rk1b (want != 0); the first kept commit is still reachable from $AR: $($G -C $T/g rev-list $AR 2>/dev/null|grep -c "^$a1k\$") (want 1); no .p / .b in the kept tree: $(sx $AR:.p|wc -l|tr -d ' ')/$(sx $AR:.b|wc -l|tr -d ' ') (want 0/0)" '[ $rk1b != 0 ]&&[ "$($G -C $T/g rev-list $AR|grep -c "^$a1k\$")" = 1 ]&&[ "$(sx $AR:.p|wc -l|tr -d " ")" = 0 ]&&[ "$(sx $AR:.b|wc -l|tr -d " ")" = 0 ]'
# k2 (R2) an `agi-wt new` tree: the node lands, a stray file in the tree is found BY DIR, kept whole, rc != 0
mkgo;nd=$(run agi-wt new .agi/nodes/doc/n.md 2>/dev/null);mkdir -p $nd/.agi/nodes/doc;printf -- '---\nid: doc:n\nmint_id: nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\ntype: doc\nparents:\n  - goal:g1\n---\nnew\n' >$nd/.agi/nodes/doc/n.md;echo stray >$nd/stray.txt;run agi-flush 2>$T/ek2;rk2=$?;AN=refs/archive/alive/n
ok "k2-flush-finds-a-new-tree-by-dir-and-keeps-it agi-wt new + a node + a stray file through agi-flush: rc $rk2 (want != 0), [kept] n lines $(grep -c '^\[kept\] n: ' $T/ek2) (want 1); the node landed: $(sx posts/alive:.agi/nodes/doc/n.md|grep -c new) (want 1); $AN holds stray.txt: $(sx $AN:stray.txt|grep -c stray) (want 1); the tree exists: $([ -d $nd ]&&echo yes||echo NO)" '[ $rk2 != 0 ]&&[ "$(grep -c "^\[kept\] n: " $T/ek2)" = 1 ]&&[ "$(sx posts/alive:.agi/nodes/doc/n.md|grep -c new)" = 1 ]&&[ "$(sx $AN:stray.txt|grep -c stray)" = 1 ]&&[ -d $nd ]'
# k2b the same new tree with NO stray file: it lands and is REMOVED, rc 0 (rc 0 iff no tree remains), no archive ref
mkgo;nd=$(run agi-wt new .agi/nodes/doc/n.md 2>/dev/null);mkdir -p $nd/.agi/nodes/doc;printf -- '---\nid: doc:n\nmint_id: nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn\ntype: doc\nparents:\n  - goal:g1\n---\nnew\n' >$nd/.agi/nodes/doc/n.md;run agi-flush 2>$T/ek2b;rk2b=$?
ok "k2b-a-clean-new-tree-is-landed-and-removed a new tree whose node landed, nothing beside it: agi-flush rc $rk2b (want 0), the tree gone: $([ -d $nd ]&&echo NO||echo yes), the node landed: $(sx posts/alive:.agi/nodes/doc/n.md|grep -c new) (want 1), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0), stderr [$(head -c 60 $T/ek2b)] (want empty)" '[ $rk2b = 0 ]&&[ ! -d $nd ]&&[ "$(sx posts/alive:.agi/nodes/doc/n.md|grep -c new)" = 1 ]&&[ "$($G -C $T/g for-each-ref refs/archive|wc -l|tr -d " ")" = 0 ]&&[ ! -s $T/ek2b ]'
# k2c one clean tree + one dirty tree: the clean one is removed, the dirty one kept, rc != 0 (the invariant is per DIR)
mk;da=$(run agi-wt pull doc:a);db=$(run agi-wt pull doc:b);echo "mine K2c" >>$da/$NA;echo "mine K2c" >>$db/$NB;echo stray >$db/stray.txt;run agi-flush 2>$T/ek2c;rk2c=$?
ok "k2c-flush-removes-the-clean-tree-and-keeps-the-dirty-one doc:a edited clean, doc:b edited with a stray file: rc $rk2c (want != 0); doc:a's tree gone: $([ -d $da ]&&echo NO||echo yes), doc:b's kept: $([ -d $db ]&&echo yes||echo NO); both edits landed: $(sx posts/alive:$NA|grep -c 'mine K2c')/$(sx posts/alive:$NB|grep -c 'mine K2c') (want 1/1); refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 1)" '[ $rk2c != 0 ]&&[ ! -d $da ]&&[ -d $db ]&&[ "$(sx posts/alive:$NA|grep -c "mine K2c")" = 1 ]&&[ "$(sx posts/alive:$NB|grep -c "mine K2c")" = 1 ]&&[ "$($G -C $T/g for-each-ref refs/archive|wc -l|tr -d " ")" = 1 ]'
# k3 (N1 survivor) a stray file whose NAME contains .p / .b (a *.py payload, a *.bak): `agi-wt drop` keeps the tree and names it (grep -vxF, not -vF)
mk;da=$(run agi-wt pull doc:a);echo "mine K3" >>$da/$NA;echo x >$da/tool.py;echo x >$da/old.bak;run agi-wt drop doc:a 2>$T/ek3;rk3=$?
ok "k3-a-stray-py-or-bak-file-keeps-the-tree agi-wt drop with tool.py and old.bak beside the edit: rc $rk3 (want != 0), the tree kept: $([ -d $da ]&&echo yes||echo NO), stderr names them: $(grep -c 'tool.py' $T/ek3)/$(grep -c 'old.bak' $T/ek3) (want 1/1)" '[ $rk3 != 0 ]&&[ -d $da ]&&grep -q tool.py $T/ek3&&grep -q old.bak $T/ek3'
# k4 (R3) ~/t built by the unit's OWN worktree-add words is DETACHED: after a landed turn it shows the tip, with NO staged revert (an attached ~/t showed `M a` and a successor read the old card)
mk;wa=$(src|grep -m1 '^ExecStartPre=.*worktree add'|grep -o 'worktree add [^;}]*'|sed "s#\$PWD#$T/hm#;s#%i#alive#");$G -C $T/g worktree remove --force $T/hm/t;$G -C $T/g $wa;da=$(run agi-wt pull doc:a);echo "mine K4" >>$da/$NA;run agi-turn 2>$T/ek4;rk4=$?
ok "k4-the-unit-makes-t-detached the unit's words [$wa]: ~/t is $($G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&echo ATTACHED||echo detached) (want detached); after a landed turn rc $rk4 (want 0): ~/t HEAD = the tip: $([ "$($G -C $T/hm/t rev-parse HEAD)" = "$(tip)" ]&&echo yes||echo NO), ~/t status: [$($G -C $T/hm/t status -s|head -c 40)] (want empty), the edit visible in ~/t: $(grep -c 'mine K4' $T/hm/t/$NA) (want 1)" '! $G -C $T/hm/t symbolic-ref -q HEAD >/dev/null&&[ $rk4 = 0 ]&&[ "$($G -C $T/hm/t rev-parse HEAD)" = "$(tip)" ]&&[ -z "$($G -C $T/hm/t status -s)" ]&&[ "$(grep -c "mine K4" $T/hm/t/$NA)" = 1 ]'
# k5 (R4, m1 ported) a KID: AGI_POST=<kid> with no posts/<kid>. agi-turn / agi-flush exit 5, commit NOTHING, never touch the parent's branch or archive entry
runk(){ (cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=kid1 RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 "$@");}
mk;pa=$($G -C $T/g rev-parse posts/alive);$G -C $T/g update-ref refs/archive/alive/$MA $pa;kd=$T/wt/kid-tree;mkdir -p $kd/.agi/nodes/doc;printf '%s\n' $NA >$kd/.p;cp $T/g/$NA $kd/$NA;echo "kid edit" >>$kd/$NA
runk agi-turn 2>$T/ek5;rk5=$?;runk agi-flush 2>$T/ek5b;rk5b=$?
ok "k5-a-kid-fails-closed AGI_POST=kid1, no posts/kid1: agi-turn rc $rk5 (want 5), agi-flush rc $rk5b (want 5), [no-branch] label: $(grep -c '^\[no-branch\]' $T/ek5) (want 1); posts/alive unchanged: $([ "$(tip)" = $pa ]&&echo yes||echo NO), the parent's archive entry unchanged: $([ "$($G -C $T/g rev-parse refs/archive/alive/$MA)" = $pa ]&&echo yes||echo NO), refs under kid1: $($G -C $T/g for-each-ref refs/archive/kid1 refs/heads/posts/kid1|wc -l|tr -d ' ') (want 0), the kid's tree and edit kept: $(grep -c 'kid edit' $kd/$NA) (want 1)" '[ $rk5 = 5 ]&&[ $rk5b = 5 ]&&[ "$(grep -c "^\[no-branch\]" $T/ek5)" = 1 ]&&[ "$(tip)" = $pa ]&&[ "$($G -C $T/g rev-parse refs/archive/alive/$MA)" = $pa ]&&[ "$($G -C $T/g for-each-ref refs/archive/kid1 refs/heads/posts/kid1|wc -l|tr -d " ")" = 0 ]&&[ "$(grep -c "kid edit" $kd/$NA)" = 1 ]'
ok "k5b-agi-kid-line-carries-the-guards-signal agi-kid's exec line carries AGI_ROLE=kid (the signal agi-turn refuses on): $(src|awk '/^### agi-kid /{p=1} p&&/AGI_ROLE=kid /{print;exit}'|grep -c 'AGI_ROLE=kid ') (want 1); no post row in the geometry has role kid: $(sed -n 's/^  - {/{/p' $R0/.agi/nodes/.geometry/posts.md 2>/dev/null|grep -c '"role": *"kid"') (want 0)" 'src|awk "/^### agi-kid /{p=1} p&&/AGI_ROLE=kid /{print;exit}"|grep -q "AGI_ROLE=kid "'
# k5c the REAL kid env: AGI_POST=<parent> INHERITED from the unit (posts/<parent> exists) + AGI_ROLE=kid: agi-turn and agi-flush still exit 5 and commit NOTHING onto the parent's branch
runr(){ (cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=alive AGI_ROLE=kid RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_WT_HOLD=101 "$@");}
mk;pa=$($G -C $T/g rev-parse posts/alive);$G -C $T/g update-ref refs/archive/alive/$MA $pa;kd=$T/wt/kid-tree;mkdir -p $kd/.agi/nodes/doc;printf '%s\n' $NA >$kd/.p;cp $T/g/$NA $kd/$NA;echo "kid edit" >>$kd/$NA
runr agi-turn 2>$T/ek5c;rk5c=$?;runr agi-flush 2>$T/ek5d;rk5d=$?
ok "k5c-a-PRE-CUT-kid-with-the-parents-post-name-fails-closed (only a kid from before agi-kid set AGI_POST=\$k still inherits the parent's name; AGI_ROLE=kid is what refuses it) AGI_POST=alive (inherited, posts/alive EXISTS) + AGI_ROLE=kid: agi-turn rc $rk5c (want 5), agi-flush rc $rk5d (want 5), [no-branch] label: $(grep -c '^\[no-branch\]' $T/ek5c) (want 1); posts/alive unchanged: $([ "$(tip)" = $pa ]&&echo yes||echo NO), the parent's archive entry unchanged: $([ "$($G -C $T/g rev-parse refs/archive/alive/$MA)" = $pa ]&&echo yes||echo NO), the kid's tree and edit kept: $(grep -c 'kid edit' $kd/$NA) (want 1)" '[ $rk5c = 5 ]&&[ $rk5d = 5 ]&&[ "$(grep -c "^\[no-branch\]" $T/ek5c)" = 1 ]&&[ "$(tip)" = $pa ]&&[ "$($G -C $T/g rev-parse refs/archive/alive/$MA)" = $pa ]&&[ "$(grep -c "kid edit" $kd/$NA)" = 1 ]'
# k6 (R5) chk FAILS CLOSED: a git failure while it reads the tree keeps the tree (the pipe took tr's status, so a failure meant an empty list and rm -rf)
for fl in faildiff faills;do mk;da=$(run agi-wt pull doc:a);echo "mine K6" >>$da/$NA;: >$T/$fl;run agi-wt drop doc:a 2>$T/ek6;rk6=$?;rm -f "${T:?}/${fl:?}"
 ok "k6-chk-fails-closed-$fl git fails while chk reads the tree: agi-wt drop rc $rk6 (want != 0), the tree kept: $([ -d $da ]&&echo yes||echo NO), the edit still in it: $(grep -c 'mine K6' $da/$NA 2>/dev/null||echo 0) (want 1), label [$(grep -c 'dirty' $T/ek6)] (want 1)" '[ $rk6 != 0 ]&&[ -d $da ]&&[ "$(grep -c "mine K6" $da/$NA)" = 1 ]&&grep -q dirty $T/ek6';done
# k7 (R6) flush resolves the trunk ONCE: the trunk moves while merge-tree runs; the merge commit's 2nd parent is the sha merge-tree was given, not the moved trunk
mk;$G -C $T/g checkout -q posts/alive;echo post >$T/g/post-only.txt;$G -C $T/g add post-only.txt;$G -C $T/g commit -qm postside;$G -C $T/g checkout -q trunk;tmove;: >$T/movetrunk;run agi-flush 2>$T/ek7;rk7=$?;t1=$(tip);mt=$(awk '{print $NF}' $T/mt.args 2>/dev/null);p2=$($G -C $T/g rev-parse $t1^2 2>/dev/null)
ok "k7-flush-resolves-the-trunk-once the trunk moved during merge-tree: agi-flush rc $rk7 (want 0), merge-tree was given [$(echo $mt|cut -c1-12)], the tip's 2nd parent is [$(echo $p2|cut -c1-12)] (want equal), the moved trunk [$($G -C $T/g rev-parse trunk|cut -c1-12)] is NOT an ancestor: $($G -C $T/g merge-base --is-ancestor trunk posts/alive&&echo YES||echo no) (want no)" '[ $rk7 = 0 ]&&[ -n "$mt" ]&&[ "$mt" = "$p2" ]&&! $G -C $T/g merge-base --is-ancestor trunk posts/alive'
# k8 (R7) a kept tree has a READER: agi-brief prints the kept ref and the open tree dir at SessionStart; a clean stop prints neither
printf '#!/bin/sh\nif [ -n "%s" ];then cat "%s";else cat %s/.agi/nodes/.geometry/engine*.md;fi|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"\n' "$PIECES" "$PIECES" "$R0" >$T/bin/sect;chmod +x $T/bin/sect;sect agi-brief >$T/bin/agi-brief;chmod +x $T/bin/agi-brief
brf(){ echo '{"source":"compact"}'|(cd $T/hm/t&&env -i PATH=$T/shim:$T/bin:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt agi-brief 2>&1);}
mk;da=$(run agi-wt pull doc:a);echo "mine K8" >>$da/$NA;echo stray >$da/stray.txt;run agi-flush 2>/dev/null;brf >$T/ek8
ok "k8-agi-brief-reads-a-kept-tree-back after a stop that kept a tree: the brief names the kept ref: $(grep -c "^\[kept\] refs/archive/alive/$MA" $T/ek8) (want 1) and the open tree: $(grep -c "^\[tree\] $da" $T/ek8) (want 1)" '[ "$(grep -c "^\[kept\] refs/archive/alive/$MA" $T/ek8)" = 1 ]&&[ "$(grep -c "^\[tree\] $da" $T/ek8)" = 1 ]'
mk;da=$(run agi-wt pull doc:a);echo "mine K8b" >>$da/$NA;run agi-flush 2>/dev/null;brf >$T/ek8b
ok "k8b-agi-brief-prints-nothing-for-a-clean-stop a stop that landed everything: [kept]/[tree] lines: $(grep -c '^\[kept\]\|^\[tree\]' $T/ek8b) (want 0)" '[ "$(grep -c "^\[kept\]\|^\[tree\]" $T/ek8b)" = 0 ]'
# ====================================================================================================================================================================
# v5e (SM's v5d return on 91393fdc42: V1-V5; DG2 lane rows, goal:g7.16.1.11.11): ONE name rule at the door (a node path whose basename holds a space or leads with a dot is refused, named, or hashed -- either way no tree is skipped); ONE writer guard (no AGI_POST, a kid, or no posts/P = rc 5 + [no-branch] from agi-at, agi-turn, agi-flush, agi-wt drop, before ANY git write, never rc 2: a Stop hook's exit 2 re-enters the model); the [kept] reader walks the ref's HISTORY; the survivors N1 N2 N4 and purge's NOT SAVED branch get rows. Rows assert the OUTCOME (landed, refused, or kept whole on a ref), not the fix's shape
# ====================================================================================================================================================================
wnode(){ mkdir -p "$(dirname "$1/$2")";printf -- '---\nid: doc:%s\nmint_id: %s\ntype: doc\n---\nnew %s\n' "$3" "$4" "$3" >"$1/$2";}
held(){ for r in $($G -C $T/g for-each-ref --format='%(refname)' refs/archive/alive);do $G -C $T/g show "$r:$1" 2>/dev/null;done;}
# v1 (V1): `agi-wt new` of '.agi/nodes/doc/my note.md' / '.agi/nodes/doc/.hid.md' names the dir wt/my note / wt/.hid: the unquoted [ -f $d.p ] / [ -d $d ] skip the first, `*/` never matches the second. v5d: the node never lands, 0 archive refs, flush rc 0 with the tree in RAM = LOST at the stop
MN=nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
for nm in "my note" ".hid";do
 id=$(echo "$nm"|tr -d ' .')
 mk;np=".agi/nodes/doc/$nm.md";nd=$(run agi-wt new "$np" 2>$T/ev1n);rn=$?;[ $rn = 0 ]&&[ -d "$nd" ]&&wnode "$nd" "$np" v1 $MN;en=$(head -c 80 $T/ev1n|tr '\n' '|')
 b0=$(tip);run agi-turn 2>$T/ev1t;rt=$?;lt=$(sx "posts/alive:$np"|grep -c 'new v1');rf=0;[ $rn = 7 ]&&grep -qF "[$nm]" $T/ev1n&&grep -qF "must match [A-Za-z0-9_-][A-Za-z0-9._-]*" $T/ev1n&&[ -z "$(ls -A $T/wt)" ]&&rf=1
 ok "v1a-new-refuses-the-name-[$id] agi-wt new '$np': rc $rn (want 7, ruling (a) = REFUSE), stderr [$en] (want it to name [$nm] and say: must match [A-Za-z0-9_-][A-Za-z0-9._-]*), no tree under \$AGI_WT: $([ -z "$(ls -A $T/wt)" ]&&echo yes||echo NO); then agi-turn rc $rt (want 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged)" '[ $rf = 1 ]&&[ $rt = 0 ]&&[ $(tip) = $b0 ]'
 mk;nd=$(run agi-wt new "$np" 2>$T/ev1n);rn=$?;[ $rn = 0 ]&&[ -d "$nd" ]&&wnode "$nd" "$np" v1 $MN
 run agi-flush 2>$T/ev1f;rf1=$?;lt=$(sx "posts/alive:$np"|grep -c 'new v1');rm1=$(ls -A $T/wt|wc -l|tr -d ' ');hd=$(held "$np"|grep -c 'new v1');rf=0;[ $rn != 0 ]&&[ -s $T/ev1n ]&&[ $rn = 7 ]&&grep -qF "[$nm]" $T/ev1n&&grep -qF "must match [A-Za-z0-9_-][A-Za-z0-9._-]*" $T/ev1n&&[ "$rm1" = 0 ]&&rf=1
 ok "v1b-flush-after-a-refused-name-has-nothing-to-lose-[$id] agi-wt new '$np' + a node written: new rc $rn (want 7, named [$nm]: $(grep -cF "[$nm]" $T/ev1n)); agi-flush rc $rf1 (want 0); the node on posts/alive: $lt (want 0: it was never taken); trees left under \$AGI_WT: $rm1 (want 0); the node on a refs/archive/alive ref: $hd (want 0)" '[ $rf = 1 ]&&[ $rf1 = 0 ]&&[ $lt = 0 ]&&[ $hd = 0 ]'
done
# v2 (V2): a KID (AGI_ROLE=kid, the parent's AGI_POST inherited) with the trunk ONE COMMIT AHEAD: agi-flush still ran merge-tree + commit-tree -S + update-ref on the PARENT's branch with the parent's key; agi-at has NO guard at all
mk;tmove;pa=$(tip);runr agi-flush 2>$T/ev2;rv2=$?
ok "v2a-a-kid-flush-with-the-trunk-ahead-moves-nothing AGI_ROLE=kid, AGI_POST=alive, posts/alive exists, the trunk has a commit the tip lacks: agi-flush rc $rv2 (want 5), posts/alive $([ "$(tip)" = $pa ]&&echo unchanged||echo MOVED) (want unchanged), [no-branch] lines: $(grep -c '^\[no-branch\]' $T/ev2) (want >= 1)" '[ $rv2 = 5 ]&&[ "$(tip)" = $pa ]&&[ "$(grep -c "^\[no-branch\]" $T/ev2)" -ge 1 ]'
mk;pa=$(tip);echo "kid at" >>$T/hm/t/README.md;runr agi-at README.md 2>$T/ev2b;rv2b=$?
ok "v2b-a-kid-agi-at-commits-nothing AGI_ROLE=kid, AGI_POST=alive, a stray edit in ~/t: agi-at README.md rc $rv2b (want 5), posts/alive $([ "$(tip)" = $pa ]&&echo unchanged||echo MOVED) (want unchanged), [no-branch] lines: $(grep -c '^\[no-branch\]' $T/ev2b) (want >= 1), the edit kept in ~/t: $(grep -c 'kid at' $T/hm/t/README.md) (want 1)" '[ $rv2b = 5 ]&&[ "$(tip)" = $pa ]&&[ "$(grep -c "^\[no-branch\]" $T/ev2b)" -ge 1 ]&&[ "$(grep -c "kid at" $T/hm/t/README.md)" = 1 ]'
mk;pa=$(tip);echo "kid at" >>$T/hm/t/README.md;runk agi-at README.md 2>$T/ev2c;rv2c=$?
ok "v2c-agi-at-with-no-branch-for-the-post-exits-5 AGI_POST=kid1, no posts/kid1: agi-at README.md rc $rv2c (want 5, not git's 1), posts/alive $([ "$(tip)" = $pa ]&&echo unchanged||echo MOVED) (want unchanged), [no-branch] lines: $(grep -c '^\[no-branch\]' $T/ev2c) (want >= 1)" '[ $rv2c = 5 ]&&[ "$(tip)" = $pa ]&&[ "$(grep -c "^\[no-branch\]" $T/ev2c)" -ge 1 ]'
mk;da=$(run agi-wt pull doc:a);echo "kid drop" >>$da/$NA;pa=$(tip);runr agi-wt drop doc:a 2>$T/ev2d;rv2d=$?
ok "v2d-a-kid-agi-wt-drop-commits-nothing-and-keeps-the-tree (stays green) AGI_ROLE=kid: agi-wt drop doc:a rc $rv2d (want 5), posts/alive $([ "$(tip)" = $pa ]&&echo unchanged||echo MOVED) (want unchanged), the tree kept with the edit: $(grep -c 'kid drop' $da/$NA 2>/dev/null||echo 0) (want 1)" '[ $rv2d = 5 ]&&[ "$(tip)" = $pa ]&&[ "$(grep -c "kid drop" $da/$NA)" = 1 ]'
# v3 (V3): agi-turn is the Stop hook and a Stop hook's exit 2 = "block the stop, feed stderr to the model". AGI_POST unset: every ref-moving piece exits 5 (agi-flush and agi-wt already do); agi-turn and agi-at died on ${AGI_POST:?} with rc 2
mk;da=$(run agi-wt pull doc:a);echo "nopost v3" >>$da/$NA;echo "nopost v3" >>$T/hm/t/README.md;b0=$(tip);rcs=;nrc2=0;nbad=0
for cmd in "agi-turn" "agi-at README.md" "agi-flush" "agi-wt drop doc:a";do run0 $cmd 2>$T/ev3;r=$?;rcs="$rcs [$cmd]=$r";[ $r = 2 ]&&nrc2=$((nrc2+1));[ $r = 5 ]||nbad=$((nbad+1));done
ok "v3-no-piece-exits-2-when-the-post-is-unset AGI_POST unset: rcs$rcs (want every one 5); exits of 2: $nrc2 (want 0); nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO); the tree and its edit kept: $(grep -c 'nopost v3' $da/$NA 2>/dev/null||echo 0) (want 1)" '[ $nrc2 = 0 ]&&[ $nbad = 0 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "nopost v3" $da/$NA)" = 1 ]'
# v4 (V4): the [kept] reader walks the ref's HISTORY. A kept whole-tree (stray file) sits on refs/archive/alive/<mint>; a LATER [moved] commit on the same ref (subject 'alive: <path>') buries it, and the stray file then lives only in that older commit
mk;db=$(run agi-wt pull doc:b);echo "mine V4" >>$db/$NB;echo stray >$db/stray.txt;run agi-flush 2>/dev/null;AR=refs/archive/alive/$MB;k1=$($G -C $T/g rev-parse -q --verify $AR||echo none)
rm -rf $db;db=$(run agi-wt pull doc:b);mv_b one;echo "mine V4b" >>$db/$NB;run agi-turn 2>$T/ev4t;sub=$($G -C $T/g log -1 --format=%s $AR 2>/dev/null);brf >$T/ev4
ok "v4-brief-reads-a-kept-commit-buried-under-a-later-moved-commit the kept commit $(echo $k1|cut -c1-10) (stray.txt in it: $($G -C $T/g cat-file -e $k1:stray.txt 2>/dev/null&&echo yes||echo NO)) is an ancestor of $AR: $($G -C $T/g merge-base --is-ancestor $k1 $AR 2>/dev/null&&echo yes||echo NO); the ref's tip subject is [$sub] (want a [moved] subject, not 'kept'); the brief names the ref: $(grep -c "^\[kept\] $AR" $T/ev4) (want 1)" '[ $k1 != none ]&&$G -C $T/g cat-file -e $k1:stray.txt&&$G -C $T/g merge-base --is-ancestor $k1 $AR&&case $sub in *kept*)false;; *)true;;esac&&[ "$(grep -c "^\[kept\] $AR" $T/ev4)" = 1 ]'
mk;db=$(run agi-wt pull doc:b);mv_b one;echo "mine V4c" >>$db/$NB;run agi-turn 2>/dev/null;AR=refs/archive/alive/$MB;brf >$T/ev4c
ok "v4b-a-moved-only-ref-is-not-kept (stays green) a ref that only ever got a [moved] commit (no kept commit in its history): the ref exists: $($G -C $T/g rev-parse -q --verify $AR >/dev/null&&echo yes||echo NO) (want yes), [kept] lines in the brief: $(grep -c '^\[kept\]' $T/ev4c) (want 0)" '$G -C $T/g rev-parse -q --verify $AR >/dev/null&&[ "$(grep -c "^\[kept\]" $T/ev4c)" = 0 ]'
# e1 (SM v5e E1): the [kept] reader must not depend on posts/P existing. A deleted or renamed branch hid every kept tree at exactly the moment they matter (`git log $r --not refs/heads/posts/P` died, rc 128, and the loop printed nothing)
mk;da=$(run agi-wt pull doc:a);echo "mine E1" >>$da/$NA;echo stray >$da/stray.txt;run agi-flush 2>/dev/null;AR=refs/archive/alive/$MA;kk=$($G -C $T/g rev-parse -q --verify $AR||echo none);$G -C $T/g update-ref -d refs/heads/posts/alive;brf >$T/ee1
ok "e1-brief-prints-kept-when-the-branch-is-gone a kept whole tree on $AR (stray.txt in it: $($G -C $T/g cat-file -e $kk:stray.txt 2>/dev/null&&echo yes||echo NO)), then posts/alive deleted (still there: $($G -C $T/g rev-parse -q --verify refs/heads/posts/alive >/dev/null&&echo YES||echo no)): the brief names the ref: $(grep -c "^\[kept\] $AR" $T/ee1) (want 1), and does not die: [$(grep -c 'fatal' $T/ee1)] fatal line(s) (want 0)" '[ $kk != none ]&&$G -C $T/g cat-file -e $kk:stray.txt&&! $G -C $T/g rev-parse -q --verify refs/heads/posts/alive >/dev/null&&[ "$(grep -c "^\[kept\] $AR" $T/ee1)" = 1 ]&&[ "$(grep -c fatal $T/ee1)" = 0 ]'
# e3 (DG1 survivor): the walk reads ONLY the archive ref's own commits (`--not` the tip). A post commit whose SUBJECT matches '^[^ ]*: kept ' (alive: kept the plan) is in the archive ref's ancestry (every archive commit is parented on the tip it was made from): without the --not the brief prints a FALSE [kept] for a ref that holds only a [moved] commit
mk;db=$(run agi-wt pull doc:b);t0=$(tip);pc=$(echo "alive: kept the plan"|$G -C $T/g commit-tree -S -p $t0 $t0^{tree});$G -C $T/g update-ref refs/heads/posts/alive $pc $t0;mv_b one;echo "mine E3" >>$db/$NB;run agi-turn 2>/dev/null;AR=refs/archive/alive/$MB;brf >$T/ee3;sb=$($G -C $T/g log -1 --format=%s $AR 2>/dev/null);ap=$($G -C $T/g merge-base --is-ancestor $pc $AR 2>/dev/null&&echo yes||echo NO)
ok "e3-a-post-commit-subject-kept-is-not-a-kept-tree the ref $AR holds only a [moved] commit (tip subject [$sb], want alive: <path>), the post's own commit [alive: kept the plan] is in its ancestry: $ap (want yes) and on posts/alive: $($G -C $T/g merge-base --is-ancestor $pc posts/alive&&echo yes||echo NO) (want yes): the brief prints [kept] lines: $(grep -c '^\[kept\]' $T/ee3) (want 0)" '[ "$ap" = yes ]&&$G -C $T/g merge-base --is-ancestor $pc posts/alive&&case $sb in *kept*)false;; *)true;;esac&&[ "$(grep -c "^\[kept\]" $T/ee3)" = 0 ]'
# v5 lane gaps. N1: purge treats a tree it cannot READ (chk rc 2) as clean and removes it -- the stray file is then lost with no ref. (the turn's own reads are not shimmed: only chk's diff --name-only / ls-files -o fail)
for fl in faildiff faills;do mk;da=$(run agi-wt pull doc:a);echo "mine N1" >>$da/$NA;echo stray >$da/stray.txt;: >$T/$fl;run agi-flush 2>$T/ev5;r5=$?;rm -f "${T:?}/${fl:?}";AR=refs/archive/alive/$MA
 ok "v5-n1-purge-keeps-a-tree-it-cannot-read-$fl git fails while purge reads the tree (a stray file beside the edit): agi-flush rc $r5 (want != 0), the tree kept: $([ -d $da ]&&echo yes||echo NO), stray.txt whole on $AR: $($G -C $T/g show $AR:stray.txt 2>/dev/null|grep -c stray) (want 1), a [kept] line: $(grep -c '^\[kept\]' $T/ev5) (want 1)" '[ $r5 != 0 ]&&[ -d $da ]&&[ "$($G -C $T/g show $AR:stray.txt|grep -c stray)" = 1 ]&&[ "$(grep -c "^\[kept\]" $T/ev5)" = 1 ]';done
# N2: the kept save is a CAS on refs/archive/P/<dir> (old value = the ref's tip, or "" = must not exist): a racer on that ref during purge is not overwritten, the save is reported NOT SAVED and the tree stays
mk;da=$(run agi-wt pull doc:a);echo "mine N2" >>$da/$NA;echo stray >$da/stray.txt;AR=refs/archive/alive/$MA;echo "$AR $NA $MA a" >$T/racespec;run agi-flush 2>$T/ev6;r6=$?;sub=$($G -C $T/g log -1 --format=%s $AR 2>/dev/null)
ok "v5-n2-the-kept-save-is-a-cas a racer creates $AR while purge saves the stray tree: agi-flush rc $r6 (want != 0), the ref's tip is the racer's: [$sub] (want racer), [kept] ... NOT SAVED lines: $(grep '^\[kept\]' $T/ev6|grep -c 'NOT SAVED') (want 1), the tree kept with stray.txt: $([ -f $da/stray.txt ]&&echo yes||echo NO)" '[ $r6 != 0 ]&&[ "$sub" = racer ]&&[ "$(grep "^\[kept\]" $T/ev6|grep -c "NOT SAVED")" = 1 ]&&[ -f $da/stray.txt ]'
# N4: a NEW tree whose node is already identical to the tip never gets a .b (the turn has nothing to commit): purge must fall back to the tip, find it clean and remove it, rc 0 -- not keep a clean tree
mk;nd=$(run agi-wt new $NA 2>/dev/null);mkdir -p $nd/.agi/nodes/doc;$G -C $T/g show posts/alive:$NA >$nd/$NA;b0=$(tip);run agi-flush 2>$T/ev7;r7=$?
ok "v5-n4-a-clean-new-tree-without-dot-b-is-removed an agi-wt new tree holding the tip's own node bytes (no commit, so no .b: $([ -e $nd/.b ]&&echo HAS-b||echo none)): agi-flush rc $r7 (want 0), the tree gone: $([ -d $nd ]&&echo NO||echo yes), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), stderr [$(head -c 60 $T/ev7)] (want empty)" '[ $r7 = 0 ]&&[ ! -d $nd ]&&[ -z "$($G -C $T/g for-each-ref refs/archive)" ]&&[ $(tip) = $b0 ]&&[ ! -s $T/ev7 ]'
# purge NOT SAVED: the kept save cannot be signed (no signer): the tree is KEPT whole in RAM with the edit, [kept] says NOT SAVED, rc != 0, no ref, nothing committed
mk;da=$(run agi-wt pull doc:a);echo "mine NS" >>$da/$NA;$G -C $T/g config --unset user.signingkey;b0=$(tip);run agi-flush 2>$T/ev8;r8=$?
ok "v5-purge-not-saved-keeps-the-tree no signer: agi-flush rc $r8 (want != 0), [kept] ... NOT SAVED lines: $(grep '^\[kept\]' $T/ev8|grep -c 'NOT SAVED') (want 1), the tree kept with the edit: $(grep -c 'mine NS' $da/$NA 2>/dev/null||echo 0) (want 1), refs/archive refs: $($G -C $T/g for-each-ref refs/archive|wc -l|tr -d ' ') (want 0), nothing committed: $([ $(tip) = $b0 ]&&echo yes||echo NO)" '[ $r8 != 0 ]&&[ "$(grep "^\[kept\]" $T/ev8|grep -c "NOT SAVED")" = 1 ]&&[ "$(grep -c "mine NS" $da/$NA)" = 1 ]&&[ -z "$($G -C $T/g for-each-ref refs/archive)" ]&&[ $(tip) = $b0 ]'
# ====================================================================================================================================================================
# GROWTH ORDER on the v5 plain path (goal:g7.16.1.11.8 falsifier; belam-s2-II 08:3xZ, SM; DG2's rows FIRST, DG3 builds the check into agi-turn): `write.py create` ran the spawn gate; a post that writes a node file with Write/Edit and lands it with agi-turn did not. Contract: on each NEW node file in the turn's commit (a path under .agi/nodes that is not on the tip) agi-turn reads the file's front matter and runs the SAME parent_shapes / allowed_parents / min_parents rule spawn_gate.check_spawn runs (reuse it, no second copy of the rule); a refusal prints ONE bracketed line naming the node and the rule, exits non-zero, commits NOTHING for that tree and keeps it. An EDIT of an existing node is never gated (a legacy node with legacy parents stays editable). The fixture is a scratch repo that carries the engine's own extensions/agi/{bin,src} and .agi/context/schemas (so the check can run from ~/t) and a tiny corpus: goal:g1, hypothesis:h1 (parent goal:g1) and a LEGACY experiment:x1 whose parent is goal:g1 (an experiment may not be parented by a goal today)

# newexp ID MINT PARENT...: a NEW experiment node in a fresh agi-wt new tree (prints the tree dir)
newexp(){ id=$1;mi=$2;shift 2;ne=$(run agi-wt new .agi/nodes/experiment/$id.md 2>/dev/null);mkdir -p $ne/.agi/nodes/experiment;{ printf -- '---\nid: experiment:%s\nmint_id: %s\ntype: experiment\n' $id $mi;if [ $# = 0 ];then echo 'parents: []';else echo parents:;for pp in "$@";do echo "  - $pp";done;fi;printf -- '---\nnew %s\n' $id;}>$ne/.agi/nodes/experiment/$id.md;}
# go1: an out-of-order NEW node (an experiment parented by a goal) is REFUSED: rc != 0, nothing committed, the tree kept, ONE bracketed line naming the node and the rule
mkgo;newexp o1 000000000000000000000000000000d1 goal:g1;b0=$(tip);run agi-turn 2>$T/ego1;rgo1=$?;fo=$ne/.agi/nodes/experiment/o1.md
ok "go1-an-out-of-order-new-node-is-refused agi-turn over a NEW experiment parented by goal:g1 (allowed: hypothesis verdict task idea experiment build): rc $rgo1 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), the node on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/o1.md 2>/dev/null&&echo YES||echo no) (want no), the tree kept with the file: $([ -f $fo ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ego1) (want exactly 1), naming the node: $(grep '^\[' $T/ego1|grep -c 'experiment/o1\|experiment:o1\|o1.md') (want 1), naming the rule: $(grep '^\[' $T/ego1|grep -c 'allowed_parents') (want 1)" '[ $rgo1 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/o1.md 2>/dev/null&&[ -f $fo ]&&[ "$(grep -c "^\[" $T/ego1)" = 1 ]&&[ "$(grep "^\[" $T/ego1|grep -c "experiment/o1\|experiment:o1\|o1.md")" = 1 ]&&[ "$(grep "^\[" $T/ego1|grep -c allowed_parents)" = 1 ]'
# go1b: a second rule class (min_parents: a NEW experiment with NO parent) -- the check is the spawn gate's rule set, not one special case
mkgo;newexp o2 000000000000000000000000000000d2;b0=$(tip);run agi-turn 2>$T/ego1b;rgo1b=$?
ok "go1b-a-parentless-new-node-is-refused a NEW experiment with parents [] : rc $rgo1b (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), bracketed lines: $(grep -c '^\[' $T/ego1b) (want 1), naming min_parents: $(grep '^\[' $T/ego1b|grep -c 'min_parents') (want 1), the tree kept: $([ -f $ne/.agi/nodes/experiment/o2.md ]&&echo yes||echo NO)" '[ $rgo1b != 0 ]&&[ $(tip) = $b0 ]&&[ "$(grep -c "^\[" $T/ego1b)" = 1 ]&&[ "$(grep "^\[" $T/ego1b|grep -c min_parents)" = 1 ]&&[ -f $ne/.agi/nodes/experiment/o2.md ]'
# go2 (control): a LEGAL new node (an experiment parented by hypothesis:h1) is accepted as before
mkgo;newexp l1 000000000000000000000000000000e1 hypothesis:h1;b0=$(tip);run agi-turn 2>$T/ego2;rgo2=$?
ok "go2-a-legal-new-node-is-accepted a NEW experiment parented by hypothesis:h1: rc $rgo2 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1) [$($G -C $T/g log -1 --format=%s posts/alive)] (want alive: .agi/nodes/experiment/l1.md), the node on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&echo yes||echo NO), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/ego2) (want 0)" '[ $rgo2 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$($G -C $T/g log -1 --format=%s posts/alive)" = "alive: .agi/nodes/experiment/l1.md" ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/ego2)" = 0 ]'
# go3 (control): an EDIT of an existing node whose parents are LEGACY (experiment:x1 under goal:g1) is accepted -- no retro-refusal
mkgo;dx=$(run agi-wt pull experiment:x1 2>/dev/null);echo "an edit" >>$dx/.agi/nodes/experiment/x1.md;b0=$(tip);run agi-turn 2>$T/ego3;rgo3=$?
ok "go3-an-edit-of-a-legacy-node-is-never-gated experiment:x1 (parent goal:g1, grandfathered) edited in its pulled tree: rc $rgo3 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), the edit on the tip: $($G -C $T/g show posts/alive:.agi/nodes/experiment/x1.md|grep -c 'an edit') (want 1), bracketed lines: $(grep -c '^\[' $T/ego3) (want 0)" '[ $rgo3 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$($G -C $T/g show posts/alive:.agi/nodes/experiment/x1.md|grep -c "an edit")" = 1 ]&&[ "$(grep -c "^\[" $T/ego3)" = 0 ]'
# go4 (SM 09:27Z): one refused tree does not stop the next (as x7b). agi-turn walks $AGI_WT/*/ in glob order, so the REFUSED tree (a1) must sort FIRST and the legal one (z1) after it: a build that stops at the first refusal (G||{ k=1;break;}) then never reaches z1. The row asserts the order itself (non-vacuous), z1 landed, a1 kept
mkgo;newexp a1 000000000000000000000000000000d1 goal:g1;do1=$ne;newexp z1 000000000000000000000000000000e1 hypothesis:h1;fst=$(ls $T/wt|head -1);b0=$(tip);run agi-turn 2>$T/ego4;rgo4=$?
ok "go4-a-refused-tree-does-not-stop-the-next the out-of-order a1 (sorts FIRST: first tree dir [$fst], a1's is [$(basename $do1)]) and the legal z1 in one turn: rc $rgo4 (want != 0), z1 on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/z1.md 2>/dev/null&&echo yes||echo NO) (want yes), a1 on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/a1.md 2>/dev/null&&echo YES||echo no) (want no), new commits: $($G -C $T/g rev-list --count $b0..posts/alive) (want 1), a1's tree kept: $([ -f $do1/.agi/nodes/experiment/a1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ego4) (want 1)" '[ "$fst" = "$(basename $do1)" ]&&[ $rgo4 != 0 ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/z1.md&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/a1.md 2>/dev/null&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ -f $do1/.agi/nodes/experiment/a1.md ]&&[ "$(grep -c "^\[" $T/ego4)" = 1 ]'
# go5 (SM 08:59Z ruling): a MISSING or UNRUNNABLE checker FAILS CLOSED with a DISTINCT bracketed line (not the refusal line, which names a rule): rc != 0, nothing committed, the tree kept. A LEGAL node is used so only the checker's absence can refuse it. go5 = spawn_gate.py absent from the fixture (removed on the trunk, ~/t on the tip); go5b = it present but crashing (exit 1: neither APPROVED 0 nor REJECTED 2); go5c (SM 09:27Z) = it exiting 2 WITHOUT the REJECTED line (an argparse usage error exits 2): that is [spawn-gate-broken], never a refusal and never a rule name. Each variant asserts its LABEL: absent = [spawn-gate-missing], the others [spawn-gate-broken]
for v in absent crashing exit2;do
 lab=broken;[ $v = absent ]&&lab=missing;ec=1;[ $v = exit2 ]&&ec=2
 mkgo;if [ $v = absent ];then $G -C $T/g rm -q extensions/agi/bin/spawn_gate.py;else printf 'import sys\nsys.exit(%s)\n' $ec >$T/g/extensions/agi/bin/spawn_gate.py;$G -C $T/g add -A;fi;$G -C $T/g commit -qm "checker $v";$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive
 newexp l1 000000000000000000000000000000e1 hypothesis:h1;b0=$(tip);run agi-turn 2>$T/ego5$v;rgo5=$?;fl=$ne/.agi/nodes/experiment/l1.md;ll=$(grep '^\[' $T/ego5$v|head -3|cut -c1-110|tr '\n' '|')
 ok "go5-a-$v-checker-fails-closed-with-its-own-line a LEGAL new node (parent hypothesis:h1) with the checker $v: rc $rgo5 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), the node on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&echo YES||echo no) (want no), the tree kept: $([ -f $fl ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ego5$v) (want exactly 1) [$ll], naming a RULE (allowed_parents / min_parents / max_parents / parent_shapes): $(grep '^\[' $T/ego5$v|grep -cE 'allowed_parents|min_parents|max_parents|parent_shapes') (want 0: distinct from a refusal), naming the checker (spawn): $(grep '^\[' $T/ego5$v|grep -ci spawn) (want 1), the label [spawn-gate-$lab]: $(grep -c "^\[spawn-gate-$lab\]" $T/ego5$v) (want 1)" '[ $rgo5 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&[ -f $fl ]&&[ "$(grep -c "^\[" $T/ego5$v)" = 1 ]&&[ "$(grep "^\[" $T/ego5$v|grep -cE "allowed_parents|min_parents|max_parents|parent_shapes")" = 0 ]&&[ "$(grep "^\[" $T/ego5$v|grep -ci spawn)" = 1 ]&&[ "$(grep -c "^\[spawn-gate-$lab\]" $T/ego5$v)" = 1 ]'
done
# newraw ID: a NEW experiment node whose WHOLE file is stdin (flow lists, quoting), in a fresh agi-wt new tree ($ne)
newraw(){ id=$1;ne=$(run agi-wt new .agi/nodes/experiment/$id.md 2>/dev/null);mkdir -p $ne/.agi/nodes/experiment;cat >$ne/.agi/nodes/experiment/$id.md;}
# refused ID RC FILE: the common shape of a refusal row: rc != 0, the tip unchanged, the node not on the tip, the tree kept, ONE bracketed line naming the node and the rule allowed_parents
# go6 (SM 09:27Z, hole a): the parents are a MULTI-LINE flow list whose SECOND entry is illegal: a line-by-line reader sees no parent and accepts it as UNVERIFIED; the engine's own YAML reader sees goal:g1 -> refused
mkgo;newraw m6 <<'XX'
---
id: experiment:m6
mint_id: 000000000000000000000000000000d6
type: experiment
parents: [hypothesis:h1,
  goal:g1]
---
new m6
XX
b0=$(tip);run agi-turn 2>$T/ego6;rgo6=$?
ok "go6-a-multi-line-flow-list-with-an-illegal-parent-is-refused a NEW experiment with parents [hypothesis:h1,\\n goal:g1]: rc $rgo6 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/m6.md 2>/dev/null&&echo YES||echo no) (want no), the tree kept: $([ -f $ne/.agi/nodes/experiment/m6.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ego6) (want 1) naming the node and allowed_parents: $(grep '^\[' $T/ego6|grep -c 'm6.*allowed_parents\|experiment:m6.*allowed_parents') (want 1)" '[ $rgo6 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/m6.md 2>/dev/null&&[ -f $ne/.agi/nodes/experiment/m6.md ]&&[ "$(grep -c "^\[" $T/ego6)" = 1 ]&&[ "$(grep "^\[" $T/ego6|grep -c "m6.*allowed_parents")" = 1 ]'
# go9 (SM 09:27Z, hole a): a SINGLE-QUOTED illegal parent is refused, not accepted as UNVERIFIED because a regex did not see goal:g1
mkgo;newraw q9 <<'XX'
---
id: experiment:q9
mint_id: 000000000000000000000000000000d9
type: experiment
parents:
  - 'goal:g1'
---
new q9
XX
b0=$(tip);run agi-turn 2>$T/ego9;rgo9=$?
ok "go9-a-single-quoted-illegal-parent-is-refused a NEW experiment with parents [- 'goal:g1']: rc $rgo9 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/q9.md 2>/dev/null&&echo YES||echo no) (want no), the tree kept: $([ -f $ne/.agi/nodes/experiment/q9.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ego9) (want 1) naming the node and allowed_parents: $(grep '^\[' $T/ego9|grep -c 'q9.*allowed_parents') (want 1)" '[ $rgo9 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/q9.md 2>/dev/null&&[ -f $ne/.agi/nodes/experiment/q9.md ]&&[ "$(grep -c "^\[" $T/ego9)" = 1 ]&&[ "$(grep "^\[" $T/ego9|grep -c "q9.*allowed_parents")" = 1 ]'
# go8 (SM 09:27Z): the new-node list comes from git diff-index; when THAT fails the gate FAILS CLOSED with [spawn-gate-broken] (it must not read as "no new node"), nothing committed, the tree kept
mkgo;newexp l1 000000000000000000000000000000e1 hypothesis:h1;b0=$(tip);: >$T/faildi;run agi-turn 2>$T/ego8;rgo8=$?;rm -f $T/faildi
ok "go8-a-failing-diff-index-fails-closed a LEGAL new node while git diff-index fails: rc $rgo8 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&echo YES||echo no) (want no), the tree kept: $([ -f $ne/.agi/nodes/experiment/l1.md ]&&echo yes||echo NO), [spawn-gate-broken] lines: $(grep -c '^\[spawn-gate-broken\]' $T/ego8) (want 1), naming a rule: $(grep '^\['  $T/ego8|grep -cE 'allowed_parents|min_parents|max_parents|parent_shapes') (want 0)" '[ $rgo8 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&[ -f $ne/.agi/nodes/experiment/l1.md ]&&[ "$(grep -c "^\[spawn-gate-broken\]" $T/ego8)" = 1 ]&&[ "$(grep "^\[" $T/ego8|grep -cE "allowed_parents|min_parents|max_parents|parent_shapes")" = 0 ]'
# go7 (SM 09:27Z, hole b): a NEW live node that REPLACES a >=50%-similar existing node (the old one deleted in the SAME tree, so git -M sees R097) is still a NEW node: gated (here an illegal parent: refused). The tree is agi-wt new <new path> <old path>: the old path rides in .p and is absent from the tree = a delete
mkgo;ne=$(run agi-wt new .agi/nodes/experiment/r7.md .agi/nodes/experiment/x1.md 2>/dev/null);mkdir -p $ne/.agi/nodes/experiment;printf -- '---\nid: experiment:r7\nmint_id: 000000000000000000000000000000d7\ntype: experiment\nparents:\n  - goal:g1\n---\nlegacy experiment\n' >$ne/.agi/nodes/experiment/r7.md;b0=$(tip);run agi-turn 2>$T/ego7;rgo7=$?
ok "go7-a-replacing-node-is-still-a-new-node a NEW experiment r7 (parent goal:g1, illegal) that replaces the similar legacy x1 in one tree: rc $rgo7 (want != 0), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), r7 on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/r7.md 2>/dev/null&&echo YES||echo no) (want no), x1 still on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/x1.md 2>/dev/null&&echo yes||echo NO) (want yes), bracketed lines: $(grep -c '^\[' $T/ego7) (want 1) naming r7 and allowed_parents: $(grep '^\[' $T/ego7|grep -c 'r7.*allowed_parents') (want 1)" '[ $rgo7 != 0 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/r7.md 2>/dev/null&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/x1.md&&[ "$(grep -c "^\[" $T/ego7)" = 1 ]&&[ "$(grep "^\[" $T/ego7|grep -c "r7.*allowed_parents")" = 1 ]'
# go7b (control): a MOVE of the legacy node into .agi/nodes/deprecated/ (retire, never delete) is never gated, whatever its parents: rc 0, ONE commit, the deprecated copy on the tip and x1 gone from the live dir
mkgo;ne=$(run agi-wt new .agi/nodes/deprecated/experiment/x1.md .agi/nodes/experiment/x1.md 2>/dev/null);mkdir -p $ne/.agi/nodes/deprecated/experiment;printf -- '---\nid: experiment:x1\nmint_id: 000000000000000000000000000000c1\ntype: experiment\nstatus: deprecated\nparents:\n  - goal:g1\n---\nlegacy experiment\n' >$ne/.agi/nodes/deprecated/experiment/x1.md;b0=$(tip);run agi-turn 2>$T/ego7b;rgo7b=$?
ok "go7b-a-move-into-deprecated-is-never-gated the legacy x1 moved to .agi/nodes/deprecated/experiment/ (parent goal:g1): rc $rgo7b (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), the deprecated copy on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/deprecated/experiment/x1.md 2>/dev/null&&echo yes||echo NO), x1 gone from the live dir: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/x1.md 2>/dev/null&&echo NO||echo yes), bracketed lines: $(grep -c '^\[' $T/ego7b) (want 0)" '[ $rgo7b = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/deprecated/experiment/x1.md&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/x1.md 2>/dev/null&&[ "$(grep -c "^\[" $T/ego7b)" = 0 ]'
# ---- agi-at on the same gate (belam 09:3xZ, relayed by SM 09:28Z): a NEW .agi/nodes node committed through agi-at passes grow.py first, else rc 6 (distinct from 1 / 4 / 5), the tip unchanged, the edit STAYS in ~/t. ga helper: file CONTENT at ~/t/PATH
gaf(){ mkdir -p "$(dirname "$T/hm/t/$1")";cat >"$T/hm/t/$1";}
# ga1: an out-of-order NEW node via agi-at: rc 6, the tip unchanged, the file kept in ~/t, ONE bracketed line naming the node and the rule
mkgo;gaf .agi/nodes/experiment/o1.md <<'XX'
---
id: experiment:o1
mint_id: 000000000000000000000000000000d1
type: experiment
parents:
  - goal:g1
---
new o1
XX
b0=$(tip);run agi-at .agi/nodes/experiment/o1.md 2>$T/ega1;rga1=$?
ok "ga1-agi-at-refuses-an-out-of-order-new-node agi-at over a NEW experiment parented by goal:g1: rc $rga1 (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), the edit stays in ~/t: $([ -f $T/hm/t/.agi/nodes/experiment/o1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ega1) (want 1) naming o1 and allowed_parents: $(grep '^\[' $T/ega1|grep -c 'o1.*allowed_parents') (want 1)" '[ $rga1 = 6 ]&&[ $(tip) = $b0 ]&&[ -f $T/hm/t/.agi/nodes/experiment/o1.md ]&&[ "$(grep -c "^\[" $T/ega1)" = 1 ]&&[ "$(grep "^\[" $T/ega1|grep -c "o1.*allowed_parents")" = 1 ]'
# ga2 (control): a LEGAL new node via agi-at lands as before: rc 0, ONE signed commit
mkgo;gaf .agi/nodes/experiment/l1.md <<'XX'
---
id: experiment:l1
mint_id: 000000000000000000000000000000e1
type: experiment
parents:
  - hypothesis:h1
---
new l1
XX
b0=$(tip);run agi-at .agi/nodes/experiment/l1.md 2>$T/ega2;rga2=$?
ok "ga2-agi-at-lands-a-legal-new-node a NEW experiment parented by hypothesis:h1: rc $rga2 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md 2>/dev/null&&echo yes||echo NO), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/ega2) (want 0)" '[ $rga2 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/l1.md&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/ega2)" = 0 ]'
# ga3 (control): a path OUTSIDE .agi/nodes is unaffected, even a .md whose front matter would be refused as a node (notes/n.md), and a NEW non-.md file under .agi/nodes (the .geometry/ring that agi-out commits through agi-at is not a typed node)
mkgo;gaf notes/n9.md <<'XX'
---
id: experiment:n9
mint_id: 000000000000000000000000000000d9
type: experiment
parents:
  - goal:g1
---
not a node: it lives outside .agi/nodes
XX
gaf .agi/nodes/.geometry/ring <<'XX'
alive ssh-ed25519 AAAAfixture
XX
b0=$(tip);run agi-at notes/n9.md .agi/nodes/.geometry/ring 2>$T/ega3;rga3=$?
ok "ga3-agi-at-ignores-a-non-node-path notes/n9.md (a .md outside .agi/nodes) and a NEW .agi/nodes/.geometry/ring (not a .md): rc $rga3 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), both on the tip: $($G -C $T/g cat-file -e posts/alive:notes/n9.md 2>/dev/null&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/.geometry/ring 2>/dev/null&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ega3) (want 0)" '[ $rga3 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&$G -C $T/g cat-file -e posts/alive:notes/n9.md&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/.geometry/ring&&[ "$(grep -c "^\[" $T/ega3)" = 0 ]'
# ga4 (control): an EDIT of the legacy x1 (parent goal:g1) via agi-at is never gated
mkgo;echo "an at edit" >>$T/hm/t/.agi/nodes/experiment/x1.md;b0=$(tip);run agi-at .agi/nodes/experiment/x1.md 2>$T/ega4;rga4=$?
ok "ga4-agi-at-never-gates-an-edit experiment:x1 (legacy parent goal:g1) edited via agi-at: rc $rga4 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), the edit on the tip: $($G -C $T/g show posts/alive:.agi/nodes/experiment/x1.md|grep -c 'an at edit') (want 1), bracketed lines: $(grep -c '^\[' $T/ega4) (want 0)" '[ $rga4 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$($G -C $T/g show posts/alive:.agi/nodes/experiment/x1.md|grep -c "an at edit")" = 1 ]&&[ "$(grep -c "^\[" $T/ega4)" = 0 ]'
# ga5 / ga6: the gate FAILS CLOSED on agi-at too, with its own rc 6 and label: the checker absent (ga5, [spawn-gate-missing]); git diff-index failing (ga6, [spawn-gate-broken])
for v in absent faildi;do
 mkgo;if [ $v = absent ];then $G -C $T/g rm -q extensions/agi/bin/spawn_gate.py;$G -C $T/g commit -qm "checker absent";$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive;lab=missing;else lab=broken;fi
 gaf .agi/nodes/experiment/l1.md <<'XX'
---
id: experiment:l1
mint_id: 000000000000000000000000000000e1
type: experiment
parents:
  - hypothesis:h1
---
new l1
XX
 b0=$(tip);[ $v = faildi ]&&: >$T/faildi;run agi-at .agi/nodes/experiment/l1.md 2>$T/ega5$v;rga5=$?;rm -f $T/faildi
 ok "ga5-agi-at-fails-closed-$v a LEGAL new node via agi-at with $v: rc $rga5 (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), the edit stays: $([ -f $T/hm/t/.agi/nodes/experiment/l1.md ]&&echo yes||echo NO), [spawn-gate-$lab] lines: $(grep -c "^\[spawn-gate-$lab\]" $T/ega5$v) (want 1), naming a rule: $(grep '^\[' $T/ega5$v|grep -cE 'allowed_parents|min_parents|max_parents|parent_shapes') (want 0)" '[ $rga5 = 6 ]&&[ $(tip) = $b0 ]&&[ -f $T/hm/t/.agi/nodes/experiment/l1.md ]&&[ "$(grep -c "^\[spawn-gate-$lab\]" $T/ega5$v)" = 1 ]&&[ "$(grep "^\[" $T/ega5$v|grep -cE "allowed_parents|min_parents|max_parents|parent_shapes")" = 0 ]'
done
# ---- DG1 rows (SM 00:0xZ 10-11, DG2 unresponsive; tests only, no grow.py edit): the growth gate's two reads and its three verdicts, each pinned by a mutant in the commit message. All through agi-at (the same grow.py agi-turn calls; the paths are arguments, so a path the shell can hold is a path the lane can land).
# nexp: how many experiment nodes are on the tip (NUL-counted, so a path with a newline still counts once); the fixture starts with ONE (x1)
nexp(){ $G -C $T/g ls-tree -r --name-only -z posts/alive -- .agi/nodes/experiment|tr -cd '\0'|wc -c|tr -d ' ';}
# go10 / go10b / go10c / go10d: a node path with a DOUBLE QUOTE / a TAB / a BACKSLASH / a NEWLINE is JUDGED, never committed unchecked. git prints such a path C-quoted ("q\"x.md") unless diff-index runs with -z, and a quoted path no longer ends in .md, so a reader without -z skips the node: the illegal one (parent goal:g1) would land. -r = refused (rc 6, tip unchanged, tree kept, ONE line naming the node and allowed_parents); -c = control (a LEGAL node at the same path lands: rc 0, ONE signed commit), so the gate judged the path instead of refusing every odd name
for v in quote:go10 tab:go10b backslash:go10c newline:go10d;do
 lb=${v#*:};v=${v%:*}
 case $v in quote)nm='q"x';;tab)nm=$(printf 'q\tx');;backslash)nm='q\x';;newline)nm=$(printf 'q\nx');;esac
 p=".agi/nodes/experiment/$nm.md"
 mkgo;gaf "$p" <<XX
---
id: experiment:q10$v
mint_id: 0000000000000000000000000000d10$(echo $v|cut -c1)
type: experiment
parents:
  - goal:g1
---
new q10 $v
XX
 b0=$(tip);run agi-at "$p" 2>$T/ega10r$v;rg=$?
 ok "$lb-agi-at-judges-a-$v-in-the-path-and-refuses-the-illegal-node a NEW experiment (parent goal:g1) at a path with a $v: rc $rg (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), experiment nodes on the tip: $(nexp) (want 1), the edit stays in ~/t: $([ -f "$T/hm/t/$p" ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ega10r$v) (want 1) naming q10$v and allowed_parents: $(grep '^\[' $T/ega10r$v|grep -c "q10$v.*allowed_parents") (want 1)" '[ $rg = 6 ]&&[ $(tip) = $b0 ]&&[ "$(nexp)" = 1 ]&&[ -f "$T/hm/t/$p" ]&&[ "$(grep -c "^\[" $T/ega10r$v)" = 1 ]&&[ "$(grep "^\[" $T/ega10r$v|grep -c "q10$v.*allowed_parents")" = 1 ]'
 mkgo;gaf "$p" <<XX
---
id: experiment:q10$v
mint_id: 0000000000000000000000000000d10$(echo $v|cut -c1)
type: experiment
parents:
  - hypothesis:h1
---
new q10 $v
XX
 b0=$(tip);run agi-at "$p" 2>$T/ega10c$v;rg=$?
 ok "$lb-c-agi-at-lands-a-legal-node-at-a-$v-path a NEW experiment (parent hypothesis:h1) at the same path: rc $rg (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), experiment nodes on the tip: $(nexp) (want 2), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/ega10c$v) (want 0)" '[ $rg = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$(nexp)" = 2 ]&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/ega10c$v)" = 0 ]'
done
# gd1 (decoy): the parent hypothesis:hd exists ONLY as a file in ~/t, never staged: the gate resolves parents against the STAGED tree, so it is refused (rc 6, ONE line: the parent resolves nowhere in the staged tree). A reader of the working tree would find the decoy and land the child
mkgo;gaf .agi/nodes/hypothesis/hd.md <<'XX'
---
id: hypothesis:hd
mint_id: 000000000000000000000000000000b2
type: hypothesis
parents:
  - goal:g1
---
a decoy: in ~/t, not staged
XX
gaf .agi/nodes/experiment/d1.md <<'XX'
---
id: experiment:d1
mint_id: 000000000000000000000000000000d1
type: experiment
parents:
  - hypothesis:hd
---
child of a decoy
XX
b0=$(tip);run agi-at .agi/nodes/experiment/d1.md 2>$T/egd1;rgd1=$?
ok "gd1-agi-at-refuses-a-decoy-parent a NEW experiment parented by hypothesis:hd, a file in ~/t that agi-at was not asked to stage: rc $rgd1 (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), experiment nodes on the tip: $(nexp) (want 1), the edit stays: $([ -f $T/hm/t/.agi/nodes/experiment/d1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/egd1) (want 1) naming d1 and 'resolve nowhere': $(grep '^\[' $T/egd1|grep -c 'experiment:d1.*resolve nowhere') (want 1)" '[ $rgd1 = 6 ]&&[ $(tip) = $b0 ]&&[ "$(nexp)" = 1 ]&&[ -f $T/hm/t/.agi/nodes/experiment/d1.md ]&&[ "$(grep -c "^\[" $T/egd1)" = 1 ]&&[ "$(grep "^\[" $T/egd1|grep -c "experiment:d1.*resolve nowhere")" = 1 ]'
# gs1 (same tree): a parent staged TOGETHER with its child resolves (the staged tree is the tree being committed, not the tip): hypothesis:hs and the experiment under it, one agi-at call: rc 0, ONE signed commit with both. A reader of the tip would refuse the child
mkgo;gaf .agi/nodes/hypothesis/hs.md <<'XX'
---
id: hypothesis:hs
mint_id: 000000000000000000000000000000b3
type: hypothesis
parents:
  - goal:g1
---
a parent staged with its child
XX
gaf .agi/nodes/experiment/s1.md <<'XX'
---
id: experiment:s1
mint_id: 000000000000000000000000000000d2
type: experiment
parents:
  - hypothesis:hs
---
child of a same-tree parent
XX
b0=$(tip);run agi-at .agi/nodes/hypothesis/hs.md .agi/nodes/experiment/s1.md 2>$T/egs1;rgs1=$?
ok "gs1-agi-at-resolves-a-parent-staged-in-the-same-tree hypothesis:hs and its child experiment:s1 in ONE agi-at: rc $rgs1 (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), both on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/hypothesis/hs.md 2>/dev/null&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/s1.md 2>/dev/null&&echo yes||echo NO), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/egs1) (want 0)" '[ $rgs1 = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/hypothesis/hs.md&&$G -C $T/g cat-file -e posts/alive:.agi/nodes/experiment/s1.md&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/egs1)" = 0 ]'
# gu1 (unresolvable): a parent that exists NOWHERE (not on the tip, not in ~/t, not staged) is refused with the same distinct line, not committed
mkgo;gaf .agi/nodes/experiment/u1.md <<'XX'
---
id: experiment:u1
mint_id: 000000000000000000000000000000d3
type: experiment
parents:
  - hypothesis:nope
---
child of nothing
XX
b0=$(tip);run agi-at .agi/nodes/experiment/u1.md 2>$T/egu1;rgu1=$?
ok "gu1-agi-at-refuses-an-unresolvable-parent a NEW experiment parented by hypothesis:nope (exists nowhere): rc $rgu1 (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), experiment nodes on the tip: $(nexp) (want 1), the edit stays: $([ -f $T/hm/t/.agi/nodes/experiment/u1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/egu1) (want 1) naming u1 and 'resolve nowhere': $(grep '^\[' $T/egu1|grep -c 'experiment:u1.*resolve nowhere') (want 1)" '[ $rgu1 = 6 ]&&[ $(tip) = $b0 ]&&[ "$(nexp)" = 1 ]&&[ -f $T/hm/t/.agi/nodes/experiment/u1.md ]&&[ "$(grep -c "^\[" $T/egu1)" = 1 ]&&[ "$(grep "^\[" $T/egu1|grep -c "experiment:u1.*resolve nowhere")" = 1 ]'
# goall: an UNKNOWN TYPE (goall, a typo of goal) whose parents all resolve is REFUSED, not passed as UNVERIFIED: rc 6, nothing committed, ONE bracketed line
mkgo;gaf .agi/nodes/goall/z1.md <<'XX'
---
id: goall:z1
mint_id: 000000000000000000000000000000d4
type: goall
parents:
  - goal:g1
---
an unknown type
XX
b0=$(tip);run agi-at .agi/nodes/goall/z1.md 2>$T/egall;rgall=$?
ok "goall-agi-at-refuses-an-unknown-type a NEW node of type goall (parent goal:g1 resolves): rc $rgall (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), on the tip: $($G -C $T/g cat-file -e posts/alive:.agi/nodes/goall/z1.md 2>/dev/null&&echo YES||echo no) (want no), the edit stays: $([ -f $T/hm/t/.agi/nodes/goall/z1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/egall) (want 1) [$(grep '^\[' $T/egall|head -1|cut -c1-120)], naming the type goall: $(grep '^\[' $T/egall|grep -c goall) (want 1), [spawn-gate-broken] lines: $(grep -c '^\[spawn-gate-broken\]' $T/egall) (want 0)" '[ $rgall = 6 ]&&[ $(tip) = $b0 ]&&! $G -C $T/g cat-file -e posts/alive:.agi/nodes/goall/z1.md 2>/dev/null&&[ -f $T/hm/t/.agi/nodes/goall/z1.md ]&&[ "$(grep -c "^\[" $T/egall)" = 1 ]&&[ "$(grep "^\[" $T/egall|grep -c "goall")" = 1 ]&&[ "$(grep -c "^\[spawn-gate-broken\]" $T/egall)" = 0 ]'
# ---- DG1 rows 2 (SM 00:4xZ 10-11, Sonnet L1 findings on 6f64095d0a): the CR twin and the forged deprecated parent
# go10e: an ILLEGAL node at a path with a CARRIAGE RETURN ('a<CR>.md') and a LEGAL twin at the path with a LINEFEED ('a<LF>.md'), staged in ONE agi-at. diff-index -z read as TEXT turns '<CR>' into '<LF>' (universal newlines), so the list holds the twin's path twice, git show reads the twin twice, and the CR node is never read: it lands unchecked. REFUSED = rc 6, the tip unchanged, the CR node not on the tip, ONE line naming the CR node (experiment:c10) and allowed_parents
mkgo;cr=$(printf 'a\r');lf=$(printf 'a\nX');lf=${lf%X};pc=".agi/nodes/experiment/$cr.md";pl=".agi/nodes/experiment/$lf.md"
gaf "$pc" <<'XX'
---
id: experiment:c10
mint_id: 000000000000000000000000000000d5
type: experiment
parents:
  - goal:g1
---
the illegal node at the CR path
XX
gaf "$pl" <<'XX'
---
id: experiment:c11
mint_id: 000000000000000000000000000000d6
type: experiment
parents:
  - hypothesis:h1
---
the legal twin at the LF path
XX
b0=$(tip);run agi-at "$pc" "$pl" 2>$T/ega10e;rg=$?
ok "go10e-agi-at-reads-the-cr-node-and-not-its-lf-twin an ILLEGAL experiment (parent goal:g1) at a path with a CR and a LEGAL twin (parent hypothesis:h1) at a path with an LF, in ONE agi-at: rc $rg (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), experiment nodes on the tip: $(nexp) (want 1), both edits stay in ~/t: $([ -f "$T/hm/t/$pc" ]&&[ -f "$T/hm/t/$pl" ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/ega10e) (want 1) naming c10 and allowed_parents: $(grep '^\[' $T/ega10e|grep -c 'experiment:c10.*allowed_parents') (want 1)" '[ $rg = 6 ]&&[ $(tip) = $b0 ]&&[ "$(nexp)" = 1 ]&&[ -f "$T/hm/t/$pc" ]&&[ -f "$T/hm/t/$pl" ]&&[ "$(grep -c "^\[" $T/ega10e)" = 1 ]&&[ "$(grep "^\[" $T/ega10e|grep -c "experiment:c10.*allowed_parents")" = 1 ]'
# go10f (control): the LEGAL twin ALONE, at the LF path, lands (rc 0, ONE signed commit): the gate did not start refusing every path with a control character
mkgo;gaf "$pl" <<'XX'
---
id: experiment:c11
mint_id: 000000000000000000000000000000d6
type: experiment
parents:
  - hypothesis:h1
---
the legal twin at the LF path
XX
b0=$(tip);run agi-at "$pl" 2>$T/ega10f;rg=$?
ok "go10f-agi-at-lands-the-lf-twin-alone the LEGAL twin alone at the LF path: rc $rg (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), experiment nodes on the tip: $(nexp) (want 2), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/ega10f) (want 0)" '[ $rg = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$(nexp)" = 2 ]&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/ega10f)" = 0 ]'
# gd2 (forged deprecated parent): a parent id staged NEW under .agi/nodes/deprecated/ in THIS tree does not exist for the gate -- deprecated/ is exempt from the gate (a retire is a move), and an exemption must not mint a parent: hypothesis:hf is added under deprecated/ together with its child experiment:f1 in ONE agi-at: refused (rc 6, ONE line: the parent resolves nowhere), neither node on the tip
mkgo;gaf .agi/nodes/deprecated/hypothesis/hf.md <<'XX'
---
id: hypothesis:hf
mint_id: 000000000000000000000000000000b4
type: hypothesis
status: deprecated
parents:
  - goal:g1
---
a forged retired parent, new in this tree
XX
gaf .agi/nodes/experiment/f1.md <<'XX'
---
id: experiment:f1
mint_id: 000000000000000000000000000000d7
type: experiment
parents:
  - hypothesis:hf
---
child of a forged retired parent
XX
b0=$(tip);run agi-at .agi/nodes/deprecated/hypothesis/hf.md .agi/nodes/experiment/f1.md 2>$T/egd2;rgd2=$?
ok "gd2-agi-at-refuses-a-parent-forged-under-deprecated hypothesis:hf added NEW under .agi/nodes/deprecated/ and its child experiment:f1 in ONE agi-at: rc $rgd2 (want 6), the tip $([ $(tip) = $b0 ]&&echo unchanged||echo MOVED) (want unchanged), experiment nodes on the tip: $(nexp) (want 1), the edits stay: $([ -f $T/hm/t/.agi/nodes/deprecated/hypothesis/hf.md ]&&[ -f $T/hm/t/.agi/nodes/experiment/f1.md ]&&echo yes||echo NO), bracketed lines: $(grep -c '^\[' $T/egd2) (want 1) naming f1 and 'resolve nowhere': $(grep '^\[' $T/egd2|grep -c 'experiment:f1.*resolve nowhere') (want 1)" '[ $rgd2 = 6 ]&&[ $(tip) = $b0 ]&&[ "$(nexp)" = 1 ]&&[ -f $T/hm/t/.agi/nodes/deprecated/hypothesis/hf.md ]&&[ -f $T/hm/t/.agi/nodes/experiment/f1.md ]&&[ "$(grep -c "^\[" $T/egd2)" = 1 ]&&[ "$(grep "^\[" $T/egd2|grep -c "experiment:f1.*resolve nowhere")" = 1 ]'
# gd2b (control): a retired node ALREADY ON THE TIP still resolves as a parent: hypothesis:hr (on the tip under deprecated/) and a new child experiment:r1 in one agi-at: rc 0, ONE signed commit
mkgo;mkdir -p $T/g/.agi/nodes/deprecated/hypothesis;printf -- '---\nid: hypothesis:hr\nmint_id: 000000000000000000000000000000b5\ntype: hypothesis\nstatus: deprecated\nparents:\n  - goal:g1\n---\na retired parent, already on the tip\n' >$T/g/.agi/nodes/deprecated/hypothesis/hr.md;$G -C $T/g add -A;$G -C $T/g commit -qm "a retired hypothesis";$G -C $T/g update-ref refs/heads/posts/alive trunk;$G -C $T/hm/t checkout -q --detach posts/alive
gaf .agi/nodes/experiment/r1.md <<'XX'
---
id: experiment:r1
mint_id: 000000000000000000000000000000d8
type: experiment
parents:
  - hypothesis:hr
---
child of a retired parent already on the tip
XX
b0=$(tip);run agi-at .agi/nodes/experiment/r1.md 2>$T/egd2b;rgd2b=$?
ok "gd2b-agi-at-resolves-a-retired-parent-already-on-the-tip a NEW experiment parented by hypothesis:hr (under deprecated/ on the tip): rc $rgd2b (want 0), $($G -C $T/g rev-list --count $b0..posts/alive) new commit(s) (want 1), experiment nodes on the tip: $(nexp) (want 2), signed: [$(sig posts/alive)] (want G), bracketed lines: $(grep -c '^\[' $T/egd2b) (want 0)" '[ $rgd2b = 0 ]&&[ "$($G -C $T/g rev-list --count $b0..posts/alive)" = 1 ]&&[ "$(nexp)" = 2 ]&&[ "$(sig posts/alive)" = G ]&&[ "$(grep -c "^\[" $T/egd2b)" = 0 ]'
echo "agi-turn: $f FAIL"
exit $f
