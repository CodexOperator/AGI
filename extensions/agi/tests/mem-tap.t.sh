#!/bin/sh
# mem-tap.t.sh [ROOT]: goal:g7.16.1.11.46.13 (M6) falsifier 1 + 2: one lane per row R1-R7, each with its MUTANT read RED
# sh + git + jq + python3 + getfacl on a scratch HOME and a scratch engine repo; no network, no root, 0 USD. ROOT = the tree whose engine-post.md / engine-wrap.md carry the pieces and whose extensions/agi/bin/{anonymize,geometry_config}.py are used. exit = the FAIL count.
# G1 (council 14:1xZ): the push negative is `push.*(refs/\*|--mirror)` -- in an ERE `[^\n]` is "not a backslash, not n", so the first spelling never matched `"push", "origin", "refs/*:refs/*"`. G3: a stubbed `id` cannot prove a permission, so R1 asserts the MODE 0700, the OWNER = the facing uid and NO ACL entry; a real second-uid read runs only where a second uid exists (else it prints `skip`).
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_MINT AGI_MEM_BATCH
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;sect agi-mem engine-post.md>$D/bin/agi-mem;sect agi-meter engine-post.md>$D/bin/agi-meter;sect agi-brief engine-post.md>$D/bin/agi-brief;sect settings.json engine-wrap.md>$D/settings.json;printf '#!/bin/sh\nexit 0\n'>$D/bin/agi-atomize;chmod +x $D/bin/*
[ -s $D/bin/agi-mem ]||{ echo "FAIL inputs: no agi-mem piece";exit 99;}
# the engine repo: posts.md rows p (mem: full, faces: owner) and q (mem: none); `trunk` is HEAD; extensions -> the tree under test
E=$D/eng;mkdir -p $E/.agi/nodes/.geometry;ln -s $R0/extensions $E/extensions
cat >$E/.agi/nodes/.geometry/posts.md<<'EOF'
---
id: config:posts
parents:
  - goal:g7
posts:
  - {"name": "p", "mem": "full", "faces": "owner"}
  - {"name": "q", "mem": "none"}
---
EOF
(cd $E&&git init -q .&&git config core.hooksPath /dev/null&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x)
HOST=$(hostname -s)
# one transcript line per call: user / queued / assistant / tool_result / compact / meta
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:00Z","message":{"content":%s}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
QL(){ printf '{"type":"attachment","uuid":"%s","timestamp":"2026-10-24T10:00:01Z","attachment":{"type":"queued_command","prompt":%s}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
AL(){ printf '{"type":"assistant","uuid":"%s","timestamp":"2026-10-24T10:00:02Z","message":{"content":[{"type":"text","text":%s},{"type":"tool_use","name":"x"}]}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
TR(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:03Z","message":{"content":[{"type":"tool_result","content":"x"}]}}\n' "$1";}
CS(){ printf '{"type":"user","uuid":"%s","isCompactSummary":true,"timestamp":"2026-10-24T10:00:04Z","message":{"content":"Earlier work, summarised for the new window"}}\n' "$1";}
ME(){ printf '{"type":"user","uuid":"%s","isMeta":true,"timestamp":"2026-10-24T10:00:05Z","message":{"content":"meta words"}}\n' "$1";}
# fresh HOME h$1 with a transcript X (session S1) and a run helper: TAP <home> [piece]; the post is p unless P=q
nh(){ H=$D/h$1;rm -rf "${H:?}";mkdir -p $H/.claude/projects/x;X=$H/.claude/projects/x/S1.jsonl;: >$X;echo S1>$H/.session;S=$H/.mem/p.git;}
TAP(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\",\"prompt\":\"hi\",\"tokens\":1}"|env HOME=$H AGI_POST=${P:-p} AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} tap 2>&1;}
AT(){ env HOME=$H AGI_POST=${P:-p} AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} at 2>&1;}
nchunks(){ git -C $S grep -c '^id: c:' refs/heads/mem 2>/dev/null|awk -F: '{n+=$NF}END{print n+0}';}
nowner(){ git -C $S grep --all-match -l -e '^speaker: owner$' -e "$1" refs/heads/mem 2>/dev/null|wc -l|tr -d ' ';}
# mutate: MUT <sed-expr> -> $D/mut (a copy of the piece with the one edit; the edit MUST change it)
MUT(){ sed "$1" $D/bin/agi-mem>$D/mut;cmp -s $D/bin/agi-mem $D/mut&&{ echo "FAIL inputs: mutant edit '$1' changed nothing";exit 99;};}

# ---- R1 STORE: own bare dir, mode 0700, owner = the facing uid, NO ACL entry, no remote; never refs/mem in the shared repo
nh r1;UL u1 "hello there" >>$X;TAP >$D/out
storeok(){ [ "$(stat -c %a $1)" = 700 ]&&[ "$(stat -c %u $1)" = "$(id -u)" ]&&[ "$(getfacl -p $1|grep -c '^user:[^:]\|^group:[^:]\|^default:')" = 0 ]&&[ -z "$(git -C $1 remote)" ];}
ok "r1-store-is-0700-own-uid-no-acl-no-remote the store $S exists, mode $(stat -c %a $S 2>/dev/null), owner uid $(stat -c %u $S 2>/dev/null) (want $(id -u)), $(getfacl -p $S 2>/dev/null|grep -c '^user:[^:]\|^group:[^:]\|^default:') ACL entries, remote '$(git -C $S remote 2>/dev/null)'" 'storeok $S'
ok "r1-parent-dir-0700 the dir holding the store is 0700 too ($(stat -c %a ${S%/*}))" '[ "$(stat -c %a ${S%/*})" = 700 ]'
ok "r1-keyed-by-the-post-mint-id the store name is the post name unless AGI_MINT names it: ${S##*/}; with AGI_MINT=m1f0 it is m1f0.git" 'nh r1k;UL u1 hi>>$X;echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_MINT=m1f0 AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/bin/agi-mem tap;[ -d $H/.mem/m1f0.git ]&&[ ! -d $H/.mem/p.git ]'
S=$D/hr1/.mem/p.git;ok "r1-nothing-under-refs-mem the shared (engine) repo lists no refs/mem and the store keeps its chunks on refs/heads/mem only" '[ -z "$(git -C $E for-each-ref refs/mem)" ]&&[ -z "$(git -C $S for-each-ref refs/mem)" ]&&git -C $S rev-parse -q --verify refs/heads/mem>/dev/null'
# mutants: mode 0750 / one ACL entry / a remote / the store placed under refs/mem in the shared repo
nh r1m;UL u1 hi>>$X;TAP>/dev/null;chmod 750 $S;ok "r1-mutant-mode-0750-RED a store at 0750 fails the same predicate" '! storeok $S'
nh r1m2;UL u1 hi>>$X;TAP>/dev/null;setfacl -m u:65534:rx $S 2>/dev/null;ok "r1-mutant-one-ACL-entry-RED a store with ONE named ACL entry fails the same predicate (getfacl lists $(getfacl -p $S|grep -c '^user:[^:]'))" '! storeok $S'
nh r1m3;UL u1 hi>>$X;TAP>/dev/null;git -C $S remote add o /nowhere;ok "r1-mutant-a-remote-RED a store with a remote fails the same predicate" '! storeok $S'
git -C $E update-ref refs/mem/p/- HEAD;ok "r1-mutant-store-under-refs-mem-RED a refs/mem ref in the shared repo makes the negative read non-empty" '[ -n "$(git -C $E for-each-ref refs/mem)" ]';git -C $E update-ref -d refs/mem/p/-
if sudo -n -u nobody true 2>/dev/null;then ok "r1-peer-uid-read-fails a read of the store from another uid fails" '! sudo -n -u nobody git -C $S log -1 refs/heads/mem >/dev/null 2>&1';else echo "skip r1-peer-uid-read-fails: no second uid on this box (sudo -n -u nobody unavailable); the mode/owner/ACL lanes above carry the permission";fi

