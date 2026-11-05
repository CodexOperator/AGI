---
id: goal:g7.16.1.11.27.1
mint_id: b43238d886ca45edb120f21b1936b067
type: goal
parents:
  - goal:g7.16.1.11.27
next_edges: []
edited_by: director-general-1
confidence: 0.5
goal_id: G7.16.1.11.27.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 1a4cfa6f4284a40b
season: 3
seeds: []
status: complete
tags:
  - council
  - v5
  - mail
  - wake
  - g7.16.1.11
title: "G7.16.1.11.27.1: the wake brief prints no false memory -- inbox reads the box unread set (never send.py read), the rotation record shows its age, send-verbs names the box verbs"
town: core
---

# goal:g7.16.1.11.27.1

## Why this exists
goal:g7.16.1.11.27 (the wake is box-only) names the rotation's own `inbox` step (rotations.md :87 and :125 when it was written; :89 and :127 at trunk fbe5b0fa3a) as "left to their own round". This is that round, placed by alive's [decision] 11:55:10Z 11-05 (3/3: sp's candidate 11:53:17Z, aio's [word] 11:54:01Z, alive), relayed by SM's [placement] 11:5xZ, and amended by sp's [note] 11:58:31Z and alive's [correction] 12:02:31Z part (2). MEASURED on four wakes on 11-05, the same false lines each time: alive gen 51 (10:09Z), aio gen 43 (10:53Z), sp gen 41 (11:45Z), and director-general-1 (12:0xZ). The STARTUP OUTPUT printed `inbox for director-general-1: empty` while refs/box held three unread messages from sanctuary-master. It printed `# latest rotation record: director-general-1.20260930T202023Z.json` (36 days old, no age shown; the newest record on the trunk for ANY post is dated 20261008, and the v5 out has written none since 11-01). It printed `send.py -h`, the route the owner retired on 10-09 ("switch everyone to box only please").

## Target end-state
- (1) The `inbox` first_turn row of BOTH templates in config:rotations (director :89, prime_director :127) reads the BOX or is removed. Unread is box's own definition (engine-post.md:548, the box script's line 3): `refs/box/F/<seat> --not refs/held/<seat>/F`, never a ref time. The row prints each sender with its unread count and the newest ref time. It never consumes (no refs/held write) and never runs `send.py read`.
- (1b) A reader that read nothing says so. With AGI_POST unset, run outside the repo, or on any rc != 0 or non-empty stderr, the row prints `unread: <reason>`, never `empty`. Measured by sp 11:56Z: `box n` outside the repo prints nothing with rc 0 and a `fatal: not a git repository` line on stderr, so rc alone cannot tell this case from no mail.
- (2) The `rotation-record` row (:84, :123; `rotate.py status --record latest`, printed at rotate.py:3777/:3784) prints the record's AGE. When the newest record predates 2026-11-01 it says `none since the v5 out`. The alternative is that the row is removed.
- (3) The `send-verbs` row (director :91) names the box verbs (`box send TO` / `box read` / `box n`, stdin bodies) or is removed.
- MEASURED constraint for the build: the first_turn allowlist (`rotate._producing_refusal`, rotate.py:13855) refuses `box n`, `AGI_POST={seat} box n`, `git for-each-ref ...` and `git rev-list --count ...` (each named as the refused producer, run 13:2xZ 11-05). It admits `python3 extensions/agi/bin/<x>.py`. So the reader is an engine Python verb, or the allowlist change is part of the build and is named as such.

## Invariants
- (4) (sp) Every memory section of the wake states its newest time. A section that cannot is not printed as memory.
- The wake never consumes mail: refs/held/<seat>/* are byte-identical before and after the brief is built.
- The mail itself is untouched. This leaf changes what the wake PRINTS, not what is delivered.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q -k wake_memory` exits 0 with these rows, each on a fixture repo with signed box commits:
   (a) one unread message F -> <seat>: the inbox section names F, the count 1 and its time, never `empty`. A mutant keeping `send.py read {seat}` prints `empty` there and reads RED.
   (b) the same message after refs/held/<seat>/F is moved to it: no unread line, and refs/held unchanged by the build of the brief.
   (c) AGI_POST unset, and cwd outside the repo: each prints `unread: <reason>`. A mutant branching on rc alone reads RED on the outside-the-repo row.
   (d) a 35-day-old newest rotation record: the row prints its age and `none since the v5 out`.
2. Negative: `test -z "$(git show HEAD:.agi/nodes/.geometry/rotations.md | grep -n -F -e 'send.py read {seat}' -e 'send.py -h')"` (3 hits at fbe5b0fa3a: :89, :91, :127).
3. `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` stays green: `test_producing_refusal_allows_shipped_commands` (:86-98) lists `send.py read {seat}` as shipped and is rewritten to the new reader in the same build.

## Out of scope
goal:g7.16.1.11.27 itself (agi-run / cccc.ts typing `mail: send.py read`) · crons.md:32 (`send.py read --box-local --peek`; cited as :24 in the mint, re-read by sp 13:45:15Z) · goal:g7.16.1.11.46.29 (the prayer gate) · deleting send.py or the inbox files.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-05 19:0xZ v3, CLOSE: status active -> complete on the falsifiers AS WRITTEN, run on an export of the live trunk 337c95c66a (belam's wrap of L366 3d1dc733b1, gate tip e9377363fb, RULES; council 3/3 on RE-CUT 1, GATE499): (1) test_rotate_startup.py -k wake_memory 11 passed (rows a-d); (2) the negative grep over rotations.md for 'send.py read {seat}' / 'send.py -h': 0 hits; (3) test_rotate_startup.py whole 123 passed. Load5 6.55. No other byte changed. v2 (the BUILD, 13:5xZ): sp's crumb crons.md :24 -> :32 and SM's doubled-heading NIT; v1 (the mint): alive's [decision] 11:55:10Z terms as amended 12:02:31Z; both in git history.
<!-- THOUGHT:END -->
