---
id: goal:g5.4.5
mint_id: 4bae4cfe5f8d4d1899243592fa7e7d93
type: goal
parents:
  - goal:g5.4
next_edges: []
confidence: 0.5
goal_id: G5.4.5
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 952ad972ed4b37a6
season: 3
seeds: []
status: complete
tags: []
title: "G5.4.5: origin's refs/heads holds only what must be a branch (master + the season trunk); every other head lives under refs/agi/*, archived at its sha before any delete, never lost"
town: core
---

# goal:g5.4.5

## Why this exists
goal:g5.4 (the season review and rollover, end to end): belam's inventory of origin, measured 16:1xZ 11-18, read 26 heads where two must be branches (master, the GitHub default that seal.yml runs from; core/season3/main, the trunk). 15 hold no commit the trunk lacks (five of them one sha, the 10-15 reshuffle's stubs); 8 hold unique commits (core/season2/main +430, archive/core-season3-main-pre-20261014 +1853, core/season2/et-grok-pilot +2410 among them). Each season's rollover and reshuffle leaves heads behind, and g19 (the L5 tidy pass, branch deletes) is retired, so no live goal carries the rule; the 10-15 reshuffle is the precedent for the act (43 refs already under refs/agi/archive/*).

## OWNER 2026-11-18 16:09:31Z, verbatim (owner chunk c:641c03d9d7ee; chat to belam, relayed [owner] 16:1xZ)
"Can we also trim the remote branches. Somewhere in the goals it should be noted that we shouldn't have any stray remote branches if we can help it unless it's more necessary now just because it's hard to find a specific branch where everything sits. I guess season3/main is it but I just see a good few others and was wondering if they were absolutely required or could be consolidated. Thank you, I'll let you all handle it"

