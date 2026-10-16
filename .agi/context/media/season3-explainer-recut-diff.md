# M2 re-cut: diff against 7d4ee1db9e (goal:g5.4.2)

Reading guide: NEW/CHANGED lines are the sentences of the new script that are not byte-identical to a sentence of 7d4ee1db9e, each with its tag (a pair id of its own chapter, or image); REMOVED lines are old sentences that are gone; NEW PAIR lines are the pairs added or changed (by claim and cite); the IMAGE LINES section lists every image sentence of the new script, per chapter, so each seat reads its own third.

## C0: 5 new or changed sentence(s), 5 removed, 3 new or changed pair(s)

- NEW/CHANGED [C0.1] The engine's own map draws it in a single line, and that line is the first piece of bytes we will read together: the graph is git, at the trunk, with the nodes under a directory and the edges written as parents.
- NEW/CHANGED [image] It grows because workers sit at their desks and change the files.
- NEW/CHANGED [image] However small, the change we follow tonight takes a road you can read in full.
- NEW/CHANGED [C0.3] From there the work climbs until the trunk itself carries it.
- NEW/CHANGED [image] The engine does exactly that, and we will watch it do so in the very next chapter, using a tiny tool.
- REMOVED The owner of this place drew it in a single line of a map, and that line is the first piece of bytes we will read together: the graph is git, at the trunk, with the nodes under a directory and the edges written as parents.
- REMOVED It grows because workers, which the machine calls posts, sit at their desks and change the files.
- REMOVED Every change a post makes, however small, takes the very same road.
- REMOVED That commit is merged with the trunk, and it climbs, edge by edge, until the trunk itself carries it.
- REMOVED The engine does exactly that, and we will watch it do so in the very next chapter, using the smallest tool in the whole engine.
- NEW PAIR C0.4: A node is pulled into a tiny tree in memory for the session. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ tiny tree
- NEW PAIR C0.5: The engine's pieces are small templates over raw commands. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L14-L14 ~ Pieces are small templates over raw commands
- NEW PAIR C0.6: The sect tool prints a piece of an engine file with sed. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ sed -n

## C1: 3 new or changed sentence(s), 3 removed, 4 new or changed pair(s)

- NEW/CHANGED [C1.8] Our first stop is among the smallest working tools in the engine, and it is called sect.
- NEW/CHANGED [image] And yet this tiny tool does a great deal of the engine's work.
- NEW/CHANGED [C1.5] Some of the engine does not live in a pile of source files the way you might expect.
- REMOVED Our first stop is the smallest working tool in the whole engine, and it is called sect.
- REMOVED And yet every other tool in this film is found by it.
- REMOVED The engine's code does not live in a pile of source files the way you might expect.
- NEW PAIR C1.5: The engine map says each piece is extracted by name and revision with sect. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L52-L52 ~ sect <name> [REV]
- NEW PAIR C1.6: Only files whose names begin with engine and end in the markdown suffix are read. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ grep '/engine[^/]*\.md$'
- NEW PAIR C1.7: With no revision named, sect reads the head. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ r=${2:-HEAD}
- NEW PAIR C1.8: The map lists the sect piece's size. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L41-L41 ~ 214 B

## C2: 2 new or changed sentence(s), 2 removed, 8 new or changed pair(s)