# ---- R2 REDACT, NEVER REFUSE
nh r2;UL u1 "build it in /home/zed/proj and ssh $HOST now" >>$X;TAP>$D/out
ok "r2-redacts-not-refuses the prompt with a home literal and this box's hostname yields ONE owner chunk with redacted: 2 and neither literal in the store (chunks $(nchunks), $(git -C $S grep -h '^redacted:' refs/heads/mem|head -1))" '[ "$(nchunks)" = 1 ]&&git -C $S grep -q "^redacted: 2$" refs/heads/mem&&! git -C $S grep -qiE "zed|$HOST" refs/heads/mem&&git -C $S grep -q "<home>/proj and ssh <host> now" refs/heads/mem'
mkdir -p $D/stub/extensions/agi/bin;cp $E/.agi -r $D/stub/ 2>/dev/null;printf 'import sys,json\nfor l in sys.stdin:\n    o=json.loads(l);o["n"]=0;print(json.dumps(o))\n' >$D/stub/extensions/agi/bin/anonymize.py;(cd $D/stub&&git init -q .&&git config core.hooksPath /dev/null&&git add -A .agi&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x)
nh r2m;UL u1 "build it in /home/zed/proj" >>$X;echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$D/stub AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/bin/agi-mem tap>/dev/null
ok "r2-mutant-no-redaction-RED a redactor that passes the text through leaves the literal in the store, the same predicate reads RED" 'git -C $S grep -q "zed" refs/heads/mem'
printf 'import sys\nsys.exit(1)\n' >$D/stub/extensions/agi/bin/anonymize.py;nh r2f;UL u1 "words" >>$X;o=$(echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$D/stub AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/bin/agi-mem tap;echo "rc=$?")
ok "r2-redactor-down-names-it-and-keeps-the-line a redactor that fails = rc 0, ONE [mem] warn, no chunk, the cursor NOT advanced (so the next sweep retries): $(echo "$o"|tr '\n' '|')" '[ "$(echo "$o"|grep -c "^\[mem\] warn")" = 1 ]&&echo "$o"|grep -q "^rc=0"&&[ ! -f $S/cursor-S1 ]'

