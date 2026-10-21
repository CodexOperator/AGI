---
id: doc:season3-explainer-outline
type: doc
mint_id: 44f8d07e0ece4f3eb5095837d29e2a8a
parents:
- goal:g5.4.2
next_edges: []
key: 3dbc163531a12b56
schema: doc@5d9146e2fcfd
title: season3-explainer-outline
tags:
- media
- season3
- explainer
- outline
origin: doc-version
---

# The season 3 explainer: the life of one node edit (outline, M1)

*Stage M1 of goal:g5.4.2. Zero spend. Written from the code at the sha below, checked by `extensions/agi/tests/media_fm1.py` (Fm1, Fm1b). No narration yet (that is M2), no voice, no render.*

sha: 6432bf88d5

## How to read this outline
- **The frame is one edit.** A post wants to change one line of one node. We follow that line from the post's wake-up to the trunk, and every box on the way is a real piece of the engine, shown as a living thing: the **ribosome** (`sect` and the unit's extraction line) reads a script out of the graph and turns it into a tool in `~/bin`; each tool is then a **function block** that takes a little git state in and hands a little git state out.
- **Every claim is a pair.** A `claim:` line says what a step does; the `fn:` line under it names the piece or function that does it, and the `@@excerpt` blocks are the bytes, cut by line number from that sha and checked byte for byte.
- **Live or not.** A step named as live carries a `live: NAME <- CALLER` line (the caller really contains it at the sha). A step the narration must call *not called* carries an `uncalled:` line. Nothing is narrated as running that the code does not run. The council's earlier pre-written chain had false steps and is withdrawn; this one was read from the bytes.
- **The example bytes.** One line of one real node: the `status:` line of `goal:g7.16.1.1.6.2` (a leaf this team closed on 10-14). It is a few bytes; we flip it and watch where those bytes go.
- **Numbers.** No count is typed in this outline's prose; every figure the narration needs comes from a facts slot read at the sha (Fm2 holds for the script).


## C0 · Cold open: a graph that lives in git

sha: 6432bf88d5

claim: The engine is a thoughtgraph kept in git at the trunk: nodes are files, edges are their `parents:`, and a post is a unit that grows the graph one signed commit at a time.

fn: piece:agi-post@.service
fn: piece:agi-project

**Living piece.** The graph as a lit constellation; one star pulses (the example node).

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine.md:L18-L18
~~~~
   GRAPH = git @trunk: .agi/nodes, edges = parents: · a post opts in by ONE row cell "engine": {"v": 4, ...}
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine.md:L23-L23
~~~~
   turn end ──▶ agi-turn: one signed commit per node tree · ~/t = a read view · mail = a turn
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine.md:L24-L24
~~~~
   stop ──▶ agi-flush ──▶ the master lands posts/<p> ──▶ next brief sees it · a write of carry.env re-runs agi-project
~~~~
**Beat.** Open on the owner's own picture: the diagram's three lines. Pull the camera down from the whole graph to one node, then to one line of that node. Promise: by the end, the viewer has followed one line from a post's keyboard to the trunk and can say what every hand-off did.


## C1 · A tiny piece: sect, a few bytes of engine

sha: 6432bf88d5

claim: `sect` prints ONE fenced piece of any engine file at any revision: a read of the graph, cut with sed, and among the smallest working tools in the engine.

fn: piece:sect
live: sect <- piece:agi-brief

**Living piece.** A ribosome sliding along a long strand of engine text until it finds the start codon `### name`, copying until the stop codon, and releasing a short chain: the piece.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77
~~~~
#!/bin/sh
r=${2:-HEAD};git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~~
**Beats.** (1) `git ls-tree` lists the engine files at the revision (`REV` defaults to HEAD). (2) `git cat-file --batch --follow-symlinks` streams them. (3) The sed address `/^###* NAME /,/^###* /` selects from the piece's heading to the next heading; inside it `/^~~~/,/^~~~/` selects the fenced block, and `{//!p}` prints everything in the block except the two fence lines. Walk it with a three-line toy file first, then the real one. Show the dash in `###*` matching both `##` and `###`.


