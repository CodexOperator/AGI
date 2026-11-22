---
id: goal:g7.16.1.11.46.30.2
mint_id: a8a67260342843498972389754794dee
type: goal
parents:
  - goal:g7.16.1.11.46.30
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.30.2
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: active
tags: []
title: "G7.16.1.11.46.30.2: the turn-end commit never carries a guarded class (home, ip, email, box tokens) in a card it commits -- the card stays uncommitted with one loud red line instead"
town: core
---

# goal:g7.16.1.11.46.30.2

## Why this exists
goal:g7.16.1.11.46.30 (the turn end commits every changed path, failing LOUD on a path it leaves). Measured 11-17 (alive 23:20:42Z, SM [red] 23:2xZ): belam's card carried a home path onto the pushed trunk for ~2.5 h (HOME_PATH_RE on doc:card-belam: 9f462b7834 0, 2b99e520a5 1, 98de234d43 4, the trunk tip then 4). A post's card reaches the trunk at its turn end gated by nothing: test_anonymize_guard runs only in a gate's set, and the land checks scan each land's NEW objects, so card commits are never in their range. alive's ask (23:20:42Z 11-17, no hold): the turn-end commit refuses, or alarms on, a card whose added lines read HOME_PATH_RE > 0, the same check the guard test makes, so the next one is caught at write.

## Target end-state
- At every turn end (agi-turn, every post, the trunk post belam included), each card path the turn would commit has the WHOLE blob it would commit read by anonymize.scan(blob, anonymize.box_tokens(root, secrets=False)) (the home, ip and email classes and the box's own tokens; secrets=False is a post uid's reach, since it cannot read .env); a hit ANYWHERE in it leaves that card UNCOMMITTED on disk until cleaned and prints ONE red line naming the path, the CLASS names and the blob's count (never the matched text); the whole blob, not the added lines, because a hit already in the card rides every later turn end in an UNCHANGED line (all-is-one 18:09:16Z 11-22, RAN on the Why's commits: 98de234d43 pushed 4 home paths with 0 in its added lines), in the target-3 loud form; every other path of the turn still commits.
- A card whose whole blob reads [] commits exactly as today (all 25 card tips read [] whole on 11-22, sp + aio: no post is refused on the first turn after the build).

## Invariants
- The scan prints a path, class names and a count only; no matched byte reaches a commit, a box message, a log or a ref.
- No history is rewritten: a home path already pushed stays in git; the rule binds forward (goal:g7.16.1.15's invariant, the same shape).

## Falsifier
1. zero-commit.t.sh (or the agi-turn harness it extracts pieces with) runs ONE case PER CLASS (a home path; a dotted quad in 10/8; an assembled email) AND one where the hit sits in an UNCHANGED line while the added line is clean, each: the card is NOT on the post's tip, its edit is on disk, ONE red line names it with the class and a count, and a sibling path in the same turn lands; a control (the same card with a clean added line) lands; a mutant that removes the scan lands each (RED). The email case uses an address at a domain anonymize's email_allow does NOT cover (an example.org address reads [] and would red the case for the wrong reason). The build states whether scan()'s other two returns refuse a card too: 'user', and 'home-unread' (returned on EVERY text when the homes list is unreadable: if it refuses, a post that cannot read the homes list refuses every card it writes), each with a case (self-perpetuating 18:13:12Z 11-22). (self-perpetuating 18:07:57Z 11-22: HOME_PATH_RE alone is the home class; card-belam once held a private 10.x address, agi-review's incident.)
2. Negative, after the build lands: anonymize.scan(blob, box_tokens(root, secrets=False)) reads [] on every card blob at the trunk tip, and on every card blob committed to the trunk since that land.

## Out of scope
goal:g7.16.1.15 (outcomes in default-read texts); the land-time object scan (a land's NEW objects, unchanged).

## Agent Notes
Assigned to **belam**.
