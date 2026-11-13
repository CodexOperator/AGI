#!/bin/sh
# zero-commit.t.sh [ROOT]: goal:g7.16.1.11.46.30 falsifier 1 (zero manual commits: the post wrapper commits every changed path and grows the grid at turn end, failing loud). The Stop hook's agi-turn, run on a fixture ~/t with NO command typed: a ~/t edit lands on posts/P signed + CAS and each changed node gets its per-node grid version (the REAL grid.py split of ROOT); a commit that fails reads ONE [uncommitted] line PER PATH in the next prompt (~/.notice), the edit kept on disk, after exactly 2 attempts, and the next turn end commits it; the rc 5 guard names git when git cannot start or a redirect cannot be made (sp's BUILD TERM 16:30:33Z 11-06); agi-sync's and the detach's rc count; every agi-turn label reaches agi-notice; rc never 2; the v5 out passes agi-captive under the wrapper commit (RE-CUT 5). Every row that can carries a mutant that must read RED.
# sh + git + ssh-keygen + python3 on SCRATCH repos (a fixture trunk, posts/alive, a DETACHED ~/t worktree, a throwaway key and ring), HOME = a stub; no network, no root, 0 USD. Pieces come from `sect` of ROOT's .geometry/engine*.md, never ~/bin; mutants are sed edits of those extracted bytes.
# Honest limits: the unwritable reflog is REPRODUCED (chmod a-w on the fixture's logs/refs/heads/posts/alive; measured: git refuses the update, rc 128, the tip unmoved), not the lab NAS's EPERM itself; a CAS miss is a racer in a git shim; 'git unable to start' = a PATH with every /usr/bin and /bin entry but git; the live Stop hook (claude calling agi-turn) is not run.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};T=$(mktemp -d);trap 'chmod -R u+w $T 2>/dev/null;rm -rf "${T:?}"' 0;f=0;G=/usr/bin/git
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
unset GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL GIT_COMMITTER_NAME GIT_COMMITTER_EMAIL GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_POST AGI_WT RUNTIME_DIRECTORY AGI_TRUNK AGI_GRID
export HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
mkdir -p $T/hm $T/bin $T/shim $T/run $T/k $T/gs $T/ss $T/nogit
ssh-keygen -q -t ed25519 -N '' -f $T/k/alive -C alive >/dev/null||{ echo "FAIL fixture: ssh-keygen";exit 99;}
echo "alive@agi namespaces=\"git\" $(cut -d' ' -f1,2 $T/k/alive.pub)" >$T/allowed
for n in agi-turn agi-at agi-notice agi-sync grow.py agi-pray agi-captive agi-flush;do sect $n >$T/bin/$n;[ -s $T/bin/$n ]||{ echo "FAIL extract: $n";exit 99;};chmod +x $T/bin/$n;done
# the git shim: logs every update-ref of posts/alive ($T/ur.log, the commit attempts), a racer that moves the tip first ($T/race), a failing checkout ($T/faildetach)
cat >$T/shim/git<<XX
#!/bin/sh
if [ "\$1" = update-ref ]&&[ "\$2" = refs/heads/posts/alive ];then echo x>>$T/ur.log
 [ -e $T/race ]&&{ t=\$($G -C $T/g rev-parse posts/alive);n=\$(echo racer|$G -C $T/g commit-tree -p \$t \$t^{tree});$G -C $T/g update-ref refs/heads/posts/alive \$n;};fi
[ "\$1" = checkout ]&&[ -e $T/faildetach ]&&{ echo "fatal: simulated checkout failure" >&2;exit 128;}
case " \$* " in *" rev-parse -q --verify refs/heads/posts/alive "*)[ -e $T/warnrp ]&&echo "warning: simulated rev-parse warning" >&2;; *" diff --no-renames --name-only HEAD "*)[ -e $T/warn ]&&echo "warning: simulated listing warning" >&2;;esac
exec $G "\$@"
XX
chmod +x $T/shim/git
printf '#!/bin/sh\necho "[growth-order] doc:a: refused by the fixture checker"\nexit 1\n' >$T/gs/grow.py;printf '#!/bin/sh\nexit 3\n' >$T/ss/agi-sync;chmod +x $T/gs/grow.py $T/ss/agi-sync
for x in /usr/bin/* /bin/*;do b=${x##*/};[ "$b" = git ]||[ -e $T/nogit/$b ]||ln -s $x $T/nogit/$b;done
MA=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;MK=cccccccccccccccccccccccccccccccc;MB=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb;NA=.agi/nodes/doc/a.md;NK=.agi/nodes/doc/card-alive.md;NB=.agi/nodes/doc/card-belam.md
mk(){ chmod -R u+w $T/g 2>/dev/null;rm -rf $T/g $T/hm/t $T/hm/.notice* $T/hm/.grid-base $T/race $T/faildetach $T/ur.log;$G init -q -b trunk $T/g;g="$G -C $T/g";$g config user.name alive;$g config user.email alive@agi;$g config gpg.format ssh;$g config user.signingkey $T/k/alive;$g config commit.gpgsign true
 mkdir -p $T/g/.agi/nodes/doc;echo '{}' >$T/g/.agi/config.json;printf '.agi/sessions/*\n' >$T/g/.gitignore
 printf -- '---\nid: doc:a\nmint_id: %s\ntype: doc\nparents: []\n---\nbody a\n' $MA >$T/g/$NA;printf -- '---\nid: doc:card-alive\nmint_id: %s\ntype: doc\nparents: []\n---\ncard\n' $MK >$T/g/$NK;printf -- '---\nid: doc:card-belam\nmint_id: %s\ntype: doc\nparents: []\n---\ncard\n' $MB >$T/g/$NB;echo readme >$T/g/README.md;echo notes >$T/g/NOTES.md
 $g add -A;$g commit -qm trunk;$g branch posts/alive trunk;$g worktree add -q --detach $T/hm/t posts/alive;B0=$($g rev-parse posts/alive);}