## C2 · The ribosome: the unit turns pieces into tools

sha: 6432bf88d5

claim: Before a post starts, its unit reads the engine files from the trunk and writes each fenced piece as an executable file in a fresh `bin`, then swaps it in whole; the tools a post runs are the graph's text, extracted.

fn: piece:agi-post@.service
live: agi-run <- piece:agi-post@.service

**Living piece.** The same ribosome, now in a row of many: each strand comes out as a tool and hangs on the wall of `~/bin`; the wall is replaced all at once.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L32-L32
~~~~
Environment="AGI_PIECE_GLOB=engine.md engine-[pw]*.md"
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41
~~~~
ExecStartPre=sh -c 'set -f;mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fqd $PWD/t posts/%i;};G="git -c safe.directory=$O -C $O";case $($G rev-parse --symbolic-full-name $AGI_TRUNK 2>/dev/null) in refs/heads/*|refs/remotes/*);;*)echo "[bad-trunk] $AGI_TRUNK is not a branch">&2;exit 255;;esac;[ "$AGI_PIECE_GLOB" ]||{ echo [no-glob]>&2;exit 255;};x(){ echo "[extract-failed] $*">&2;rm -rf bin.new .e;exit 255;};rm -rf bin.new .e;mkdir bin.new||x bin.new;l=$($G ls-tree --name-only $AGI_TRUNK .agi/nodes/.geometry/)||x ls-tree $AGI_TRUNK;for f in $l;do for g in $AGI_PIECE_GLOB;do case $f in */$g)$G show $AGI_TRUNK:$f>.e||x $f;for x in $(grep -o "^### [^ ]*" .e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" .e>bin.new/$x||x $f $x;done;;esac;done;done;rm -f .e;[ -s bin.new/agi-run ]||x agi-run is not in the extracted set;set +f;chmod +x bin.new/*;rm -rf bin.old;mv bin bin.old&&mv bin.new bin||{ [ -d bin ]||mv bin.old bin;x swap;};rm -rf bin.old;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkfifo -m600 %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o'
~~~~
**Beats.** Break the long ExecStartPre line into its verbs, in order: make the dirs; make the worktree `t` on `posts/NAME` if absent; refuse a trunk that is not a branch; list the engine files at the trunk; for each file the glob names, read it and, for every `### name` heading, cut the fenced body with the same sed `sect` uses into `bin.new/name`; insist `agi-run` is in the set; chmod; swap `bin` and `bin.new` (the old one is kept until the move works, restored if it fails); move the `gitconfig` and `settings.json` into place. The glob in the first excerpt is the post's read set. Failure is named, never silent: `[extract-failed]`, `[no-glob]`, `[bad-trunk]`.


## C3 · The graph: a node is a file

sha: 6432bf88d5

claim: A node is a markdown file with front matter; its `parents:` list is the edge set, and an authored THOUGHT region records why this version differs.

fn: def:extensions/agi/bin/frontmatter.py:read_frontmatter
fn: piece:grow.py

**Living piece.** A node as a small organelle with a membrane (front matter) and cytoplasm (body); a thread (`parents:`) runs from it up to its parent.

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L1-L19
~~~~
---
id: goal:g7.16.1.1.6.2
mint_id: 1faf6042fac7494ca79514ffbc6300f4
type: goal
parents:
  - goal:g7.16.1.1.6
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G7.16.1.1.6.2
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 1c2a9f6fa94ef626
season: 2
seeds: []
status: complete
tags:
  - council-loop
~~~~
(excerpt, byte-exact in the script's own excerpt block: 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md, line 54, the line that opens the node's authored thought region. It is not repeated in this node: a node body must not carry that marker at the start of a line, or the thought-block count of the node is wrong.)
**Beats.** Name each front-matter key by what reads it (`id`, `mint_id` forever, `type`, `parents`, `status`). Show `parents:` as an arrow upward to goal:g7.16.1.1.6, the node's place in the tree. Show that the address (`id`) may be renumbered but `mint_id` never changes; the grid history is keyed by it. The example line, `status:`, is the bytes we will carry. The THOUGHT block is the node's delta, rewritten whole.


