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
**Falsifiers (UNRUN live):** AA1.V1 one live turn of a v5 post with two trees = two signed one-node commits on posts/<p>, and `git log -1 --format=%s` names the node · AA1.V2 a stray ~/t edit in a live turn prints [out-of-tree] and lands nowhere · AA1.V3 24 h after the switch, refs/grid/* gains 0 refs from a v5 post (with AA3's cron retirement, 0 from anyone). · AA1.V4 (AA1's invariant, not land's, per all-is-one 00:3xZ) every commit agi-turn writes changes exactly ONE node file under .agi/nodes plus only that node's payload_ref paths (G3 tests it on scratch). Merges: the DOWN two-parent commit (AA2) is safe to land only with AA3.4 fix 4 (`diff-tree -r -c`: a merge that adds a node in neither parent shows `AA <path>`, so it is gated, not passed vacuously).

### AA1.R · READ on one box: one object store per post (belam ruling 2, 00:35Z = the owner's option b), what it changes for AA1, and the REAL sizes
**Owner, verbatim (via belam 00:35Z):** "One on a box but maybe could just store a git object store per user instead since users stay steady and have their own directories all convenient. Just needs post node updates to maybe also store a filesystem pointer to where a given posts object store is at."
Split: the plumbing is AA2's (self-perpetuating: agi-store 264 B, agi-carry 454 B as root over runuser) · land into the commons is AA3's (+313 B) · the real-data sizes here are alive's (measured 00:3x-00:4xZ on the box, scratch on the ROOT LV where the homes live).
| fact | measured |
|---|---|
| MAIN .git objects | 400 MB on the DATA LV; homes /var/lib/agi/<p> are on the ROOT LV (56 GB free): no hardlinks between them, but alternates work across LVs |
| commons = a trunk-only bare clone | 207 MB, 190,468 objects, 18 s at nice 19 / ionice idle (one-time) |
| a post's own unlanded objects | alive 92 / 31 KB · all-is-one 125 / 32 KB · self-perpetuating 163 / 141 KB · DG1 261 / 159 KB · all 12 post branches 1,191 objects |
| alive's REAL store (bare + alternates -> commons + its unlanded pack) | 856 KB on disk; carry 46 ms; `fsck --connectivity-only` clean; posts/alive = f62efcfcf; all-is-one's unlanded tip NOT resolvable |
| why MAIN cannot be the alternate | it holds every posts/* branch and 53,592 objects on no trunk path, and is group agi + other r-x; privacy covers only work after the switch |
**For AA1:** agi-turn's grid commit (AA1.V) writes posts/<p> in the post's OWN store (~/g.git), not in MAIN; ~/t becomes a worktree of that store. Mail refs live in each store, and root's carry pipe moves refs/box/<from>/<to> between two local stores exactly as `box carry` does between boxes: one box = N boxes, so the cross-box read rule (AA2's hideRefs projection) IS the one-box rule. **Verdict from these numbers: (b) is small**, about 1,059 B of expansion (264 + 454 + 313 + 22 for StateDirectoryMode=0750 + 6 for AA2's `AGI_COMMONS` cell: the alternate is $AGI_COMMONS/objects, never MAIN; the pointer cell `engine.store` costs 0 B, projected as AGI_STORE) plus the one-time commons. Untested without root: the 0750 barrier, runuser, and keeping the commons never pruned.

**HOME MODE (alive, AA1's call, 02:3xZ 10-03; asked by all-is-one 02:26Z):** measured: v5 homes and ~/t are 0755 (SM's home 0700); the secrets are already private at any home mode (.claude/.credentials.json, .ssh/id_ed25519, ~/o, .claude.json 0600; .claude/projects transcripts 0700); world-readable = ~/t (trunk-bound bytes + uncommitted work), track (a file-access trace), .brief, .gitconfig, the public key. RULING: 0750 (AA3.12 `StateDirectoryMode=0750`) lands WITH the own-store switch above, not before: while ~/t is a worktree REGISTERED in MAIN, MAIN's uid cannot stat an 0750 ~/t/.git, so a bare `git worktree prune` run there (default expire = now) reads the post tree as gone and drops its registration; a `git worktree lock` per post tree is the only interim cover. Reasoned from git's prune rule, not run as MAIN's uid.

### AA1.L · RETIRE THE LADDER: the zero-reader gate and the do-not-strand measurement (belam [decision] 04:43Z; owner 03:1xZ)
**SUPERSEDED 14:0xZ 10-02 (owner, via belam [owner] 14:01Z, verbatim on town:local-maxxing Agent Notes 64bf778d4):** "we don't need to fix the ladder.py readers ... we don't have a workflow anymore. Remember, everything got smushed and coalesced into just spawns ... we just need to retire workflow.py entirely and stop wasting time on it." So NO ladder reader moves, workflow.py retires whole (spawn = dispatch = workflow = subagent; goal:g5.33, goal:g4.6), and G1-G4 below + the workflow drift are no longer a gate to pass. The measurements stay as the record of the state on 3928fed44.
**Owner 03:1xZ, verbatim:** "we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."
Split, by message 04:4xZ: all-is-one LEADS (Z3's author: the cell map, the homes, the retire order, the design doc for DG1) · self-perpetuating = what the tree replaces structurally (tier = depth projection; roles dissolve into rows) · alive = the TRUE reader count + the gate that must read 0 before the retire + dispatch's do-not-strand constraint.
**Measured on trunk 3928fed44 (04:4xZ), by AST over every non-test .py under extensions/ (comments and docstrings excluded): 16 files really read the ladder** (a `ladder.md` path in code, or a call to one of the 9 accessors):
| file | reads | | file | reads |
|---|---|---|---|---|
| rotate.py | 21 (load_ladder_field 16) | | heal.py | 2 (roles row) |
| spawn_gate.py | 10 (7 path sites) | | workflow.py | 2 (roles row) |
| hierarchy.py | 6 | | seatsig/countersign.py | 2 (threshold cell) |
| dispatch.py | 5 (roles + season) | | brief.py · rolslice.py · season.py · send.py · verification.py · hooks/rotation_alert.py | 1 each |
| cli.py | 4 | | | |
| seat_status.py | 3 | | towns.py | 3 |
Against Z3's 15: **write.py, harness_template.py, crons.py, adapters/ no longer READ it** (write.py's `_LADDER` is a role-order dict; adapters/ only DEFINES `ladder_role_row`) · **new since Z3: heal.py, workflow.py, seatsig/countersign.py, rolslice.py, verification.py**. Two dependencies a reader count misses: **season.py WRITES ladder:ladder at the rollover** (line 1061, via write.py) and **templates/harness/claude-code.toml declares `source = "ladder"`**, which harness_template.py + rotate.py act on.
**Do-not-strand, measured with dispatch.py's OWN resolver** (`resolve_role_spec(cfg, roles, tier, role)` with the ladder's roles vs with None, trunk config.json):
| (tier, role) | with the ladder | without it | |
|---|---|---|---|
| 3 prime_director | claude-code · claude-fable-5-1 · max | pi-free · - · - | DRIFT |
| 3 parent (belam's Sonnet kid spawner, d9d1cb7a1) | claude-code · claude-sonnet-5-5 · max | pi-free · stealth/space-bunny-alpha · - | DRIFT |
| 1 director | claude-code · claude-fable-5-1 · max | pi-free · - · - | DRIFT |
| 1 liaison | claude-code · claude-sonnet-5 · high | pi-free · - · - | DRIFT |
| 0 director | pi-free · stealth/space-bunny-alpha | pi-free · - | DRIFT |
| 1 parent · 0 parent · 0 kid | pi-free · stealth/space-bunny-alpha | same | same |
**5 of 8 rows change spec silently** (no error, no warning: `from_ladder` just turns False), because the fallback is config.json's `harnesses.*`, whose default harness is pi-free. Deleting or emptying the ladder first would turn the only claude-code dispatcher into a pi-free stealth parent. So the order is fixed: **homes first, parity proven, readers moved, THEN retire.**
**The role rows have THREE spawners, not one** (05:0xZ, against AA2's "the 8 role rows serve only dispatch.py"): dispatch.py · heal.py (imports dispatch; old setup) · **workflow.py**, where `_resolve_pi_model` takes each pi stage's model from the ladder row for the stage's (tier, role). Workflows run by NAME from any post (skill agi-workflow), so this reader is not old-setup-only. Measured with workflow.py's own resolver: stage role kid -> stealth/space-bunny-alpha both ways · parent -> same both ways · **director -> claude-fable-5-1 with the ladder, stealth/space-bunny-alpha without: DRIFT**. So "retire the ladder together with dispatch.py" still strands workflow.py's director stages, unless workflow.py moves to the row/kid cells first. ANSWERED by AA2 (05:0xZ): workflow.py moves FIRST. A stage resolves as a kid of the invoking post (`kid-of <post>`), overridden by a per-stage `model` in the manifest, so the director-stage change Fable -> Sonnet 5.5 becomes DELIBERATE and named (owner 02:27Z 10-01, via belam: "Everyone else on sonnet 5.5 for everything they need"), not silent. The ladder retires only when dispatch.py has 0 users AND workflow.py reads 0 role rows. Falsifier AA2.25.
**The gate (all four must read 0 / equal before `ladder:ladder` is deprecated):**
```
G1 readers      AST count below over extensions/ (+ skills/ scripts)       == 0 files
G2 writers      git grep -n '"ladder:ladder"' -- extensions ':!*/tests/*' (season.py rollover)  == 0
G3 declarations git grep -n 'source *= *"ladder"' -- extensions/agi/templates  == 0
G4 parity       for every (tier, role) in the ladder AND every config:posts row a spawner reads:
                resolve_role_spec with the ladder == the spec from its new home (row / template)   byte-equal, 8/8 + rows
```
G1's counter, whole (the one used for the table above):
```python
import ast,pathlib,collections,sys
acc={'load_ladder','load_ladder_field','read_ladder_season','read_ladder_towns','read_ladder_roles','_ladder_roles_table','_ladder_global_season','ladder_path','ladder_role_row'}
uses=collections.defaultdict(collections.Counter)
for f in sorted(pathlib.Path(sys.argv[1]).rglob('*.py')):
    if '/tests/' in str(f): continue
    t=ast.parse(f.read_text()); doc=set()
    for n in ast.walk(t):
        if isinstance(n,(ast.Module,ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) and n.body and isinstance(n.body[0],ast.Expr) and isinstance(getattr(n.body[0],'value',None),ast.Constant): doc.add(id(n.body[0].value))
    for n in ast.walk(t):
        if isinstance(n,ast.Constant) and isinstance(n.value,str) and id(n) not in doc and 'ladder.md' in n.value: uses[str(f)]['path']+=1
        if isinstance(n,ast.Call):
            nm=n.func.attr if isinstance(n.func,ast.Attribute) else getattr(n.func,'id',None)
            if nm in acc: uses[str(f)][nm]+=1
for k,v in sorted(uses.items(), key=lambda x:-sum(x[1].values())): print(f"{sum(v.values()):3d} {k.replace(sys.argv[1]+'/','')}  {dict(v)}")
print('FILES', len(uses))
```
Not built: these are the falsifiers DG1 turns into the retirement's acceptance test. Today: G1 = 16, G2 = 1, G3 = 1, G4 = 5/8 drift with no home.

### AA1.T · TESTS: shell or Python, the true state (owner 14:0xZ via belam [owner] 14:01Z)
**Owner, verbatim:** "do we even need all these tests to be in Python or can the tests also be shell scripts and they could probably run a lot faster that way?"
Split, by inbox 14:0xZ (the first council round over send.py from v5 uids): alive = TRUE STATE · all-is-one = the gate side as shell checks (lanes.sh is a 13-lane shell test today) · self-perpetuating = the test as a matrix row run by the projector (agi-frontier) + the 8 KB budget.
| fact | measured 14:0xZ on trunk 1517e4b7d |
|---|---|
| tests that guard a v5 ENGINE piece (open an engine*.md and run the piece) | **6 files, 48 tests** (meter 10, boot 15, project_pi_direct 10, run_strace 3, wt_archive 8, project_agi_box 2) = **0.6% of 7,965**; the other 99.4% guard old-setup Python that retires with the old setup |
| can a v5 post run the Python suite at all? | **NO: `python3 -m pytest` -> "No module named pytest" for agi-alive**; no venv under /data/work/agi or /opt/agi. Every v5 engine test is unrunnable by the posts it guards |
| one shell twin, `agi-meter.t.sh` (2,015 B), vs its Python file (10 cases, the same assertions, the meter extracted from engine-post.md the same way) | 10/10 ok · wall **116-148 ms** (3 runs) |
| the same file through a minimal Python runner (no pytest: import + call each test with a tmp dir) | 10/10 · wall **135-138 ms** (3 runs) |
**Reading, not the hoped-for one:** per case, shell is NOT faster for a test that already runs a shell piece; both are dominated by spawning the piece (one `sh` + `jq` per case). The real wins are elsewhere: (1) no 3.2 s pytest collection for the whole suite, (2) **no pytest dependency at all**, which today makes the v5 tests unrunnable by v5 posts, (3) a twin is plain `sh`, the same language as the piece it guards. So: move the 48 v5 tests to shell twins (or matrix rows, AA2), and let the 7,917 old-setup tests retire with their code, never porting them.
The twin, whole (not committed under extensions/: no build before the bundle):
```sh
#!/bin/sh
# agi-meter.t.sh: the shell twin of test_agi_meter.py (10 cases, same assertions); prints one line per case, exit = number of fails
G=$(cd "$(dirname "$0")/../../.." && pwd)/.agi/nodes/.geometry;T=$(mktemp -d);trap 'rm -rf $T' 0;f=0
sed -n '/^### agi-meter /,/^### /{/^~~~/,/^~~~/{//!p}}' $G/engine-post.md>$T/m.sh
U(){ echo "{\"type\":\"assistant\",\"message\":{\"usage\":{\"input_tokens\":$1,\"cache_read_input_tokens\":0,\"cache_creation_input_tokens\":0}}}";}
S='{"type":"system","subtype":"bridge"}';P='{"message":{"usage":{"input_tokens":"a","cache_read_input_tokens":"b"}}}'
m(){ w=$1;h=$2;shift 2;printf '%s\n' "$@">$T/t;echo "{\"transcript_path\":\"$T/t\"$h}"|AGI_WINDOW=$w AGI_ROTATE_PCT=50 sh $T/m.sh 2>$T/e;}
ok(){ if eval "$2";then echo "ok $1";else echo "FAIL $1";f=$((f+1));fi;}
ok a  '[ "$(m 1000 "" "$(U 900)" "$S")" = "At the line (900/1000): write your card, git commit it, then run: touch ~/.fresh;kill \$PPID" ]'
ok b  '[ -z "$(m 1000 "" "$(U 100)" "$S")" ]'
ok c1 'm 1000 ",\"tokens\":900" "$(U 100)" "$S"|grep -qF "(900/1000)"'
ok c2 '[ -z "$(m 1000 ",\"tokens\":100" "$(U 900)" "$S")" ]'
ok d  '[ -z "$(m 1000 "" "$S" "{\"type\":\"user\"}" "not json")" ]'
ok e  'm 1000 "" "$(U 900)" "{\"type\":\"assistant\",\"message\":{\"content\":[{\"type\":\"text\",\"text\":\"the \\\"usage\\\" word\"}]}}" "$S"|grep -qF "(900/1000)"'
ok null 'm 1000 "" "{\"message\":{\"usage\":{\"input_tokens\":900,\"cache_read_input_tokens\":null}}}"|grep -qF "(900/1000)"'
ok nonobj 'm 1000 "" "$(U 900)" "{\"message\":{\"usage\":\"x\"}}" "{\"message\":{\"usage\":[1]}}" "{\"message\":{\"usage\":7}}" "{\"message\":\"s\"}" 5 "$S"|grep -qF "(900/1000)"'
ok stop 'm 1000 "" "$P" "$P" "$P" "$S" "$(U 900)"|grep -qF "(900/1000)"'
ok poison 'm 1000 "" "$(U 900)" "$P" "$S"|grep -qF "(900/1000)"&&[ ! -s $T/e ]'
ok strcache 'm 1800 "" "$(U 100)" "{\"message\":{\"usage\":{\"input_tokens\":900,\"cache_read_input_tokens\":\"b\",\"cache_creation_input_tokens\":5}}}"|grep -qF "(905/1800)"&&[ ! -s $T/e ]'
exit $f
```

### AA1.W · ONE-SHOT WORKFLOW SPAWNS: the manifests' true state (belam [owner] 14:54Z; owner: "we can still re-use the workflow manifests and just use spawn with workflow manifests as well as graph slices")
Split, by inbox 14:5xZ: self-perpetuating = the one-shot launch template (agi-kid + manifest-as-prompt + seeds-as-slice) · all-is-one = the graph slice now, then the skill pass + belam's config:rotations rename sub · alive = convene, the return path, and this count.
| fact | measured 14:5xZ (trunk + every post's ~/track, the agi-track strace sink) |
|---|---|
| manifests on the trunk | 30 files in extensions/agi/workflows/ (14 `.js` + 16 `.json`); `.claude/workflows/` links the 14 `.js` |
| opened by any post since its track began | **5 `.js` (brief-drafting, deep-search, l3w-route-probe, l4-plan-research, round-review) + drafting.json + review.json**, the SAME set on four thought-side posts (DG5, DT-1, DT-2, TM-new); 0 on the council, DG1-3, SM |
| never opened by any post | **23 of 30** |
| limit | a track line is a file OPEN, not a run: identical sets on four posts read like one shared listing or test, not four choices. workflow.py execve counts (all-is-one, 14:0xZ): DG5 4, DT-1 2, TM-new 1, DT-2 1 |
**Return path (alive's part), CORRECTED 14:5xZ after AA2's template:** a one-shot runs INSIDE its launcher's unit (agi-kid -m: same uid, same key, no unit, no card), so it has no identity of its own. Box mail from it would be the launcher mailing ITSELF, signed by itself, and AA1's matrix refuses a self-edge (a post is not its own parent). So **no mail on the return**: the result is a file and ref the launcher owns (§L's "its result IS refs/L/<hash>"), done = the ref exists. Mail starts only when the launcher sends the result UP its own edge, as any post does. **Cross-check with AA2's runner:** of the 5 manifests posts actually open, 2 (l3w-route-probe, l4-plan-research) are among the 4 the runner cannot run (`repeat.of = <TODO>`): fix or retire those two first, since they are the ones in use.

### AA1.F · FLOW ROTATION: the hand-off to a perpetual phase and its return (belam [owner] 17:48Z; skill = agi-spawn-chain)
**Owner 17:4xZ, verbatim (part):** "a given graph slice can be handed to a perpetual post as a flow rotation and it'd include the permissions and rails to spawn the review right after the chain growth is marked done and the post executes the next phase of its own personal flow rotation assignment. Then they can also be recursed as needed."
Split (settled 17:5xZ): self-perpetuating = the ORDER (PHI over a phase tree; a flow = a manifest whose stages are one-shot, `flow: <m>` or `post: <name>`; its runner is THE runner) · all-is-one = DONE + TRIGGER + RAILS (Z4.8: done = refs/spawn exists, or the post phase's seed goal reads MET in agi-frontier; the finisher runs agi-next; one-shots grow nothing, the invoker adopts and lands) · alive = the hand-off to a `post:` phase and its return, cross-checked on a scratch runner, plus the true state.
```
 phase i = post: P     result key r = refs/spawn/<flow>/<i>-<sha12(flow, i, ARGS, prev)>     (a hash chain: the position is DERIVED, never stored)
 OUT     box send P  'handoff <r> <prev>'     ONCE (a held marker refs/held/<owner>/handoff-<h>), then [paused] + exit 75; a re-run while paused sends nothing
 RETURN  P's mail back up the edge carries ONLY the sha its work produced: 'done <r> <sha>'
 DONE    all-is-one's rule, NOT the reply's word: P's seed goal reads met in agi-frontier at <sha> (a reply without met = still paused)
 NEXT    the chain continues THROUGH P's work: phase i+1's parent = <sha>, so the flow's history contains the post's commits
```
**Measured (scratch, 13/13; a cross-check runner of 1,363 B with a stub kid, box for the mail, the AA1 fixture rows; NOT a second runner to build):** linear 2-phase chain = 2 signed commits · a re-run with the same ARGS re-runs nothing · new ARGS = a new chain · a nested `flow:` runs inside · a `post:` phase mails the hand-off once and pauses (rc 75) · a re-run while paused mails nothing more · after P's reply the walk resumes and phase i+1 descends from P's own commit · refs/spawn shows the position (1 2 3 4) with no stored cursor · every result commit verifies (G) under the owner's signers · a failing kid commits nothing (`[failed]`, rc 1).
**Found while measuring:** the kid must receive the flow's ARGS; my cross-check runner first passed only the stage line + prev, and two ARGS gave byte-identical result commits. AA2's runner already puts ARGS in the kid's prompt (checked by self-perpetuating 17:53Z), so this was mine only. **Aligned with THE runner (AA2, 1,856 B, 17:53Z):** the RESULT ref is one per flow run, `refs/spawn/<manifest>/<sha12(ARGS)>`, written once at completion as ONE signed commit; phases and position come from the resume rule (a phase with output is done). The per-phase key sha12(flow, i, ARGS, prev) above is used ONLY for the hand-off marker of a `post:` phase.
**True state (17:4xZ):** today NO v5 post can fire a one-shot phase: 0 of 12 engine rows carry a kid model, no v5 post has an OpenRouter key in its env (only director-general-5.env exists under /var/lib/agi), pi is installed. A `post:` phase can already run (box mail, once AA1 is built). So the first live flow needs AA2's kid cell + a per-post key (the owner's root key ring) before its one-shot phases fire.
**Matrix answer for the owner (with AA2):** no new matrix. The order is PHI over a different tree, done is the growth matrix + falsifier rows, and the hand-off is the adjacency projection AA1 already checks; a flow's state is a chain of refs.

### AA1.M · MAIL WITHOUT send.py (belam [owner] 18:16Z, item M1): a message is a ref update; a box carrier cascades it; goal:g1.40's lost append cannot happen
**Owner 18:1xZ, verbatim:** "we should have a way to send messages without using send.py at all just a simple shell command to send stuff to someone else's inbox if they have permission to do so via user perms and our other clever guard combos. I don't believe it's that complicated it needs a python file, a message sent is just a git commit to the appropriate branch or nearest remote head and a local box cron takes care of cascading it down into the appropriate branch then worktree via the other location references the posts hold."
Split (settled 18:17Z, first to land): alive = M1 · self-perpetuating = K1 (per-spawn capped key) · all-is-one = K2 (spawn classes) + K3 (direct inference).
```
 SEND     box send Q <msg      sh + git + jq, no Python: ONE signed commit on refs/box/P/Q in P's own store; adjacency + squat checked; CAS update-ref, retried <= 5x
 PERMIT   user perms (P writes only its own store, AA1.R) x the parent-cell matrix (AA1's projection, at send AND read)
 CASCADE  ONE carrier per box (root; the owner's "local box cron"), reading the rows' LOCATION cells (box, store):
            Q.box == this box  -> runuser pipe: P's store refs/box/P/Q -> Q's store (AA2's agi-carry, 454 B)
            Q.box != this box  -> push refs/box/P/* to the remote head; Q's box carrier fetches it (box carry, AA1)
          woken by a path unit on each store's refs/box (PathChanged: no polling cron), plus one timer for remote fetches
 WAKE     Q's pane: agi-run's `box n` grew -> "mail: box read" (AA1, already designed)
 READ     box read: verify signer + adjacency, print, move refs/held/Q/P (only Q writes it)
```
**"then worktree" collapses:** mail lives in refs and is read by `box read`; a worktree copy would be a second store that can drift from the first. The cascade stops at Q's store.
**goal:g1.40 (the lost append), measured on scratch 18:1xZ:** send.py appends to ONE shared file per post, and a mark-read REWRITES that file, so an append in between is lost. Boxes rewrite nothing shared: each ref has one writer (out = sender, held = reader) and every move is an atomic update-ref.
| case | result |
|---|---|
| 2 senders (belam, sm) x 100 sends to alive while alive reads in a loop the whole time | **200/200 delivered**, 0 duplicates, 0 refused, each sender's order kept, 5 s |
| 2 writers on the SAME channel (two sessions of one post) x 50, no retry | 100/100 accounted: 50 delivered + 50 reported `cannot lock ref`, **0 silent** (42/8 split on a re-run: real races) |
| the same with send's 5x CAS retry (+142 B, box now 1,927 B) | **100/100 delivered**, 0 unsent, 0 stderr |
| the 25-case AA1 suite after the retry | 25/25 |
send, whole (the retry re-reads the tip; a squatted tip still stops at once, never retried):
```sh
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;b=$(cat);k=0
 until o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P@agi with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;}
  c=$(printf '%s\n' "$b"|GIT_AUTHOR_EMAIL=$P@agi GIT_COMMITTER_EMAIL=$P@agi git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o" 2>/dev/null;do k=$((k+1));[ $k -lt 5 ]||{ echo "[unsent] $r: the tip moved 5 times">&2;exit 1;};done;;
```
**Bytes:** box 1,927 B (+142 for the retry) · the carrier = AA2's agi-carry (454 B) + one rows-reading line (~200 B) + a path unit (~60 B), all expansion, 0 B in the zygote · retires send.py (317,096 B) for every v5 post.
**Not measured (needs root):** runuser between two real post uids, the path unit firing on a store write, a remote head on a second box.
**THE LEVEL RULE (owner 19:5xZ via belam [owner] 19:56Z; SUPERSEDES the figure-eight edge below, which stays as the record):** owner, verbatim: "post trees can talk within a level or to the level above ... No separate set needed just use the post tree". **Mail between a and b iff |level(a) - level(b)| <= 1**, where level = the count of NON-inert rows from the post up to `owner` (an inert group row such as council or keep adds NO level; its members carry it). Measured why: if inert rows counted, belam <-> alive and belam <-> SM would be two apart and refused. A row whose parents never reach `owner` is unplaced (level <= 0) and refused both ways; inert rows send and receive nothing; a post never mails itself. Symmetric, so one level DOWN is allowed (belam -> members, SM -> DG1), and so is any post one level up, not only the parent (DG1 -> TM-new, DG1 -> alive), per "to the level above". self-perpetuating measured the same rule independently (an awk level-ok, 373 B: 41 of 55 post pairs on belam's proposed rows).
The line, whole (replaces box's `a()` line: 328 -> 444 B, +116; the held next-sibling line was 420 B):
```sh
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def i(x):$r[x]|has("harness")|not;def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if i(x) then 0 else 1 end)+l($r[x].parent//"";n+1) end;l($a;0) as $x|l($b;0) as $y|$x>0 and $y>0 and ($r[$a]|has("harness")) and ($r[$b]|has("harness")) and $a!=$b and ($x-$y|fabs)<=1'>/dev/null;}
```
Tested on TODAY's trunk rows (4f8ff13f2): 21/21: DG1 <-> DG2 ON both ways · DG3 -> DG1 ON · DG1 -> DT-1 ON · DG1 <-> SM ON · DG1 -> TM-new ON · DG1 -> alive ON · DG1 <-> belam OFF · belam <-> alive ON · alive -> SM ON · alive -> all-is-one ON · SM -> TM-new ON · alive <-> council OFF · DG4 (no parent) <-> DG1 OFF · an unknown post OFF · alive -> alive OFF. With an inert `keep` row added (SM, TM-new under it) the same 23 cases come out identical: the keep row changes NO mail edge. AA3 note (all-is-one): agi-land hardcodes "council"; a keep row needs its ~+10 B members-cell fix, and today TM-new is landable by nobody (council lands = [sanctuary-master]).

**THE FIGURE-EIGHT EDGE (belam [decision] 19:44Z, after option (a) 87fb057c5):** measured by belam with the built filter (posts/director-general-3 engine-post.md:160), DG1 -> DG2 and DG2 -> DG3 were OFF: siblings under a NON-inert parent (SM) are not adjacent. Owner 00:4xZ: "the next post in the figure eight loop can only have access to the post branches of the post/posts placed directly before it". **Smallest rule, 0 new cells:** a -> b is also allowed when b is a's NEXT sibling in row order under the same parent (row order IS sibling order, as AA2's lap rings already use). It is ONE-WAY: `a()` is always called as a(sender, receiver), at send and at read, so DG2 -> DG1 stays off, there is no wrap (DG3 -> DG1 off), and DG1 -> DG3 (a skip) stays off. A chain of parent cells is not needed (it would break DG3 -> SM), and general sibling adjacency is not opened.
The line, whole (replaces engine-post.md's `a()` line; +92 B, box 1,927 -> 2,019 B):
```sh
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 '. as $l|map({(.name):.})|add as $r|def p(x):$r[x].parent//"";def i(x):$r[x]!=null and ($r[x]|has("harness")|not);([$l[]|select(.parent==p($a))|.name]|index($a) as $k|$k!=null and .[$k+1]==$b) or ([[$a,$b],[$b,$a]]|any(p(.[0])==.[1] or (i(p(.[0])) and (p(.[0])==p(.[1]) or p(p(.[0]))==.[1]))))'>/dev/null;}
```
Tested (scratch, the ruled tree: belam <- council (inert) <- alive, all-is-one, SM <- DG1, DG2, DG3): DG1 -> DG2 ON · DG2 -> DG3 ON · DG2 -> DG1 OFF · DG1 -> DG3 OFF · DG3 -> DG1 OFF · DG3 -> SM ON · SM -> DG2 ON · DG3 -> belam OFF (one tier, by design) · belam -> alive ON · alive -> SM ON · alive -> all-is-one ON · an unknown post either way OFF = 13/13; the 25-case box suite with the new line: 25/25. Limit: a row reorder changes the edge (the same limit as AA2's lap, honest limit 2).
**HOST ACT 1 RESULT (belam, as root, 18:27:58Z; script read whole, sha256 OK; rolled back):** rc 0 · `CARRIED hello-m1 U` · `BARRIER HOLDS`. The two-uid carry works and the 0700 barrier holds. **U, not G = the receiver does not trust the sender's key**, and the cause is measured (18:3xZ): each post's ~/.signers = the trunk's `.agi/keys/*` (3 keys: DT-1, DT-2, TM-new) + its own key from its own branch, so all-is-one's lacks alive. And the row's `pubkey` cell is NOT the git signing key: alive's row pubkey (c4934724..., raw ed25519, the seatsig key send.py signs with) != the raw 32 bytes of alive's ~/.ssh/id_ed25519.pub (591644178e...). Two keys per post, and the signers file was built from neither source of truth. **Fix (closes AA1's NEEDS (1)), REVISED 18:3xZ on self-perpetuating's objection:** NOT a row `sshkey` cell (AA2 mints a fresh key per generation, so a cell would need a config:posts write at every rotation). Instead, AA2's root-side ring: at unit start (ExecStartPre=+), root reads ~<post>/.ssh/id_ed25519.pub and appends `<post>@agi namespaces="git" valid-after=<now> <pub>` to ONE root-owned allowed_signers only when the key changed, stamping `valid-before` on that post's previous line, so old generations still verify at their own dates. `.agi/keys/` stops being a source; the row hex `pubkey` stays send.py's seatsig and retires with it. **Cross-box (alive's addition):** another box's root cannot read this box's homes, so the allowed_signers file itself TRAVELS: root's carrier ships it as a commit signed by the box's root key (the owner's "key stored on root on box", ring member 1), and a receiving box accepts it only if it verifies against the ring. Specified in AA2 'keys: Source and travel' (18:30Z): ONE file at refs/agi/ring/<box> in the commons, carried like mail, signed by the box root key; the receiver verifies it against ITS current ring and merges append-only by (principal, valid-after): lines only added, valid-before only gained, nothing deleted (falsifier AA2.46). Then act 1 re-run expects `CARRIED ... G`.
**HOST ACT 1 (belam GO pending, 18:3xZ): runuser carry between two real uids, scratch dirs only.** Run as root: `echo "90cdb304cfd265d41980eadf6b7e8552b1153e8dbe43cadfb107520b9d84a1ca  /tmp/claude-983/-var-lib-agi-alive-t/211c16c4-9ca4-4884-b506-fecf8ea999ae/scratchpad/act1/act1.sh" | sha256sum -c - && sh /tmp/claude-983/-var-lib-agi-alive-t/211c16c4-9ca4-4884-b506-fecf8ea999ae/scratchpad/act1/act1.sh /tmp/m1 runuser`. Before: /tmp/m1 absent; no live store, ref or file touched. Expect: `CARRIED hello-m1 G` (an alive-signed commit carried into all-is-one's store by the two-uid pipe) and `BARRIER HOLDS` (all-is-one cannot list alive's 0700 dir). Rollback: `rm -rf /tmp/m1`. Dry-checked as one uid (no root): CARRIED G, barrier open as expected for a single uid. The script, whole (915 B, sha256 above):
```sh
d=$1;R=${2:-runuser};A=${3:-alive};B=${4:-all-is-one}
r(){ u=$1;shift;if [ "$R" = runuser ];then runuser -u agi-$u -- env HOME=/var/lib/agi/$u "$@";else env "$@";fi;}
install -d -m 755 $d;for u in $A $B;do if [ "$R" = runuser ];then install -d -o agi-$u -g agi-$u -m 700 $d/$u;else mkdir -p $d/$u;fi;r $u git init -q --bare $d/$u/g.git;done
s=$(r $A sh -c "cd $d/$A/g.git && c=\$(echo hello-m1 | GIT_COMMITTER_EMAIL=$A@agi GIT_AUTHOR_EMAIL=$A@agi git commit-tree -S \$(git hash-object -w -t tree /dev/null)) && git update-ref refs/box/$A/$B \$c && echo \$c")
printf '%s\n' "$s" | r $A git -C $d/$A/g.git pack-objects --revs --stdout | r $B sh -c "git -C $d/$B/g.git unpack-objects -q && git -C $d/$B/g.git update-ref refs/box/$A/$B $s && git -C $d/$B/g.git log -1 --format='CARRIED %s %G?' refs/box/$A/$B"
r $B ls $d/$A >/dev/null 2>&1 && echo "BARRIER OPEN: $B reads $A" || echo "BARRIER HOLDS: $B cannot read $A"
```

**OPEN for AA2/AA3:** who owns KEYS (all-is-one proposed self-perpetuating) · AA3 land = mail up one edge, so it reuses `box read` as root (AA3 = doc:rse-aa3-land, all-is-one; principal form `<post>@agi` agreed and applied above).
**SETTLED by belam (1efd017e6, [decision] 23:51Z, superseding ec5daa28a):** members<-council; council<-belam; SM + TM-new<-council. Through this section's elimination of the inert council row, {belam, alive, all-is-one, self-perpetuating, SM, TM-new} is ONE clique (group chat and handoff down, belam's stated reason); DG1 is adjacent to SM only, DT-1 to TM-new only. So a council -> DG1 send is off-matrix under AA1 once built: the bundle went to DG1 by belam's explicit GO, over today's route.

## AA1.C CONFIG RING + ANCHOR on v5 (goal:g7.16.1.11.17 items 3+4; DESIGN ONLY, no build; alive 02:4xZ 10-03)
Asked: belam [rule] 02:34Z ("council: place (3) + (4) as design: what writes config:* and anchor edits on v5 with no write.py"). Split (accepted 02:35Z): alive = both grow-gate lines (here) · all-is-one = the land side, refusal lanes through agi-land (doc:rse-aa3-land) · self-perpetuating = WHO holds the anchor key and belam's v5 key (doc:radically-simple-engine AA2 "KEYS FOR .17 (3)+(4)"). The owner's 21:3xZ key hold stands.

**Measured on the trunk (02:3xZ):** (a) the BUILT grow-gate (config:engine-grow) checks a ring ONLY on ADDED nodes; a CHANGED node faces only the agi-fill ratchet, a deleted or retired one nothing. So on v5 any signer in the ring file can edit or retire any of the 20 `type: config` nodes, engine*.md included. (b) The RSE design's anchor line (`K=${AGI_ANCHOR:?}` ... "changes the rules, not signed by the anchor", doc:radically-simple-engine ~1676) was DROPPED from the built piece. (c) Who edits config today: since 10-01, 119 commits by belam (old setup, write.py's [config] gate: written_by [owner, prime_director] + self_row + actor_rows) and 8 by v5 posts (DG3 6, DG1 2: engine pieces, landed by SM's hand gate). A belam-only ring would refuse today's builders.

**(3) The config ring = a `ring:` cell in the node's own frontmatter, read from the RECEIVING tip R, never from the pushed version** (so a push cannot widen its own ring; changing a ring takes a signer in the OLD ring). Absent cell = open, as today. Generic: any node type may carry one. The check (381 B), run for every CHANGED or DELETED node f with signer s (the built sed already strips @agi):
```sh
g=$(git show $R:$f 2>/dev/null|awk '/^---$/{n++;next} n==1&&/^ring:/{sub(/^ring: *\[/,"");sub(/\].*/,"");gsub(/[ ,]+/," ");print;exit} n>1{exit}');[ -z "$g" ]||case " $g " in *" $s "*);;*)echo "$f: ring $g, signed by ${s:-nobody}";exit 1;;esac
```
Delta to grow-gate: `--diff-filter=AM` -> `AMD` (a retire is a D of the live path; the A under deprecated/ is already skipped); a D runs ONLY this check (no `git show $c:$f`); an M runs it, then the agi-fill ratchet as now. Tested 10/10 (scratch, R = a fixture trunk): ring member passes · non-member, unsigned, prefix `sanctuary`, suffix `belam-x` refused · open node passes · a `ring:` line in the BODY is not a ring · a node absent at R passes (ADDED nodes keep grow-check's ring).

**(4) The anchor = the RSE line restored, with `-c`** (271 B): a commit that changes `.agi/context/schemas` or `growth.tsv` verifies against a SEPARATE allowed-signers file AGI_ANCHOR, else refused.
```sh
git diff-tree -r -c --root --no-commit-id --name-only $c -- .agi/context/schemas .agi/nodes/.geometry/growth.tsv|grep -q .&&{ git -c gpg.ssh.allowedSignersFile=$K verify-commit $c 2>/dev/null||{ echo "refused: $c changes the rules, not signed by the anchor";exit 1;};};:
```
Tested 6/6 (scratch, real ssh-signed commits, K = one `anchor@agi` line): anchor-signed schema edit passes · belam-signed schema edit refused · unsigned growth.tsv edit refused · a node edit touching no rules passes · a CLEAN merge by DG1 of the anchor-signed commit passes (the commit itself is checked on its own) · an EVIL merge adding a growth.tsv line in neither parent is refused. MEASURED: without `-c` (the RSE line as designed) the evil merge passes, rc 0 = AA3.4 fix 4's blindness, again.

**Cells (owner/belam decide; alive's recommendation from the measured writers):**
| nodes | ring | why |
|---|---|---|
| posts.md | [belam, sanctuary-master] | write.py's actor_rows already grant SM the posts rows |
| engine.md engine-grow engine-post engine-root engine-wrap | [belam, sanctuary-master, director-general-1, director-general-2, director-general-3] | the builders who sign them today; the lander + agi-gate's regrow still gate |
| brief census formations guard key-authority links rotations secrets vetoes workflows | [belam] | written_by [owner, prime_director]; the owner reaches them through belam |
| the 4 config-typed build docs (doc:g716111-round5-build, -round7-build, -stage25-engine-v4c, mvp:dg3-a-one-formation-cell) | none | build records, not live cells |
Writing the cells is a config edit BEFORE the ring exists: belam, old setup, one write.py commit, then grow-gate reads them. AGI_ANCHOR's path and holder = self-perpetuating's AA2 part; agi-land passes AGI_ANCHOR to grow-gate (all-is-one's land side, +1 env).

**Lost on v5, said plainly:** write.py's ROW grants (self_row: a post edits its own seat row; actor_rows: SM only the posts-row fields) are row-scoped; a file ring is not. On v5 a ring member may edit ANY row of a ringed node. Measured cost today: none (every spawn-row commit since 10-01 is belam@local-town, old setup); OPEN for AA2: if a v5 rotation writes the post's own row, posts.md needs a row rule or root writes the row.
**AA1.C seams (02:4xZ, answering all-is-one AA3.15 + self-perpetuating AA2 "KEYS FOR .17" 64f1fff0f):**
- FRESHNESS (self-perpetuating measured: git checks a cert and a ring line's valid-before at the COMMIT's own date, so a backdated commit under an expired key reads G). Third line, per commit in the range (202 B), S = a cell (default 1 day), +300 s skew:
```sh
d=$(git log -1 --format=%ct $c);n=$(date +%s);[ $d -ge $((n-${AGI_FRESH_S:-86400})) ]&&[ $d -le $((n+300)) ]||{ echo "refused: $c dated $(date -u -d @$d +%FT%TZ), outside the freshness window";exit 1;}
```
Tested 8/8 (scratch): now, -23 h pass · -25 h, -30 d, +1 h refused · +2 min passes · S=3600: -2 h refused, -30 min passes. COST, plainly: an honest commit older than S that has not landed yet is refused too, so a merge-up must land within S or be re-signed; the backdating hole shrinks to S, it does not close. The other shape (verify only against each signer's CURRENT ring line) closes it but refuses a previous generation's unlanded commits at every rotation. The lead picks one; alive's lean = S, because rotation happens many times a day and a late land is rarer.
- RING SOURCE: self-perpetuating proposes the [config] ring = the row role (0 new cells). Measured against today's writers: role = prime_director names belam alone, and SM, DG1 and DG3 are role director, so a role-only ring refuses all 8 v5 config edits since 10-01 (DG3 6, DG1 2: engine pieces) and SM's posts-row grant. The per-node `ring:` cell above covers them; a role ring works only if the builders stop editing engine pieces or the role cell grows a value. The lead folds one.
- ONE anchor-path list for grow-gate and agi-land (all-is-one's seam): `.agi/context/schemas .agi/nodes/.geometry/growth.tsv`, written ONCE as a cell both read from R (proposal: an `anchor_paths:` cell on config:engine-grow), never as two literals.
- MERGES (all-is-one's 6m): the ring check runs in grow-gate's non-ADD branch, which the built `diff-tree -r -c` reaches for an evil merge (status MM); with `AMD` the merge statuses carrying D reach it too. NOT run on a merge by me: one lane, an evil merge by DG1 changing posts.md, closes it.
**Bytes:** grow-gate 1,465 -> ~2,330 B (+381 ring, +271 anchor, +202 freshness, +~10 filter). **Falsifiers (.17's):** a belam-signed config edit lands through agi-land with no write.py; a DG1-signed edit of posts.md is refused naming the ring; a non-anchor schema edit is refused; an anchor-signed one lands.

## AA1.K PRIVATE-KEY GATE LINE (belam [decision] 03:2xZ: its own round, a pure leak guard; RE-SCOPED by §AB.5, self-perpetuating 03:21Z: the trunk is pushed hourly to a PUBLIC origin, so it refuses EVERY private key block; a publication lives only on refs/revoked, ruled by `revoke`)
THE PATTERN (176 B as first written for grow-gate's node loop; no key parsing, so no hang and no derivation to fool):
```sh
grep -q -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' "$1"&&{ echo "refused: $1 carries a private key block (the trunk is public; a publication lives on refs/revoked)";exit 1;};:
```
Tested 12/12 (scratch, alive 03:2xZ): retired, live and unknown OpenSSH keys refused · RSA PEM, EC PEM, PKCS8 RSA, PKCS8 ed25519, ENCRYPTED PKCS8 refused · a passphrase-encrypted OpenSSH key refused (no hang) · a retired + a live key in one node refused · a node with no key, or naming a PUBLIC key / an SSH signature block, passes.
PLACEMENT CORRECTED (all-is-one 03:25Z, measured through the built agi-land, 9 lanes): in grow-gate's NODE loop (`.agi/nodes/**.md`, deprecated/ skipped) this pattern MISSES 4 that land: a key in extensions/, in a deprecated node, in a .geometry .tsv, and in a signed MERGE adding a key file in neither parent. The trunk is public, so the scope is EVERY path a commit adds or changes, binaries included: the line that ships is all-is-one's per-commit one, in GROW-GATE beside the signer read (grow-gate 1,465 -> ~1,746 B). Its bytes live in ONE place: doc:rse-aa3-land AA3.15 (all-is-one merge-up 26, landed 1c0edcf20; byte-equal to the copy alive carried here from 03:2xZ until then, now dropped). all-is-one measured 9/9 + the 17 AA3 lanes through agi-land; alive re-ran it 8/8 (non-node path, deprecated node, .tsv, binary, path with spaces, EVIL merge refused; prose + CLEAN merge pass). DG3 built it in grow-gate (45d468f83).
WHY not narrower, measured on the same fixtures: an OPENSSH-only pattern passes RSA / EC / PKCS8 blocks; any step that runs `ssh-keygen -y` on the block (alive's 03:13Z 490 B line, kept "for the refusal message" in §AB.5's first text) HANGS on a passphrase-encrypted key, so one such block stalls every land; the 490 B line also checked only the FIRST block. The 630 B per-block ring-lookup line (alive 03:2xZ, 12/12) is NOT the trunk gate; refs/revoked is ruled by self-perpetuating's `revoke` (1,384 B), which may reuse its per-block + `-P ''` shape if it parses keys.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v6, alive 14:0xZ 10-02: AA1.L marked SUPERSEDED (owner 14:0xZ: no reader moves, workflow.py retires whole) + AA1.T tests true state (0.6% guard v5, pytest absent for v5 uids, one shell twin measured equal per case). v5, alive 04:4xZ 10-02: + AA1.L, the ladder's true reader count by AST (16 files, 5 new since Z3, 4 gone) and the do-not-strand drift by dispatch's own resolver (5/8 rows); a gate of four checks, not built. v4, alive 00:4xZ 10-02: + AA1.R, the real sizes for belam's ruling 2 (per-post object stores), measured from the box's own data; the plumbing is AA2's, not redone here. v3, alive 00:2xZ 10-02 (date -u): + AA1.V versioning, on belam's [decision] 00:25Z (owner 00:3xZ/00:4xZ: every turn is a grid commit from a tiny tree). The grid commit reuses box send's primitive with a one-node tree, so mail and versioning share ONE git shape. agi-link retires because a payload can only change inside its node's tree. ~/t becomes a detached read view whose stray edits are REPORTED rather than silently committed (true state over convenience). Scratch 19/19. v2, alive 23:5xZ 10-01 (date -u): three deltas. (1) principal form `<post>@agi` (all-is-one's vote; what the unit already sets), box re-tested 25/25, 1,769 -> 1,785 B. (2) belam's council row ec5daa28a computed through the elimination: members adjacent to belam only, stated as a consequence for belam to rule on, not chosen here. (3) owner 23:4xZ skills line: AA1.S = the agi-send delta only, as a table; no skill text changes before the bundle is built. Edited with plain Edit per belam's [rule] 23:49Z (write.py is old-setup only). FIRST VERSION 23:4xZ: own node, because doc:radically-simple-engine is 268,943 B and three branches appending at its tail would conflict; scratch only; the inert-row elimination is the smallest rule that keeps a crossing one clique without a new cell.
<!-- THOUGHT:END -->
