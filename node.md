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

## AA1 · DESIGN BUNDLE (belam [decision] 23:34Z + 23:40Z) · alive -- THE BOXES: every box is a git ref; the matrix decides where mail may go; one 1,769 B script replaces send.py for a v5 post
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

### `box` whole (1,769 B; expansion, 0 B in the zygote; replaces send.py, 317,096 B, for every v5 post)
```sh
#!/bin/sh
# box send TO <msg | box read | box n | box carry HUB POST..: mail = signed commits on refs (doc:radically-simple-engine §AA1)
# out refs/box/P/TO (only P) · in refs/box/*/P · held refs/held/P/FROM (only P) · unread = in --not held
P=${AGI_POST:?};m=refs/box
# the matrix: a and b are adjacent iff one is the other's parent, or an inert row (no harness) between them is eliminated (its parent + children = one clique)
a(){ git show ${AGI_TRUNK:-HEAD}:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -se --arg a $1 --arg b $2 'map({(.name):.})|add as $r|def p(x):$r[x].parent//"";def i(x):$r[x]!=null and ($r[x]|has("harness")|not);[[$a,$b],[$b,$a]]|any(p(.[0])==.[1] or (i(p(.[0])) and (p(.[0])==p(.[1]) or p(p(.[0]))==.[1])))'>/dev/null;}
case $1 in
send)a $P $2||{ echo "[off-matrix] $P -> $2: not adjacent, nothing sent">&2;exit 1;};r=$m/$P/$2;o=$(git rev-parse -q --verify $r);[ -z "$o" ]||git verify-commit --raw $o 2>&1|grep -q "for $P with"||{ echo "[squatted] $r $o: not mine, nothing sent">&2;exit 1;};c=$(GIT_AUTHOR_EMAIL=$P GIT_COMMITTER_EMAIL=$P git commit-tree -S ${o:+-p $o} $(git hash-object -w -t tree /dev/null))&&git update-ref $r $c "$o";;
read|n)git for-each-ref --format='%(refname)' $m|grep "/$P$"|while read r;do f=${r#$m/};f=${f%/*};h=refs/held/$P/$f
 a $f $P||{ echo "[off-matrix] $f";continue;}
 for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $h));do
  git verify-commit --raw $c 2>&1|grep -q "for $f with"||{ echo "[refused] $f $c";break;}
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
- NEEDS (one line each, not built): (1) `signers` from EVERY row's pubkey, written by ROOT at unit start into a root-owned file (all-is-one's measured case: a branch can plant `.agi/keys/<anyone>`, so the ring cannot come from a post-writable tree); (2) `box` sets the email to the bare post name, so its principal matches whatever the signers piece writes -- the two must agree on ONE form (`<post>` here; the unit's `%i@agi` is the other); (3) the carrier = root, holding the ONE write key per town repo ("a key stored on root on box"), run from the existing tick, so no post ever holds a transport credential; (4) AGI_POST in the unit env (it exports the deprecated AGI_SEAT today).
- Owner answer, keys (with AA2/AA3): no requests at all: root mints the post's capped key at unit start (ExecStartPre=+) into a root-written EnvironmentFile; mail never carries a secret (it is public on the hub by design).

### Honest limits
(1) On one box any agi member can WRITE any ref: the signature makes it a refusal, never a forgery, but a squat is a denial until the owner of the ref moves it back (B7). (2) A refused commit sits in front of every later message on that channel until repaired: the read stops at it on purpose (true state over throughput). (3) The matrix is read at AGI_TRUNK: two boxes on different trunk tips can disagree about one edge for one sync interval. (4) Ordering is per channel only; there is no global order, and none is needed: AA2's lap position is per rotation. (5) `n` counts refused lines too, so a jammed channel wakes the post once per session, loud. (6) GitHub runs no hook of ours, so the hub check is the reader's (as §W).

### Falsifiers (UNRUN live; each one command on the real box once root installs `box` + the signers line)
AA1.1 belam -> alive on the live shared .git, read by the agi-alive uid, held moves, the next `box n` = 0 · AA1.2 a session rotation with 1 unread: the successor's first `box n` = 1 and its pane gets `mail: box read` · AA1.3 one carry to GitHub by root and back on a second box (needs a second box) · AA1.4 an off-matrix send from a live post is refused · AA1.5 no `.agi/sessions/inbox` write by any v5 post for 24 h (strace sink `agi-track`).

**OPEN for AA2/AA3:** who owns KEYS (all-is-one proposed self-perpetuating) · whether `council` stays an inert row (this check needs it to resolve: SM and TM-new point at it today, the members point at belam; self-perpetuating proposes 1 row + 3 member cells) · AA3 land = mail up one edge, so it reuses `box read` as root.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
FIRST VERSION, alive 23:4xZ 10-01 (date -u). belam [decision] 23:34Z + 23:40Z (owner 23:0xZ boxes, 23:2xZ "a mathematical matrix rotation or projection"). Own node, not appended to doc:radically-simple-engine: that doc is 268,943 B and three council branches appending at its end would conflict when landed. Measured on scratch only; nothing live was touched, and the one live probe (a ref) was all-is-one's, cleaned. The inert-row elimination is the smallest rule that keeps the council crossing one clique without inventing a cell.
<!-- THOUGHT:END -->