GRID="python3 $R0/extensions/agi/bin/grid.py"
# run [PIECE-DIR] CMD..: the hook's world, env -i; BIN (default $T/bin) is where the pieces come from; XP = extra PATH dirs first
run(){ (cd $T/hm/t&&env -i PATH=${XP:+$XP:}$T/shim:${BIN:-$T/bin}:/usr/bin:/bin HOME=$T/hm GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_GRID="${AGI_GRID_X:-$GRID}" "$@");}
tip(){ $G -C $T/g rev-parse posts/alive;}
sig(){ $G -C $T/g -c gpg.ssh.allowedSignersFile=$T/allowed log -1 --format=%G? $1;}
nl_(){ if [ -f $T/hm/.notice ];then grep -c "$1" $T/hm/.notice;else echo 0;fi;}
att(){ [ -f $T/ur.log ]&&wc -l <$T/ur.log|tr -d ' '||echo 0;}
mut(){ d=$T/m-$1;mkdir -p $d;cp $T/bin/* $d/;}
RCS=
# ---- z1 a ~/t edit (a node + a non-node file) lands at the turn end, no command typed; each changed node gets its grid version
mk;echo "edit z1" >>$T/hm/t/$NA;echo "edit z1" >>$T/hm/t/README.md;run agi-turn >$T/o1 2>$T/e1;r1=$?;RCS="$RCS $r1"
gv=$($G -C $T/g rev-parse -q --verify refs/grid/node/$MA 2>/dev/null);gb=$($G -C $T/g cat-file -p "$gv:node.md" 2>/dev/null|grep -c 'edit z1')
ok "z1-a-t-edit-lands-at-the-turn-end-and-the-grid-grows agi-turn rc $r1 (want 0), stderr [$(head -c 200 $T/e1)] (want empty); ONE new commit: $($G -C $T/g rev-list --count $B0..posts/alive) (want 1), parent = the old tip: $([ "$($G -C $T/g rev-parse posts/alive^)" = $B0 ]&&echo yes||echo NO), %G? [$(sig posts/alive)] (want G), both paths on the tip: $($G -C $T/g show posts/alive:$NA|grep -c 'edit z1')/$($G -C $T/g show posts/alive:README.md|grep -c 'edit z1') (want 1/1); grid ref of doc:a holds the edit: ${gb:-0} (want 1), its commit names the land: $($G -C $T/g log -1 --format=%B $gv 2>/dev/null|grep -c "^Split-Land: $(tip)") (want 1); ~/t clean: [$($G -C $T/hm/t status -s)] (want empty), ~/.notice lines: $(cat $T/hm/.notice 2>/dev/null|wc -l|tr -d ' ') (want 0)" '[ $r1 = 0 ]&&[ ! -s $T/e1 ]&&[ "$($G -C $T/g rev-list --count $B0..posts/alive)" = 1 ]&&[ "$($G -C $T/g rev-parse posts/alive^)" = $B0 ]&&[ "$(sig posts/alive)" = G ]&&[ "$($G -C $T/g show posts/alive:$NA|grep -c "edit z1")" = 1 ]&&[ "${gb:-0}" = 1 ]&&[ "$($G -C $T/g log -1 --format=%B $gv|grep -c "^Split-Land: $(tip)")" = 1 ]&&[ -z "$($G -C $T/hm/t status -s)" ]&&[ ! -s $T/hm/.notice ]'
# ---- z2 control: a clean turn prints no line
run agi-turn >$T/o2 2>$T/e2;r2=$?;RCS="$RCS $r2"
ok "z2-control-a-clean-turn-prints-no-line rc $r2 (want 0), stderr bytes $(wc -c <$T/e2|tr -d ' ') (want 0), ~/.notice lines $(cat $T/hm/.notice 2>/dev/null|wc -l|tr -d ' ') (want 0), the tip unchanged: $([ "$(tip)" = "$($G -C $T/hm/t rev-parse HEAD)" ]&&echo yes||echo NO)" '[ $r2 = 0 ]&&[ ! -s $T/e2 ]&&[ ! -s $T/hm/.notice ]'
# ---- z3 an unwritable reflog: ONE line naming the path, the edit on disk, exactly 2 attempts; the next turn end commits it once the reflog is writable; mutant: 0 retries
mk;echo "edit z3" >>$T/hm/t/README.md;chmod a-w $T/g/.git/logs/refs/heads/posts/alive;run agi-turn >/dev/null 2>$T/e3;r3=$?;RCS="$RCS $r3";a3=$(att)
ok "z3-an-unwritable-reflog-is-one-line-naming-the-path agi-turn rc $r3 (want != 0 and != 2), commit attempts $a3 (want 2: one in-turn retry), ~/.notice [$(cat $T/hm/.notice 2>/dev/null|cut -c1-220)] (want ONE [uncommitted] README.md line carrying git's own 'unable to append'), the tip unchanged: $([ "$(tip)" = $B0 ]&&echo yes||echo NO), the edit on disk: $(grep -c 'edit z3' $T/hm/t/README.md) (want 1)" '[ $r3 != 0 ]&&[ $r3 != 2 ]&&[ $a3 = 2 ]&&[ "$(cat $T/hm/.notice|wc -l|tr -d " ")" = 1 ]&&[ "$(nl_ "^\[uncommitted\] README.md: .*\[ref\].*unable to append")" = 1 ]&&[ "$(tip)" = $B0 ]&&[ "$(grep -c "edit z3" $T/hm/t/README.md)" = 1 ]'
chmod u+w $T/g/.git/logs/refs/heads/posts/alive;rm -f $T/ur.log;run agi-turn >/dev/null 2>$T/e3b;r3b=$?;RCS="$RCS $r3b"
ok "z3b-the-next-turn-end-commits-it-once-the-reflog-is-writable rc $r3b (want 0), new commits $($G -C $T/g rev-list --count $B0..posts/alive) (want 1), the edit on the tip: $($G -C $T/g show posts/alive:README.md|grep -c 'edit z3') (want 1), attempts $(att) (want 1)" '[ $r3b = 0 ]&&[ "$($G -C $T/g rev-list --count $B0..posts/alive)" = 1 ]&&[ "$($G -C $T/g show posts/alive:README.md|grep -c "edit z3")" = 1 ]&&[ "$(att)" = 1 ]'
mut retry;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();i=s.index("A||{ echo \"$l\"|while");j=s.index(";;1)",i);open(p,"w").write(s[:i]+"A||U x"+s[j:])' $T/m-retry/agi-turn
mk;echo "edit z3" >>$T/hm/t/README.md;chmod a-w $T/g/.git/logs/refs/heads/posts/alive;BIN=$T/m-retry run agi-turn >/dev/null 2>&1;m3=$(att)
ok "m3-zero-retries-reads-RED the mutant (no in-turn retry; the edit hit: $(grep -c '0)A||U x;;1)' $T/m-retry/agi-turn)) made $m3 attempt(s) (want 1 != 2: RED)" '[ "$(grep -c "0)A||U x;;1)" $T/m-retry/agi-turn)" = 1 ]&&[ $m3 = 1 ]'
# ---- z4 two NON-node paths uncommitted in one turn read TWO lines, each naming its path; mutant: the old KEY (label + hex only)
mk;echo "edit z4" >>$T/hm/t/README.md;echo "edit z4" >>$T/hm/t/NOTES.md;chmod a-w $T/g/.git/logs/refs/heads/posts/alive;run agi-turn >/dev/null 2>&1;r4=$?;RCS="$RCS $r4"
ok "z4-two-uncommitted-paths-read-two-lines rc $r4 (want != 0), [uncommitted] lines: README.md $(nl_ '^\[uncommitted\] README.md:') NOTES.md $(nl_ '^\[uncommitted\] NOTES.md:') (want 1 1), all lines $(cat $T/hm/.notice|wc -l|tr -d ' ') (want 2)" '[ $r4 != 0 ]&&[ "$(nl_ "^\[uncommitted\] README.md:")" = 1 ]&&[ "$(nl_ "^\[uncommitted\] NOTES.md:")" = 1 ]&&[ "$(cat $T/hm/.notice|wc -l|tr -d " ")" = 2 ]'
run agi-turn >/dev/null 2>&1;ok "z4b-a-stuck-path-stays-ONE-line-per-path the same failure a 2nd turn: lines $(cat $T/hm/.notice|wc -l|tr -d ' ') (want 2: deduped by the KEY, not one per turn)" '[ "$(cat $T/hm/.notice|wc -l|tr -d " ")" = 2 ]'
mut key;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="if(a[i]~/^\\[/)r=r a[i] \" \" a[i+1] \" \";else if(length(a[i])>6&&a[i]~/^[0-9a-f]+$/)r=r a[i] \" \";return r}";assert s.count(o)==1;open(p,"w").write(s.replace(o,"if(a[i]~/^\\[/||(length(a[i])>6&&a[i]~/^[0-9a-f]+$/))r=r a[i];return r}"))' $T/m-key/agi-notice
mk;echo "edit z4" >>$T/hm/t/README.md;echo "edit z4" >>$T/hm/t/NOTES.md;chmod a-w $T/g/.git/logs/refs/heads/posts/alive;BIN=$T/m-key run agi-turn >/dev/null 2>&1
ok "m4-the-old-KEY-reads-RED with today's KEY (label + 7+ hex words) the two paths read $(cat $T/hm/.notice|wc -l|tr -d ' ') line(s) (want 1: one path dropped, RED)" '[ "$(cat $T/hm/.notice|wc -l|tr -d " ")" = 1 ]'
chmod u+w $T/g/.git/logs/refs/heads/posts/alive
# ---- z5 the rc 5 guard: git unable to start, and a redirect that cannot be made, each name git or pass; never [no-branch]; mutant: the old guard (sp's BUILD TERM: RED on both)
mut guard;python3 -I -c 'import sys;p=sys.argv[1];L=open(p).read().split("\n");i=[k for k,l in enumerate(L) if l.startswith("{ [ \"$P\" ]&&[ \"$AGI_ROLE\" != kid ];}||{ echo \"[no-branch]")];assert len(i)==1;L[i[0]]="{ [ \"$P\" ]&&[ \"$AGI_ROLE\" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo \"[no-branch] $P: a kid, or no posts/$P: nothing committed\">&2;exit 5;}";open(p,"w").write("\n".join(L))' $T/m-guard/agi-turn
mk;(cd $T/hm/t&&env -i PATH=$T/bin:$T/nogit HOME=$T/hm AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_GRID=: agi-turn) >/dev/null 2>$T/e5;r5=$?;RCS="$RCS $r5"
ok "z5-git-unable-to-start-names-git rc $r5 (want != 0, != 2, != 5), stderr [$(head -c 200 $T/e5)] (want a [git] line carrying 'git: not found', never [no-branch]), ~/.notice [git] lines $(nl_ '^\[git\] alive: .*not found') (want 1)" '[ $r5 != 0 ]&&[ $r5 != 2 ]&&[ $r5 != 5 ]&&grep -q "^\[git\] alive: .*not found" $T/e5&&! grep -q "no-branch" $T/e5&&[ "$(nl_ "^\[git\] alive: .*not found")" = 1 ]'
mk;(cd $T/hm/t&&env -i PATH=$T/m-guard:$T/nogit HOME=$T/hm AGI_POST=alive RUNTIME_DIRECTORY=$T/run AGI_WT=$T/wt AGI_GRID=: agi-turn) >/dev/null 2>$T/m5;rm5=$?
ok "m5a-the-old-guard-says-no-branch-when-git-cannot-start (RED) the old guard (sed hit: $(grep -c 'verify $b>/dev/null' $T/m-guard/agi-turn)): rc $rm5, [no-branch] $(grep -c '^\[no-branch\]' $T/m5) (want rc 5 and 1: RED)" '[ "$(grep -c "verify \$b>/dev/null" $T/m-guard/agi-turn)" = 1 ]&&[ $rm5 = 5 ]&&[ "$(grep -c "^\[no-branch\]" $T/m5)" = 1 ]'
for v in bin m-guard;do mut rd-$v;cp $T/$v/agi-turn $T/m-rd-$v/agi-turn;sed -i '/^{ \[ "\$P" \]&&/s|/dev/null|'$T'/no/such/dir/null|g' $T/m-rd-$v/agi-turn;done
mk;echo "edit z5" >>$T/hm/t/README.md;BIN=$T/m-rd-bin run agi-turn >/dev/null 2>$T/e5r;r5r=$?;RCS="$RCS $r5r"
ok "z5b-a-redirect-that-cannot-be-made-does-not-read-no-branch the guard line with every /dev/null pointed at a missing dir (redirects the edit hit in the NEW guard: $(grep '^{ \[ "\$P" \]&&' $T/bin/agi-turn|grep -o /dev/null|wc -l|tr -d ' '), want 0: there is none to fail; in the OLD guard: $(grep '^{ \[ "\$P" \]&&' $T/m-guard/agi-turn|grep -o /dev/null|wc -l|tr -d ' ')): rc $r5r (want 0: the guard has no redirect to fail), [no-branch] $(grep -c 'no-branch' $T/e5r) (want 0), the edit landed: $($G -C $T/g show posts/alive:README.md|grep -c 'edit z5') (want 1)" '[ $r5r = 0 ]&&! grep -q no-branch $T/e5r&&[ "$($G -C $T/g show posts/alive:README.md|grep -c "edit z5")" = 1 ]'
mk;echo "edit z5" >>$T/hm/t/README.md;BIN=$T/m-rd-m-guard run agi-turn >/dev/null 2>$T/m5r;rm5r=$?
ok "m5b-the-old-guard-says-no-branch-on-an-unwritable-redirect (RED): rc $rm5r, [no-branch] $(grep -c '^\[no-branch\]' $T/m5r), stderr [$(head -c 160 $T/m5r)] (want rc 5 and 1: RED, posts/alive exists)" '[ $rm5r = 5 ]&&[ "$(grep -c "^\[no-branch\]" $T/m5r)" = 1 ]'
# ---- z6 a CAS miss on both attempts: the line names the path and the race
mk;echo "edit z6" >>$T/hm/t/README.md;: >$T/race;run agi-turn >/dev/null 2>$T/e6;r6=$?;RCS="$RCS $r6";rm -f $T/race
ok "z6-a-CAS-miss-gives-the-line rc $r6 (want != 0, != 2), attempts $(att) (want 2), ~/.notice [$(cut -c1-160 $T/hm/.notice 2>/dev/null)] (want [uncommitted] README.md carrying [raced]), the edit on disk: $(grep -c 'edit z6' $T/hm/t/README.md) (want 1), the tip is the racer's: $($G -C $T/g log -1 --format=%s posts/alive) (want racer)" '[ $r6 != 0 ]&&[ $r6 != 2 ]&&[ "$(att)" = 2 ]&&[ "$(nl_ "^\[uncommitted\] README.md: .*\[raced\]")" = 1 ]&&[ "$(grep -c "edit z6" $T/hm/t/README.md)" = 1 ]'
# ---- z7 a grow.py refusal gives the line, carrying grow.py's own label
mk;echo "edit z7" >>$T/hm/t/$NA;XP=$T/gs run agi-turn >/dev/null 2>$T/e7;r7=$?;RCS="$RCS $r7"
ok "z7-a-grow-refusal-gives-the-line rc $r7 (want != 0, != 2), ~/.notice [$(cut -c1-200 $T/hm/.notice 2>/dev/null)] (want [uncommitted] $NA carrying [growth-order]), the tip unchanged: $([ "$(tip)" = $B0 ]&&echo yes||echo NO), the edit on disk: $(grep -c 'edit z7' $T/hm/t/$NA) (want 1)" '[ $r7 != 0 ]&&[ $r7 != 2 ]&&[ "$(nl_ "^\[uncommitted\] .agi/nodes/doc/a.md: .*\[growth-order\]")" = 1 ]&&[ "$(tip)" = $B0 ]&&[ "$(grep -c "edit z7" $T/hm/t/$NA)" = 1 ]'
# ---- z8 a failed agi-sync and a failed detach: each a line and a non-zero rc; mutants: their rc uncounted
mut sync;sed -i 's/^agi-sync||{ N "\[sync\] \$P: agi-sync rc \$?";k=1;};/agi-sync;/' $T/m-sync/agi-turn
mut det;sed -i 's/\[ \$j != 0 \]||{ e=\$(git checkout -q --detach \$b 2>&1)||{ N "\[detach\] \$P: \$(echo "\$e"|tr .\\n. . .)";k=1;};};/[ $j != 0 ]||git checkout -q --detach $b;/' $T/m-det/agi-turn;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();i=s.index("j=0;e=$(git checkout");j=s.index(";j=2;};",i)+len(";j=2;};");open(p,"w").write(s[:i]+"j=0;git checkout -q --detach $b;"+s[j:])' $T/m-det/agi-turn
mk;XP=$T/ss run agi-turn >/dev/null 2>$T/e8;r8=$?;RCS="$RCS $r8";n8=$(nl_ '^\[sync\] alive: agi-sync rc 3')
mk;XP=$T/ss BIN=$T/m-sync run agi-turn >/dev/null 2>&1;m8=$?
ok "z8-a-failed-agi-sync-is-a-line-and-a-non-zero-rc rc $r8 (want != 0, != 2), [sync] lines in ~/.notice $n8 (want 1); m8 the mutant (rc uncounted, sed hit $(grep -c '^agi-sync;' $T/m-sync/agi-turn)) rc $m8 (want 0: RED)" '[ $r8 != 0 ]&&[ $r8 != 2 ]&&[ "$n8" = 1 ]&&[ "$(grep -c "^agi-sync;" $T/m-sync/agi-turn)" = 1 ]&&[ $m8 = 0 ]'
mk;: >$T/faildetach;run agi-turn >/dev/null 2>$T/e8d;r8d=$?;RCS="$RCS $r8d";n8d=$(nl_ '^\[detach\] alive: .*fatal: simulated checkout failure')
mk;: >$T/faildetach;BIN=$T/m-det run agi-turn >/dev/null 2>&1;m8d=$?;rm -f $T/faildetach
ok "z8b-a-failed-detach-is-a-line-and-a-non-zero-rc rc $r8d (want != 0, != 2), [detach] lines $n8d (want 1); m8b the mutant (sed hit $(grep -c '||git checkout -q --detach $b;' $T/m-det/agi-turn)) rc $m8d (want 0: RED)" '[ $r8d != 0 ]&&[ $r8d != 2 ]&&[ "$n8d" = 1 ]&&[ "$(grep -c "||git checkout -q --detach \$b;" $T/m-det/agi-turn)" = 1 ]&&[ $m8d = 0 ]'
# ---- z9 every label agi-turn writes goes through agi-notice: no bracketed label is echoed to stderr alone (grow.py's own output is echoed AND its [growth] notice added; [no-branch], the guard's rc 5 for a kid or a post with no branch, is not a failure of target 3 (iii) and is said on stderr only, as before: classed, not counted); mutant: one label back on stderr only
lb(){ grep -o 'echo "\[[a-z-]*\]' $1|grep -vc 'no-branch';}
mut lab;sed -i 's/N "\[raced\] \$m"/echo "[raced] $m">\&2/' $T/m-lab/agi-turn
ok "z9-every-label-goes-through-agi-notice labels echoed to stderr alone in agi-turn: $(lb $T/bin/agi-turn) (want 0); N (stderr + agi-notice add) calls: $(grep -o 'N "\[' $T/bin/agi-turn|wc -l|tr -d ' ') (want >= 12), the [growth] notice: $(grep -c 'agi-notice add "\[growth\]' $T/bin/agi-turn) (want 1); m9 one label on stderr only: $(lb $T/m-lab/agi-turn) (want 1: RED)" '[ "$(lb $T/bin/agi-turn)" = 0 ]&&[ "$(grep -o "N \"\[" $T/bin/agi-turn|wc -l)" -ge 12 ]&&[ "$(grep -c "agi-notice add \"\[growth\]" $T/bin/agi-turn)" = 1 ]&&[ "$(lb $T/m-lab/agi-turn)" = 1 ]'
# ---- z12 a STRANDED HEAD (commits on no ref) and a ~/t edit: the strand is never abandoned (agi-at's reset would move HEAD off it), nothing from ~/t is committed, each path is a line; mutant: the ~/t commit before the strand check -> the strand is lost (RED)
st(){ mk;(cd $T/hm/t&&$G -c user.name=alive -c user.email=alive@agi -c commit.gpgsign=false commit -q --no-verify --allow-empty -m stranded);SH=$($G -C $T/hm/t rev-parse HEAD);echo "edit z12" >>$T/hm/t/README.md;}
st;run agi-turn >/dev/null 2>$T/e12;r12=$?;RCS="$RCS $r12";h12=$($G -C $T/hm/t rev-parse HEAD);n12=$(nl_ '^\[uncommitted\] README.md: kept on disk: HEAD is stranded');s12=$(nl_ '^\[strand-refused\]');t12=$(tip);b12=$B0;s12h=$SH;d12=$(grep -c 'edit z12' $T/hm/t/README.md)
mut ord;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="if agi-turn strand;then j=0;";assert s.count(o)==1;open(p,"w").write(s.replace(o,"agi-at $(git diff --no-renames --name-only HEAD) 2>/dev/null;if agi-turn strand;then j=0;"))' $T/m-ord/agi-turn
st;BIN=$T/m-ord run agi-turn >/dev/null 2>&1;hm=$($G -C $T/hm/t rev-parse HEAD)
ok "z12-a-stranded-HEAD-is-never-abandoned rc $r12 (want != 0, != 2), HEAD still the stranded commit: $([ "$h12" = "$s12h" ]&&echo yes||echo NO), [strand-refused] $s12 (want 1), [uncommitted] README.md naming the strand $n12 (want 1), the tip unchanged: $([ "$t12" = $b12 ]&&echo yes||echo NO), the edit on disk: $d12 (want 1); m12 the commit before the check: HEAD on the strand $([ "$hm" = "$SH" ]&&echo yes||echo no) (want no: RED)" '[ $r12 != 0 ]&&[ $r12 != 2 ]&&[ "$h12" = "$s12h" ]&&[ "$s12" = 1 ]&&[ "$n12" = 1 ]&&[ "$t12" = $b12 ]&&[ "$d12" = 1 ]&&[ "$hm" != "$SH" ]'
# ---- z13 (SM Q1, alive (4)/(a), sp (7)) the trunk post RUNS as AGI_POST=belam (its branch posts/belam IS the trunk): its turn end commits its OWN card alone and never splits; every other ~/t path is ONE [trunk-post] line; mutants: no exclusion -> README on the trunk (RED); no card exception -> the card left (RED)
bm(){ mk;$G -C $T/g branch posts/belam trunk;(cd $T/hm/t&&$G checkout -q --detach posts/belam);echo "edit z13" >>$T/hm/t/README.md;echo "card z13" >>$T/hm/t/$NB;}
btip(){ $G -C $T/g rev-parse posts/belam;}
bm;run env AGI_POST=belam agi-turn >/dev/null 2>$T/e13;r13=$?;RCS="$RCS $r13";b13=$B0;c13=$($G -C $T/g rev-list --count $b13..posts/belam);k13=$($G -C $T/g show posts/belam:$NB|grep -c 'card z13');q13=$($G -C $T/g show posts/belam:README.md|grep -c 'edit z13');n13=$(nl_ '^\[trunk-post\] belam: posts/belam is the trunk: only its card is committed here, 1 other path(s) left: README.md');g13=$(nl_ '^\[grid\]');a13=$($G -C $T/g rev-parse posts/alive)
mut tp;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="[ $b != refs/heads/posts/belam ]||tp=1;";assert s.count(o)==1;open(p,"w").write(s.replace(o,""))' $T/m-tp/agi-turn
bm;BIN=$T/m-tp run env AGI_POST=belam agi-turn >/dev/null 2>&1;m13=$($G -C $T/g show posts/belam:README.md|grep -c 'edit z13')
mut tc;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="l=$(echo \"$l\"|grep -xF \"$c\");}";assert s.count(o)==1;open(p,"w").write(s.replace(o,"l=;}"))' $T/m-tc/agi-turn
bm;BIN=$T/m-tc run env AGI_POST=belam agi-turn >/dev/null 2>&1;mc13=$($G -C $T/g show posts/belam:$NB|grep -c 'card z13')
ok "z13-the-trunk-post-commits-its-card-alone AGI_POST=belam: rc $r13 (want 0), ONE commit on posts/belam: $c13 (want 1), its card on the tip: $k13 (want 1), README on the tip: $q13 (want 0), [trunk-post] lines $n13 (want 1), [grid] $g13 (want 0), posts/alive untouched: $([ "$a13" = $b13 ]&&echo yes||echo NO), no AGI_TRUNK arm left: $(grep -c AGI_TRUNK $T/bin/agi-turn) (want 0); m13 no exclusion: README on the trunk $m13 (want 1: RED); mc13 no card exception: the card on the tip $mc13 (want 0: RED)" '[ $r13 = 0 ]&&[ "$c13" = 1 ]&&[ "$k13" = 1 ]&&[ "$q13" = 0 ]&&[ "$n13" = 1 ]&&[ "$g13" = 0 ]&&[ "$a13" = $b13 ]&&[ "$(grep -c AGI_TRUNK $T/bin/agi-turn)" = 0 ]&&[ "$m13" = 1 ]&&[ "$mc13" = 0 ]'
# ---- z14 (SM N1) a git warning on the listing's stderr is never a path: the edit lands; mutant: the listing's stderr into l -> [stage] (RED)
mk;echo "edit z14" >>$T/hm/t/README.md;: >$T/warn;run agi-turn >/dev/null 2>$T/e14;r14=$?;RCS="$RCS $r14";l14=$($G -C $T/g show posts/alive:README.md|grep -c 'edit z14');o14=$(cat $T/hm/.notice 2>/dev/null)
mut wn;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="ls-files -o --exclude-standard;} 2>$x.e)";assert s.count(o)==1;open(p,"w").write(s.replace(o,"ls-files -o --exclude-standard;} 2>&1)"))' $T/m-wn/agi-turn
mk;echo "edit z14" >>$T/hm/t/README.md;: >$T/warn;BIN=$T/m-wn run agi-turn >/dev/null 2>&1;m14=$(nl_ '^\[uncommitted\] warning: simulated listing warning');rm -f $T/warn
ok "z14-a-listing-warning-is-never-a-path rc $r14 (want 0), the edit landed $l14 (want 1), ~/.notice [$o14] (want empty); m14 stderr into l: an [uncommitted] line naming git's warning as a path: $m14 (want 1: RED)" '[ $r14 = 0 ]&&[ "$l14" = 1 ]&&[ -z "$o14" ]&&[ "$m14" = 1 ]'
# ---- z15 (SM N2) a refused path never blocks its siblings: a NEW node (grow.py refuses it: no spawn_gate.py in this ~/t) beside a README edit -> README lands, the node is ONE line; mutant: attempt 2 over all paths again -> README blocked (RED)
mk;printf -- '---\nid: doc:n15\nmint_id: dddddddddddddddddddddddddddddddd\ntype: doc\nparents:\n  - doc:a\n---\nnew\n' >$T/hm/t/.agi/nodes/doc/n15.md;echo "edit z15" >>$T/hm/t/README.md;run agi-turn >/dev/null 2>$T/e15;r15=$?;RCS="$RCS $r15"
l15=$($G -C $T/g show posts/alive:README.md|grep -c 'edit z15');q15=$($G -C $T/g cat-file -e posts/alive:.agi/nodes/doc/n15.md 2>/dev/null&&echo yes||echo no);n15=$(nl_ '^\[uncommitted\] .agi/nodes/doc/n15.md: ');o15=$(cat $T/hm/.notice 2>/dev/null|wc -l|tr -d ' ')
mut pp;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();i=s.index("A||{ echo \"$l\"|while");j=s.index(";;1)",i);open(p,"w").write(s[:i]+"A||A||U x"+s[j:])' $T/m-pp/agi-turn
mk;printf -- '---\nid: doc:n15\nmint_id: dddddddddddddddddddddddddddddddd\ntype: doc\nparents:\n  - doc:a\n---\nnew\n' >$T/hm/t/.agi/nodes/doc/n15.md;echo "edit z15" >>$T/hm/t/README.md;BIN=$T/m-pp run agi-turn >/dev/null 2>&1;m15=$($G -C $T/g show posts/alive:README.md|grep -c 'edit z15')
ok "z15-a-refused-path-never-blocks-its-siblings rc $r15 (want != 0, != 2), README landed $l15 (want 1), the new node on the tip: $q15 (want no), its [uncommitted] line $n15 (want 1), ~/.notice lines $o15 (want 1); m15 attempt 2 over all paths: README landed $m15 (want 0: RED)" '[ $r15 != 0 ]&&[ $r15 != 2 ]&&[ "$l15" = 1 ]&&[ $q15 = no ]&&[ "$n15" = 1 ]&&[ "$o15" = 1 ]&&[ "$m15" = 0 ]'
# ---- z11 the v5 out end to end under the wrapper commit (RE-CUT 5): card edit, a reply ending on a prayer, its turn end commits the card, the next reply's out call passes agi-captive; control: the same out with no prayer is refused; mutant: the old commit clock refuses it (RED)
JES='Господи Іисусе Христе, Сыне Божїй, помилуй мѧ грѣшнаго.';NOW=$(date +%s);W=$((NOW-100))
tr_(){ o=$1;t0=$2;shift 2;: >$o;i=0;for x in "$@";do python3 -I -c 'import json,sys,datetime;print(json.dumps({"type":"assistant","timestamp":datetime.datetime.fromtimestamp(int(sys.argv[2]),datetime.timezone.utc).isoformat().replace("+00:00","Z"),"message":{"role":"assistant","content":[{"type":"text","text":sys.argv[1]}] if sys.argv[1]!="-" else [{"type":"tool_use","name":"Bash","input":{}}]}}))' "$x" $((t0+i)) >>$o;i=$((i+1));done;}
pray(){ python3 -I -c 'import json,sys;print(json.dumps({"session_id":sys.argv[1],"transcript_path":sys.argv[2],"cwd":sys.argv[3],"tool_input":{"command":"touch ~/.fresh; kill $"+"PPID"}}))' $2 $3 $T/hm/t|(cd $T/hm/t&&env -i HOME=$T/hm PATH=$T/shim:/usr/bin:/bin AGI_POST=alive $1 captive) >/dev/null 2>$T/ep;}
mk;mkdir -p $T/hm/.prayed;: >$T/hm/.prayed/o1;: >$T/hm/.prayed/o2;: >$T/hm/.prayed/o3;echo "gen N+1: where it stops" >>$T/hm/t/$NK;touch -d @$W $T/hm/t/$NK
tr_ $T/tp $((W+5)) "card written. $JES" '-';tr_ $T/tn $((W+5)) "card written. $JES" "rotating now" '-'
run agi-turn >/dev/null 2>$T/e11;r11=$?;RCS="$RCS $r11";ct=$($G -C $T/g log -1 --format=%ct posts/alive -- $NK)
pray $T/bin/agi-pray o1 $T/tp;p1=$?;pray $T/bin/agi-pray o2 $T/tn;p2=$?
mut clk;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="try:k=os.path.getmtime(os.path.join(j.get(\"cwd\") or os.path.expanduser(\"~/t\"),\".agi/nodes/doc/card-%s.md\"%post))";assert s.count(o)==1;open(p,"w").write(s.replace(o,"try:k=int(subprocess.run([\"git\",\"log\",\"-1\",\"--format=%ct\",\"--\",\".agi/nodes/doc/card-%s.md\"%post],capture_output=True,text=True,cwd=j.get(\"cwd\") or os.path.expanduser(\"~/t\"),timeout=10).stdout.strip())"))' $T/m-clk/agi-pray;pray $T/m-clk/agi-pray o3 $T/tp;p3=$?
ok "z11-the-v5-out-passes-under-the-wrapper-commit the turn end committed the card: rc $r11 (want 0), its commit time $ct > the prayer's $((W+5)): $([ "${ct:-0}" -gt $((W+5)) ]&&echo yes||echo NO); the out call with the prayer as the newest text since the card's write: agi-pray captive rc $p1 (want 0); control, a later text with no prayer: rc $p2 (want 2); m11 the old commit clock: rc $p3 (want 2: RED)" '[ $r11 = 0 ]&&[ "${ct:-0}" -gt $((W+5)) ]&&[ $p1 = 0 ]&&[ $p2 = 2 ]&&[ $p3 = 2 ]'
# ---- z16 (alive (1)) a git mv in ~/t commits BOTH sides: the old path gone at the tip; mutant: the listing without --no-renames -> the old path stays (RED)
mk;(cd $T/hm/t&&$G mv README.md README2.md);run agi-turn >/dev/null 2>$T/e16;r16=$?;RCS="$RCS $r16";a16=$($G -C $T/g cat-file -e posts/alive:README.md 2>/dev/null&&echo yes||echo no);b16=$($G -C $T/g cat-file -e posts/alive:README2.md 2>/dev/null&&echo yes||echo no)
mut mv;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="diff --no-renames --name-only HEAD";assert s.count(o)==1;open(p,"w").write(s.replace(o,"diff --name-only HEAD"))' $T/m-mv/agi-turn
mk;(cd $T/hm/t&&$G mv README.md README2.md);BIN=$T/m-mv run agi-turn >/dev/null 2>&1;m16=$($G -C $T/g cat-file -e posts/alive:README.md 2>/dev/null&&echo yes||echo no)
ok "z16-a-git-mv-commits-both-sides rc $r16 (want 0), the old path on the tip: $a16 (want no), the new: $b16 (want yes); m16 rename-detecting listing: the old path still on the tip: $m16 (want yes: RED)" '[ $r16 = 0 ]&&[ $a16 = no ]&&[ $b16 = yes ]&&[ $m16 = yes ]'
# ---- z17 (all-is-one (3)) a node TREE edit and a ~/t edit in ONE turn: ~/t ends on the tip's bytes and the NEXT turn end commits nothing (no silent revert of the tree edit); mutant: r1's order (no detach before the listing) -> turn 2 commits the old bytes (RED)
tr17(){ mk;mkdir -p $T/wt/x/.agi/nodes/doc;echo .agi/nodes/doc/a.md >$T/wt/x/.p;cp $T/g/$NA $T/wt/x/$NA;echo "tree edit z17" >>$T/wt/x/$NA;echo "edit z17" >>$T/hm/t/README.md;}
tr17;run agi-turn >/dev/null 2>$T/e17;r17=$?;RCS="$RCS $r17";c17=$($G -C $T/g rev-list --count $B0..posts/alive);s17=$($G -C $T/hm/t status -s);run agi-turn >/dev/null 2>&1;d17=$($G -C $T/g rev-list --count $B0..posts/alive);e17=$($G -C $T/g show posts/alive:$NA|grep -c 'tree edit z17')
mut ord3;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();i=s.index("j=0;e=$(git checkout");j=s.index(";j=2;};",i)+len(";j=2;};");open(p,"w").write(s[:i]+"j=0;"+s[j:])' $T/m-ord3/agi-turn
tr17;BIN=$T/m-ord3 run agi-turn >/dev/null 2>&1;BIN=$T/m-ord3 run agi-turn >/dev/null 2>&1;m17=$($G -C $T/g show posts/alive:$NA|grep -c 'tree edit z17')
ok "z17-a-tree-edit-and-a-t-edit-in-one-turn-never-revert rc $r17 (want 0), commits after turn 1: $c17 (want 2: the tree's + ~/t's), ~/t status after it: [$s17] (want empty: ~/t on the tip's bytes), after turn 2: $d17 (want 2: nothing more), the tree edit on the tip: $e17 (want 1); m17 r1's order: the tree edit on the tip after turn 2: $m17 (want 0: reverted, RED)" '[ $r17 = 0 ]&&[ "$c17" = 2 ]&&[ -z "$s17" ]&&[ "$d17" = 2 ]&&[ "$e17" = 1 ]&&[ "$m17" = 0 ]'
# ---- z18 (self-perpetuating (2)) a card edited in its node TREE: the turn end checks it out over ~/t after the praying reply, so the out is refused once (refused-and-taught: the meter's line and agi-rotate step 1 say ~/t)
mk;mkdir -p $T/wt/c/.agi/nodes/doc $T/hm/.prayed;: >$T/hm/.prayed/o4;echo $NK >$T/wt/c/.p;cp $T/g/$NK $T/wt/c/$NK;echo "tree card z18" >>$T/wt/c/$NK;tr_ $T/tq $(($(date +%s)-50)) "card written in its tree. $JES" '-'
run agi-turn >/dev/null 2>$T/e18;r18=$?;RCS="$RCS $r18";pray $T/bin/agi-pray o4 $T/tq;p18=$?
mt=$(sect agi-meter|grep -c 'write your card WHOLE in ~/t (never its node tree');rs=$(grep -c 'in ~/t at .agi/nodes/doc/card-<post>.md (Write AND Edit both refuse the quorum link .agi/sessions/quorum/<post>.md, which resolves there), NEVER its agi-wt node tree' $R0/skills/agi-rotate/SKILL.md)
ok "z18-a-tree-card-is-refused-once-and-taught rc $r18 (want 0), the tree card on the tip: $($G -C $T/g show posts/alive:$NK|grep -c 'tree card z18') (want 1), the out after the praying reply: agi-pray rc $p18 (want 2: refused once, fails closed); agi-meter's line names ~/t: $mt (want 1), agi-rotate step 1 names ~/t: $rs (want 1)" '[ $r18 = 0 ]&&[ "$($G -C $T/g show posts/alive:$NK|grep -c "tree card z18")" = 1 ]&&[ $p18 = 2 ]&&[ "$mt" = 1 ]&&[ "$rs" = 1 ]'
# ---- z19 (all-is-one's g NOTE) a git warning on the guard's read is never the grid split's base: the edit lands and the grid grows, no [grid] line; mutant: g keeps the warning -> [grid] (RED)
mk;echo "edit z19" >>$T/hm/t/$NA;: >$T/warnrp;run agi-turn >/dev/null 2>$T/e19;r19=$?;RCS="$RCS $r19";g19=$(nl_ '^\[grid\]');v19=$($G -C $T/g rev-parse -q --verify refs/grid/node/$MA >/dev/null&&echo yes||echo no)
mut gw;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o=";exit 1;};g=$h";assert s.count(o)==1;open(p,"w").write(s.replace(o,";exit 1;}"))' $T/m-gw/agi-turn
mk;echo "edit z19" >>$T/hm/t/$NA;: >$T/warnrp;BIN=$T/m-gw run agi-turn >/dev/null 2>&1;m19=$(nl_ '^\[grid\]');rm -f $T/warnrp
ok "z19-a-guard-warning-is-never-the-split-base rc $r19 (want 0), [grid] lines $g19 (want 0), the grid grew: $v19 (want yes), the guard's g = the sha line only in all three pieces: $(grep -c ';g=$h' $T/bin/agi-turn)/$(sect agi-at|grep -c ';g=$h')/$(sect agi-flush|grep -c ';g=$h') (want 1/1/1); m19 g keeps the warning: [grid] $m19 (want 1: RED)" '[ $r19 = 0 ]&&[ "$g19" = 0 ]&&[ $v19 = yes ]&&[ "$(grep -c ";g=\$h" $T/bin/agi-turn)" = 1 ]&&[ "$(sect agi-at|grep -c ";g=\$h")" = 1 ]&&[ "$(sect agi-flush|grep -c ";g=\$h")" = 1 ]&&[ "$m19" = 1 ]'
# ---- goal:g7.16.1.11.46.31: a grid-lock miss is not a failed turn. The lock is held by a stand-in writer: AGI_GRID = $T/glk, which logs each call ($T/gl.log = the lock waits), waits W s and fails as the real split does on a held lock; agi-flush (the out's ExecStopPost) runs on it
W=3;printf '#!/bin/sh\necho x>>%s/gl.log;sleep %s;echo "grid: split could not acquire the grid lock (held by a stand-in writer) within %ss";exit 1\n' $T $W $W >$T/glk;chmod +x $T/glk
gw(){ [ -f $T/gl.log ]&&wc -l <$T/gl.log|tr -d ' '||echo 0;}
fl(){ rm -f $T/gl.log;s0=$(date +%s%N);AGI_GRID_X=$T/glk run agi-flush >/dev/null 2>$T/ef;fr=$?;ms=$((($(date +%s%N)-s0)/1000000));}
nz(){ printf -- '---\nid: doc:n%s\nmint_id: eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee%s\ntype: doc\nparents:\n  - doc:a\n---\nnew\n' $1 $2 >$T/hm/t/.agi/nodes/doc/n$1.md;}
# z20c (belam 09:5xZ 11-13, sp) a split that exits 0 but prints 'rewind-skip' (L562) reaches the post: ONE [grid] line naming it, rc 0, ~/.grid-base dropped (the split DID run); control: a clean rc 0 split prints none; mu20c today's agi-turn (success branch = rm -f only) prints none (RED)
printf '#!/bin/sh\necho "  rewind-skip eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee .agi/nodes/doc/a.md (its blob is an older version)"\necho "split: 1 changed node(s); 0 written, clean"\nexit 0\n' >$T/rsk;chmod +x $T/rsk
mk;echo "edit z20c" >>$T/hm/t/$NA;AGI_GRID_X=$T/rsk run agi-turn >/dev/null 2>$T/e21;rc20c=$?;RCS="$RCS $rc20c";gl20c=$(nl_ '^\[grid\] alive: 1 node(s) rewind-skipped');bs20c=$([ -e $T/hm/.grid-base ]&&echo yes||echo no)
mk;echo "edit z20cc" >>$T/hm/t/$NA;run agi-turn >/dev/null 2>&1;cn20c=$(nl_ 'rewind-skipped')
mut gr;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="&&{ rm -f $s;w=";assert s.count(o)==1;i=s.index(o);j=s.index("}||{",i);open(p,"w").write(s[:i]+"&&rm -f $s"+s[j+1:])' $T/m-gr/agi-turn
mk;echo "edit mu20c" >>$T/hm/t/$NA;AGI_GRID_X=$T/rsk BIN=$T/m-gr run agi-turn >/dev/null 2>&1;mu20c=$(nl_ 'rewind-skipped')
ok "z20c-a-rewind-skip-on-rc-0-reaches-the-post rc $rc20c (want 0), [grid] rewind-skipped lines $gl20c (want 1), the base dropped: $bs20c (want no); control, a clean split: $cn20c (want 0); mu20c today's success branch: $mu20c (want 0: RED)" '[ $rc20c = 0 ]&&[ "$gl20c" = 1 ]&&[ $bs20c = no ]&&[ "$cn20c" = 0 ]&&[ "$mu20c" = 0 ]'
# z20 the grid miss ALONE: agi-flush finishes inside ONE wait (one call, under 2 x W), ONE [grid] line, ~/.grid-base kept; z20b the next agi-turn with the lock free grows it and drops the base; m20 today's k=1 in the grid branch = 4 waits (RED)
mk;echo "edit z20" >>$T/hm/t/$NA;echo "edit z20" >>$T/hm/t/README.md;fl;r20=$fr;RCS="$RCS $r20";w20=$(gw);t20=$ms;g20=$(nl_ '^\[grid\] alive: ');k20=$([ -s $T/hm/.grid-base ]&&echo yes||echo no);l20=$($G -C $T/g show posts/alive:README.md|grep -c 'edit z20')
run agi-turn >/dev/null 2>$T/e20b;r20b=$?;RCS="$RCS $r20b";gv=$($G -C $T/g rev-parse -q --verify refs/grid/node/$MA 2>/dev/null);v20=$($G -C $T/g cat-file -p "$gv:node.md" 2>/dev/null|grep -c 'edit z20');b20=$([ -e $T/hm/.grid-base ]&&echo yes||echo no)
mut gk;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="not grown: $(echo \"$o\"|tail -2|tr '"'"'\\n'"'"' '"'"' '"'"'|cut -c1-240)\";};";assert s.count(o)==1;open(p,"w").write(s.replace(o,o[:-2]+"k=1;};"))' $T/m-gk/agi-turn
mk;echo "edit m20" >>$T/hm/t/$NA;BIN=$T/m-gk fl;m20=$(gw);mr20=$fr
ok "z20-a-grid-miss-alone-is-not-a-failed-turn agi-flush with the lock held: rc $r20 (want 0), lock waits $w20 (want 1), ${t20} ms (want < $((2*W*1000))), [grid] lines $g20 (want 1), ~/.grid-base kept: $k20 (want yes), the edit landed: $l20 (want 1); z20b the next agi-turn, lock free: rc $r20b (want 0), doc:a's grid version holds the edit: $v20 (want 1), the base left: $b20 (want no); m20 today's k=1 in the grid branch (sed hit: $(grep -c 'not grown: .*";k=1;};' $T/m-gk/agi-turn)): lock waits $m20, rc $mr20 (want 4 and != 0: RED)" '[ $r20 = 0 ]&&[ "$w20" = 1 ]&&[ $t20 -lt $((2*W*1000)) ]&&[ "$g20" = 1 ]&&[ $k20 = yes ]&&[ "$l20" = 1 ]&&[ $r20b = 0 ]&&[ "$v20" = 1 ]&&[ $b20 = no ]&&[ "$(grep -c "not grown: .*\";k=1;};" $T/m-gk/agi-turn)" = 1 ]&&[ "$m20" = 4 ]&&[ $mr20 != 0 ]'
# z21 COMBINED, the lock held AND a ~/t path left (a NEW node grow.py refuses, z15's, beside a README edit that lands and moves the tip): non-zero, agi-flush re-runs the turn (4 waits); mutants: the grid branch clears k (m21a), the exit zeroes k on a grid miss (m21b): rc 0 after one wait (RED)
mk;nz 21 1;echo "edit z21" >>$T/hm/t/README.md;fl;r21=$fr;RCS="$RCS $r21";w21=$(gw);n21=$(nl_ '^\[uncommitted\] .agi/nodes/doc/n21.md: ');g21=$(nl_ '^\[grid\] alive: ')
mut gz;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read();o="not grown: $(echo \"$o\"|tail -2|tr '"'"'\\n'"'"' '"'"' '"'"'|cut -c1-240)\";};";assert s.count(o)==1;open(p,"w").write(s.replace(o,o[:-2]+"k=0;};"))' $T/m-gz/agi-turn
mut gx;python3 -I -c 'import sys;p=sys.argv[1];s=open(p).read().rstrip("\n");assert s.endswith("exit $k");open(p,"w").write(s[:-7]+"[ -s ~/.grid-base ]&&k=0;exit $k\n")' $T/m-gx/agi-turn
mk;nz 21 1;echo "edit m21a" >>$T/hm/t/README.md;BIN=$T/m-gz fl;ma21=$fr;wa21=$(gw)
mk;nz 21 1;echo "edit m21b" >>$T/hm/t/README.md;BIN=$T/m-gx fl;mb21=$fr;wb21=$(gw)
ok "z21-the-lock-held-and-a-path-left-still-re-runs agi-flush: rc $r21 (want != 0, != 2), lock waits $w21 (want 4: every re-run), [uncommitted] n21 $n21 (want 1), [grid] $g21 (want 1); m21a the grid branch clears k: rc $ma21, waits $wa21 (want 0 and 1: RED); m21b the exit zeroes k on a grid miss: rc $mb21, waits $wb21 (want 0 and 1: RED)" '[ $r21 != 0 ]&&[ $r21 != 2 ]&&[ "$w21" = 4 ]&&[ "$n21" = 1 ]&&[ "$g21" = 1 ]&&[ $ma21 = 0 ]&&[ "$wa21" = 1 ]&&[ $mb21 = 0 ]&&[ "$wb21" = 1 ]'
# z22 COMBINED, the lock held AND a commit fault (z6's racer: a CAS miss on both attempts, the racer moving the tip): non-zero, re-run, each turn still 2 attempts; m22 the exit zeroes k: rc 0 (RED)
mk;echo "edit z22" >>$T/hm/t/README.md;: >$T/race;fl;r22=$fr;RCS="$RCS $r22";w22=$(gw);a22=$(att);n22=$(nl_ '^\[uncommitted\] README.md: .*\[raced\]');rm -f $T/race
mk;echo "edit m22" >>$T/hm/t/README.md;: >$T/race;BIN=$T/m-gx fl;m22=$fr;rm -f $T/race
ok "z22-the-lock-held-and-a-commit-fault-still-re-runs agi-flush: rc $r22 (want != 0, != 2), lock waits $w22 (want 4), commit attempts $a22 (want 8: 2 per turn x 4), [uncommitted] README.md [raced] $n22 (want 1); m22 the exit zeroes k: rc $m22 (want 0: RED)" '[ $r22 != 0 ]&&[ $r22 != 2 ]&&[ "$w22" = 4 ]&&[ "$a22" = 8 ]&&[ "$n22" = 1 ]&&[ $m22 = 0 ]'
# n2 falsifier 2: the grid-miss branch sets no failure: lines of agi-turn carrying both 'not grown' and 'k=1'; control (the same grep on L418's line, today's k=1, written back as m-gk): 1 (RED)
ok "n2-the-grid-miss-branch-sets-no-failure agi-turn lines with 'not grown' and 'k=1': $(grep 'not grown' $T/bin/agi-turn|grep -c 'k=1') (want 0); control, L418's line (m-gk): $(grep 'not grown' $T/m-gk/agi-turn|grep -c 'k=1') (want 1: RED)" '[ "$(grep "not grown" $T/bin/agi-turn|grep -c "k=1")" = 0 ]&&[ "$(grep "not grown" $T/m-gk/agi-turn|grep -c "k=1")" = 1 ]'
# ---- z10 the wrapper's rc is never 2 (every agi-turn rc above)
n2=0;for r in $RCS;do [ $r = 2 ]&&n2=$((n2+1));done
ok "z10-the-wrapper-never-exits-2 rcs [$RCS] (want no 2), 2s: $n2" '[ $n2 = 0 ]&&[ -n "$RCS" ]'
# ---- n1 falsifier 2 (negative): over skills/, CLAUDE.md, QUICKSTART.md and the role docs (extensions/agi/briefs) no line teaches a post a hand commit: agi-at appears on 0 lines; every other hit of `grid.py commit --all` / `git commit` is CLASSED below by file + a fragment of its own line (maintainer = MAIN / the Prime's merge; gate = a master's trunk commit; lane = a gate tip; never = a line that forbids one; read = an unreferenced stack; history = a trap's incident); an unclassed hit reads RED; mutant: one teaching line added -> RED
CL=$T/classes;cat >$CL<<'XX'
CLAUDE.md	MAIN (maintainer): `git commit` · 	maintainer
CLAUDE.md	MAIN (maintainer): `grid.py commit --all` (G6.3)	maintainer
CLAUDE.md	| MAIN (maintainer) only: version every changed node	maintainer
extensions/agi/briefs/prime-director-successor.md	`grid.py commit --all` ONLY on `season2/main`	maintainer
skills/agi-corrective/SKILL.md	# MAIN (maintainer): a real commit before dispatch	maintainer
skills/agi-master-gate/SKILL.md	signing a commit: spell the flags apart	gate
skills/agi-master-gate/SKILL.md	a director's grid.py commit --all in ITS worktree	history
skills/agi-master-gate/SKILL.md	a hand `git commit-tree` without -S	gate
skills/agi-merge-pass/SKILL.md	ff local-maxxing/main to TIP · grid.py commit --all	maintainer
skills/agi-merge-pass/SKILL.md	`grid.py commit --all` in prime-root	maintainer
skills/agi-node-write/SKILL.md	MAIN (maintainer): edit, then `git commit -- <path>`	maintainer
skills/agi-post/SKILL.md	no hand `git commit`	never
skills/agi-review/SKILL.md	-m stack` (unreferenced)	read
skills/agi-rotate/SKILL.md	a plain `git commit` is refused	never
skills/agi-verify/SKILL.md	a cherry-pick in a lane worktree	lane
skills/agi-verify/SKILL.md	`grid.py commit --all` (MAIN, maintainer	maintainer
skills/agi/SKILL.md	| `bin/grid.py commit --all [--prefix P]` | MAIN (maintainer	maintainer
skills/agi/SKILL.md	runs only on master after a merge (MAIN, maintainer	maintainer
skills/agi/SKILL.md	MAIN (maintainer) by exact path, `git commit -- <path>`	maintainer
skills/agi/SKILL.md	**do not commit**	never
skills/agi/SKILL.md	MAIN (maintainer): one commit `iter-N	maintainer
skills/agi/SKILL.md	git commit                              # the thought and the code, together	maintainer
skills/agi/SKILL.md	grid.py commit --all                    # the graph records your edit as vN+1	maintainer
skills/agi/SKILL.md	**`grid.py commit --all` stays (MAIN, maintainer)	maintainer
skills/agi/SKILL.md	**After every iteration commit (MAIN, maintainer	maintainer
XX
hits(){ (cd $1&&grep -rnE 'agi-at\b|grid\.py commit --all|git commit' skills CLAUDE.md QUICKSTART.md extensions/agi/briefs 2>/dev/null);}
uncl(){ hits $1|python3 -I -c 'import sys
C=[l.rstrip("\n").split("\t") for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
for h in sys.stdin:
    f,_,t=h.rstrip("\n").split(":",2)
    if not any(f==c[0] and c[1] in t for c in C):print(h.strip()[:160])' $CL;}
na=$(hits $R0|grep -c 'agi-at\b');nh=$(hits $R0|wc -l|tr -d ' ');nu=$(uncl $R0|wc -l|tr -d ' ')
mkdir -p $T/dt;for d in skills extensions/agi/briefs;do mkdir -p $T/dt/$d;cp -r $R0/$d/. $T/dt/$d/;done;cp $R0/CLAUDE.md $T/dt/;cp $R0/QUICKSTART.md $T/dt/ 2>/dev/null;echo '- commit the card with `agi-at <card>`' >>$T/dt/skills/agi-rotate/SKILL.md;mu=$(uncl $T/dt|wc -l|tr -d ' ')
ok "n1-no-doc-teaches-a-post-a-hand-commit agi-at lines $na (want 0); hits $nh, unclassed $nu (want 0) [$(uncl $R0|head -2|tr '\n' '|')]; table rows $(grep -c . $CL); mn1 one teaching line added: unclassed $mu (want 1: RED)" '[ $na = 0 ]&&[ $nh -ge 1 ]&&[ $nu = 0 ]&&[ $mu = 1 ]'
echo "zero-commit: $f FAIL";[ $f = 0 ]
