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
status: active
tags: []
title: "G5.4.5: origin's refs/heads holds only what must be a branch (master + the season trunk); every other head lives under refs/agi/*, archived at its sha before any delete, never lost"
town: core
---

# goal:g5.4.5

## Why this exists
goal:g5.4 (the season review and rollover, end to end): belam's inventory of origin, measured 16:1xZ 11-18, read 26 heads where two must be branches (master, the GitHub default that seal.yml runs from; core/season3/main, the trunk). 15 hold no commit the trunk lacks (five of them one sha, the 10-15 reshuffle's stubs); 8 hold unique commits (core/season2/main +430, archive/core-season3-main-pre-20261014 +1853, core/season2/et-grok-pilot +2410 among them). Each season's rollover and reshuffle leaves heads behind, and g19 (the L5 tidy pass, branch deletes) is retired, so no live goal carries the rule; the 10-15 reshuffle is the precedent for the act (43 refs already under refs/agi/archive/*).

## OWNER 2026-11-18 16:1xZ, verbatim (chat to belam, relayed [owner] 16:1xZ)
"Can we also trim the remote branches. Somewhere in the goals it should be noted that we shouldn't have any stray remote branches if we can help it unless it's more necessary now just because it's hard to find a specific branch where everything sits. I guess season3/main is it but I just see a good few others and was wondering if they were absolutely required or could be consolidated. Thank you, I'll let you all handle it"

## Target end-state
- STANDING RULE: origin's refs/heads holds only what must be a branch: master (the GitHub default; seal.yml runs there), the current season's trunk (today core/season3/main), and season3/main while config:key-authority reads it (authority_ref: origin/season3/main; send.py's authority read fetches it by name on every send-verify and whois, and a failed fetch leaves every caller UNVERIFIED; self-perpetuating 16:18:21Z 11-18). Re-pointing key-authority is its own cut and the council's call; season3/main is archived only after it. Everything else lives under refs/agi/* (hidden from GitHub's branch list, never lost).
- Every head moved off refs/heads today is first pushed to refs/agi/archive/heads/<name> at its own sha and read back equal; its delete uses --force-with-lease=<name>:<sha>, so a head that moved meanwhile is refused, never lost.
- posts/belam stops reappearing as a head: whatever pushes it writes refs/agi/posts/belam instead (its own lane, after the act). F1 reads green only once that lane has landed and posts/belam is archived; the leaf closes on both.
- A season rollover that adds a head names it here, with why it must be a branch, or archives it in the same act.

## Invariants
- No commit reachable from origin before the act becomes unreachable after it: every removed head's sha is reachable from a refs/agi/archive/heads/* ref.
- master, the trunk and season3/main (while key-authority reads it) are never touched by the act.
- Reversible per head: push the archived sha back to refs/heads/<name>.

## Falsifier
1. Run at the repo's top level; exits 0 only when origin's heads are master + the trunk (+ season3/main while key-authority reads it) alone, refusing an empty read (a failed ls-remote reads no heads, a vacuous pass) and a read with the trunk gone (self-perpetuating 16:18:21Z: without the trunk conjunct, 'master only' read rc 0):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && h=$(git ls-remote --heads origin) && printf '%s\n' "$h" | grep -q 'refs/heads/master$' && printf '%s\n' "$h" | grep -q 'refs/heads/core/season3/main$' && [ "$(printf '%s\n' "$h" | awk '{print $2}' | sed 's#^refs/heads/##' | grep -cvxE 'master|core/season3/main|season3/main')" = 0 ]`
2. Negative, nothing lost: for each line `<name> <sha>` of the act's before-record (quoted whole in this leaf's close THOUGHT), `git ls-remote origin refs/agi/archive/heads/<name>` prints that sha; 0 lines missing.

## Out of scope
goal:g19 (retired: the L5 tidy pass). The engine's local branch SPELLINGS in branches.py and the frozen test fixture strings (local refs, not origin heads). Another box's fetch of a town head by name (local-town, lab): read by the council before the act, never assumed.

## Agent Notes
Assigned to **belam**.