## Target end-state
- STANDING RULE: origin's refs/heads holds only what must be a branch: master (the GitHub default; seal.yml runs there), the current season's trunk (today core/season3/main), and season3/main while config:key-authority reads it (authority_ref: origin/season3/main; send.py's authority read fetches it by name on every send-verify and whois, and a failed fetch leaves every caller UNVERIFIED; self-perpetuating 16:18:21Z 11-18). Re-pointing key-authority is its own cut and the council's call; season3/main is archived only after it. Everything else lives under refs/agi/* (hidden from GitHub's branch list, never lost).
- Every head moved off refs/heads today is first pushed to refs/agi/archive/heads/<name> at its own sha, never forced (a name already archived at another sha = refuse, never overwrite the older archive), and read back equal; its delete uses --force-with-lease=<name>:<sha>, so a head that moved meanwhile is refused, never lost.
- Before the act, read outward and stop on any change: GitHub's open pull requests' head branches intersect the act's heads in 0 (deleting a PR's head branch closes that PR; any such head is named and kept, its PR closed only on the owner's word), and the repo's default branch reads master (all-is-one 16:27:25Z 11-18; belam's read 16:3xZ: 0 open PRs, default master).
- posts/belam stops reappearing as a head: whatever pushes it writes refs/agi/posts/belam instead (its own lane, after the act). F1 reads green only once that lane has landed and posts/belam is archived; the leaf closes on both.
- A season rollover that adds a head names it here, with why it must be a branch, or archives it in the same act.

## Invariants
- No commit reachable from origin before the act becomes unreachable after it: every removed head's sha is reachable from a refs/agi/archive/heads/* ref.
- master, the trunk and season3/main (while key-authority reads it) are never touched by the act.
- Reversible per head: push the archived sha back to refs/heads/<name>.

## Falsifier
1. Run at the repo's top level; exits 0 only when origin's heads are master + the trunk (+ season3/main while key-authority reads it) alone, refusing an empty read (a failed ls-remote reads no heads, a vacuous pass) and a read with the trunk gone (self-perpetuating 16:18:21Z: without the trunk conjunct, 'master only' read rc 0):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && h=$(git ls-remote --heads origin) && printf '%s\n' "$h" | grep -q 'refs/heads/master$' && printf '%s\n' "$h" | grep -q 'refs/heads/core/season3/main$' && [ "$(printf '%s\n' "$h" | awk '{print $2}' | sed 's#^refs/heads/##' | grep -cvxE 'master|core/season3/main|season3/main')" = 0 ]`
2. Negative, nothing lost, on a SECOND WITNESS: before the act starts, a seat that is NOT the act's runner boxes its own `git ls-remote --heads origin` read whole (names + shas, its line count beside it; 26 at alive's and self-perpetuating's reads 16:1xZ 11-18); the act's own before-record (its own read, quoted whole in this leaf's close THOUGHT) must hold the same lines, a count or line mismatch = RED; and for EVERY line of the WITNESS read except master, the trunk, season3/main and posts/belam, `git ls-remote origin refs/agi/archive/heads/<name>` prints that line's sha, 0 missing. A head that moved between the witness read and the act is refused by the lease and named in the record. (alive 16:22:56Z: a record the act writes itself lets an omitted head pass; self-perpetuating 16:24:46Z: a count taken from that same record misses it too, so the count is checked against a read the act did not make.) AMENDED AT CLOSE (11-22, reason in the THOUGHT): the two KEPT trunk heads (core/season3/main, posts/belam) are compared by ANCESTRY, not sha (the witness sha must be an ancestor of the before-record sha): a land between the witness read and the act fast-forwards them and omits nothing; every other line by name + sha.

## Out of scope
goal:g19 (retired: the L5 tidy pass). The engine's local branch SPELLINGS in branches.py and the frozen test fixture strings (local refs, not origin heads). Another box's fetch of a town head by name (local-town, lab): read by the council before the act, never assumed.

## Agent Notes
Assigned to **belam**.
Closed 11-22: the 11-18 act archived 22 heads (refs/agi/archive/heads/*); lane A (belam's land.sh push of refs/heads/posts/belam dropped, the head archived at 2dd9a2bb4e and deleted 11-22); lane B = B3 (season3/main stays while config:key-authority reads it; council 3/3 16:4xZ 11-22). Origin heads: master, core/season3/main, season3/main.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v6 (sanctuary-master gen 104, 17:1xZ 11-22): CLOSED complete. Each falsifier's own words beside its reading:
- F1 'exits 0 only when origin's heads are master + the trunk (+ season3/main while key-authority reads it) alone': rc 0 at MAIN's top level 16:5xZ 11-22 (sanctuary-master; self-perpetuating 16:50:07Z re-ran it from the node, rc 0); belam's L643 [landed] 17:07Z, land.sh's own falsifier line: 'posts|archive|box|held heads=0, core/season3/main==land yes', 3 heads.
- F2 'the act's own before-record (its own read, quoted whole in this leaf's close THOUGHT) must hold the same lines' as the second witness: the before-record is quoted below (belam's g545/trim.sh, 17:51:35Z 11-18, 26 lines, sha256 9c0022f67b2a0eb9); vs all-is-one's witness (box abeb55b520, 17:47:47Z 11-18, 26 lines): 26 names equal; 24 lines equal by sha; 2 differ, BOTH kept trunk heads, core/season3/main and posts/belam: witness 2e3c11992d (L636) -> act c031a072b9 (L637, landed between the reads), 2e3c11992d an ancestor of c031a072b9 (ff). As written that is a line mismatch = RED; it omits nothing, so F2 is AMENDED (kept trunk heads by ancestry) with this reason, never rewritten to fit after the fact. 'for EVERY line of the WITNESS read except master, the trunk, season3/main and posts/belam, ls-remote origin refs/agi/archive/heads/<name> prints that line's sha, 0 missing': 22 of 22 at the before-record sha, 0 missing (sanctuary-master 17:1xZ 11-22); alive 16:51:54Z against its own witness (26 lines, 16:25:48Z 11-18) and self-perpetuating 16:50:07Z against all-is-one's: 0 missing each.
The ACT's before-record, whole (git ls-remote --heads origin, 17:51:35Z 11-18):
```
4b8f28b5e16373dd4de6b58e25f099deed4a48f1	refs/heads/archive/core-season3-main-pre-20261014
93167c7104b57275a0b2a2fb795a7f18886559b2	refs/heads/belam-dr1-row
a67ea78861ef3abf2b49037273716f0ec8059f96	refs/heads/codex-town/main
8fb4fe77727740d59318642cd3d5801373f66c43	refs/heads/codex-town/season2/main
2a8056bcb5a246c53650053f1c8d655cf3a01ed9	refs/heads/core/main
f0b99691cd4160ea4a3a3722e23b87705c801017	refs/heads/core/season2/et-grok-pilot
ccb285d98fd501c5a4cc0263e0799404c9333d57	refs/heads/core/season2/main
c031a072b9d18f788b3efc7fb39e7022f11e6188	refs/heads/core/season3/main
1e94cd0822e19783b4d93fbeaf66bf85be1fe4c4	refs/heads/encryption-town/main
4a6524137373b35d544e8b96b4fb997c8ba7ebf5	refs/heads/encryption-town/season2/main
3bb25d254aa706552b87fbbac6a6454b0d9fa28c	refs/heads/local-maxxing/main
da9deccaef859b8108dd3c3cea09a3d1c9a6b864	refs/heads/local-maxxing/season3/main
dc7ec920bafd2c117a269beb3356988f4f3ec859	refs/heads/master
c031a072b9d18f788b3efc7fb39e7022f11e6188	refs/heads/posts/belam
2a8056bcb5a246c53650053f1c8d655cf3a01ed9	refs/heads/sanctuary/main
7067a03ae4816c9837e61ef7387ebb7504ef94d2	refs/heads/sanctuary/season3/main
2a8056bcb5a246c53650053f1c8d655cf3a01ed9	refs/heads/season3/main
2a8056bcb5a246c53650053f1c8d655cf3a01ed9	refs/heads/streaming-suite/main
51f6817640aec5efae234751db17df9556888aba	refs/heads/streaming-suite/season3/main
54ef0873c491ceb7ca69271ff81e1c0798338a5c	refs/heads/tip/belam/agi-cred-unread
468ef2a9807c2be46e28712f6c1165082ef48ccd	refs/heads/tip/belam/b1-and-flip-word
8b8a2843acff32d0f9aefebbff4dc5b98b490be9	refs/heads/tip/belam/b1-flip-row1
6dee81eef6b603a5ac74740c700de58384904562	refs/heads/tip/belam/stall-watch-n1n2
6fce4e8ce13a8d60c824a2dfec5a4fb8766b730b	refs/heads/tip/belam/stall-watch-unread
2a8056bcb5a246c53650053f1c8d655cf3a01ed9	refs/heads/web-app-suite/main
37a1761443993a416c736fba07dba89b8ce2e16b	refs/heads/web-app-suite/season3/main
```
<!-- THOUGHT:END -->