## C4 · The body: a unit, a tree, a branch

sha: 6432bf88d5

claim: A post is one systemd unit under the memory slice with its own uid, its own worktree `~/t` on its own branch `posts/NAME`, and a pane; the unit restarts a fresh successor if the session ends.

fn: piece:agi-post@.service
fn: piece:agi-project

**Living piece.** A cell with its own membrane: uid and slice are the wall, `~/t` is the nucleus holding a copy of the genome, `posts/NAME` is the strand only this cell may extend.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L33-L33
~~~~
RuntimeDirectory=agi-%i
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L45-L45
~~~~
ExecStart=sh -c 'export AGI_BOX=$(sed -n "s/^AGI_BOX=//p" /etc/agi/carry.env 2>/dev/null);exec 3<>%t/agi-%i/i;exec script -qfaO$HOME/o -c agi-run <&3'
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L49-L52
~~~~
Restart=always
RestartSec=30
Slice=agi.slice
MemoryHigh=4G
~~~~
**Beats.** The unit's name carries the post's name (`%i`). `RuntimeDirectory` is the RAM directory where node trees will live. `Slice=agi.slice` and `MemoryHigh` are the cap the box's memory guard counts against. `Restart=always` with a thirty-second pause is why a rotation is a clean new session, not a repair. `agi-project` is the genome that writes this unit from the rows of `posts.md` at a pinned revision, so a post exists because a row in the graph says so.


## C5 · Waking: the brief

sha: 6432bf88d5

claim: At every session start a hook runs `agi-brief`, which walks the post's card, its seeds and its claims in the graph and prints them, so a fresh session begins knowing what it is doing.

fn: piece:agi-brief
fn: piece:brief.py
fn: piece:settings.json
live: agi-brief <- piece:settings.json
live: agi-meter <- piece:settings.json
live: agi-turn <- piece:settings.json