- NEW/CHANGED [C2.10] It tells git that any directory is safe to read.
- NEW/CHANGED [C2.1] The root pieces and the growth pieces are not in that set.
- REMOVED It tells git that any directory is safe to read, because the repository belongs to another user and the post is only a guest in it.
- REMOVED The root pieces and the growth pieces are kept out of a post's hands on purpose, because a post has no business running them.
- NEW PAIR C2.7: It reads each engine file from the trunk with git show. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ $G show $AGI_TRUNK:$f
- NEW PAIR C2.8: The extraction is an ExecStartPre of the unit, so it runs before the post starts. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ ExecStartPre=sh -c
- NEW PAIR C2.9: It makes the key, tool, harness and hook directories. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ mkdir -p .ssh bin .claude hooks
- NEW PAIR C2.10: It tells git that any directory is safe. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ safe.directory "*"
- NEW PAIR C2.11: It lists the engine files at the trunk. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ ls-tree --name-only $AGI_TRUNK
- NEW PAIR C2.12: A failed step prints extract-failed and removes its scratch work. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ [extract-failed]
- NEW PAIR C2.13: It makes the extracted pieces executable. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ chmod +x bin.new/*
- NEW PAIR C2.14: It moves the git configuration and the harness settings into place and makes the pane's named pipe. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ mv bin/gitconfig .gitconfig;mv bin/settings.json .claude;mkfifo

## C3: 6 new or changed sentence(s), 6 removed, 6 new or changed pair(s)

- NEW/CHANGED [C3.1,C3.5] It is a goal, a closed leaf, and it will be our example for the rest of the night.
- NEW/CHANGED [C3.3] That list is how the engine's map counts the graph's edges.
- NEW/CHANGED [C3.4,C3.3] The field called next edges sits just above it, present and empty, and the map's own picture counts the parents as the edges.
- NEW/CHANGED [C3.3] If you remove a parent from the list, you have cut an edge.
- NEW/CHANGED [C3.5] A leaf that is finished says so here.
- NEW/CHANGED [C3.3] The map counts the parents lists as the edges.
- REMOVED It is a goal, a small closed leaf that this very team finished a few days ago, and it will be our example for the rest of the night.
- REMOVED That list is the whole of the graph's edge structure.
- REMOVED There is no separate table of edges.
- REMOVED If you remove a parent from the list, you have cut an edge, and nothing else needs to be told.
- REMOVED When a leaf is finished, this is the word that changes.
- REMOVED Edges are only the parents lists.
- NEW PAIR C3.3: The engine's map counts a node's parents as its edges. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L18-L18 ~ edges = parents:
- NEW PAIR C3.4: The next edges field is present in the example node and empty. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L7-L7 ~ next_edges: []
- NEW PAIR C3.8: A node is a markdown file that opens with a front matter block between dash lines. => 6432bf88d5:.agi/nodes/goal/g7.16.1.1.6.2.md:L1-L1 ~ ---
- NEW PAIR C3.9: Goal addresses may be renumbered while the mint id is kept. => 6432bf88d5:CLAUDE.md:L109-L109 ~ mint_id
- NEW PAIR C3.10: The mint id never changes, and the grid refs and provenance are keyed by it. => 6432bf88d5:CLAUDE.md:L103-L103 ~ mint id** never changes
- NEW PAIR C3.11: The growth check reads a new node's front matter with the same read_frontmatter function. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L118-L118 ~ f.read_frontmatter

## C4: 4 new or changed sentence(s), 5 removed, 6 new or changed pair(s)

- NEW/CHANGED [C4.2] There is also a named pipe that feeds the pane its input.
- NEW/CHANGED [C4.3] That pause is what lets a rotation be gentle.
- NEW/CHANGED [C4.3] It starts a fresh successor, who wakes and carries on.
- NEW/CHANGED [C4.5,C4.11] So a post exists because a row in the graph says it should, and the engine unlinks it when the row is dropped.
- REMOVED There is also a named pipe that feeds the pane its input, which is how mail can wake a sleeping post.
- REMOVED That is why a rotation is gentle.
- REMOVED It starts a fresh successor, who wakes, reads the card its predecessor left, and carries on.
- REMOVED That is the number the box's memory guard counts against when it asks whether it is wise to start another heavy job.
- REMOVED So a post exists because a row in the graph says it should, and it ceases to exist when the row goes away.
- NEW PAIR C4.6: The map describes the unit as one unit with its own uid, tree, key and pane. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L33-L33 ~ a post = one unit: own uid, tree, key, pane
- NEW PAIR C4.7: The unit runs in the agi slice. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L51-L51 ~ Slice=agi.slice
- NEW PAIR C4.8: The unit makes the post's worktree t on its own branch posts/NAME. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ worktree add -fqd $PWD/t posts/%i
- NEW PAIR C4.9: The node trees live in a wt directory under the runtime directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L181-L190 ~ RUNTIME_DIRECTORY/wt
- NEW PAIR C4.10: agi-project writes units only for rows of the current engine version. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L56-L62 ~ .engine.v==4
- NEW PAIR C4.11: A dropped row is unlinked. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L27-L27 ~ a dropped row is unlinked

## C5: 3 new or changed sentence(s), 3 removed, 7 new or changed pair(s)

- NEW/CHANGED [image] A post wakes with nothing in its head.
- NEW/CHANGED [C5.7] First, if there are any notices waiting in the post's home, among the engine's channels to a post, it prints them.
- NEW/CHANGED [C5.9,C5.11] It reads the parents of every node, treats each as an edge in both directions, spreads weight outward from those starting points over repeated passes, and prints the top few nodes, most relevant first, each with its path.
- REMOVED A post wakes with nothing at all, and that is by design.
- REMOVED First, if there are any notices waiting in the post's home, the engine's sole channel to a post, it prints them.
- REMOVED It follows the edges outward a short distance and prints a compact description of each node it finds, sorted so the most relevant come first.
- NEW PAIR C5.6: The settings file is itself one of the engine's pieces and holds the hooks. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "hooks"
- NEW PAIR C5.7: It prints any waiting notices first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ ls ~/.notice* >/dev/null 2>&1&&agi-notice
- NEW PAIR C5.8: The walk starts from the post's card, its seeds and its claims. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ doc:card-$p,$AGI_SEEDS
- NEW PAIR C5.9: brief.py spreads weight over the graph in repeated passes. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L59-L73 ~ for _ in range(30)
- NEW PAIR C5.10: The meter's notice tells a post to write its card in a node tree. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ write your card in its node tree
- NEW PAIR C5.11: brief.py prints only the top few nodes. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L59-L73 ~ [:int(k)]
- NEW PAIR C5.12: The brief prints the start of the top files up to a byte limit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ head -c ${B:-0}

## C6: 2 new or changed sentence(s), 2 removed, 6 new or changed pair(s)

- NEW/CHANGED [C6.7] Instead, it uses a tool called agi wt, and what the tool does is lift a single organelle out of the cell and set it in a dish of its own.
- NEW/CHANGED [image] Later we will watch how the trunk's news reaches the branch.
- REMOVED Instead, it uses a tool called agi wt, which is short for working tree, and what the tool does is lift a single organelle out of the cell and set it in a dish of its own.
- REMOVED The trunk reaches the branch through the merge we will watch later.
- NEW PAIR C6.7: The wt tool pulls a node's tiny tree into memory for the session. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ agi-wt pull ID
- NEW PAIR C6.8: The pull refuses without a post name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L183 ~ agi-wt: no AGI_POST
- NEW PAIR C6.9: The trees live in a wt directory under the runtime directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L184 ~ RUNTIME_DIRECTORY/wt
- NEW PAIR C6.10: The default revision is the post's own branch. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L183-L184 ~ r=${3:-posts/$AGI_POST}
- NEW PAIR C6.11: The tag holds one path per line, and agi-turn versions what it names. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L182-L182 ~ ONE PATH PER LINE in .p
- NEW PAIR C6.12: The turn lane's header says agi-link is gone. => 6432bf88d5:extensions/agi/tests/agi-turn.t.sh:L2-L2 ~ agi-link` is gone

## C7: 3 new or changed sentence(s), 4 removed, 9 new or changed pair(s)

- NEW/CHANGED [image] In our telling, the line said something else before the leaf was closed, and the post changes that word.
- NEW/CHANGED [C7.3] Otherwise the dish stays in place, and the post is told by name that it was kept.
- NEW/CHANGED [C7.8,C7.9] No commit, signature or reference moves yet.
- REMOVED Before it was closed, the line said something else, the word for work in progress, and the post changes that word.
- REMOVED No hook fires.
- REMOVED Otherwise, the whole dish is saved, signed, on an archive reference, and the post is told by name that it was kept.
- REMOVED No hook, commit, signature or reference moves yet.
- NEW PAIR C7.3: A dish with a file outside its tag is kept, not committed, and named as kept. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L134-L134 ~ kept, not in the commit
- NEW PAIR C7.4: The drop checks the dish against its commit before it removes it. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L190-L190 ~ agi-turn chk $d
- NEW PAIR C7.6: The node's path from the tag is untarred under a directory named for the mint id. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L186-L186 ~ d=$w/$(git show $r:$f
- NEW PAIR C7.7: The extracted files are unpacked into that directory. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ tar -xC $d
- NEW PAIR C7.8: A commit is made by agi-turn, with commit-tree. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L143-L143 ~ git commit-tree -S
- NEW PAIR C7.9: A reference is moved by agi-turn's update-ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L144-L144 ~ git update-ref $r $c
- NEW PAIR C7.10: The turn adds exactly the paths on the tag. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ --pathspec-from-file=$d.p
- NEW PAIR C7.11: The base commit is written to the dot-b receipt at the pull. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L189-L189 ~ git rev-parse $r>$d/.b
- NEW PAIR C7.12: The turn compares the tag's paths between the receipt and the tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L142 ~ git diff --quiet $(cat $d.b) $t

## C8: 4 new or changed sentence(s), 4 removed, 4 new or changed pair(s)

- NEW/CHANGED [image] That line matters, and I want you to see why.
- NEW/CHANGED [C8.3] The real index moves only later, when the read view is re-attached to the branch tip.
- NEW/CHANGED [C8.9] A turn in which a post only read things makes no commit for that dish.
- NEW/CHANGED [C8.2,C8.6,C8.7,C8.8,C8.9] It exports a throwaway GIT_INDEX_FILE, then for each tree with a .p tag: read the branch tip into the index, add exactly the tagged paths with the work tree pointed at the dish, write the tree object; an unchanged tree name means no commit for that dish.
- REMOVED That line is the safest thing in the whole engine, and I want you to see why.
- REMOVED It never touched the real index.
- REMOVED A turn in which a post only read things leaves no mark at all.
- REMOVED It exports a throwaway GIT_INDEX_FILE, then for each tree with a .p tag: read the branch tip into the index, add exactly the tagged paths with the work tree pointed at the dish, write the tree object; an unchanged tree name means no commit.
- NEW PAIR C8.2: The turn stages and commits in a throwaway index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ GIT_INDEX_FILE=$x
- NEW PAIR C8.3: The real index moves only when the read view is re-detached onto the branch tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146 ~ git checkout -q --detach $b
- NEW PAIR C8.4: The turn sets up with the branch name and a temporary index file name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ x=$(mktemp -u)
- NEW PAIR C8.5: The temporary file is removed when the tool exits. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ rm -f $x $x.l

## C9: 1 new or changed sentence(s), 1 removed, 5 new or changed pair(s)

- NEW/CHANGED [image] On the next turn, the post can try again.
- REMOVED On the next turn, the loop will try again from the new tip.
- NEW PAIR C9.7: The ssh signing format is set. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L254-L254 ~ format=ssh
- NEW PAIR C9.8: The post's key is made by the unit's start-up if it is missing. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L39-L39 ~ ssh-keygen -qN
- NEW PAIR C9.9: A piece keeps the one allowed signers file for every key generation. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L158-L167 ~ allowed_signers
- NEW PAIR C9.10: Between the tree and the commit the turn calls the growth check. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ grow.py $t
- NEW PAIR C9.11: It also sets the file of allowed signers and the hooks path. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L256-L263 ~ hooksPath=~/bin

## C10: 1 new or changed sentence(s), 2 removed, 8 new or changed pair(s)

- NEW/CHANGED [C10.4,C10.9] A moved node is checked at its new place, unless it moved into the deprecated directory, where retired nodes rest.
- REMOVED A moved file does not count.
- REMOVED A file under the deprecated directory, where retired nodes rest, does not count.
- NEW PAIR C10.4: A move counts as an add at the new path, because the list is read without rename detection. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L101-L101 ~ --no-renames
- NEW PAIR C10.5: Each new node is read from its staged blob and its front matter parsed. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L118-L118 ~ read_frontmatter
- NEW PAIR C10.6: A node with no readable front matter is refused as a growth-order failure. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L119-L119 ~ no readable front matter
- NEW PAIR C10.7: A node whose parents do not resolve in the staged tree is refused. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L121-L121 ~ resolve nowhere in the staged tree
- NEW PAIR C10.8: A document needs a goal as its single parent. => 6432bf88d5:.agi/context/schemas/[doc].md:L25-L27 ~ max_parents: 1
- NEW PAIR C10.9: A new node under the deprecated directory is not gated. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L102-L102 ~ .agi/nodes/deprecated/
- NEW PAIR C10.13: A new node is written through the fill tool, which opens a window for a key. => 6432bf88d5:.agi/nodes/.geometry/engine-grow.md:L160-L161 ~ FILL WINDOW OPEN
- NEW PAIR C10.14: The fill tool refuses parents the key does not unlock. => 6432bf88d5:.agi/nodes/.geometry/engine-grow.md:L159-L159 ~ unlocks

## C11: 4 new or changed sentence(s), 4 removed, 5 new or changed pair(s)

- NEW/CHANGED [C11.1] If the node itself had changed on the branch tip since the dish was lifted, then committing on top of the new tip would silently overwrite whatever changed.
- NEW/CHANGED [C11.3] If the trunk is an ancestor of the branch, there is nothing to do, and the tool also erases a little marker file.
- NEW/CHANGED [C11.10,C11.9] And it mails the nearest ancestor that actually has a harness, skipping the groups that are only labels, and stopping short of the Prime.
- NEW/CHANGED [C11.1] If the node changed on the tip since the pull, the commit goes to refs/archive/<post>/<tree> and the post is told by name.
- REMOVED If, when our dish was committed, the branch tip had changed since the dish was lifted, then committing on top of the new tip would silently overwrite whatever changed.
- REMOVED If the trunk is an ancestor of the branch, there is nothing to do, and the tool also erases a little marker file that it uses to avoid nagging.
- REMOVED And it mails the nearest ancestor that actually has a harness, skipping the groups that are only labels, and stopping short of the Prime, because the household rule is that the Prime is never boxed for this.
- REMOVED If the tip moved since the pull, the commit goes to refs/archive/<post>/<tree> and the post is told by name.
- NEW PAIR C11.1: A tree whose node changed on the tip since the pull is committed to an archive reference instead. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L142 ~ r=refs/archive/$P/$m
- NEW PAIR C11.7: A conflict is named in the post's notice file. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L218 ~ [trunk-conflict]
- NEW PAIR C11.8: A moved dish is named moved, with the archive reference that holds the commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145 ~ [moved]
- NEW PAIR C11.9: The mail walk stops below the Prime's row. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L219 ~ prime_director
- NEW PAIR C11.10: It is mailed to the nearest harnessed ancestor, once per episode of conflict. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L218-L219 ~ box send $u

## C12: 1 new or changed sentence(s), 2 removed, 6 new or changed pair(s)

- NEW/CHANGED [image] They make the right thing easy, and the wrong thing loud.
- REMOVED It was never meant to bind the man who owns the barn.
- REMOVED They make the right thing easy, the wrong thing loud, and the dangerous thing impossible.
- NEW PAIR C12.6: The hook is called for prepared, committed and aborted, and git honours a refusal only in prepared. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ honours a non-zero exit ONLY in prepared
- NEW PAIR C12.7: The Prime's post may move any reference. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ agi-belam)exit 0
- NEW PAIR C12.8: The hook exists so that a post's mistake cannot move a peer's ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ a post's MISTAKE cannot move a peer's ref
- NEW PAIR C12.9: The read view is a read view, and a commit made there is on no ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L151-L154 ~ ~/t is a read view
- NEW PAIR C12.10: agi-at checks new nodes with the growth check before it commits. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L85-L90 ~ grow.py $t>&2||exit 6
- NEW PAIR C12.11: agi-at says raced and keeps the edit when the swap loses. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L85-L90 ~ [raced]

## C13: 0 new or changed sentence(s), 0 removed, 6 new or changed pair(s)

- NEW PAIR C13.10: agi-flush checks the writer guard first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L201-L204 ~ [no-branch]
- NEW PAIR C13.11: Purge commits an unclean dish whole to an archive reference and says kept. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L138-L139 ~ [kept]
- NEW PAIR C13.12: Purge removes a dish only when it is clean against its commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L138-L138 ~ rm -rf $d;exit
- NEW PAIR C13.13: A stranded commit makes the detach refuse, by name. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L136-L137 ~ [strand-refused]
- NEW PAIR C13.14: The map lists agi-land as a root tool. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L42-L42 ~ root: ff-lands a post range one edge up
- NEW PAIR C13.15: agi-land takes a sender, a post and a sha. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L218-L231 ~ agi-land <sender> <post> <sha>

## C14: 1 new or changed sentence(s), 2 removed, 7 new or changed pair(s)

- NEW/CHANGED [C14.12] That is why a post cannot mail a distant ancestor directly.
- REMOVED That is why some posts must ask a master to relay a message for them, and that is the reason you sometimes hear a master say, the Prime cannot mail you directly.
- REMOVED The stored commit was intact; only the printing lied.
- NEW PAIR C14.10: The box piece's first comment says mail is signed commits on references. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ mail = signed commits on refs
- NEW PAIR C14.11: Out goes to refs/box/from/to, in comes from refs/box/*/me, and held markers are under refs/held. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ held refs/held/P/FROM
- NEW PAIR C14.12: Two posts may mail if their levels differ by at most a step. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ levels differ by <= 1
- NEW PAIR C14.13: A send verifies that the tip's signer is the sender. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ for $P@agi with
- NEW PAIR C14.14: A read asks the matrix about each sender. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L322-L338 ~ [off-matrix] $f
- NEW PAIR C14.15: Before the fix the read line used echo, and then moved the held marker. => c6dc743482:.agi/nodes/.geometry/engine-post.md:L336-L336 ~ echo "[$f] $(git log -1 --format=%B $c)"
- NEW PAIR C14.16: The boot chain once ran a fetched script through echo, and under dash echo rewrote a backslash sequence in it. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L250-L250 ~ whose echo rewrites a backslash sequence

