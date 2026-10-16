# The season 3 explainer: the life of one node edit (the script, M2)

*Stage M2 of goal:g5.4.2. Zero spend. Per chapter: the claim-to-cite pairs the council reads, the narration the voice will read (every number comes through a slot, none is typed), and the HTML explainer's additions with the byte-exact excerpts. Checked by `extensions/agi/tests/media_fm1.py` (excerpts, functions, callers) and `media_fm2.py` (pairs, bare numbers, slots). No voice yet, no render.*

sha: 6432bf88d5

Tags: every sentence ends with `[Cn.k]` (the pair or pairs of its chapter that prove what it says about the engine) or `[image]` (a picture, greeting or transition that claims nothing about the engine; the council reads these). The voice run strips the tags (`media_fm2.render`).

Reading rules for the narrator: the spoken numbers are filled from the slots at voice time (`media_fm2.render`); letters spelled out stay as written; "dash", "slash" and "dot" are spoken where a path or a flag is named.


## C0 · Cold open: a graph that lives in git

sha: 6432bf88d5

fn: piece:agi-post@.service
fn: piece:agi-project

pair C0.1: The graph is git at the trunk: the nodes are files under the nodes directory and the edges are their parents lists. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L18-L18 ~ .agi/nodes
pair C0.2: The end of a turn runs agi-turn, which writes a signed commit for each node tree. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L23-L23 ~ one signed commit per node tree
pair C0.3: At stop the post runs agi-flush, and the master lands the branch. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L24-L24 ~ agi-flush
pair C0.4: A node is pulled into a tiny tree in memory for the session. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ tiny tree
pair C0.5: The engine's pieces are small templates over raw commands. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L14-L14 ~ Pieces are small templates over raw commands
pair C0.6: The sect tool prints a piece of an engine file with sed. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ sed -n

### narration

Well now, good evening, friends, and welcome. [image] Pull up a chair and make yourself comfortable, for we have a long road ahead of us tonight, and I intend to walk it slowly, the way a gentleman walks a porch at sundown. [image] I am going to show you, step by careful step, how a single change travels through a living machine. [image]

Let me set the scene. [image] There is a repository, and in that repository lives a graph of thoughts. [C0.1] Every thought is a plain text file. [C0.1] The files point at their parents, and those pointers are the edges that make the whole thing a graph. [C0.1] The engine's own map draws it in a single line, and that line is the first piece of bytes we will read together: the graph is git, at the trunk, with the nodes under a directory and the edges written as parents. [C0.1]

Now, a graph that only sits still is a library. [image] This garden grows. [image] It grows because workers sit at their desks and change the files. [image] And here is the thing I want you to hold in your mind for the next hour. [image] However small, the change we follow tonight takes a road you can read in full. [image] It begins as a few bytes edited in a small private tree. [C0.4] At the end of the turn it becomes a signed commit. [C0.2] From there the work climbs until the trunk itself carries it. [C0.3]

So here is our promise to each other. [image] We are going to follow a single line of a single node, a status line, a handful of bytes, from the moment a post picks it up to the moment the trunk holds it. [image] At every stop along the road there is a box, and every box is a real piece of the engine, a few lines of shell or a short script, and we will read each of them aloud and see exactly what it takes in and what it hands back. [C0.5]

I should tell you a last thing before we ride out. [image] The pieces you will see tonight are sometimes called ribosomes and function blocks, and I will lean on that picture, because it is a fair picture. [image] A ribosome reads a strand of instructions and builds a small working tool. [image] The engine does exactly that, and we will watch it do so in the very next chapter, using a tiny tool. [image]

So settle in, friends. [image] We begin with a few bytes, and a tool small enough to hold in your hand. [image]

### html

The graph is git. [C0.1] Nodes are files; edges are the parents listed in each file. [C0.1] A single change, a single road: edit in a private tree, sign at the turn's end, merge the trunk, climb. [C0.2,C0.3,C0.4] Every box in this film is a section of a markdown file in the repository that the sect tool will print for you. [C0.5,C0.6]

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


## C1 · The smallest piece: sect, a few bytes of engine

sha: 6432bf88d5

fn: piece:sect
live: sect <- piece:agi-brief