# ---- R3 TAP: user strings AND queued_command, deduped by uuid, a Stop sweep from a cursor
nh r3;UL u1 "string ask" >>$X;QL u2 "queued ask" >>$X;UL u1 "string ask" >>$X;TAP>/dev/null
ok "r3-queued-and-string-lines-chunk a user string AND a queued_command line each yield an owner chunk, a repeated uuid yields none (chunks $(nchunks))" 'git -C $S grep -q "^queued ask$" refs/heads/mem&&git -C $S grep -q "^string ask$" refs/heads/mem&&[ "$(nchunks)" = 2 ]'
UL u3 "after the cursor" >>$X;AL a1 "On it: a12">>$X;TAP>/dev/null;c1=$(nchunks);TAP>/dev/null
ok "r3-stop-sweep-from-the-cursor a later sweep reads only the new lines (chunks 2 -> $c1, the post's text block is a post chunk), and a repeat sweep adds none ($(nchunks))" '[ "$c1" = 4 ]&&[ "$(nchunks)" = 4 ]&&git -C $S grep -q "^speaker: post$" refs/heads/mem&&[ "$(cat $S/cursor-S1)" = "$(wc -l <$X|tr -d " ")" ]'
MUT 's/elif .type=="attachment" and .attachment.type=="queued_command"/elif false/';nh r3m;QL u2 "queued ask" >>$X;TAP $D/mut>/dev/null
ok "r3-mutant-queued-line-dropped-RED a tap that reads no queued_command yields no chunk for it ($(nchunks)), the lane r3 wants it" '[ "$(nchunks)" = 0 ]'

# ---- R4 SPEAKER TRUTH: never owner for a compact summary, meta, tool_result, a nudge or another harness-injected prompt
nh r4;CS u1>>$X;ME u2>>$X;TR u3>>$X;UL u4 "mail: box read">>$X;UL u5 "keepalive: reply with the one word ok">>$X;QL u6 "<task-notification><task-id>x</task-id></task-notification>">>$X;QL u7 "mail: box read">>$X;TAP>/dev/null
ok "r4-no-owner-chunk-for-injected-lines a compact summary, a meta line, a tool_result, 'mail: box read' (string and queued), a keepalive and a task-notification yield 0 chunks (got $(nchunks))" '[ "$(nchunks)" = 0 ]'
MUT 's/ and .isCompactSummary!=true//';nh r4m;CS u1>>$X;TAP $D/mut>/dev/null;ok "r4-mutant-compact-summary-RED a tap that drops the isCompactSummary test writes an owner chunk ($(nowner 'speaker'))" '[ "$(nchunks)" -ge 1 ]'
MUT 's/mail: box read|//';nh r4m2;UL u4 "mail: box read">>$X;TAP $D/mut>/dev/null;ok "r4-mutant-nudge-RED a tap that drops the nudge test writes an owner chunk for 'mail: box read' ($(nchunks))" '[ "$(nchunks)" -ge 1 ]'

