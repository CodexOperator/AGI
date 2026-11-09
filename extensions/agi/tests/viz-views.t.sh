#!/bin/sh
# viz-views.t.sh: goal:g7.16.1.11.9.1 (the dashboard): ONE graphweb export (/views.json, build_views) feeds the crew, workflow and comms views beside the 3D graph; every file it reads is `git show <sha>:<path>` at ONE sha, every box count is `git rev-list --count` over the stated window; post names and counts only; loopback only; the page reads only graphweb's own relative endpoints.
# sh + git + python3 -I on a scratch fixture repo, no network (one loopback port this lane starts and stops), no root, 0 USD. Usage: sh viz-views.t.sh [ROOT] (or ROOT=): ROOT = the tree under test (its extensions/agi/bin/graphweb.py and extensions/agi/web/graph/); row b diffs graphweb.py against this build's PARENT, pinned by sha (PIN_PARENT 32063f957b1f41184a6c80de01012dd56156fa76, in full, resolved in ROOT's repo; unresolvable = a FAIL, never a pass); env BASE is an explicit override, printed in the row. Exit = the FAIL count.
# Lanes: f-* the FIXTURE (posts.md 3 rows at S, 4 at S' = HEAD; crons.md 2 jobs; refs/box/a/b 3 commits, b/a 1, c/a 1 old, a/zz not a post); e-* an EMPTY source; live-* ROOT's own trunk at its HEAD (live-graph-json-nodes serves a COPY of ROOT's .agi; with no persisted layout under ROOT/.agi/sessions the cold /graph.json build takes minutes, GRAPH_TIMEOUT default 900 s); a/b/c the page and the diff; p-* the port; m-* MUTANTS, each applied to a COPY and each must turn its row RED.
# Honest limits: the views' draw code (DOM/SVG) is not executed here, save the footer (setFoot + dirtyWords, run by node on a stub element, row d) (the graphweb pytest harnesses run app.js's 3D boot); 'nodes == the verify count' (leaf Falsifier 1) compares against verify's READER (metrics), not the verify command (see live-graph-json-nodes); a clone with no refs/box reads the live comms view as read_nothing.
set -f
R0=${ROOT:-${1:-$(cd "$(dirname "$0")/../../.." && pwd)}};f=0
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
BIN=$R0/extensions/agi/bin;WEB=$R0/extensions/agi/web/graph;PIN_PARENT=32063f957b1f41184a6c80de01012dd56156fa76
[ -f "$BIN/graphweb.py" ]&&[ -f "$WEB/app.js" ]&&[ -f "$WEB/index.html" ]||{ echo "FAIL inputs: $BIN/graphweb.py, $WEB/app.js, $WEB/index.html";exit 99;}
T=$(mktemp -d "${TMPDIR:-/tmp}/viz-views.XXXXXX")||exit 99;SPID=
trap '[ -n "$SPID" ]&&kill "$SPID" 2>/dev/null;rm -rf "$T"' EXIT
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
cat >"$T/chk.py" <<'PY'
import hashlib, http.client, json, os, re, socket, subprocess, sys
a = sys.argv[1:]
K = ("name", "parent", "role", "tier", "boot")
def ld(p): return json.load(open(p))
def out(*v): print("\t".join(str(x) for x in v))
def fm(t): return t.split("\n---", 1)[0]
if a[0] == "export":   # export GWDIR BIN AGI -> build_views JSON (env GRAPHWEB_REV)
    sys.path[:0] = [a[1], a[2]]
    import graphweb; from pathlib import Path
    print(json.dumps(graphweb.build_views(Path(a[3]))))
elif a[0] == "crew":   # crew EXPORT POSTS_TEXT -> got want same
    x = ld(a[1])["crew"]["rows"]
    want = [{k: json.loads(l[4:]).get(k) for k in K} for l in fm(open(a[2]).read()).splitlines() if l.startswith("  - {")]
    out(len(x), len(want), int(x == want))
elif a[0] == "keys":   # keys EXPORT PRIVATE... -> bad-key-rows leaked-values
    x = ld(a[1]); t = json.dumps(x)
    out(sum(1 for r in x["crew"]["rows"] if tuple(r) != K), sum(1 for v in a[2:] if v in t))
elif a[0] == "clocks":  # clocks EXPORT CRONS_TEXT -> got want same (each job: its schedule cell, or every_mins)
    want, job, inside = [], None, False
    for l in fm(open(a[2]).read()).splitlines():
        if re.match(r"^\S", l): inside = l.startswith("cadences:"); job = None; continue
        m = re.match(r"^  ([A-Za-z0-9_]+):\s*$", l)
        if inside and m: job = m.group(1); want.append([job, None]); continue
        m = re.match(r"^    (schedule|every_mins):\s*(.+?)\s*$", l)
        if job and m and (m.group(1) == "schedule" or want[-1][1] is None):
            want[-1][1] = m.group(2) if m.group(1) == "schedule" else "every %s min" % m.group(2)
    got = [[c["job"], c["schedule"]] for c in ld(a[1])["workflow"]["clocks"]]
    out(len(got), len(want), int(got == want), ";".join("%s=%s" % tuple(c) for c in got)[:200])
elif a[0] == "edges":  # edges EXPORT REPO -> got want same edges-as-words
    x = ld(a[1]); names = {r["name"] for r in x["crew"]["rows"]}; w = x["window_s"]
    g = lambda *c: subprocess.run(["git", "-C", a[2], *c], capture_output=True, text=True).stdout
    want = []
    for ref in sorted(g("for-each-ref", "--format=%(refname)", "refs/box/").split()):
        p = ref.split("/")
        if len(p) == 4 and p[2] in names and p[3] in names:
            want.append({"from": p[2], "to": p[3], "count": int(g("rev-list", "--count", "--since=%d seconds ago" % w, ref))})
    got = x["comms"]["edges"]
    out(len(got), len(want), int(got == want), sum(int(e.get("count") or 0) for e in got), " ".join("%s>%s=%s" % (e.get("from"), e.get("to"), e.get("count")) for e in got)[:200] or "-")
