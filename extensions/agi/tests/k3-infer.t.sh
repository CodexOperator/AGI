#!/bin/sh
# k3-infer.t.sh: goal:g7.16.1.11.18 falsifier 1 (Z4.j + Z4.l, K3): agi-infer streams. sh + curl + jq + python3 (the FIXTURE SERVER only) + strace, scratch only,
# 0 USD: a canned SSE fixture served on 127.0.0.1, a canary where a key would be (no real key is read or printed). One ok/FAIL line per case; exit = number of FAILs.
# PIECE = the file under test (default: `sect agi-infer` read from the .geometry engine*.md of ROOT, the working tree); a mutation = PIECE=<edited copy>.
T=$(mktemp -d);S=;trap '[ -z "$S" ]||kill $S 2>/dev/null;rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};CEIL=${CEIL:-1100}
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
[ -n "$PIECE" ]||{ sect agi-infer>$T/piece;PIECE=$T/piece;}
[ -s $PIECE ]||{ echo "FAIL extract: agi-infer $(wc -c<$PIECE) B";exit 99;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
# --- fixture server (harness only, never part of the spawn): /<case>/v1/chat/completions; records the body + the Authorization line per case
cat >$T/srv.py<<'XX'
import http.server,sys,time,os
T=sys.argv[1]
C=[b': OPENROUTER PROCESSING',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"role":"assistant","content":""}}]}',
 b': OPENROUTER PROCESSING',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":"ok lane\\n"}}]}',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":"next "}}]}',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":"caf\\u00e9 \\"q\\" \\\\ \\t"}}]}',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":""}}]}',
 b': OPENROUTER PROCESSING',
 b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":"end"},"finish_reason":"stop"}]}',
 b'data: {"id":"g1","choices":[],"usage":{"prompt_tokens":3,"completion_tokens":5,"cost":0}}']
