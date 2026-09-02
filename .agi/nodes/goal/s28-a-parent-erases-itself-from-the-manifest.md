---
confidence: 1.0
goal_id: S28
goal_kind: short-term
heading_level: 2
id: "goal:s28"
mint_id: c43a2514d4a843339de9e0f4244232a3
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S28: A parent erases itself from the iteration manifest by spawning a kid"
type: goal
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
Minted the moment it was found, because it invalidates part of what the same
session had just shipped and that is worth recording immediately rather than
discovering later. `goal:s27`'s design is right and its code is right; one of
its five changes is dead on arrival for a reason none of the five could have
anticipated.

The honest framing is that `goal:s27` was verified at the wrong level. Its
falsifier's first two clauses were checked in tests and in a live run and both
hold -- no scaffold, nothing authored, no metric artefact. The completion half
was checked by reading `agent.json` and finding `owns` correctly written. What
was never checked is whether anything downstream READS it, which is exactly the
lesson this repo already paid for once: `post_wire`'s docstring claimed for
months that it "reads all agent.json records" while the loop never did.
Believing a field is consumed because it is written is the same mistake, and I
made it four hours after writing the commit message about it.

Filed `active` rather than `horizon`: it is a live defect in a path shipped
today, and the parent tier does not honestly work until it is fixed.
<!-- THOUGHT:END -->