**Living piece.** The cell's lights come on: a ribosome loads `brief.py`, which reads the card node and prints it as a short ticker tape.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43
~~~~
{"skipDangerousModePermissionPrompt":true,"tui":"default","hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"agi-captive"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn","timeout":180}]}]}}
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54
~~~~
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;p=$AGI_POST;cd ~/t;s=$(jq -r .source);case $AGI_HARNESS in pi*)B=${B:-40000};;esac
sect brief.py|python3 - .agi/nodes doc:card-$p,$AGI_SEEDS$(find $(git rev-parse --git-common-dir)/refs/claims -user $USER -printf ,%f 2>/dev/null) ${K:-20}>~/.brief;cat ~/.brief;cut -d' ' -f4 ~/.brief|xargs tail -n+1|head -c ${B:-0}
w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};x=$(git rev-parse -q --verify refs/heads/posts/${AGI_POST:-$p});for r in $(git for-each-ref --format='%(refname)' refs/archive/${AGI_POST:-$p});do git log --format=%s $r ${x:+--not $x}|grep -q '^[^ ]*: kept '&&echo "[kept] $r: a stop left this tree whole; recover it, then git update-ref -d it";done;ls -d $w/*/ 2>/dev/null|sed 's/^/[tree] /'
[ "$s" = compact ]&&exit;jq -n "{seat:\"$p\",rotation:\"engine-v4\",result:\"success\",source:\"$s\",pid:0,window:\"\",recorded_at:\"$(date -u +%FT%TZ)\"}">$O/.agi/sessions/rotations/$p.$(date -u +%Y%m%dT%H%M%SZ).json
[ "$s" = resume ]||{ echo "## STARTUP OUTPUT";sed -n "/^  $AGI_ROLE:/,/^  [a-z_]*:\$/{/first_turn:/,/after_join:/s/^        - //p}" .agi/nodes/.geometry/rotations.md|jq -r '"\(.label)\t\(.byte_cap//3000)\t\(.cmd)"'|sed "s|{seat}|$p|g;s|{repo}|$O|g;s|{worktree}|$PWD|g;s|{prime_ref}|belam|g"|while IFS='	' read -r l b c;do echo "### $l";timeout 30 sh -c "$c" 2>&1|head -c $b;done|head -c 8000;}
~~~~
**Beats.** `settings.json` wires four hooks: PreToolUse to `agi-captive`, SessionStart to `agi-brief`, UserPromptSubmit to `agi-meter`, Stop to `agi-turn`. `agi-brief` pipes `sect brief.py` into python (the tool is itself extracted by the ribosome), prints the walk, lists any `[kept]` archive and any `[tree]` left in the RAM directory, and on a fresh start prints the startup block from the rotations cell. The card is a node; the brief reads the graph, never a scratch file.


## C6 · Pulling one node into a tiny tree

sha: 6432bf88d5

claim: `agi-wt pull ID` finds the node by `id` or `mint_id`, extracts that node and its payload from the post's own branch into a small directory in RAM, and writes two bookkeeping files: `.p` (the paths) and `.b` (the base commit).

fn: piece:agi-wt
live: agi-wt <- piece:agi-meter

**Living piece.** A forceps lifts one organelle out of the cell into a dish of its own, with a luggage tag (`.p`) and a receipt (`.b`).

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L190
~~~~
cd ~/t;[ "$AGI_POST" ]||{ echo "agi-wt: no AGI_POST">&2;exit 5;};IFS='
';set -f;w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};r=${3:-posts/$AGI_POST};mkdir -p $w
case $1 in new)n=$(basename $2 .md);case $n in ''|[!A-Za-z0-9_-]*|*[!A-Za-z0-9._-]*)echo "agi-wt: new $2: the basename [$n] must match [A-Za-z0-9_-][A-Za-z0-9._-]*">&2;exit 7;;esac;d=$w/$n;mkdir $d||exit 3;printf '%s\n' "$2" ${3:+"$3"}>$d/.p;echo $d;exit;;esac
f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);[ "$f" ]||exit 2;d=$w/$(git show $r:$f|sed -n 's/^mint_id: //p')
case $1 in pull)[ -d $d ]&&{ echo $d;exit;};[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;}
mkdir $d;printf '%s\n' "$f" $(git show $r:$f|sed -n 's/^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$/\1/p')>$d/.p
e=$(git archive -o $d.tar $r $(cat $d/.p) 2>&1&&tar -xC $d -f $d.tar 2>&1)||{ rm -rf $d $d.tar;echo "agi-wt: pull $2 failed: $e">&2;exit 6;};rm $d.tar;git rev-parse $r>$d/.b;echo $d;;
drop)[ -d $d ]||{ echo "agi-wt: no tree $d for $2 (a 'new' tree is dropped by agi-flush)">&2;exit 2;};agi-turn&&{ [ ! -d $d ]||agi-turn chk $d $(cat $d/.b)&&rm -rf $d;};;esac
~~~~
**Beats.** `git grep -lE` over the branch finds the file; the directory is named by the node's `mint_id`; `.p` holds one path per line (the node, and its payload if `payload_ref` names one); `git archive` + `tar` fill the directory from the branch tip, and `git rev-parse` of that tip becomes `.b`. A full RAM disk holds the pull (`hold`). Say aloud what this is NOT: not a checkout of the whole graph, not a branch. **Retired and old paths, named as such:** the earlier node writer `write.py` is the OLD setup's path (the skill `agi-node-write` says so in its first line, quoted below); `agi-link` is gone.
@@excerpt 6432bf88d5:skills/agi-node-write/SKILL.md:L1-L4
~~~~
---
name: agi-node-write
description: >
  OLD SETUP ONLY (a post whose row has engine.v 4 edits node files with plain Write/Edit
~~~~


## C7 · The edit: a few bytes change

sha: 6432bf88d5

claim: The post edits the file in the tiny tree with a plain edit; nothing in the engine writes to the history at that moment. The change is only bytes in a file until the turn ends.

fn: piece:agi-wt

**Living piece.** The dish under the microscope: one letter of the strand is swapped; the membrane does not notice.

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L17-L17
~~~~
status: complete
~~~~
**Beats.** Show the `status:` line of the example node, one line, and the single word that changes when a leaf is closed. Make the point the owner asked for: nothing happened yet. No commit, no ref, no signature. The dish sits in RAM. Then show what the next steps will have to prove: that this directory still matches `.b`, that `.p` names exactly what may be committed, that nothing else sneaked in.


## C8 · The turn ends: the Stop hook

sha: 6432bf88d5

claim: When the model's turn ends, the Stop hook runs `agi-turn`; every pulled tree with a `.p` file becomes at most one commit.

fn: piece:agi-turn
live: agi-turn <- piece:settings.json

**Living piece.** The dish is photographed against the cell wall: a tiny contact print of exactly the files on the luggage tag.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140
~~~~
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;m=$(basename $d);t=$(git rev-parse $b)&&git read-tree $t&&a=$(git --work-tree=$d add -A --pathspec-from-file=$d.p 2>&1)&&n=$(git write-tree)||{ echo "[stage] $m: $(echo "${a:-git failed}"|tr '\n' ' ')">&2;k=1;continue;}
~~~~
**Beats.** The loop walks every directory under the RAM path; a directory without `.p` is not a tree and is skipped. For each: `git read-tree` of the branch tip into a TEMPORARY index (`GIT_INDEX_FILE` is a throwaway), then `git add` with the work tree pointed at the dish and the paths read from `.p` (`--pathspec-from-file`), then `git write-tree`. If the resulting tree equals the tip's tree, the turn changed nothing and the loop continues. The index used is a throwaway: nothing another post staged can ride along (the real index moves only when the read view is re-detached).


## C9 · One signed commit, by compare-and-swap

sha: 6432bf88d5

claim: `agi-turn` makes ONE commit per changed tree with `git commit-tree -S` on top of the tip it read, and moves the branch with `git update-ref NEW OLD`: if the branch moved meanwhile, the update loses and says `[raced]`.

fn: piece:agi-turn

**Living piece.** A tiny stamp with the post's seal presses the contact print onto the strand; the strand's end pointer moves one notch, but only if nobody else moved it.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L144
~~~~
 [ $n = $(git rev-parse $t^{tree}) ]&&continue;grow.py $t>&2||{ k=1;continue;};r=$b;o=$t;q=;[ ! -f $d.b ]||(IFS='
';set -f;git diff --quiet $(cat $d.b) $t -- $(cat $d.p))||{ r=refs/archive/$P/$m;o=$(git rev-parse -q --verify $r||:);q=${o:+-p $o};}
 c=$(echo "$P: $(sed q $d.p)"|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[commit] $m: cannot sign or commit: $c">&2;k=1;continue;}
 git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
~~~~
**Beats.** The commit message is the post's name and the first line of `.p`. The `-S` is a signature by the post's own key (the `gitconfig` piece sets `gpgsign` and the signing key). `update-ref` with the old value is the compare-and-swap: a second writer cannot silently overwrite. The tree is stamped with `.b` = the new commit so the next turn knows its base. This is the moment the bytes become history: the status line is now a signed fact on `posts/NAME`.


## C10 · The growth gate: a NEW node must be legal

sha: 6432bf88d5

claim: Before the commit, `grow.py` checks every NEW node file against the spawn rules (parents must resolve and the shape must be legal); an edit is never gated, and a refusal leaves the tree kept.

fn: piece:grow.py
fn: piece:grow-check
fn: piece:agi-fill
fn: def:extensions/agi/bin/spawn_gate.py:check_spawn
live: grow.py <- piece:agi-turn
live: grow.py <- piece:agi-at

**Living piece.** A gatekeeper cell with a lookup table: a newcomer must show the right parent molecules, or the membrane stays shut. An existing organelle is waved through.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L101-L101
~~~~
 A=[p for p in(q.decode() for q in S.run(["git","diff-index","-z","--cached","--no-renames","--name-only","--diff-filter=A",sys.argv[1],"--",".agi/nodes"],capture_output=True,check=True).stdout.split(b"\0")) if p.endswith(".md")]
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L122-L122
~~~~
   r=g.check_spawn(m.get("type"),q,rules=R,type_index=I,fm=m,node_id=m.get("id") or p,season_parents=m.get("season_parents"),current_season=C)
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/growth.tsv:L32-L32
~~~~
3dbc163531a12b56	doc	-	goal	*
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-grow.md:L155-L155
~~~~
if A[1]=='open':
~~~~
**Beats.** Our example is an EDIT of an existing line, so `grow.py` finds no added node and passes at once; say so, because that is how an edit stays cheap. Then contrast the other path in a sidebar: a NEW node. `diff-index --diff-filter=A` against the tip lists the adds; each is read from the STAGED blob; `check_spawn` judges its type against its parents. A new node is born through `agi-fill`, a captive window whose first line reads a row of `growth.tsv` (here the row for a doc under a goal) and refuses parents the row does not unlock.


## C11 · The tip moved, and the trunk comes in

sha: 6432bf88d5

claim: If the node itself changed on the branch tip since the pull, the commit goes to an archive ref instead and the tree is dropped or kept by name; at the end of every turn `agi-sync` merges the trunk into the branch, or says by name that it cannot.

fn: piece:agi-turn
fn: piece:agi-sync
live: agi-sync <- piece:agi-turn
live: box <- piece:agi-sync
live: agi-notice <- piece:agi-sync

**Living piece.** Two strands approach: if one is a prefix of the other, it just slides; if they only touch at a base, a signed clasp joins them; if they collide, a flag goes up and a messenger runs to the nearest director.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146
~~~~
unset GIT_INDEX_FILE;agi-sync;if agi-turn strand;then git checkout -q --detach $b;else k=1;fi;git status -s|grep -q .&&{ m="[out-of-tree] ~/t has $(git status -s|wc -l) unversioned change(s): edit in a node's tree (agi-wt pull)";echo "$m">&2;agi-notice add "$m";};exit $k
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L214-L215
~~~~
git merge-base --is-ancestor $T $b&&{ rm -f ~/.trunk-boxed;exit 0;}
git merge-base --is-ancestor $b $T&&{ git update-ref $b $T $t||agi-notice add "[trunk-merge-failed] $P: cannot move posts/$P";rm -f ~/.trunk-boxed;exit 0;}
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L216-L216
~~~~
n=$(git merge-tree --write-tree --name-only $b $T 2>/dev/null);r=$?;[ $r = 1 ]||rm -f ~/.trunk-boxed
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L217-L217
~~~~
case $r in 0)c=$(echo "$P: merge $R"|git commit-tree -S -p $t -p $T $n)&&git update-ref $b $c $t||agi-notice add "[trunk-merge-failed] $P: cannot sign or move posts/$P";;
~~~~
**Beats.** The three outcomes of `agi-sync`: the branch already contains the trunk (nothing); the branch is merely behind (the ref moves forward by compare-and-swap, no commit); a clean divergence (`merge-tree --write-tree`, exit 0) becomes one signed merge commit; a conflict (exit 1) changes nothing, writes `[trunk-conflict]` to the post's notice file and mails the nearest harnessed ancestor once per episode, never the Prime. Then `agi-turn` detaches `~/t` onto the branch tip: `~/t` is a READ view.


## C12 · The guards: a post's mistake is refused when it tries to move a peer's ref

sha: 6432bf88d5

claim: Two hooks in `~/bin` (git is told to read hooks there) make the safe path the only path: `reference-transaction` stops one post moving another's refs, and `pre-commit` refuses a plain commit on the detached read view.

fn: piece:reference-transaction
fn: piece:pre-commit
fn: piece:gitconfig
live: hooksPath <- piece:gitconfig

**Living piece.** Turnstiles at the membrane: your own strand opens; a neighbour's strand does not.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L263-L263
~~~~
hooksPath=~/bin
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L153-L154
~~~~
[ . -ef ~/t ]&&! git symbolic-ref -q HEAD>/dev/null&&{ echo "[detached] commit through: agi-at <path>">&2;exit 1;}
[ -x ~/hooks/pre-commit ]&&exec ~/hooks/pre-commit "$@";:
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L169-L176
~~~~
[ "$1" = prepared ]||exit 0
f(){ echo "[ref-guard] fail open: $1">&2;agi-notice add "[ref-guard] fail open: $1 $(date +%Y%m%d)" 2>/dev/null;exit 0;}
u=$(id -un)&&[ "$u" ]||f "no user"
case $u in agi-belam)exit 0;;agi-?*);;*)exit 0;;esac
while read o n r;do [ "$r" ]||f "unparsed input"
 case $r in refs/heads/posts/*)q=${r#refs/heads/posts/};;refs/box/*|refs/held/*)q=${r#refs/*/};;*)continue;;esac
 [ "${q%%/*}" = "${u#agi-}" ]||{ echo "[ref-guard] $u may not move $r (a peer's ref), nothing changed">&2;exit 1;}
