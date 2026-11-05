#!/bin/sh
# mem-summary.t.sh [ROOT]: goal:g7.16.1.11.46.25 (M9) falsifier 1 + 2: `agi-mem view` (what agi-brief prints after `agi-mem at`) stays under its bound for a store of any size; `agi-mem compact` sends ONE request, no tools, to the STUB while the trunk's summary_live cell is not true, and the real endpoint gets 0; each lane has its MUTANT read RED.
# sh + git + jq + python3 on a scratch HOME, a scratch engine repo and two LOCAL stub endpoints (stub = AGI_MEM_STUB, canary = the "real" AGI_INFER_URL); the REAL agi-mem and agi-infer pieces; no network, no root, 0 USD. ROOT = the tree whose engine-post.md carries the piece. exit = the FAIL count.
# Lanes: v1 the view of a 10-chunk store is whole and bounded; v2 a 10000-chunk store's view is bounded and leads with the newest chunk; v3 the mutant without the cut is unbounded; v4 an unread store prints `mem view: unread`, rc 1; c1 under the byte cell 0 requests; c1b summary_live UNREAD (the cell absent): the stub, never the canary; c1c its mutant (stub only on an explicit false); c2 summary_live false: the stub gets the ONE request, the canary 0, sum/1.md names its range + upto; c3 the mutant without the forcing line sends it to the canary; c4 a second compact with nothing new makes 0 requests; c5 the cap: an oldest-first slice, upto mid-range, the next compact goes on from it; c6 summary_live true: the real endpoint gets it; c7 the view leads with the summary.
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};D=$(mktemp -d);f=0;unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE AGI_MINT AGI_MEM_VIEW AGI_MEM_COMPACT AGI_MEM_COMPACT_MAX AGI_INFER_URL AGI_MEM_STUB
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
sect(){ awk -v n="$1" '$0~"^### "n" "{h=1;next}h&&/^~~~/{if(z)exit;z=1;next}h&&z' $R0/.agi/nodes/.geometry/$2;}
mkdir $D/bin;sect agi-mem engine-post.md>$D/bin/agi-mem;sect agi-infer engine-wrap.md>$D/bin/agi-infer;chmod +x $D/bin/*
for x in agi-mem agi-infer;do [ -s $D/bin/$x ]||{ echo "FAIL inputs: no $x piece";exit 99;};done
# two stub endpoints, each answering /v1/chat/completions with a fixed summary and counting its requests in $Q/calls
cat >$D/stub.py<<'PY'
import http.server,json,sys,os
Q=sys.argv[1]
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_POST(self):
        b=json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        n=int(open(Q+"/calls").read()) if os.path.exists(Q+"/calls") else 0
        open(Q+"/calls","w").write(str(n+1));open(Q+"/last","w").write(b["messages"][0]["content"])
        self.send_response(200);self.send_header("Content-Type","text/event-stream");self.end_headers()
        self.wfile.write(("data: "+json.dumps({"choices":[{"delta":{"content":"SUMMARY from "+os.path.basename(Q)}}]})+"\n\ndata: [DONE]\n\n").encode())
s=http.server.HTTPServer(("127.0.0.1",0),H);open(Q+"/port","w").write(str(s.server_port));s.serve_forever()
PY
for q in stub canary;do mkdir $D/$q;python3 -I $D/stub.py $D/$q & eval PID_$q=$!;done
trap 'kill $PID_stub $PID_canary 2>/dev/null;rm -rf "${D:?}"' 0
i=0;while { [ ! -s $D/stub/port ]||[ ! -s $D/canary/port ];}&&[ $i -lt 50 ];do sleep 0.1;i=$((i+1));done;[ -s $D/stub/port ]&&[ -s $D/canary/port ]||{ echo "FAIL inputs: the stub endpoints did not start";exit 99;}
STUB=http://127.0.0.1:$(cat $D/stub/port)/v1;CAN=http://127.0.0.1:$(cat $D/canary/port)/v1
calls(){ cat $D/$1/calls 2>/dev/null||echo 0;}
# the engine: the trunk (HEAD) holds posts.md (p: mem full) and secrets.md; CELL v rewrites summary_live and commits
E=$D/eng;mkdir -p $E/.agi/nodes/.geometry;git -C $E init -q .;git -C $E config core.hooksPath /dev/null
printf -- '---\nid: config:posts\nposts:\n  - {"name": "p", "mem": "full"}\n---\n'>$E/.agi/nodes/.geometry/posts.md
CELL(){ printf -- '---\nid: config:secrets\ncredits_live: true\n%s---\n' "${1:+summary_live: $1
}">$E/.agi/nodes/.geometry/secrets.md;git -C $E add -A;git -C $E -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm cell --allow-empty;}
CELL false
# a store: STORE N [K]: N chunks in ONE commit (fast-import), then K more commits of one chunk each (the newest last); each chunk ~ 200 B
STORE(){ H=$D/h$1;rm -rf "${H:?}";S=$H/.mem/p.git;mkdir -p $H/.mem;git init -q --bare $S;git -C $S config core.hooksPath /dev/null
 awk -v n=$2 -v k=${3:-0} 'function ch(i,  c){c="---\nid: c:" sprintf("%012d",i) "\nspeaker: owner\nt: 2026-10-31T10:00:00Z\n---\nchunk " i " body: the owner asks for the widget and the red test, a line of padding to make the chunk near two hundred bytes long.\n";printf "M 100644 inline mem/2026-10-31/c-%012d.md\ndata %d\n%s\n",i,length(c),c}
  BEGIN{print "commit refs/heads/mem";print "committer mem <mem@agi> 1700000000 +0000";print "data 3\ntap";for(i=1;i<=n;i++)ch(i);for(j=1;j<=k;j++){print "commit refs/heads/mem";print "committer mem <mem@agi> " 1700000000+j " +0000";print "data 3\ntap";ch(n+j)}}'|git -C $S fast-import --quiet;}
AM(){ env HOME=$H AGI_POST=p AGI_ENGINE=$E AGI_TRUNK=HEAD PATH=$D/bin:$PATH sh ${MB:-$D/bin/agi-mem} "$@";}
MUT(){ python3 -I -c 'import sys;s=open(sys.argv[1]).read();a,b=sys.argv[2],sys.argv[3];assert s.count(a)==1,a;open(sys.argv[4],"w").write(s.replace(a,b))' $D/bin/agi-mem "$1" "$2" $D/mut||{ echo "FAIL inputs: mutant text not found once: $1";exit 99;};}

# ---- F1: the view stays under its bound for a store of any size
STORE v1 10;AM view>$D/o;rc=$?
ok "v1-ten-chunks-whole-and-bounded a 10-chunk store: the view shows all 10 chunks ($(grep -c '^### mem/' $D/o)) in $(wc -c <$D/o) B (<= 4000 + its header line), rc $rc" '[ $rc = 0 ]&&[ $(grep -c "^### mem/" $D/o) = 10 ]&&[ $(wc -c <$D/o) -le 4100 ]'
STORE v2 9999 1;t0=$(date +%s);AM view>$D/o;t1=$(date +%s)
ok "v2-ten-thousand-chunks-bounded a 10000-chunk store: the view is $(wc -c <$D/o) B (<= 4000 + its header line) in $((t1-t0)) s, and leads with the NEWEST chunk (c-000000010000)" '[ $(wc -c <$D/o) -le 4100 ]&&sed -n 2p $D/o|grep -q "c-000000010000"&&[ $((t1-t0)) -le 20 ]'
MUT 'done|head -c $V;echo;;' 'done;echo;;';MB=$D/mut AM view>$D/o
ok "v3-m-unbounded-RED the mutant without the cut prints $(wc -c <$D/o) B for the 10000-chunk store: the v2 lane catches it" '[ $(wc -c <$D/o) -gt 100000 ]'
AGI_MEM_VIEW=1000 AM view>$D/o
ok "v3b-the-bound-is-the-cell AGI_MEM_VIEW=1000: $(wc -c <$D/o) B (<= 1000 + its header line)" '[ $(wc -c <$D/o) -le 1100 ]'
H=$D/none;mkdir -p $H;AM view>$D/o;rc=$?
ok "v4-unread-store-named no store: 'mem view: unread', rc $rc (never 0, never an empty pass)" '[ $rc = 1 ]&&grep -qx "mem view: unread" $D/o'

# ---- F2: summary_live not true -> the stub gets every compactor request, the real endpoint 0
STORE c1 10;AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact
ok "c1-under-the-cell-no-request 10 chunks (~2 KB < AGI_MEM_COMPACT 20000): stub $(calls stub), canary $(calls canary), no summary ref" '[ "$(calls stub)" = 0 ]&&[ "$(calls canary)" = 0 ]&&! git -C $S rev-parse -q --verify refs/heads/summary>/dev/null'
STORE c2 120;AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact;tip=$(git -C $S rev-parse refs/heads/mem);sm=$(git -C $S show refs/heads/summary:sum/1.md 2>/dev/null)
ok "c2-stub-gets-it summary_live false, 120 chunks (~24 KB): ONE request to the stub ($(calls stub)), 0 to the canary ($(calls canary)); sum/1.md covers c:000000000001..c:000000000120, chunks 120, upto the mem tip, the stub's text" '[ "$(calls stub)" = 1 ]&&[ "$(calls canary)" = 0 ]&&printf %s "$sm"|grep -qx "covers: c:000000000001..c:000000000120"&&printf %s "$sm"|grep -qx "chunks: 120"&&printf %s "$sm"|grep -qx "upto: $tip"&&printf %s "$sm"|grep -q "SUMMARY from stub"'
ok "c2b-the-request-carries-the-chunks the stub's request names the post and holds chunk 120's body" 'grep -q "post p" $D/stub/last&&grep -q "chunk 120 body" $D/stub/last'
# e (alive [decision] 19:52:47Z, sp): the UNREAD direction of the spend gate: the cell ABSENT from the trunk's secrets.md -> summary_live unread -> the stub gets the ONE request, the canary 0 (AGI_TRUNK at no such ref cannot be the fixture: agi-mem's preamble reads posts.md from the same trunk and exits 0 before compact runs)
CELL '';STORE c1b 120;s0=$(calls stub);c0=$(calls canary);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact
ok "c1b-unread-cell-goes-to-the-stub summary_live unread (the cell absent): stub $s0 -> $(calls stub), canary $c0 -> $(calls canary)" '[ "$(calls stub)" = $((s0+1)) ]&&[ "$(calls canary)" = $c0 ]'
MUT '[ "$l" = true ]||export AGI_INFER_URL=' '[ "$l" = false ]&&export AGI_INFER_URL=';STORE c1c 120;s0=$(calls stub);c0=$(calls canary);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB MB=$D/mut AM compact;CELL false
ok "c1c-m-stub-only-on-false-RED the mutant forcing the stub only on an explicit false sends the unread-cell request to the canary (canary $c0 -> $(calls canary)): the c1b lane catches it" '[ "$(calls canary)" = $((c0+1)) ]&&[ "$(calls stub)" = $s0 ]'
MUT 'export AGI_INFER_URL=${AGI_MEM_STUB:-http://127.0.0.1:9/v1}' ':';STORE c3 120;s0=$(calls stub);c0=$(calls canary);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB MB=$D/mut AM compact
ok "c3-m-forcing-dropped-RED the mutant without the forcing line sends the request to the canary (canary $c0 -> $(calls canary), stub $s0 -> $(calls stub)): the c2 lane catches it" '[ "$(calls canary)" = $((c0+1)) ]&&[ "$(calls stub)" = $s0 ]'
STORE c4 120;AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact;s0=$(calls stub);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact
ok "c4-nothing-new-no-request a second compact with no chunk past upto: stub $s0 -> $(calls stub), still one summary" '[ "$(calls stub)" = $s0 ]&&[ "$(git -C $S rev-list --count refs/heads/summary)" = 1 ]'
STORE c5 0 150;s0=$(calls stub);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AGI_MEM_COMPACT=5000 AGI_MEM_COMPACT_MAX=10000 AM compact;u1=$(git -C $S show refs/heads/summary:sum/1.md|sed -n 's/^upto: //p');n1=$(git -C $S rev-list --count $u1);e1=$(git -C $S show refs/heads/summary:sum/1.md|sed -n 's/^covers: .*\.\.c:0*//p')
AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AGI_MEM_COMPACT=5000 AGI_MEM_COMPACT_MAX=10000 AM compact;cv2=$(git -C $S show refs/heads/summary:sum/2.md 2>/dev/null|sed -n 's/^covers: //p')
ok "c5-the-cap-slices-oldest-first 150 one-chunk commits (after an empty root), cap 10000 B: sum/1 ends at chunk $e1 (upto = commit $n1 of 151, mid-range), sum/2 goes on from chunk $((e1+1)) ($cv2); requests $s0 -> $(calls stub)" '[ $n1 -gt 2 ]&&[ $n1 -lt 151 ]&&[ "$e1" = $((n1-1)) ]&&[ "${cv2%%..*}" = "c:$(printf %012d $((e1+1)))" ]&&[ "$(calls stub)" = $((s0+2)) ]'
CELL true;STORE c6 120;s0=$(calls stub);c0=$(calls canary);AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact;CELL false
ok "c6-summary-live-true-goes-real summary_live true: the request goes to AGI_INFER_URL (canary $c0 -> $(calls canary)), the stub none ($s0 -> $(calls stub))" '[ "$(calls canary)" = $((c0+1)) ]&&[ "$(calls stub)" = $s0 ]'
STORE c7 120;AGI_INFER_URL=$CAN AGI_MEM_STUB=$STUB AM compact;AM view>$D/o
ok "c7-the-view-leads-with-the-summary after a compaction the view's first entry is sum/1.md, then the newest chunks, still bounded ($(wc -c <$D/o) B)" '[ "$(sed -n 2p $D/o)" = "### sum/1.md" ]&&grep -q "^### mem/" $D/o&&[ $(wc -c <$D/o) -le 4100 ]'
echo "mem-summary: $f FAIL";exit $f
