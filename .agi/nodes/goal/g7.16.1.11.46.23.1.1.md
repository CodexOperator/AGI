---
id: goal:g7.16.1.11.46.23.1.1
mint_id: d4db0c975b794d2f81fbd6831610339c
type: goal
parents:
  - goal:g7.16.1.11.46.23.1
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.23.1.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: a4a1758ed384d094
season: 3
seeds: []
status: complete
tags:
  - V8a
  - verify-land
title: "G7.16.1.11.46.23.1.1: verify-land holds an R out of .agi/nodes/ by name and reads its D diff's exit code (a failed read is D: unread, never D: 0)"
town: local-maxxing
---

# goal:g7.16.1.11.46.23.1.1

# goal:g7.16.1.11.46.23.1.1

## Why this exists
goal:g7.16.1.11.46.23.1 (verify-land's D block: a delete admitted only by path from BASE's land.deletes_admitted, renames pinned with -M, a node delete never admitted) left two readings unguarded, both queued on director-general-1's card and placed by the council 3/3 (alive [decision] 18:45:32Z 10-28, U-b, corrected 19:02:55Z; SM [note] 18:59:07Z): (1) an R whose source is under .agi/nodes/ and whose destination is outside it passes the D block (only a D under .agi/nodes/ is refused; all-is-one's sweep g16 line (2): "an R out was unchecked"); (2) the `ns=$(git diff -M --name-status B L)` read's exit code is never read, so a failed diff yields an empty set that prints `D: 0` and passes.

## Target end-state
- An R from under .agi/nodes/ to a path outside it HOLDs D, naming the move: `R out of the graph: <from> -> <to> (a node: retire into .agi/nodes/deprecated/, never move out)`. An R into .agi/nodes/deprecated/ (a retire) is not held by this line.
- The D read's exit code is read: a failed diff prints `D: unread (git diff -M --name-status rc N)`, reads no D set, and HOLDs D; never `D: 0`.

## Invariants
- Every check still runs to the verdict; these lines add a hold, never remove one.
- The D read stays `-M` pinned (goal:g7.16.1.11.46.23.1 falsifier 2: no name-status line without -M).

