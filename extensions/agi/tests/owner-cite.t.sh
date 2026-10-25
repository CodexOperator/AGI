#!/bin/sh
# owner-cite.t.sh [ROOT]: goal:g7.16.1.11.46.26 (M10) falsifier 1 + 2: every `## OWNER` block written after the leaf lands cites the chunk id(s) of the owner's words in the M6 store; each lane has its MUTANT (an input that must read RED, and a piece edit the lane must notice).
# sh + git + jq + awk on a scratch HOME, a scratch engine tree and a scratch store; the REAL agi-mem piece (verb `cite`); no network, no root, 0 USD. ROOT = the tree whose engine-post.md carries the piece. exit = the FAIL count.
# Lanes: g* the grandfather list (a committed file of node ids, never a pattern; the REAL list covers the REAL tree: real-file-first); c* the check (a cited valid owner chunk passes; none, an absent id, a post chunk, a malformed id each read RED by name; a fenced heading or a fenced id is no block / no citation; a block ends at the next ## heading); u* unread (no list, a bad list line, no store while a block cites) prints `unread`, rc 1, never 0; p* it runs on a post with no `mem: full` row.
# Honest limits: the check proves the id is a live OWNER chunk of the store the caller can read, not that the block's words are that chunk's words (the verbatim match is not built); the store is 0700 under the facing post's uid, so a post that cannot read it gets `unread` for a block that cites; a grandfathered node may still gain a new OWNER block (the list is node ids, as the leaf says).
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'chmod -R u+w "${D:?}" 2>/dev/null;rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_MINT AGI_MEM_BATCH AGI_ATOM_COMMIT
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;for x in agi-mem agi-atom agi-notice;do sect $x engine-post.md>$D/bin/$x;done;chmod +x $D/bin/*
for x in agi-mem agi-atom agi-notice;do [ -s $D/bin/$x ]||{ echo "FAIL inputs: no $x piece";exit 99;};done
E=$D/eng;mkdir -p $E/.agi/nodes/.geometry $E/.agi/nodes/goal;ln -s $R0/extensions $E/extensions
printf -- '---\nid: config:posts\nparents:\n  - goal:g7\nposts:\n  - {"name": "p", "mem": "full", "faces": "owner"}\n---\n'>$E/.agi/nodes/.geometry/posts.md
printf -- 'credits_live: false\n'>$E/.agi/nodes/.geometry/secrets.md
(cd $E&&git init -q .&&git config core.hooksPath /dev/null&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x)
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"%s","origin":{"kind":"human"},"message":{"content":%s}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
AL(){ printf '{"type":"assistant","uuid":"%s","timestamp":"%s","message":{"content":[{"type":"text","text":%s}]}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
EV(){ env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_T=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH "$@";}
MUT(){ sed "$1" $D/bin/$2>$D/mut_$2;cmp -s $D/bin/$2 $D/mut_$2&&{ echo "FAIL inputs: mutant edit '$1' changed nothing in $2";exit 99;};}
# a store with ONE owner chunk and ONE post chunk, planted by the real tap (the label/derive/walk a real tap ends with are shimmed away: this lane reads the store, not the labels)
mkdir $D/tb;printf '#!/bin/sh\ncase $1 in label|walk) exit 0;; esac\nexec sh %s/bin/agi-mem "$@"\n' $D>$D/tb/agi-mem;printf '#!/bin/sh\ncase $1 in derive) exit 0;; esac\nexec sh %s/bin/agi-atom "$@"\n' $D>$D/tb/agi-atom;chmod +x $D/tb/*
H=$D/h;mkdir -p $H/.claude/projects/x;X=$H/.claude/projects/x/S1.jsonl;echo S1>$H/.session;S=$H/.mem/p.git
{ UL o1 "ship the widget by friday" 2026-10-25T10:00:00.000Z;AL p1 "Opened atom a1 for it" 2026-10-25T10:00:05.000Z;}>$X
echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_T=$E AGI_TRUNK=HEAD PATH=$D/tb:$D/bin:$PATH sh $D/bin/agi-mem tap >/dev/null 2>&1
OC=$(EV sh $D/bin/agi-mem map|awk -F'	' '$2=="owner"{print $1;exit}');PC=$(EV sh $D/bin/agi-mem map|awk -F'	' '$2=="post"{print $1;exit}')
[ -n "$OC" ]&&[ -n "$PC" ]||{ echo "FAIL inputs: the planted store has no owner ($OC) or post ($PC) chunk";exit 99;}
GF=$E/.agi/nodes/.geometry/owner-cite-grandfather.txt;NG=$E/.agi/nodes/goal
# nn <name> <body>: a goal node goal:<name>; gl <ids..>: the grandfather list (one id a line); CT [piece]: run cite, output in $o, rc in $rc
nn(){ printf -- '---\nid: goal:%s\nstatus: active\n---\n# t\n\n%s\n' "$1" "$2">$NG/$1.md;}
gl(){ : >$GF;for i in "$@";do echo "$i">>$GF;done;}
rn(){ rm -f $NG/*.md;gl goal:old1;}
CT(){ o=$(EV sh ${1:-$D/bin/agi-mem} cite 2>&1);rc=$?;}
CTX(){ o=$(env HOME=$D/nohome AGI_POST=q AGI_ENGINE=${2:-$E} AGI_TRUNK=nosuch PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} cite 2>&1);rc=$?;}

# ---- g: the grandfather list is a committed file of node ids; real-file-first: the REAL list covers the REAL tree
RG=$R0/.agi/nodes/.geometry/owner-cite-grandfather.txt;nf=$(grep -rlE '^## OWNER' $R0/.agi/nodes|wc -l|tr -d ' ');ng=$(wc -l <$RG 2>/dev/null|tr -d ' ')
CTX $D/bin/agi-mem $R0
nr=$(echo "$o"|grep -c '^owner-cite: RED')
ok "g1-the-real-tree-names-no-uncited-block the REAL graph ($nf nodes with an OWNER block, $ng ids in the REAL list), run with no store on a post with no mem row: $nr RED line(s) (want 0: every OWNER block outside the list cites an id); rc $rc; last line '$(echo "$o"|tail -1)' (an id that cites reads unread here, the store being belam's: the host check is the existence read)" '[ $nr = 0 ]&&echo "$o"|grep -q "^owner-cite: [0-9]* new OWNER blocks ($ng grandfathered nodes), 0 violations"&&{ [ $rc = 0 ]||echo "$o"|grep -q "^owner-cite: unread (the store"; }'
nbk=$(echo "$o"|sed -n 's/^owner-cite: \([0-9]*\) new OWNER blocks.*/\1/p')
ok "g1b-the-list-covers-the-graph the real list ($ng ids, every line a node id) covers every node with an OWNER block but the ones the check calls new ($nf nodes, $nbk new blocks): the gap is at most the new blocks" '[ $ng -gt 50 ]&&! grep -vqE "^[a-z]+:[A-Za-z0-9._-]+$" $RG&&[ $((nf-ng)) -le "${nbk:-0}" ]&&[ $((nf-ng)) -ge 0 ]'
MUT 's/grep -qxF -- "\$i" \$GF&&continue/false/' agi-mem;CTX $D/mut_agi-mem $R0
ok "g1m-mutant-list-ignored-RED a check that never reads the list flags the REAL graph: '$(echo "$o"|tail -1)' rc $rc (the lane wants GREEN, so this must differ)" '[ $rc = 1 ]&&echo "$o"|tail -1|grep -q RED'

