#!/bin/sh
# lane-header.t.sh: goal:g7.16.1.11.46.8 (C3) falsifier 1: the three fronts that reach the Console each send the lane's anthropic-workspace-id, from the lane CELL of config:secrets, with the key read from the credential FILE and
# never in a front's argv or environ. The fronts are the REAL ones: the agi-infer piece, pi 0.73.x (models.json provider claude-lane from `agi-lane pi`), claude -p (ANTHROPIC_CUSTOM_HEADERS from `agi-lane header` + apiKeyHelper from
# `agi-lane claude`). A LOCAL capture endpoint (127.0.0.1, python3 = the FIXTURE server only) records every request; no real key, no network, 0 USD. strace -f -v -e execve on each front proves the canary key is in no argv/environ.
# One ok/FAIL line per case; exit = number of FAILs. A MUTANT is one edit of a piece (rep) and its row passes only when the clean row is RED on it. Live leg (one real request per front, the response header == the cell) = banked.
T=$(mktemp -d);S=;trap '[ -z "$S" ]||kill $S 2>/dev/null;rm -rf $T' 0;f=0;R0=${ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)};G=/usr/bin/git
sect(){ cat $R0/.agi/nodes/.geometry/engine*.md|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}";}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
for x in pi claude strace jq python3;do command -v $x >/dev/null||{ echo "FAIL inputs: $x is not on PATH";exit 99;};done
sect agi-infer>$T/infer;sect agi-lane>$T/lane;[ -s $T/infer ]&&[ -s $T/lane ]||{ echo "FAIL extract: agi-infer $(wc -c<$T/infer) B, agi-lane $(wc -c<$T/lane) B";exit 99;}
INFER=$T/infer;LANE=$T/lane
KP=sk-an;KP=${KP}t;K="${KP}-api03-LANECANARY0123"
rep(){ A=$1 B=$2 awk '{o="";r=$0;while((i=index(r,ENVIRON["A"]))>0){o=o substr(r,1,i-1) ENVIRON["B"];r=substr(r,i+length(ENVIRON["A"]))}print o r}' $3>$T/mut.$4;cmp -s $3 $T/mut.$4&&echo "# NO EDIT for [$1]";}
# --- the cells: a scratch main repo whose secrets.md carries three test ids (and an option-B lane in a second commit)
M=$T/main;mkdir -p $M/.agi/nodes/.geometry;$G -C $M init -q
sed -e '/^  agi-batch:/s/"workspace": ""/"workspace": "wrkspc_BATCH111"/' -e '/^  agi-kids:/s/"workspace": ""/"workspace": "wrkspc_KIDS2222"/' -e '/^  agi-council:/s/"workspace": ""/"workspace": "wrkspc_COUNCIL333"/' $R0/.agi/nodes/.geometry/secrets.md>$M/.agi/nodes/.geometry/secrets.md
$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm ids >/dev/null 2>&1;TR=$($G -C $M rev-parse HEAD)
sed -e '/^  agi-council:/s/"workspace": "wrkspc_COUNCIL333"/"scoped_key": "claude-council"/' $M/.agi/nodes/.geometry/secrets.md>$T/optb;cp $T/optb $M/.agi/nodes/.geometry/secrets.md;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm optb >/dev/null 2>&1;TB=$($G -C $M rev-parse HEAD)
mkdir -p $T/cred;printf %s "$K">$T/cred/claude-sp;printf %s "$K">$T/cred/claude-council
# --- the capture endpoint: every request's path + lowercased headers, one JSON per line; 200 + [DONE] for a chat call, 401 otherwise
cat >$T/srv.py<<'XX2'
import http.server,sys,json
T=sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
  protocol_version='HTTP/1.0'
  def log_message(self,*a):pass
  def do_POST(s):
    b=s.rfile.read(int(s.headers.get('Content-Length') or 0))
    open(T+'/req.log','a').write(json.dumps({'p':s.path,'h':{k.lower():v for k,v in s.headers.items()}})+'\n')
    if s.path.endswith('/chat/completions'):
      s.send_response(200);s.send_header('Content-Type','text/event-stream');s.end_headers();s.wfile.write(b'data: {"choices":[{"delta":{"content":"ok"},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n');return
    s.send_response(401);s.send_header('Content-Type','application/json');s.end_headers();s.wfile.write(b'{"type":"error","error":{"type":"authentication_error","message":"capture"}}')