done
~~~~
**Beats.** `hooksPath=~/bin` is the line that connects the extracted pieces to git. `reference-transaction` acts only in the `prepared` phase (git honours a non-zero exit only there): a post user may not update `refs/heads/posts/OTHER`, `refs/box/OTHER/*` or `refs/held/OTHER/*`. It fails OPEN with a named notice if it cannot tell who it is, and it does not restrain the Prime's post. `pre-commit` makes `~/t` a read view: a hand commit there would be on no ref and would be stranded by the next detach, so `agi-at` is the one write path.


## C13 · Stop, and the climb to the trunk

sha: 6432bf88d5

claim: At stop, `agi-flush` lands every tree and then purges the directories proven clean; the branch then climbs to the trunk when a master lands it one edge up, signed commit by signed commit.

fn: piece:agi-flush
fn: piece:agi-land
fn: piece:grow-gate
fn: piece:agi-gate
live: agi-flush <- piece:agi-post@.service
uncalled: agi-land

**Living piece.** A gate with a ledger: each signature on the strand is checked against the ring of keys before the strand is allowed to join the trunk's.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L203-L204
~~~~
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};agi-turn||agi-turn||agi-turn||agi-turn;k=$?;for d in $w/*/;do [ -d $d ]&&{ agi-turn purge $d||[ $k != 0 ]||k=1;};done
if agi-turn strand;then git checkout -q --detach $b;else k=1;fi;exit $k
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L228-L229
~~~~
for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
[ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L230-L230
~~~~
echo "$o $n $T"|AGI_ALLOWED=$A AGI_TRUNK=$o AGI_NOT=$o grow-gate||exit 1;agi-gate $n||{ echo "refused: engine would not regrow";exit 1;}
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L231-L231
~~~~
git update-ref $T $n $o
~~~~
@@excerpt 6432bf88d5:skills/agi-master-gate/SKILL.md:L1-L6
~~~~
---
name: agi-master-gate
description: >
  A master's gate for a director's merge-up onto its town trunk: the merge-tree / commit-tree
  landing that never stages a merge, what the range carries (config:posts cells, evidence
  demotions, kid-committed nodes), the suite on tmpfs and how to attribute a
~~~~
**Beats.** `agi-flush` is the unit's ExecStopPost. Then the part the narration must state exactly. `agi-land` is the root tool for the climb: the sender must be the post's parent, every commit in the range must be signed by that sender or a post beneath the landing post, the growth gate and the regrow gate must pass, and the final `update-ref` is a fast-forward by compare-and-swap. **At this sha nothing in a cell or in engine code calls `agi-land`** (the `uncalled:` line is the check); the masters' landing is done by the procedure in the skill `agi-master-gate`, the merge-tree / commit-tree landing, quoted above. Narrate both, in that order, and do not say the engine lands it by itself.


## C14 · Mail is a signed commit too

sha: 6432bf88d5

claim: A post-to-post message is one signed commit on `refs/box/FROM/TO`, sent with a compare-and-swap retry and read by printing the commit's message, so mail travels the same way a node edit does.

fn: piece:box
live: box <- piece:agi-sync

**Living piece.** A signed envelope that is also a tiny strand: the sender's seal on the outside, the words on the inside, a bookmark where the reader stopped.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L329-L329
~~~~
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;b=$(cat);k=0
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L332-L332
~~~~
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L336-L336
~~~~
  [ $1 = n ]&&echo "$f"&&continue;printf '[%s] %s\n' "$f" "$(git log -1 --format=%B $c)";git update-ref $h $c;done;done;;
~~~~
**Beats.** `send` first asks the matrix whether the two posts are adjacent levels; `[off-matrix]` is the refusal. The commit's tree is the empty tree, its body is the message, its signature is the sender's. `read` lists the refs into this post, verifies each new commit's signature, prints the body, and moves a `refs/held/ME/FROM` marker so the mail is read once. **A story inside the story:** the read line prints with `printf '%s'`, not `echo`; in dash `echo` rewrites a backslash sequence, which once cut a mail off at a `\c`. The same family of bug as the boot pin's, caught the same way.


## C15 · The meter: knowing when to hand over

sha: 6432bf88d5

claim: On every prompt a hook runs `agi-meter`; past a set fraction of the context window it tells the post to write its card in a tree, flush, and touch the fresh marker, so a clean successor starts.

fn: piece:agi-meter
live: agi-meter <- piece:settings.json

**Living piece.** A gauge on the cell wall; at the red line the cell lays an egg (the card) and a fresh cell hatches from the same genome.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80
~~~~
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card in its node tree (agi-wt pull), run agi-flush, then: touch ~/.fresh;kill \$PPID";:
~~~~
**Beats.** The meter reads the token count the harness passes in (or the last usage line of the transcript), divides by the window, compares with the rotate percent cell, and prints the instruction. The card is a node, edited in a tree like any other; the successor reads it through the brief. Memory of a post is the graph, not the session.


## C16 · Is the body what the graph says? (tick and drift)

sha: 6432bf88d5

claim: The engine has a piece that compares what the graph projects with what is observed and commits the difference; at this sha it is defined and tested, but no cell or unit calls it.

fn: piece:tick.sh
fn: piece:observe.sh
fn: piece:project.sh
uncalled: tick.sh

**Living piece.** A mirror held up to the cell: the reflection (projection) is compared with the cell (observation); a note is pinned where they differ.

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L281-L282
~~~~
#!/bin/sh
o=$(mktemp -d);sect agi-project|sh -s $o HEAD;sed -n 's/^u agi-\([^ ]*\) .*/user agi-\1\nunit agi-post@\1\nbrief agi-\1/p' $o/agi-users.conf;rm -rf $o
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L287-L289
~~~~
#!/bin/sh
getent passwd|awk -F: '/^agi-/{print "user",$1;system("jq -e .hooks.SessionStart "$6"/.claude/settings.json>/dev/null 2>&1&&echo brief "$1)}'
systemctl list-units --state=active --plain --no-legend 'agi-post@*'|sed 's/\.service .*//;s/^/unit /'
~~~~
@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L294-L296
~~~~
#!/bin/sh
cd ~/t;mkdir -p .agi/drift;sect project.sh|sh|sort>~/.p;sect observe.sh|sh|sort>~/.q;diff ~/.p ~/.q>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|grep -x agi-post@${USER#agi-}|xargs -rn1 systemctl start;agi-at .agi/drift
~~~~
**Beats.** `project.sh` runs `agi-project` at HEAD and prints the users, units and briefs the graph wants; `observe.sh` prints what exists; `tick.sh` diffs them, starts only its OWN unit if it is missing, and commits the drift file with `agi-at`. State plainly that nothing at this sha schedules it (the `uncalled:` line): it is a built tool waiting for its trigger, narrated as such.


## C17 · The whole path again, in one breath

sha: 6432bf88d5

claim: One line, one dish, one stamp, one clasp, one climb.

fn: piece:agi-turn
fn: piece:agi-sync
fn: piece:agi-flush

**Beats.** Replay chapters 5 to 13 as a single unbroken shot with the example line riding along: pull, edit, Stop hook, temporary index, gate (a no-op for an edit), signed compare-and-swap commit, trunk merge, detach, flush, the master's landing. End on the first diagram line from C0, now fully understood. Close with what the viewer can check: every box in the film is a section of a markdown file in the repo, and `sect` will print it.