# ---- R5 ADDRESS: sha over (speaker, session, transcript uuid, body); the body stays verbatim
nh r5;UL u1 "same words" >>$X;UL u2 "same words" >>$X;TAP>/dev/null
ok "r5-same-words-two-uuids-two-chunks the same words under two uuids are 2 chunks with 2 ids ($(git -C $S grep -h '^id: ' refs/heads/mem|sort -u|wc -l|tr -d ' '))" '[ "$(nchunks)" = 2 ]&&[ "$(git -C $S grep -h "^id: " refs/heads/mem|sort -u|wc -l|tr -d " ")" = 2 ]'
nh r5b;UL u1 "  verbatim:   spaces, tabs	and a trailing blank line

" >>$X;TAP>/dev/null;git -C $S show refs/heads/mem:$(git -C $S ls-tree -r --name-only refs/heads/mem|head -1)|sed '1,/^---$/{/^---$/!d;}' |sed '1,/^---$/d'>$D/body1;printf '  verbatim:   spaces, tabs\tand a trailing blank line\n\n'>$D/body0
ok "r5-body-verbatim the chunk body is the line's text byte for byte (no trim, no edit)" 'cmp -s $D/body0 $D/body1'
MUT 's/printf .%s\\0%s\\0%s\\0. \$sp \$s \$u;/printf "%s\\0%s\\0" $sp $s;/';nh r5m;UL u1 "same words" >>$X;UL u2 "same words" >>$X;TAP $D/mut>/dev/null;ok "r5-mutant-no-uuid-in-the-address-RED an address without the uuid makes the same words ONE chunk ($(nchunks))" '[ "$(nchunks)" = 1 ]'

# ---- R6 NEVER BLOCKS, NEVER SILENT
nh r6;UL u1 "one" >>$X;UL u2 "two" >>$X;UL u3 "three" >>$X;TAP>/dev/null;a=$(AT)
ok "r6-at-line-tapped-k-of-m after a sweep the at line reads 'mem: tapped 3/3' and is not RED (got '$a')" '[ "$a" = "mem: tapped 3/3" ]'
nh r6u;UL u1 "words" >>$X;TAP>/dev/null;chmod 500 $S/objects;UL u2 "more words" >>$X;o=$(TAP;echo "rc=$?")
ok "r6-unwritable-store-warns-once-and-exits-0 an unwritable store leaves the hook at rc 0 with ONE [mem] warn line: $(echo "$o"|tr '\n' '|')" '[ "$(echo "$o"|grep -c "^\[mem\] warn")" = 1 ]&&echo "$o"|grep -q "^rc=0$"'
chmod 700 $S/objects
sed 's/{ w "store $S not writable";exit 0;}/{ w "store $S not writable";exit 3;}/' $D/bin/agi-mem>$D/mut;cmp -s $D/bin/agi-mem $D/mut&&{ echo "FAIL inputs: r6 mutant changed nothing";exit 99;}
nh r6um;UL u1 "words" >>$X;TAP>/dev/null;chmod 500 $S/objects;UL u2 "more" >>$X;TAP $D/mut>/dev/null;ok "r6-mutant-the-store-raises-and-the-hook-exits-non-zero-RED a tap that exits non-zero on a store failure is the one the lane catches" '! echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/mut tap >/dev/null 2>&1';chmod 700 $S/objects
nh r6x;UL u1 "words" >>$X;a=$(AT)
ok "r6-unread-when-the-store-cannot-be-read no store yet but an owner line to cover = 'mem: unread' (got '$a')" '[ "$a" = "mem: unread" ]'
MUT 's/case $u in//;s/^  id=/  case $u in *2) continue;; esac\n  id=/';nh r6d;UL u1 a>>$X;UL u2 b>>$X;UL u3 c>>$X;TAP $D/mut>/dev/null;a=$(AT)
ok "r6-mutant-the-hook-drops-one-line-RED a tap that drops a line leaves chunks 2 of 3 eligible and the at line says RED (got '$a')" '[ "$a" = "mem: tapped 2/3 RED" ]'
P=q;nh r6q;UL u1 hi>>$X;o=$(TAP;AT);P=;ok "r6-not-a-full-row-is-silent-and-writes-nothing a post whose row is not mem: full taps nothing and prints no at line (out '$o', store $( [ -d $H/.mem ]&&echo present||echo absent))" '[ -z "$o" ]&&[ ! -d $H/.mem ]'
# wiring: the prompt side rides agi-meter, the Stop hook is NEW, the at line rides agi-brief
nh r6m;echo "{\"prompt\":\"mail: box read\",\"transcript_path\":\"$X\",\"session_id\":\"S1\",\"tokens\":1}">$D/pj;UL u1 "via the meter" >>$X;env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/bin/agi-meter <$D/pj>/dev/null 2>&1
ok "r6-prompt-side-rides-agi-meter agi-meter, given the hook JSON, taps the owner line (chunks $(nchunks))" '[ "$(nchunks)" = 1 ]'
ok "r6-stop-hook-is-new settings.json wires 'agi-mem tap' on Stop beside agi-turn, and agi-brief calls 'agi-mem at'" 'jq -e "[.hooks.Stop[].hooks[].command]|index(\"agi-mem tap\") and index(\"agi-turn\")" $D/settings.json>/dev/null&&grep -q "agi-mem at" $D/bin/agi-brief'