elif a[0] == "nosubject":  # nosubject EXPORT TOKEN -> edges-with-extra-keys token-hits
    x = ld(a[1]); out(sum(1 for e in x["comms"]["edges"] if sorted(e) != ["count", "from", "to"]), json.dumps(x).count(a[2]))
elif a[0] == "scan":   # scan EXPORT BIN -> export-hits control-hits (one call)
    sys.path.insert(0, a[2]); import anonymize
    ctl = "fixture contact " + "viz.control" + "@" + "gmail" + ".com"
    out(json.dumps(anonymize.scan(open(a[1]).read(), [])).replace(" ", ""), json.dumps(anonymize.scan(ctl, [])).replace(" ", ""))
elif a[0] == "get":    # get EXPORT KEY.PATH -> the value (json)
    v = ld(a[1])
    for k in a[2].split("."): v = v.get(k) if isinstance(v, dict) else None
    print(json.dumps(v))
elif a[0] == "urls":   # urls WEBDIR -> one line per load site, then BAD <n>
    # load sites: fetch( import( getJSON( src= ; <link href=> (an <a href=> is navigation, not a load: out); CSS url( and @import;
    # new Worker( SharedWorker( WebSocket( EventSource( ; static `import ... from "x"` / `import "x"` / `export ... from "x"`. A protocol-relative //host URL is not relative: it is not an endpoint.
    ok = {"/graph.json", "/live.json", "/commands.json", "/views.json", "/vendor/three.module.min.js", "/app.js"}
    bad = 0
    files = ["app.js", "index.html"] + sorted(x for x in os.listdir(a[1]) if x.endswith(".css") or (x.endswith(".js") and x != "app.js"))
    SITE = re.compile(r'\b(fetch|import|getJSON)\(\s*([^,)]*)'
                      r'|\bsrc=["\']([^"\']*)'
                      r'|(<link\b[^>]*?\bhref=)["\']?([^"\'\s>]*)'
                      r'|(@import)\s+(?:url\(\s*)?["\']?([^"\'\s;)]*)'
                      r'|(?<!@import )(?<![\w-])(url)\(\s*["\']?([^"\')\s]*)'
                      r'|\bnew\s+(Worker|SharedWorker|WebSocket|EventSource)\(\s*([^,)]*)'
                      r'|^\s*((?:import|export)\b[^"\'`;]*?\bfrom|import)\s*["\']([^"\']*)')
    for fn in files:
        t = open(os.path.join(a[1], fn)).read()
        consts = dict(re.findall(r'const\s+([A-Za-z_$][\w$]*)\s*=\s*"([^"]*)"', t))
        for i, l in enumerate(t.splitlines(), 1):
            for m in SITE.finditer(l):
                g = m.groups()
                if g[2] is not None: kind, arg, lit = "src=", g[2], True
                elif g[3] is not None: kind, arg, lit = "link href=", g[4], True
                elif g[5] is not None: kind, arg, lit = "@import", g[6], True
                elif g[7] is not None: kind, arg, lit = "url", g[8], True
                elif g[9] is not None: kind, arg, lit = "new " + g[9], g[10].strip(), False
                elif g[11] is not None: kind, arg, lit = "static " + g[11].split()[0], g[12], True
                else: kind, arg, lit = g[0], g[1].strip(), False
                if lit: u = arg
                elif arg[:1] in "\"'`": u = arg.strip("\"'`")
                elif arg in consts: u = consts[arg]
                elif kind == "fetch" and arg == "p" and "function getJSON(p)" in t: u = "(getJSON's argument: its own sites below)"
                elif kind == "getJSON" and arg == "p" and l.lstrip().startswith("async function getJSON"): continue
                else: u = "UNRESOLVED " + arg
                good = u in ok or u.startswith("(getJSON")
                bad += not good
                print("  site %s:%d %s(%s) -> %s%s" % (fn, i, kind, arg, u, "" if good else "  <- NOT an endpoint"))
    print("BAD", bad)
elif a[0] == "mut":    # mut SRC DST OLD NEW -> the hit line; exit 3 unless OLD occurs exactly once
    t = open(a[1]).read(); n = t.count(a[3])
    if n != 1: print("mutant text occurs %d times in %s" % (n, a[1])); sys.exit(3)
    i = t[:t.index(a[3])].count("\n") + 1
    print("hit %s:%d: %s" % (os.path.basename(a[1]), i, t.splitlines()[i - 1].strip()[:160]))
    open(a[2], "w").write(t.replace(a[3], a[4]))
elif a[0] == "jlist":  # jlist PORT PATH KEY -> the list at KEY, comma-joined (- when empty, null when null, ABSENT when no key)
    try:
        c = http.client.HTTPConnection("127.0.0.1", int(a[1]), timeout=60); c.request("GET", a[2]); b = json.loads(c.getresponse().read()); v = b.get(a[3])
        print("ABSENT" if a[3] not in b else "null" if v is None else ",".join(v) if isinstance(v, list) and v else ("-" if v == [] else "OTHER"))
    except Exception as e: print("ERR", type(e).__name__)
elif a[0] == "port":   # a free loopback port
    s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()
elif a[0] == "http":   # http PORT PATH -> status content-type sha256
    try:
        c = http.client.HTTPConnection("127.0.0.1", int(a[1]), timeout=20); c.request("GET", a[2]); r = c.getresponse(); b = r.read()
        print(r.status, (r.getheader("Content-Type") or "-").split(";")[0], hashlib.sha256(b).hexdigest())
    except Exception as e: print("ERR", type(e).__name__, "-")