## C15: 0 new or changed sentence(s), 0 removed, 6 new or changed pair(s)

- NEW PAIR C15.4: The rotate percent is a cell on the post's row of the posts file. => 6432bf88d5:.agi/nodes/.geometry/posts.md:L11-L11 ~ rotate_pct
- NEW PAIR C15.5: agi-run continues the old session unless the fresh marker exists. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L32-L38 ~ [ -e ~/.fresh ]&&rm ~/.fresh&&c=
- NEW PAIR C15.6: The brief walk starts from the post's card node. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ doc:card-$p
- NEW PAIR C15.7: The unit restarts the post when its session ends. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L49-L49 ~ Restart=always
- NEW PAIR C15.8: The meter prints any waiting notices first. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ ls ~/.notice* >/dev/null 2>&1&&agi-notice
- NEW PAIR C15.9: The meter reads the window size from the input, or from a default. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L78-L80 ~ context_window

## C16: 0 new or changed sentence(s), 0 removed, 2 new or changed pair(s)

- NEW PAIR C16.6: The map lists tick.sh; the uncalled line of the checker verifies that nothing calls it. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L39-L39 ~ diff them; start own unit; commit
- NEW PAIR C16.7: The repository's own turn lane exercises the tick piece. => 6432bf88d5:extensions/agi/tests/agi-turn.t.sh:L196-L196 ~ tick.sh

