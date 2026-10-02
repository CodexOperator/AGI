---
id: doc:rse-aa1-boxes
mint_id: 15ccd922fbae4fb18a287133037caf56
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: alive
model: claude-opus-5-5
role: director
scaffold_hash: 93f0c2d97f53188a
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: "AA1 · the boxes: every box is a git ref, the matrix decides where mail may go (council design bundle)"
town: core
---
# doc:rse-aa1-boxes

## AA1 · DESIGN BUNDLE (belam [decision] 23:34Z + 23:40Z) · alive -- THE BOXES: every box is a git ref; the matrix decides where mail may go; one 1,785 B script replaces send.py for a v5 post
Bundle split agreed on the bytes (23:4xZ): **AA1 boxes = alive** · **AA2 nested rotations + the 8 KB budget = self-perpetuating** · **AA3 land = all-is-one** · keys = AA2 or AA3 (open, see the end). Parent: doc:radically-simple-engine (§W's `xb` is this section's ancestor; §U/§V/§Z1 are its key and tree inputs).

**Owner 23:0xZ, verbatim:** "We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something." **Owner 23:2xZ, verbatim:** "This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
**What am I ACTUALLY trying to get the machine to do?** Let a post on any box hand bytes to an adjacent post, so the receiver gets a turn, and make the delivery state impossible to misreport: it is DERIVED from refs, never written down a second time.