elif a[0] == "jget":   # jget PORT PATH [TIMEOUT_S] -> status sha built_at entries unique-non-seat-ids seat-ids
    try:
        c = http.client.HTTPConnection("127.0.0.1", int(a[1]), timeout=int(a[3]) if len(a) > 3 else 60); c.request("GET", a[2]); r = c.getresponse(); b = json.loads(r.read())
        ns = b.get("nodes") or []; ids = {n.get("id") for n in ns}
        out(r.status, b.get("sha"), b.get("built_at"), len(ns), len({i for i in ids if not str(i).startswith("seat:")}), len({i for i in ids if str(i).startswith("seat:")}))
    except Exception as e: out("ERR", type(e).__name__, "-", "-", "-", "-")
PY
py(){ python3 -I "$T/chk.py" "$@";}
pyv(){ py "$@" >"$T/v";A=;B=;C=;D=;E=;F=;IFS='	' read -r A B C D E F <"$T/v";}   # tab-split fields into A..F
# ---------------------------------------------------------------- the fixture
FX=$T/fx;mkdir -p "$FX/.agi/nodes/.geometry"
fg(){ GIT_CONFIG_GLOBAL=/dev/null git -C "$FX" -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=fx -c user.email=fx@example.com "$@";}
fg init -q && fg config core.hooksPath /dev/null || { echo "FAIL inputs: fixture git init";exit 99;}
echo '{}' >"$FX/.agi/config.json"
P3='  - {"name": "a", "parent": "owner", "role": "prime", "tier": 3, "boot": true, "uid": 4242, "home": "/srv/fxhome-a", "persona": "fxpersona-a"}
  - {"name": "b", "parent": "a", "role": "director", "tier": 1, "boot": true, "key": "fxkey-b", "host": "fxhost-b"}
  - {"name": "c", "parent": "a", "role": "council", "tier": 1, "session": "fxsession-c"}'
printf -- '---\nid: config:posts\ntype: config\nposts:\n%s\n---\n\n# posts\n' "$P3" >"$FX/.agi/nodes/.geometry/posts.md"
printf -- '---\nid: cron:crons\ntype: cron\ncadences:\n  job_one:\n    schedule: 7 * * * *\n    enabled: true\n  job_two:\n    every_mins: 30\n    enabled: false\ncrons_live: true\n---\n' >"$FX/.agi/nodes/.geometry/crons.md"
fg add -A && fg commit -qm "S: three posts" || { echo "FAIL inputs: fixture commit S";exit 99;}
S=$(fg rev-parse HEAD)
printf -- '---\nid: config:posts\ntype: config\nposts:\n%s\n  - {"name": "d", "parent": "b", "role": "parent", "tier": 2}\n---\n' "$P3" >"$FX/.agi/nodes/.geometry/posts.md"
fg commit -qam "S-prime: four posts";SP=$(fg rev-parse HEAD)
ET=$(fg mktree </dev/null)
box(){ r=$1;n=$2;p=;i=0;while [ $i -lt "$n" ];do i=$((i+1));c=$(fg commit-tree $ET ${p:+-p $p} -m "BOXSUBJ $r $i" -m "BOXBODY $r $i");p=$c;done;fg update-ref "refs/box/$r" "$p";}
box a/b 3;box b/a 1;box a/zz 2
c=$(GIT_COMMITTER_DATE='2001-01-01T00:00:00Z' GIT_AUTHOR_DATE='2001-01-01T00:00:00Z' fg commit-tree $ET -m "BOXSUBJ c/a old");fg update-ref refs/box/c/a "$c"
FX2=$T/fx2;mkdir -p "$FX2/.agi";echo '{}' >"$FX2/.agi/config.json"
GIT_CONFIG_GLOBAL=/dev/null git -C "$FX2" init -q;GIT_CONFIG_GLOBAL=/dev/null git -C "$FX2" config core.hooksPath /dev/null
GIT_CONFIG_GLOBAL=/dev/null git -C "$FX2" -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=fx -c user.email=fx@example.com commit -q --allow-empty -m "empty source"
# ---------------------------------------------------------------- the rows (each takes the graphweb dir GW, so a mutant re-runs it on a copy)
xp(){ GRAPHWEB_REV=$3 py export "$1" "$BIN" "$2";}   # xp GW AGI [REV] -> export JSON
r_crew(){ GW=$1;xp "$GW" "$FX/.agi" "$S" >"$T/xs.json";xp "$GW" "$FX/.agi" "" >"$T/xh.json"
 fg show "$S:.agi/nodes/.geometry/posts.md" >"$T/ps";fg show "$SP:.agi/nodes/.geometry/posts.md" >"$T/psp"
 pyv crew "$T/xs.json" "$T/ps";ok "f-crew-rows-at-the-exports-sha export at S ($(echo $S|cut -c1-12)): $A crew row(s), posts.md at S: $B (want equal rows, the five keys each: $C=1)" '[ "$C" = 1 ]'
 pyv crew "$T/xh.json" "$T/psp";ok "f-crew-rows-at-head export at HEAD=S' ($(echo $SP|cut -c1-12)): $A crew row(s), posts.md at S': $B (want equal: $C=1)" '[ "$C" = 1 ]';}
r_keys(){ xp "$1" "$FX/.agi" "$S" >"$T/xk.json";pyv keys "$T/xk.json" 4242 /srv/fxhome-a fxpersona-a fxkey-b fxhost-b fxsession-c
 ok "f-crew-carries-only-name-parent-role-tier-boot $A row(s) with any other key, $B of the fixture's uid, home, persona, key, host and session values in the export (want 0 0)" '[ "$A" = 0 ]&&[ "$B" = 0 ]';}
r_clocks(){ xp "$1" "$FX/.agi" "$S" >"$T/xc.json";fg show "$S:.agi/nodes/.geometry/crons.md" >"$T/cs"
 pyv clocks "$T/xc.json" "$T/cs";ok "f-each-clock-is-its-crons-md-cell $A clock(s), crons.md at S: $B job(s), [$D] (want equal: $C=1)" '[ "$C" = 1 ]';}
