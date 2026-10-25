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
2. The census of existing wrapped shares prints `opened k/m` with k == m > 0 after the switch; m = 0 or an unreadable share prints `unread`, rc 1.
3. Negative: `grep -c -E 'python3|cryptography|X25519' ` over the installed agi-out piece (the repo bytes in .geometry, and the installed set's sha256 matching them) prints 0.

## Out of scope
goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
