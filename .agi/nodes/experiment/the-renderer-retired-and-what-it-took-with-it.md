---
id: experiment:the-renderer-retired-and-what-it-took-with-it
mint_id: bbb96f0d46d247d8895b68aee22b7ce8
type: experiment
parents:
  - hypothesis:the-briefing-is-the-missing-half
next_edges: []
confidence: 0.9
edited_by: director
evidence_runs: 1
scaffold_hash: 5de2d0901f862a85
thought_session: L1.07
title: render-context.py retired — and the two invariants that came off with it, both silently
verdict: proved
---
# experiment:the-renderer-retired-and-what-it-took-with-it

## Experiment

Replace `render-context.py` with `bin/inject.py`, which composes
`briefing.to_markdown()` over `viewport.frame_stream` — so the map a session is
handed *is* what `viewport.py --emit llm` shows. Retire the node, delete the
payload, and see what breaks.

**The extraction in L1.04 is what made this a deletion rather than a
migration.** The nine briefing sections were already out; this only swapped
which renderer draws the tree beneath them.

## Evidence

### It works, both callers

`driver.sh --smoke` and `hooks/cc-session-start.sh` both rebuild the map
through `inject.py`. Deleting `INJECTION.md` and re-running regenerates it.
`viewport --verify` PASS, `goals-check` 111 goals byte-identical, 937 active +
8 deprecated = 945, **node count did not drop**.

### 🔴 Regression 1: the map started showing retired nodes

`render-context.py` wrapped its graph in `_LiveOnly` before rendering, so the
injected map lost deprecated nodes (`goal:s23`). **The filter did not come
across with the rewrite.**

It looked fine. `grep -c bin-render-context INJECTION.md` → `0`. That was
**luck**: the one retired build node sat outside depth 3 of any root. Anchoring
on its parent showed it immediately:

```
$ viewport --emit llm --anchor idea:engine-render-context --depth 2
- `idea:engine-render-context` (idea) Engine surface: …render-context.py
  - `build:bin-render-context` (build) Build: …render-context.py     <- retired
```

`goal:s23` exists because an agent handed a retired node as a live chain head
will extend it. Fixed with `frame_stream(hide_deprecated=)`, and the subtree
goes with the node — a live node reachable only through a retired parent is
not a live head either.

**The two readers genuinely want opposite things here**, which is why it is a
flag and not a default. `viewport.py`'s own contract is to render damage
rather than a flattering picture, and deprecated mass is part of that picture.
The *injected* map must hide what an agent must not extend. Both now hold, and
a test asserts each direction.

### 🔴 Regression 2: `broken_links` had never met a retired payload

Deprecating a build node and deleting its file is the **documented end state
of retirement** — and it drove `broken_links` from 0 to 1, permanently. A
standing invariant would have gone red for doing the right thing.

It cannot be edited away either: `[build]` **requires** `payload_ref`, so the
write gate correctly refused to remove it from the deprecated node. The field
has to keep naming a path that is deliberately gone.

```
rejected: build:bin-render-context — build requires payload_ref;
          an update may not REMOVE a required field
```

The convention and the metric had simply never met, because **no build node
had ever been retired before.** Resolved by making damage mean *a broken link
on a live node*, with retired payloads counted and printed separately rather
than excluded silently:

```
links: 942 resolved, 0 broken (1 retired payload(s), not damage)
  retired build:bin-render-context -> …/render-context.py (deprecated; bytes in the grid ref)
```

### Recovery, checked rather than asserted

The thought block first claimed *every* version is recoverable. It is not:

```
v13 OK 268 lines   v12 OK 337   v11/v10 OK 323   v8 OK 276   v5 OK 279
v1  ERR: no payload recorded  — predates payload recording
```

Corrected in the node to "every version since payload recording began".

### Two more silent zeros, caught before the swap

`briefing.py` was written against `load_directory`'s graph and then used with
`zoom._load_wired_graph`'s, and **the two disagree about where adjacency
lives** — the first answers `edges_from`, the second builds no `Edge` objects
at all and hangs `children` on the nodes. Result:

- `edges: 0` on a graph with 869 of them;
- **every idea reported `0 descendants`**, so the attractor list — what an
  agent reads to choose a target — came out all zeros in alphabetical order
  and looked like a plausible ranking.

Neither raised. Both fixed by making the walk representation-agnostic;
attractors now match `render-context.py`'s ranking exactly
(`idea:domain-graph-core :: 68` at the head).

### Tests: retargeted, not deleted

8 failures, all from the deleted file. Every one was a property of the *map*,
not of the renderer — so `test_render_context.py` became `test_inject.py`
unchanged but for its target, and the `goal:s23` guard now follows the
invariant to `frame_stream(hide_deprecated=)`. `1352 → 1357`.

## What is NOT proved

- **"Four of five render paths deleted" was optimistic and did not happen.**
  One did. `renderers/ascii` is orphaned from production but keeps its own
  tests; `zoom.py`'s internal renderers are untouched, because they build
  *kid* context and moving those changes what every spawned agent receives.
  Five paths → four.
- **No agent has been spawned against an `inject.py`-generated map.** Parity
  is proved by comparison and by tests, not by an agent working from it.
- **The `nodes:` count still includes deprecated nodes** (945 vs 937 live).
  That is unchanged from `render-context.py`, which applied `_LiveOnly` only
  to the tree and never to `by_type` — pre-existing, not introduced, and left
  alone deliberately rather than fixed in the same change.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Both regressions here share one shape and it is the shape worth remembering: a rewrite carried the *visible* behaviour across and dropped an invariant that was implemented somewhere other than where it was stated. `_LiveOnly` was a class in a file being deleted, so `goal:s23` went with the file. `broken_links == 0` was a metric that had simply never been run against a retired build node, because there had never been one.

The first was found by testing the mechanism instead of the output. `grep -c` on the generated map said 0 and I nearly took it — the honest check was to anchor the viewport at the retired node's parent and look, which took one command and turned a green into a red. A verification that passes because of where the data happened to sit is not a verification, and this session has now produced three of those (the command-subcommand guard, the `_verify` backtick match, and this).

Scope is recorded honestly against my own plan: I wrote "delete 4 of 5 render paths" into the iteration plan and delivered one. The other three are load-bearing in ways I had not checked when I wrote the number, and `zoom.py`'s in particular changes every kid's context, which deserves its own falsifier rather than being swept into a cleanup.
<!-- THOUGHT:END -->