## C17: 1 new or changed sentence(s), 1 removed, 12 new or changed pair(s)

- NEW/CHANGED [C17.5] And then a master gates the branch and lands it by the merge tree and commit tree procedure, onto the trunk.
- REMOVED And then a master lands the branch, a signed range, a single edge up, with a fast forward and the gates, onto the trunk.
- NEW PAIR C17.5: A master gates the branch and lands it by the merge-tree and commit-tree procedure, onto the trunk. => 6432bf88d5:skills/agi-master-gate/SKILL.md:L3-L6 ~ merge-tree / commit-tree
- NEW PAIR C17.6: The brief walk prints the post's orientation at the start. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L49-L54 ~ sect brief.py|python3
- NEW PAIR C17.7: The unit cuts the pieces from the graph into the post's tool directory. => 6432bf88d5:.agi/nodes/.geometry/engine-root.md:L41-L41 ~ bin.new/$x
- NEW PAIR C17.8: The turn adds exactly the tag's paths. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L140-L140 ~ --pathspec-from-file=$d.p
- NEW PAIR C17.9: The turn stages in a throwaway index. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L132-L132 ~ GIT_INDEX_FILE=$x
- NEW PAIR C17.10: The growth check runs before the commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L141-L141 ~ grow.py $t
- NEW PAIR C17.11: The read view is re-detached onto the branch tip. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L146-L146 ~ git checkout -q --detach $b
- NEW PAIR C17.12: The reference guard stops a post from moving a peer's ref. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L167-L176 ~ may not move $r (a peer's ref), nothing changed
- NEW PAIR C17.13: The pre-commit hook stops a stray commit on the read view. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L151-L154 ~ [detached]
- NEW PAIR C17.14: The harness settings run agi-turn when a turn ends. => 6432bf88d5:.agi/nodes/.geometry/engine-wrap.md:L43-L43 ~ "Stop":[{"hooks":[{"type":"command","command":"agi-turn"
- NEW PAIR C17.15: The receipt takes the new commit. => 6432bf88d5:.agi/nodes/.geometry/engine-post.md:L145-L145 ~ echo $c>$d.b
- NEW PAIR C17.16: The sect tool prints a piece with sed. => 6432bf88d5:.agi/nodes/.geometry/engine.md:L76-L77 ~ sed -n

TOTAL: 41 new or changed sentences, 46 removed, 110 new or changed pairs.

# IMAGE LINES (every image sentence of the new script)

## C0 (17)
- Well now, good evening, friends, and welcome.
- Pull up a chair and make yourself comfortable, for we have a long road ahead of us tonight, and I intend to walk it slowly, the way a gentleman walks a porch at sundown.
- I am going to show you, step by careful step, how a single change travels through a living machine.
- Let me set the scene.
- Now, a graph that only sits still is a library.
- This garden grows.
- It grows because workers sit at their desks and change the files.
- And here is the thing I want you to hold in your mind for the next hour.
- However small, the change we follow tonight takes a road you can read in full.
- So here is our promise to each other.
- We are going to follow a single line of a single node, a status line, a handful of bytes, from the moment a post picks it up to the moment the trunk holds it.
- I should tell you a last thing before we ride out.
- The pieces you will see tonight are sometimes called ribosomes and function blocks, and I will lean on that picture, because it is a fair picture.
- A ribosome reads a strand of instructions and builds a small working tool.
- The engine does exactly that, and we will watch it do so in the very next chapter, using a tiny tool.
- So settle in, friends.
- We begin with a few bytes, and a tool small enough to hold in your hand.

## C1 (14)
- You could write it on the back of a feed-store receipt.
- And yet this tiny tool does a great deal of the engine's work.
- Here is the job.
- Let me walk it slowly.
- Think of it as a ribbon unrolling from a spool.
- The last step is the interesting part.
- That is the whole machine.
- A reader that finds a start mark, copies until a stop mark, and lets go.
- If you have ever heard how a ribosome slides along a strand of messenger and builds a protein, you already have the picture.
- The strand is a long engine file.
- The start signal is the heading.
- The stop signal is the next heading.
- The protein it releases is a tool you can run.
- A reader that finds a start mark, copies, and stops.

## C2 (7)
- Now let us watch the ribosome at work on a much larger strand.
- And where does it get them?
- Next, a sanity check that I find mighty comforting.
- The machine would rather refuse to start than run on the wrong ground.
- Now comes the heart of it, and you will recognize it.
- The glob matters, so let me say plainly what it is.
- A gentleman does not burn the bridge before he is sure of the far bank.

## C3 (14)
- We have tools now.
- Let us meet what they work upon, for a tool without a material is just ornament.
- The material is the node.
- Here, on the screen, is the top of a real node.
- Look at the first lines.
- I want you to remember that difference, because it saves a great deal of confusion.
- Now the line that matters most for tonight: the parents.
- And here is the line we are going to carry on our journey.
- It is the status line.
- It is a small thing, a mere handful of characters, and I chose it for that very reason.
- When you have followed a handful of bytes all the way to the trunk, you have followed anything.
- Hold the status line in your mind.
- Next we meet the creature that holds it.
- The status line is the few bytes we follow.

## C4 (12)
- I know that is a dry way to put it, so let me dress it up.
- Think of a single living cell.
- It has a wall, a nucleus, and a bit of its own cytoplasm.
- Let us read the unit's own words.
- That percent i is systemd's way of saying, whatever this instance is called.
- Look at the line that starts the work.
- Now the lines that make me feel the machine is looking after its own.
- When a post decides its head is full and ends its session, the unit does not mourn.
- And who writes this unit, you may ask?
- Nobody has to remember to start it or stop it by hand.
- That is the body: a wall, a nucleus, a branch of its own, and a promise to restart.
- In the next chapter we wake it up.

## C5 (16)
- The cell is built.
- Now we wake it.
- And I should tell you how a post wakes, because it is nothing like how a man wakes.
- A man wakes with yesterday still in his head.
- A post wakes with nothing in its head.
- We will meet each of them in turn.
- What does the brief do?
- There is the ribosome again, supplying the very tool that reads the graph.
- Nothing here is a scratch file.
- A post's memory, you see, is the graph.
- The brief does a couple more kind things.
- And so the post is awake, oriented, and holding a map of its own corner of the graph.
- It has a task.
- The task is to change a line.
- And for that, it needs to lift a single node out of the graph and into a dish of its own.
- That is where we go next.

## C6 (12)
- Our post is awake and has a job: change a line of a node.
- Now, it could go and fetch the whole graph, but that would be like moving the entire library to a desk just to correct a single misspelled word.
- Let us read how.
- Then comes the search.
- That is worth stating plainly.
- Later we will watch how the trunk's news reaches the branch.
- That is the permanent birth certificate again, doing honest work.
- This tag is important.
- I should be careful here to speak plainly about what is old and what is new.
- Neither is part of the road we walk tonight.
- So here we are.
- The post may now edit.

## C7 (14)
- Now the edit itself.
- I want to be careful, because this is the moment where it would be easy to imagine a great deal going on, and in truth, nothing is going on at all.
- The post has a tool for changing files, which is an ordinary text editing tool of the harness.
- In our telling, the line said something else before the leaf was closed, and the post changes that word.
- That is all.
- A word of a few letters, swapped for another.
- And here is what I would have you notice.
- But the engine has been set up so that the room is never forgotten.
- Remember the luggage tag.
- There is a second guard, and it is rather elegant.
- So the stage is set.
- A word has changed.
- The dish is dirty and the history is clean.
- And in a moment, the turn will end.

## C8 (18)
- The model finishes its answer.
- The turn ends.
- This is the hinge of the whole story, so I will go slowly.
- First, the tool sets itself up.
- That line matters, and I want you to see why.
- The index is the place where git stages what is about to be committed.
- If a pair of things shared the real index, either could stage something and the other could commit it by accident.
- Then the loop.
- For each dish that has a tag, it does a few things in a row.
- Second, it asks git to add, but with a twist.
- Only those.
- This is a content address: a name derived from the bytes of every file in the new state of the branch.
- And that is the test that follows.
- No commit, no noise.
- Our post did change a word.
- What it does next, the gate and the stamp, are the next chapters.
- For now, take a breath, friends, and notice how little it took to get here: a throwaway index, a pathspec from a tag, and a content address.
- Honest tools from git, arranged in a row.

## C9 (15)
- We have a new tree, a content address that says what the post's branch ought to look like with the edit in it.
- Now we turn it into history.
- That command does nothing clever.
- How does the tool know how to sign?
- I have it on the screen.
- Now the delicate part.
- The tool has a new commit.
- It must make the branch point at it.
- How does the tool avoid trampling them?
- Nothing is destroyed.
- On the next turn, the post can try again.
- When the swap succeeds, there is a little bookkeeping step.
- But hold on.
- We skipped something, did we not?
- Let us go and meet the gatekeeper.

## C10 (12)
- Here is the gatekeeper.
- I want you to see how modest the question is.
- That is the answer for our example.
- We changed the word in a status line of a node that already exists.
- The gate swings open without a word.
- It was important to say so, because otherwise you might think every small edit has to pass through a long inquisition.
- It does not.
- But since we are standing at the gate, let me tell you what it does for a newcomer, for that is a thing worth seeing.
- The key is the name of a door.
- So: a gate that waves edits through and weighs only newcomers.
- That is a sensible gate, to my mind.
- It protects the shape of the garden without making a man ask permission to prune a branch.

## C11 (18)
- The commit is made.
- The edit is safe in the post's branch.
- But the branch is not alone in the world.
- While our post was thinking, the trunk, which is the shared line of history that everyone's work eventually joins, may have moved on.
- Other posts, other directors, may have landed work.
- First, a footnote about the tree that moved.
- The tool does not do that.
- The post can recover and merge by hand.
- That is the safe answer to a race it cannot decide.
- Now to agi sync proper.
- It asks questions, in order, with git.
- The first question: is the trunk already part of my branch?
- It exits.
- The second question: am I merely behind?
- A plain slide forward, tidy as a man smoothing a tablecloth.
- The last question is the hard question: have we diverged?
- Remarkable how much care sits behind a word of a few letters.
- But the care is the point, and now we turn to the guards that make the safe road the only road.

## C12 (8)
- What does it forbid?
- Let me say it the way a neighbor would.
- I like a pair of small things about this hook.
- First, it is honest about its limits.
- A guard that locks everybody out because it is confused is worse than no guard.
- The second fence is smaller.
- These are not fences made to frustrate a man.
- They make the right thing easy, and the wrong thing loud.

## C13 (13)
- A session ends.
- Perhaps the post has said its piece and gone quiet, or perhaps its head is full and it has been told to rotate.
- Read it with me.
- And purge is careful.
- So the post's branch is complete and sound.
- But a post's branch is not the trunk.
- For the work to be part of the engine, it has to climb.
- Let me read what it would do.
- That is a handsome piece of work.
- And now the honest part.
- I looked.
- The tool is the engine's design for the climb.
- The skill is the hand that does it now.

## C14 (4)
- Let us read the send.
- Now the commit.
- The read does the mirror.
- And now a short story, because it belongs here.

## C15 (7)
- A mind has a limit.
- The model that animates a post can hold only so much in its head at once, and as a session grows longer, that head grows crowded.
- The household has a meter for it, and it is the next to last tool on our road.
- And what does the meter do?
- It is a few short lines of shell, and I find the plainness of them admirable.
- The memory of a post is not its session.
- It is the graph.

## C16 (11)
- We have a last tool to look at, and it is a curious tool.
- I include it because it shows the engine's ambition, and because I promised you honesty about what is wired and what is not.
- The engine has an idea about itself that goes like this.
- A post's unit has died.
- A row has been added and nobody started it.
- The engine wants to notice, and to act.
- So it has a few little pieces.
- And the third is called tick.
- Do notice the modesty of the thing.
- Now, the honest part.
- It is a built tool waiting for its trigger.

## C17 (12)
- Let us ride the whole road once more, friends, quickly, with the status word on our saddle, and see that you can name every stop.
- It edits the word.
- Nothing happens, nothing at all, and that is the point.
- They differ, so there is work.
- The session ends.
- That is the road, friends.
- A word, a dish, a stamp, a clasp, and a climb.
- You can read it.
- You can check what I have said against it.
- A machine that can be read this plainly is a machine that can be trusted, and mended, by any honest hand.
- I thank you for your company, and for your patience.
- Good night.