r_edges(){ xp "$1" "$FX/.agi" "$S" >"$T/xe.json";pyv edges "$T/xe.json" "$FX"
 ok "f-each-edge-count-is-rev-list-count $A edge(s) [$E] total $D, refs/box between posts: $B (want equal, a>b=3 b>a=1 c>a=0, a/zz not a post: $C=1)" '[ "$C" = 1 ]&&[ "$E" = "a>b=3 b>a=1 c>a=0" ]';}
r_nosubj(){ xp "$1" "$FX/.agi" "$S" >"$T/xn.json";pyv nosubject "$T/xn.json" BOX;ok "f-no-box-subject-or-body $A edge(s) with a key beyond from/to/count, $B 'BOX' (subject/body) token(s) in the export (want 0 0)" '[ "$A" = 0 ]&&[ "$B" = 0 ]';}
r_sha(){ xp "$1" "$FX/.agi" "" >"$T/xa.json";h=$(py get "$T/xa.json" sha|tr -d '"');b=$(py get "$T/xa.json" built_at|tr -d '"')
 ok "f-export-names-the-fixture-head-sha-and-built-at sha $(echo $h|cut -c1-12) (fixture HEAD $(echo $SP|cut -c1-12)), built_at $b (want equal + UTC ISO)" '[ "$h" = "$SP" ]&&echo "$b"|grep -qE "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z$"';}
r_scan(){ xp "$1" "$FX/.agi" "$S" >"$T/xz.json";pyv scan "$T/xz.json" "$BIN"
 ok "f-anonymize-scan-clean-beside-a-control-that-flags export $A (want []), control $B (want [\"email\"]), one call" '[ "$A" = "[]" ]&&[ "$B" = "[\"email\"]" ]';}
r_empty(){ xp "$1" "$FX2/.agi" "" >"$T/x0.json";w=$(py get "$T/x0.json" crew.read_nothing);n=$(py get "$T/x0.json" crew.rows)
 ok "e-empty-source-says-read-nothing crew.read_nothing $w, rows $n (want words naming posts.md and the sha, rows [])" '[ "$n" = "[]" ]&&echo "$w"|grep -q "read nothing (posts.md"';}
# d: the footer names the node files that differ from the shown commit, in words (the export's uncommitted_nodes; the page's setFoot)
DN=.agi/nodes/.geometry/posts.md;DU=.agi/nodes/idea/fx-untracked.md
dirty(){ printf '\n# dirty\n' >>"$FX/$DN";mkdir -p "$FX/.agi/nodes/idea";printf -- '---\nid: idea:fx-untracked\n---\n' >"$FX/$DU";}
clean(){ fg checkout -q -- "$DN";rm -rf "$FX/.agi/nodes/idea";}
r_dirty(){ xp "$1" "$FX/.agi" "" >"$T/xd0.json";c0=$(py get "$T/xd0.json" uncommitted_nodes);dirty;xp "$1" "$FX/.agi" "" >"$T/xd1.json";clean;c1=$(py get "$T/xd1.json" uncommitted_nodes)
 ok "d-export-names-each-uncommitted-node-file clean fixture $c0 (want []), one modified + one untracked node file $c1 (want [\"$DN\", \"$DU\"])" '[ "$c0" = "[]" ]&&[ "$c1" = "[\"$DN\", \"$DU\"]" ]';}
# the footer: app.js's own setFoot + dirtyWords, run by node on a stub element (the one piece of draw code this lane executes)
cat >"$T/foot.js" <<'JS'
const t = require("fs").readFileSync(process.argv[2], "utf8");
const grab = (n) => { const i = t.indexOf("function " + n + "("); if (i < 0) return ""; const j = t.indexOf("\n}\n", i); return t.slice(i, j + 2); };
const el = { textContent: "" }; const document = { getElementById: () => el };
eval(grab("setFoot") + grab("dirtyWords"));
const out = [];
for (const l of [[], [process.argv[3]], ["a", "b", "c", "d", "e"], null]) { setFoot({ sha: "0123456789abcdef", built_at: "T", uncommitted_nodes: l }); out.push(el.textContent); }
console.log(out.join("\t"));
JS
# an UNREAD status (FX3: no repo; GIT_CEILING_DIRECTORIES=$T keeps git from finding one above it) reads unread in words, never clean
FX3=$T/fx3;mkdir -p "$FX3/.agi/nodes";echo '{}' >"$FX3/.agi/config.json";printf -- '---\nid: idea:fx3\n---\n' >"$FX3/.agi/nodes/fx3.md"
r_unread(){ GIT_CEILING_DIRECTORIES=$T xp "$1" "$FX3/.agi" "" >"$T/xu.json";u=$(py get "$T/xu.json" uncommitted_nodes);w=$(py get "$T/xu.json" uncommitted_read_nothing)
 rc=$(GIT_CEILING_DIRECTORIES=$T git -C "$FX3" status >/dev/null 2>&1;echo $?);xp "$1" "$FX/.agi" "" >"$T/xc0.json";w0=$(py get "$T/xc0.json" uncommitted_read_nothing)
 ok "d-unread-status-says-unread-never-clean no repo (git status rc $rc): uncommitted_nodes $u (want null), words $w (want 'uncommitted node files: unread ..'); a clean repo's words $w0 (want null)" '[ "$u" = null ]&&echo "$w"|grep -q "uncommitted node files: unread"&&[ "$w0" = null ]&&[ "$rc" != 0 ]';}
# no nodes directory (FX2, a repo whose .agi holds none) reads unread too; a WORKTREE-column rename (git add -N) names the new path alone
r_nonodes(){ xp "$1" "$FX2/.agi" "" >"$T/xnn.json";u=$(py get "$T/xnn.json" uncommitted_nodes);w=$(py get "$T/xnn.json" uncommitted_read_nothing)
 ok "d-no-nodes-directory-says-unread a repo with no .agi/nodes: uncommitted_nodes $u (want null), words $w (want 'uncommitted node files: unread ..')" '[ "$u" = null ]&&echo "$w"|grep -q "uncommitted node files: unread"';}
