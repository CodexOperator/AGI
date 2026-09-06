---
id: goal:s28
mint_id: c43a2514d4a843339de9e0f4244232a3
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S28
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S28: A parent erases itself from the iteration manifest by spawning a kid"
---
**Found by the parent, in its `struggles:` line, on the second parent-tier run
(2026-09-02). Third time this session that field beat the review it came
attached to.** Quoted verbatim:

> dispatch.py rewrites the whole iter manifest each call, so spawning my kid
> dropped my own parent entry from manifest.json — the system tracked only the
> kid, not me; I closed my session by hand via cli.py done instead

Confirmed in one command. After a parent spawned one kid:

```
agents in manifest: ['a00-f0fd9669/kid']      # the parent is gone
```

`dispatch.py:329` writes `manifest.json` **wholesale** from the agents of that
one invocation. It was written when a dispatch was the only dispatch in an
iteration. A parent shelling out to `dispatch.py --tier kid` is a *second*
dispatch into the *same* iteration directory, and the second write clobbers the
first.

## 🔴 It makes `goal:s27`'s completion path unreachable

This is the part that matters and it is not cosmetic. `post_wire` iterates
`manifest["agents"]`. The parent-admission branch added for `goal:s27` —

```python
if not finished and not node_id and completion.owns_all_complete(root, owns):
```

— is **correct and never runs**, because the parent is no longer in the list
`post_wire` is iterating. `owns` is written faithfully to the parent's own
`agent.json` (verified: `owns=['experiment:a00-f0fd9669-ce583f']`) and nothing
reads it. **A parent's completion is currently recorded and discarded**, which
is precisely the four-hop marshalling failure that dropped every pi verdict for
the life of the pi runtime — same shape, one tier up.

`heal.py` is affected the same way: it cannot monitor, time out or restart an
agent that is not in the manifest.

## What the fix has to be, and the constraint it must respect

**Merge, do not overwrite.** A dispatch into an existing iteration directory
must union its agents into the manifest rather than replace them, keyed by
agent id so a re-dispatch of the same agent updates rather than duplicates.

**The constraint:** two dispatches can race. A parent may spawn kids while
another dispatch is writing, so read-modify-write needs to be atomic — write to
a temp file and rename, at minimum. This is `goal:g4.1`'s territory (parallel
kids share one working tree) arriving one level up, and it is the first
concrete instance of it that is not hypothetical.

## Falsifier

Spawn a parent; have it spawn two kids; assert the manifest contains **three**
agents with the parent's `tier: parent` entry intact. Then run `post_wire` and
assert the parent is admitted via `owns_all_complete` — the branch executing at
all is the real test, since today it cannot. Finally, spawn two kids
concurrently from one parent and assert no agent entry is lost.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed 2026-09-02, iteration 101, and the way it closed is the record worth
keeping: **every clause of the falsifier was executed, and executing the last
one found a second defect that the fix for the first had introduced.**

Clauses 1 and 2 held. A live parent (`a00-dea93ac5`, qwen) spawned a kid into
its own iteration directory and its `tier: parent` entry survived — the exact
sequence that erased it before. The same parent then ran `post_wire` on a
scratch project and watched the `owns_all_complete` branch fire and admit a
parent, so the path this goal called unreachable is now observed live rather
than argued for.

Clause 3 did not hold, and it was never run before today. `b8cb2ec05` shipped
the merge with **no test behind it** — `grep -c manifest tests/test_dispatch.py`
returned 0 — so the concurrency clause had been asserted in a commit message
and nowhere else. The parent measured entry loss in 3 of 6 runs; the director
reproduced it at 8 concurrent dispatches and lost entries in **6 of 6, usually
6-7 of the 8 kids**. Two causes, and the second is the nastier one: the
read-merge-write cycle was not atomic even though its final `rename` was, and
`.manifest.json.tmp` was a *fixed shared name*, so one dispatch renamed the
file out from under another, which then died `FileNotFoundError` **after**
`Popen` had already run. That is a spawned agent nothing tracks — `heal.py`
cannot time it out and `post_wire` cannot wire its node, which is `goal:g7`
failing at the instant of spawn.

The correction was mine as director rather than a kid's, because the diagnosis
was unambiguous and the fix is small: an `flock` around the cycle, a re-read
under that lock so the merge runs against what is on disk *now*, and a unique
`tempfile.mkstemp` name. Six tests now carry the falsifier, including the
concurrent one, and the full suite is green at 1221.

**Recording the lesson rather than only the fix, because it is the same lesson
this goal was minted for.** `goal:s27` was verified at the wrong level, and
this goal's own THOUGHT says so. Its fix was then verified at the wrong level
in turn — read line by line and believed, in a commit that asserted atomicity
the code did not have. Both times the missing step was running the thing under
the conditions it claimed to survive. The parent's `struggles:` line is what
surfaced it again, which is the fourth time this session's field note has held.

Kept `active` until all three clauses passed, then `complete` — not when the
code looked right.
<!-- THOUGHT:END -->