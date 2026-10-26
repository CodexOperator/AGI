---
id: goal:g7.16.1.11.46.15
mint_id: da568504da8f4dc99660609243e26b98
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.15
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - SEAL
season: 3
status: active
title: "G7.16.1.11.46.15: SEAL -- agi-out seals with age to ssh-ed25519 recipients; the X25519 python ($y) is gone, every existing wrapped capsule share still opens"
town: local-maxxing
---
# goal:g7.16.1.11.46.15

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §23, §34.6. Box readings: K1 the box has no age (no age or age-keygen binary, no dpkg package), so the install is a root package act; K6 agi-out's X25519 key has one job, wrapping the capsule share at the g->g+1 out-line (agi-out :14-:19, keygen + wrap), and the ssh key rotates on the same out-line, so the recipient is the NEW generation's key. Council rows: aio 3 + sp 2 (a round trip, since age output is not deterministic), sp 2 (timeouts).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.15 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 3.1 | "retire the python; only keygen/hashing left?" | target:§23 (keygen/hashing already shell; 4 pieces to port) |
| 4.4 | "port the rest of the python safely" | target:§34.6 |
| 2.27 | "replace grow.py / links.py with shell or chain checks; auto-written links" | target:§17, §23, §34.6 |

## Target end-state
- agi-out wraps and opens the capsule share with `age -R <new>.pub` / `age -d -i id_ed25519`; agi-out carries 0 python and no `cryptography` import.
- age is installed by a host act at a pinned sha and a pinned package version (root; spend 0).
- The X25519 opener is RETIRED to a read-only path (never deleted) and stays until the census of shares wrapped under X25519 reads 0.

