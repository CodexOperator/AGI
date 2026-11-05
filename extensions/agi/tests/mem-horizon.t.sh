#!/bin/sh
# mem-horizon.t.sh [ROOT]: goal:g7.16.1.11.46.24 (V4) falsifier 1 + 2: the row's `mem:` cell is the memory HORIZON; a new horizon NESTS the old store (tip unchanged, still readable) and starts empty; each lane has its MUTANT read RED.
# sh + git + jq on a scratch HOME and a scratch engine repo; the REAL agi-mem piece through the claude-code adapter (the Stop-hook tap); no network, no root, 0 USD. ROOT = the tree whose engine-post.md carries the piece. exit = the FAIL count.
# Lanes: h1 a `goal` post taps under its owning goal's mint id; h2 a goal change nests the old store (tip unchanged, readable through `nest`) and the live branch starts empty; h3 the mutant that drops the old store; h4 a name taken gets .2 (an old nest is never overwritten); h5 `full` is horizon `-` and never resets; h6 `season`; h7 a store from before V4 is adopted, not nested; h8 `at` counts the session over the live branch and every nest; h9 an unknown horizon; h10 an owning goal with no node falls back to its id; n no pi adapter file is added.
# Honest limits: the horizon is read from the TRUNK's posts.md and goal node (as the gate already read the row), so a goal change shows at the next tap after the row lands; no director row carries `mem: goal` yet (the rows are the council's), so the live tap changes nothing until one does; the nest is a branch in the same 0700 store (a graph `nest:` container would put chunk ids into the graph), and the summary tree and bounded view are M9.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_MINT AGI_MEM_BATCH AGI_MEM_REF
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;for x in agi-mem agi-atom agi-notice;do sect $x engine-post.md>$D/bin/$x;done;chmod +x $D/bin/*;printf '#!/bin/sh\nexit 0\n'>$D/bin/agi-atomize;chmod +x $D/bin/agi-atomize
[ -s $D/bin/agi-mem ]||{ echo "FAIL inputs: no agi-mem piece";exit 99;}
E=$D/eng;mkdir -p $E/.agi/nodes/.geometry $E/.agi/nodes/goal;ln -s $R0/extensions $E/extensions
printf -- '---\nid: goal:g1.2\nmint_id: m1111\nstatus: active\n---\n# a\n'>$E/.agi/nodes/goal/g1.2.md;printf -- '---\nid: goal:g1.3\nmint_id: m2222\nstatus: active\n---\n# b\n'>$E/.agi/nodes/goal/g1.3.md
# rows: d (mem: goal), f (mem: full), s (mem: season); GO <goal-id> <trunk> rewrites the rows and commits (the tap reads the trunk = HEAD)
GO(){ printf -- '---\nid: config:posts\nparents:\n  - goal:g7\nposts:\n  - {"name": "d", "mem": "goal", "owning_goal": "%s", "engine": {"trunk": "%s"}}\n  - {"name": "f", "mem": "full", "owning_goal": "%s", "engine": {"trunk": "%s"}}\n  - {"name": "s", "mem": "season", "engine": {"trunk": "%s"}}\n---\n' "$1" "${2:-core/season3/main}" "$1" "${2:-core/season3/main}" "${2:-core/season3/main}">$E/.agi/nodes/.geometry/posts.md;(cd $E&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm "go $1 $2")>/dev/null 2>&1||(cd $E&&git init -q .&&git config core.hooksPath /dev/null&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x);}
GO goal:g1.2>/dev/null 2>&1
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-25T10:00:00Z","origin":{"kind":"human"},"message":{"content":%s}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
nh(){ H=$D/h$1;rm -rf "${H:?}";mkdir -p $H/.claude/projects/x;X=$H/.claude/projects/x/S1.jsonl;: >$X;echo S1>$H/.session;P=${2:-d};S=$H/.mem/$P.git;}
TAP(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=$P AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} tap 2>&1;}
AM(){ env HOME=$H AGI_POST=$P AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${MB:-$D/bin/agi-mem} "$@" 2>&1;}
nlive(){ git -C $S ls-tree -r --name-only refs/heads/mem -- mem 2>/dev/null|wc -l|tr -d ' ';}
MUT(){ sed "$1" $D/bin/agi-mem>$D/mut;cmp -s $D/bin/agi-mem $D/mut&&{ echo "FAIL inputs: mutant edit '$1' changed nothing";exit 99;};}

# ---- h1 a goal post taps under its owning goal's mint id
GO goal:g1.2;nh h1;UL u1 "first goal words">>$X;TAP>/dev/null;T1=$(git -C $S rev-parse refs/heads/mem);ID1=$(AM map|awk -F'	' '{print $1;exit}')
ok "h1-a-goal-post-taps-under-the-goals-mint-id the store keeps its horizon file = $(cat $S/horizon 2>/dev/null) (want m1111, goal:g1.2's mint id) and 1 chunk ($(nlive))" '[ "$(cat $S/horizon)" = m1111 ]&&[ "$(nlive)" = 1 ]&&[ -n "$ID1" ]'

# ---- h2 a goal change nests the old store (tip unchanged, still readable), the live branch starts empty
GO goal:g1.3;UL u2 "second goal words">>$X;TAP>/dev/null
ok "h2-a-goal-change-nests-the-old-store horizon file now $(cat $S/horizon) (m2222); refs/heads/nest/m1111 = the OLD tip ($(git -C $S rev-parse --short refs/heads/nest/m1111 2>&1)); the live branch holds only the new chunk ($(nlive))" '[ "$(cat $S/horizon)" = m2222 ]&&[ "$(git -C $S rev-parse refs/heads/nest/m1111)" = "$T1" ]&&[ "$(nlive)" = 1 ]&&! AM map|grep -q "^$ID1"'
ok "h2b-the-nest-is-still-readable nest ls lists it with its chunk count ($(AM nest ls)); nest m1111 map lists the old chunk, show prints its words, find finds them" 'AM nest ls|grep -q "^m1111	[0-9a-f]\{12\}	1$"&&AM nest m1111 map|grep -q "^$ID1"&&AM nest m1111 show $ID1|grep -q "first goal words"&&AM nest m1111 find "first goal"|grep -q "^$ID1"&&! AM nest m1111 show $ID1|grep -q "second goal"'
ok "h2c-the-new-horizon-starts-from-the-new-cursor the second tap did not re-sweep the old line: chunk count $(nlive) and the new chunk holds the second words" '[ "$(nlive)" = 1 ]&&AM map|awk -F"	" "{print \$1}"|while read -r c;do AM show $c;done|grep -q "second goal words"'
ok "h2d-nest-of-an-unknown-horizon-is-named nest nope map: '$(AM nest nope map)'" '[ "$(AM nest nope map)" = "nest: no horizon nope" ]'

# ---- h3 the mutant: a reset that drops the old store
MUT 's/{ \[ "\$nt" = "\$ot" \]||git -C \$S update-ref refs\/heads\/nest\/\$nn \$ot "";}&&//'
GO goal:g1.2;nh h3;UL u1 "first goal words">>$X;TAP $D/mut>/dev/null;GO goal:g1.3;UL u2 "second goal words">>$X;TAP $D/mut>/dev/null
ok "h3-mutant-a-reset-that-drops-the-old-store-RED a tap that resets without keeping the old branch leaves nest refs: $(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ') (the lane wants 1), and the first words are in no ref: $(git -C $S grep -l 'first goal' refs/heads/mem 2>/dev/null|wc -l|tr -d ' ') files" '[ "$(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d " ")" = 0 ]&&[ -z "$(git -C $S for-each-ref --format="%(refname)"|while read -r r;do git -C $S grep -l "first goal" $r;done)" ]'

# ---- h4 a name taken gets .2: an old nest is never overwritten
GO goal:g1.2;nh h4;UL u1 "words A1">>$X;TAP>/dev/null;GO goal:g1.3;UL u2 "words B1">>$X;TAP>/dev/null;TA=$(git -C $S rev-parse refs/heads/nest/m1111);TB=$(git -C $S rev-parse refs/heads/mem);GO goal:g1.2;UL u3 "words A2">>$X;TAP>/dev/null;GO goal:g1.3;UL u4 "words B2">>$X;TAP>/dev/null
ok "h4-a-taken-name-gets-a-suffix going m1111 -> m2222 -> m1111 -> m2222 keeps nest/m1111 at its first tip, nests m2222's store, and puts the second m1111 store at nest/m1111.2 (refs: $(git -C $S for-each-ref --format='%(refname:short)' refs/heads/nest|tr '\n' ' '))" '[ "$(git -C $S rev-parse refs/heads/nest/m1111)" = "$TA" ]&&[ "$(git -C $S rev-parse refs/heads/nest/m2222)" = "$TB" ]&&git -C $S rev-parse -q --verify refs/heads/nest/m1111.2 >/dev/null&&[ "$(git -C $S grep -l "words A2" refs/heads/nest/m1111.2|wc -l|tr -d " ")" = 1 ]'
MUT 's/while nt=\$(git -C \$S rev-parse -q --verify refs\/heads\/nest\/\$nn);do/while false;do/;s/update-ref refs\/heads\/nest\/\$nn \$ot "";/update-ref refs\/heads\/nest\/$nn $ot;/'
GO goal:g1.2;nh h4m;UL u1 "words A1">>$X;TAP $D/mut>/dev/null;GO goal:g1.3;UL u2 "words B1">>$X;TAP $D/mut>/dev/null;TA=$(git -C $S rev-parse refs/heads/nest/m1111);GO goal:g1.2;UL u3 "words A2">>$X;TAP $D/mut>/dev/null;GO goal:g1.3;UL u4 "words B2">>$X;TAP $D/mut>/dev/null
ok "h4m-mutant-a-taken-name-is-overwritten-RED a tap that reuses the name moves nest/m1111 off its first tip (now $(git -C $S rev-parse --short refs/heads/nest/m1111)): the lane wants it unchanged" '[ "$(git -C $S rev-parse refs/heads/nest/m1111)" != "$TA" ]'

# ---- h5 full is horizon `-`: an owning-goal change resets nothing
GO goal:g1.2;nh h5 f;UL u1 "full words 1">>$X;TAP>/dev/null;GO goal:g1.3;UL u2 "full words 2">>$X;TAP>/dev/null
ok "h5-full-never-resets a full post is horizon '$(cat $S/horizon)' (want -): its owning goal changing nests nothing ($(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ') nests) and both chunks stay on the live branch ($(nlive))" '[ "$(cat $S/horizon)" = - ]&&[ -z "$(git -C $S for-each-ref refs/heads/nest)" ]&&[ "$(nlive)" = 2 ]'
# ---- h6 season: the trunk's season segment
GO goal:g1.2 core/season3/main;nh h6 s;UL u1 "season words 3">>$X;TAP>/dev/null;GO goal:g1.2 core/season4/main;UL u2 "season words 4">>$X;TAP>/dev/null
ok "h6-season-horizon a season post is horizon season4 now ($(cat $S/horizon)); season3's store is nested (nest/season3: $(git -C $S ls-tree -r --name-only refs/heads/nest/season3 -- mem 2>/dev/null|wc -l|tr -d ' ') chunk) and the live branch holds the new one ($(nlive))" '[ "$(cat $S/horizon)" = season4 ]&&[ "$(git -C $S ls-tree -r --name-only refs/heads/nest/season3 -- mem|wc -l|tr -d " ")" = 1 ]&&[ "$(nlive)" = 1 ]'

# ---- h7 a store from before V4 (no horizon file) is adopted, not nested
GO goal:g1.2;nh h7;UL u1 "old words">>$X;TAP>/dev/null;rm -f $S/horizon;GO goal:g1.3;UL u2 "new words">>$X;TAP>/dev/null
ok "h7-a-pre-V4-store-is-adopted a store with chunks and no horizon file takes the current horizon ($(cat $S/horizon)) without nesting ($(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ') nests) and keeps both chunks ($(nlive))" '[ "$(cat $S/horizon)" = m2222 ]&&[ -z "$(git -C $S for-each-ref refs/heads/nest)" ]&&[ "$(nlive)" = 2 ]'

# ---- h8 at counts the session over the live branch and every nest
GO goal:g1.2;nh h8;UL u1 "words one">>$X;TAP>/dev/null;GO goal:g1.3;UL u2 "words two">>$X;TAP>/dev/null
ok "h8-at-counts-the-nest the session has 2 owner lines, one in the nest and one live: '$(AM at|head -1)' (want mem: tapped 2/2)" '[ "$(AM at|head -1)" = "mem: tapped 2/2" ]'
MUT 's/hg "\$(ar)"|awk/hg refs\/heads\/mem|awk/'
ok "h8m-mutant-at-reads-the-live-branch-only-RED an at that ignores the nests reads '$(MB=$D/mut AM at|head -1)': the lane wants 2/2, so this must be 1/2 RED" '[ "$(MB=$D/mut AM at|head -1)" = "mem: tapped 1/2 RED" ]'

# ---- h10 (V-2) the horizon FAILS CLOSED: a goal that cannot be read is not a change
mkdir -p $E/.agi/nodes/deprecated/goal
GO goal:g9.9 >/dev/null 2>&1;nh h10;UL u1 "orphan goal words">>$X;o=$(TAP)
ok "h10-a-fresh-store-with-an-unreadable-goal-taps-nothing no node for goal:g9.9 and no stored horizon: ONE warn line and no store content (got '$o'; chunks $(nlive); horizon file: $(cat $S/horizon 2>/dev/null))" '[ "$o" = "[mem] warn: horizon unread (goal goal:g9.9) (the turn goes on)" ]&&[ "$(nlive)" = 0 ]&&[ ! -s $S/horizon ]'
GO goal:g1.2 >/dev/null 2>&1;nh h11;UL u1 "first goal words">>$X;TAP>/dev/null
mv $E/.agi/nodes/goal/g1.2.md $E/.agi/nodes/deprecated/goal/g1.2.md;GO goal:g1.2 >/dev/null 2>&1;UL u2 "second words">>$X;o=$(TAP)
ok "h11-a-retired-owning-goal-keeps-its-horizon the goal node moved to deprecated/goal/ (same mint id): read there, horizon still $(cat $S/horizon), no nest ($(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ')), no warn (got '$o'), both chunks live ($(nlive))" '[ "$(cat $S/horizon)" = m1111 ]&&[ -z "$(git -C $S for-each-ref refs/heads/nest)" ]&&[ -z "$o" ]&&[ "$(nlive)" = 2 ]'
git -C $E rm -q -f .agi/nodes/deprecated/goal/g1.2.md;GO goal:g1.2 >/dev/null 2>&1;UL u3 "third words">>$X;o=$(TAP)
ok "h12-a-goal-that-reads-nowhere-keeps-the-stored-horizon the node is gone from goal/ and deprecated/: ONE warn line, the stored horizon m1111 is kept ($(cat $S/horizon)), nothing nests ($(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ')) and the third chunk still taps under it ($(nlive)); got '$o'" '[ "$o" = "[mem] warn: horizon unread (goal goal:g1.2) (the turn goes on)" ]&&[ "$(cat $S/horizon)" = m1111 ]&&[ -z "$(git -C $S for-each-ref refs/heads/nest)" ]&&[ "$(nlive)" = 3 ]'
MUT 's/\[ "$hu" \]&&H=$(cat $S\/horizon 2>\/dev\/null);//';UL u4 "fourth words">>$X;TAP $D/mut>/dev/null
ok "h12m-mutant-a-missed-read-counts-as-a-change-RED the old fallback (the goal id as the horizon) reads the missed goal as a NEW horizon and nests the store (nests: $(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d ' ')): the lane wants 0, so this must be 1" '[ "$(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d " ")" = 1 ]'
printf -- '---\nid: goal:g1.2\nmint_id: m1111\nstatus: active\n---\n# a\n'>$E/.agi/nodes/goal/g1.2.md;GO goal:g1.2 >/dev/null 2>&1

# ---- h13 (V-1) the drop is a CAS: a sweep between the read and the drop loses nothing
RGIT=$(command -v git);mkdir $D/gw;cat >$D/gw/git<<EOF
#!/bin/sh
$RGIT "\$@";rc=\$?
case "\$*" in *"update-ref refs/heads/nest/"*)if [ -f $D/adv ];then rm -f $D/adv;t=\$($RGIT -C \$2 rev-parse refs/heads/mem);c=\$($RGIT -C \$2 -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit-tree \$($RGIT -C \$2 rev-parse \$t^{tree}) -p \$t -m adv);$RGIT -C \$2 update-ref refs/heads/mem \$c;fi;;esac
exit \$rc
EOF
chmod +x $D/gw/git
TAPG(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=$P AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/gw:$D/bin:$PATH sh ${1:-$D/bin/agi-mem} tap 2>&1;}
GO goal:g1.2 >/dev/null 2>&1;nh h13;UL u1 "first goal words">>$X;TAP>/dev/null;T1=$(git -C $S rev-parse refs/heads/mem);GO goal:g1.3 >/dev/null 2>&1;touch $D/adv;o=$(TAPG);T2=$(git -C $S rev-parse refs/heads/mem 2>/dev/null)
ok "h13-a-sweep-between-the-read-and-the-drop-is-kept the other writer's commit advanced mem after the nest was cut: the drop is refused ('$o'), mem is KEPT at the advanced tip (${T2:-gone}, was ${T1}), nest/m1111 is the first tip, the horizon file still says $(cat $S/horizon)" 'echo "$o"|grep -q "^\[mem\] warn: store .* horizon m1111 not nested"&&[ -n "$T2" ]&&[ "$T2" != "$T1" ]&&[ "$(git -C $S rev-parse refs/heads/nest/m1111)" = "$T1" ]&&[ "$(cat $S/horizon)" = m1111 ]'
UL u2 "second goal words">>$X;TAP>/dev/null
ok "h13b-the-retry-advances-the-same-nest the next tap moves nest/m1111 to the advanced tip (a descendant of the first, no .2: nests $(git -C $S for-each-ref --format='%(refname:short)' refs/heads/nest|tr '\n' ' ')), nothing is lost, and the live branch starts from the second chunk ($(nlive))" '[ "$(git -C $S rev-parse refs/heads/nest/m1111)" = "$T2" ]&&[ "$(git -C $S for-each-ref refs/heads/nest|wc -l|tr -d " ")" = 1 ]&&[ "$(cat $S/horizon)" = m2222 ]&&[ "$(nlive)" = 1 ]'
MUT 's/update-ref -d refs\/heads\/mem $ot/update-ref -d refs\/heads\/mem/'
GO goal:g1.2 >/dev/null 2>&1;nh h13m;UL u1 "first goal words">>$X;TAP $D/mut>/dev/null;GO goal:g1.3 >/dev/null 2>&1;touch $D/adv;TAPG $D/mut>/dev/null;AV=$(git -C $S for-each-ref --format='%(refname)'|while read -r r;do git -C $S log --format=%s $r;done|grep -c '^adv$')
ok "h13m-mutant-an-unconditional-drop-loses-the-sweep-RED a drop that is not a CAS deletes mem with the other writer's commit on it: that commit is in $AV refs (the lane wants it kept in 1, so this must be 0)" '[ "$AV" = 0 ]'

# ---- n falsifier 2: no pi adapter file is ADDED by this leaf (V4_BASE=<rev> names the base; none = the merge-base with core/season3/main; an unreadable base is a FAIL, never a pass)
pa(){ grep -iE '(^|/)(pi[-_.]|optchat|uniichat)' ;}
B=${V4_BASE:-$(git -C $R0 merge-base HEAD core/season3/main 2>/dev/null)}
AD=$(git -C $R0 diff --name-only --diff-filter=A $B HEAD 2>/dev/null)&&[ -n "$B" ]&&AOK=1||AOK=0
ok "n1-no-pi-adapter-file-added the files this tip ADDS over its base ($(echo "$B"|cut -c1-10)) include $(echo "$AD"|pa|wc -l|tr -d ' ') named like a pi / optchat / uniichat adapter (want 0; base readable: $AOK)" '[ $AOK = 1 ]&&[ "$(echo "$AD"|pa|wc -l|tr -d " ")" = 0 ]'
ok "n1m-mutant-a-pi-adapter-file-RED the same name test reads a planted extensions/agi/bin/adapters/pi-optchat.ts as a hit ($(echo extensions/agi/bin/adapters/pi-optchat.ts|pa|wc -l|tr -d ' ')): the lane wants 0 on the added files, so this must be 1" '[ "$(echo extensions/agi/bin/adapters/pi-optchat.ts|pa|wc -l|tr -d " ")" = 1 ]'
echo "mem-horizon: $f FAIL";exit $f
