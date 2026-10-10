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
# config:engine — the ZYGOTE: the code that runs before any post exists + the map of 43 pieces (every `###` block in engine*.md)
Depth 0 = diagram · 1 = pieces · 2 = one piece: `sect <name>` (any `.geometry/engine*.md`: this node, config:engine-post, config:engine-wrap, config:engine-grow, config:engine-root) · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

## diagram — depth 0
~~~
   GRAPH = git @trunk: .agi/nodes, edges = parents: · a post opts in by ONE row cell "engine": {"v": 4, ...}
   root, once ──▶ agi-project (FROM this node @REV) ──▶ BODY: user · unit in agi.slice · env cells
   unit ──▶ own uid · worktree ~/t of MAIN on posts/<p> · pane = fifo i + typescript o (script) · strace
   start|resume|compact ──CC hooks, or pi via cccc.ts──▶ agi-brief: walk(card+seeds+claims) + STARTUP
   prompt ──▶ agi-meter: at the line: card, .fresh, kill ──▶ Restart = a FRESH successor
   turn end ──▶ agi-turn: one signed commit per node tree · ~/t = a read view · mail = a turn
   stop ──▶ agi-flush ──▶ the master lands posts/<p> ──▶ next brief sees it · a write of carry.env re-runs agi-project
   harness: claude --remote-control <p> (hooks native; the owner's app lists it) · pi + cccc.ts · agi-kid
   tick: project(graph) == observe(body)? equal = alive · differ = start its OWN unit + a drift commit
   start: PSI admission; .fresh = a new session, else -c resumes · work: plain paths in ~/t; inbox, budget, records resolve to MAIN · a dropped row is unlinked
   ZYGOTE = this read (map · sect · agi-project · agi-gate) ──sect @REV──▶ EXPANSION: config:engine-post · config:engine-wrap · config:engine-grow · config:engine-root
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service 2251 B  a post = one unit: own uid, tree, key, pane
agi-run           1057 B  pane cmd: .fresh or -c, strace; inbox + box -> i
settings.json      342 B  the ONE hook wiring: brief, meter, turn commit
cccc.ts           1956 B  pi events -> the CC hooks; mail -> a turn
agi-kid           2049 B  a pi-free kid in this unit: own HOME and tree
agi-infer          1077 B  ONE chat call, OpenAI-compatible: stdin -> stdout
agi-brief         1316 B  walk card+seeds+claims; record; STARTUP
brief.py           810 B  the complex walk over parents: edges
agi-meter          574 B  past rotate_pct of the window: out-line
agi-at             899 B  signed CAS commit of ~/t paths to posts/<P>
agi-turn          3122 B  a signed commit per changed node tree
agi-wt            1506 B  a node's tiny RAM tree: pull; drop = turn + purge
agi-track           89 B  strace sink: each path once
agi-flush         1005 B  drop trees, turn, merge trunk
agi-out           3357 B  the out-line: next keys, ring commit, re-wrap, swap
gitconfig          198 B  signed commits against root's allowed_signers
sysusers.conf       41 B  a post = one user in group agi
agi.rules          242 B  a post starts only its OWN unit
project.sh         161 B  what the body SHOULD be
observe.sh         255 B  what the body IS
tick.sh            254 B  diff them; start own unit; commit
agi-project       2560 B  the genome: units + cells for v4 rows
agi-frontier       460 B  each active goal runs its falsifier
agi-gate           542 B  refuse a tip whose body would not regrow
agi-vstore         856 B  root: fetches the pin into a re-hashed RAM store
agi-boot         1797 B  root: gate the pin, start the posts
agi-boot.service  826 B  runs agi-boot after agi-vstore
matrix            100 B  who reads which node via which piece
sect               214 B  ONE piece of any engine*.md node, byte-exact, any REV
agi-fill          5973 B  a node key opens a captive window
agi-captive        576 B  window open: only agi-fill passes
grow-check        1298 B  one node vs its matrix row + key
grow-gate         7098 B  pre-receive: added/changed nodes must pass
ckpt              3444 B  signed hand-offs at one tip; check lists them
grow-project      1185 B  schemas -> the growth matrix
agi-land          1855 B  root: ff-lands a post range one edge up
box               2005 B  mail: one signed ref update per send (5x CAS)
box-carry         3253 B  root: refs/box/P/<Q> -> the recipient's store or hub
agi-signers       1727 B  root: the ONE allowed_signers, every key generation
agi-carry@.path     149 B  PathChanged on refs/box/<P>; first send only
agi-carry@.service  308 B  oneshot: box-carry %i
agi-carry-fetch.timer   88 B  every 60 s: carry each local post, then hub
agi-carry-fetch.service 229 B  oneshot: box-carry --fetch
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-project (2560 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
u=$(s agi-post@.service);[ "$u" ]||exit 3;P=$(printf '%s\n' "$u"|sed -n 's/^Environment=PATH=\([^ ]*\).*/\1/p'|tr : '\n'|while read d;do [ -f $d/pi ]&&[ -x $d/pi ]&&echo $d&&break;done);[ "$P" ]||{ g posts.md|sed -n 's/^  - {/{/p'|jq -e --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|select(.harness|test("^pi"))'>/dev/null;[ $? = 4 ]||exit 3;}
mkdir -p $w;rm -f $w/agi-post@*;printf '%s\n' "$u">$o/agi-post@.service;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$P" --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|select(.name|(type=="string" and test("^[a-z][a-z0-9-]{0,27}\\z")) or (debug(@json "agi-project: skipped post name \(.)")|false))|[.name,if .harness|test("^pi") then "node \($p)/pi --provider openrouter --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)","AGI_BOX=\(.box)"]|join(" ")),.boot==true]|@tsv'|while IFS='	' read p h e b;do [ $b = true ]&&ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s %s\n' "$h" "$PWD" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nEnvironmentFile=/etc/agi/carry.env\nEnvironment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=* GIT_NO_REPLACE_OBJECTS=1 GIT_NO_LAZY_FETCH=1 AGI_VSTORE=/run/agi-v-project.git GIT_DIR=/run/agi-v-project.git\nExecStartPre=/usr/local/libexec/agi-vstore\nExecStart=sh -c "echo $AGI_TRUNK:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s $AGI_TRUNK&&ls %s/agi-post@*.service.d/h.conf>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD $o $o $o>$o/agi-project.service
printf '[Path]\nPathChanged=/etc/agi/carry.env\n'>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-gate (542 B)
~~~sh
#!/bin/sh
[ $(id -u) = 0 ]&&exec runuser -u nobody -- env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0='*' "$0" "$@"
git grep -ho "^### [^ ]*" $1 -- ":/.agi/nodes/.geometry/engine*.md"|sort|uniq -d|grep -q .&&exit 2
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&[ -s $o/agi-post@.service ]&&ls $o/agi-post@*.service.d/h.conf>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;AGI_TRUNK=$1 sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
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
v5 (owner GO 06:1xZ; doc:radically-simple-engine §Q+§R): ZYGOTE = what runs before any post exists + the map; the rest is EXPANSION read by `sect @REV`. .5 (belam R' 08:4xZ): the FENCED bytes <= 8,192 with a margin: 14 map descriptions shortened to <= ~55 B (names and sizes untouched), the loop block folded into the diagram's start/work line.
<!-- THOUGHT:END -->
