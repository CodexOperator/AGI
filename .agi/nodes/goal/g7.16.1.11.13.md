---
id: goal:g7.16.1.11.13
mint_id: 0d5e0a34405d4ec0aab3c608edee9433
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.13
goal_kind: subgoal
origin: goal
scaffold_hash: c6b17011fb0f9e1d
season: 2
seeds:
  - goal:g7.16.1.11
status: retired
tags:
  - council
  - design
  - g7.16.1.11
  - aa3
  - land
  - trunk
title: "G7.16.1.11.13: AA3 land -- a land is mail one parent edge up; root ff-lands a post's range on the trunk after edge + ring-signer + grow-gate + agi-gate checks; the trunk has ONE writer"
town: core
---
# goal:g7.16.1.11.13

## Why this exists
goal:g7.16.1.11: the council's AA3 section (doc:rse-aa3-land on posts/all-is-one, measured on a scratch repo borrowing MAIN's objects, now 17 lanes (AA3.14), 0 shared refs written) answers the owner's 'things could only go where they must go' for the merge path: today the master's hand-gated merge-up (skill agi-master-gate's landing) and the hub's pre-receive are the only gates. It found three byte defects that make today's gates read nothing (AA3.4) and, after belam's ruling 1efd017e6 (members <- council), a fail-closed rule for council authority (AA3.8: a name in the council row's `members` cell, absent = nobody; belam wrote the cell, faabf9b7a). The author's follow-up: the three byte fixes come BEFORE agi-land, or its checks read nothing. Two later additions (all-is-one 00:4xZ 10-02): AA3.11, the `lands` mask (AA2 defines a `lands` cell on a row, AA3 enforces it in ONE line of agi-land: the council row `lands: ["sanctuary-master"]` means a council member cannot land alive; +294 B), and AA3.10, versioning (belam [decision] 00:25Z, owner 00:3x-00:4xZ): the hourly snapshot is root's carrier pushing the trunk, the trunk's history IS the grid, grid_sync retires with refs/grid/* kept as the archive, and the crontab applier gets its own cadence.

## OWNER 2026-10-01 23:0xZ + 23:2xZ, verbatim (via the council bundle)
"We just need to allow each post to have a will box which they already do, an inbox and a holding box or an outbox or something."
"This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go."
"Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."
Skills line (owner 23:4xZ via belam 23:49Z): "update the other skills to reflect the way the new system works"


## Target end-state
- agi-land (<= 1,829 B, the AA3.14 text as committed in doc:rse-aa3-land AA3.2; root-side, in config:engine-root, 0 B in the zygote) ff-lands <post>'s <sha> on the trunk iff ALL hold at the RECEIVING tip $o: EDGE sender = parent(post) on the parent cells, and a parent with a `members` cell is an INERT group that passes the land to ITS parent (SM and thought-master-new under keep are landed by belam; a group member lands neither itself nor a peer; a post whose parent is owner lands itself) AND MASK the immediate parent's `lands` cell (absent = all children, [] = none: council lands [] since the level round 3a33c71b9), SIGNERS every commit in $o..$sha verifies on root's ring as the sender or a post under <post>, GROWTH grow-gate over $o..$sha, BODY agi-gate $sha, FF $o is an ancestor and the move is compare-and-swap (in MAIN the last step is `git merge --ff-only`).
- The request travels as AA1 mail to root: refs/box/<sender>/root, body `land <post> <sha>`; no master role, no human gate step.
- FOUR byte fixes land FIRST (AA3.4 + fix 4, all-is-one 00:5xZ): (1) [SUPERSEDED by A3: council ruling (alive 22:1xZ, relayed by SM 22:4xZ): SKIP item 1 only, A3's agi-signers ring writes <post>@agi and agi-land strips @agi itself; item 3 (the @agi strip in GROW-GATE's signer sed) BUILDS, grow-gate stays after A3] (2) grow-gate `rev-list $n --not ${AGI_NOT:---all}` (+12 B); (3) grow-gate signer sed strips `@agi` (+7 B); (4) grow-gate is blind to merges (`diff-tree -r` prints nothing for a merge, so a signed merge adding a node in neither parent lands unchecked; lane 4m): `diff-tree -r -c` + treat `AA` as an add (+14 B; grow-gate +33 B in all).
- The trunk reflog shows ONLY root as the trunk writer after the switch.
- VERSIONING (AA3.10): root's carrier pushes the trunk (+ refs/box/*) hourly (branch_push retires: no snapshot commit, every change already IS a commit); the trunk's history is the grid (`git log -- <node path>` replaces refs/grid/node/<mint>); grid_sync is disabled and refs/grid/* are NOT moved or deleted (they are the archive); the crontab applier gets its own cadence (`crons_apply: every_mins 5`, 0 engine bytes), then becomes a projection of cron:crons at the trunk tip with no polling.

## Invariants
- A land is ff-only and compare-and-swap: a not-ff is refused (the child merges the trunk and re-requests), never merged by root.
- Root runs no suite on the land path (small and synchronous); the parent's judgment (suites on tmpfs, reds attributed) happens BEFORE it mails `land`.
- A forged commit (a key outside the subtree) moves nothing; SM cannot land alive; DG1 cannot land itself.
- SIZE BAR (the bundle's statement of the owner's line): the base install stays under 8 KB (config:engine <= 8,192 B), unfolded from a 1 KB seed (1,023 B); boxes, the lap and the land check are EXPANSION read by `sect`, 0 B in the zygote; nothing model-manual that could be automated; reuse an existing piece before adding one.

## Falsifier
1. All 17 lanes of doc:rse-aa3-land AA3.3 + AA3.11 + AA3.14 (3c-3k) + 4m reproduce on a scratch clone against the real ring + real trunk cells (never MAIN): the harness is AA3.9 of doc:rse-aa3-land (17 lanes, committed as extensions/agi/tests/aa3-lanes.t.sh; self-contained, alternates, 0 shared refs written; extract + run: `sed -n '/^## AA3.9/,$p' .agi/nodes/doc/rse-aa3-land.md | sed -n '/^```sh/,/^```$/{//!p}' > /tmp/lanes.sh; sh /tmp/lanes.sh`) and prints 17 lines `ok`. TODAY (trunk 3a33c71b9, with `AGI_LAND=<AA3.14 block>`): 15 ok + `FAIL 4m` + `FAIL 4v`, exit 2; WITHOUT it exit 17 (agi-land is not an engine node yet: DG3's build); with the byte fixes (`GROW_GATE=<fixed grow-gate>`) 17/17 expected; 4m + 4v are the byte-fix witnesses, so the blocking order is a test that fails now and passes when they land.
3. Versioning (AA3.10 V1-V4, see the hypotheses): `git for-each-ref refs/grid | wc -l` is constant for 1 h while posts work; the origin trunk tip is never older than 65 min; a hand edit of the crontab is undone within 5 min; `git log --format=%h -1 -- <node>` on the trunk names the land that carried the node's last per-turn commit.
2. Negative: after the switch `git reflog <trunk>` shows no writer other than root, and `git grep -n 'refs/heads/trunk' -- <post-writable scripts>` returns zero hits.

## Out of scope
goal:g7.16.1.11.11 (the box root reads) · goal:g7.16.1.11.12 (the ring) · goal:g7.16.1.11.14 (skill deltas) · the agi-land build until the three byte fixes land.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
