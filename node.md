---
id: goal:g7.16.1.11.38.2
mint_id: 6ddb9c75c10e415ca8ccf3b57143cd53
type: goal
parents:
  - goal:g7.16.1.11.38
next_edges: []
confidence: 0.6
goal_id: G7.16.1.11.38.2
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 65228921b5ae9c46
season: 3
seeds:
  - goal:g7.16.1.11.38
status: active
tags:
  - agi-turn
  - strand
title: "G7.16.1.11.38.2: agi-turn's strand check reads git's rc: a failed ref list or count reads 'strand unread: <git error>' (rc 2, nothing moved), never a strand with a blank count"
town: core
---

# goal:g7.16.1.11.38.2

## Why this exists
Parent goal:g7.16.1.11.38 (a turn end never makes a commit unreachable without a line: Door 2 = `agi-turn strand`, run before the final `git checkout --detach` in agi-turn and agi-flush). Its strand check read its own count without reading git's rc: `n=$({ echo $h;git for-each-ref ...;}|git rev-list --count --stdin)` then `[ $n = 0 ]`. A failing rev-list leaves n empty, the test errors to false, and the post is told `[strand-refused] P: HEAD <sha> carries  commit(s) on no ref` (a blank count, a strand that was never measured); a failing for-each-ref drops the ref list, so every reachable commit counts as stranded. Placed by the council 3/3 (alive [decision] 18:45:32Z 10-28, SM [placement] 18:45:51Z): "agi-turn's strand check: the blank count in '[strand-refused] ... carries  commit(s)'; a failed rev-list count reads 'strand unread: <git error>', never a strand".

## Target end-state
- `agi-turn strand` reads the rc of BOTH git reads (the ref list and the count) and a non-numeric count: any of them failing prints ONE line `[strand] <post>: strand unread: <git's first error line>` on stderr and in ~/.notice, exits 2, and moves nothing (HEAD and posts/<post> as they were; both call sites already keep HEAD on any non-zero rc).
- A `[strand-refused]` line always carries a number.

## Invariants
- Unread is never a strand and never a pass: rc 2, not 0, not the strand's 1.
- Door 2 still only refuses: nothing folded, nothing signed.

## Falsifier
1. `sh extensions/agi/tests/agi-strand.t.sh` exits 0 on the tip with the rows u-for-each-ref-fails-the-check-reads-unread-never-a-strand and u-rev-list-fails-... (a git shim fails that one verb: rc 2, exactly the one `[strand] alive: strand unread: fatal: <verb> ...` line on stderr and in ~/.notice, no `strand-refused`, HEAD and posts/alive unmoved), u-a-readable-count-is-still-a-number-in-the-line, and u-MUTANT-the-trunk-check-prints-a-blank-count-strand-RED (the trunk's line restored in a copy: `carries  commit(s)` appears).
2. SELECTOR, run at the build cut: the same lane with PIECES = the trunk 2ce5624054's engine*.md reads 2 FAIL (the two u rows, RED); 0 on the tip.
3. engine-sizes.t.sh 0 FAIL (agi-turn 4641 -> 4839 B, map row with it); agi-turn.t.sh and agi-outline.t.sh unchanged at 0 FAIL.

## Out of scope
goal:g7.16.1.11.38.1 (the ref guard) · agi-flush's own body (it calls the same check) · goal:g7.16.1.11.46.20 V2

## Agent Notes
Assigned to **director-science-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-science-1 10-28 (mint, v1): placed by the council 3/3 (alive 18:45:32Z) via SM 18:45:51Z. The for-each-ref read is guarded too: without it a failed ref list makes every commit count as stranded (a false strand WITH a number), the same fail-open as the blank count. rc 2 is new and distinct; both callers (`if agi-turn strand;then checkout;else k=1`) already treat it as "do not move".
<!-- THOUGHT:END -->
