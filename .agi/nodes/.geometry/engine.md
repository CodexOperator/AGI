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
# config:engine — ZYGOTE (map + 4 readers). Prose: doc:radically-simple-engine §Q. Parity: doc:g716111-stage25-parity.

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
agi-post@.service 1801 B
agi-run            501 B
settings.json      342 B
cccc.ts           1647 B
agi-kid           2015 B
agi-infer         1077 B
agi-brief          938 B
brief.py           810 B
agi-meter          439 B
agi-turn           269 B
agi-link           358 B
agi-wt             688 B
agi-track           89 B
agi-flush          181 B
agi-out           3120 B
gitconfig          198 B
sysusers.conf       41 B
agi.rules          211 B
project.sh         161 B
observe.sh         255 B
tick.sh            254 B
agi-project       1841 B
agi-frontier       460 B
agi-gate           404 B
sect               214 B
agi-fill          5973 B
agi-captive        576 B
grow-check        1298 B
grow-gate         7088 B
ckpt              3444 B
grow-project      1185 B
agi-land          1855 B
box               2005 B
box-carry         3246 B
agi-signers       1727 B
agi-carry@.path    149 B
agi-carry@.service 287 B
agi-carry-fetch    317 B
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-project (2539 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/multi-user.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};s(){ git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
u=$(s agi-post@.service);[ "$u" ]||exit 3;P=$(printf '%s\n' "$u"|sed -n 's/^Environment=PATH=\([^ ]*\).*/\1/p'|tr : '\n'|while read d;do [ -f $d/pi ]&&[ -x $d/pi ]&&echo $d&&break;done);[ "$P" ]||{ g posts.md|sed -n 's/^  - {/{/p'|jq -e --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|select(.harness|test("^pi"))'>/dev/null;[ $? = 4 ]||exit 3;}
mkdir -p $w;rm -f $w/agi-post@*;printf '%s\n' "$u">$o/agi-post@.service;:>$o/agi-users.conf
g posts.md|sed -n 's/^  - {/{/p'|jq -r --arg p "$P" --arg b ${AGI_BOX:-local-town} 'select(.box==$b and .engine.v==4)|.+.engine|[.name,if .harness|test("^pi") then "node \($p)/pi --provider \(if (.model|tostring)|test("^grok") then "xai" else "openrouter" end) --model \(.model) --thinking \(.effort) --skill skills -e ../bin/cccc.ts" elif .harness|test("^grok") then "grok-bot --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" else "claude --remote-control \(.name) --model \(.model) --effort \(.effort) --permission-mode bypassPermissions" end,([.engine|to_entries[]|"\"AGI_\(.key|ascii_upcase)=\(.value)\""]+["AGI_ROLE=\(.role)","AGI_LADDER_TIER=\(.tier)","AGI_BOX=\(.box)"]|join(" ")),.boot==true]|@tsv'|while IFS='	' read p h e b;do [ $b = true ]&&ln -s ../agi-post@.service $w/agi-post@$p.service;mkdir -p $o/agi-post@$p.service.d;printf '[Service]\nEnvironment="H=%s" O=%s %s\n' "$h" "$(git rev-parse --show-toplevel)" "$e">$o/agi-post@$p.service.d/h.conf;s sysusers.conf|sed s/@/$p/g>>$o/agi-users.conf;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nEnvironment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=* AGI_BOX=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/agi-post@*.service.d/h.conf>/dev/null&&systemctl daemon-reload&&systemd-sysusers %s/agi-users.conf"\n' $PWD ${AGI_BOX:-local-town} $r $o $r $o $o>$o/agi-project.service
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
owner 2026-10-05 via liaison: two zygote reds (9651>8192, map 39>38). Cut = diagram/loop/map descriptions → pointers to doc:radically-simple-engine §Q + doc:g716111-stage25-parity; fold agi-carry-fetch.timer+.service to one map line (both ### headings stay in engine-root). Four reader fences byte-exact. grow-gate map 7088 = live heading.
<!-- THOUGHT:END -->