# ---- R6' / R7' (alive 15:1xZ): the cell is read from ROW lines only (the real posts.md has a `  - goal:g7` frontmatter item before `posts:` that killed the first pipeline), and a read that FAILS is named, never silent
nh r6r;UL u1 "words" >>$X;TAP>/dev/null
ok "r7p-real-frontmatter-shape-still-taps the fixture carries the real frontmatter shape (parents: + '  - goal:g7' before posts:) and the full row still taps (chunks $(nchunks))" '[ "$(nchunks)" = 1 ]&&grep -q "^  - goal:g7$" $E/.agi/nodes/.geometry/posts.md'
MUT 's/sed -n .s\/^  - {\/{\/p.|jq -rR "fromjson?|/sed -n "s\/^  - \/\/p"|jq -r "/' agi-mem;nh r6r2;UL u1 "words" >>$X;TAP $D/mut>/dev/null
ok "r7p-mutant-the-old-hand-parser-RED the first pipeline (every '  - ' line piped to jq) taps NOTHING on the real shape (chunks $(nchunks)): the lane above wants 1" '[ "$(nchunks)" = 0 ]'
nh r6r3;UL u1 "words" >>$X;o=$(echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=nosuchref PATH=$D/bin:$PATH sh $D/bin/agi-mem tap 2>&1;echo "rc=$?");a=$(env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=nosuchref PATH=$D/bin:$PATH sh $D/bin/agi-mem at 2>&1)
ok "r6p-unreadable-posts-md-is-named a trunk ref that cannot be read: tap = ONE [mem] warn and rc 0 ($(echo "$o"|tr '\n' '|')), at = 'mem: unread' (got '$a')" '[ "$(echo "$o"|grep -c "^\[mem\] warn")" = 1 ]&&echo "$o"|grep -q "^rc=0$"&&[ "$a" = "mem: unread" ]'
P=nobody;nh r6r4;UL u1 "words" >>$X;o=$(TAP;AT);P=;ok "r6p-no-row-for-the-post-is-quiet a post with no row in posts.md taps nothing and prints nothing (out '$o')" '[ -z "$o" ]&&[ ! -d $H/.mem ]'

