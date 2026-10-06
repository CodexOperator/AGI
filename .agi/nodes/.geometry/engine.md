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
# config:engine — the ZYGOTE: the code that runs before any post exists + the map of 39 pieces (44 `###` in engine*.md; 5 unmapped: boot, boot.service, agi-sync, matrix, seed)
Depth 0 = diagram · 1 = loop + pieces · 2 = one piece: `sect <name>` (any `.geometry/engine*.md`: this node, config:engine-post, config:engine-wrap, config:engine-grow, config:engine-root) · 3 = this file. Pieces are small templates over raw commands; parameters are cells: a row's ONE `engine` object is projected as AGI_<KEY> env. Parity: doc:g716111-stage25-parity.

## diagram — depth 0
~~~
GRAPH = git @trunk .agi/nodes · post opts in by engine.v 4
root ─▶ agi-project @REV ─▶ user · unit · AGI_* cells
unit ─▶ uid · ~/t · brief/meter/turn ─▶ flush ─▶ land
ZYGOTE = this · EXPANSION = engine-post|wrap|grow|root via sect @REV
~~~

## loop — depth 1
~~~
1 BOOT agi-project  2 START PSI+key+tree  3 WORK ~/t
4 TURN signed commit  5 LAND agi-flush → master
~~~

## pieces — depth 1 (bytes on disk; 38 names, fetch timer+service folded)
~~~
agi-post@.service 1801 B  unit: uid, tree, key, pane
agi-run           501 B  pane: .fresh or -c + strace
settings.json      342 B  hooks: brief, meter, turn
cccc.ts           1647 B  pi events -> CC hooks
agi-kid           2037 B  pi-free kid in this unit
agi-infer          1077 B  one OpenAI-compat chat call
agi-brief          938 B  card+seeds+claims STARTUP
brief.py           810 B  parent-edge walk
agi-meter          439 B  rotate_pct out-line
agi-turn           269 B  drop trees; signed commit
agi-link           358 B  node <-> payload_ref
agi-wt             688 B  per-node RAM tree
agi-track           89 B  strace sink, path once
agi-flush          181 B  exit: drop, commit, merge
agi-out           3120 B  out-line keys + ring wrap
gitconfig          198 B  signed commits + signers
sysusers.conf       41 B  post user in group agi
agi.rules          211 B  group agi starts units
project.sh         161 B  body SHOULD
observe.sh         255 B  body IS
tick.sh            254 B  diff; start; commit
agi-project       3395 B  genome: v4 units+cells
agi-frontier       460 B  each goal's falsifier
agi-gate           404 B  refuse a tip that would not regrow
sect               214 B  one piece @REV, any engine*.md
agi-fill          6106 B  captive fill window
agi-captive        576 B  only agi-fill while open
grow-check        1298 B  node vs matrix row+key
grow-gate         7088 B  pre-receive ratchet
ckpt              3444 B  signed hand-offs at one tip
grow-project      1185 B  schemas -> matrix
agi-land          1855 B  root ff-land, one parent up
box               2005 B  signed ref mail, 5x CAS
box-carry         3246 B  root: P refs -> store or hub
agi-signers       1727 B  ONE allowed_signers
agi-carry@.path     149 B  PathChanged refs/box/<P>
agi-carry@.service  287 B  oneshot box-carry %i
agi-carry-fetch.timer   88 B  60s carry local then hub
agi-carry-fetch.service 229 B  oneshot box-carry --fetch
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-project (3395 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;git rev-parse -q --verify "$r^{commit}">/dev/null||exit 4;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
u=$(s agi-post@.service);[ "$u" ]||exit 3;P=$(printf '%s\n' "$u"|sed -n 's/^Environment=PATH=\([^ ]*\).*/\1/p'|tr : '\n'|while read d;do [ -f $d/pi ]&&[ -x $d/pi ]&&echo $d&&break;done);[ "$P" ]||{ g posts.md|sed -n 's/^  - {/{/p'|jq -e --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|select(.harness|test("^pi"))'>/dev/null;[ $? = 4 ]||exit 3;}
mkdir -p $w;rm -f $w/agi-post@*;printf '%s\n' "$u">$o/agi-post@.service;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$P" --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|[.name,if .harness|test("^pi") then "node \($p)/pi --provider \(if (.model|tostring)|test("^grok") then "xai" else "openrouter" end) --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" elif .harness|test("^grok") then "grok-bot --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" elif .harness|test("^raw-shell|^shell$|^bash$") then "bash" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)","AGI_BOX=\(.box)"]|join(" ")),.boot==true]|@tsv'|while IFS='	' read p h e b;do [ $b = true ]&&ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s AGI_POST=%s %s\n' "$h" "$(git rev-parse --show-toplevel)" "$p" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Unit]\nStartLimitIntervalSec=0\n[Service]\nType=oneshot\nWorkingDirectory=%s\nEnvironment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=%s AGI_BOX=%s\nExecStart=sh -c "git cat-file -e %s:.agi/nodes/.geometry/engine.md&&echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/agi-post@*.service.d/h.conf>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD $(git rev-parse --show-toplevel) ${AGI_BOX:-local-town} $r $r $o $r $o $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s/logs/%s\n' $(git rev-parse --absolute-git-dir) $(git rev-parse --symbolic-full-name $r|grep .||echo HEAD)>$o/agi-project.path;ln -sf ../agi-project.path $w
# g5.34.6.2 P1: project agi-carry PathChanged (instant carry; retire sleep-loop SoT)
s agi-carry@.path>$o/agi-carry@.path;s agi-carry@.service>$o/agi-carry@.service
s agi-carry-fetch.timer>$o/agi-carry-fetch.timer;s agi-carry-fetch.service>$o/agi-carry-fetch.service
tw=$1/paths.target.wants;mkdir -p $tw $1/timers.target.wants
ln -sf ../agi-carry-fetch.timer $1/timers.target.wants/agi-carry-fetch.timer
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg b ${AGI_BOX:-local-town} 'select(.box==$b)|.name'|while read p;do [ -n "$p" ]&&ln -sf ../agi-carry@.path $tw/agi-carry@$p.path;done
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
01:5xZ 10-05: merged trunk 00d5983fa (storage_trunk=refs/grid/et-grok-pilot). Map +ckpt (39). Short descriptions restored so whole <=8192. NEVER write refs/grid/local-maxxing from this checkout.
<!-- THOUGHT:END -->
