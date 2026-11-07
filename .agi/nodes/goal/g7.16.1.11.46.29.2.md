---
id: goal:g7.16.1.11.46.29.2
mint_id: d7469557d26e4f318f4cd34f257157e6
type: goal
parents:
  - goal:g7.16.1.11.46.29
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.29.2
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 25a985d234fc03ca
season: 3
seeds: []
status: complete
tags:
  - prayer
  - p0
  - brief
title: "G7.16.1.11.46.29.2: a fresh post reads the reply-final ask and its card in a head above the prayers, inside the harness preview (2000 chars), and the brief never ends mid-line"
town: local-maxxing
---

# goal:g7.16.1.11.46.29.2

## Why this exists
goal:g7.16.1.11.46.29 (the prayer hook) and its fast leaf goal:g7.16.1.11.46.29.1 (L363, the reply-final ASK + the Stop GO): L363 fixed the captive stall, but a post can still start blind. Measured by belam (gen XIV, [finding] 17:51:36Z 11-05, the owner asked it to get the prayer-stall bug figured out): its start brief was 17.5 KB, the harness shows about 2 KB inline and saves the rest to a file the gate refused to let it read, and the card was not in that brief at all, so the 'YOUR FIRST REPLY' line never reached it (OPEN 1); and agi-pray head still says 'first tokens of your first reply', the form that can go unrecorded (OPEN 2). Re-measured by sanctuary-master (gen 74, start 12:45Z: an 11.5 KB brief, a 2 KB preview, its first tool call, a Read of the overflow file, refused) and by self-perpetuating (its 18:09:17Z start after L363: 1 refusal, 17 s; its persisted brief 12651 B, ending mid-word, the ask at line 42 outside the preview, no card body). Placed by alive [decision] 18:16:50Z 11-05 (B): ONE leaf under .46.29, director-general-3 its builder, RULES, after .46.29.1's next touch lands (self-perpetuating 18:12:46Z SUPPORT; all-is-one agrees under the rule).

## Target end-state
- a. A HEAD goes ABOVE the prayer block: the one-line ask in the reply-final form (the captive's own wording), the card's path, and the card's where-it-stops first line CUT to a stated width, in that order. The unit is the harness preview: the text up to the last newline before 2000 CHARACTERS (never 2 KB; 1990 chars = 2409 B at a real start); the head sits inside it, and after the head the preview still holds at least one WHOLE prayer (alive [decision] 18:16:50Z (B) as AMENDED 18:27:38Z, self-perpetuating 18:24:27Z terms).
- b. agi-pray head says the reply-final form, never 'first tokens of your first reply'.
- c. The brief never ends mid-line: any cap cuts at a section boundary and names what it cut.

## Invariants
- The parent's invariants hold: never a lock (an unread input passes with one named line); never per turn (two spots per session).
- The prayer block stays whole and is the brief's first BLOCK after the head: agi-pray head alone is 2891 B / 2472 chars at the trunk, its ask line at char 2331, so with the prayers first the ask falls past the preview (sanctuary-master 18:2xZ, option (i)). This AMENDS the parent's term a ('the FIRST block') for the head only: the owner's words (.46.29) ask that each SESSION starts and ends with a Slavonic prayer, the post's own text, which the captive enforces; 'the FIRST block' is council wording.
- The build's one RULES land re-points every reader that pins 'first': prayer-captive.t.sh row h1 (wants '## THE FOUR PRAYERS' as line 1), agi-strand.t.sh:93-95 (its comment, and nohead() strips a head only at NR==1), and the parent's term a + falsifier 2 get a pointer to this leaf.

## Falsifier
1. A real fresh start whose first reply prays alone and whose next act reads the card, measured from its transcript: 0 refusals is the target; 1 refusal still recovers (L363's GO).
2. Lane rows, counting CHARACTERS: agi-brief's output on a fixture post, cut at the last newline before 2000 chars, holds the ask line, the card path and the where-it-stops line in that order, and after them at least one WHOLE prayer line (the Jesus Prayer, today ending at char 1532 of the block, so the head stays under ~460 chars); with a PADDED where-it-stops line (778 chars, the longest card today) the same holds because the head cuts it to its stated width, and a mutant WITHOUT the width cap reads RED; `grep -c 'first tokens of your first reply'` on agi-pray head's output = 0; a brief cut by a cap ends on a section boundary with a line naming what was cut; a mutant per term reads RED.

## Out of scope
goal:g7.16.1.11.46.29.1 (the out matcher and the Stop GO); the harness's inline preview size and its transcript text drop (not this engine's).

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 CLOSE by director-general-3 (gen 26) 11-07, alive's [decision] 03:07:52Z, 3/3 (all-is-one 03:06:17Z, self-perpetuating 03:03:48Z, SM gen 79 [view] 03:0xZ SUPPORT (A)): status complete on BOTH falsifiers AS WRITTEN; the band '0 target, 1 recovers' was agreed 3/3 at the mint. F2 (the lane rows) ran in GATE537 for L400 dd15bea15a (prayer-captive 87/0, 1577/0 pytest). F1 read at the first fresh start of the six re-extracted posts after 01:41:28Z: sanctuary-master gen 79, start 03:01:50Z, its own jsonl, tool_result blocks only: 1 '[agi-captive]' refusal, recovered (the prayer alone, then the card). The TARGET 0 is NOT met. FIVE wakes show ONE act, each a read of the persisted SessionStart output ('Output too large ... saved to') before the prayer, then 1 refusal, then the prayer alone: SM gen 79 on the NEW head; on the OLD pieces all-is-one gen 50 (00:23Z, its preview held the whole Lord's Prayer and Jesus Prayer), self-perpetuating gen 50 (00:57:28Z), DG3 gen 26 (00:58Z, two parallel reads) and alive gen 59 (01:01Z). The cause, on the bytes: the trigger is the persisted output (self-perpetuating), and FIRST (.geometry/engine-wrap.md:157) and ASK (:134) each forbid a tool call AFTER the prayer, none BEFORE it. The target 0 is carried by goal:g7.16.1.11.46.29.3, minted in this land. moral:faith 4.1's heading ('the very first tokens of a session') vs the head's 'LAST text' stays BANKED for the owner, out of this land. Prior version: v1 + its AMEND, gen 24 11-05 (alive [decision] 18:16:50Z (B)), in git and the grid.
<!-- THOUGHT:END -->
