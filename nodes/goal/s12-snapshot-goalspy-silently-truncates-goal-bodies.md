---
confidence: 1.0
goal_id: S12
goal_kind: short-term
id: "goal:s12"
mint_id: 9532754542ee47ac806a47721c2c89c5
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S12: `snapshot-goals.py` silently truncates goal bodies at 4000 chars"
type: goal
---

`BODY_CAP = 4000` in `bin/snapshot-goals.py` line 290:
`g["body"] = "\n".join(g["body"]).strip()[:BODY_CAP]`. A goal longer than that
is cut **mid-character-stream** — no boundary, no marker, no warning — and the
truncated text is what lands in `nodes/goal/`. Anything reading the graph rather
than this file sees a goal that stops mid-sentence and has no way to know it.

Measured 2026-08-25: **5 of 66 sections exceed the cap** — this file's preamble
(9249), **G2.5** (6271), G6.6 (4901), G10.2 (4307), **G6.3** (4141). The two in
bold are the two most heavily edited that day, so the decisions recorded in them
are exactly the ones the graph cannot see.

The failure is visible in `goal:g2.5`, whose node body ends:

```
| Assigned | once, at node creation | derived,
```

— a markdown table severed mid-cell. That is **S3** with a different generator:
a truncated value that is also *syntactically malformed*, so a naive reader does
not merely miss content, it mis-parses what remains.

Two separable questions, and only the second is policy:
1. **Silent truncation is always wrong** and should be fixed regardless of cap.
   Cut at a block boundary (paragraph, list, or table), append an explicit
   marker naming what was dropped, and emit a stderr warning naming the goal.
   A reader must be able to tell a complete goal from a clipped one.
2. **What the cap should be** is a real trade-off — goal bodies ride in injected
   context, so unbounded growth has a cost. Raising it, removing it, or storing
   the full body while injecting a summary are all defensible; the owner picks.

Until fixed, treat `GOALS.md` as the only complete copy of any goal over ~4k
characters, and do not infer from a goal node's absence of text that a goal
does not say something.