pair C1.1: The sect tool lists the engine files at a revision with git ls-tree. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ git ls-tree --full-tree --name-only
pair C1.2: It streams them through git cat-file in batch mode. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ git cat-file --batch --follow-symlinks
pair C1.3: The sed address runs from a piece's heading to the next heading. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ /^###* $1 /,/^###* /
pair C1.4: Inside that, a second range keeps only the fenced block, and the empty-pattern test drops the two fence lines. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ {//!p}
pair C1.5: The engine map says each piece is extracted by name and revision with sect. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L52-L52 ~ sect <name> [REV]
pair C1.6: Only files whose names begin with engine and end in the markdown suffix are read. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ grep '/engine[^/]*\.md$'
pair C1.7: With no revision named, sect reads the head. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ r=${2:-HEAD}
pair C1.8: The map lists the sect piece's size. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L41-L41 ~ 214 B

### narration

Our first stop is among the smallest working tools in the engine, and it is called sect. [C1.8] It is only {{bytes:sect}} bytes long. [C1.8] You could write it on the back of a feed-store receipt. [image] And yet a small thing is a fine place to begin. [image]

Here is the job. [image] Some of the engine does not live in a pile of source files the way you might expect. [C1.5] It lives inside markdown nodes, in fenced blocks, each block under a heading with the tool's name. [C1.5,C1.3] A tool called sect reads those nodes and prints just a single block. [C1.1,C1.4] Give it a name, and it hands back that piece, exactly as written, at whatever revision of the repository you like. [C1.5,C1.7]

Let me walk it slowly. [image] The script has just a few lines, and the working line chains a short series of steps. [C1.1] The first step asks git to list the engine files at the revision you named. [C1.1] If you name none, it uses the head of the branch. [C1.7] Only files whose names begin with the word engine and end in the markdown suffix are kept. [C1.6]

The second step feeds those names, each prefixed by the revision, to git's batch reader. [C1.2] That reader follows symbolic links, and it prints the content of every file in turn, each after the other, as a long stream. [C1.2] Think of it as a ribbon unrolling from a spool. [image]

The last step is the interesting part. [image] It is a stream editor with a single instruction, and the instruction is a pair of nested ranges. [C1.3,C1.4] The outer range begins at a line that starts with some hashes, then your piece's name, then a space, and it ends at the next line that starts with hashes. [C1.3] The little star after the second hash is what lets it match both a heading of a pair of hashes and a heading of a trio. [C1.3]

Inside that outer range sits an inner range. [C1.4] It begins at the first line that starts with the fence marker, the little row of tildes, and it ends at the next such line. [C1.4] Then comes a curious bit of notation, a pair of slashes with nothing between them and an exclamation mark. [C1.4] Empty slashes mean, reuse the last pattern that matched. [C1.4] With the exclamation, it says, print every line of the block except the lines that matched, which are both fence lines themselves. [C1.4] So what is left, and printed, is the bare code and nothing else. [C1.4]

That is the whole machine. [image] A reader that finds a start mark, copies until a stop mark, and lets go. [image] If you have ever heard how a ribosome slides along a strand of messenger and builds a protein, you already have the picture. [image] The strand is a long engine file. [image] The start signal is the heading. [image] The stop signal is the next heading. [image] The protein it releases is a tool you can run. [image]

### html

sect: ls-tree lists the engine files at a revision, cat-file streams them, sed cuts from a heading to the next heading and prints only the fenced block. [C1.1,C1.2,C1.3,C1.4] A reader that finds a start mark, copies, and stops. [image]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77
~~~~
#!/bin/sh
r=${2:-HEAD};git ls-tree --full-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s|^|$r:|"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~~


## C2 · The ribosome: the unit turns pieces into tools

sha: 6432bf88d5

fn: piece:agi-post@.service
live: agi-run <- piece:agi-post@.service

pair C2.1: The unit names the files a post reads: the engine map and the post and wrap files. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L32-L32 ~ engine.md engine-[pw]*.md
pair C2.2: It makes the post's worktree on its own branch if the worktree is missing. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ worktree add
pair C2.3: It refuses a trunk that is not a branch. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ [bad-trunk]
pair C2.4: For every heading it cuts the fenced body with the same sed range that sect uses, into a new bin directory. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ bin.new/$x
pair C2.5: It insists the run tool is among the extracted pieces. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ agi-run is not in the extracted set
pair C2.6: It swaps the new directory in whole and keeps the old until the move works. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ mv bin bin.old&&mv bin.new bin
pair C2.7: It reads each engine file from the trunk with git show. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ $G show $AGI_TRUNK:$f
pair C2.8: The extraction is an ExecStartPre of the unit, so it runs before the post starts. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ ExecStartPre=sh -c
pair C2.9: It makes the key, tool, harness and hook directories. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ mkdir -p .ssh bin .claude hooks
pair C2.10: It tells git that any directory is safe. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ safe.directory "*"
pair C2.11: It lists the engine files at the trunk. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ ls-tree --name-only $AGI_TRUNK
pair C2.12: A failed step prints extract-failed and removes its scratch work. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ [extract-failed]
pair C2.13: It makes the extracted pieces executable. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ chmod +x bin.new/*
pair C2.14: It moves the git configuration and the harness settings into place and makes the pane's named pipe. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkfifo

### narration

Now let us watch the ribosome at work on a much larger strand. [image] Before a post can do a lick of work, its unit has to put tools in its hands. [C2.8] And where does it get them? [image] Not from a package, and not from a folder somebody copied over last spring. [C2.7] It gets them from the graph, at the trunk, at the very moment the post starts. [C2.7,C2.8]

It begins by making a few directories in the post's home: a place for keys, a place for tools, a place for the harness settings, a place for hooks. [C2.9] It tells git that any directory is safe to read. [C2.10]

Then it checks whether the post has a worktree. [C2.2] If it does not, it makes a branch for the post, named for the post, off the trunk, and attaches a worktree to it. [C2.2] That worktree is the small tree, the tree named t, where the post will read the graph. [C2.2]

Next, a sanity check that I find mighty comforting. [image] It asks git to name what the trunk is, and it insists that it is a real branch. [C2.3] If the trunk is something else, it prints a bracketed complaint, bad trunk, and it stops. [C2.3] The machine would rather refuse to start than run on the wrong ground. [image]

Now comes the heart of it, and you will recognize it. [image] The line lists the engine files at the trunk. [C2.11] For each file the glob allows, it reads the file and, for every heading, it cuts out the fenced block, with the very same sed range we studied a moment ago, and writes the block into a fresh directory named bin dot new. [C2.4,C2.1] Each block becomes an executable. [C2.4] If any step fails, it prints a bracketed word, extract failed, and removes its scratch work, so a half-built toolbox never sits on the shelf. [C2.12]

The glob matters, so let me say plainly what it is. [image] It names the engine map file and the files whose names begin with a P or a W, which are the post pieces and the wrap pieces. [C2.1] That is a post's read set. [C2.1] The root pieces and the growth pieces are not in that set. [C2.1]

When the cutting is done, the line demands that the run tool be in the new directory, since a post without its run tool is a body without a heartbeat. [C2.5] It makes everything executable, and then comes the swap. [C2.13,C2.6] It moves the old tool directory aside, moves the new directory into its place, and only if that second move works does it throw the old directory away. [C2.6] If it fails, the old directory is put back. [C2.6] A gentleman does not burn the bridge before he is sure of the far bank. [image]

Finally it tucks the git configuration and the harness settings where they belong, makes a named pipe for the pane, and the post is ready to wake. [C2.14]

So there is the whole ribosome, friends: the engine installed from the graph, atomically, every single time. [C2.4,C2.6] Change a piece in the graph, land it on the trunk, and the next time a post starts, its hands are new. [C2.7,C2.8]

### html

The unit's extraction line: make directories, make the worktree, check the trunk is a branch, list the engine files, cut every fenced piece into bin.new with the same sed range as sect, require the run tool, make them executable, swap bin for bin.new keeping the old until the move works. [C2.2,C2.3,C2.4,C2.5,C2.6,C2.9,C2.11,C2.13] A post reads the engine map and the files whose names begin with p or w. [C2.1]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L32-L32
~~~~
Environment="AGI_PIECE_GLOB=engine.md engine-[pw]*.md"
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41
~~~~
ExecStartPre=sh -c 'set -f;mkdir -p .ssh bin .claude hooks;git config --global safe.directory "*";[ -d t ]||{ git -C $O branch posts/%i $AGI_TRUNK;git -C $O worktree add -fqd $PWD/t posts/%i;};G="git -c safe.directory=$O -C $O";case $($G rev-parse --symbolic-full-name $AGI_TRUNK 2>/dev/null) in refs/heads/*|refs/remotes/*);;*)echo "[bad-trunk] $AGI_TRUNK is not a branch">&2;exit 255;;esac;[ "$AGI_PIECE_GLOB" ]||{ echo [no-glob]>&2;exit 255;};x(){ echo "[extract-failed] $*">&2;rm -rf bin.new .e;exit 255;};rm -rf bin.new .e;mkdir bin.new||x bin.new;l=$($G ls-tree --name-only $AGI_TRUNK .agi/nodes/.geometry/)||x ls-tree $AGI_TRUNK;for f in $l;do for g in $AGI_PIECE_GLOB;do case $f in */$g)$G show $AGI_TRUNK:$f>.e||x $f;for x in $(grep -o "^### [^ ]*" .e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" .e>bin.new/$x||x $f $x;done;;esac;done;done;rm -f .e;[ -s bin.new/agi-run ]||x agi-run is not in the extracted set;set +f;chmod +x bin.new/*;rm -rf bin.old;mv bin bin.old&&mv bin.new bin||{ [ -d bin ]||mv bin.old bin;x swap;};rm -rf bin.old;mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkfifo -m600 %t/agi-%i/i;[ -e o ]||install -m600 /dev/null o'
~~~~


## C3 · The graph: a node is a file

sha: 6432bf88d5

fn: def:extensions/agi/bin/frontmatter.py:read_frontmatter
fn: piece:grow.py

pair C3.1: A node's front matter carries its address, its permanent mint id and its type. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L2-L4 ~ mint_id:
pair C3.2: The parents list is the edge from this node up to its parent goal. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L5-L6 ~ goal:g7.16.1.1.6
pair C3.3: The engine's map counts a node's parents as its edges. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L18-L18 ~ edges = parents:
pair C3.4: The next edges field is present in the example node and empty. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L7-L7 ~ next_edges: []
pair C3.5: The status field is a single line of the front matter. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L17-L17 ~ status: complete
pair C3.6: The front matter is read by a function named read_frontmatter. => 6432bf88d5:extensions/agi/bin/frontmatter.py:L55-L55 ~ def read_frontmatter
pair C3.7: The authored region of a node is fenced by THOUGHT markers. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L54-L54 ~ THOUGHT:BEGIN
pair C3.8: A node is a markdown file that opens with a front matter block between dash lines. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L1-L1 ~ ---
pair C3.9: Goal addresses may be renumbered while the mint id is kept. => 6432bf88d5:CLAUDE.md:L109-L109 ~ mint_id
pair C3.10: The mint id never changes, and the grid refs and provenance are keyed by it. => 6432bf88d5:CLAUDE.md:L103-L103 ~ mint id** never changes
pair C3.11: The growth check reads a new node's front matter with the same read_frontmatter function. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L118-L118 ~ f.read_frontmatter

### narration

We have tools now. [image] Let us meet what they work upon, for a tool without a material is just ornament. [image] The material is the node. [image]

A node is nothing grander than a markdown file. [C3.8] It begins with a block of front matter, set off between a pair of lines made of dashes, and below that comes the body, ordinary prose that a person can read. [C3.8] Here, on the screen, is the top of a real node. [image] It is a goal, a closed leaf, and it will be our example for the rest of the night. [C3.1,C3.5]

Look at the first lines. [image] There is an id, which is the node's address, the name other nodes use when they refer to it. [C3.1] Right under it is a mint id, a long string of letters and digits that is handed out once and never changes. [C3.1,C3.10] I want you to remember that difference, because it saves a great deal of confusion. [image] The address may be renumbered, if the family of goals is reorganized. [C3.9] The mint id is permanent. [C3.10] It is the node's birth certificate, and the history of the node is filed under it. [C3.10]

Now the line that matters most for tonight: the parents. [image] A list of addresses, here with just a single entry, the goal above this node. [C3.2] That list is how the engine's map counts the graph's edges. [C3.3] The field called next edges sits just below it, present and empty, and the map's own picture counts the parents as the edges. [C3.4,C3.3] A node says who its parents are, and from all those sayings the graph assembles itself. [C3.3] If you remove a parent from the list, you have cut an edge. [C3.3]

And here is the line we are going to carry on our journey. [image] It is the status line. [image] A few bytes: the word status, a colon, and a single word after it. [C3.5] A leaf that is finished says so here. [C3.5] It is a small thing, a mere handful of characters, and I chose it for that very reason. [image] When you have followed a handful of bytes all the way to the trunk, you have followed anything. [image]

Reading all this is the work of a function called read frontmatter, in a small file of its own. [C3.6] It takes the text of a node and gives back a dictionary, or nothing at all if the text has no readable front matter. [C3.6] We will meet it again when a brand new node tries to join the graph, because the gate that guards the door uses this very reader to check the newcomer's papers. [C3.11]

So that is our material, friends: a file with a name, a birth certificate, a type, a list of parents, a status, and a thought. [C3.1,C3.2,C3.5,C3.7] Hold the status line in your mind. [image] Next we meet the creature that holds it. [image]

### html

A node is a markdown file: front matter (id, mint id that never changes, type, parents, status, tags) and a body, with an authored THOUGHT region that records why this version differs. [C3.8,C3.1,C3.10,C3.7] The map counts the parents lists as the edges. [C3.3] The status line is the few bytes we follow. [image]

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L2-L2
~~~~
id: goal:g7.16.1.1.6.2
~~~~

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L5-L6
~~~~
parents:
  - goal:g7.16.1.1.6
~~~~

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L17-L17
~~~~
status: complete
~~~~

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L54-L54
~~~~
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
~~~~


## C4 · The body: a unit, a tree, a branch

sha: 6432bf88d5

fn: piece:agi-post@.service
fn: piece:agi-project

pair C4.1: The unit's runtime directory is named for the post, and that is where its node trees will live. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L33-L33 ~ agi-%i
pair C4.2: The unit starts the run tool under script so the pane is recorded. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L45-L45 ~ exec script -qfaO$HOME/o -c agi-run
pair C4.3: The unit restarts the post if it ends. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L49-L49 ~ Restart=always
pair C4.4: The unit lives in the memory slice with a cap. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L52-L52 ~ MemoryHigh=4G
pair C4.5: The agi-project piece writes the unit and its users from the rows of the posts file. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L56-L62 ~ posts.md
pair C4.6: The map describes the unit as one unit with its own uid, tree, key and pane. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L33-L33 ~ a post = one unit: own uid, tree, key, pane
pair C4.7: The unit runs in the agi slice. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L51-L51 ~ Slice=agi.slice
pair C4.8: The unit makes the post's worktree t on its own branch posts/NAME. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ worktree add -fqd $PWD/t posts/%i
pair C4.9: The node trees live in a wt directory under the runtime directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L181-L190 ~ RUNTIME_DIRECTORY/wt
pair C4.10: agi-project writes units only for rows of the current engine version. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L56-L62 ~ .engine.v==4
pair C4.11: A dropped row is unlinked. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L27-L27 ~ a dropped row is unlinked

### narration

A creature needs a body, and the body of a post is a systemd unit. [C4.6] I know that is a dry way to put it, so let me dress it up. [image] Think of a single living cell. [image] It has a wall, a nucleus, and a bit of its own cytoplasm. [image] The wall is a Unix user and a memory slice. [C4.6,C4.7] The nucleus is a copy of the genome, the small tree called t. [C4.8] And the part that only this cell may extend is a branch of its own, named for it, called posts slash the post's name. [C4.8]

Let us read the unit's own words. [image] The runtime directory line says agi dash percent i. [C4.1] That percent i is systemd's way of saying, whatever this instance is called. [image] For a post named after, say, a director, the unit is named for the director, and so is its runtime directory. [C4.1] This is a directory in memory, and it is where the post's tiny working trees will live, each of them vanishing when the machine reboots unless it has been committed. [C4.1,C4.9]

Look at the line that starts the work. [image] It exports the box's name, and then it executes the run tool under a recorder called script. [C4.2] The recorder writes the whole pane into a file in the post's home, a typescript, so that a post's session can be looked back on. [C4.2] There is also a named pipe that feeds the pane its input. [C4.2]

Now the lines that make me feel the machine is looking after its own. [image] The unit restarts always, and waits a short while between tries, here {{val:6432bf88d5:.agi/nodes/.geometry/engine-root.md:L50:RestartSec=(\d+)}} seconds. [C4.3] That pause is what lets a rotation be gentle. [C4.3] When a post decides its head is full and ends its session, the unit does not mourn. [image] It starts a fresh successor, who wakes and carries on. [C4.3]

The unit lives in the memory slice that the whole population shares, and it has a soft ceiling: it may use a good deal, but once it passes {{val:6432bf88d5:.agi/nodes/.geometry/engine-root.md:L52:MemoryHigh=(\d+)G}} gigabytes the kernel begins to press on it. [C4.4,C4.7]

And who writes this unit, you may ask? [image] A piece called agi project, which we met on the map, the genome. [C4.5] It reads the rows of a file that lists the posts, a row for each post, with its name, its parent, its harness, its model. [C4.5] For every row that says the post is of the current kind, it writes a user, a unit, and the little configuration the unit needs. [C4.5,C4.10] So a post exists because a row in the graph says it should, and the engine unlinks it when the row is dropped. [C4.5,C4.11] If it ends, the unit starts it again. [C4.3]

That is the body: a wall, a nucleus, a branch of its own, and a promise to restart. [image] In the next chapter we wake it up. [image]

### html

The post's body: a unit named for the post, its runtime directory in memory for node trees, the run tool under script, restart always, the shared memory slice with a soft cap. [C4.1,C4.2,C4.3,C4.4,C4.7] The unit is written by agi-project from the rows of the posts file. [C4.5]

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


## C5 · Waking: the brief

sha: 6432bf88d5

fn: piece:agi-brief
fn: piece:brief.py
fn: piece:settings.json
live: agi-brief <- piece:settings.json
live: agi-meter <- piece:settings.json
live: agi-turn <- piece:settings.json

pair C5.1: The harness settings wire the session start to the brief tool. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "SessionStart":[{"hooks":[{"type":"command","command":"agi-brief"
pair C5.2: They wire each prompt to the meter and the end of a turn to agi-turn. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "Stop":[{"hooks":[{"type":"command","command":"agi-turn"
pair C5.3: The brief pipes the brief script, itself extracted by sect, into python. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ sect brief.py|python3
pair C5.4: The brief names any trees left in the memory directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ [tree]
pair C5.5: It names any archive a stopped session left whole. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ [kept]
pair C5.6: The settings file is itself one of the engine's pieces and holds the hooks. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "hooks"
pair C5.7: It prints any waiting notices first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ ls ~/.notice* >/dev/null 2>&1&&agi-notice
pair C5.8: The walk starts from the post's card, its seeds and its claims. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ doc:card-$p,$AGI_SEEDS
pair C5.9: brief.py spreads weight over the graph in repeated passes. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L59-L73 ~ for _ in range(30)
pair C5.10: The meter's notice tells a post to write its card in a node tree. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ write your card in its node tree
pair C5.11: brief.py prints only the top few nodes. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L59-L73 ~ [:int(k)]
pair C5.12: The brief prints the start of the top files up to a byte limit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ head -c ${B:-0}

### narration

The cell is built. [image] Now we wake it. [image] And I should tell you how a post wakes, because it is nothing like how a man wakes. [image] A man wakes with yesterday still in his head. [image] A post wakes with nothing in its head. [image]

The harness, which is the program that runs the language model, reads a settings file. [C5.1] This file is itself a piece, tiny, extracted by the ribosome like all the rest. [C5.6] It lists hooks, little commands the harness runs at certain moments. [C5.1] Some run before any tool is used, some at the start of a session, some whenever a prompt is submitted, and some when a turn comes to its end. [C5.1,C5.2] We will meet each of them in turn. [image] The hook that matters just now is the session start hook, and it names a tool called agi brief. [C5.1]

What does the brief do? [image] It tells the fresh mind who it is and what it was doing. [C5.3] First, if there are any notices waiting in the post's home, among the engine's channels to a post, it prints them. [C5.7] Then it moves into the post's tree and runs a small python script, which it gets by asking sect for the piece called brief dot py. [C5.3] There is the ribosome again, supplying the very tool that reads the graph. [image]

That script walks the graph. [C5.3] It starts from the post's card, which is a node, and from a list of seed nodes, and from any claims the post holds, which are little marker files saying this is mine. [C5.8] It reads the parents of every node, treats each as an edge in both directions, spreads weight outward from those starting points over repeated passes, and prints the top few nodes, most relevant first, each with its path. [C5.9,C5.11] Then the brief prints the start of the most relevant files themselves, up to a byte limit. [C5.12]

Nothing here is a scratch file. [image] A post's memory, you see, is the graph. [image] When a post knows what it was doing yesterday, it is because its predecessor wrote that down in a node, and the brief found it. [C5.8] That is why the instructions of this household insist that a card be written in a tree like any other node, and never left in the head of a session that is about to end. [C5.10]

The brief does a couple more kind things. [image] It looks through the archive references this post has, and if a previous session ended with a tree it could not prove clean, it says so in a bracketed line, kept, with the name of the reference, so the new session can recover the work. [C5.5] And it lists any trees still sitting in the memory directory, each marked with the word tree, so that a post that simply walked away from a half-finished edit finds its edit waiting. [C5.4]

And so the post is awake, oriented, and holding a map of its own corner of the graph. [image] It has a task. [image] The task is to change a line. [image] And for that, it needs to lift a single node out of the graph and into a dish of its own. [image] That is where we go next. [image]

### html

The harness settings file wires hooks: before a tool, at session start (agi-brief), on each prompt (agi-meter), at the end of a turn (agi-turn). [C5.1,C5.2] The brief tool prints notices, runs brief.py (extracted by sect) to walk the post's card, seeds and claims, then lists any kept archives and any trees left in the memory directory. [C5.3,C5.4,C5.5,C5.8]

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


## C6 · Pulling a node into a tiny tree

sha: 6432bf88d5

fn: piece:agi-wt
live: agi-wt <- piece:agi-meter

pair C6.1: The pull finds the node's file by searching the post's own branch for its id or mint id. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L186-L186 ~ git grep -lE
pair C6.2: The tree directory is named for the node's mint id. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L186-L186 ~ mint_id: 
pair C6.3: The pull refuses when the memory disk is too full. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L187-L187 ~ hold $w
pair C6.4: The dot-p file lists the node's path, and its payload path if it has one, a path to a line. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L188-L188 ~ >$d/.p
pair C6.5: A git archive of the branch tip is untarred into the directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ git archive -o $d.tar
pair C6.6: The tip it came from is written to the dot-b file as the tree's base. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ git rev-parse $r>$d/.b
pair C6.7: The wt tool pulls a node's tiny tree into memory for the session. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ agi-wt pull ID
pair C6.8: The pull refuses without a post name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L183 ~ agi-wt: no AGI_POST
pair C6.9: The trees live in a wt directory under the runtime directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L184 ~ RUNTIME_DIRECTORY/wt
pair C6.10: The default revision is the post's own branch. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L184 ~ r=${3:-posts/$AGI_POST}
pair C6.11: The tag holds one path per line, and agi-turn versions what it names. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ ONE PATH PER LINE in .p
pair C6.12: The turn lane's header says agi-link is gone. => 6432bf88d5:extensions/agi/tests/agi-turn.t.sh:L2-L2 ~ agi-link` is gone
pair C6.13: The older node writer is the old setup's path, and its skill says so in its first lines. => 6432bf88d5:skills/agi-node-write/SKILL.md:L3-L7 ~ OLD SETUP ONLY

### narration

Our post is awake and has a job: change a line of a node. [image] Now, it could go and fetch the whole graph, but that would be like moving the entire library to a desk just to correct a single misspelled word. [image] Instead, it uses a tool called agi wt, and what the tool does is lift a single organelle out of the cell and set it in a dish of its own. [C6.7]

Let us read how. [image] The command is called with the word pull and the node's address. [C6.7] The tool first makes sure it knows who the post is, and it works out where the dishes live: a directory in memory, called wt, which the unit gave the post. [C6.8,C6.9] Then comes the search. [image] It asks git to grep the post's own branch for a file whose id line, or whose mint id line, is exactly the address given, and it takes the first hit. [C6.1] The branch it searches is posts slash the post's own name, unless you ask for another revision. [C6.10] That is worth stating plainly. [image] A post pulls from its own branch, not from the trunk. [C6.10] Later we will watch how the trunk's news reaches the branch. [image]

Having found the file, the tool reads its mint id, and it names the dish after it. [C6.2] That is the permanent birth certificate again, doing honest work. [image] So the dish for our example node is named by a long string of letters and digits, and it will be the same string every time, however the node's address may be rearranged. [C6.2]

Now it makes the directory, and it writes a small file, named dot p, which is a luggage tag. [C6.4] On the tag, a path to a line, goes the node's own path, and, if the node has a payload file, which is a file the node stands for, that path as well. [C6.4] This tag is important. [image] Remember it, because it is the list of the only things this dish is allowed to carry back. [C6.4,C6.11]

Next, a git archive of those paths at the branch tip is unpacked into the directory. [C6.5] Not a checkout, mind you, and not a branch: an archive, a plain snapshot of just those few files. [C6.5] And finally the tool writes the tip's commit id into a second small file, dot b, which is a receipt. [C6.6] It says, this dish was lifted from that commit. [C6.6]

I should be careful here to speak plainly about what is old and what is new. [image] There was an earlier way to change nodes, a tool called write dot py, with verbs for setting a key or appending a note. [C6.13] It is still in the repository, and its skill says in its first lines that it is for the old setup only, the posts that edit node files with plain tools and commit through the older routine. [C6.13] And there was a little tool called agi link, which is gone altogether. [C6.12] Neither is part of the road we walk tonight. [image]

So here we are. [image] The dish holds a single node, a luggage tag and a receipt, in memory. [C6.4,C6.6] The post may now edit. [image]

### html

agi-wt pull: grep the post's own branch for the node, name the tree by mint id, refuse if the memory disk is too full, write the .p path list, git archive the tip into the tree, write the base commit to .b. [C6.1,C6.2,C6.3,C6.4,C6.5,C6.6] The older write.py verbs are the old setup's path; agi-link is gone. [C6.13,C6.12]

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


## C7 · The edit: a few bytes change

sha: 6432bf88d5

fn: piece:agi-wt
fn: piece:agi-turn

pair C7.1: The status line of the example node is a single short line of the file. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L17-L17 ~ status: complete
pair C7.2: A directory under the memory path with no dot-p file is not a tree, and the turn skips it. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ [ -f $d.p ]||continue
pair C7.3: A dish with a file outside its tag is kept, not committed, and named as kept. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L134-L134 ~ kept, not in the commit
pair C7.4: The drop checks the dish against its commit before it removes it. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L190-L190 ~ agi-turn chk $d
pair C7.5: The tree is dropped only after a proven turn: the drop runs agi-turn first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L190-L190 ~ agi-turn&&
pair C7.6: The node's path from the tag is untarred under a directory named for the mint id. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L186-L186 ~ d=$w/$(git show $r:$f
pair C7.7: The extracted files are unpacked into that directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ tar -xC $d
pair C7.8: A commit is made by agi-turn, with commit-tree. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L143 ~ git commit-tree -S
pair C7.9: A reference is moved by agi-turn's update-ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L144-L144 ~ git update-ref $r $c
pair C7.10: The turn adds exactly the paths on the tag. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ --pathspec-from-file=$d.p
pair C7.11: The base commit is written to the dot-b receipt at the pull. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ git rev-parse $r>$d/.b
pair C7.12: The turn compares the tag's paths between the receipt and the tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L142 ~ git diff --quiet $(cat $d.b) $t
pair C7.13: The dish is made under the runtime directory's wt directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L184 ~ RUNTIME_DIRECTORY/wt

### narration

Now the edit itself. [image] I want to be careful, because this is the moment where it would be easy to imagine a great deal going on, and in truth, nothing is committed at all. [C7.8]

The post has a tool for changing files, which is an ordinary text editing tool of the harness. [image] It points that tool at the file in the dish, the node's path under the directory named for the mint id, and it replaces a few characters. [C7.6,C7.7] The line we chose is the status line. [C7.1] A closed leaf says complete. [C7.1] In our telling, the line said something else before the leaf was closed, and the post changes that word. [image] That is all. [image] A word of a few letters, swapped for another. [image]

And here is what I would have you notice. [image] No commit is made. [C7.8] No signature is written. [C7.8] No reference moves. [C7.9] The engine does not know, yet, that the file changed. [C7.8,C7.9] The dish sits in memory, under the runtime directory's wt directory, and a few bytes in it differ from the receipt. [C7.6,C7.13] If the machine were to lose power this instant, the edit would vanish, and the history would show that nothing had ever happened. [C7.6,C7.13]

But the engine keeps a pair of small notes about the dish. [C7.10,C7.11] Remember the luggage tag. [image] It is the list of exactly which files may travel. [C7.10] And remember the receipt, which says which commit this dish was lifted from. [C7.11] When the turn ends, the engine will use the tag to decide what to take, and the receipt to decide whether the world moved in the meantime. [C7.10,C7.12]

There is a second guard, and it is rather elegant. [image] A directory in the working area is only treated as a tree if it has a tag in it. [C7.2] If a post makes some other folder there, for scratch, the turn walks right past it. [C7.2] And when a post is finished with a tree and asks to drop it, the drop does not simply delete. [C7.5] It runs the turn routine first, to be sure everything is committed, and only if that succeeds does it check once more that the dish is clean against its commit, and then remove it. [C7.4,C7.5] A tree is purged only once its work is proven safe. [C7.4,C7.5] Otherwise the dish stays in place, and the post is told by name that it was kept. [C7.3]

So the stage is set. [image] A word has changed. [image] The dish is dirty and the history is clean. [image] And in a moment, the turn will end. [image]

### html

The edit is plain bytes in a file in memory: the status word changes. [C7.6,C7.1] No commit, signature or reference moves yet. [C7.8,C7.9] A directory without a .p tag is not a tree; a drop runs agi-turn first and purges only a proven-clean tree. [C7.2,C7.5,C7.4]

@@excerpt 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L17-L17
~~~~
status: complete
~~~~


## C8 · The turn ends: the Stop hook

sha: 6432bf88d5

fn: piece:agi-turn
live: agi-turn <- piece:settings.json

pair C8.1: The harness settings run agi-turn when a turn ends. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "Stop":[{"hooks":[{"type":"command","command":"agi-turn"
pair C8.2: The turn stages and commits in a throwaway index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ GIT_INDEX_FILE=$x
pair C8.3: The real index moves only when the read view is re-detached onto the branch tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146 ~ git checkout -q --detach $b
pair C8.4: The turn sets up with the branch name and a temporary index file name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ x=$(mktemp -u)
pair C8.5: The temporary file is removed when the tool exits. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ rm -f $x $x.l
pair C8.6: For every tree it reads the branch tip into that throwaway index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ git read-tree $t
pair C8.7: It adds exactly the paths on the tag, with the work tree pointed at the dish. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ --pathspec-from-file=$d.p
pair C8.8: It writes the tree object from that index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ git write-tree
pair C8.9: If the new tree equals the tip's tree, nothing changed and the loop moves on. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ &&continue;grow.py

### narration

The model finishes its answer. [image] The turn ends. [image] And the harness, which has been told what to do at such a moment, runs a command. [C8.1] The settings file we read earlier has a line for it: when a turn stops, run a tool called agi turn. [C8.1] This is the hinge of the whole story, so I will go slowly. [image]

First, the tool sets itself up. [image] It moves into the post's tree, works out the name of the branch, and makes up the name of a temporary file. [C8.4] Then it exports a variable that tells git, use this file as your index. [C8.2] That line matters, and I want you to see why. [image] The index is the place where git stages what is about to be committed. [image] If a pair of things shared the real index, either could stage something and the other could commit it by accident. [image] By pointing git at a throwaway index for the duration of this run, the tool guarantees that nothing another process has staged can ride along. [C8.2] When the tool finishes, the temporary file is deleted. [C8.5] The real index moves only later, when the read view is set again at the branch tip, detached. [C8.3]

Then the loop. [image] The tool looks at every directory in the memory working area. [C8.6] Any directory without a luggage tag is skipped. [C8.6] For each dish that has a tag, it does a few things in a row. [image]

First, it reads the branch tip into the temporary index. [C8.6] That fills the index with the whole tree of the post's branch, exactly as it stands, ready to be modified. [C8.6]

Second, it asks git to add, but with a twist. [image] The work tree, for this command, is the dish, not the repository. [C8.7] And the paths to add are read from the luggage tag. [C8.7] So git looks at the files named on the tag, in the dish, and stages them into the temporary index over the top of the branch's old copies. [C8.7] Only those. [image] Nothing else in the dish could be staged, and nothing outside the dish, because git was told that the dish is the work tree. [C8.7]

Third, it writes the tree object from the index. [C8.8] This is a content address: a name derived from the bytes of every file in the new state of the branch. [image] If our edit changed a single word in a single node, this name differs from the tip's tree name. [C8.9] If nothing changed, it is the same. [C8.9]

And that is the test that follows. [image] If the new tree name equals the tip's tree name, the post made no change that counts, and the loop simply goes on to the next dish. [C8.9] No commit, no noise. [image] A turn in which a post only read things makes no commit for that dish. [C8.9]

Our post did change a word. [image] So the names differ, and the tool proceeds. [C8.9] What it does next, the gate and the stamp, are the next chapters. [image] For now, take a breath, friends, and notice how little it took to get here: a throwaway index, a pathspec from a tag, and a content address. [image] Honest tools from git, arranged in a row. [image]

### html

The Stop hook runs agi-turn. [C8.1] It exports a throwaway GIT_INDEX_FILE, then for each tree with a .p tag: read the branch tip into the index, add exactly the tagged paths with the work tree pointed at the dish, write the tree object; an unchanged tree name means no commit for that dish. [C8.2,C8.6,C8.7,C8.8,C8.9]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43
~~~~
{"skipDangerousModePermissionPrompt":true,"tui":"default","hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"agi-captive"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief","timeout":180}]}],"UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"}]}],"Stop":[{"hooks":[{"type":"command","command":"agi-turn","timeout":180}]}]}}
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140
~~~~
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;m=$(basename $d);t=$(git rev-parse $b)&&git read-tree $t&&a=$(git --work-tree=$d add -A --pathspec-from-file=$d.p 2>&1)&&n=$(git write-tree)||{ echo "[stage] $m: $(echo "${a:-git failed}"|tr '\n' ' ')">&2;k=1;continue;}
~~~~


## C9 · One signed commit, by compare-and-swap

sha: 6432bf88d5

fn: piece:agi-turn
fn: piece:gitconfig

pair C9.1: The commit is made with commit-tree and the signing flag, on top of the tip it read. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L143 ~ git commit-tree -S -p $t
pair C9.2: The commit message is the post's name and the first line of the tag. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L143 ~ $(sed q $d.p)
pair C9.3: The branch is moved by update-ref with the old value, so a lost race fails. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L144-L144 ~ git update-ref $r $c
pair C9.4: A lost race is named raced and the turn goes on. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L144-L144 ~ [raced]
pair C9.5: On success the new commit becomes the tree's base in the dot-b file. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145 ~ echo $c>$d.b
pair C9.6: The git configuration of every post turns signing on. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L258-L258 ~ gpgsign=true
pair C9.7: The ssh signing format is set. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L254-L254 ~ format=ssh
pair C9.8: The post's key is made by the unit's start-up if it is missing. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L39-L39 ~ ssh-keygen -qN
pair C9.9: A piece keeps the one allowed signers file for every key generation. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L158-L167 ~ allowed_signers
pair C9.10: Between the tree and the commit the turn calls the growth check. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ grow.py $t
pair C9.11: It also sets the file of allowed signers and the hooks path. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L256-L263 ~ hooksPath=~/bin

### narration

We have a new tree, a content address that says what the post's branch ought to look like with the edit in it. [image] Now we turn it into history. [image]

The tool builds a commit with the lowest-level command git offers for the purpose, commit tree. [C9.1] That command does nothing clever. [image] It takes a tree, a parent, and a message, and it writes a commit object. [C9.1] The parent is the branch tip the tool read at the start. [C9.1] The message is the post's name, a colon, and the first line of the luggage tag, which is the node's path. [C9.2] So the history will say, in plain words, who changed which file. [C9.2]

And there is a flag on that command, a capital S, which means sign it. [C9.1] How does the tool know how to sign? [image] The post's git configuration says so. [C9.6] I have it on the screen. [image] In that small file, signing is switched on for every commit. [C9.6] The signing format is ssh, which means the post's own key, the key made for it when its unit first started. [C9.7,C9.8] There is a file of allowed signers, a ledger, in which every post's public key is listed, so that anyone can check a signature. [C9.11,C9.9] And there is the line that points git's hooks at the post's tool directory, which we will meet when we get to the guards. [C9.11]

Now the delicate part. [image] The tool has a new commit. [image] It must make the branch point at it. [image] But somebody else, a different process, might have moved the branch in the meantime. [C9.3] How does the tool avoid trampling them? [image] It uses git's update ref with these arguments: the reference, the new commit, and the old value it expects to find. [C9.3] That third argument is the compare and swap. [C9.3] Git will move the reference to the new commit only if the reference still holds exactly the old value. [C9.3] If another writer got there first, git refuses, and the tool prints a bracketed word, raced, with the tree's name, and goes on without losing its place. [C9.4] The edit stays in the dish. [C9.4] Nothing is destroyed. [image] On the next turn, the post can try again. [image]

When the swap succeeds, there is a little bookkeeping step. [image] The tool writes the new commit's name into the receipt file, so that the dish's base is now the commit just made. [C9.5] That matters for the next turn: if the post edits the same dish again, the receipt will say what the dish was last lifted from or last committed as. [C9.5]

But hold on. [image] We skipped something, did we not? [image] Between the content address and the commit there was a call to a checker. [C9.10] A gate. [C9.10] Let us go and meet the gatekeeper. [image]

### html

git commit-tree -S makes the commit on top of the tip read; update-ref with the old value is the compare-and-swap, a lost race prints [raced] and the edit stays; the receipt .b takes the new commit. [C9.1,C9.3,C9.4,C9.5] The post's git configuration turns signing on, names the ledger of allowed signers and points hooks at the post's tool directory. [C9.6,C9.11]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L144
~~~~
 c=$(echo "$P: $(sed q $d.p)"|git commit-tree -S -p $t $q $n 2>&1)||{ echo "[commit] $m: cannot sign or commit: $c">&2;k=1;continue;}
 git update-ref $r $c "$o"||{ echo "[raced] $m">&2;k=4;continue;}
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145
~~~~
 [ $r = $b ]&&{ echo $c>$d.b;continue;};agi-turn chk $d $c&&{ echo "[moved] $m: changed on the tip since pull; your version is $r, the tree is dropped">&2;rm -rf $d;continue;};echo "[moved] $m: your version is $r, the tree is KEPT">&2;k=1;done
~~~~


## C10 · The growth gate: a NEW node must be legal

sha: 6432bf88d5

fn: piece:grow.py
fn: piece:grow-check
fn: piece:agi-fill
fn: def:extensions/agi/bin/spawn_gate.py:check_spawn
live: grow.py <- piece:agi-turn
live: grow.py <- piece:agi-at

pair C10.1: Before the commit, the turn calls the growth check on the temporary index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ grow.py $t
pair C10.2: The check looks only at nodes the index ADDS against the tip: an edit is never gated. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L96-L96 ~ an edit is never gated
pair C10.3: The adds are listed by diff-index with the add filter. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L101-L101 ~ --diff-filter=A
pair C10.4: A move counts as an add at the new path, because the list is read without rename detection. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L101-L101 ~ --no-renames
pair C10.5: Each new node is read from its staged blob and its front matter parsed. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L118-L118 ~ read_frontmatter
pair C10.6: A node with no readable front matter is refused as a growth-order failure. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L119-L119 ~ no readable front matter
pair C10.7: A node whose parents do not resolve in the staged tree is refused. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L121-L121 ~ resolve nowhere in the staged tree
pair C10.8: A document needs a goal as its single parent. => 6432bf88d5:.agi/context/schemas/[doc].md:L25-L27 ~ max_parents: 1
pair C10.9: A new node under the deprecated directory is not gated. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L102-L102 ~ .agi/nodes/deprecated/
pair C10.10: Each new node is judged by the spawn gate's check_spawn. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L122-L122 ~ g.check_spawn
pair C10.11: The spawn gate function is named check_spawn. => 6432bf88d5:extensions/agi/bin/spawn_gate.py:L966-L966 ~ def check_spawn
pair C10.12: A growth table names, for each type and parent shape, a key. => 6432bf88d5:.agi/nodes/.geometry/growth.tsv:L32-L32 ~ 3dbc163531a12b56
pair C10.13: A new node is written through the fill tool, which opens a window for a key. => 6432bf88d5:.agi/nodes/.geometry/engine-grow.md:L160-L161 ~ FILL WINDOW OPEN
pair C10.14: The fill tool refuses parents the key does not unlock. => 6432bf88d5:.agi/nodes/.geometry/engine-grow.md:L159-L159 ~ unlocks

### narration

Here is the gatekeeper. [image] Before the commit is made, the turn calls a small python script named grow dot py, and it hands it the tip, so that the script can compare. [C10.1] The script's whole business is to ask a single question: has this turn added any brand new nodes to the graph? [C10.2,C10.3] And if it has, are they legal? [C10.10]

I want you to see how modest the question is. [image] The script lists what the temporary index adds, against the tip, with the filter that means added and nothing else. [C10.3] A changed file does not count. [C10.3] A moved node is checked at its new place, unless it moved into the deprecated directory, where retired nodes rest. [C10.4,C10.9] And the comment at the top of the script says the thing outright: an edit is never gated. [C10.2]

That is the answer for our example. [image] We changed the word in a status line of a node that already exists. [image] So the list of additions is empty, the script finds nothing to check, and it exits with success at once. [C10.2,C10.3] The gate swings open without a word. [image] It was important to say so, because otherwise you might think every small edit has to pass through a long inquisition. [image] It does not. [image] Editing is cheap. [C10.2] Growing is what is guarded. [C10.10]

But since we are standing at the gate, let me tell you what it does for a newcomer, for that is a thing worth seeing. [image] A new node is read from its staged copy, byte for byte, and its front matter is parsed with that function we met earlier. [C10.5] If the front matter cannot be read, the node is refused with a bracketed word, growth order, and the reason. [C10.6] The node's parents are looked up: each must resolve to some node in the staged tree, or the newcomer is turned away. [C10.7] Then comes a call to a function in the spawn gate, called check spawn, which takes the node's type and its parents and the rules, and says approved or not. [C10.10,C10.11] A document, for example, must have a goal as its parent, and only a single parent. [C10.8]

Behind that stands a table, kept in the graph, that lists for every type and every shape of parents a key, a long hexadecimal name. [C10.12] Here is the line for a document under a goal. [C10.12] The key is the name of a door. [image] When a new node is made through the proper tool, which is called fill, the tool opens a window for that key and checks the parents offered against the row. [C10.13,C10.14] If the row unlocks a goal and you offer a hypothesis, it says refused, parents wrong, and tells you which shape the row unlocks. [C10.14]

So: a gate that waves edits through and weighs only newcomers. [image] That is a sensible gate, to my mind. [image] It protects the shape of the garden without making a man ask permission to prune a branch. [image]

### html

grow.py runs on the temporary index before the commit; it lists only ADDED nodes (diff-filter A), parses their staged front matter, requires every parent to resolve, and asks spawn_gate.check_spawn. [C10.1,C10.3,C10.5,C10.7,C10.10] An edit is never gated. [C10.2] A growth table keys each type and parent shape; the fill tool opens a window for a key and refuses parents it does not unlock. [C10.12,C10.13,C10.14]

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


## C11 · The tip moved, and the trunk comes in

sha: 6432bf88d5

fn: piece:agi-turn
fn: piece:agi-sync
live: agi-sync <- piece:agi-turn
live: box <- piece:agi-sync
live: agi-notice <- piece:agi-sync

pair C11.1: A tree whose node changed on the tip since the pull is committed to an archive reference instead. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L142 ~ r=refs/archive/$P/$m
pair C11.2: The turn runs agi-sync at its end, before it detaches the read view. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146 ~ agi-sync;if agi-turn strand
pair C11.3: If the trunk is already inside the branch, agi-sync does nothing. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L214-L214 ~ is-ancestor $T $b
pair C11.4: If the branch is merely behind, the reference moves to the trunk tip by compare-and-swap. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L214-L215 ~ git update-ref $b $T $t
pair C11.5: Otherwise git merge-tree writes the merge in memory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L216-L216 ~ git merge-tree --write-tree
pair C11.6: A clean merge becomes a signed merge commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L217-L217 ~ git commit-tree -S -p $t -p $T
pair C11.7: A conflict is named in the post's notice file. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L218 ~ [trunk-conflict]
pair C11.8: A moved dish is named moved, with the archive reference that holds the commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145 ~ [moved]
pair C11.9: The mail walk stops below the Prime's row. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L219 ~ prime_director
pair C11.10: It is mailed to the nearest harnessed ancestor, once per episode of conflict. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L219 ~ box send $u

### narration

The commit is made. [image] The edit is safe in the post's branch. [image] But the branch is not alone in the world. [image] While our post was thinking, the trunk, which is the shared line of history that everyone's work eventually joins, may have moved on. [image] Other posts, other directors, may have landed work. [image] So at the end of every turn, a tool called agi sync runs, and its job is to bring the trunk's news into our post's branch, and to say so loudly if it cannot. [C11.2,C11.7]

First, a footnote about the tree that moved. [image] If the node itself had changed on the branch tip since the dish was lifted, then committing on top of the new tip would silently overwrite whatever changed. [C11.1] The tool does not do that. [image] It sends that commit to an archive reference instead, under the post's name and the dish's name, and it tells the post, in a bracketed line, moved, that the dish's version lives on the archive and that the dish was dropped or kept. [C11.1,C11.8] Nothing is lost. [C11.8] The post can recover and merge by hand. [image] That is the safe answer to a race it cannot decide. [image]

Now to agi sync proper. [image] It asks questions, in order, with git. [image]

The first question: is the trunk already part of my branch? [image] It uses merge base with the flag that tests for an ancestor. [C11.3] If the trunk is an ancestor of the branch, there is nothing to do, and the tool also erases a little marker file. [C11.3] It exits. [image]

The second question: am I merely behind? [image] If the branch is an ancestor of the trunk, then the trunk contains everything the branch has, and more. [C11.4] In that case, the tool does not make a merge commit at all. [C11.4] It moves the branch reference forward to the trunk tip, again by compare and swap, and exits. [C11.4] A plain slide forward, tidy as a man smoothing a tablecloth. [image]

The last question is the hard question: have we diverged? [image] Then the tool asks git to write the merge, but in memory, with merge tree and the write tree option. [C11.5] Git builds the merged tree and tells the tool its exit status. [C11.5] If the status is clean, the tool makes a signed merge commit, with a pair of parents, the old branch and the trunk, and the same compare and swap moves the branch. [C11.6]

And if the status says conflict, the tool changes nothing. [C11.7] It does not leave the branch in a half-merged state. [C11.7] It writes a bracketed line, trunk conflict, with the number of paths and the first few names, to the post's notice file, so that the next turn the post sees it. [C11.7] And it mails the nearest ancestor that actually has a harness, skipping the groups that are only labels, and stopping short of the Prime. [C11.10,C11.9] It mails once per episode of conflict, not once per turn, by remembering a hash of the set of conflicting paths. [C11.10]

So our status word now lies in a signed commit, on a branch that has absorbed the trunk, with no conflicts. [C11.2,C11.6] Remarkable how much care sits behind a word of a few letters. [image] But the care is the point, and now we turn to the guards that keep the safe road the easy road, and make a wrong turn loud. [image]

### html

If the node changed on the tip since the pull, the commit goes to refs/archive/<post>/<tree> and the post is told by name. [C11.1] At the end of every turn agi-sync: trunk already inside the branch, nothing; branch merely behind, the reference slides forward by compare-and-swap; diverged, git merge-tree writes the merge in memory and a clean merge becomes a signed merge commit, a conflict changes nothing, is named in the notice file and boxed once per episode to the nearest harnessed ancestor (never the Prime). [C11.2,C11.3,C11.4,C11.5,C11.6,C11.7,C11.10]

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


## C12 · The guards: a mistake cannot move a peer's ref

sha: 6432bf88d5

fn: piece:reference-transaction
fn: piece:pre-commit
fn: piece:gitconfig
fn: piece:agi-at
live: hooksPath <- piece:gitconfig

pair C12.1: The git configuration points git's hooks at the post's tool directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L263-L263 ~ hooksPath=~/bin
pair C12.2: The reference-transaction hook acts only in the prepared phase. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ [ "$1" = prepared ]||exit 0
pair C12.3: It refuses an update to another post's branch, box or held reference, and says so in one line. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ may not move $r (a peer's ref), nothing changed
pair C12.4: If it cannot tell who is asking, it fails open and leaves a notice. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ [ref-guard] fail open
pair C12.5: The pre-commit hook refuses a plain commit on the detached read view and names agi-at. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L151-L154 ~ [detached] commit through: agi-at <path>
pair C12.6: The hook is called for prepared, committed and aborted, and git honours a refusal only in prepared. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ honours a non-zero exit ONLY in prepared
pair C12.7: The Prime's post may move any reference. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ agi-belam)exit 0
pair C12.8: The hook exists so that a post's mistake cannot move a peer's ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ a post's MISTAKE cannot move a peer's ref
pair C12.9: The read view is a read view, and a commit made there is on no ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L151-L154 ~ ~/t is a read view
pair C12.10: agi-at checks new nodes with the growth check before it commits. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L85-L90 ~ grow.py $t>&2||exit 6
pair C12.11: agi-at says raced and keeps the edit when the swap loses. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L85-L90 ~ [raced]
pair C12.12: The agi-at tool makes a signed commit by compare-and-swap, the one hand write path. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L85-L90 ~ git commit-tree -S -p $t $n)&&git update-ref $b $c $t

### narration

The first fence is called reference transaction. [C12.2] Git calls it whenever any reference is about to change, and it calls it more than once, at the stage of preparing, then again at the stage of committed or aborted. [C12.6] Git only listens to a refusal at the first stage, and so the hook acts only there. [C12.6] The first line of the script says exactly that. [C12.2]

What does it forbid? [image] Let me say it the way a neighbor would. [image] A post may not reach over the fence and move a neighbor's branch, nor drop a letter in a neighbor's mailbox, nor mark a neighbor's mail as read. [C12.3] In the language of git, a user who is a post may not update a reference under posts slash someone else, nor under the mail space with another post's name in the sender position, nor the held space for another post. [C12.3] If it tries, the hook prints a single line saying so, with the reference's name and the words nothing changed, and exits with failure, and git cancels the whole transaction. [C12.3]

I like a pair of small things about this hook. [image] First, it is honest about its limits. [image] If it cannot work out who is asking, or the input is not in the shape it expects, it does not guess and it does not block the world. [C12.4] It fails open, which is to say it lets the update through, but it leaves a dated notice in the post's own channel, so the failure is visible. [C12.4] A guard that locks everybody out because it is confused is worse than no guard. [image] Second, it does not restrain the Prime's post, which by the household's design may move any reference. [C12.7] The guard stops accidents among the workers. [C12.8]

The second fence is smaller. [image] It is called pre commit. [C12.5] Remember that the tree named t is a read view, detached from any branch. [C12.9] If a post, by habit, ran a plain commit there, the commit would land on no branch at all. [C12.9] The next turn, when the tool sets the view again at the branch tip, detached, that stray commit would be stranded, nearly invisible, hanging by a thread. [C12.9] So this hook looks at where the commit is being made. [C12.5] If it is in the post's read view with a detached head, it prints a bracketed word, detached, and the instruction: commit through agi at, and it refuses. [C12.5] Any other worktree, any attached head, and any commit with the no verify flag, are left alone. [C12.9]

And agi at is the answer the hook gives. [C12.12] It is the hand tool, the sibling of the turn. [C12.12] It makes the same kind of commit: it reads the tip, builds a throwaway index, adds the paths you name, checks any new nodes against the growth gate, makes a signed commit with commit tree, and moves the branch with compare and swap. [C12.12,C12.10] If the swap loses, it says raced and your edit stays where it is. [C12.11]

These are not fences made to frustrate a man. [image] They make the right thing easy, and the wrong thing loud. [image]

### html

hooksPath points git at the post's tool directory. reference-transaction acts only in the prepared phase and forbids a post from moving a peer's posts, box or held refs; it fails open with a notice and does not bind the Prime's post. pre-commit refuses a plain commit on the detached read view. agi-at is the hand write path: signed, compare-and-swap, growth-gated. [C12.1,C12.2,C12.3,C12.5,C12.12]

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

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L153-L154
~~~~
[ . -ef ~/t ]&&! git symbolic-ref -q HEAD>/dev/null&&{ echo "[detached] commit through: agi-at <path>">&2;exit 1;}
[ -x ~/hooks/pre-commit ]&&exec ~/hooks/pre-commit "$@";:
~~~~


## C13 · Stop, and the climb to the trunk

sha: 6432bf88d5

fn: piece:agi-flush
fn: piece:agi-land
fn: piece:grow-gate
fn: piece:agi-gate
live: agi-flush <- piece:agi-post@.service
uncalled: agi-land

pair C13.1: The unit runs agi-flush when the post stops. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L47-L47 ~ ExecStopPost=sh -c agi-flush
pair C13.2: agi-flush runs the turn several times so every tree lands. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ agi-turn||agi-turn||agi-turn||agi-turn
pair C13.3: It purges each directory left, saving anything unproven to an archive. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ agi-turn purge $d
pair C13.4: It detaches the read view onto the branch tip only if no commit is stranded. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ git checkout -q --detach $b
pair C13.5: The landing tool requires that the sender be the post's parent. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L226-L226 ~ is not the parent of
pair C13.6: It requires a fast-forward. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L222-L222 ~ refused: not ff
pair C13.7: It verifies the signature of every commit in the range against the ledger. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L228-L228 ~ verify-commit --raw
pair C13.8: It runs the growth gate and the regrow gate on the range. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L230-L230 ~ agi-gate $n
pair C13.9: It moves the trunk by compare-and-swap. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L231-L231 ~ git update-ref $T $n $o
pair C13.10: agi-flush checks the writer guard first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ [no-branch]
pair C13.11: Purge commits an unclean dish whole to an archive reference and says kept. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L138-L139 ~ [kept]
pair C13.12: Purge removes a dish only when it is clean against its commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L138-L138 ~ rm -rf $d;exit
pair C13.13: A stranded commit makes the detach refuse, by name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L136-L137 ~ [strand-refused]
pair C13.14: The map lists agi-land as a root tool. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L42-L42 ~ root: ff-lands a post range one edge up
pair C13.15: agi-land takes a sender, a post and a sha. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L218-L231 ~ agi-land <sender> <post> <sha>
pair C13.16: The masters' landing is the merge-tree and commit-tree procedure of the master gate skill. => 6432bf88d5:skills/agi-master-gate/SKILL.md:L3-L6 ~ merge-tree / commit-tree

### narration

A session ends. [image] Perhaps the post has said its piece and gone quiet, or perhaps its head is full and it has been told to rotate. [image] Either way the unit's stop routine runs a tool called agi flush, and its job is to leave nothing behind that cannot be accounted for. [C13.1]

Read it with me. [image] First it checks who it is, the same guard line every writer carries. [C13.10] Then it runs the turn tool, and, if that fails, again, up to several times, because a race with another writer is a thing that passes. [C13.2] Then for every directory that is still lying in the working area, it calls the turn tool's purge. [C13.3] And purge is careful. [image] It checks that the dish is clean against its commit. [C13.12] If it is, it removes the dish. [C13.12] If it is not, if there is a file outside the luggage tag, or git cannot answer, it does not delete a single byte. [C13.11] It commits the entire dish, signed, to an archive reference, and prints a bracketed word, kept, with the dish's name, so the next session's brief can tell the new mind where its predecessor's unfinished work sits. [C13.11] Last of all it detaches the read view onto the branch tip, but only if there is no commit stranded outside every reference. [C13.4] If there is, it refuses and says so. [C13.13]

So the post's branch is complete and sound. [image] But a post's branch is not the trunk. [image] For the work to be part of the engine, it has to climb. [image] And now I must be exact, because the thing I am about to describe has a pair of halves, and the first of them is built and the other is not wired to anything at this revision. [C13.14,C13.16]

The built half is a root tool called agi land. [C13.14] Let me read what it would do. [image] It takes a sender, a post, and a commit. [C13.15] It insists that the sender be the post's parent in the tree of posts, or that the post be a parent-owner landing itself. [C13.5] It insists on a fast forward: the commit must descend from the trunk's current tip, or the tool prints refused, not ff. [C13.6] Then it walks every commit in the range and asks git to verify the signature against the ledger of allowed keys; the signer must be the sender or a post under the landing post, or the tool prints refused, signed by nobody, and stops. [C13.7] It runs the growth gate over the range, and a gate I have not yet named called agi gate, which refuses a tip whose body would not regrow. [C13.8] And only then does it move the trunk, with the compare and swap we have admired several times already. [C13.9]

That is a handsome piece of work. [image] And now the honest part. [image] At this revision, nothing in the repository's cells or engine code, nor in the host's tool directories, calls it. [C13.14] I looked. [image] The way masters actually land a director's work today is the procedure described in a skill named for the master's gate: a merge tree and a commit tree, which build the landing in memory and never stage a merge in the working tree, followed by the gates and the suites. [C13.16] The tool is the engine's design for the climb. [C13.14] The skill is the hand that does it now. [C13.16] I will not tell you the engine lands a branch by itself, because it does not. [C13.14]

### html

agi-flush at stop: run the turn up to several times, purge each remaining tree (clean = remove, anything else = committed whole to an archive reference and named kept), detach the read view unless a commit is stranded. agi-land (built, no caller at this revision): sender must be the post's parent, fast-forward only, every commit signed by the sender or a post beneath, growth gate and regrow gate, compare-and-swap on the trunk. [C13.1,C13.2,C13.3,C13.4,C13.5,C13.6,C13.7,C13.8,C13.9,C13.14] The masters' landing today is the master-gate skill's merge-tree and commit-tree procedure. [C13.16]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L203-L204
~~~~
cd ~/t;P=$AGI_POST;b=refs/heads/posts/$P;{ [ "$P" ]&&[ "$AGI_ROLE" != kid ]&&git rev-parse -q --verify $b>/dev/null;}||{ echo "[no-branch] $P: a kid, or no posts/$P: nothing committed">&2;exit 5;};w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};agi-turn||agi-turn||agi-turn||agi-turn;k=$?;for d in $w/*/;do [ -d $d ]&&{ agi-turn purge $d||[ $k != 0 ]||k=1;};done
if agi-turn strand;then git checkout -q --detach $b;else k=1;fi;exit $k
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L222-L222
~~~~
git merge-base --is-ancestor $o $n||{ echo "refused: not ff";exit 1;};t=$(mktemp -d);trap 'rm -rf $t' EXIT
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L228-L229
~~~~
for c in $(git rev-list $o..$n);do s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \([^@]*\)@agi with.*/\1/p')
[ "$s" ]&&{ [ $s = $1 ]||u $s $2;}||{ echo "refused: $c signed by ${s:-nobody}: not $1, not under $2";exit 1;};done
~~~~

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L231-L231
~~~~
git update-ref $T $n $o
~~~~


## C14 · Mail is a signed commit too

sha: 6432bf88d5

fn: piece:box
live: box <- piece:agi-sync

pair C14.1: A send first asks the matrix whether the two posts are adjacent, and refuses by name if not. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [off-matrix] $P -> $2: not adjacent, nothing sent
pair C14.2: A send stops at once if the channel's tip is not the sender's own commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [squatted]
pair C14.3: The mail is a signed commit with the empty tree, the message in the body. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ git hash-object -w -t tree /dev/null
pair C14.4: The channel reference is moved by compare-and-swap. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ git update-ref $r $c "$o"
pair C14.5: A lost race is retried a bounded number of times, and then named unsent. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [unsent]
pair C14.6: A read lists the references into this post and holds a marker per sender. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ refs/held/$P/$f
pair C14.7: A read verifies each new commit's signature and refuses a bad one by name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [refused]
pair C14.8: A read prints the commit's message with printf, not echo. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ printf '[%s] %s
pair C14.9: A read moves the held marker so the mail is read once. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ git update-ref $h $c
pair C14.10: The box piece's first comment says mail is signed commits on references. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ mail = signed commits on refs
pair C14.11: Out goes to refs/box/from/to, in comes from refs/box/*/me, and held markers are under refs/held. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ held refs/held/P/FROM
pair C14.12: Two posts may mail if their levels differ by at most a step. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ levels differ by <= 1
pair C14.13: A send verifies that the tip's signer is the sender. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ for $P@agi with
pair C14.14: A read asks the matrix about each sender. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [off-matrix] $f
pair C14.15: Before the fix the read line used echo, and then moved the held marker. => c6dc743482:.agi/nodes/.geometry/engine-post.md:L336-L336 ~ echo "[$f] $(git log -1 --format=%B $c)"
pair C14.16: The boot chain once ran a fetched script through echo, and under dash echo rewrote a backslash sequence in it. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L250-L250 ~ whose echo rewrites a backslash sequence

### narration

Here is the piece called box. [C14.10] Its first comment line says it plainly: mail is signed commits on references. [C14.10] Out goes to a reference named for the sender and the recipient, under a mail space. [C14.11] In comes from references with the recipient's name last. [C14.11] And a third space, held, remembers how far each reader has read. [C14.11]

Let us read the send. [image] Before anything, the tool asks the matrix: may these posts mail each other? [C14.1] The matrix is computed from the posts file, and the rule is a fair rule: a pair of posts may mail if their levels in the tree differ by no more than a single step. [C14.12] Groups that are only labels count for nothing. [C14.12] If the answer is no, the tool prints a bracketed word, off matrix, with both names, and sends nothing. [C14.1] That is why a post cannot mail a distant ancestor directly. [C14.12]

Then it looks at the channel's current tip. [C14.2] If a commit is there, the tool asks git to verify its signature, and checks that the signer is the sender itself. [C14.13] If the tip belongs to somebody else, a squatter, it prints squatted and sends nothing. [C14.2] It will not build on a stranger's commit. [C14.2]

Now the commit. [image] The tool takes the message from standard input, and it calls commit tree with the signing flag, with a tree that is the empty tree, the tree of nothing at all. [C14.3] The message is the body. [C14.3] The parent is the old tip, so a channel is a chain of letters, each linked to the letter before it. [C14.3] And it moves the reference by compare and swap. [C14.4] If the swap loses, because the same sender, from a second session perhaps, sent at the same instant, the tool loops back and tries again, up to a limit of {{val:6432bf88d5:.agi/nodes/.geometry/engine-post.md:L331:\[ \$k -lt (\d+) \]}} attempts, and after that it prints unsent and gives up loudly. [C14.5] A bounded retry, and a loud failure. [C14.5] Never a silent drop. [C14.5]

The read does the mirror. [image] For every reference ending in the reader's name, it asks whether the sender is adjacent. [C14.14] Then, for every commit newer than the held marker, it verifies the signature, and refuses any that fail with a bracketed word, refused, the sender's name, and the commit. [C14.7] Good ones it prints, with the sender's name in brackets before the message, and then it moves the held marker to that commit, so that the same letter is never read twice. [C14.8,C14.9]

And now a short story, because it belongs here. [image] The line that prints the message used to be a plain echo. [C14.15] The shell on this machine is dash, and dash's echo is a meddlesome fellow: it interprets backslash sequences. [C14.16] A message that happened to contain a backslash and a letter b would print a backspace character, and a message that contained a backslash and a letter c would stop printing at that very point, silently, dropping the rest of the letter, while the marker moved on as if it had been read. [C14.15] The fix was a single line: print with printf, giving the message as an argument, so that nothing in it is ever interpreted. [C14.8] The same family of trouble had been found once before, in the boot chain, where an echo had rewritten a backslash inside a fetched script. [C14.16]

### html

box: mail is a signed commit with the empty tree on refs/box/<from>/<to>; a send asks the adjacency matrix, refuses a squatted channel, retries a bounded number of times by compare-and-swap, and says unsent loudly; a read verifies signatures, prints each message with printf (not echo, because dash echo interprets backslashes) and moves refs/held/<me>/<from>. [C14.10,C14.11,C14.1,C14.2,C14.5,C14.7,C14.8,C14.9]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L325-L338
~~~~
P=${AGI_POST:?};m=refs/box
# the matrix: a and b mail iff their levels differ by <= 1; level = rows up to owner, an inert row (no harness) counts 0
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def i(x):$r[x]|has("harness")|not;def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if i(x) then 0 else 1 end)+l($r[x].parent//"";n+1) end;l($a;0) as $x|l($b;0) as $y|$x>0 and $y>0 and ($r[$a]|has("harness")) and ($r[$b]|has("harness")) and $a!=$b and ($x-$y|fabs)<=1'>/dev/null;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;b=$(cat);k=0
 until o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;}
  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o" 2>/dev/null;do k=$((k+1));[ $k -lt 5 ]||{ echo "[unsent] $r: the tip moved 5 times">&2;exit 1;};done;;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
 a $f $P||{ echo "[off-matrix] $f";continue;}
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||{ echo "[refused] $f $c";break;}
  [ $1 = n ]&&echo "$f"&&continue;printf '[%s] %s\n' "$f" "$(git log -1 --format=%B $c)";git update-ref $h $c;done;done;;
carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";done;git -c transfer.fsckObjects=1 fetch -q $h "$m/*:$m/*" $x;;
esac
~~~~


## C15 · The meter: knowing when to hand over

sha: 6432bf88d5

fn: piece:agi-meter
live: agi-meter <- piece:settings.json

pair C15.1: The harness settings run agi-meter on every prompt. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "UserPromptSubmit":[{"hooks":[{"type":"command","command":"agi-meter"
pair C15.2: The meter reads the token count from the harness input, or from the transcript. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ .tokens//empty
pair C15.3: It compares the count with the window times a percent cell. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L80-L80 ~ AGI_ROTATE_PCT
pair C15.4: The rotate percent is a cell on the post's row of the posts file. => 6432bf88d5:.agi/nodes/.geometry/posts.md:L11-L11 ~ rotate_pct
pair C15.5: agi-run continues the old session unless the fresh marker exists. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L32-L38 ~ [ -e ~/.fresh ]&&rm ~/.fresh&&c=
pair C15.6: The brief walk starts from the post's card node. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ doc:card-$p
pair C15.7: The unit restarts the post when its session ends. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L49-L49 ~ Restart=always
pair C15.8: The meter prints any waiting notices first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ ls ~/.notice* >/dev/null 2>&1&&agi-notice
pair C15.9: The meter reads the window size from the input, or from a default. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ context_window
pair C15.10: Past the line it tells the post to write its card in a tree, flush, and touch the fresh marker. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L80-L80 ~ touch ~/.fresh

### narration

A mind has a limit. [image] The model that animates a post can hold only so much in its head at once, and as a session grows longer, that head grows crowded. [image] The household has a meter for it, and it is the next to last tool on our road. [image]

The harness runs the meter every time a prompt is submitted. [C15.1] The settings file we read has the line. [C15.1] And what does the meter do? [image] It is a few short lines of shell, and I find the plainness of them admirable. [image]

First it prints any waiting notices, so that a post sees the engine's messages on its very next prompt. [C15.8] Then it reads the input the harness gave it, which is a small piece of structured data. [C15.2] It looks for a field named tokens, which some harnesses supply. [C15.2] If there is none, it opens the transcript file the harness named, reads it from the end backwards, and finds the most recent line that carries a usage record, and adds up the input tokens, the cached tokens read, and the cached tokens created. [C15.2] That sum is how much the model is holding right now. [C15.2]

Then it learns the window, the size of the model's head, from the same input, or from a default. [C15.9] And it asks a simple question: is the count past a set percentage of the window? [C15.3] The percentage is a cell, with a default of {{val:6432bf88d5:.agi/nodes/.geometry/engine-post.md:L80:AGI_ROTATE_PCT:-(\d+)}} percent. [C15.3,C15.4] A cell is a setting kept in the graph, so changing it is a commit like any other. [C15.4]

If the count is past the line, the meter prints an instruction to the post. [C15.10] It says, you are at the line, write your card in its node tree, with the working tree tool, run the flush tool, and then touch a file called fresh in your home, and end your session. [C15.10] The card is a node, edited in a dish like any other node, and committed by the turn. [C15.10,C15.6] The fresh marker tells the unit, when the session ends, that the next session is to be a new session, not a resumption. [C15.5]

And then, as we saw in the very first chapters, the unit restarts the post, and the successor wakes with nothing, runs the brief, finds the card, and picks up the work. [C15.7,C15.6] The memory of a post is not its session. [image] It is the graph. [image]

### html

agi-meter runs on every prompt: it reads the token count (tokens field, or the transcript's latest usage record), compares it with the window times the rotate-percent cell, and past the line tells the post to write its card in a tree, flush, and touch the fresh marker; the unit then starts a fresh successor that reads the card through the brief. [C15.1,C15.2,C15.3,C15.10]

@@excerpt 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80
~~~~
#!/bin/sh
ls ~/.notice* >/dev/null 2>&1&&agi-notice;j=$(cat);t=$(echo "$j"|jq '.tokens//empty');[ "$t" ]||t=$(echo "$j"|jq -r .transcript_path|xargs tac 2>/dev/null|jq -nR 'first(inputs|fromjson?|select((.message.usage.input_tokens)?|type=="number")|.message.usage|.input_tokens+((.cache_read_input_tokens|numbers)//0)+((.cache_creation_input_tokens|numbers)//0))');w=$(echo "$j"|jq ".context_window//${AGI_WINDOW:-1000000}")
[ "${t:-0}" -gt $((w*${AGI_ROTATE_PCT:-47}/100)) ] 2>/dev/null&&echo "At the line ($t/$w): write your card in its node tree (agi-wt pull), run agi-flush, then: touch ~/.fresh;kill \$PPID";:
~~~~


## C16 · Is the body what the graph says? (tick and drift)

sha: 6432bf88d5

fn: piece:tick.sh
fn: piece:observe.sh
fn: piece:project.sh
uncalled: tick.sh

pair C16.1: project.sh runs the genome at the head and prints the users, units and briefs the graph wants. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L281-L282 ~ sect agi-project|sh -s
pair C16.2: observe.sh prints the users and units that actually exist. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L287-L289 ~ systemctl list-units
pair C16.3: tick.sh diffs the two lists. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L294-L296 ~ diff ~/.p ~/.q
pair C16.4: It starts only its own unit if that unit is missing. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L294-L296 ~ xargs -rn1 systemctl start
pair C16.5: It commits the drift file through agi-at. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L294-L296 ~ agi-at .agi/drift
pair C16.6: The map lists tick.sh; the uncalled line of the checker verifies that nothing calls it. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L39-L39 ~ diff them; start own unit; commit
pair C16.7: The repository's own turn lane exercises the tick piece. => 6432bf88d5:extensions/agi/tests/agi-turn.t.sh:L196-L196 ~ tick.sh

### narration

We have a last tool to look at, and it is a curious tool. [image] I include it because it shows the engine's ambition, and because I promised you honesty about what is wired and what is not. [image]

The engine has an idea about itself that goes like this. [image] The graph says what bodies ought to exist: there is a row for each post. [C16.1] The machine has what bodies do exist: users, and units, and a brief tool in each home. [C16.2] If those lists disagree, something has drifted. [C16.3] A post's unit has died. [image] A row has been added and nobody started it. [image] The engine wants to notice, and to act. [image]

So it has a few little pieces. [image] The first is called project, and it runs the genome at the head of the branch, into a scratch directory, and prints a sorted list of what the graph says should exist: a user, a unit, a brief, for each post. [C16.1] The second is called observe, and it prints a sorted list of what does exist: every user whose name begins with the household's prefix, whether it has the session start hook in its settings, and every active unit of the post kind. [C16.2] And the third is called tick. [image] It makes both lists, compares them with the plain old diff, and writes the difference into a file named for the post, in a drift directory in the tree. [C16.3] Then, for any missing unit that belongs to this very post, and no other, it asks systemd to start it. [C16.4] And finally it commits the drift file through the hand tool, so that the difference is part of the history. [C16.5]

Do notice the modesty of the thing. [image] It starts only its own unit. [C16.4] It never reaches over to start a neighbor's. [C16.4] A post that finds its neighbor missing writes the fact down and leaves the neighbor's door alone. [C16.3,C16.4]

Now, the honest part. [image] At this revision, I could find nothing that calls tick. [C16.6] No schedule names it, no unit runs it, no cell enables it, and no other piece invokes it. [C16.6] It is defined, it is tested in the repository's own test lanes, and it appears in the map. [C16.6,C16.7] But it is not scheduled. [C16.6] It is a built tool waiting for its trigger. [C16.6]

### html

project.sh prints what the graph says should exist; observe.sh prints what exists; tick.sh diffs them, starts only its own unit, and commits the drift file with agi-at. [C16.1,C16.2,C16.3,C16.4,C16.5] At this revision nothing schedules or calls tick.sh: it is built and waiting for its trigger. [C16.6]

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


## C17 · The whole path again, in a breath

sha: 6432bf88d5

fn: piece:agi-turn
fn: piece:agi-sync
fn: piece:agi-flush

pair C17.1: The node is lifted into a tree by agi-wt. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L181-L190 ~ git archive -o $d.tar
pair C17.2: The turn commits it, signed, by compare-and-swap. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L130-L146 ~ git commit-tree -S -p $t $q $n
pair C17.3: The sync folds the trunk in. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L209-L220 ~ git merge-tree --write-tree
pair C17.4: The flush leaves nothing unaccounted for. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ agi-turn purge $d
pair C17.5: A master gates the branch and lands it by the merge-tree and commit-tree procedure, onto the trunk. => 6432bf88d5:skills/agi-master-gate/SKILL.md:L3-L6 ~ merge-tree / commit-tree
pair C17.6: The brief walk prints the post's orientation at the start. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ sect brief.py|python3
pair C17.7: The unit cuts the pieces from the graph into the post's tool directory. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ bin.new/$x
pair C17.8: The turn adds exactly the tag's paths. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ --pathspec-from-file=$d.p
pair C17.9: The turn stages in a throwaway index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ GIT_INDEX_FILE=$x
pair C17.10: The growth check runs before the commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ grow.py $t
pair C17.11: The read view is re-detached onto the branch tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146 ~ git checkout -q --detach $b
pair C17.12: The reference guard stops a post from moving a peer's ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ may not move $r (a peer's ref), nothing changed
pair C17.13: The pre-commit hook stops a stray commit on the read view. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L151-L154 ~ [detached]
pair C17.14: The harness settings run agi-turn when a turn ends. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "Stop":[{"hooks":[{"type":"command","command":"agi-turn"
pair C17.15: The receipt takes the new commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145 ~ echo $c>$d.b
pair C17.16: The sect tool prints a piece with sed. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ sed -n
pair C17.17: A commit is made by agi-turn, with commit-tree. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L143 ~ git commit-tree -S
pair C17.18: A reference is moved by agi-turn's update-ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L144-L144 ~ git update-ref $r $c

### narration

Let us ride the whole road once more, friends, quickly, with the status word on our saddle, and see that you can name every stop. [image]

A post wakes, and the unit has already put the engine's tools in its hands, cut from the graph by a ribosome the size of a feed-store receipt. [C17.7] The brief tells it who it is. [C17.6] It needs to change a word in a node, so it lifts that node out of its own branch into a dish of memory, with a luggage tag and a receipt. [C17.1] It edits the word. [image] Nothing is committed, and no reference moves, and that is the point. [C17.17,C17.18]

The turn ends. [C17.14] A throwaway index is made so nobody's staging can leak in. [C17.9] The tag's paths are added from the dish, the tree is written, and its name is compared with the tip's. [C17.8] They differ, so there is work. [image] The gate looks at the additions, finds none, and waves an edit through. [C17.10] A signed commit is made on top of the tip, and the branch is moved with compare and swap. [C17.2] The receipt is updated. [C17.15]

Then the trunk is folded in: already inside, or slid forward, or merged cleanly in memory and signed, or, if it conflicts, named and mailed once. [C17.3] The read view is set again at the branch tip, detached. [C17.11] The guards stood by all the while: the reference guard refuses a post that tries to move a neighbor's branch, and the commit guard stops a stray commit where it would be stranded. [C17.12,C17.13]

The session ends. [image] The flush lands every tree, saves whatever it cannot prove clean, and leaves the branch whole. [C17.4] And then a master gates the branch and lands it by the merge tree and commit tree procedure, onto the trunk. [C17.5] The trunk is never edited. [C17.5] Only extended. [C17.5]

That is the road, friends. [image] A word, a dish, a stamp, a clasp, and a climb. [image] If you take away only a single thing, let it be this: every box you have seen tonight is a section of a text file in a repository. [C17.16] You can print it with the little tool we met at the start. [C17.16] You can read it. [image] You can check what I have said against it. [image] A machine that can be read this plainly is a machine that can be trusted, and mended, by any honest hand. [image]

I thank you for your company, and for your patience. [image] Good night. [image]

### html

The whole road: ribosome tools, brief, lift a node into a tree, edit, Stop hook, throwaway index, signed compare-and-swap commit, trunk folded in, read view detached, guards throughout, flush, the master's landing, mail, meter, card. [C17.7,C17.6,C17.1,C17.14,C17.9,C17.2,C17.3,C17.11] Every box is a section of a text file you can print with sect. [C17.16]

