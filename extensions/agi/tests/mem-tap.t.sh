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
UL(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:00Z","origin":{"kind":"human"},"message":{"content":%s}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
UO(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:00Z","origin":%s,"message":{"content":%s}}\n' "$1" "$3" "$(printf '%s' "$2"|jq -Rs .)";}
QL(){ printf '{"type":"attachment","uuid":"%s","timestamp":"2026-10-24T10:00:01Z","attachment":{"type":"queued_command","origin":{"kind":"human"},"prompt":%s}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
AL(){ printf '{"type":"assistant","uuid":"%s","timestamp":"2026-10-24T10:00:02Z","message":{"content":[{"type":"text","text":%s},{"type":"tool_use","name":"x"}]}}\n' "$1" "$(printf '%s' "$2"|jq -Rs .)";}
TR(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:03Z","message":{"content":[{"type":"tool_result","content":"x"}]}}\n' "$1";}
CS(){ printf '{"type":"user","uuid":"%s","isCompactSummary":true,"origin":{"kind":"human"},"timestamp":"2026-10-24T10:00:04Z","message":{"content":"Earlier work, summarised for the new window"}}\n' "$1";}
ME(){ printf '{"type":"user","uuid":"%s","isMeta":true,"timestamp":"2026-10-24T10:00:05Z","message":{"content":"meta words"}}\n' "$1";}
# fresh HOME h$1 with a transcript X (session S1) and a run helper: TAP <home> [piece]; the post is p unless P=q
nh(){ H=$D/h$1;rm -rf "${H:?}";mkdir -p $H/.claude/projects/x;X=$H/.claude/projects/x/S1.jsonl;: >$X;echo S1>$H/.session;S=$H/.mem/p.git;}
TAP(){ echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\",\"prompt\":\"hi\",\"tokens\":1}"|env HOME=$H AGI_POST=${P:-p} AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} tap 2>&1;}
AT(){ env HOME=$H AGI_POST=${P:-p} AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} at 2>&1;}
nchunks(){ git -C $S grep -c '^id: c:' refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|awk -F: '{n+=$NF}END{print n+0}';}
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

# R4 live red (belam 15:4xZ): a CROSS-SESSION message and the harness's own openers were stored as `speaker: owner`
nh r4x;UL c1 '<cross-session-message from="x" from-name="t-e4">hand-off: rows 8.1-8.8 and 2.5</cross-session-message>'>>$X;UL c2 '[SYSTEM NOTIFICATION - NOT USER INPUT] a task ended'>>$X;UL c3 '<system-reminder>reminder text'>>$X;UL c4 '<task-notification>done</task-notification>'>>$X;UL u9 "my real words">>$X;TAP>/dev/null
ok "r4x-cross-session-and-harness-openers-are-not-owner a <cross-session-message, a [SYSTEM NOTIFICATION, a <system-reminder and a <task-notification opener yield 0 chunks; the one real owner line yields 1 (chunks $(nchunks))" '[ "$(nchunks)" = 1 ]&&git -C $S grep -q "^my real words$" refs/heads/mem'
MUT 's/<\[a-z\]\[a-z-\]\*\[ >\]|//';nh r4xm;UL c1 '<cross-session-message from="x">hand-off</cross-session-message>'>>$X;TAP $D/mut>/dev/null
ok "r4x-mutant-cross-session-reads-owner-RED a filter without the <cross-session-message opener stores it as an owner chunk ($(nchunks)): the lane above wants 0" '[ "$(nchunks)" = 1 ]&&git -C $S grep -q "^speaker: owner$" refs/heads/mem'
# REPAIR' (council 15:4xZ): scrub RETIRES (moves, bytes unchanged) an owner chunk that carries a not-owner opener to mem/retired/ and clears that session's cursor; at / derive / label / find read mem/<date>/ only; at is RED on k != m
XS='<cross-session-message from="x">hand-off</cross-session-message>'
MUT 's/<\[a-z\]\[a-z-\]\*\[ >\]|//';cp $D/mut $D/mut_f
MUT 's/ -- mem .:!mem\/retired. 2>\/dev\/null|awk "\$HT"/ -- mem 2>\/dev\/null|awk "$HT"/';cp $D/mut $D/mut_at
MUT 's/\[ \$new -gt 0 \]&&cm "speaker not human.*;exit 0;;/exit 0;;/';cp $D/mut $D/mut_scrub
SCR(){ env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} scrub;}
nh r4s;UL c1 "$XS">>$X;UL u9 "my real words">>$X;TAP $D/mut_f>/dev/null;n0=$(nchunks);a0=$(AT);px=$(git -C $S grep -l cross-session refs/heads/mem|sed 's/^[^:]*://');b0=$(git -C $S rev-parse refs/heads/mem:$px);SCR;n1=$(nchunks);b1=$(git -C $S rev-parse refs/heads/mem:mem/retired/${px#mem/});cur=$([ -f $S/cursor-S1 ]&&echo kept||echo cleared);a1=$(AT);TAP>/dev/null;a2=$(AT);msg=$(git -C $S log -1 --format=%s refs/heads/mem~1 2>/dev/null)
ok "r4s-k-not-m-is-red a misattribution left in the store reads RED on k > m: '$a0'" '[ "$a0" = "mem: tapped 2/1 RED (1 owner chunk not owner by the current filter)" ]'
ok "r4s-scrub-retires-never-deletes the real scrub moves the chunk to mem/retired/ (live $n0 -> $n1), its blob is unchanged ($b0 = $b1), the session cursor is $cur, the commit names the rule; right after at is '$a1', after the re-sweep '$a2'" '[ "$n0" = 2 ]&&[ "$n1" = 1 ]&&[ "$b0" = "$b1" ]&&[ "$cur" = cleared ]&&git -C $S log --format=%s refs/heads/mem|grep -q "^speaker not human"&&[ "$a1" = "mem: unread" ]&&[ "$a2" = "mem: tapped 1/1" ]&&git -C $S grep -q "^my real words$" refs/heads/mem -- mem ":!mem/retired"&&! git -C $S grep -q cross-session refs/heads/mem -- mem ":!mem/retired"'
nh r4sx;UL c1 "$XS">>$X;UL u9 "my real words">>$X;TAP $D/mut_f>/dev/null;SCR;TAP>/dev/null;ax=$(AT $D/mut_at);ac=$(AT)
ok "r4s-mutant-retired-counts-in-k-RED an at that does not exclude mem/retired/ reads '$ax' where the real at reads '$ac'" '[ "$ax" = "mem: tapped 2/1 RED (1 owner chunk not owner by the current filter)" ]&&[ "$ac" = "mem: tapped 1/1" ]'
nh r4sm;UL c1 "$XS">>$X;TAP $D/mut_f>/dev/null;SCR $D/mut_scrub
ok "r4s-mutant-scrub-that-never-commits-RED a scrub that commits nothing leaves the chunk live ($(nchunks)); the lane above wants it retired" '[ "$(nchunks)" = 1 ]'

# R4' (council 15:4xZ): owner = origin.kind human AND no tag opener (leading blanks allowed) AND no nudge prefix
nh r4o;UO k1 "plain words from a task" '{"kind":"task-notification","producer":"session-task"}'>>$X;printf '{"type":"user","uuid":"k2","timestamp":"2026-10-24T10:00:00Z","message":{"content":"no origin at all"}}\n'>>$X;UL k3 '<new-envelope x="y">unknown wrapper'>>$X;UL k4 '
<task-notification>after a newline'>>$X;UL k5 "a plain human line">>$X;TAP>/dev/null
ok "r4o-owner-needs-human-origin-and-no-tag-opener origin.kind task-notification with plain text, a missing origin, an unknown <new-envelope x=\"y\"> with kind human and a leading newline before <task-notification all yield 0 chunks; the plain human line yields 1 (chunks $(nchunks))" '[ "$(nchunks)" = 1 ]&&git -C $S grep -q "^a plain human line$" refs/heads/mem'
MUT 's/ and \.origin\.kind=="human" then {sp:"owner"/ then {sp:"owner"/';nh r4om;UO k1 "plain words from a task" '{"kind":"task-notification"}'>>$X;TAP $D/mut>/dev/null
ok "r4o-mutant-no-origin-check-RED a tap that ignores origin.kind stores a task-notification's plain text as an owner chunk ($(nchunks)): the lane above wants 0" '[ "$(nchunks)" = 1 ]'
MUT "s/^NU='\[\[:space:\]\]\*(/NU='(/";nh r4on;UL k4 '
<task-notification>after a newline'>>$X;TAP $D/mut>/dev/null
ok "r4o-mutant-no-leading-blank-allowance-RED an opener test anchored without the blank allowance stores a leading-newline <task-notification as an owner chunk ($(nchunks)): the lane above wants 0" '[ "$(nchunks)" = 1 ]'
MUT 's/<\[a-z\]\[a-z-\]\*\[ >\]|//';nh r4ou;UL k3 '<new-envelope x="y">unknown wrapper'>>$X;TAP $D/mut>/dev/null
ok "r4o-mutant-deny-list-only-RED a prefix deny-list without the generic tag-opener rule stores an unknown <new-envelope> as an owner chunk ($(nchunks)): the lane above wants 0" '[ "$(nchunks)" = 1 ]'

# the real red's shape (belam 15:4xZ): a queued_command whose attachment.origin.kind is "peer"
nh r4q;printf '{"type":"attachment","uuid":"q1","timestamp":"2026-10-24T10:00:01Z","attachment":{"type":"queued_command","origin":{"kind":"peer"},"prompt":"plain words from another session"}}\n'>>$X;QL q2 "a human queued line">>$X;TAP>/dev/null
ok "r4q-queued-peer-origin-is-not-owner a queued_command with attachment.origin.kind peer and plain text yields 0 chunks; a human queued line yields 1 (chunks $(nchunks))" '[ "$(nchunks)" = 1 ]&&git -C $S grep -q "^a human queued line$" refs/heads/mem'
MUT 's/ and \.attachment\.origin\.kind=="human" then/ then/';nh r4qm;printf '{"type":"attachment","uuid":"q1","timestamp":"2026-10-24T10:00:01Z","attachment":{"type":"queued_command","origin":{"kind":"peer"},"prompt":"plain words from another session"}}\n'>>$X;TAP $D/mut>/dev/null
ok "r4q-mutant-queued-origin-unchecked-RED a tap that checks no queued_command origin stores the peer's plain text as an owner chunk ($(nchunks)): the lane above wants 0" '[ "$(nchunks)" = 1 ]'

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
MUT 's/sed -n .s\/^  - {\/{\/p.|jq -cR "fromjson?|/sed -n "s\/^  - \/\/p"|jq -c "/' agi-mem;nh r6r2;UL u1 "words" >>$X;TAP $D/mut>/dev/null
ok "r7p-mutant-the-old-hand-parser-RED the first pipeline (every '  - ' line piped to jq) taps NOTHING on the real shape (chunks $(nchunks)): the lane above wants 1" '[ "$(nchunks)" = 0 ]'
nh r6r3;UL u1 "words" >>$X;o=$(echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=nosuchref PATH=$D/bin:$PATH sh $D/bin/agi-mem tap 2>&1;echo "rc=$?");a=$(env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=nosuchref PATH=$D/bin:$PATH sh $D/bin/agi-mem at 2>&1)
ok "r6p-unreadable-posts-md-is-named a trunk ref that cannot be read: tap = ONE [mem] warn and rc 0 ($(echo "$o"|tr '\n' '|')), at = 'mem: unread' (got '$a')" '[ "$(echo "$o"|grep -c "^\[mem\] warn")" = 1 ]&&echo "$o"|grep -q "^rc=0$"&&[ "$a" = "mem: unread" ]'
P=nobody;nh r6r4;UL u1 "words" >>$X;o=$(TAP;AT);P=;ok "r6p-no-row-for-the-post-is-quiet a post with no row in posts.md taps nothing and prints nothing (out '$o')" '[ -z "$o" ]&&[ ! -d $H/.mem ]'

nh r7r;UL u1 "words on the real file" >>$X;echo "{\"transcript_path\":\"$X\",\"session_id\":\"S1\"}"|env HOME=$H AGI_POST=belam AGI_ENGINE=$R0 AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh $D/bin/agi-mem tap >/dev/null 2>&1;S=$H/.mem/belam.git
ok "r7p-the-real-posts-md-reads-belam-full the cell read run ONCE on this tree's REAL posts.md (not the fixture): belam's row reads mem: full, so a tap writes its chunk (chunks $(nchunks)); a lane that only ever sees its own fixture proved nothing here once" '[ "$(nchunks)" = 1 ]'

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
# ---- R8 (council 18:56:18Z ROW 2, rides goal:g7.16.1.11.46.26): a question-prompt answer taps as an OWNER chunk, kind: answer, body = the question and the answer verbatim; aio R4': only when the asking tool_use is THIS post's own AskUserQuestion (main transcript, tied by tool_use_id), the result is no error and no origin but human, and no other tool's result ever becomes owner speech; sp: an answer that is one of the post's option labels carries `picked-from: post options` (the label is the POST's words, the owner's word is the choice), any other text `picked-from: owner text`; tier 0 never labels it, so a label holding `atom 2.5` acks nothing
# built on the documented AskUserQuestion result (toolUseResult.answers = {question: answer}); this box holds no real record of it, and the harness's tool_result records carry NO origin field (measured: 618 of 618 in this post's transcript), so "human" means: no origin that says otherwise
Q1='[{"question":"Which approach?","header":"Approach","multiSelect":false,"options":[{"label":"Alpha (Recommended)","description":"a"},{"label":"Beta","description":"b"}]}]'
QM='[{"question":"Which parts?","header":"Parts","multiSelect":true,"options":[{"label":"Alpha","description":"a"},{"label":"Beta","description":"b"}]}]'
AUQ(){ printf '{"type":"assistant","uuid":"%s","timestamp":"2026-10-24T10:00:06Z"%s,"message":{"content":[{"type":"tool_use","id":"%s","name":"%s","input":{"questions":%s}}]}}\n' "$1" "$5" "$2" "${4:-AskUserQuestion}" "$3";}
ANS(){ printf '{"type":"user","uuid":"%s","timestamp":"2026-10-24T10:00:07Z"%s,"message":{"content":[{"type":"tool_result","tool_use_id":"%s","content":"User has answered your questions"%s}]},"toolUseResult":{"questions":[],"answers":%s}}\n' "$1" "$5" "$2" "$4" "$3";}
CF(){ x=$(git -C $S grep -l -F -- "$1" refs/heads/mem|sed 's/^[^:]*://'|head -1);git -C $S show refs/heads/mem:$x;}
nans(){ git -C $S grep -l '^kind: answer$' refs/heads/mem -- mem ':!mem/retired' 2>/dev/null|wc -l|tr -d ' ';}
nh a1;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"Alpha (Recommended)"}'>>$X;TAP>/dev/null
ok "r8-a-picked-label-taps-as-an-owner-answer one chunk, speaker owner, kind: answer, picked-from: post options, body the question and the label verbatim ($(nans) answer chunks): $(CF 'Which approach?'|sed -n '3p;7p;9p;11,13p'|tr '\n' '|')" '[ "$(nans)" = 1 ]&&CF "Which approach?"|grep -qx "speaker: owner"&&CF "Which approach?"|grep -qx "picked-from: post options"&&CF "Which approach?"|grep -qx "Q: Which approach?"&&CF "Which approach?"|grep -qx "A: Alpha (Recommended)"&&CF "Which approach?"|grep -qx "atom: ?"'
nh a2;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"do the third thing instead"}'>>$X;TAP>/dev/null
ok "r8-other-free-text-is-the-owners-own an answer that is no option label carries picked-from: owner text ($(CF 'third thing'|grep '^picked-from')) and kind: answer" '[ "$(nans)" = 1 ]&&CF "third thing"|grep -qx "picked-from: owner text"'
nh a3;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"Alpha (Recommended)"}'>>$X;AUQ a3 tu2 "$QM">>$X;ANS a4 tu2 '{"Which parts?":"Alpha, Beta"}'>>$X;AUQ a5 tu3 "$QM">>$X;ANS a6 tu3 '{"Which parts?":"Alpha, plus my extra"}'>>$X;TAP>/dev/null
ok "r8-multiselect-is-a-pick-only-when-every-part-is-a-label 'Alpha, Beta' picks post options, 'Alpha, plus my extra' is the owner's text ($(CF 'Alpha, Beta'|grep '^picked-from') / $(CF 'plus my extra'|grep '^picked-from'))" 'CF "A: Alpha, Beta"|grep -qx "picked-from: post options"&&CF "plus my extra"|grep -qx "picked-from: owner text"'
nh a4;AUQ a1 tu1 "$QM">>$X;printf '{"type":"user","uuid":"a2","timestamp":"2026-10-24T10:00:07Z","message":{"content":[{"type":"tool_result","tool_use_id":"tu1","content":"x"}]},"toolUseResult":{"answers":{"Which parts?":"Alpha"},"questions":[{"question":"Which parts?"},{"question":"Second?"}]}}\n'>>$X;AUQ a3 tu2 '[{"question":"First?","options":[{"label":"x"}]},{"question":"Second?","options":[{"label":"y"}]}]'>>$X;ANS a4 tu2 '{"First?":"x","Second?":"typed"}'>>$X;TAP>/dev/null
ok "r8-one-chunk-per-question two questions in one result give two chunks with different ids ($(git -C $S grep -h '^id: c:' refs/heads/mem|sort -u|wc -l|tr -d ' ') ids), x picked from the post, 'typed' the owner's" '[ "$(nans)" = 3 ]&&CF "A: typed"|grep -qx "picked-from: owner text"&&CF "A: x"|grep -qx "picked-from: post options"'
# the guards (aio R4'): each reads NO chunk; each mutant reads one
nh g1;AUQ a1 tu1 '[]' Bash>>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}'>>$X;TAP>/dev/null;n1=$(nans)
nh g2;ANS a2 nope '{"Which approach?":"owner-looking words"}'>>$X;TAP>/dev/null;n2=$(nans)
nh g3;AUQ a1 tu1 "$Q1" AskUserQuestion ',"isSidechain":true'>>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}'>>$X;TAP>/dev/null;n3=$(nans)
nh g4;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}' ',"is_error":true'>>$X;TAP>/dev/null;n4=$(nans)
nh g5;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}' '' ',"origin":{"kind":"task-notification"}'>>$X;TAP>/dev/null;n5=$(nans)
ok "r8-guard-another-tools-result-is-never-owner-speech a Bash tool_use's result carrying 'answers' ($n1), a result tied to no tool_use ($n2), a subagent's AskUserQuestion ($n3), an errored result ($n4) and a result with a non-human origin ($n5) each tap NO answer chunk" '[ "$n1$n2$n3$n4$n5" = 00000 ]'
MUT 's/ and (\$aq\[.tool_use_id\]|type)=="array"//';nh m1;AUQ a1 tu1 '[]' Bash>>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}'>>$X;TAP $D/mut>/dev/null;m1=$(nans);nh m2;ANS a2 nope '{"Which approach?":"owner-looking words"}'>>$X;TAP $D/mut>/dev/null;m2=$(nans)
ok "r8-mutant-no-tool-use-tie-RED a tap that does not tie the result to the post's own AskUserQuestion by tool_use_id makes a chunk of a Bash result ($m1) and of an orphan ($m2): the lane wants 0 and 0" '[ "$m1" = 1 ]&&[ "$m2" = 1 ]'
MUT 's/select(.type=="assistant" and .isSidechain!=true)|.message.content\[\]?|select(.type=="tool_use"/select(.type=="assistant")|.message.content[]?|select(.type=="tool_use"/';nh m3;AUQ a1 tu1 "$Q1" AskUserQuestion ',"isSidechain":true'>>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}'>>$X;TAP $D/mut>/dev/null
ok "r8-mutant-subagent-ask-counts-RED a tap that reads a subagent's AskUserQuestion as the post's own makes a chunk ($(nans)): the lane wants 0" '[ "$(nans)" = 1 ]'
MUT 's/ and .is_error!=true//';nh m4;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}' ',"is_error":true'>>$X;TAP $D/mut>/dev/null
ok "r8-mutant-errored-result-counts-RED a tap that ignores is_error makes a chunk of an errored result ($(nans)): the lane wants 0" '[ "$(nans)" = 1 ]'
MUT 's/(.origin.kind\/\/"human")=="human" and (.toolUseResult.answers/(.toolUseResult.answers/';nh m5;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"owner-looking words"}' '' ',"origin":{"kind":"task-notification"}'>>$X;TAP $D/mut>/dev/null
ok "r8-mutant-any-origin-counts-RED a tap that ignores the origin makes a chunk of a task-notification result ($(nans)): the lane wants 0" '[ "$(nans)" = 1 ]'
# at counts the answer on both sides; a re-sweep adds nothing
nh a5;UL u1 "go on">>$X;AUQ a1 tu1 "$Q1">>$X;ANS a2 tu1 '{"Which approach?":"Beta"}'>>$X;TAP>/dev/null;c1=$(nchunks);rm -f $S/cursor-S1;TAP>/dev/null
ok "r8-at-counts-the-answer-and-a-resweep-adds-nothing at: '$(AT|head -1)' (want 2/2, the typed line and the answer); chunks before/after a re-sweep from a cleared cursor: $c1/$(nchunks)" '[ "$(AT|head -1)" = "mem: tapped 2/2" ]&&[ "$c1" = "$(nchunks)" ]'
# M7 never reads a post-written label as an owner ack: a picked label holding `atom 2.5` stays atom: ? and acks no row
G8=$D/g8;mkdir -p $G8;printf '# card\n\n## §7 ATOMS\n\n| # | atom (verbatim slice) | source | state | lap |\n|---|---|---|---|---|\n| 2.5 | "pick one" | src:doc | target:y | lap5 |\n\n## §8 after\n'>$G8/p.md
LB8(){ env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=HEAD AGI_ATOM_CARD=$G8/p.md PATH=$D/bin:$PATH sh ${1:-$D/bin/agi-mem} label 2>&1;}
Q5='[{"question":"Which approach?","header":"Approach","multiSelect":false,"options":[{"label":"Ship atom 2.5","description":"a"},{"label":"Beta","description":"b"}]}]'
nh a6;AUQ a1 tu1 "$Q5">>$X;ANS a2 tu1 '{"Which approach?":"Ship atom 2.5"}'>>$X;AL p1 "Noted.">>$X;TAP>/dev/null;LB8>/dev/null
ok "r8-a-picked-label-holding-atom-2.5-acks-nothing the answer chunk keeps atom: ? and kind: answer after label (got '$(CF 'Ship atom 2.5'|grep -E '^(atom|kind):'|tr '\n' ' ')'): the post's option text is not the owner's ack" 'CF "Ship atom 2.5"|grep -qx "atom: ?"&&CF "Ship atom 2.5"|grep -qx "kind: answer"'
MUT 's/\[ "\$p" = post \]||{ \[ "\$R" = redo \]&&{ y=\${x##\*c-};echo "label --redo: c:\${y%.md} is an owner chunk";miss=1;};continue;};//';LB8 $D/mut>/dev/null
ok "r8-mutant-label-reads-the-owner-chunk-RED a labeler that also labels owner chunks gives the answer chunk 'atom: $(CF 'Ship atom 2.5'|sed -n 's/^atom: //p')' (an ack on 2.5 from the POST's own option text): the lane wants ?" '[ "$(CF "Ship atom 2.5"|sed -n "s/^atom: //p")" = 2.5 ]'
echo "mem-tap: $f FAIL";exit $f