class H(http.server.BaseHTTPRequestHandler):
  protocol_version='HTTP/1.0'
  def log_message(self,*a):pass
  def do_POST(s):
    k=s.path.split('/')[1];b=s.rfile.read(int(s.headers.get('Content-Length') or 0))
    open(T+'/body.'+k,'wb').write(b);open(T+'/auth.'+k,'w').write(s.headers.get('Authorization') or '')
    if k=='e500':
      s.send_response(500);s.end_headers();s.wfile.write(b'{"error":"boom"}');return
    s.send_response(200);s.send_header('Content-Type','text/event-stream');s.end_headers()
    def w(l):s.wfile.write(l+b'\n\n');s.wfile.flush()
    if k=='slow':
      w(C[1]);w(C[3]);time.sleep(3);w(C[4]);w(b'data: [DONE]');return
    E={'err':b'data: {"id":"g1","error":{"code":"server_error","message":"upstream died"},"choices":[{"index":0,"delta":{"content":""},"finish_reason":"error"}]}',
       'err2':b'data: {"id":"g1","choices":[{"index":0,"delta":{"content":""},"finish_reason":"error"}]}',
       'err3':b'data: {"id":"g1","error":{"code":429,"message":"rate limited"},"choices":[]}'}
    if k in E:
      w(C[1]);w(C[3]);w(C[4]);w(E[k]);w(b'data: [DONE]');return
    for l in C:
      w(l)
      if k=='ok':time.sleep(0.05)
    if k!='trunc':w(b'data: [DONE]')
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);open(T+'/port','w').write(str(s.server_address[1]));s.serve_forever()
XX
python3 $T/srv.py $T & S=$!
n=0;while [ ! -s $T/port ]&&[ $n -lt 50 ];do sleep 0.1;n=$((n+1));done
[ -s $T/port ]||{ echo "FAIL fixture: server did not start";exit 99;}
U=http://127.0.0.1:$(cat $T/port);KEY=sk-canary-$$-$(od -An -N6 -tx1 /dev/urandom|tr -d ' \n')
# the expected result, written by hand (never derived from the fixture): the content deltas concatenated, nothing else, no trailing newline added
printf 'ok lane\nnext caf\303\251 "q" \\ \tend'>$T/want
printf 'line one\nsays "hi" \\ and\ttab\n'>$T/prompt
# run K CASE [ARGS]: the piece as the caller would run it: prompt on stdin, key by NAME, schema off
run(){ k=$1;shift;AGI_INFER_URL=$U/$k/v1 AGI_INFER_KEY=TESTK TESTK=$KEY sh $PIECE "$@"<$T/prompt;}
# --- Z4.l: the streamed text == the committed result, byte for byte
run ok m-arg>$T/ok.out 2>$T/ok.err;rc=$?
ok "z4l-rc0 a clean stream exits 0 (rc=$rc)" '[ $rc -eq 0 ]'
ok "z4l-bytes the streamed text == the canned deltas concatenated, byte for byte ($(wc -c<$T/ok.out) B)" 'cmp -s $T/ok.out $T/want'
ok "z4l-comments no ': OPENROUTER PROCESSING' line reaches the result" '! grep -q OPENROUTER $T/ok.out'
ok "z4l-done no '[DONE]' and no 'data:' reaches the result" '! grep -qE "DONE|data:" $T/ok.out'
ok "z4l-stderr nothing on stderr on a clean stream" '[ ! -s $T/ok.err ]'
# the byte-exact case WITHOUT a model arg: the model comes from the cell
AGI_INFER_MODEL=m-env run ok2>$T/ok2.out 2>/dev/null
ok "z4l-cell the model cell (no arg) streams the same bytes" 'cmp -s $T/ok2.out $T/want'
# --- the request: streaming is asked for, the prompt rides whole, the key rides the header and nowhere else
ok "req-stream the body carries stream:true" '[ "$(jq -r .stream $T/body.ok)" = true ]'
ok "req-prompt the body holds the stdin prompt whole as ONE user message" '[ "$(jq -r ".messages|length" $T/body.ok)" = 1 ]&&[ "$(jq -r ".messages[0].role" $T/body.ok)" = user ]&&[ "$(jq -j ".messages[0].content" $T/body.ok|od -An -tx1)" = "$(od -An -tx1<$T/prompt)" ]'
ok "req-model the arg is the model" '[ "$(jq -r .model $T/body.ok)" = m-arg ]'
ok "req-model-cell with no arg the cell model reached the body" '[ "$(jq -r .model $T/body.ok2)" = m-env ]'
ok "req-key the Authorization header is Bearer <the var the NAME points at>" '[ "$(cat $T/auth.ok)" = "Bearer $KEY" ]'
ok "req-key-quiet the key value is on neither stdout nor stderr" '! grep -qF "$KEY" $T/ok.out $T/ok.err'
AGI_INFER_SCHEMA=$T/schema.json;printf '{"type":"object","properties":{"a":{"type":"string"}},"required":["a"]}'>$T/schema.json;export AGI_INFER_SCHEMA
run sch m-s>$T/sch.out 2>/dev/null;unset AGI_INFER_SCHEMA
ok "req-schema the schema fence still rides with streaming (closed, name fill) and stream:true" '[ "$(jq -c "[.stream,.response_format.type,.response_format.json_schema.name,.response_format.json_schema.schema.additionalProperties]" $T/body.sch)" = "[true,\"json_schema\",\"fill\",false]" ]'
# no key NAME in the cells = NO Authorization header at all (a keyless local server), not an empty 'Bearer '
AGI_INFER_URL=$U/nokey/v1 sh $PIECE m<$T/prompt>$T/nk.out 2>/dev/null
ok "req-nokey with no infer_key cell no Authorization header is sent (got: '$(cat $T/auth.nokey)') and the text still streams" '[ ! -s $T/auth.nokey ]&&cmp -s $T/nk.out $T/want'
# the key cell is a NAME, never shell text: a non-name cell (metacharacters, a space) exits 2, runs nothing and sends no request (all-is-one measured: AGI_INFER_KEY="X;touch F" ran the touch under eval)
for raw in 'X;touch @T@/PWN1' 'X$(touch @T@/PWN2)' 'X`touch @T@/PWN3`' 'a b' '-x' 1 0 9ab;do
 bad=$(printf %s "$raw"|sed "s,@T@,$T,g");rm -f $T/body.evil;AGI_INFER_URL=$U/evil/v1 AGI_INFER_KEY="$bad" sh $PIECE m<$T/prompt>$T/bad.out 2>/dev/null;rc=$?
 ok "key-name a non-name infer_key cell ($raw) exits 2, sends no request, prints nothing (rc=$rc)" '[ $rc = 2 ]&&[ ! -e $T/body.evil ]&&[ ! -s $T/bad.out ]'