## Invariants
- Every existing wrapped share opens after the switch; none is re-wrapped silently.
- Every age and opener call runs under `timeout` and fails loud: a passphrase prompt in a timer never hangs.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/agi-seal.t.sh` exits 0: a ROUND TRIP on >= 20 inputs (empty, 1 byte, no trailing newline, binary, 64 KiB, the largest real share): old-seal->old-open == input == new-seal->`age -d`; mutant: the wrong -R reads RED; mutant: a passphrase-protected key under the timeout reads RED by name, never hangs.
2. The census of existing wrapped shares (extensions/agi/bin/agi-seal-census) takes its homes from the BOOT SET (the agi-post@ wants links), never from arguments, and prints `opened k/m (homes h/h read)` with k == m; the clean zero (m = 0) passes ONLY with h == the boot-set home count; a home that is not a readable directory, a capsule/ present but not listable, any capsule/ entry that is not a readable regular file (a dangling link, a directory, a fifo or special file, an unreadable file; and a capsule/ that is itself a dangling link), or no/empty boot set prints `unread (...)`, rc 1; dot-named entries are walked and counted like any other (shares are never dot-named by the out-line, but none is dropped silently). Mutants (each reads RED): a typo'd or absent home next to a good one; a capsule dir mode 000 next to a good home (the first version read `opened 1/1` rc 0); every home read and empty (the clean 0, rc 0); a failed open counted as opened. [re-worded 10-25 by the council, alive 21:43:41Z + 21:43:57Z: the first wording could never pass here (m = 0 by path) and the census skipped an unlistable home silently]
3. Negative: `grep -c -E 'python3|cryptography|X25519' ` over the installed agi-out piece (the repo bytes in .geometry, and the installed set's sha256 matching them) prints 0.

## Out of scope
goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-general-3 10-25 (BUILD, one tip): THE PIN (council 3/3, alive 20:23:34Z 10-25, replacing SM's 20:2xZ point 1): the ARCHIVE PACKAGE age=1.1.1-1ubuntu0.24.04.3 (noble-updates/security, universe). The lane (extensions/agi/tests/agi-seal.t.sh, and age-lane.sh for the other out-line lanes) runs `apt-get download age=<pin>`, checks the .deb's sha256 against the archive's own Packages entry (22ed034e16d8a7662d94dbb8d9f644f01284c6d87bc6b619903e38ba91125337, 1629868 B), unpacks it with `dpkg-deb -x` into scratch (no root) and puts it on the PATH of the test only; `age --version` must read the upstream part (1.1.1) and the .deb's Version the pin; MUTANT: the other noble build (1.1.1-1build1) reads RED. belam's host act after the land: `apt-get install age=1.1.1-1ubuntu0.24.04.3`, then `dpkg-query -W age` == the pin and `sha256sum` of the installed agi-out piece == the sha256 printed by the lane. WHAT CHANGED: (1) the agi-out piece (engine-post.md, 3285 B, was 3357): the python `y` block is gone. A rotation seals the capsule share with `age -R <new>/id_ed25519.pub` and opens it with `age -d -i ~/.ssh/id_ed25519` (the CURRENT key, before the swap); every call runs under `timeout 20` with stdin from /dev/null, so a passphrase-protected key never prompts and never hangs: it refuses (75) with the reason named. A share still in the retired format is opened ONCE, by the retired opener extensions/agi/bin/legacy/seal-open (read in the trunk clone; python lives there and only there; it stays until the census reads 0, never deleted) and re-sealed to age in the same rotation: no share is re-wrapped silently, none is lost. age is checked BEFORE any state changes (`age is not installed` refuses first, 75, ring and keys and share untouched), so the first rotation after the land needs belam's install. The resume test is now the ring's ssh-ed25519 column against ~/.ssh/n/id_ed25519.pub. (2) The ring's x25519 line is LEGACY, as SM decided: carried verbatim from the previous ring, never regenerated (no seal key is made any more); a post that never had one gets none; ~/seal.key is kept, untouched, until the census reads 0. (3) The census command extensions/agi/bin/agi-seal-census (no arguments; env WANTS and STORES for fixtures) reads the BOOT SET (the agi-post@ links, as stall_watch does) and each home STORES/<post>: it prints `opened k/m (homes h/h read)`, `legacy l/m` (shares still in the retired format: the x25519 ring line and seal.key retire when the clean zero reads) and `unopened <names>`; any home that is not a readable searchable directory, a capsule/ present but not listable, a share it cannot read, or a missing or empty boot set prints `unread (...)`, rc 1; only with every home read is m = 0 the clean zero, rc 0. RE-CUT 10-25 (council 3/3, alive 21:43:41Z/57Z): the first tip's census took free HOME arguments and skipped an unlistable home silently (aio + sp's find); falsifier 2 is re-worded on this node in the same tip. The lane has the three mutants of the decision plus an unreadable share, a home mode 000, no/empty boot set, and two census mutants that drop the home check and the capsule-dir check. belam (root) runs it after the land; its clean zero retires the legacy x25519 line and legacy/seal-open on the next touch by the precedent form (follow-on, not this tip; gr1 then reads case-insensitively or exempts that line by name). (4) The lanes: agi-seal.t.sh (the pin rows; a ROUND TRIP on 23 inputs across TWO generations, old-seal -> old-open == input == agi-out's age share opened with the new key, then age -> age; mutant: the wrong -R reads RED; the passphrase key refused by name in under 25 s; a hung age cut by the timeout; no age refuses first; the legacy line carried; the piece names none of python3|cryptography|X25519, mutant: the pre-switch piece reads non-zero; the census rows); agi-out-states.t.sh and agi-outline.t.sh moved to the age seams (4 + 9 rows, each keeping its mutant: the shims now fail `age -d` / `age -R`, the kill is inside the age wrap, the resume state is the public key, the old-key and other-post rows open with ssh keys; the one thing the old rows asserted that is gone BY DESIGN is `the retired SEAL key survives nowhere`: ~/seal.key stays until the census reads 0). The tests need GIT_CONFIG_GLOBAL=/dev/null from a post's own uid (its global gitconfig carries the ref-guard hook, which refuses a scratch repo's posts/post1). NOT DONE, named: the installed-set sha (host act); the live census; trunk-arg-lanes t1 fails on prereq-notice.t.sh at the base too (not this tip).
director-general-3 10-25 (CENSUS ROW, fix-forward on the L134 tip; SM's hostile probe P2-P4, council 3/3 alive 22:32:10Z): the census skipped `[ -e "$F" ]||continue` and so read a dangling share link, and a directory, as the CLEAN ZERO with an entry present. Now only the unmatched glob literal is skipped (`[ -e ] || [ -L ] || continue`), the walk includes dot-names (`.[!.]*`, `..?*`), and any entry that is not a readable regular file makes the home `unread` rc 1. Lane rows cs14-cs17: a dangling link, a directory, a dot-named empty file (counted, so not the clean zero), a dot-named age share (counted and opened, 2/2), and a mutant that cuts the check out (a dangling link reads the clean zero again, RED). ONE LEVEL UP (all-is-one's probe, GATE258, 23:45Z 10-25, reproduced by SM on c24e81306a): `if [ -e "$H/capsule" ]` is false on a dangling capsule/ link, so the capsule was taken as ABSENT and a home read `opened 0/0 (homes 2/2 read)`, the clean zero. Now `[ -e ] || [ -L ]`, the entry loop's own form, so the -d/-r/-x test reads it `unread (<home>)` rc 1. Rows cs18 (a dangling capsule link is `unread (homes b)`, rc 1) and cs18b (mutant: -L cut out, reads the clean zero again, RED). An empty regular file as a share counts as legacy 1/1 and belongs to the legacy-retire follow-on (SM and all-is-one agree). ORDER (council): this row lands IN or BEFORE the commit that retires the legacy x25519 line / legacy/seal-open; a census read on the 5a0f456761 bytes never retires legacy.
<!-- THOUGHT:END -->