# ---- c: a new OWNER block cites a live owner chunk
rn;nn n-ok "## OWNER 2026-10-25, verbatim

\"ship the widget by friday\" ($OC)
";CT
ok "c1-a-valid-owner-chunk-passes a new node whose OWNER block cites $OC, a live owner chunk: '$o' rc $rc" '[ $rc = 0 ]&&echo "$o"|grep -q "^owner-cite: 1 new OWNER blocks (1 grandfathered nodes), 0 violations$"'
rn;nn n-none "## OWNER 2026-10-25, verbatim

\"ship the widget by friday\"
";CT
ok "c2-no-chunk-id-reads-RED a new OWNER block with no chunk id reads RED by node and heading: '$o' rc $rc" '[ $rc = 1 ]&&echo "$o"|grep -q "^owner-cite: RED goal:n-none: .OWNER 2026-10-25, verbatim. cites no chunk id$"&&echo "$o"|tail -1|grep -q "1 violations RED$"'
MUT 's/if \[ -z "\$t" \];then/if false;then/' agi-mem;CT $D/mut_agi-mem
ok "c2m-mutant-a-block-without-an-id-passes-RED a check with the no-id branch cut lets the bare block through (rc $rc): the lane wants rc 1, so this must be 0" '[ $rc = 0 ]'
rn;nn n-abs "## OWNER 2026-10-25, verbatim