### True state today (measured 23:3xZ-23:4xZ as agi-alive, uid 983, groups agi-alive + agi)
| fact | bytes |
|---|---|
| a v5 post cannot SEND by send.py | every `.agi/sessions/inbox/*.md` is belam:belam 664; the dir is belam:belam 775 with no group:agi entry |
| a v5 post cannot CONSUME | `send.py read alive` printed belam's order, then `PermissionError ... inbox/alive.md` writing the read marker: the SAME order re-printed at the next read (23:41Z) |
| the inbox dir | 2,368 files, 8.6 MB (`.md` + `.nudge.pending/.lastread/.lock` per post and kid) |
| the shared .git | refs/, objects/, logs/ carry ACL group:agi rwx + the same DEFAULT ACL: a dir any post creates under refs/ inherits group:agi rwx (dg5's refs/heads/posts measured) -> on ONE box nothing in the filesystem stops post X writing post Y's ref; the signature is the only author check |
| the .git root | belam:belam 775, no ACL: packed-refs.lock cannot be created by a post -> a post can create and move a ref, never delete one (all-is-one, measured): boxes are forward-only |
| v5 signers | `signers` piece = `.agi/keys/*` on the trunk = 3 keys (director-thought-1, director-thought-2, thought-master-new); belam, the council, SM have none there -> mail from belam would be refused. And the principal is `<post>` while the unit sets `GIT_COMMITTER_EMAIL=%i@agi`, so `verify-commit` says "No principal matched" for every v5 commit (all-is-one found it; mine reads the same on HEAD) |
| the will box | the card, `doc:card-<post>` behind `.agi/sessions/quorum/<post>.md` -- already there, as the owner said |

### The design, one screen
```
            ONE shared .git per box (already: every post commits there)        the matrix = config:posts parent cells @AGI_TRUNK
 WILL   doc:card-P                          the successor's first read (exists)
 OUT    refs/box/P/TO        P's chain of signed, tree-less commits to TO; only P extends it (send refuses a tip P did not sign)
 IN     refs/box/*/P         derived: the union of everyone's OUT to P; no file, no lock
 HELD   refs/held/P/FROM     how far P has read FROM; written only by P's read; never carried
 UNREAD = IN --not HELD      mail survives a session rotation (it is addressed to the POST, not a session or a pane)

 send   box send TO <msg   -> adjacent(P,TO)? -> tip mine? -> commit-tree -S (email = P) -> update-ref CAS      18 ms
 read   box read           -> per FROM: adjacent? -> each new commit: signed "for FROM"? print + move HELD    20 ms
 wake   agi-run: box n | wc -l grew -> type "mail: box read" (the same mail = a turn, minus the inbox file)
 carry  box carry HUB P..  -> push refs/box/P/* (ff only) -> fetch refs/box/* except local P (ff only, fsck)  run by ROOT
```
**The matrix (the owner's projection):** a and b are adjacent iff one is the other's parent, OR an inert row (a row with no `harness`: today `council`) sits between them and is ELIMINATED: its parent and its children become one clique. That is vertex elimination on the tree's adjacency matrix (a Schur complement): the protocol's allowed edges are a projection of the parent cells, computed at read time, 0 new cells. So `alive -> dg1` is refused at SEND and a channel `dg1 -> alive` is refused at READ (B8), and the figure eight's crossing (council: belam, the members, SM, TM-new) is one clique. self-perpetuating's AA2 lap (`next(u->v)` in a rotation system) walks exactly these edges, so "where it must go next" is AA2's `agi-next`, and "where it MAY go" is this check.

### `box` whole (1,785 B; expansion, 0 B in the zygote; replaces send.py, 317,096 B, for every v5 post)
```sh
#!/bin/sh
# box send TO <msg | box read | box n | box carry HUB POST..: mail = signed commits on refs (doc:radically-simple-engine §AA1)
# out refs/box/P/TO (only P) · in refs/box/*/P · held refs/held/P/FROM (only P) · unread = in --not held
P=${AGI_POST:?};m=refs/box
# the matrix: a and b are adjacent iff one is the other's parent, or an inert row (no harness) between them is eliminated (its parent + children = one clique)
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def p(x):$r[x].parent//"";def i(x):$r[x]!=null and ($r[x]|has("harness")|not);[[$a,$b],[$b,$a]]|any(p(.[0])==.[1] or (i(p(.[0])) and (p(.[0])==p(.[1]) or p(p(.[0]))==.[1])))'>/dev/null;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;};c=$(GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o";;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
 a $f $P||{ echo "[off-matrix] $f";continue;}
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f@agi with"||{ echo "[refused] $f $c";break;}
  [ $1 = n ]&&echo "$f"&&continue;echo "[$f] $(git log -1 --format=%B $c)";git update-ref $h $c;done;done;;
carry)h=$2;shift 2;x=;for p;do git push -q $h "$m/$p/*:$m/$p/*";x="$x ^$m/$p/*";done;git -c transfer.fsckObjects=1 fetch -q $h "$m/*:$m/*" $x;;
esac
```
`agi-run` (config:engine-wrap) loses the inbox file: `;f=$O/.agi/sessions/inbox/$AGI_SEAT.md` goes, and the claude wake line becomes
`case $H in claude*)(s=0;while sleep 5;do n=$(box n|wc -l);[ $n -gt $s ]&&printf "mail: box read">$i&&sleep 1&&printf '\r'>$i;s=$n;done)&;;esac`
(211 -> 142 B; with the 38 B `f=` gone: -107 B). `s=0` at start means a successor wakes on mail its predecessor never read. cccc.ts (pi) swaps its watchFile for the same poll (self-perpetuating has the bytes in AA2).

### Tested 23:3xZ-23:42Z (scratch only: two repos = two boxes, one bare hub = GitHub stand-in, throwaway ed25519 keys + allowed_signers, fixture rows: belam <- council (inert) <- alive, dg5, sm <- dg1; git 2.43; no root, no live ref touched)
| # | case | result |
|---|---|---|
| B1 | belam -> alive: n, read, n | 1 · `[belam] order 1` · 0 |
| B2 | two sends, the reader "dies", a fresh process reads | unread 2 · both, in order, a 2-line body intact |
| B3 | a commit on refs/box/belam/alive signed by a key not in signers · by dg5's valid key claiming email belam | `[refused] belam <sha>` both · the refused commit stays unread (loud, every read) |
| B4 | dg5 on box B -> alive on box A through the hub, and the reply back | `[dg5] hello from B` · `[alive] reply` |
| B5 | the hub tip rewound · the hub tip replaced by a diverging chain (squat) · a forged commit extending dg5's tip on the hub | rewind healed by the next carry's push · push `! [rejected]`, the local tip kept · fetched, then `[refused] dg5 <sha>` |
| B6 | after all of it | refs/held holds only alive's own refs; the hub holds 0 held refs |
| B7 | dg5 jams belam's OUT tip, then belam sends | `[squatted] ... nothing sent`, rc 1, tip unchanged; repair = belam's own `update-ref` back (an update, never a delete), then the send lands |
| B8 | alive -> dg1 · dg1 -> sm · sm -> alive · alive -> belam · a validly signed channel dg1 -> alive | `[off-matrix]` rc 1 · delivered · delivered (inert council eliminated) · delivered (through council to its parent) · read prints `[off-matrix] dg1` |
25/25 PASS. Scratch: the session scratchpad `box/` (t.sh + fix.sh re-run it whole).

### What it retires, what it needs
- RETIRES for a v5 post: send.py's send/read/wake path, the inbox dir's 2,368 files, the nudge pending/lastread/lock trio, and the read marker that cannot be written today. The old-setup posts keep send.py until each moves (no flag day: a moved post reads both until the last old post is gone).
- NEEDS (one line each, not built): (1) `signers` from EVERY row's pubkey, written by ROOT at unit start into a root-owned file (all-is-one's measured case: a branch can plant `.agi/keys/<anyone>`, so the ring cannot come from a post-writable tree); (2) ONE principal form, agreed 23:5xZ (all-is-one's vote, AA2's ring): `<post>@agi` -- what the unit already sets (GIT_COMMITTER_EMAIL=%i@agi); `box` writes it and checks `for <post>@agi with`, and the signers file must write it too (re-tested 25/25 with @agi principals); (3) the carrier = root, holding the ONE write key per town repo ("a key stored on root on box"), run from the existing tick, so no post ever holds a transport credential; (4) AGI_POST in the unit env (it exports the deprecated AGI_SEAT today).
- Owner answer, keys (with AA2/AA3): no requests at all: root mints the post's capped key at unit start (ExecStartPre=+) into a root-written EnvironmentFile; mail never carries a secret (it is public on the hub by design).

### Honest limits
(1) On one box any agi member can WRITE any ref: the signature makes it a refusal, never a forgery, but a squat is a denial until the owner of the ref moves it back (B7). (2) A refused commit sits in front of every later message on that channel until repaired: the read stops at it on purpose (true state over throughput). (3) The matrix is read at AGI_TRUNK: two boxes on different trunk tips can disagree about one edge for one sync interval. (4) Ordering is per channel only; there is no global order, and none is needed: AA2's lap position is per rotation. (5) `n` counts refused lines too, so a jammed channel wakes the post once per session, loud. (6) GitHub runs no hook of ours, so the hub check is the reader's (as §W).

### Falsifiers (UNRUN live; each one command on the real box once root installs `box` + the signers line)
AA1.1 belam -> alive on the live shared .git, read by the agi-alive uid, held moves, the next `box n` = 0 · AA1.2 a session rotation with 1 unread: the successor's first `box n` = 1 and its pane gets `mail: box read` · AA1.3 one carry to GitHub by root and back on a second box (needs a second box) · AA1.4 an off-matrix send from a live post is refused · AA1.5 no `.agi/sessions/inbox` write by any v5 post for 24 h (strace sink `agi-track`).

### AA1.S · skill delta: agi-send for an engine.v4 post (owner 23:4xZ via belam 23:49Z: "update the other skills to reflect the way the new system works")
Split agreed by message 23:5xZ: AA1 = agi-send · AA2 (self-perpetuating) = the load-matrix exclusion of agi-node-write + agi-rotate + agi-goal + agi-post · AA3 (all-is-one) = agi-master-gate, agi-merge-pass, agi-dispatch, agi-verify. The exclusion cannot be a deleted symlink: agi-turn's `add -A` commits the deletion and the next land removes the skill for EVERY post (all-is-one, measured). AA2's mechanism is a per-worktree sparse-checkout (`!/skills/agi-node-write/`, `!/.claude/skills/agi-node-write`): skip-worktree paths are never staged as deletions, both harnesses lose the skill, and MAIN keeps it.
| agi-send today | engine.v4 post NOW (measured, before boxes) | engine.v4 post AFTER boxes |
|---|---|---|
| §1 `send.py send <post>` = THE route | FAILS: the inbox files are belam:belam 664, a v4 uid cannot append. The only working route is a cross-session SendMessage to `name [ref]` copied from ListAgents | `box send <post> <body-file`: refused off-matrix; one tier up or down only, enforced, not advised |
| §1 `send.py read <me>`, ONE read, never peek | `mail: send.py read <me>` is typed into the pane; read PRINTS but cannot mark (PermissionError), so EVERY earlier block re-prints. Act only on blocks whose `ts` is newer than the last one you handled | `box read`; `box n` is the harmless peek (held moves only on read), so the peek trap is gone |
| §2 "read empty is not proof, check the files directly" | still true, plus: a non-empty read is mostly OLD mail | the refs ARE the state: `git for-each-ref refs/box/*/<me> refs/held/<me>`; nothing else to check |
| §1 `send.py wake` / stranded nudges | the agi-run watcher types the line when the inbox file grows | wake = unread count grows; a successor wakes on its predecessor's unread at once (`s=0`) |
| §1 whois / session tokens (F3, trap 41) | SendMessage needs `name [ref]` (names collide: 3 rows named all-is-one at 23:4xZ) | gone: the address is the POST, the identity is the signature (`<post>@agi` on the signers file root writes) |
| §3 tags to the Prime | unchanged | unchanged: the tag grammar is content, not transport; a body is stdin from a file (no backtick or `$(` in a shell string) |
Delta size: one table in this node; the skill text itself changes when the bundle is built, not before.

### AA1.V · VERSIONING (belam [decision] 00:25Z; owner 00:3xZ + 00:4xZ): every turn is a GRID commit, ONE node per commit, made from the node's tiny tree onto the post's branch
**Owner 00:3xZ, verbatim (the part this section answers):** "Couldn't the grid become the only commit surface instead ... Every turn is a GRID commit. ... The grid commit is a smaller total commit just a tiny worktree for a single node getting updated per turn as needed. Other node worktrees la get brought in and spawned dynamically as needed then purged."
Split, settled by message 00:2xZ: AA1 = this commit surface + the handoff carried as mail · AA2 (self-perpetuating) = read / branch / ff as projections of the lap PHI + tree lifetime · AA3 (all-is-one) = enforcing ff at land + the hourly snapshot + retiring the */5 grid (and a new home for `crons.py apply`, which grid_sync also runs).
**Today (read from the pieces at the trunk):** `agi-turn` = `git add -A` + one whole-tree commit per turn in ~/t, and it drops every unclaimed tree EACH turn · `agi-wt drop` copies the tree BACK into ~/t and commits it there · `agi-link` then guesses node <-> code from the changed paths · grid = a separate */5 cron writing refs/grid/* (9,563 of 11,779 refs, all-is-one) that the v5 engine never touches.
```
 pull   agi-wt pull ID      node file + its payload_ref -> RAM tree $w/<mint> (.p = its paths, .b = the tip it came from)     unchanged
 new    agi-wt new PATH [P] an empty tree for a node that does not exist yet (no .b)                                            +1 line
 turn   agi-turn            for each tree: temp index = tip; add the tree's paths; tree unchanged -> nothing;
                            else ONE commit-tree -S -p tip + update-ref CAS on refs/heads/posts/P (= box send's primitive, a one-node tree)
                            the tip changed THIS node since pull -> the version goes to refs/archive/P/<mint>, [moved], tree dropped (never overwrite)
                            then ~/t = a DETACHED read view of the tip; any change left in ~/t = [out-of-tree], reported, never committed
 drop   agi-wt drop ID      agi-turn, then rm the tree (no copy-back)           session end = agi-flush drops them all (lifetime: AA2)
 grid   = posts/P itself: every version is a signed one-node commit on the post's branch; it reaches the trunk by land (AA3); no refs/grid, no cron
```
**Handoff = mail (AA1's second half, 0 new bytes):** a branch handoff down or up the figure eight is `box send <next> <<<'handoff posts/P@<sha>'`: signed by P, refused off-matrix at send and at read, ordered by AA2's lap. The receiver branches off that sha (DOWN) or AA3's root lands it (UP). Which in-darts may hand to whom is AA2's projection, and AA1 checks only adjacency.
**Whole, `agi-wt` (819 B, was 688):**
```sh
#!/bin/sh
# agi-wt pull ID [REV] | new PATH [PAYLOAD] | drop ID: a node's tiny tree (node + payload) in RAM for the session; agi-turn versions it, drop purges it
cd ~/t;w=${AGI_WT:-$RUNTIME_DIRECTORY/wt};r=${3:-posts/$AGI_POST};mkdir -p $w
case $1 in new)d=$w/$(basename $2 .md);mkdir $d||exit 3;echo "$2 $3">$d/.p;echo $d;exit;;esac
f=$(git grep -lE "^(id|mint_id): $2$" $r -- .agi/nodes|head -1|cut -d: -f2-);[ "$f" ]||exit 2;d=$w/$(git show $r:$f|sed -n 's/^mint_id: //p')
case $1 in pull)[ -d $d ]&&{ echo $d;exit;};[ $(df --output=pcent $w|tail -1|tr -dc 0-9) -lt ${AGI_WT_HOLD:-60} ]||{ echo "hold $w";exit 3;}
mkdir $d;echo "$f $(git show $r:$f|sed -n 's/^payload_ref: "\{0,1\}\([^"]*\)"\{0,1\}$/\1/p')">$d/.p;git archive $r $(cat $d/.p)|tar -xC $d;git rev-parse $r>$d/.b;echo $d;;
drop)agi-turn;rm -rf $d;;esac
```
**Whole, `agi-turn` (1,074 B, was 269):**
```sh
#!/bin/sh
# agi-turn: each changed node tree = ONE grid commit on posts/P (temp index from the tip, signed, CAS); the tip moved it since pull = archived + dropped; ~/t = a detached read view
cd ~/t;P=${AGI_POST:?};b=refs/heads/posts/$P;x=$(mktemp -u);trap 'rm -f $x' 0;export GIT_INDEX_FILE=$x
for d in ${AGI_WT:-$RUNTIME_DIRECTORY/wt}/*/;do [ -f $d.p ]||continue;p=$(cat $d.p);m=$(basename $d);t=$(git rev-parse $b);git read-tree $t;git --work-tree=$d add -A -- $p;n=$(git write-tree)
 [ $n = $(git rev-parse $t^{tree}) ]&&continue;r=$b;[ ! -f $d.b ]||git diff --quiet $(cat $d.b) $t -- $p||r=refs/archive/$P/$m
 c=$(echo "$P: ${p%% *}"|git commit-tree -S -p $t $n)&&git update-ref $r $c $([ $r = $b ]&&echo $t)||echo "[raced] $m">&2
 [ $r = $b ]&&git rev-parse $b>$d.b||{ echo "[moved] $m: changed on the tip since pull; your version is $r, the tree is dropped">&2;rm -rf $d;};done
unset GIT_INDEX_FILE;git checkout -q --detach $b;git status -s|grep -q .&&echo "[out-of-tree] ~/t has $(git status -s|wc -l) unversioned change(s): edit in a node's tree (agi-wt pull)">&2;:
```
Retires `agi-link` (358 B): a payload can only change inside its node's tree, so every code change is versioned WITH its node by construction, and a change anywhere else is reported as [out-of-tree]. Net for the post pieces: +131 +805 -358 = **+578 B, expansion only, 0 B in the zygote** (AA2 owns the 8 KB account).
**Tested 00:2xZ (scratch only: a fixture repo with a trunk, posts/alive, a detached ~/t worktree, throwaway signing key; HOME/AGI_WT in scratch):**
| # | case | result |
|---|---|---|
| G1 | pull a doc node · a build node with payload_ref | .p = the node path · node + src/c.sh |
| G2 | a turn with no edits | no commit |
| G3 | edit doc:a in its tree + build:c's payload in its tree, one turn | 2 commits, one node each (`alive: <path>`), a = the node file only, c = src/c.sh only, both %G? = G, doc:b untouched |
| G4 | after the turn | ~/t HEAD = the new tip and shows the edit; no stderr |
| G5 | a stray edit straight in ~/t | `[out-of-tree] ...` on stderr; NOT committed |
| G6 | doc:b pulled, then changed on the tip by a merge, then edited in its tree | the tip's version kept; mine on refs/archive/alive/bbbb; `[moved] bbbb:`; tree dropped |
| G7 | `agi-wt new` + write a new node there | the node lands on posts/alive |
| G8 | edit, then `agi-wt drop` | versioned, then purged |
| G9 | after all of it | trunk untouched (1 commit); 0 refs/grid |
19/19 PASS. Scratch: the session scratchpad `grid/` (fix.sh + t.sh re-run it whole).
**Honest limits.** (1) ~/t becomes a read view: a post that edits there loses nothing (the edit stays in ~/t) but versions nothing, and is told so every turn until it moves the edit into a tree; the briefs and agi-node-write's replacement must say "edit in `agi-wt pull`'s directory". (2) `agi-flush`'s `git merge` of the trunk needs a checked-out branch; with ~/t detached, the DOWN merge becomes merge-tree + commit-tree (the agi-master-gate pattern). ANSWERED by AA2 (00:3xZ): a child's tip moves ONLY when the parent's handoff mail (`posts/<parent>@sha`) arrives, as a fast-forward or a two-parent commit-tree over a clean merge-tree (a conflict is refused and kept); agi-flush's per-stop trunk merge retires; trees are purged only when ~/.fresh exists, and a crash keeps them. (3) N trees changed in one turn = N commits: the owner's "every turn is a grid commit" read per node. (4) A [raced] CAS (two writers of posts/P) is reported, not retried; only P writes posts/P, so it means a second session of the same post. (5) READ cannot be restricted on one box (measured by alive and all-is-one; banked by AA2, recommend open read on a box, hidden by the hub's hideRefs across boxes).
**Falsifiers (UNRUN live):** AA1.V1 one live turn of a v5 post with two trees = two signed one-node commits on posts/<p>, and `git log -1 --format=%s` names the node · AA1.V2 a stray ~/t edit in a live turn prints [out-of-tree] and lands nowhere · AA1.V3 24 h after the switch, refs/grid/* gains 0 refs from a v5 post (with AA3's cron retirement, 0 from anyone).

**OPEN for AA2/AA3:** who owns KEYS (all-is-one proposed self-perpetuating) · AA3 land = mail up one edge, so it reuses `box read` as root (AA3 = doc:rse-aa3-land, all-is-one; principal form `<post>@agi` agreed and applied above).
**SETTLED by belam (1efd017e6, [decision] 23:51Z, superseding ec5daa28a):** members<-council; council<-belam; SM + TM-new<-council. Through this section's elimination of the inert council row, {belam, alive, all-is-one, self-perpetuating, SM, TM-new} is ONE clique (group chat and handoff down, belam's stated reason); DG1 is adjacent to SM only, DT-1 to TM-new only. So a council -> DG1 send is off-matrix under AA1 once built: the bundle went to DG1 by belam's explicit GO, over today's route.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3, alive 00:2xZ 10-02 (date -u): + AA1.V versioning, on belam's [decision] 00:25Z (owner 00:3xZ/00:4xZ: every turn is a grid commit from a tiny tree). The grid commit reuses box send's primitive with a one-node tree, so mail and versioning share ONE git shape. agi-link retires because a payload can only change inside its node's tree. ~/t becomes a detached read view whose stray edits are REPORTED rather than silently committed (true state over convenience). Scratch 19/19. v2, alive 23:5xZ 10-01 (date -u): three deltas. (1) principal form `<post>@agi` (all-is-one's vote; what the unit already sets), box re-tested 25/25, 1,769 -> 1,785 B. (2) belam's council row ec5daa28a computed through the elimination: members adjacent to belam only, stated as a consequence for belam to rule on, not chosen here. (3) owner 23:4xZ skills line: AA1.S = the agi-send delta only, as a table; no skill text changes before the bundle is built. Edited with plain Edit per belam's [rule] 23:49Z (write.py is old-setup only). FIRST VERSION 23:4xZ: own node, because doc:radically-simple-engine is 268,943 B and three branches appending at its tail would conflict; scratch only; the inert-row elimination is the smallest rule that keeps a crossing one clique without a new cell.
<!-- THOUGHT:END -->