FX4=$T/fx4;cp -r "$FX" "$FX4";f4(){ GIT_CONFIG_GLOBAL=/dev/null git -C "$FX4" -c core.hooksPath=/dev/null "$@";}
mv "$FX4/.agi/nodes/.geometry/crons.md" "$FX4/.agi/nodes/.geometry/crons-moved.md";f4 add -N .agi/nodes/.geometry/crons-moved.md
r_wtrename(){ st=$(f4 status --porcelain=v1|tr '\n' ';');xp "$1" "$FX4/.agi" "" >"$T/xwr.json";u=$(py get "$T/xwr.json" uncommitted_nodes)
 ok "d-worktree-rename-names-the-new-path-alone status [$st] -> $u (want [\".agi/nodes/.geometry/crons-moved.md\"], never the source cut to a path that does not exist)" '[ "$u" = "[\".agi/nodes/.geometry/crons-moved.md\"]" ]&&echo "$st"|grep -q "^ R "';}
r_unreadhttp(){ P=$(py port)
 GIT_CEILING_DIRECTORIES=$T python3 -I -c 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];import graphweb;graphweb.main(["serve","--port",sys.argv[3],"--root",sys.argv[4]])' "$1" "$BIN" "$P" "$FX3/.agi" >/dev/null 2>"$T/serve3.err" &
 SPID=$!;i=0;while [ $i -lt 100 ]&&[ -z "$(ss -Hltn "sport = :$P" 2>/dev/null)" ];do i=$((i+1));sleep 0.1;done
 GU=$(py jlist "$P" /graph.json uncommitted_nodes);VU=$(py jlist "$P" /views.json uncommitted_nodes);kill "$SPID" 2>/dev/null;wait "$SPID" 2>/dev/null;SPID=
 ok "p-unread-status-is-null-in-both-exports no repo: /graph.json [$GU], /views.json [$VU] (want null each, never - which reads clean)" '[ "$GU" = null ]&&[ "$VU" = null ]';}
r_foot(){ if ! command -v node >/dev/null;then echo "FAIL d-footer-says-so-in-words node absent: the footer row is unread, never a pass";f=$((f+1));return;fi
 node "$T/foot.js" "$1/app.js" "$DN" >"$T/v" 2>&1;A=;B=;C=;D=;IFS='	' read -r A B C D <"$T/v"
 ok "d-footer-says-so-in-words none [$A] (want no 'uncommitted'), one [$B] (want '1 uncommitted node file: $DN'), five [$C] (want '5 uncommitted node files: a, b, c (+2 more)'), unread (null) [$D] (want 'uncommitted node files: unread')" 'echo "$A"|grep -qv uncommitted&&echo "$B"|grep -qF "· 1 uncommitted node file: $DN"&&echo "$C"|grep -qF "· 5 uncommitted node files: a, b, c (+2 more)"&&echo "$D"|grep -qF "· uncommitted node files: unread"';}
# a: every fetch( import( getJSON( src= site resolves to one graphweb endpoint
r_urls(){ py urls "$1" >"$T/u";cat "$T/u"|grep '^  site';b=$(sed -n 's/^BAD //p' "$T/u")
 ok "a-every-page-url-is-a-relative-graphweb-endpoint $(grep -c '^  site' "$T/u") site(s) above, $b not one of /graph.json /live.json /commands.json /views.json /vendor/three.module.min.js /app.js (want 0)" '[ "$b" = 0 ]';}
# b: the lines graphweb.py ADDS vs this build's PARENT (pinned sha; env BASE overrides, printed) hold no write verb or write mode
WR='open\([^)]*["'"'"'][wax+]|\.write_(text|bytes)\(|mkdir|touch\(|update-ref|commit-tree|write-tree|hash-object|git push|"push"|os\.(rename|replace|remove|unlink)|shutil\.'
r_nowrite(){ # r_nowrite TIPDIR [REPO [REV]]: graphweb.py in TIPDIR vs REPO's graphweb.py at REV (default ROOT at ${BASE:-the pinned parent})
 rp=${2:-$R0};rv=${3:-${BASE:-$PIN_PARENT}};lab=pinned;[ -n "$3" ]&&lab=given;[ -z "$3" ]&&[ -n "$BASE" ]&&lab="BASE override"
 bs=$(git -C "$rp" rev-parse --verify -q "$rv^{commit}" 2>/dev/null);: >"$T/gw.base";[ -n "$bs" ]&&git -C "$rp" show "$bs:extensions/agi/bin/graphweb.py" >"$T/gw.base" 2>/dev/null
 if [ -z "$bs" ]||[ ! -s "$T/gw.base" ];then echo "FAIL b-graphweb-added-lines-hold-no-write SETUP: base $rv ($lab) unread (rev-parse ${bs:-failed}; graphweb.py at it ${bs:+empty or absent}): an unread base is never a pass";f=$((f+1));return;fi
 diff "$T/gw.base" "$1/graphweb.py"|grep '^>' >"$T/add";h=$(grep -cE "$WR" "$T/add");grep -nE "$WR" "$T/add"|sed 's/^/  write-hit /'
 ok "b-graphweb-added-lines-hold-no-write $(wc -l <"$T/add"|tr -d ' ') line(s) added vs $bs ($lab: $rv), $h with a write verb/mode (want 0)" '[ "$h" = 0 ]';}