srv=http.server.HTTPServer(('127.0.0.1',0),H);open(T+'/port','w').write(str(srv.server_address[1]));srv.serve_forever()
XX2
python3 $T/srv.py $T & S=$!;i=0;while [ ! -s $T/port ]&&[ $i -lt 50 ];do sleep 0.1;i=$((i+1));done;PORT=$(cat $T/port);[ "$PORT" ]||{ echo "FAIL inputs: the capture endpoint did not start";exit 99;}
BASE=http://127.0.0.1:$PORT
lane(){ ( cd $M && AGI_TRUNK=${LT:-$TR} AGI_LANE_URL=$BASE/$TAG sh ${LP:-$LANE} "$@" );}
# first request of a front (by its path prefix) and every request lacking the header
got(){ jq -rs --arg t "/$1/" --arg k "$2" '[.[]|select(.p|startswith($t))]|(.[0].h[$k]//"")' $T/req.log 2>/dev/null;}
nreq(){ jq -rs --arg t "/$1/" '[.[]|select(.p|startswith($t))]|length' $T/req.log 2>/dev/null;}
nolack(){ jq -rs --arg t "/$1/" --arg v "$2" '[.[]|select(.p|startswith($t))|select(.h["anthropic-workspace-id"]!=$v)]|length' $T/req.log 2>/dev/null;}
# --- the three fronts: each under strace (execve, env expanded) so a key in any argv/environ of the front or its children is seen
front_infer(){ TAG=$1;echo hi|strace -f -v -s 4096 -qq -e trace=execve -o $T/st.$1 env -i PATH=$PATH CREDENTIALS_DIRECTORY=$T/cred AGI_INFER_URL=$BASE/$1/v1 AGI_INFER_MODEL=m AGI_INFER_WORKSPACE="$(lane id agi-batch)" sh ${IP:-$INFER}>/dev/null 2>&1;}
front_pi(){ TAG=$1;rm -rf $T/pi.$1;mkdir -p $T/pi.$1/.pi/agent;lane pi agi-kids capmodel>$T/pi.$1/.pi/agent/models.json;strace -f -v -s 4096 -qq -e trace=execve -o $T/st.$1 env -i PATH=$PATH HOME=$T/pi.$1 CREDENTIALS_DIRECTORY=$T/cred timeout 90 pi --provider claude-lane --model capmodel -p hi </dev/null >/dev/null 2>&1;}
front_claude(){ TAG=$1;rm -rf $T/cl.$1;mkdir -p $T/cl.$1;strace -f -v -s 4096 -qq -e trace=execve -o $T/st.$1 env -i PATH=$PATH HOME=$T/cl.$1 CREDENTIALS_DIRECTORY=$T/cred ANTHROPIC_BASE_URL=$BASE/$1 ANTHROPIC_CUSTOM_HEADERS="$(lane header agi-council)" DISABLE_AUTOUPDATER=1 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 timeout 90 claude -p hi --settings "$(lane claude agi-council)" </dev/null >/dev/null 2>&1;}
leak(){ echo "$(grep -c LANECANARY $T/st.$1) / $(grep -c execve $T/st.$1) execve";}
# ================= the lane verbs themselves
ok "v-a-id-prints-the-cell lane agi-batch: [$(TAG=x lane id agi-batch)] (want wrkspc_BATCH111)" '[ "$(TAG=x lane id agi-batch)" = wrkspc_BATCH111 ]'
ok "v-a-header-is-name-colon-value [$(TAG=x lane header agi-kids)]" '[ "$(TAG=x lane header agi-kids)" = "anthropic-workspace-id: wrkspc_KIDS2222" ]'
ok "v-a-claude-settings-cat-the-credential-file-by-name-not-by-value [$(TAG=x lane claude agi-kids)]" '[ "$(TAG=x lane claude agi-kids)" = "{\"apiKeyHelper\":\"cat \$CREDENTIALS_DIRECTORY/claude-sp\"}" ]'
ok "v-a-pi-provider-has-the-header-and-the-bang-cat-key [$(TAG=x lane pi agi-kids m|cut -c1-120)]" 'TAG=x lane pi agi-kids m|jq -e ".providers[\"claude-lane\"]|.api==\"anthropic-messages\" and .headers[\"anthropic-workspace-id\"]==\"wrkspc_KIDS2222\" and .apiKey==\"!cat \$CREDENTIALS_DIRECTORY/claude-sp\"" >/dev/null'
ok "v-a-no-verb-prints-a-key-byte canary hits in all four: $(for v in id header pi claude;do TAG=x lane $v agi-kids;done|grep -c LANECANARY)" '[ "$(for v in id header pi claude;do TAG=x lane $v agi-kids;done|grep -c LANECANARY)" = 0 ]'
ok "v-b-option-B-lane-sends-no-header-and-names-its-own-file header out [$(LT=$TB TAG=x lane header agi-council)] rc, pi: $(LT=$TB TAG=x lane pi agi-council|jq -c '.providers["claude-lane"]|[.headers,.apiKey]')" '[ -z "$(LT=$TB TAG=x lane header agi-council)" ]&&[ "$(LT=$TB TAG=x lane pi agi-council|jq -c ".providers[\"claude-lane\"]|[.headers,.apiKey]")" = "[null,\"!cat \$CREDENTIALS_DIRECTORY/claude-council\"]" ]'
ok "v-c-an-unknown-lane-is-rc-2 rc $(TAG=x lane id agi-nope >/dev/null 2>&1;echo $?)" '[ "$(TAG=x lane id agi-nope >/dev/null 2>&1;echo $?)" = 2 ]'
cp $M/.agi/nodes/.geometry/secrets.md $T/keep;sed -e '/^  agi-kids:/s/"workspace": "wrkspc_KIDS2222"/"workspace": ""/' $T/keep>$M/.agi/nodes/.geometry/secrets.md;$G -C $M add -A;$G -C $M -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm empty >/dev/null 2>&1;TE=$($G -C $M rev-parse HEAD)
ok "v-c-an-empty-workspace-cell-is-rc-3-and-says-whose-act rc $(LT=$TE TAG=x lane id agi-kids >/dev/null 2>&1;echo $?)" '[ "$(LT=$TE TAG=x lane id agi-kids >/dev/null 2>&1;echo $?)" = 3 ]&&LT=$TE TAG=x lane id agi-kids 2>&1|grep -q "owner makes the workspace"'
# ================= the fronts, clean
front_infer a;front_pi b;front_claude c
ok "f-a-agi-infer-sends-the-lane-header header [$(got a anthropic-workspace-id)] (cell wrkspc_BATCH111), requests $(nreq a), without it $(nolack a wrkspc_BATCH111)" '[ "$(got a anthropic-workspace-id)" = wrkspc_BATCH111 ]&&[ "$(nolack a wrkspc_BATCH111)" = 0 ]'
ok "f-a-agi-infer-sends-the-key-from-the-file auth line equals the canary bearer: $([ "$(got a authorization)" = "Bearer $K" ]&&echo yes||echo NO)" '[ "$(got a authorization)" = "Bearer $K" ]'
ok "f-b-pi-sends-the-lane-header header [$(got b anthropic-workspace-id)] (cell wrkspc_KIDS2222), requests $(nreq b), without it $(nolack b wrkspc_KIDS2222)" '[ "$(got b anthropic-workspace-id)" = wrkspc_KIDS2222 ]&&[ "$(nolack b wrkspc_KIDS2222)" = 0 ]'
ok "f-b-pi-sends-the-key-from-the-bang-cat x-api-key equals the canary: $([ "$(got b x-api-key)" = "$K" ]&&echo yes||echo NO)" '[ "$(got b x-api-key)" = "$K" ]'
ok "f-c-claude-p-sends-the-lane-header header [$(got c anthropic-workspace-id)] (cell wrkspc_COUNCIL333), requests $(nreq c), without it $(nolack c wrkspc_COUNCIL333)" '[ "$(got c anthropic-workspace-id)" = wrkspc_COUNCIL333 ]&&[ "$(nolack c wrkspc_COUNCIL333)" = 0 ]'
ok "f-c-claude-p-sends-the-key-from-the-apiKeyHelper auth line equals the canary bearer: $([ "$(got c authorization)" = "Bearer $K" ]&&echo yes||echo NO)" '[ "$(got c authorization)" = "Bearer $K" ]'
for x in a b c;do ok "f-$x-no-key-byte-in-any-argv-or-environ-of-the-front-or-its-children canary/execve: $(leak $x) (want 0 / >= 1: non-vacuous)" '[ "$(grep -c LANECANARY $T/st.'$x')" = 0 ]&&[ "$(grep -c execve $T/st.'$x')" -ge 1 ]';done
# ================= MUTANTS: a front with the header dropped reads RED (the clean row above is what it breaks)
rep '${AGI_INFER_WORKSPACE:+anthropic-workspace-id: $AGI_INFER_WORKSPACE}' '' $INFER inf;IP=$T/mut.inf front_infer ma;IP=
ok "m1-MUTANT-agi-infer-without-the-header-line-RED header [$(got ma anthropic-workspace-id)] (clean: wrkspc_BATCH111), requests $(nreq ma)" '[ "$(nreq ma)" -ge 1 ]&&[ "$(got ma anthropic-workspace-id)" != wrkspc_BATCH111 ]'
rep 'if $w!="" then' 'if false then' $LANE lpi;LP=$T/mut.lpi front_pi mb;LP=
ok "m2-MUTANT-the-pi-provider-without-headers-RED header [$(got mb anthropic-workspace-id)] (clean: wrkspc_KIDS2222), requests $(nreq mb)" '[ "$(nreq mb)" -ge 1 ]&&[ "$(got mb anthropic-workspace-id)" != wrkspc_KIDS2222 ]'
rep 'header)[ "$w" ]&&echo "anthropic-workspace-id: $w"' 'header)true' $LANE lcl;LP=$T/mut.lcl front_claude mc;LP=
ok "m3-MUTANT-claude-p-without-the-custom-header-RED header [$(got mc anthropic-workspace-id)] (clean: wrkspc_COUNCIL333), requests $(nreq mc)" '[ "$(nreq mc)" -ge 1 ]&&[ "$(got mc anthropic-workspace-id)" != wrkspc_COUNCIL333 ]'
# ================= NEGATIVE (leaf falsifier 3)
n=$($G -C $R0 grep -c 'ANTHROPIC_API_KEY=' -- .agi/nodes/.geometry 2>/dev/null|awk -F: '{s+=$NF}END{print s+0}')
ok "n-no-geometry-node-sets-ANTHROPIC_API_KEY hits $n (want 0)" '[ "$n" = 0 ]'
echo "lane-header: $f FAIL";exit $f
