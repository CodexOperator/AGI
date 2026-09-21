---
id: hypothesis:l4-seat-session-iter-dirs
mint_id: 0aa1eca066914ad4a1c38d25c4dc694b
type: hypothesis
parents:
  - idea:l4-seat-session-owns-its-iter-dirs
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 855480a2980faff5
season: 2
status: pending
tags:
  - l4
  - g15
  - seat-protocol
testable_claim: "TWO HALVES, both required. (a) RESOLUTION: an agent's `iter-<id>/` session dir resolves to the RUNNING WORKTREE's own `.agi/sessions/`, not the main checkout's. The line is `dispatch.py:1075` — `sess_root = locations.shared_project_root(root) or root` — which routes through the shared-state resolver. 🔴 `locations.git_common_root` (`locations.py:212-227`) must KEEP routing the spawn budget, the comms root and the meter pins to the main checkout: a tree-wide concurrency bound that splits per worktree is not a bound. Only the iteration dirs move. Proved by: dispatching from a seat worktree puts the agent dirs under that worktree's `.agi/sessions/iter-<id>/`, while `spawn_budget.py status` still reports ONE budget across every worktree. (b) SESSION-COMPLETE: a command (a `worktree.py` or `rotate.py` subcommand) that REFUSES unless the seat branch is already an ancestor of its parent branch, then COPIES the worktree's `iter-*` dirs into the main checkout's `.agi/sessions/` — an explicit copy, because `sessions/` is gitignored so a merge carries nothing — and only then removes the worktree and the branch. Proved by: it refuses on a non-ancestor branch and removes nothing; on an ancestor branch the iter dirs appear in main and the worktree and branch are gone; and an existing dir of the same name in main is NEVER overwritten. NO node is deleted. The code lands under goal:g15 by the owner's relevance rule. HARD CEILING: 3 kids. 🔴 Do NOT run the full pytest suite — run the targeted test files only and say which. A whole-directory run collides with the other seat and the prime."
thought_session: sanctuary-director-genII-L4
title: Agent iteration dirs land in the main checkout instead of the seat worktree that made them, so a seat cannot harvest its own round
---
<!-- BODY:BEGIN -->
# hypothesis:l4-seat-session-iter-dirs

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
**DIRECTOR HARVEST RECORD (L4.37, sanctuary-director L4 gen II). Both halves PROMOTED. The parent's own verdict never landed, and I am correcting my first account of why.**

🔴 **WHAT I WROTE IN THE HARVEST COMMIT IS WRONG AND THIS IS THE CORRECTION.** That commit says the parent was "alive and looping unproductively" for 1h51m. It was not looping. Twenty seconds before I killed it, it spawned a THIRD kid, `a00-9d75c67b` -- inside its own stated ceiling of 3, with 2 used. It was iterating legitimately at the moment I stopped it. I only learned this because killing the parent and sweeping the budget surfaced a kid that had been minted seconds earlier. The commit message is in pushed history and is not being rewritten; this note is the correction, and a reader should believe this over that.

**What is true about the parent:** it held both completed kids' work STAGED and uncommitted for over an hour, and never wrote a verdict. For comparison, L4.42's parent did the same job with two kids in 18 minutes. Slow and verdict-less is the real finding. "Looping" was my inference, and it was wrong.

**THE SWEEP RULE EARNED ITS KEEP, MEASURABLY.** The brief says one kill is never a stop -- sweep by PID off `spawn_budget.py status` until two consecutive reads are clean. My read BEFORE the kill showed one entry (the parent). My read AFTER showed `a00-9d75c67b tier=kid` -- a kid minted in the seconds around the kill, which a single kill would have left ORPHANED: no parent to review it, burning key with nobody reading the result. It was 20s old, a bare 542-byte scaffold, $0.00145 spent, nothing to harvest. Killed, and the budget then read 0/25 on three consecutive reads with no `pi` process left.

**WHY I HARVESTED RATHER THAN WAITED.** The owner said it looked hung. I measured before acting rather than acting on the description: burn had moved $0.1221 -> $0.1519 over 25 minutes and kid 2's node had been touched two minutes earlier, so it was NOT stopped -- and I said so. What made harvesting right was not that it was dead but that it had produced everything it was going to produce and was not converting it into a verdict, under a standing ruling from the prime for exactly this case.

**WHAT VERIFIED, checked by me in the round's own worktree before promotion:** kid 1's half (local `sess_root` in `dispatch.py`/`cli.py`/`zoom.py` plus `cli._legacy_fallback`) -- 7 passed, 68 insertions / 1 deletion, the deleted line a comment header, and the test asserting the OLD routing this round REVERSES still present and green through the fallback. Kid 2's half (`rotate.py cmd_complete`) -- 12 passed, and for a command that DELETES a worktree and a branch it ships both refusal paths (non-ancestor removes nothing; dirty worktree refuses) plus byte-for-byte preservation of anything already in main and an explicit no-node-deleted assertion. Both honour `goal:g17.13`'s one DO-NOT-MOVE with a test: the spawn budget STAYS on `shared_project_root`.

**Kid 3 produced nothing and is recorded as orphaned, not as a failure** -- it never got far enough to be judged, and attributing a verdict to it would be inventing evidence.