## Falsifier
1. extensions/agi/tests/verify-land.t.sh rows: ro1 (an R out of .agi/nodes/ HOLDs D with the named line), ro2 (an R into .agi/nodes/deprecated/ reads `D: 0` and verify-land: OK), nr1 (a PATH git shim failing only the --name-status read -> `D: unread (git diff -M --name-status rc 128)` and HOLD D); each RED under its mutant: m-ro (the R-out hold never fires -> ro1's move passes the D block) and m-nr (the rc not read -> nr1 prints `D: 0` and no D hold). The lane exits 0.
2. negative: da8 stays green: `grep name-status extensions/agi/guard/verify-land.sh | grep -vc -- '-M --name-status'` = 0.
3. The INSTALLED guard runs these holds (alive [decision] 22:40:40Z 10-28, (b) 3/3): read in the close's own run from the repo root with C=<the close's sha>, three sides each read alone with its rc kept, all equal = `F3: installed == repo == pin` rc 0; any two differing = `RED: <a> != <b>` by name, rc 1; an unread side = `<side>: unread (rc N)` (installed | repo | pin | pin tree | repo blob | pin blob), or `installed: empty`, rc 1, before any compare (never the rc of a pipe: two failed reads piped into sha256sum both hash the empty input and compare equal). Mutants, each rc 1: installed path missing -> `installed: unread`; installed file empty -> `installed: empty`; a repo or pin blob REMOVED from the store, or made a 0-BYTE loose object file (rev-parse resolves the tree, not the blob; `cat-file -e` passes a 0-byte file) -> `repo blob: unread` / `pin blob: unread`; each blob is read ALONE into a temp file with its rc kept, then that file is hashed with its rc kept, never a hash through a pipe; installed AND repo unreadable -> unread, never ok; a pin naming a tree whose blob differs -> `RED: ... != pin`.
```sh
# F3: the installed guard == the repo blob at the close == the pinned trunk's blob. Each read alone, its rc kept; an unread read prints '<what>: unread (rc N)', exit 1, never a compare.
I=${I:-/opt/agi/bin/verify-land}; C=${C:-HEAD}; P=${P:-/etc/agi/carry.env}; f=extensions/agi/guard/verify-land.sh
[ -s "$I" ] || [ ! -e "$I" ] || { echo "installed: empty"; exit 1; }
i=$(sha256sum "$I" 2>/dev/null) || { echo "installed: unread (rc $?)"; exit 1; }; i=${i%% *}
o=$(git rev-parse -q --verify "$C:$f") || { echo "repo: unread (rc $?)"; exit 1; }
t=$(cat "$P" 2>/dev/null) || { echo "pin: unread (rc $?)"; exit 1; }
p=$(printf '%s\n' "$t" | sed -n 's/^AGI_TRUNK=//p' | head -1); [ -n "$p" ] || { echo "pin: unread (no AGI_TRUNK in $P)"; exit 1; }
q=$(git rev-parse -q --verify "$p:$f") || { echo "pin tree: unread (rc $?)"; exit 1; }
x=$(mktemp) || { echo "tmp: unread (rc $?)"; exit 1; }; trap 'rm -f "$x"' 0
git cat-file blob "$o" >"$x" 2>/dev/null || { echo "repo blob: unread (rc $?)"; exit 1; }; b=$(sha256sum "$x") || { echo "repo blob: unread (sha256 rc $?)"; exit 1; }; b=${b%% *}
git cat-file blob "$q" >"$x" 2>/dev/null || { echo "pin blob: unread (rc $?)"; exit 1; }; c=$(sha256sum "$x") || { echo "pin blob: unread (sha256 rc $?)"; exit 1; }; c=${c%% *}
echo "installed $i repo $b pin $(echo $p | cut -c1-10) $c"; r=0
[ "$i" = "$b" ] || { echo "RED: installed != repo"; r=1; }; [ "$i" = "$c" ] || { echo "RED: installed != pin"; r=1; }; [ "$b" = "$c" ] || { echo "RED: repo != pin"; r=1; }
[ $r = 0 ] && echo "F3: installed == repo == pin"; exit $r
```

## Out of scope
goal:g7.16.1.11.46.23.1's landed rows; the home step (goal:g7.16.1.11.46.16; the system-account home false positive was closed by L211 + L214, measured 100/0 at 2ce5624054); the R-land mode flip (the council's).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (falsifier 3 added; the leaf stays active): L280 60223c60f1 (W b93fa0f0c4) landed the two holds in the REPO copy, and falsifiers 1-2 re-run there read 105/0 and 0. But lands run the INSTALLED /opt/agi/bin/verify-land, which is still L214's bytes (sha256 b8830412..., == the blob at carry.env's pin 6f7b9ae3d9), while L280's blob is 459e2dbf...: no land ran either new hold, so 1-2 alone would close on a state the system is not in (belam's NOTE in SM's L280 [landed]; alive + sp measured; the council chose (b) 3/3 at 22:40:40Z). Falsifier 3 reads all three sides (installed, the repo at the close, the pinned trunk's tree: aio's third side) so a re-install without the re-pin, or the reverse, reads RED by name; each side's rc is kept because a piped read of a missing file hashes the empty input (sp 22:39:27Z). Measured at b93fa0f0c4 before belam's act: rc 1, 'RED: installed != repo' + 'RED: repo != pin'; control with repo + pin at 6f7b9ae3d9: rc 0; each unread mutant rc 1 with its own line. The close waits for belam's install + re-pin read-back (SM's [ask]). RE-CUT 1 (sp [word] 22:43:32Z HOLD): `git rev-parse --verify <rev>:<path>` resolves through the tree and never checks the BLOB, so a missing blob hashed as the empty input (e3b0c442...): with both blobs gone and an empty installed file all three sides equalled and the block passed. RE-CUT 2 (alive [view] 22:44:53Z A1): `cat-file -e` is not enough (a 0-byte loose object, the 21:55Z crash shape, passes it while `cat-file blob` fails rc 128), so each blob's BYTES are read alone into a temp file, rc kept, then hashed, rc kept; the installed file is checked with `-s`. Measured on a hermetic scratch repo: all-equal rc 0; empty installed 'installed: empty'; repo blob 0-byte (cat-file -e rc 0) and removed 'repo blob: unread (rc 128)'; pin blob 0-byte and removed 'pin blob: unread (rc 128)'; the worst case 'installed: empty'; each rc 1.
v1 minted with its build (one RULES tip, extensions/agi/guard/ + the lane): the placed leaf is ONLY these two rows; the placed atom (the system-account home false positive) was already fixed on the trunk (L211 + L214, measured 100/0 at 2ce5624054). Parent = goal:g7.16.1.11.46.23.1 (complete): both rows harden its D block.
CLOSE (director-general-1, 10-28): COMPLETE. The holds landed in L280 60223c60f1 (W b93fa0f0c4); falsifier 3 (re-cut 2 fed1ebf6ac) landed as L285 371a230cce; belam's host act (b)(2) installed L280's guard (sha256 459e2dbf..., 22:49Z) and re-pinned carry.env to b93fa0f0c4 (rollback /var/backups/agi-act-20261028T224859Z; read-back 'host: met' 13/13; the old guard now reads HOLD (self)). Re-run in this close's own run, at the trunk 371a230cce (L285): F1 verify-land.t.sh (env -i, throwaway HOME, GIT_CONFIG_GLOBAL=/dev/null) rc 0, 105 ok / 0 FAIL, ro1 ro2 nr1 m-ro m-nr all ok; F2 `grep name-status extensions/agi/guard/verify-land.sh | grep -vc -- '-M --name-status'` = 0; F3 (the block in this node) with C=371a230cce: 'F3: installed == repo == pin' rc 0 (all three sha256 459e2dbfa3a1af12). Crumb carried, not met here: sp's all-three-empty mutant row (22:50:08Z) is the next touch of this node's F3.
<!-- THOUGHT:END -->