# ---- R7 CELLS: mem: full|season|goal|none, faces: owner|posts|none; absent mem reads none; faces: owner needs mem: full
GC=$R0/extensions/agi/bin/geometry_config.py;G7=$D/g7;mkdir -p $G7/nodes/.geometry
row(){ printf -- '---\nid: config:posts\nposts:\n  - {"name": "a", "mem": "full", "faces": "owner"}\n  - {"name": "b"}\n  - {"name": "c", "mem": "season"}\n%s---\n' "$1">$G7/nodes/.geometry/posts.md;}
row '';o=$(python3 $GC --root $G7 --cells 2>&1);rc=$?;ok "r7-legal-cells-accepted faces: owner + mem: full, an absent mem:, and mem: season without faces pass (rc $rc, '$o')" '[ $rc = 0 ]'
row '  - {"name": "d", "mem": "season", "faces": "owner"}
';o=$(python3 $GC --root $G7 --cells 2>&1);rc=$?;ok "r7-faces-owner-needs-mem-full a row with faces: owner + mem: season is refused: rc $rc, ONE named line '$o'" '[ $rc != 0 ]&&[ "$(echo "$o"|wc -l|tr -d " ")" = 1 ]&&echo "$o"|grep -q "^\[cells\] d: faces: owner requires mem: full (has mem: season)$"'
row '  - {"name": "e", "faces": "owner"}
';o=$(python3 $GC --root $G7 --cells 2>&1);rc=$?;ok "r7-absent-mem-reads-none faces: owner with no mem: is refused as mem: none (rc $rc, '$o')" '[ $rc != 0 ]&&echo "$o"|grep -q "has mem: none"'
row '  - {"name": "f", "mem": "always"}
';o=$(python3 $GC --root $G7 --cells 2>&1);rc=$?;ok "r7-unknown-value-refused mem: always is not a value (rc $rc, '$o')" '[ $rc != 0 ]&&echo "$o"|grep -q "mem: always is not"'
sed 's/elif faces == "owner" and mem != "full":/elif False:/' $GC>$D/gc_mut.py;cmp -s $GC $D/gc_mut.py&&{ echo "FAIL inputs: r7 mutant changed nothing";exit 99;};mkdir -p $D/m/agi/bin;ln -s $R0/extensions/agi/src $D/m/agi/src;cp $D/gc_mut.py $D/m/agi/bin/geometry_config.py
row '  - {"name": "d", "mem": "season", "faces": "owner"}
';ok "r7-mutant-reader-without-the-check-RED a reader without the faces/mem check accepts faces: owner + mem: season (rc 0), the lane r7 wants rc != 0" 'python3 $D/m/agi/bin/geometry_config.py --root $G7 --cells >/dev/null 2>&1'
ok "r7-belam-only the trunk's posts.md carries mem: full + faces: owner on belam and no other row carries either" '[ "$(python3 $GC --root $R0/.agi --cells|head -1)" != "" ]&&[ "$(grep -c "\"mem\": " $R0/.agi/nodes/.geometry/posts.md)" = 1 ]&&grep -q "\"name\": \"belam\", \"mem\": \"full\", \"faces\": \"owner\"" $R0/.agi/nodes/.geometry/posts.md&&python3 $GC --root $R0/.agi --cells >/dev/null'

# ---- falsifier 2: no refs/mem in the shared repo, no engine push spelling that covers the store
PG='push.*(refs/\*|--mirror)'
ok "f2-no-refs-mem-on-the-shared-repo git for-each-ref refs/mem prints nothing on this tree" '[ -z "$(git -C $R0 for-each-ref refs/mem 2>/dev/null)" ]'
ok "f2-no-push-spelling-covers-the-store 'git grep -nE \"$PG\" -- extensions/agi/bin extensions/agi/hooks' prints nothing (G1: the ERE the council fixed)" '[ -z "$(cd $R0&&{ git grep -nE "$PG" -- extensions/agi/bin extensions/agi/hooks 2>/dev/null||grep -rnE "$PG" extensions/agi/bin extensions/agi/hooks;})" ]'
mkdir -p $D/pm/extensions/agi/bin $D/pm/extensions/agi/hooks;printf 'x = ["git", "push", "origin", "refs/*:refs/*"]\n'>$D/pm/extensions/agi/bin/a.py;printf 'git push origin --mirror\n'>$D/pm/extensions/agi/hooks/b.sh
(cd $D/pm&&git init -q .&&git add -A&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm x)
ok "f2-mutant-a-refs-star-push-spelling-RED the planted \"push\", \"origin\", \"refs/*:refs/*\" line AND a --mirror push both hit the fixed ERE ($(cd $D/pm&&git grep -nE "$PG" -- extensions/agi/bin extensions/agi/hooks|wc -l|tr -d ' ') hits)" '[ "$(cd $D/pm&&git grep -nE "$PG" -- extensions/agi/bin extensions/agi/hooks|wc -l|tr -d " ")" = 2 ]'
ok "f2-the-old-ere-was-vacuous the council-measured fault: the old not-backslash-not-n ERE hits NEITHER planted spelling (0 hits), which is why G1 replaced it" '[ "$(cd $D/pm&&git grep -nE "push[^\\n]*(refs/\*|--mirror)" -- extensions/agi/bin extensions/agi/hooks|wc -l|tr -d " ")" = 0 ]'
echo "mem-tap: $f FAIL";exit $f