# c: no absolute URL under web/graph; the control (one absolute URL in a temp copy) prints 1
# gg DIR ERE [FILES]: git grep -n -E over DIR (no index: a temp copy greps the same way); prints the hits, then the count; a git error is a count of ERR
gg(){ d=$1;e=$2;shift 2;[ $# -eq 0 ]&&set -- .;( cd "$d"&&git grep --no-index -n -E "$e" -- "$@" );rc=$?;[ $rc -gt 1 ]&&echo ERR;}
# CE: an absolute address, scheme or protocol-relative (a quote, paren or = then //host)
CE='(https?|wss?)://|["'"'"'(=]//[A-Za-z0-9]'
r_abs(){ gg "$1" "$CE" >"$T/g";n=$(grep -c . "$T/g");grep -q '^ERR$' "$T/g"&&n=ERR;sed 's/^/  abs-url /' "$T/g"
 ok "c-no-absolute-url-under-web-graph $n line(s) match $CE (want 0)" '[ "$n" = 0 ]';}
r_pagenoread(){ gg "$1" 'open\(.*[wa]|subprocess|refs/box' app.js index.html >"$T/g";n=$(grep -c . "$T/g");grep -q '^ERR$' "$T/g"&&n=ERR
 ok "c-the-page-never-reads-the-repo-refs-or-a-box $n line(s) of open(..w/a / subprocess / refs/box in app.js + index.html (want 0)" '[ "$n" = 0 ]';}
# p: graphweb serve with the DEFAULT host listens on 127.0.0.1 only; it serves /views.json, the pinned vendor file and nothing else under /vendor/
r_port(){ P=$(py port);sys_gw=$1
 python3 -I -c 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];import graphweb;graphweb.main(["serve","--port",sys.argv[3],"--root",sys.argv[4]])' "$sys_gw" "$BIN" "$P" "$FX/.agi" >/dev/null 2>"$T/serve.err" &
 SPID=$!;i=0;L=
 while [ $i -lt 100 ];do L=$(ss -Hltn "sport = :$P" 2>/dev/null|awk '{print $4}'|tr '\n' ' ');[ -n "$L" ]&&break;i=$((i+1));sleep 0.1;done
 L=${L% };ok "p-graphweb-listens-on-loopback-only port $P listeners [$L] (want exactly 127.0.0.1:$P)" '[ "$L" = "127.0.0.1:$P" ]'
 if [ -n "$L" ];then V=$(py http "$P" /views.json);G=$(py http "$P" /vendor/three.module.min.js);N=$(py http "$P" /vendor/LICENSE)
  ok "p-serves-views-json-and-the-pinned-vendor-file /views.json [$(echo $V|cut -c1-40)], /vendor/three.module.min.js [$(echo $G|cut -c1-30)..] (want 200 application/json; 200 text/javascript sha256 = PIN.txt)" '[ "${V%% *}" = 200 ]&&[ "$(echo $G|cut -d" " -f1-2)" = "200 text/javascript" ]&&grep -q "sha256: $(echo $G|cut -d" " -f3)" "$R0/extensions/agi/web/vendor/three/PIN.txt"'
  pyv jget "$P" /graph.json;ok "p-graph-json-names-its-sha-and-built-at /graph.json [$A] sha $(echo $B|cut -c1-12) (fixture HEAD $(echo $SP|cut -c1-12)), built_at $C, $D node(s) (want 200, equal, UTC ISO)" '[ "$A" = 200 ]&&[ "$B" = "$SP" ]&&echo "$C"|grep -qE "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z$"'
  dirty;GD=$(py jlist "$P" /graph.json uncommitted_nodes);VD=$(py jlist "$P" /views.json uncommitted_nodes);clean
  ok "p-graph-and-views-json-name-the-uncommitted-node-files one modified + one untracked: /graph.json [$GD], /views.json [$VD] (want $DN,$DU each)" '[ "$GD" = "$DN,$DU" ]&&[ "$VD" = "$DN,$DU" ]'
  ok "p-nothing-else-under-vendor /vendor/LICENSE -> [$(echo $N|cut -d" " -f1)] (want 404)" '[ "${N%% *}" = 404 ]';fi
 kill "$SPID" 2>/dev/null;wait "$SPID" 2>/dev/null;SPID=;}
# live: ROOT's own trunk at its HEAD (posts.md / crons.md read back at that one sha; refs/box as the clone holds them)
r_live(){ LS=$(git -C "$R0" rev-parse HEAD);xp "$BIN" "$R0/.agi" "" >"$T/xl.json";git -C "$R0" show "$LS:.agi/nodes/.geometry/posts.md" >"$T/lp";git -C "$R0" show "$LS:.agi/nodes/.geometry/crons.md" >"$T/lc"
 pyv crew "$T/xl.json" "$T/lp";ok "live-crew-rows-are-config-posts-rows at $(echo $LS|cut -c1-12): $A row(s), posts.md: $B (want equal: $C=1)" '[ "$C" = 1 ]'
 pyv clocks "$T/xl.json" "$T/lc";ok "live-each-clock-is-its-crons-md-cell $A clock(s), crons.md: $B job(s) (want equal: $C=1)" '[ "$C" = 1 ]'
 pyv edges "$T/xl.json" "$R0";rn=$(py get "$T/xl.json" comms.read_nothing)
 ok "live-each-edge-count-is-rev-list-count $A edge(s) (total count $D over the window), refs/box between posts: $B (want equal: $C=1; none -> read_nothing $(echo "$rn"|cut -c1-60)..)" '[ "$C" = 1 ]&&{ [ "$A" -gt 0 ]||[ "$rn" != null ];}'
 h=$(py get "$T/xl.json" sha|tr -d '"');pyv scan "$T/xl.json" "$BIN"
 ok "live-one-sha-and-scan-clean export sha $(echo $h|cut -c1-12) (want HEAD $(echo $LS|cut -c1-12)), scan $A (want []), control $B (want [\"email\"])" '[ "$h" = "$LS" ]&&[ "$A" = "[]" ]&&[ "$B" = "[\"email\"]" ]';}
# live-nodes (leaf Falsifier 1 'nodes == the verify count'): /graph.json as the page reads it (HTTP from `graphweb serve`) over a COPY of ROOT's
# .agi (nodes + context + config; ROOT's persisted layout copied too when it has one, else the build is cold: minutes) vs active_node_count from
# the reader verify uses: the smoke check's METRIC active_node_count (verification.py:364) = metrics.compute's node_count = len(_load_graph)
# (metrics.py:1053) minus node_lifecycle_stats' deprecated count (metrics.py:1060, :332). The verify COMMAND is not run: its smoke check is
# driver.sh --smoke (snapshot + render: it writes into the tree) and its metrics stage alone takes ~75 s here.
# Like with like: graphweb draws ACTIVE nodes minus nodes/.geometry/ (config, drawn as synthetic seat:<name> nodes instead), and ROOT goal:g17 twice
# (once per layer): so unique non-seat ids == active_node_count - the non-deprecated .geometry node files.
LA=$T/live/.agi;mkdir -p "$LA";cp -r "$R0/.agi/nodes" "$R0/.agi/context" "$R0/.agi/config.json" "$LA/" 2>/dev/null
WARM=no;[ -f "$R0/.agi/sessions/graphweb-layout.json" ]&&mkdir -p "$LA/sessions"&&cp "$R0/.agi/sessions/graphweb-layout.json" "$LA/sessions/"&&WARM=yes
VC=$(timeout "${VERIFY_TIMEOUT:-300}" python3 -I -c 'import sys;sys.path.insert(0,sys.argv[1]);from pathlib import Path;import metrics;r=Path(sys.argv[2]);g=metrics._load_graph(r);print(metrics.node_lifecycle_stats(r/"nodes",len(g))["active_node_count"])' "$BIN" "$LA" 2>/dev/null)
GEO=0;for x in $(find "$LA/nodes/.geometry" -name '*.md' 2>/dev/null);do sed -n '2,/^---/p' "$x"|grep -qE '^status: *deprecated'||GEO=$((GEO+1));done
r_livenodes(){ P=$(py port)
 python3 -I -c 'import sys;sys.path[:0]=[sys.argv[1],sys.argv[2]];import graphweb;graphweb.main(["serve","--port",sys.argv[3],"--root",sys.argv[4]])' "$1" "$BIN" "$P" "$LA" >/dev/null 2>"$T/serve2.err" &
 SPID=$!;i=0;while [ $i -lt 100 ]&&[ -z "$(ss -Hltn "sport = :$P" 2>/dev/null)" ];do i=$((i+1));sleep 0.1;done
 pyv jget "$P" /graph.json "${GRAPH_TIMEOUT:-900}";kill "$SPID" 2>/dev/null;wait "$SPID" 2>/dev/null;SPID=
 ok "live-graph-json-nodes-equal-the-verify-active-count /graph.json [$A]: $D entries = $E unique non-seat ids + $F seat:<name> + goal:g17 once more (layer 1); verify's reader (metrics.py:1053 len(_load_graph) - metrics.py:332 deprecated, parsed at verification.py:364): active_node_count ${VC:-UNREAD}, minus $GEO non-deprecated nodes/.geometry/ file(s) graphweb draws as seats = $(( ${VC:-0} - GEO )) (want $E = that; layout warm: $WARM)" '[ "$A" = 200 ]&&[ -n "$VC" ]&&[ "$E" = "$((VC-GEO))" ]';}
r_crew "$BIN";r_keys "$BIN";r_clocks "$BIN";r_edges "$BIN";r_nosubj "$BIN";r_sha "$BIN";r_scan "$BIN";r_empty "$BIN"
r_dirty "$BIN";r_unread "$BIN";r_nonodes "$BIN";r_wtrename "$BIN";r_unreadhttp "$BIN";r_foot "$WEB";r_urls "$WEB";r_nowrite "$BIN";r_abs "$WEB"
mkdir -p "$T/ctl";cp "$WEB/app.js" "$WEB/index.html" "$T/ctl/";printf '\n// control: https://example.invalid/x.js\n' >>"$T/ctl/app.js"
gg "$T/ctl" "$CE" >"$T/g";n=$(grep -c . "$T/g");grep -q '^ERR$' "$T/g"&&n=ERR;sed 's/^/  control /' "$T/g";ok "c-control-one-absolute-url-in-a-temp-copy-prints-1 $n (want 1)" '[ "$n" = 1 ]'
r_pagenoread "$WEB";r_port "$BIN";r_live;r_livenodes "$BIN"
# ---------------------------------------------------------------- mutants: each on a COPY, the old text exactly once, its row must read RED
M=$T/m;mkdir -p "$M"
mut(){ # mut NAME FILE ROWFN OLD NEW: copy, mutate, re-run ROWFN on the copy's dir
 rm -rf "$M/$1";mkdir -p "$M/$1";hit=$(py mut "$2" "$M/$1/$(basename "$2")" "$4" "$5")||{ echo "FAIL m-$1 $hit";f=$((f+1));return;}
 case $2 in "$WEB"/*) for x in $(ls "$WEB");do [ -e "$M/$1/$x" ]||cp "$WEB/$x" "$M/$1/";done;;esac   # (set -f: no glob; ls lists the page dir)
 out=$($3 "$M/$1");r=$(echo "$out"|grep -c '^FAIL')
 ok "m-$1-turns-its-row-red $hit -> $r RED row(s): $(echo "$out"|grep '^FAIL'|cut -c1-90|head -2|tr '\n' ' ')" '[ "$r" -ge 1 ]';}
GW=$BIN/graphweb.py
mut hardcoded-clock "$GW" r_clocks '"schedule": _clock(j)' '"schedule": "7 * * * *"'
mut box-subject-on-an-edge "$GW" r_nosubj '"count": int(n.strip())}' '"count": int(n.strip()), "subject": (_git(source_root(graph_root), "log", "-1", "--format=%s", ref) or "").strip()}'
mut edge-count-plus-one "$GW" r_edges '"count": int(n.strip())' '"count": int(n.strip()) + 1'
mut a-second-reader-at-another-rev "$GW" r_crew '_frontmatter_at(graph_root, sha, "posts.md")' '_frontmatter_at(graph_root, head_sha(graph_root, "HEAD"), "posts.md")'
mut view-emptied-read-nothing-removed "$GW" r_empty '"crew": {"rows": crew, "read_nothing": crew_rn}' '"crew": {"rows": [], "read_nothing": None}'
mut view-emptied-read-nothing-removed-crew "$GW" r_crew '"crew": {"rows": crew, "read_nothing": crew_rn}' '"crew": {"rows": [], "read_nothing": None}'
mut absolute-url-in-app-js "$WEB/app.js" r_abs 'const THREE_URL = "/vendor/three.module.min.js";' 'const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";'
mut absolute-url-in-app-js-site "$WEB/app.js" r_urls 'const THREE_URL = "/vendor/three.module.min.js";' 'const THREE_URL = "https://unpkg.com/three@0.160.0/build/three.module.js";'
H=$WEB/index.html
mut link-href-protocol-relative-font "$H" r_urls '</head>' '<link rel="stylesheet" href="//fonts.googleapis.com/css2?family=Inter">
</head>'
mut css-import-protocol-relative-font "$H" r_urls '<style>' '<style>
  @import url(//fonts.googleapis.com/css2?family=Inter);'
mut new-worker-protocol-relative "$WEB/app.js" r_urls '"use strict";' '"use strict";
new Worker("//cdn.example.org/w.js");'
# control: an <a href=> is navigation, not a load: planted alone on a copy, row a stays GREEN
rm -rf "$M/ctl-a";mkdir -p "$M/ctl-a";for x in $(ls "$WEB");do cp "$WEB/$x" "$M/ctl-a/";done;hit=$(py mut "$H" "$M/ctl-a/index.html" '</body>' '<a href="//example.org/">x</a>
</body>');out=$(r_urls "$M/ctl-a");r=$(echo "$out"|grep -c '^FAIL')
ok "m-control-a-href-is-navigation-stays-green $hit -> $r RED row(s) (want 0: an <a href> is not a load site)" '[ "$r" = 0 ]&&echo "$hit"|grep -q "^hit "'
mut c-link-href-protocol-relative-font "$WEB/index.html" r_abs '</head>' '<link rel="stylesheet" href="//fonts.googleapis.com/css2?family=Inter">
</head>'
mut c-three-url-protocol-relative "$WEB/app.js" r_abs 'const THREE_URL = "/vendor/three.module.min.js";' 'const THREE_URL = "//unpkg.com/three@0.160.0/build/three.module.js";'
mut open-w-added "$GW" r_nowrite '    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")' '    return open(os.devnull, "w").close() or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")'
mut node-dropped-from-build-graph "$BIN/graphweb.py" r_livenodes 'out_nodes = nodes_out(layer0, pos0, 0) + nodes_out(layer1, pos1, 1)' 'out_nodes = (nodes_out(layer0, pos0, 0) + nodes_out(layer1, pos1, 1))[1:]'
FB=$T/fb;mkdir -p "$FB/extensions/agi/bin";fb(){ GIT_CONFIG_GLOBAL=/dev/null git -C "$FB" -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=fx -c user.email=fx@example.com "$@";}
fb init -q;fb config core.hooksPath /dev/null;git -C "$R0" show "$PIN_PARENT:extensions/agi/bin/graphweb.py" >"$FB/extensions/agi/bin/graphweb.py" 2>/dev/null
fb add -A;fb commit -qm "base: the pinned parent's graphweb.py";B0=$(fb rev-parse HEAD)
printf '%s\n' '_W = open(p, "w")' >>"$FB/extensions/agi/bin/graphweb.py";fb commit -qam "c1: one write line";echo note >"$FB/note.txt";fb add note.txt;fb commit -qm "c2: graphweb.py untouched"
v1=$(fb diff HEAD~1 HEAD -- extensions/agi/bin/graphweb.py|grep '^+'|grep -v '^+++'|grep -cE "$WR")
out=$(r_nowrite "$FB/extensions/agi/bin" "$FB" "$B0");r=$(echo "$out"|grep -c '^FAIL')
ok "m-b-pinned-base-sees-a-write-two-commits-back fixture: base = the pinned parent's graphweb.py ($(echo $B0|cut -c1-12)), c1 adds 'open(p, \"w\")', c2 touches no graphweb.py; at c2 a HEAD~1 diff finds $v1 write line(s) (the vacuous pass), the pinned-base row -> $r RED row(s): $(echo "$out"|grep '^FAIL'|cut -c1-110)" '[ "$r" -ge 1 ]&&[ "$v1" = 0 ]'
mut export-drops-uncommitted-nodes "$GW" r_dirty '**uncommitted_fields(graph_root),' '"uncommitted_nodes": [],'
mut graph-json-drops-uncommitted-nodes "$GW" r_port 'g.update(uncommitted_fields(self.graph_root))' 'g["uncommitted_nodes"] = []'
mut unread-status-reads-clean "$GW" r_unread 'if out is None:
        return None
    paths, items = [], out.split(' 'paths, items = [], (out or "").split('
mut unread-status-reads-clean-http "$GW" r_unreadhttp 'if out is None:
        return None
    paths, items = [], out.split(' 'paths, items = [], (out or "").split('
mut no-nodes-dir-reads-clean "$GW" r_nonodes 'if not (root / "nodes").is_dir():' 'if False:'
mut rename-index-column-only "$GW" r_wtrename 'if e[0] in "RC" or e[1] in "RC":' 'if e[0] in "RC":'
mut footer-unread-reads-clean "$WEB/app.js" r_foot 'if (!Array.isArray(list)) return " · uncommitted node files: unread";' 'list = list || [];'
mut footer-drops-the-words "$WEB/app.js" r_foot '" · built " + (d.built_at || "unknown") + dirtyWords(d.uncommitted_nodes);' '" · built " + (d.built_at || "unknown");'
mut status-misses-untracked "$GW" r_dirty '"--untracked-files=all", "--",' '"--untracked-files=no", "--",'
mut static-import-protocol-relative "$WEB/app.js" r_urls '"use strict";' '"use strict";
import * as X from "//cdn.example.org/x.js";'
mut host-default-0000 "$GW" r_port 'serve_p.add_argument("--host", default="127.0.0.1")' 'serve_p.add_argument("--host", default="0.0.0.0")'
echo "viz-views: $f FAIL"
exit $f
