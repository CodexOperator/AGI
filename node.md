---
id: doc:g716111-round6-build
mint_id: 684aa8a2465f416889b60e4741998152
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-3
scaffold_hash: 5f55fad00dc0c222
season: 2
tags:
  - doc
  - engine
  - round-6
  - g7.16.1.11
title: "g7.16.1.11 ROUND 6 (§T) build: the seed (1,019 B) + matrix (100 B) byte-exact, T1-T7 dry PASS, 6 holes (4 patched beside: H1 H2 H4 T7c), live needs for T6/T7"
town: core
---
# doc:g716111-round6-build

ROUND 6 = §T of goal:g7.16.1.11 (owner night plan 06:5xZ item 4; doc:radically-simple-engine §T @c3e43efc3: ONE seed script 1,019 B + ONE matrix 100 B; incl. T6 DG5 boots from the seed + T7 a Prime wake line for refs/conflicts/*). Built and dry-tested by an Opus 5.5 subagent of director-general-3 in scratch repos (two clones of one bare remote, throwaway signing keys); no root, nothing landed. DG3 checked: the doc's seed (981 B with the anchor placeholder; 1,019 B with the 82 B anchor) and matrix (100 B) are VERBATIM in §T; the patch diff below read line by line. SUPERSEDED FOR THE BUILD (alive, 08:0xZ): the council folded H1 H2 H4 T7c into doc:radically-simple-engine §T.1 @3772d6ff7 (1,023 B WITH the real anchor; H7 decided --ff-only: the seed never authors a merge, every divergence = a refs/conflicts ref for the Prime); BUILD FROM §T.1 (cd ${AGI_ROOT:-.} -> set WorkingDirectory/AGI_ROOT in the unit; ls-tree --format needs git >= 2.36; the notice carries the bare local tip); this doc stays as the record of the holes.

## T1-T7 (doc seed and patched both PASS)
T1 local first: the body (7 entries: DG5's unit, h.conf, users, path) written before any network · T2 signed fast-forward rc 0, mode rw, body re-expanded · T3 conflict: merge aborted, HEAD = local tip, refs/conflicts/<local tip> -> remote tip, 1 notice · T4a remote unreachable / T4b hangs (3 s timeout): rc 0, mode ro · T5a unsigned tip / T5b other key: rc 1, no merge · T5c replay to an older signed tip: no-op, HEAD never moves back · T6 DG5 from the seed alone = agi-project at the same commit (7/7), agi-gate rc 0 (dry) · T7 the row through agi-brief's own startup step prints ### conflicts + the ref (dry).

## Holes in the doc's bytes (each reproduced; doc kept byte-exact, patched copy beside it)
| # | doc behaviour | patched |
|---|---|---|
| H1 | re-running on the same conflict appends a 2nd [conflict] line (the notice is ';'-joined after the create-only update-ref): T7 does not fire once | update-ref ... ''&&m: 1 notice after 3 runs |
| H2 | a merge that succeeds but whose re-expansion fails makes a FALSE conflict ref + notice with HEAD already moved (merge&&x\|\|{...}) | merge\|\|{...};x HEAD: rc 2, no false conflict |
| H4 | git failing at the top leaves g empty -> writes /s at the filesystem ROOT (succeeds as root); as root in another user's checkout git refuses everything (dubious ownership): the LIKELY live case | g=$(...)\|\|exit 1 -> rc 1 |
| T7c | the bare [conflict] line lands inside the Prime's last unread message, so send.py reads it as that message's text (a signed one would read FORGED; from reading the code) | each notice its own message (ts / from: seed) |
| H5 | remote reachable but branch missing -> read-only + the first-boot greeting | named only |
| H7 | a diverged conflict-free merge with no git identity (a fresh root) fails -> a 'conflict' (fails safe) | named only; --ff-only vs a -c user.* identity = a decision to BANK |
Cost: H1+H2+H4 alone +8 B (1,027 B); the message-shaped notice takes the patched seed to 1,103 B (over 1 KiB). Also named: the offline greeting repeats each offline boot; the matrix post rows are read by nothing yet.

## What the LIVE box needs (after Phase C)
T6: a ### matrix section in config:engine (+128 B -> 16,512) + the DG5 engine cell (non-root, write.py) · the trunk tip SIGNED by the anchor (S7), K = the master's/owner's allowed_signers line (else every sync rc 1) · the seed run once as ROOT + systemd-sysusers + daemon-reload + start (the doc seed makes 0 systemctl calls; matrix.patched.tsv adds an up row, +140 B piece) -- root needs git config --global --add safe.directory <repo> or H4 bites; UNDO: stop the unit, remove the agi files under /run/systemd/system, daemon-reload, userdel agi-director-general-5, rm <repo>/.git/s, git config --unset agi.mode · T7: ONE first_turn row under prime_director in config:rotations (git -C {repo} for-each-ref refs/conflicts/), write.py, undo = remove the row; needs the message-shaped notice.

§Q seam: built against v4c; the seed calls each boot piece as sh -s OUT REV; matrix row 2 names ### agi-project; ### matrix must sit in ONE .geometry/engine* file; if §Q splits the engine, agi-project's own read must still find its pieces.

## Bytes (the doc versions live in doc:radically-simple-engine §T; the patched copies here)

### seed.patched.doc.sh (placeholder anchor line) (1065 B, sha256 49b40c6cea0f8164)
~~~~~sh
#!/bin/sh
# agi seed [REMOTE] [S]
K='<the anchor: ONE allowed_signers line, 82 B>'
cd ${AGI_ROOT:-/data/work/agi}||exit 1;b=$(git symbolic-ref --short HEAD);g=$(git rev-parse --git-dir)||exit 1;i=.agi/sessions/inbox/belam.md;mkdir -p ${i%/*}
m(){ printf -- "---\nts: %s\nfrom: seed\nto: belam\n\n%s\n" $(date -u +%FT%TZ) "$*">>$i;}
e(){ git ls-tree --name-only $1 .agi/nodes/.geometry/|grep /engine|sed "s/^/$1:/"|git cat-file --batch --follow-symlinks|sed -n "/^### $2 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
x(){ e $1 matrix|awk '$1=="boot"&&$4!="sect"{print $4}'|while read v;do e $1 $v|sh -s ${AGI_OUT:-/run/systemd/system} $1;done;};x HEAD;echo "$K">$g/s
if timeout ${2:-60} git -c transfer.fsckObjects=1 fetch -q ${1:-origin} $b;then git -c gpg.ssh.allowedSignersFile=$g/s verify-commit FETCH_HEAD||exit 1
git config agi.mode rw;h=$(git rev-parse HEAD);git merge -q FETCH_HEAD||{ git merge --abort;git update-ref refs/conflicts/$h FETCH_HEAD ''&&m "[conflict] refs/conflicts/$h";};x HEAD
else git config agi.mode ro;m "[owner] first boot, local read-only. Hello.";fi
~~~~~

### matrix.patched.tsv (118 B, sha256 27e7104f4975be6b)
~~~~~
boot	matrix	engine	sect
boot	body	posts	agi-project
boot	up	engine	up
post	bin	engine*	sect
post	brief	card-<p>	brief
~~~~~

### t7-wake-row.txt (161 B, sha256 3abfcc60f6f843e4)
~~~~~
        - {"label": "conflicts", "cmd": "git -C {repo} for-each-ref refs/conflicts/", "why": "goal:g7.16.1.11 T7: a seed sync left these; resolve or bank each"}
~~~~~

### ### up piece (from src/engine.up.md) (165 B, sha256 5191eac112d77a25)
~~~~~markdown
### up (140 B)
~~~sh
#!/bin/sh
systemd-sysusers $1/agi-users.conf&&systemctl daemon-reload&&cd $1/multi-user.target.wants&&systemctl start --no-block agi-post@*
~~~
~~~~~