\"ship it\" c:0123456789ab
";CT
ok "c3-an-id-absent-from-the-store-reads-RED a cited c:0123456789ab no store holds reads RED by id: '$o' rc $rc" '[ $rc = 1 ]&&echo "$o"|grep -q "cites c:0123456789ab, absent from the store$"'
rn;nn n-post "## OWNER 2026-10-25, verbatim

\"ship it\" $PC
";CT
ok "c4-a-post-chunk-is-not-the-owners-words a cited $PC is the POST'S chunk: RED by speaker: '$o' rc $rc" '[ $rc = 1 ]&&echo "$o"|grep -q "cites $PC, a post chunk, not the owner.s words$"'
MUT 's/\[ "\$w" = owner \]||{/true||{/' agi-mem;rn;nn n-abs "## OWNER x, verbatim

c:0123456789ab
";CT $D/mut_agi-mem;r1=$rc;rn;nn n-post "## OWNER x, verbatim

$PC
";CT $D/mut_agi-mem
ok "c3m-mutant-no-store-lookup-passes-RED a check that never looks the id up passes an absent id (rc $r1) and a post chunk (rc $rc): the lane wants rc 1 on both" '[ $r1 = 0 ]&&[ $rc = 0 ]'
MUT 's/\[ "\$w" = owner \]||{/[ "$w" ]||{/' agi-mem;CT $D/mut_agi-mem
ok "c4m-mutant-any-chunk-counts-passes-RED a check that accepts a chunk of any speaker passes the post chunk (rc $rc): the lane wants rc 1" '[ $rc = 0 ]'
rn;nn n-bad "## OWNER x, verbatim

c:abc and c:0123456789abcd and $OC
";CT
ok "c5-a-malformed-id-earns-nothing c:abc (3 hex) and c:0123456789abcd (14 hex) are no chunk ids, so only the real one counts ('$o' rc $rc)" '[ $rc = 0 ]'
rn;nn n-bad2 "## OWNER x, verbatim

c:abc and c:0123456789abcd
";CT
ok "c5b-only-malformed-ids-read-as-none a block with only malformed ids reads 'cites no chunk id' (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "cites no chunk id$"'
MUT 's/if(RLENGTH==14)/if(1)/' agi-mem;CT $D/mut_agi-mem
ok "c5m-mutant-any-hex-token-counts-RED a check that takes any c:<hex> as an id reads the malformed ids as cited-and-absent, not as none (got '$(echo "$o"|head -1)'): the lane wants 'cites no chunk id'" '! echo "$o"|grep -q "cites no chunk id$"'
rn;nn n-two "## OWNER first, verbatim

$OC

## OWNER second, verbatim

his other words, no id
";CT
ok "c6-ids-do-not-bleed-between-blocks the second block of one node has no id of its own: exactly 1 violation naming 'OWNER second, verbatim' (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "RED goal:n-two: .OWNER second, verbatim. cites no chunk id$"&&! echo "$o"|grep -q "OWNER first"&&echo "$o"|grep -q "2 new OWNER blocks"'
MUT 's/h=\/^## OWNER\/?\$0:"";t=""}/h=\/^## OWNER\/?$0:""}/' agi-mem;CT $D/mut_agi-mem
ok "c6m-mutant-ids-bleed-RED a check that never resets the ids per block gives the second block the first one's id (rc $rc): the lane wants 1 violation, so this must be 0" '[ $rc = 0 ]'
rn;nn n-next "## OWNER x, verbatim

no id here

## Falsifier

$OC
";CT
ok "c7-a-citation-below-the-next-heading-is-not-the-blocks the block ends at the next ## heading: an id under '## Falsifier' does not cite for it (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "cites no chunk id$"'
rn;nn n-fence 'prose

