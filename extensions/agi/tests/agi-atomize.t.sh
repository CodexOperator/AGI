#!/bin/sh
# agi-atomize.t.sh [ROOT]: goal:g7.16.1.11.46.3 (M2) falsifier 1+2 against a LOCAL STUB model endpoint (a python3 http.server answering /v1/chat/completions from scripted replies; the REAL agi-infer piece talks to it): fixtures ask / fyi / report / quoted-only / re-read give the expected rows (fyi 0, quoted-only 0 calls, re-read +0 calls); a paraphrasing reply is refused by agi-atom add; an overlapping-slices reply is refused; a `?` target escalates ONCE to the second model; mutant m (no marker ref) reads RED on the re-read lane; negative: the box piece's body names no atomiz*.
# sh + git + jq + curl + python3 on a scratch repo with throwaway ssh keys; no network beyond 127.0.0.1, no root, 0 USD. ROOT = the tree whose engine-post.md / engine-wrap.md carry the pieces; PIECE=<file> tests a candidate agi-atomize. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'kill $SV 2>/dev/null;rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_ATOM_CARD AGI_ATOM_COMMIT AGI_INFER_SCHEMA AGI_INFER_KEY
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;sect agi-atom engine-post.md>$D/bin/agi-atom;sect agi-meter engine-post.md>$D/bin/agi-meter;sect agi-mem engine-post.md>$D/bin/agi-mem;sect agi-infer engine-wrap.md>$D/bin/agi-infer;sect box engine-post.md>$D/bin/box;PC=${PIECE:-$D/bin/agi-atomize};[ -n "$PIECE" ]||sect agi-atomize engine-post.md>$PC;chmod +x $D/bin/*
for x in agi-atom agi-infer;do [ -s $D/bin/$x ]||{ echo "FAIL inputs: no $x piece";exit 99;};done;[ -s "$PC" ]||{ echo "FAIL inputs: no agi-atomize piece";exit 99;}
printf '#!/bin/sh\ncd "$AGI_T"&&git add -A -- "$@"&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm "stub agi-at: $*"\n' >$D/stub;chmod +x $D/stub
# the stub endpoint: reply n of a run = file $D/q/r<n> (its text is the assistant message); every request is logged (model, prompt) to $D/q/log<n>
mkdir $D/q;cat >$D/stub.py<<'PY'
import http.server,json,sys,os,time
Q=sys.argv[1]
def reset():
    for n in os.listdir(Q):
        if n.startswith(("r","log","calls")) and n!="port": os.unlink(Q+"/"+n)
class H(http.server.BaseHTTPRequestHandler):
    n=0
    def log_message(self,*a): pass
    def do_POST(self):
        b=json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        H.n=int(open(Q+"/calls").read()) if os.path.exists(Q+"/calls") else 0
        if os.path.exists(Q+"/sleep"): time.sleep(float(open(Q+"/sleep").read()))
        H.n+=1;open(Q+"/log%d"%H.n,"w").write(json.dumps({"model":b["model"],"prompt":b["messages"][0]["content"]}))
        open(Q+"/calls","w").write(str(H.n))
        r=Q+"/r%d"%H.n
        if not os.path.exists(r): self.send_response(500);self.end_headers();return
        try:   # a client killed by its timeout (the P-a row) has gone: nothing to answer
            self.send_response(200);self.send_header("Content-Type","text/event-stream");self.end_headers()
            self.wfile.write(("data: "+json.dumps({"choices":[{"delta":{"content":open(r).read()}}]})+"\n\ndata: [DONE]\n\n").encode())
        except BrokenPipeError: pass
s=http.server.HTTPServer(("127.0.0.1",0),H);open(Q+"/port","w").write(str(s.server_port));s.serve_forever()
PY
python3 -I $D/stub.py $D/q & SV=$!;i=0;while [ ! -s $D/q/port ]&&[ $i -lt 50 ];do sleep 0.1;i=$((i+1));done;[ -s $D/q/port ]||{ echo "FAIL inputs: the stub endpoint did not start";exit 99;}
export AGI_INFER_URL=http://127.0.0.1:$(cat $D/q/port)/v1
# keys + a repo: sender sm signs, recipient p reads; a second key (evil) signs a forged "sm" commit
mkdir $D/k;: >$D/signers;for u in sm evil p far;do ssh-keygen -q -t ed25519 -N '' -f $D/k/$u -C $u>/dev/null;done;for u in sm far;do echo "$u@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/$u.pub)">>$D/signers;done
SG(){ k=$1;shift;env GIT_AUTHOR_NAME=$k GIT_AUTHOR_EMAIL=sm@agi GIT_COMMITTER_NAME=$k GIT_COMMITTER_EMAIL=sm@agi git -c user.signingkey=$D/k/$k -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$D/signers "$@";}
mk(){ T=$D/w$1/t;for x in $D/q/r* $D/q/log* $D/q/calls;do [ -e "$x" ]&&rm -f "$x";done;mkdir -p $T/.agi/nodes/goal $T/.agi/sessions/quorum;cd $T;git init -q .;git config core.hooksPath /dev/null;git config gpg.format ssh;git config gpg.ssh.allowedSignersFile $D/signers
 printf -- '---\nid: goal:g1.2\nstatus: active\n---\n# g\n## Agent Notes\nAssigned to **p**.\n' >.agi/nodes/goal/g1.2.md;printf '# card\n\n## §0 x\nhi\n' >.agi/sessions/quorum/p.md
 # the matrix box ok reads (P-c): sm -> p adjacent; far sits 2 levels under p (off the matrix)
 mkdir -p .agi/nodes/.geometry;printf -- '---\nid: config:posts\nposts:\n  - {"name": "sm", "parent": "owner", "harness": "claude"}\n  - {"name": "p", "parent": "sm", "harness": "claude"}\n  - {"name": "x", "parent": "p", "harness": "claude"}\n  - {"name": "far", "parent": "x", "harness": "claude"}\n---\n'>.agi/nodes/.geometry/posts.md
 git add -A;git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm base;C=$T/.agi/sessions/quorum/p.md
 # P-b: the atoms go onto posts/p's committed card; ~/t is a DETACHED view of that tip, as on a post; p signs its commit
 git update-ref refs/heads/posts/p HEAD;git checkout -q --detach posts/p;git config user.name p;git config user.email p@agi;git config user.signingkey $D/k/p;}
# msg KEY BODY [FROM]: a signed message onto refs/box/FROM/p (FROM default sm), on top of the last one; DT = its date (@epoch)
msg(){ e=$(git hash-object -w -t tree /dev/null);q=$(git rev-parse -q --verify refs/box/${3:-sm}/p);c=$(printf '%s\n' "$2"|{ [ -z "$DT" ]||export GIT_COMMITTER_DATE=$DT;SG $1 commit-tree -S ${q:+-p $q} $e;})&&git update-ref refs/box/${3:-sm}/p $c;SHA=$c;}
reply(){ printf '%s' "$2">$D/q/r$1;}
calls(){ cat $D/q/calls 2>/dev/null||echo 0;}
AT(){ (cd $T;env AGI_T=$T AGI_POST=p AGI_LAP=5 HOME=$D PATH=$D/bin:$PATH AGI_ATOMIZE_AGE=${AGE:-99999999} AGI_TRUNK=${TR:-HEAD} ${TO:+timeout $TO} sh ${1:-$PC}) 2>$D/err;}
# rp OUT: a mutant of the piece, OUT = PC with ONE exact text replaced; stdin = the old text, a line @@, the new text (both verbatim)
rp(){ python3 -I -c 'import sys;a,b=sys.stdin.read().rstrip("\n").split("\n@@\n");s=open(sys.argv[1]).read();assert s.count(a)==1,a;open(sys.argv[2],"w").write(s.replace(a,b))' $PC $1;}
natom(){ git for-each-ref refs/atomized/p|wc -l;}
rows(){ grep -c '^| a[0-9]* | ' $C;}
marked(){ git rev-parse -q --verify refs/atomized/p/$SHA>/dev/null;}
M1='Please build the widget now. Also fix the red test. Thanks!'
# --- ask: Haiku cuts two atoms with real targets, one call
mk a;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"},{"slice":"fix the red test","target":"g1.2"}]}';AT
ok "ask-two-rows an ask yields its two atoms as §7 rows with src:<the commit> and the real goal as target (rows $(rows))" '[ $(rows) = 2 ]&&grep -qF "| a1 | \"build the widget now\" | src:$SHA | target:goal:g1.2 |" $C'
ok "ask-one-call-first-model the first model is claude-haiku-5-5 and there was ONE call (calls $(calls), model $(jq -r .model $D/q/log1))" '[ "$(calls)" = 1 ]&&[ "$(jq -r .model $D/q/log1)" = claude-haiku-5-5 ]'
ok "ask-prompt-carries-leaf-ids the model is handed the recipient's leaf ids (g1.2) and the message" 'jq -r .prompt $D/q/log1|grep -q "g1.2"&&jq -r .prompt $D/q/log1|grep -qF "$M1"'
ok "ask-card-committed the atoms went onto posts/p's card in ONE signed commit, ~/t's detached view followed it, the tree is clean, no status (a clean run)" '[ "$(git rev-list --count posts/p)" = 2 ]&&[ "$(git rev-parse HEAD)" = "$(git rev-parse posts/p)" ]&&git show posts/p:.agi/sessions/quorum/p.md|grep -qF "| a1 | \"build the widget now\"" &&[ -n "$(git log -1 --format=%GG posts/p)" ]&&[ -z "$(git status --porcelain)" ]&&[ ! -e $D/.atomize.status ]'
ok "ask-marker-ref the commit carries its marker refs/atomized/p/<sha>" 'marked'
ok "ask-stamps-the-pass a run ends by stamping ~/.atomize.last (agi-atom derive check measures owner chunks still ? against it; got '$(cat $D/.atomize.last 2>/dev/null)')" 'grep -qE "^20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z$" $D/.atomize.last'
c1=$(calls);AT;ok "re-read-plus-zero a second wake reads nothing again: calls $c1 -> $(calls), rows $(rows)" '[ "$(calls)" = "$c1" ]&&[ $(rows) = 2 ]'
# --- fyi / report: 0 atoms, marked, never re-read
mk b;msg sm 'Just so you know: the build is green.';reply 1 '{"kind":"fyi","atoms":[{"slice":"the build is green","target":"?"}]}';AT;c1=$(calls);AT
ok "fyi-zero-rows an fyi gives 0 rows even when the model offered one, is marked, and the re-read costs 0 calls (rows $(rows), calls $c1 -> $(calls))" '[ $(rows) = 0 ]&&marked&&[ "$(calls)" = "$c1" ]'
mk c;msg sm 'Numbers: 12 landed, 3 red.';reply 1 '{"kind":"report","atoms":[]}';AT
ok "report-zero-rows a report gives 0 rows and is marked (rows $(rows))" '[ $(rows) = 0 ]&&marked'
# --- quoted-only: the model is never called; > lines never reach it
mk d;msg sm '> Please build the widget
> and the gadget';AT
ok "quoted-only-no-call a message of only > lines makes 0 calls, 0 rows, and is marked (calls $(calls))" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&marked'
mk e;msg sm '> secret quoted line
Please build the widget now.';reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"?"}]}';reply 2 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';AT
ok "quote-excluded the > line is not in the prompt (prompt has it: $(jq -r .prompt $D/q/log1|grep -c "secret quoted"))" '[ "$(jq -r .prompt $D/q/log1|grep -c "secret quoted")" = 0 ]'
ok "question-target-escalates-once a ? target from Haiku: ONE call to the second model (claude-sonnet-5-5), its result used (calls $(calls))" '[ "$(calls)" = 2 ]&&[ "$(jq -r .model $D/q/log2)" = claude-sonnet-5-5 ]&&grep -qF "| target:goal:g1.2 |" $C'
# --- refusals: nothing marked, nothing written, the next wake retries
mk f;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the whole widget right now","target":"g1.2"}]}';AT;c1=$(calls)
ok "paraphrase-refused a slice that is not a substring of the message is refused: 0 rows, no marker (rows $(rows))" '[ $(rows) = 0 ]&&! marked&&grep -q "atom was refused\|no usable reply" $D/err'
reply 2 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';AT
ok "refusal-retried-next-wake the next wake asks again (calls $c1 -> $(calls)) and lands the row (rows $(rows))" '[ "$(calls)" = $((c1+1)) ]&&[ $(rows) = 1 ]'
mk g;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget","target":"g1.2"},{"slice":"the widget now","target":"g1.2"}]}';AT
ok "overlap-refused two slices that overlap in the message are refused: 0 rows, no marker (rows $(rows))" '[ $(rows) = 0 ]&&! marked'
mk h;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[]}';AT
ok "ask-with-no-atoms-refused an ask with 0 atoms is refused, not marked (rows $(rows))" '[ $(rows) = 0 ]&&! marked'
mk i;msg sm "$M1";reply 1 'this is not json';AT
ok "garbage-reply-refused a reply that is not JSON writes nothing and marks nothing" '[ $(rows) = 0 ]&&! marked'
mk j;msg evil "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';AT
ok "forged-signature-skipped a commit not signed by its sender is never read, is NOT marked (T2: box read holds it neither), counted and named (calls $(calls), rows $(rows))" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&! marked&&grep -q "not signed by sm, no atom (not marked)" $D/err&&grep -q "unsigned=1" $D/err'
rp $D/mus<<'X'
us=$((us+1));continue;
@@
us=$((us+1));git update-ref $M/$c $c "";continue;
X
mk jm;msg evil "$M1";AT $D/mus
ok "m-unsigned-marked-RED the mutant with the unsigned mark restored marks the forged commit: the forged lane (! marked) catches it" 'marked&&! cmp -s $D/mus $PC'
mk k;msg sm '[town] up 0123456789012345678901234567890123456789';AT
ok "town-line-skipped belam's [town] line is marked and never sent to a model (calls $(calls))" '[ "$(calls)" = 0 ]&&marked'
# --- P-b: the atoms go onto posts/p's COMMITTED card; an uncommitted edit of the working card stays uncommitted, untouched, and is named
CP=.agi/sessions/quorum/p.md;mk pb;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';echo 'MY UNCOMMITTED EDIT'>>$C;AT
ok "pb-card-edit-kept the commit carries the atom only (posts/p's card: the atom, not the edit); the working card keeps the edit and gets no atom; the status names it (card=kept)" 'git show posts/p:$CP|grep -qF "| a1 | \"build the widget now\""&&! git show posts/p:$CP|grep -q "MY UNCOMMITTED EDIT"&&grep -q "MY UNCOMMITTED EDIT" $C&&[ $(rows) = 0 ]&&grep -q "card=kept" $D/.atomize.status&&marked'
sed 's/AGI_ATOM_CARD=\$W\/card agi-atom add/agi-atom add/' $PC>$D/mpb;mk pm;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';echo 'MY UNCOMMITTED EDIT'>>$C;AT $D/mpb
ok "m-working-card-RED an atomizer that writes the WORKING card commits posts/p's card WITHOUT the atom (and puts it in the working file): the pb lane catches it" '! git show posts/p:$CP|grep -q "| a1 |"&&[ $(rows) = 1 ]&&! cmp -s $D/mpb $PC'
# a lost CAS marks nothing: posts/p moves between the read and the commit
printf '#!/bin/sh\nagi-infer "$@";r=$?;cd "$AGI_T";c=$(git -c user.name=r -c user.email=r@r commit-tree -p refs/heads/posts/p refs/heads/posts/p^{tree} -m race </dev/null);git update-ref refs/heads/posts/p $c;exit $r\n'>$D/race;chmod +x $D/race
mk pc;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';export AGI_ATOMIZE_INFER=$D/race;AT;unset AGI_ATOMIZE_INFER
ok "pb-lost-cas-marks-nothing posts/p moved under the run: nothing marked, posts/p's card has no atom, [raced] named in the log" '! marked&&grep -qF "[raced]" $D/err&&! git show posts/p:$CP|grep -q "| a1 |"'
# T1: the branch CAS and the markers are ONE ref transaction: a marker blocked by a D/F ref leaves the branch unmoved and nothing marked, named
mk pt;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';git update-ref refs/atomized/p/$SHA/x $SHA;b0=$(git rev-parse posts/p);AT
ok "pb-one-transaction a marker blocked by a D/F ref (refs/atomized/p/<sha>/x): posts/p unmoved, no marker, the failed transaction named, not [raced]" '[ "$(git rev-parse posts/p)" = $b0 ]&&! marked&&grep -q "the ref transaction failed" $D/err&&! grep -qF "[raced]" $D/err'
rp $D/mpt<<'X'
{ echo start;echo "update $B $nc $t";while read -r h;do echo "create $M/$h $h";done<$W/mk;echo commit;}|git update-ref --stdin >/dev/null 2>$W/ue
@@
{ git update-ref $B $nc $t&&while read -r h;do git update-ref $M/$h $h "";done<$W/mk;} 2>$W/ue
X
mk pu;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';git update-ref refs/atomized/p/$SHA/x $SHA;b0=$(git rev-parse posts/p);AT $D/mpt
ok "m-two-call-RED the two-call form (branch update-ref, then a marker loop) moves posts/p with an UNMARKED commit: the one-transaction lane catches it" '[ "$(git rev-parse posts/p)" != $b0 ]&&! marked&&! cmp -s $D/mpt $PC'
# T7: a failed step that is not a race names itself; [raced] only when the branch did move
mk pv;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';git config user.signingkey $D/k/no-such-key;b0=$(git rev-parse posts/p);AT
ok "pb-signing-failure-named a signing failure: commit-tree -S failed rc <n> named, not [raced]; posts/p unmoved, nothing marked" 'grep -q "commit-tree -S failed rc [1-9]" $D/err&&! grep -qF "[raced]" $D/err&&[ "$(git rev-parse posts/p)" = $b0 ]&&! marked'
rp $D/mpv<<'X'
e="commit-tree -S failed rc $x"
@@
e="[raced] $B moved under the run"
X
mk pw;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';git config user.signingkey $D/k/no-such-key;AT $D/mpv
ok "m-one-message-for-all-RED the mutant naming every failure [raced] reads a signing failure as a race: the signing lane catches it" 'grep -qF "[raced]" $D/err&&! cmp -s $D/mpv $PC'
# T4: a run killed at its bound keeps what it committed (ONE commit per message); the next wake continues; a soft deadline counts the rest deferred
mk px;for i in 1 2 3 4 5 6 7 8;do msg sm "message $i: build the widget now";done;i=1;while [ $i -le 30 ];do reply $i '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';i=$((i+1));done;echo 1 >$D/q/sleep;TO=4;AT;rc=$?;TO=;rm -f $D/q/sleep;n1=$(natom);h1=$(git rev-parse HEAD);p1=$(git rev-parse posts/p);r1=$(rows);sleep 2;AT;n2=$(natom)
ok "pa-killed-run-keeps-progress 8 asks, 1 s per request, killed at 4 s (rc $rc): the first wake committed and marked $n1 (>= 1, < 8), ~/t followed each commit (working card $r1 rows == $n1 marked), the next wake finished: $n2 marked, posts/p's card and the working card hold 8 rows, HEAD == posts/p" '[ $rc = 124 ]&&[ $n1 -ge 1 ]&&[ $n1 -lt 8 ]&&[ $h1 = $p1 ]&&[ $r1 = $n1 ]&&[ $n2 = 8 ]&&[ "$(git rev-parse HEAD)" = "$(git rev-parse posts/p)" ]&&[ $(rows) = 8 ]&&[ "$(git show posts/p:$CP|grep -c "^| a[0-9]* | ")" = 8 ]'
rp $D/mpx<<'X'
pk=$((pk+k));fl||break 2;
@@
pk=$((pk+k));
X
mk py;for i in 1 2 3 4 5 6 7 8;do msg sm "message $i: build the widget now";done;i=1;while [ $i -le 30 ];do reply $i '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';i=$((i+1));done;echo 1 >$D/q/sleep;TO=4;AT $D/mpx;rc=$?;TO=;rm -f $D/q/sleep;n1=$(natom);sleep 2
ok "m-commit-after-both-loops-RED the mutant committing only after both loops is killed (rc $rc) with $n1 marked (0): the killed-run lane catches it" '[ $rc = 124 ]&&[ $n1 = 0 ]&&! cmp -s $D/mpx $PC'
rp $D/mpf<<'X'
if [ -z "$cs" ]&&[ "$(git rev-parse -q --verify HEAD)" = $t ]
@@
if false&&[ "$(git rev-parse -q --verify HEAD)" = $t ]
X
mk pq;for i in 1 2 3 4 5 6 7 8;do msg sm "message $i: build the widget now";done;i=1;while [ $i -le 30 ];do reply $i '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';i=$((i+1));done;echo 1 >$D/q/sleep;TO=4;AT $D/mpf;TO=;rm -f $D/q/sleep;n1=$(natom);sleep 2
ok "m-no-follow-per-commit-RED the mutant without the per-commit follow leaves ~/t at the run's start tip after the kill ($n1 marked, working card $(rows) rows): the killed-run lane catches it" '[ $n1 -ge 1 ]&&[ "$(git rev-parse HEAD)" != "$(git rev-parse posts/p)" ]&&[ $(rows) = 0 ]&&! cmp -s $D/mpf $PC'
mk pz;for i in 1 2 3;do msg sm "message $i: build the widget now";done;AGI_ATOMIZE_SOFT=0 AT;unset AGI_ATOMIZE_SOFT
ok "pa-deferred-named a soft deadline already passed: 0 requests, nothing marked, deferred=3 in the run line and the status" '[ "$(calls)" = 0 ]&&[ $(natom) = 0 ]&&grep -q "deferred=3" $D/err&&grep -q "deferred=3" $D/.atomize.status'
rm -f $D/.atomize.status
# --- P-c: the sender passes box's own matrix through ONE exposed check (box ok FROM), never a copy
mk pd;msg far "$M1" far;reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';AT
ok "pc-off-matrix-no-atom a signed message from far (2 levels under p: off box's matrix) makes 0 calls and 0 rows, is NOT marked (T2), counted and named" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&! marked&&grep -q "far -> p is off the matrix" $D/err&&grep -q "off-matrix=1" $D/err'
# T2: box ok cannot tell an unread posts.md from a no: sm (ON the matrix) read with AGI_TRUNK at a missing ref is off-matrix=1, never marked, so the next readable wake reads it
mk pg;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';TR=refs/heads/no-such-ref;AT;TR=
ok "pc-unread-posts-md-not-marked an on-matrix sender read while posts.md is unreadable (AGI_TRUNK at a missing ref): 0 calls, NOT marked, off-matrix=1 named" '[ "$(calls)" = 0 ]&&! marked&&grep -q "off-matrix=1" $D/err'
rp $D/mom<<'X'
om=$((om+1));continue;
@@
om=$((om+1));git update-ref $M/$c $c "";continue;
X
mk ph;msg sm "$M1";TR=refs/heads/no-such-ref;AT $D/mom;TR=
ok "m-off-matrix-marked-RED the mutant with the off-matrix mark restored marks the unread-posts.md message for good: the unread lane catches it" 'marked&&! cmp -s $D/mom $PC'
sed 's/box ok \$f||/true||/' $PC>$D/mpc;mk pe;msg far "$M1" far;reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';AT $D/mpc
ok "m-box-ok-dropped-RED an atomizer without the box ok check sends far's message to the model (calls $(calls); the pc lane wants 0)" '[ "$(calls)" = 1 ]&&! cmp -s $D/mpc $PC'
# --- P-e: a message past the age bound is COUNTED, never silent
mk pf;DT=@$(($(date +%s)-18000));msg sm "$M1";DT=;AGE=3600;AT;AGE=
ok "pe-skipped-age-counted a message past the age bound makes 0 calls, is not marked, the run line counts it (skipped-age=1) and NO status is written (T5: aged mail only)" '[ "$(calls)" = 0 ]&&! marked&&grep -q "skipped-age=1" $D/err&&[ ! -e $D/.atomize.status ]'
rp $D/mpe<<'X'
[ $rf != 0 ]||[ $df != 0 ]
@@
[ $rf != 0 ]||[ $sa != 0 ]||[ $df != 0 ]
X
mk pi;DT=@$(($(date +%s)-18000));msg sm "$M1";DT=;AGE=3600;AT $D/mpe;AGE=
ok "m-skipped-age-status-RED the mutant with skipped-age back in the status trigger writes a status for aged mail only: the pe lane catches it" '[ -e $D/.atomize.status ]&&! cmp -s $D/mpe $PC'
rm -f $D/.atomize.status
# T5 + sp 16:43:33Z: the age window is ONE rev-list --max-age per box ref, skipped-age its count: 30 aged + 1 fresh read in a bounded number of git calls
RG=$(command -v git);mkdir -p $D/gw;printf '#!/bin/sh\necho x>>%s/gcalls\nexec %s "$@"\n' $D $RG>$D/gw/git;chmod +x $D/gw/git
mk pj;DT=@$(($(date +%s)-18000));i=0;while [ $i -lt 30 ];do msg sm "old $i";i=$((i+1));done;DT=;msg sm 'Just so you know: fresh.';reply 1 '{"kind":"fyi","atoms":[]}';AGE=3600;OP=$PATH;PATH=$D/gw:$PATH;: >$D/gcalls;AT;PATH=$OP;AGE=;g1=$(wc -l <$D/gcalls)
ok "pe-age-window-one-call 30 aged + 1 fresh: read=1 skipped-age=30, the fresh one marked, in $g1 git calls (< 30: never a per-commit walk of the aged)" 'grep -q "read=1 " $D/err&&grep -q "skipped-age=30" $D/err&&marked&&[ $g1 -lt 30 ]'
rp $D/mpw<<'X'
 ag=$(($(date +%s)-${AGI_ATOMIZE_AGE:-86400}));ma=--since-as-filter=@$ag;sa=$((sa+$(git rev-list --min-age=$((ag-1)) $r|grep -cvxF -f $W/am)))
 for c in $(git rev-list --reverse $ma $r);do git rev-parse -q --verify $M/$c>/dev/null&&continue;
@@
 for c in $(git rev-list --reverse $r);do git rev-parse -q --verify $M/$c>/dev/null&&continue;[ $(($(date +%s)-$(git log -1 --format=%ct $c))) -le ${AGI_ATOMIZE_AGE:-86400} ]||{ sa=$((sa+1));continue;};
X
mk pk;DT=@$(($(date +%s)-18000));i=0;while [ $i -lt 30 ];do msg sm "old $i";i=$((i+1));done;DT=;msg sm 'Just so you know: fresh.';reply 1 '{"kind":"fyi","atoms":[]}';AGE=3600;OP=$PATH;PATH=$D/gw:$PATH;: >$D/gcalls;AT $D/mpw;PATH=$OP;AGE=;g2=$(wc -l <$D/gcalls)
ok "m-per-commit-age-walk-RED the mutant with the per-commit age walk back makes $g2 git calls for the same box (>= 60): the age-window lane catches it" '[ $g2 -ge 60 ]&&! cmp -s $D/mpw $PC'
# T5(b) as alive 17:16:15Z: skipped-age counts the aged commits with NO marker: one aged marked + one aged unmarked -> skipped-age=1
mk pl;DT=@$(($(date +%s)-18000));msg sm "old marked";git update-ref refs/atomized/p/$SHA $SHA;msg sm "old unmarked";DT=;AGE=3600;AT;AGE=
ok "pe-skipped-age-unmarked-only one aged marked + one aged unmarked: skipped-age=1 (an atomized message never reads as skipped)" 'grep -q "skipped-age=1 " $D/err'
rp $D/mpl<<'X'
sa=$((sa+$(git rev-list --min-age=$((ag-1)) $r|grep -cvxF -f $W/am)))
@@
sa=$((sa+$(git rev-list --count $r)-$(git rev-list --count $ma $r)))
X
mk pm2;DT=@$(($(date +%s)-18000));msg sm "old marked";git update-ref refs/atomized/p/$SHA $SHA;msg sm "old unmarked";DT=;AGE=3600;AT $D/mpl;AGE=
ok "m-whole-minus-window-RED the mutant counting whole minus window reads the marked one too (skipped-age=2): the unmarked-only lane catches it" 'grep -q "skipped-age=2 " $D/err&&! cmp -s $D/mpl $PC'
# --- the transport term (alive [decision] 14:17:17Z 10-31, D2): a dead endpoint ends the RUN at the first message
mk tq;for i in 1 2 3 4 5;do msg sm "message $i: build the widget now";done;rm -f $D/.atomize.last;AT;rc=$?
ok "transport-one-request a dead endpoint (500, no reply) and 5 unmarked messages: ONE request (calls $(calls)), rc 3, no marker at all (natom 0, crumb iii), no stamp, the status names the transport" '[ "$(calls)" = 1 ]&&[ $rc = 3 ]&&[ $(natom) = 0 ]&&[ ! -e $D/.atomize.last ]&&grep -q "transport=" $D/.atomize.status&&! grep -q "transport=none" $D/.atomize.status'
sed 's/\[ \$x = 0 \]||\[ -s \$W\/r \]||{ tp="\$c (rc \$x)";return 1;};//' $PC>$D/mtq;mk tm;for i in 1 2 3 4 5;do msg sm "message $i: build the widget now";done;AT $D/mtq
ok "m-transport-check-dropped-RED without the transport check every message asks the dead endpoint (calls $(calls); the transport lane wants 1)" '[ "$(calls)" = 5 ]&&! cmp -s $D/mtq $PC'
rm -f $D/.atomize.status
# --- mutant m: no marker ref -> the re-read lane reads it again
M=$D/m;sed 's/elif \[ \$k = 0 \];then git update-ref \$M\/\$c \$c ""/elif [ $k = 0 ];then :/' $PC>$M;mk l;msg sm 'Just so you know: all is well.';reply 1 '{"kind":"fyi","atoms":[]}';reply 2 '{"kind":"fyi","atoms":[]}';reply 3 '{"kind":"fyi","atoms":[]}'
AT $M;AT $M
ok "m-no-marker-RED the mutant without the marker ref read the same fyi twice (calls $(calls), want 2): the re-read lane catches it" '[ "$(calls)" = 2 ]&&! cmp -s $M $PC'
rm -f $D/.atomize.last;M2=$D/ms;sed '/^date -u +%FT%TZ>/d' $PC>$M2;mk s;msg sm 'Numbers: 1 landed.';reply 1 '{"kind":"report","atoms":[]}';AT $M2
ok "m-no-stamp-RED the mutant without the stamp line leaves no ~/.atomize.last: the stamp lane catches it" '[ ! -e $D/.atomize.last ]&&! cmp -s $M2 $PC'
# --- the WAKE-PATH CALLER (the remainder of .46.3): agi-meter, the UserPromptSubmit hook, runs `agi-atomize wake` on the prompt "mail: box read"
# the meter runs agi-mem tap from PATH: the TREE's agi-mem (not an installed one: SM's finding 23:1xZ 10-25) against a tiny repo whose `trunk` ref holds a posts.md with no mem row for p, so the tap is silent by its own gate
mkdir -p $D/me/.agi/nodes/.geometry;printf -- '---\nid: config:posts\nposts:\n  - {"name": "p", "mem": "none"}\n---\n'>$D/me/.agi/nodes/.geometry/posts.md;(cd $D/me&&git init -q .&&git config core.hooksPath /dev/null&&git add -A&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm posts&&git update-ref refs/heads/trunk HEAD)>/dev/null 2>&1;[ -s $D/bin/agi-mem ]||{ echo "FAIL inputs: no agi-mem piece";exit 99;}
[ -n "$PIECE" ]&&cp $PC $D/bin/agi-atomize;[ -s $D/bin/agi-meter ]||{ echo "FAIL inputs: no agi-meter piece";exit 99;};chmod +x $D/bin/*
# cred CREDITS: the secrets cell; AL = atomize_live (default true, so the credits rows reach agi-atomize; AL=- writes no atomize_live line)
cred(){ mkdir -p .agi/nodes/.geometry;if [ -n "$1" ];then printf 'credits_live: %s\ndoppler: x\n' "$1">.agi/nodes/.geometry/secrets.md;else printf 'doppler: x\n'>.agi/nodes/.geometry/secrets.md;fi;[ "${AL-true}" = - ]||echo "atomize_live: ${AL-true}">>.agi/nodes/.geometry/secrets.md;git add -A;git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm cred;git update-ref refs/heads/trunk HEAD;git update-ref refs/heads/posts/p HEAD;}
WK(){ printf '%s' "${1:-{\"prompt\":\"mail: box read\"\}}" | (cd $T;env AGI_T=$T AGI_POST=p AGI_LAP=5 HOME=$D PATH=$WKP$D/bin:$PATH AGI_ATOMIZE_AGE=99999999 AGI_ATOMIZE_TIMEOUT=${TO:-45} AGI_TRUNK=trunk AGI_ENGINE=$D/me sh ${2:-$D/bin/agi-meter}) 2>$D/err;flock -w 60 $D/.atomize.lock true 2>/dev/null;}   # the wake runs in the BACKGROUND now (the hook returns in seconds): wait for it by the flock its child holds
WP='{"prompt":"mail: box read"}';WKP=;rm -f $D/.atomize.log
mk m;cred false;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';o=$(WK "$WP")
ok "wake-credits-false-stdout-empty-skip-logged with credits_live false the hook's STDOUT is EMPTY (it enters the post's context), the named skip line goes to ~/.atomize.log, 0 calls, 0 rows, nothing marked (out: '$o', log: $(tail -1 $D/.atomize.log 2>/dev/null|cut -d' ' -f2-), calls $(calls))" '[ -z "$o" ]&&grep -qF "[atomize] skipped: credits_live is false, no model call" $D/.atomize.log&&[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&! marked'
mk n;cred "";msg sm "$M1";o=$(WK "$WP")
ok "wake-credits-unreadable-logged a secrets cell with no credits_live is named in the log too, stdout empty (out: '$o')" '[ -z "$o" ]&&grep -qF "[atomize] skipped: credits_live is unreadable, no model call" $D/.atomize.log&&[ "$(calls)" = 0 ]'
# mutant a: the skip line back on stdout -> the stdout-empty lane is RED
sed 's|>>\$HOME/.atomize.log;exit 0|;exit 0|' $PC>$D/ma;chmod +x $D/ma;mkdir -p $D/bina;cp $D/ma $D/bina/agi-atomize;sed 's|)>>~/.atomize.log 2>&1 </dev/null &|);|' $D/bin/agi-meter>$D/mfg;mk r;cred false;msg sm "$M1";WKP=$D/bina: o=$(WK "$WP" $D/mfg);WKP=
ok "m-skip-on-stdout-RED a caller that lets the wake's stdout through (no log redirect, foreground) puts the skip line in the hook's stdout (out: '$(echo "$o"|cut -c1-60)'): the stdout-empty lane catches it" '[ -n "$o" ]&&! cmp -s $D/mfg $D/bin/agi-meter'
mk o;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"},{"slice":"fix the red test","target":"g1.2"}]}';o=$(WK "$WP");c1=$(calls);r1=$(rows);WK "$WP">/dev/null
ok "wake-one-message-one-request after \`box read\` with ONE new message the stub gets exactly ONE request and the rows land (calls $c1, rows $r1); the second read gets 0 more (calls $(calls)); the hook prints nothing (out: '$o')" '[ "$c1" = 1 ]&&[ "$r1" = 2 ]&&[ "$(calls)" = 1 ]&&[ -z "$o" ]&&marked'
mk p;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK '{"prompt":"hello there"}'>/dev/null
ok "wake-only-on-the-box-read-prompt any other prompt makes 0 requests (calls $(calls))" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]'
# the failure of a REAL run is named: a stub agi-atomize exiting 124 (the timeout) with credits on -> ONE named line in ~/.atomize.log, NOTHING on stdout (the wake is backgrounded: its stdout/stderr are the log)
mkdir -p $D/b124;printf '#!/bin/sh\nexit 124\n'>$D/b124/agi-atomize;chmod +x $D/b124/agi-atomize;mk s;cred true;msg sm "$M1";rm -f $D/.atomize.log;WKP=$D/b124: o=$(WK "$WP");WKP=
ok "wake-failure-named a real run that exits 124 (credits on) logs ONE named line in ~/.atomize.log and prints nothing on stdout (out: '$o', log: $(grep -c 'wake rc=124' $D/.atomize.log 2>/dev/null))" '[ -z "$o" ]&&[ "$(grep -c "\[atomize\] wake rc=124: no atoms this read; the next read retries" $D/.atomize.log)" = 1 ]'
sed 's/||echo "[^"]*wake rc=[^"]*")/||:)/' $D/bin/agi-meter>$D/mf;mk t;cred true;msg sm "$M1";rm -f $D/.atomize.log;WKP=$D/b124: o=$(WK "$WP" $D/mf);WKP=
ok "m-failure-swallowed-RED an agi-meter whose call ends in ||: swallows the 124 (log: $(grep -c 'wake rc=124' $D/.atomize.log 2>/dev/null)): the wake-failure lane catches it" '[ "$(grep -c "wake rc=124" $D/.atomize.log 2>/dev/null)" = 0 ]&&! cmp -s $D/mf $D/bin/agi-meter'
# mutant: agi-meter without the caller -> 0 requests -> the wake lane (wants 1) is RED
sed '/agi-atomize wake/d' $D/bin/agi-meter>$D/mm;mk q;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK "$WP" $D/mm>/dev/null
ok "m-caller-removed-RED agi-meter without the agi-atomize call makes 0 requests (calls $(calls); the wake-one-message lane wants 1): that lane catches it" '[ "$(calls)" = 0 ]&&! cmp -s $D/mm $D/bin/agi-meter'
# --- the GATE CELL (alive [decision] 14:17:17Z 10-31, D1): agi-meter forks the wake only on atomize_live: true, whatever credits_live says
mk gf;AL=false cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';rm -f $D/.atomize.log;o=$(WK "$WP")
ok "gate-false-no-request with atomize_live false and credits_live TRUE the hook forks nothing: 0 requests, 0 rows, nothing marked, stdout empty, the log names it (out: '$o', log: $(tail -1 $D/.atomize.log 2>/dev/null|cut -d' ' -f2-), calls $(calls))" '[ -z "$o" ]&&grep -qF "[atomize] wake not run: atomize_live is false, no request" $D/.atomize.log&&[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&! marked'
mk ga;AL=- cred true;msg sm "$M1";rm -f $D/.atomize.log;o=$(WK "$WP")
ok "gate-absent-unreadable-no-request a secrets cell with no atomize_live line is unreadable, never live: 0 requests, the log names it (out: '$o', calls $(calls))" '[ -z "$o" ]&&grep -qF "[atomize] wake not run: atomize_live is unreadable, no request" $D/.atomize.log&&[ "$(calls)" = 0 ]'
# mutant: the cell read dropped (the gate always open) -> with atomize_live false the stub gets the request -> the gate-false lane is RED
sed 's/if \[ "\$al" != true \];then/if false;then/' $D/bin/agi-meter>$D/mg;mk gm;AL=false cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK "$WP" $D/mg>/dev/null
ok "m-gate-read-dropped-RED an agi-meter that never reads atomize_live sends the request with the cell false (calls $(calls); the gate-false lane wants 0)" '[ "$(calls)" = 1 ]&&! cmp -s $D/mg $D/bin/agi-meter'
# --- P-a: a run past its bound (124) is named by the NEXT wake, ONCE (the run's own status file, printed by agi-meter, then removed)
mk ws;cred true;rm -f $D/.atomize.status;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';reply 2 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';echo 5 >$D/q/sleep;TO=2;o1=$(WK "$WP");TO=;rm -f $D/q/sleep;s1=$(cat $D/.atomize.status 2>/dev/null);o2=$(WK "$WP");o3=$(WK "$WP")
ok "pa-timeout-named-on-the-next-wake a run past its bound (2 s; the endpoint sleeps 5 s) leaves rc=124 in the status ('$s1'); the NEXT wake prints ONE line naming it ('$o2'), the one after prints nothing ('$o3'); the first printed nothing ('$o1')" '[ -z "$o1" ]&&echo "$s1"|grep -q "rc=124"&&echo "$o2"|grep -q "^\[atomize\] last wake: .*rc=124"&&[ "$(printf "%s\n" "$o2"|wc -l)" = 1 ]&&[ -z "$o3" ]'
sed 's/\[ -s ~\/.atomize.status \]&&{ echo "\[atomize\] last wake: \$(cat ~\/.atomize.status)";rm -f ~\/.atomize.status;};//' $D/bin/agi-meter>$D/mpa;mk wt;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';echo "x rc=124: the run did not finish">$D/.atomize.status;o=$(WK "$WP" $D/mpa);rm -f $D/.atomize.status
ok "m-status-print-dropped-RED a meter that never prints the status says nothing about the last run's 124 ('$o'): the pa lane catches it" '[ -z "$o" ]&&! cmp -s $D/mpa $D/bin/agi-meter'
# --- P-d: the board's unatomized count (success_metrics --unatomized) reads 0 after a live wake and RED when the caller's match drifts
UN(){ (cd $T&&AGI_TRUNK=trunk AGI_ATOMIZE_AGE=99999999 python3 $R0/extensions/agi/bin/success_metrics.py --unatomized $T);}
mk wd;cred true;DT=@$(($(date +%s)-18000));msg sm "$M1";DT=;reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK "$WP">/dev/null;u1=$(UN)
sed 's/"mail: box read"\*)al=/"mail: box readX"*)al=/' $D/bin/agi-meter>$D/mpd;mk we;cred true;DT=@$(($(date +%s)-18000));msg sm "$M1";DT=;reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK "$WP" $D/mpd>/dev/null;u2=$(UN)
ok "pd-unatomized-zero-after-a-wake a message 5 h old atomized by a live wake: the board reads '$u1'" '[ "$u1" = "unatomized: 0" ]'
ok "m-wake-string-drifted-RED a meter whose match drifted never wakes, so the board reads '$u2' (want unatomized: RED 1 (p=1))" '[ "$u2" = "unatomized: RED 1 (p=1)" ]&&! cmp -s $D/mpd $D/bin/agi-meter'
# --- negative (falsifier 2): the box piece carries no model call
n=$(awk '/^### box /{f=1;next} /^### /{f=0} f' $R0/.agi/nodes/.geometry/engine-post.md|grep -c atomiz)
ok "box-body-names-no-atomiz the box piece's body names no atomiz* (got $n)" '[ "$n" = 0 ]'
n=$(awk '/^### box /{f=1;next} /^### /{f=0} f' $R0/.agi/nodes/.geometry/engine-post.md|sed 's/^case \$1 in$/case $1 in # atomize/'|grep -c atomiz)
ok "m-atomize-planted-in-box-RED the word planted in the box body reads 1 (got $n)" '[ "$n" = 1 ]'
echo "agi-atomize.t.sh: $f FAIL";exit $f