done
ok "key-name-noexec no cell text was executed (no PWN file)" '[ -z "$(ls $T|grep PWN)" ]'
# a digit-leading cell is no variable NAME: under eval k=$1 it would read the MODEL arg (cell 1) or the script path (cell 0) and send it as the Bearer (mur dg2-k3-c2 R3). And an inherited k must never ride when the cell is empty.
AGI_INFER_URL=$U/inh/v1 k=INHERITED-LEAK sh $PIECE m<$T/prompt>/dev/null 2>&1
ok "key-inherited-k with NO key cell an inherited env var k is never sent as a Bearer (got: '$(cat $T/auth.inh)')" '[ ! -s $T/auth.inh ]'
AGI_INFER_URL=$U/inh2/v1 AGI_INFER_KEY=TESTK TESTK=$KEY k=INHERITED-LEAK sh $PIECE m<$T/prompt>/dev/null 2>&1
ok "key-cell-wins with a key cell set the cell's value is the Bearer, never an inherited k" '[ "$(cat $T/auth.inh2)" = "Bearer $KEY" ]'
# --- streaming, not buffering: the first chunk is in the log while the request is still open (the slow case holds the 2nd chunk back 3 s)
AGI_INFER_URL=$U/slow/v1 AGI_INFER_KEY=TESTK TESTK=$KEY sh $PIECE m<$T/prompt>$T/slow.out 2>$T/slow.err & P=$!
n=0;while [ ! -s $T/slow.out ]&&[ $n -lt 20 ];do sleep 0.1;n=$((n+1));done
alive=0;kill -0 $P 2>/dev/null&&alive=1;first=$(wc -c<$T/slow.out)
wait $P;rc=$?
ok "stream-live the first chunk is in the log within 2 s, while the request is still open (first=$first B after $n x 0.1 s, alive=$alive)" '[ $first -gt 0 ]&&[ $alive -eq 1 ]'
ok "stream-whole the slow stream still ends as the full text (rc=$rc)" '[ $rc -eq 0 ]&&[ "$(cat $T/slow.out)" = "$(printf "ok lane\nnext ")" ]'
# --- Z4.j: the spawn starts no process but curl, sed, grep, jq (the interpreter itself is the first execve and is not counted)
AGI_INFER_URL=$U/ok/v1 AGI_INFER_KEY=TESTK TESTK=$KEY strace -f -qq -s 4096 -e trace=execve -o $T/exec.log sh $PIECE m<$T/prompt>$T/x.out 2>/dev/null
ok "z4j-ran the traced run is the same bytes (the trace saw the real run)" 'cmp -s $T/x.out $T/want'
procs=$(grep 'execve("' $T/exec.log|grep -v '= -1 '|sed 's/.*execve("\([^"]*\)".*/\1/;s,.*/,,'|sed 1d|sort -u|tr '\n' ' ')
ok "z4j-set no process but curl, sed, grep, jq (saw: ${procs:-none})" '[ -n "$procs" ]&&[ -z "$(printf "%s" "$procs"|tr " " "\n"|grep -vxE "curl|sed|grep|jq")" ]'
ok "z4j-argv the key value is in no process argument (ps-visible)" '! grep -qF "$KEY" $T/exec.log'
# --- failure is loud: a refused request and a stream cut before [DONE] are NOT a clean result (the committed result must be the whole text)
run e500 m>$T/e.out 2>/dev/null;rc=$?
ok "fail-http an HTTP 500 exits 5 with nothing on stdout (rc=$rc)" '[ $rc = 5 ]&&[ ! -s $T/e.out ]'
run trunc m>$T/t.out 2>/dev/null;rc=$?
ok "fail-trunc a stream cut before [DONE] exits 5 (rc=$rc): a cut text is never committed as the result" '[ $rc = 5 ]'
# --- a provider ERROR event in the stream is NOT a clean result: OpenRouter sends {"error":{..},"choices":[{"finish_reason":"error"}]} (or either half alone) and THEN [DONE], so the stream looks complete
# while the text is cut. The runner commits stdout as the result, so the exit status is the only signal (security mur dg2-k3, SM 03:0xZ).
for e in err err2 err3;do run $e m>$T/$e.out 2>/dev/null;rc=$?
 ok "fail-error-$e a mid-stream error event ($([ $e = err ]&&echo 'error + finish_reason error'||{ [ $e = err2 ]&&echo 'finish_reason error alone'||echo 'an error object alone, no choices'; })) then [DONE] exits 5 (rc=$rc)" '[ $rc = 5 ]'
done
ok "fail-error-ok-still-clean a normal finish_reason stop + usage chunk + [DONE] still exits 0 (the error check is not a blanket)" 'run ok m>/dev/null 2>&1'
# --- bounds
sz=$(wc -c<$PIECE)
ok "bytes the piece is <= $CEIL B ($sz B; 829 B at the start; measured steps +131 B the streaming parser (960), +34 B the key-name guard (994), +73 B the provider-error clause (1,067), +10 B the digit-leading + inherited-k guard (1,077); 1,100 B ceiling raised by SM's order, see the lane commit)" '[ $sz -le $CEIL ]'
ok "bytes-sh the piece is POSIX sh (dash -n parses it; no bashism needed)" 'dash -n $PIECE 2>/dev/null||sh -n $PIECE'
echo "k3-infer: $f FAIL"
exit $f
