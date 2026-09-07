---
id: goal:s12
mint_id: 9532754542ee47ac806a47721c2c89c5
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S12
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S12: `snapshot-goals.py` silently truncates goal bodies at 4000 chars"
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

~~Until fixed, treat `GOALS.md` as the only complete copy of any goal over ~4k
characters, and do not infer from a goal node's absence of text that a goal
does not say something.~~ **Fixed 2026-08-25 — a clipped goal now says so, in
the node, in the sentence above's own words.**

Both questions are answered, and separately, as the split above demanded:

1. **Silent truncation is gone.** `cap_body()` cuts at a blank-line block
   boundary, so a table, list or fenced block is wholly present or wholly
   absent — never severed mid-cell. It appends an explicit marker naming how
   many characters were dropped and where the complete text lives, and it warns
   on stderr naming the goal. A single block bigger than the cap is **kept
   whole and over-cap**, because an honest overrun beats a malformed fragment
   and there is no boundary inside it to cut at.
2. **The cap is the owner's, so the engine stopped picking.** `goal_body_cap`
   in `agi-tree.config.json` overrides the 4000 default; `0` disables capping
   entirely. That is the project's own customization surface, which is where a
   policy knob belongs rather than in an engine constant invisible from inside
   the project. **The default is unchanged at 4000 — nobody has picked yet.**

Live on the next `--smoke`: 7 goals now report their own truncation
(G2.5 −2365, G7.8 −2256, S16 −1658, G6.6 −983, G10.2 −600, G7.5 −538,
G6.3 −336). `goal:g2.5`'s body no longer ends `| Assigned | once, at node
creation | derived,` — it ends on a complete sentence followed by the marker.

**Recorded because of how it was fixed, not only that it was:** this is the
first engine change to originate in `agi-tree` and reach `agi` without anyone
opening a file in the engine repo. See **G6.1**.