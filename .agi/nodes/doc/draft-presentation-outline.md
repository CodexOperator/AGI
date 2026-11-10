---
id: doc:draft-presentation-outline
mint_id: 17f16e98ca174006bbfdfc18905c3513
type: doc
parents:
  - goal:g5.4.3
next_edges: []
edited_by: meme-master
season: 3
tags:
  - draft
title: "DRAFT presentation outline v1 -- the class rough draft (under 7 min), from the owner's board + the 11-07 Atlas"
town: core
---
# DRAFT — presentation outline v1

DRAFT. Structure and prompts only: the owner writes every final word (role (b)). Built from the owner's whiteboard (transcribed, privacy-scanned) and the 11-07 "agi Atlas" page.

## The owner's words 2026-11-09 08:18:05Z (c:787879d6bc35), verbatim (in meme-master's own session, with the five board photos) [meme-master store; not an OWNER heading under the interim rule, sp 19:55:55Z 11-09: OWNER blocks cite belam's store only, until the cite leaf under .46 lands]
> For the initial presentation rough draft I have several photos that should be turned into an outline and then followed to flesh out to completion. We can also do benchmarks and data collection via thought master as part of the process. 
>
> Use subagents as needed. 
>
> 1. Yes our class and professors. This is rough draft so no one really other than professor but overall the directors of departments may also be there. [elided, c:2763ec818294] 
>
> 2. Super short 5-10 mins tops. Try to do under 7. Rough draft due Tuesday evening I believe but morning would be best. Tuesday morning. 
>
> 3. Done 
>
> 4. A class paper first but good enough to publish as a long form blog post not necessarily arxiv level yet.

**Frame:** class + professors; department directors may attend (they will ask "what did it produce?"). Rough draft due **Tue 11-11 morning**. Target **6:30**, hard cap 7:00. ~8 slides, ~45 s each.

```
1 Title ─ 2 Problem ─ 3 Why organize ─ 4 Solution ─ 5 Humans ─ 6 Walkthrough ─ 7 Results ─ 8 Measuring success
  0:15     0:50        0:45            0:50          0:40       1:40            0:50         0:40      = 6:30
```

## 1 · Title (0:15)
- Name of the project, one line on what it is. Atlas hero line is the raw material ("one repo: a graph of thoughts + the code that grows it").

## 2 · The problem: multiple agents (0:50)
- Question: can more agents speed up production?
- Running example: rewriting a program in a new language.
- Wall #1: one agent = one context window.
- Problem definition: **code quality + scalability** as the agent count grows.

## 3 · Why organization? (0:45)
- Human examples: teams need structure for the same reason.
- Bad vs good vs beginner organizations.
- Beginner tools for agents today: kanban board · code graph · OpenClaw / Hermes-style self-prompting.

## 4 · The solution (0:50)
- Combine those beginner techniques with:
  - **a thought graph**: a code graph for the *whole process*, not just the code (useful even for one agent). Atlas: the node chain goal → idea → hypothesis → experiment → verdict → mvp.
  - **an agent hierarchy**: chain of command + a job description per agent. Atlas: the crew tree.
- Visual: the board's tree sketch.

## 5 · How humans fit in (0:40)
- What does the human have to give the agents? **Morals, vision, goals**, and the shape of the thought graph.
- Atlas: "the owner writes the morals; agents never do" (the six morals).

## 6 · Walkthrough (1:40) — board order: 1st input → output, 2nd the whole process
- **1st, input → output** (20 s): the one-sentence version: a human hands in a vision, the system hands back finished goals.
- **2nd, the whole process** (80 s), the website as the hypothetical example:
  1. Download the repo. What's inside: role templates (used whenever a new agent is created) + the core graph (the boot sequence: how agents talk, when/how to spawn one, the working graph's geometry; generates the scripts so each agent knows what to do next; searchable).
  2. Ask an agent to run `agi.sh` → it builds the core graph + scripts, creates the Prime Director for the new working graph.
  3. It prompts the user for: visions (discussion) → roles (the website example) → it **creates goals** → a simplified workflow.
  4. Output: "done" when it meets its goals → checks against the vision → writes new goals, or stops and asks the user.
- Visual: a node `.md` with `parents:` and `thought:` (board sketch, top right).

## 7 · Results / recent updates (0:50) — what it produced
- Atlas numbers (as of 11-07; refresh before Tuesday): 5,842 live nodes, 25,400 commits since 30 Apr, 426 reviewed lands, 104k lines of engine code.
- How a change lands: build → council 3/3 → gate → land; every claim carries a falsifier.
- One day: 22 lands on 11-07; the published `falsify` plugin.
- PENDING: benchmarks from thought-master (asked 11-09).

## 8 · Measuring success → open discussion (0:40)
- How do we measure "success"? Attempts? Ideas for the future.
- End on the question, which invites the room to talk.

## Shepherd chunks (one at a time, at the owner's pace)
| chunk | the owner does | size |
|---|---|---|
| 1 | Approve or reorder these 8 slides and timings | 5 min |
| 2 | Write slide 2 in their own words (3-4 bullets) | 10 min |
| 3 | Slide 3 | 10 min |
| 4 | Slide 4 | 10 min |
| 5 | Slide 5 | 5 min |
| 6 | Slide 6, input → output + steps 1-2 | 10 min |
| 7 | Slide 6, steps 3-4 | 10 min |
| 8 | Slide 7 (with TM's numbers) + slide 8 | 10 min |
| 9 | Title + one timed read-through | 10 min |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, meme-master gen 1: v1. Owner 11-09 (this session): "several photos that should be turned into an outline and then followed to flesh out to completion"; audience class + professors (+ department directors), 5-10 min "try to do under 7", rough draft due Tuesday morning. Board order kept (problem → organization → solution → humans → 1st input/output, 2nd walkthrough → updates → metrics); the Atlas plates mapped onto slides 4, 5 and 7. The faculty audience is why "results" is its own slide rather than folded into the walkthrough.
v1.1, same day: the owner's chunk-0 answers placed verbatim as an OWNER block citing c:787879d6bc35 (store up at 19:51Z); the outline itself unchanged.
Then, same day: OWNER headings turned back into plain headings (words and chunk ids kept) on the council's interim rule (self-perpetuating 19:55:55Z 11-09, via SM): verify-land runs agi-mem cite as belam, so an OWNER block citing a chunk in this post's store would HOLD every later OWNER-file land town-wide. They return to OWNER once the cite leaf under .46 lands.
v1.2, 11-10: every mention of the owner's verbal-only item elided or reworded, on the owner's word (c:4b5d4abae03e: "cut"; the item itself kept verbal-only, c:2763ec818294), matching goal:g5.4.3.1's A2 (council alive 04:42:39Z 11-10). No other change.
<!-- THOUGHT:END -->
