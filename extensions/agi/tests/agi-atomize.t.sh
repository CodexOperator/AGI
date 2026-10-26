#!/bin/sh
# agi-atomize.t.sh [ROOT]: goal:g7.16.1.11.46.3 (M2) falsifier 1+2 against a LOCAL STUB model endpoint (a python3 http.server answering /v1/chat/completions from scripted replies; the REAL agi-infer piece talks to it): fixtures ask / fyi / report / quoted-only / re-read give the expected rows (fyi 0, quoted-only 0 calls, re-read +0 calls); a paraphrasing reply is refused by agi-atom add; an overlapping-slices reply is refused; a `?` target escalates ONCE to the second model; mutant m (no marker ref) reads RED on the re-read lane; negative: the box piece's body names no atomiz*.
# sh + git + jq + curl + python3 on a scratch repo with throwaway ssh keys; no network beyond 127.0.0.1, no root, 0 USD. ROOT = the tree whose engine-post.md / engine-wrap.md carry the pieces; PIECE=<file> tests a candidate agi-atomize. exit = the FAIL count.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);trap 'kill $SV 2>/dev/null;rm -rf "${D:?}"' 0;f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_ATOM_CARD AGI_ATOM_COMMIT AGI_INFER_SCHEMA AGI_INFER_KEY
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;sect agi-atom engine-post.md>$D/bin/agi-atom;sect agi-meter engine-post.md>$D/bin/agi-meter;sect agi-mem engine-post.md>$D/bin/agi-mem;sect agi-infer engine-wrap.md>$D/bin/agi-infer;PC=${PIECE:-$D/bin/agi-atomize};[ -n "$PIECE" ]||sect agi-atomize engine-post.md>$PC;chmod +x $D/bin/*
for x in agi-atom agi-infer;do [ -s $D/bin/$x ]||{ echo "FAIL inputs: no $x piece";exit 99;};done;[ -s "$PC" ]||{ echo "FAIL inputs: no agi-atomize piece";exit 99;}
printf '#!/bin/sh\ncd "$AGI_T"&&git add -A -- "$@"&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm "stub agi-at: $*"\n' >$D/stub;chmod +x $D/stub
# the stub endpoint: reply n of a run = file $D/q/r<n> (its text is the assistant message); every request is logged (model, prompt) to $D/q/log<n>
mkdir $D/q;cat >$D/stub.py<<'PY'
import http.server,json,sys,os
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
        H.n+=1;open(Q+"/log%d"%H.n,"w").write(json.dumps({"model":b["model"],"prompt":b["messages"][0]["content"]}))
        open(Q+"/calls","w").write(str(H.n))
        r=Q+"/r%d"%H.n
        if not os.path.exists(r): self.send_response(500);self.end_headers();return
        self.send_response(200);self.send_header("Content-Type","text/event-stream");self.end_headers()
        self.wfile.write(("data: "+json.dumps({"choices":[{"delta":{"content":open(r).read()}}]})+"\n\ndata: [DONE]\n\n").encode())
s=http.server.HTTPServer(("127.0.0.1",0),H);open(Q+"/port","w").write(str(s.server_port));s.serve_forever()
PY
python3 -I $D/stub.py $D/q & SV=$!;i=0;while [ ! -s $D/q/port ]&&[ $i -lt 50 ];do sleep 0.1;i=$((i+1));done;[ -s $D/q/port ]||{ echo "FAIL inputs: the stub endpoint did not start";exit 99;}
export AGI_INFER_URL=http://127.0.0.1:$(cat $D/q/port)/v1
# keys + a repo: sender sm signs, recipient p reads; a second key (evil) signs a forged "sm" commit
mkdir $D/k;: >$D/signers;for u in sm evil;do ssh-keygen -q -t ed25519 -N '' -f $D/k/$u -C $u>/dev/null;done;echo "sm@agi namespaces=\"git\" $(cut -d' ' -f1,2 $D/k/sm.pub)">$D/signers
SG(){ k=$1;shift;env GIT_AUTHOR_NAME=$k GIT_AUTHOR_EMAIL=sm@agi GIT_COMMITTER_NAME=$k GIT_COMMITTER_EMAIL=sm@agi git -c user.signingkey=$D/k/$k -c gpg.format=ssh -c gpg.ssh.allowedSignersFile=$D/signers "$@";}
mk(){ T=$D/w$1/t;for x in $D/q/r* $D/q/log* $D/q/calls;do [ -e "$x" ]&&rm -f "$x";done;mkdir -p $T/.agi/nodes/goal $T/.agi/sessions/quorum;cd $T;git init -q .;git config core.hooksPath /dev/null;git config gpg.format ssh;git config gpg.ssh.allowedSignersFile $D/signers
 printf -- '---\nid: goal:g1.2\nstatus: active\n---\n# g\n## Agent Notes\nAssigned to **p**.\n' >.agi/nodes/goal/g1.2.md;printf '# card\n\n## §0 x\nhi\n' >.agi/sessions/quorum/p.md;git add -A;git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm base;C=$T/.agi/sessions/quorum/p.md;}
msg(){ e=$(git hash-object -w -t tree /dev/null);c=$(printf '%s\n' "$2"|SG $1 commit-tree -S $e)&&git update-ref refs/box/sm/p $c;SHA=$c;}
reply(){ printf '%s' "$2">$D/q/r$1;}
calls(){ cat $D/q/calls 2>/dev/null||echo 0;}
AT(){ (cd $T;env AGI_T=$T AGI_POST=p AGI_LAP=5 HOME=$D PATH=$D/bin:$PATH AGI_ATOM_COMMIT=$D/stub AGI_ATOMIZE_AGE=99999999 sh ${1:-$PC}) 2>$D/err;}
rows(){ grep -c '^| a[0-9]* | ' $C;}
marked(){ git rev-parse -q --verify refs/atomized/p/$SHA>/dev/null;}
M1='Please build the widget now. Also fix the red test. Thanks!'
# --- ask: Haiku cuts two atoms with real targets, one call
mk a;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"},{"slice":"fix the red test","target":"g1.2"}]}';AT
ok "ask-two-rows an ask yields its two atoms as §7 rows with src:<the commit> and the real goal as target (rows $(rows))" '[ $(rows) = 2 ]&&grep -qF "| a1 | \"build the widget now\" | src:$SHA | target:goal:g1.2 |" $C'
ok "ask-one-call-first-model the first model is claude-haiku-5-5 and there was ONE call (calls $(calls), model $(jq -r .model $D/q/log1))" '[ "$(calls)" = 1 ]&&[ "$(jq -r .model $D/q/log1)" = claude-haiku-5-5 ]'
ok "ask-prompt-carries-leaf-ids the model is handed the recipient's leaf ids (g1.2) and the message" 'jq -r .prompt $D/q/log1|grep -q "g1.2"&&jq -r .prompt $D/q/log1|grep -qF "$M1"'
ok "ask-card-committed the card went through the commit step in ONE commit and the tree is clean" '[ "$(git rev-list --count HEAD)" = 2 ]&&[ -z "$(git status --porcelain)" ]'
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
ok "forged-signature-skipped a commit not signed by its sender is never read (calls $(calls), rows $(rows))" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]'
mk k;msg sm '[town] up 0123456789012345678901234567890123456789';AT
ok "town-line-skipped belam's [town] line is marked and never sent to a model (calls $(calls))" '[ "$(calls)" = 0 ]&&marked'
# --- mutant m: no marker ref -> the re-read lane reads it again
M=$D/m;sed 's/\[ "\$ok" \]&&git update-ref \$M\/\$c \$c ""/[ "$ok" ]/' $PC>$M;mk l;msg sm 'Just so you know: all is well.';reply 1 '{"kind":"fyi","atoms":[]}';reply 2 '{"kind":"fyi","atoms":[]}';reply 3 '{"kind":"fyi","atoms":[]}'
AT $M;AT $M
ok "m-no-marker-RED the mutant without the marker ref read the same fyi twice (calls $(calls), want 2): the re-read lane catches it" '[ "$(calls)" = 2 ]&&! cmp -s $M $PC'
rm -f $D/.atomize.last;M2=$D/ms;sed '/^date -u +%FT%TZ>/d' $PC>$M2;mk s;msg sm 'Numbers: 1 landed.';reply 1 '{"kind":"report","atoms":[]}';AT $M2
ok "m-no-stamp-RED the mutant without the stamp line leaves no ~/.atomize.last: the stamp lane catches it" '[ ! -e $D/.atomize.last ]&&! cmp -s $M2 $PC'
# --- the WAKE-PATH CALLER (the remainder of .46.3): agi-meter, the UserPromptSubmit hook, runs `agi-atomize wake` on the prompt "mail: box read"
# the meter runs agi-mem tap from PATH: the TREE's agi-mem (not an installed one: SM's finding 23:1xZ 10-25) against a tiny repo whose `trunk` ref holds a posts.md with no mem row for p, so the tap is silent by its own gate
mkdir -p $D/me/.agi/nodes/.geometry;printf -- '---\nid: config:posts\nposts:\n  - {"name": "p", "mem": "none"}\n---\n'>$D/me/.agi/nodes/.geometry/posts.md;(cd $D/me&&git init -q .&&git config core.hooksPath /dev/null&&git add -A&&git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm posts&&git update-ref refs/heads/trunk HEAD)>/dev/null 2>&1;[ -s $D/bin/agi-mem ]||{ echo "FAIL inputs: no agi-mem piece";exit 99;}
[ -n "$PIECE" ]&&cp $PC $D/bin/agi-atomize;[ -s $D/bin/agi-meter ]||{ echo "FAIL inputs: no agi-meter piece";exit 99;};chmod +x $D/bin/*
cred(){ mkdir -p .agi/nodes/.geometry;if [ -n "$1" ];then printf 'credits_live: %s\ndoppler: x\n' "$1">.agi/nodes/.geometry/secrets.md;else printf 'doppler: x\n'>.agi/nodes/.geometry/secrets.md;fi;git add -A;git -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm cred;git update-ref refs/heads/trunk HEAD;}
WK(){ printf '%s' "${1:-{\"prompt\":\"mail: box read\"\}}" | (cd $T;env AGI_T=$T AGI_POST=p AGI_LAP=5 HOME=$D PATH=$WKP$D/bin:$PATH AGI_ATOM_COMMIT=$D/stub AGI_ATOMIZE_AGE=99999999 AGI_TRUNK=trunk AGI_ENGINE=$D/me sh ${2:-$D/bin/agi-meter}) 2>$D/err;}
WP='{"prompt":"mail: box read"}';WKP=;rm -f $D/.atomize.log
mk m;cred false;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';o=$(WK "$WP")
ok "wake-credits-false-stdout-empty-skip-logged with credits_live false the hook's STDOUT is EMPTY (it enters the post's context), the named skip line goes to ~/.atomize.log, 0 calls, 0 rows, nothing marked (out: '$o', log: $(tail -1 $D/.atomize.log 2>/dev/null|cut -d' ' -f2-), calls $(calls))" '[ -z "$o" ]&&grep -qF "[atomize] skipped: credits_live is false, no model call" $D/.atomize.log&&[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]&&! marked'
mk n;cred "";msg sm "$M1";o=$(WK "$WP")
ok "wake-credits-unreadable-logged a secrets cell with no credits_live is named in the log too, stdout empty (out: '$o')" '[ -z "$o" ]&&grep -qF "[atomize] skipped: credits_live is unreadable, no model call" $D/.atomize.log&&[ "$(calls)" = 0 ]'
# mutant a: the skip line back on stdout -> the stdout-empty lane is RED
sed 's|>>\$HOME/.atomize.log;exit 0|;exit 0|' $PC>$D/ma;chmod +x $D/ma;mkdir -p $D/bina;cp $D/ma $D/bina/agi-atomize;mk r;cred false;msg sm "$M1";WKP=$D/bina: o=$(WK "$WP");WKP=
ok "m-skip-on-stdout-RED a wake that prints the skip line on stdout puts it in the hook's stdout (out: '$(echo "$o"|cut -c1-60)'): the stdout-empty lane catches it" '[ -n "$o" ]&&! cmp -s $D/ma $PC'
mk o;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"},{"slice":"fix the red test","target":"g1.2"}]}';o=$(WK "$WP");c1=$(calls);r1=$(rows);WK "$WP">/dev/null
ok "wake-one-message-one-request after \`box read\` with ONE new message the stub gets exactly ONE request and the rows land (calls $c1, rows $r1); the second read gets 0 more (calls $(calls)); the hook prints nothing (out: '$o')" '[ "$c1" = 1 ]&&[ "$r1" = 2 ]&&[ "$(calls)" = 1 ]&&[ -z "$o" ]&&marked'
mk p;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK '{"prompt":"hello there"}'>/dev/null
ok "wake-only-on-the-box-read-prompt any other prompt makes 0 requests (calls $(calls))" '[ "$(calls)" = 0 ]&&[ $(rows) = 0 ]'
# the failure of a REAL run is named: a stub agi-atomize exiting 124 (the timeout) with credits on -> ONE named line on stdout
mkdir -p $D/b124;printf '#!/bin/sh\nexit 124\n'>$D/b124/agi-atomize;chmod +x $D/b124/agi-atomize;mk s;cred true;msg sm "$M1";WKP=$D/b124: o=$(WK "$WP");WKP=
ok "wake-failure-named a real run that exits 124 (credits on) prints ONE named line on stdout: '$o'" '[ "$o" = "[atomize] wake rc=124: no atoms this read (~/.atomize.log); the next read retries" ]'
sed 's/||echo .*;;esac/||:;;esac/' $D/bin/agi-meter>$D/mf;mk t;cred true;msg sm "$M1";WKP=$D/b124: o=$(WK "$WP" $D/mf);WKP=
ok "m-failure-swallowed-RED an agi-meter whose call ends in ||: swallows the 124 (stdout: '$o'): the wake-failure lane catches it" '[ -z "$o" ]&&! cmp -s $D/mf $D/bin/agi-meter'
# mutant: agi-meter without the caller -> 0 requests -> the wake lane (wants 1) is RED
sed '/agi-atomize wake/d' $D/bin/agi-meter>$D/mm;mk q;cred true;msg sm "$M1";reply 1 '{"kind":"ask","atoms":[{"slice":"build the widget now","target":"g1.2"}]}';WK "$WP" $D/mm>/dev/null
ok "m-caller-removed-RED agi-meter without the agi-atomize call makes 0 requests (calls $(calls); the wake-one-message lane wants 1): that lane catches it" '[ "$(calls)" = 0 ]&&! cmp -s $D/mm $D/bin/agi-meter'
# --- negative (falsifier 2): the box piece carries no model call
n=$(awk '/^### box /{f=1;next} /^### /{f=0} f' $R0/.agi/nodes/.geometry/engine-post.md|grep -c atomiz)
ok "box-body-names-no-atomiz the box piece's body names no atomiz* (got $n)" '[ "$n" = 0 ]'
n=$(awk '/^### box /{f=1;next} /^### /{f=0} f' $R0/.agi/nodes/.geometry/engine-post.md|sed 's/^case \$1 in$/case $1 in # atomize/'|grep -c atomiz)
ok "m-atomize-planted-in-box-RED the word planted in the box body reads 1 (got $n)" '[ "$n" = 1 ]'
echo "agi-atomize.t.sh: $f FAIL";exit $f