~~~
## OWNER 2026-10-25, verbatim

nothing
~~~
';CT
ok "c8-a-fenced-heading-is-no-block an OWNER heading inside a ~~~ fence is text: 0 new blocks (got '$o' rc $rc)" '[ $rc = 0 ]&&echo "$o"|grep -q "^owner-cite: 0 new OWNER blocks"'
MUT 's/awk -v m=s "\$FZ" \$x|awk/cat $x|awk/' agi-mem;CT $D/mut_agi-mem
ok "c8m-mutant-fence-blind-RED a check that ignores fences counts the fenced heading as a block (got '$(echo "$o"|tail -1)'): the lane wants 0 new blocks" 'echo "$o"|grep -q "RED goal:n-fence"'
rn;nn n-fid "## OWNER x, verbatim

his words

~~~
$OC
~~~
";CT
ok "c9-a-fenced-id-is-no-citation the only id sits inside a fence: the block still reads 'cites no chunk id' (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "cites no chunk id$"'
MUT 's/awk -v m=s "\$FZ" \$x|awk/cat $x|awk/' agi-mem;CT $D/mut_agi-mem
ok "c9m-mutant-fence-blind-counts-the-fenced-id-RED a fence-blind check lets the fenced id cite (rc $rc): the lane wants rc 1" '[ $rc = 0 ]'
rn;nn n-two2 "## OWNER one, verbatim

$OC and c:0123456789ab
";CT
ok "c10-every-cited-id-must-hold one real id and one absent id in a block: RED naming the absent one only (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "cites c:0123456789ab, absent"&&! echo "$o"|grep -q "cites $OC"'
rn;nn n-head "## OWNER 2026-10-25, verbatim ($OC)

his words, no id below
";CT
ok "c12-an-id-in-the-heading-cites the id sits in the OWNER heading line itself (the b1 idea node's shape): the block passes (got '$o' rc $rc)" '[ $rc = 0 ]&&echo "$o"|grep -q "1 new OWNER blocks (1 grandfathered nodes), 0 violations$"'
MUT 's/h=\/^## OWNER\/?\$0:"";t=""}h!=""{/h=\/^## OWNER\/?$0:"";t="";next}h!=""{/' agi-mem;CT $D/mut_agi-mem
ok "c12m-mutant-the-heading-is-not-read-RED a check that skips the heading line reads the heading-cited block as 'cites no chunk id' (rc $rc): the lane wants rc 0, so this must be 1" '[ $rc = 1 ]&&echo "$o"|grep -q "cites no chunk id$"'
# a chunk the scrub retired is no live chunk
rn;nn n-ret "## OWNER x, verbatim

