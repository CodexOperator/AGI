---
id: config:engine
mint_id: e228cdddac334a71b2764fb2fb26821b
type: config
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: belam
scaffold_hash: 1a5628596065214d
season: 2
town: core
---
# config:engine — the ZYGOTE: the code that runs before any post exists + the map of 39 pieces (42 `###` blocks in engine*.md: agi-boot, agi-boot.service and matrix are not mapped)
Depth 0 = diagram · 1 = loop + pieces · 2 = one piece: `sect <name>` (any `.geometry/engine*.md`: this node, config:engine-post, config:engine-wrap, config:engine-grow, config:engine-root) · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

## diagram — depth 0
~~~
   GRAPH = git @trunk: .agi/nodes, edges = parents: · a post opts in by ONE row cell "engine": {"v": 4, ...}
   root, once ──▶ agi-project (FROM this node @REV) ──▶ BODY: user · unit in agi.slice · env cells
   unit ──▶ own uid · worktree ~/t of MAIN on posts/<p> · pane = fifo i + typescript o (script) · strace
   start|resume|compact ──CC hooks, or pi via cccc.ts──▶ agi-brief: walk(card+seeds+claims) + STARTUP
   prompt ──▶ agi-meter: at the line: card, .fresh, kill ──▶ Restart = a FRESH successor
   turn end ──▶ agi-turn: one signed commit · agi-link · released agi-wt trees dropped · mail = a turn
   stop ──▶ agi-flush ──▶ the master lands posts/<p> ──▶ agi-project re-runs ──▶ next brief sees it
   harness: claude --remote-control <p> · grok-bot --model --effort --permission-mode (hooks native; the owner's app lists it) · pi + cccc.ts · agi-kid
   tick: project(graph) == observe(body)? equal = alive · differ = start it + a drift commit
   ZYGOTE = this read (map · sect · agi-project · agi-gate) ──sect @REV──▶ EXPANSION: config:engine-post · config:engine-wrap · config:engine-grow · config:engine-root
~~~

## loop — depth 1
~~~
1 BOOT   root runs agi-project @REV: unit, user, cells for engine.v==4 rows; dropped rows unlinked
2 START  PSI admission; key, worktree, tools from this node; .fresh = new session, else -c resumes
3 WORK   brief in the system prompt; plain paths in ~/t; inbox, budget, records resolve to MAIN
4 TURN   one signed commit; agi-link; at the line: card, touch ~/.fresh, kill $PPID = rotation
5 LAND   ExecStopPost agi-flush; the master gates posts/<p> onto the trunk (skill agi-master-gate)
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service 1801 B  a post = one unit in agi.slice: own uid, tree, key, pane
agi-run           501 B  pane cmd: .fresh or -c, under strace; claude: mail -> i
settings.json      342 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1647 B  pi events -> those CC hooks; inbox growth -> a turn
agi-kid           2037 B  a pi-free kid in this unit: own HOME, tree, cccc.ts
agi-infer          1077 B  ONE chat call, OpenAI-compatible: stdin -> stdout
agi-brief          938 B  walk card+seeds+claims; record; STARTUP
brief.py           810 B  the complex walk over parents: edges
agi-meter          439 B  past rotate_pct of the window: the out-line
agi-turn           269 B  drop released trees; signed commit; agi-link
agi-link           358 B  node <-> code file via payload_ref
agi-wt             688 B  a node's tiny RAM tree: pull; drop = commit+purge
agi-track           89 B  strace sink: each path once
agi-flush          181 B  on exit: drop trees, commit, merge trunk
agi-out           3120 B  the out-line: next keys, ONE ring commit, re-wrap, swap
gitconfig          198 B  signed commits, verified against the root-owned allowed_signers, own hooks
sysusers.conf       41 B  a post = one user in group agi
agi.rules          211 B  group agi may start agi-post@ units
project.sh         161 B  what the body SHOULD be
observe.sh         255 B  what the body IS
tick.sh            254 B  diff them; start the drift; commit
agi-project       1841 B  the genome: units + cells for v4 rows
agi-frontier       460 B  each active goal runs its falsifier
agi-gate           404 B  refuse a tip whose body would not regrow; one name, one piece
sect               214 B  ONE piece of any engine*.md node, byte-exact, any REV
agi-fill          5973 B  a node key opens a captive fill window
agi-captive        576 B  window open: only agi-fill passes
grow-check        1298 B  one node vs its matrix row + key
grow-gate         6335 B  pre-receive: added/changed nodes must pass
grow-project      1185 B  schemas -> the growth matrix
agi-land          1855 B  root: ff-lands a post range on the trunk, one parent edge up (ring-signed, grow-gate, agi-gate)
box               2005 B  mail: one signed ref update per send (5x CAS), read from the store
box-carry         3246 B  root: P's refs/box/P/<Q> -> the recipient's store (pipe, ff-only) or the hub; --fetch = the timer
agi-signers       1727 B  root: the ONE allowed_signers, every key generation, valid-after/before; one strict key line
agi-carry@.path     149 B  PathChanged on the sender's own refs/box/<P> (a unit on refs/box fires only on the first send)
agi-carry@.service  287 B  oneshot: box-carry %i
agi-carry-fetch.timer   88 B  every 60 s: carry each local post, then the hub      
agi-carry-fetch.service 229 B  oneshot: box-carry --fetch
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-project (2420 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
u=$(s agi-post@.service);[ "$u" ]||exit 3;P=$(printf '%s\n' "$u"|sed -n 's/^Environment=PATH=\([^ ]*\).*/\1/p'|tr : '\n'|while read d;do [ -f $d/pi ]&&[ -x $d/pi ]&&echo $d&&break;done);[ "$P" ]||{ g posts.md|sed -n 's/^  - {/{/p'|jq -e --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|select(.harness|test("^pi"))'>/dev/null;[ $? = 4 ]||exit 3;}
mkdir -p $w;rm -f $w/agi-post@*;printf '%s\n' "$u">$o/agi-post@.service;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$P" --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|[.name,if .harness|test("^pi") then "node \($p)/pi --provider \(if (.model|tostring)|test("^grok") then "xai" else "openrouter" end) --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" elif .harness|test("^grok") then "grok-bot --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)","AGI_BOX=\(.box)"]|join(" ")),.boot==true]|@tsv'|while IFS='	' read p h e b;do [ $b = true ]&&ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s %s\n' "$h" "$(git rev-parse --show-toplevel)" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/agi-post@*.service.d/h.conf>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD $r $o $r $o $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s/logs/%s\n' $(git rev-parse --absolute-git-dir) $(git rev-parse --symbolic-full-name $r)>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-gate (397 B)
~~~sh
#!/bin/sh
git grep -ho "^### [^ ]*" $1 -- ":/.agi/nodes/.geometry/engine*.md"|sort|uniq -d|grep -q .&&exit 2
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&[ -s $o/agi-post@.service ]&&ls $o/agi-post@*.service.d/h.conf>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

### sect (214 B)
~~~sh
#!/bin/sh
r=${2:-HEAD};git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~

### matrix (100 B)
~~~
boot	matrix	engine	sect
boot	body	posts	agi-project
post	bin	engine*	sect
post	brief	card-<p>	brief
~~~

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PROPOSED v5 (owner GO 06:1xZ; doc:radically-simple-engine §Q+§R): v4c cut by one rule: ZYGOTE = what runs before any post exists + the map; the rest is EXPANSION read by sect @REV. Only the 4 readers changed (sect, agi-project, agi-gate, agi-post@.service): every .geometry/engine*.md at the REV, ranges end at ^##; the gate refuses a duplicate name (2) and an empty unit (1). R7: + `### matrix` + engine-grow. SPLIT: the unit is in engine-root; a post's loop reads engine.md + engine-[pw]*.md. Scope add: post identity env (parity 42), pane trim (agi-run, pane_max_mb).
<!-- THOUGHT:END -->