$OC
";T=$(git -C $S rev-parse refs/heads/mem);export GIT_INDEX_FILE=$D/ri;git -C $S read-tree $T;x=$(git -C $S ls-tree -r --name-only $T|grep "c-${OC#c:}.md");b=$(git -C $S rev-parse $T:$x);printf '0 %040d\t%s\n100644 %s\tmem/retired/%s\n' 0 $x $b ${x#mem/}|git -C $S update-index --index-info;c=$(git -C $S -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit-tree $(git -C $S write-tree) -p $T -m retire);git -C $S update-ref refs/heads/mem $c;unset GIT_INDEX_FILE;CT
ok "c11-a-retired-owner-chunk-is-absent the owner chunk moved to mem/retired/ (agi-mem scrub) is no live chunk: RED absent (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "cites $OC, absent from the store$"'
git -C $S update-ref refs/heads/mem $T

# ---- g2: the list is node ids, never a pattern (falsifier 2)
rn;nn g1.2 "## OWNER x, verbatim

no id
";gl 'goal:g1.*';CT
ok "g2-a-pattern-line-in-the-list-is-unread a list line 'goal:g1.*' is no node id: 'unread', rc 1, and it grandfathers nothing (got '$o' rc $rc)" '[ $rc = 1 ]&&echo "$o"|grep -q "^owner-cite: unread (grandfather line 1 is not a node id)$"'
MUT 's/!\/\^\[a-z\]+:\[A-Za-z0-9._-\]+\$\//!\/.\//' agi-mem;CT $D/mut_agi-mem
ok "g2m-mutant-a-pattern-line-is-accepted-RED a check that never validates the list reads the pattern line as a node id (got '$(echo "$o"|head -1)'): the lane wants unread" '! echo "$o"|grep -q "grandfather line 1"'
rn;nn g1.2 "## OWNER x, verbatim

no id
";gl goal:g1.20;CT
ok "g3-a-longer-id-does-not-grandfather-a-shorter goal:g1.20 in the list leaves goal:g1.2 (whole-line match) RED (got '$o')" '[ $rc = 1 ]&&echo "$o"|grep -q "RED goal:g1.2: "'
MUT 's/grep -qxF -- "\$i" \$GF/grep -q -- "$i" $GF/' agi-mem;CT $D/mut_agi-mem
ok "g3m-mutant-substring-match-RED a check that matches the id as a substring grandfathers goal:g1.2 off goal:g1.20 (rc $rc): the lane wants rc 1, so this must be 0" '[ $rc = 0 ]'
rn;nn g1.2 "## OWNER x, verbatim

no id
";gl goal:g1.2;CT
ok "g4-a-listed-node-is-grandfathered goal:g1.2 listed by id: its bare block is named in the count, not flagged (got '$o' rc $rc)" '[ $rc = 0 ]&&echo "$o"|grep -q "^owner-cite: 0 new OWNER blocks (1 grandfathered nodes), 0 violations$"'

# ---- u: an input it cannot read prints `unread` and exits 1, never 0
rn;rm -f $GF;CT
ok "u1-no-list-is-unread no grandfather list: 'unread', rc 1 (got '$o' rc $rc)" '[ $rc = 1 ]&&echo "$o"|grep -q "^owner-cite: unread (no nodes dir or grandfather list under "'
CTX $D/bin/agi-mem $D/nowhere
ok "u2-no-nodes-dir-is-unread an engine tree with no .agi/nodes: 'unread', rc 1 (got '$o' rc $rc)" '[ $rc = 1 ]&&echo "$o"|grep -q "^owner-cite: unread (no nodes dir"'
rn;nn n-cites "## OWNER x, verbatim

$OC
";CTX
ok "u3-no-store-while-a-block-cites a post that cannot read the store (no ~/.mem) and a block that cites an id: 'unread', rc 1, never a pass (got '$o' rc $rc)" '[ $rc = 1 ]&&echo "$o"|grep -q "owner-cite: unread (the store .*cannot be read and a block cites a chunk id)"'
MUT 's/||{ un=1;: >\$D\/hg;}/||{ : >$D\/hg;}/' agi-mem;CTX $D/mut_agi-mem $E
ok "u3m-mutant-unread-store-reads-as-absent-RED a check that treats an unreadable store as an empty one says 'absent', not 'unread' (got '$(echo "$o"|head -1)'): the lane wants unread" '! echo "$o"|grep -q unread'
rn;nn n-bare "## OWNER x, verbatim

no id
";CTX
ok "u4-a-bare-block-is-RED-without-a-store the bare block needs no store to be wrong: RED by name even where the store is unreadable (got '$o' rc $rc)" '[ $rc = 1 ]&&echo "$o"|grep -q "RED goal:n-bare: .*cites no chunk id$"&&! echo "$o"|grep -q unread'

# ---- p: it runs on any post
rn;nn n-p "## OWNER x, verbatim

no id
";CTX
ok "p1-runs-on-a-post-with-no-mem-row posts.md unreadable (AGI_TRUNK=nosuch) and the post q has no row: cite still runs and names the block (a silent exit 0 would pass it): rc $rc" '[ $rc = 1 ]&&echo "$o"|grep -q "RED goal:n-p"'
MUT 's/\[ "\$1" = cite \]||case/[ "$1" = nocite ]||case/' agi-mem;CTX $D/mut_agi-mem $E
ok "p1m-mutant-gated-by-the-mem-row-RED a cite that sits behind the mem: full gate exits 0 and says nothing on a post without a row (rc $rc, output '$o'): the lane wants the block named" '[ $rc = 0 ]&&[ -z "$o" ]'
echo "owner-cite: $f FAIL";exit $f
