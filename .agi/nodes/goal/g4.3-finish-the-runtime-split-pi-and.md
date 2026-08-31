---
confidence: 1.0
goal_id: G4.3
goal_kind: subgoal
heading_level: 3
id: "goal:g4.3"
mint_id: 486acf4bc70c403aa16c9d1efdcb8107
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G4.3: Finish the runtime split: pi and Claude Code as one path"
type: goal
---

**L12** remainder plus **H9**. Anywhere the engine invokes `pi`, allow invoking
Claude Code instead — a runtime flag, not a parallel code path — and audit hook
parity between the two. H9's kid→parent question channel exists for the CC path
(four escalation triggers, one question per kid) and not for pi.

Two halves of the split are now asymmetric in a way worth naming. The pi half
is real and was verified live on 2026-08-31: `driver.sh --max-iters 1`
dispatches, kids write nodes, `heal.py` closes them out, `post_wire` wires the
edges. The CC half is configuration with nothing behind it.

## The CC dispatcher — two spawn modes, models per tier

**Added 2026-08-31, on finding that `cc_dispatch` has no dispatcher behind it.**
`agent_dispatch.*` becomes real pi flags; `cc_dispatch.kid_model` and
`parent_model` are read by nothing. Claude Code's own subagent tool spawns
Claude models only, so a project cannot reach a non-Claude provider from the CC
side by configuration — it needs code. What that code must do:

1. **Spawn kids directly.** Dispatcher → N kids, one node each, exactly the
   shape `dispatch.py` produces for pi. This is the cheap mode and the one
   that must work first.
2. **Spawn parents, which then spawn their own kids.** A parent owns one loop:
   picks targets, spawns kids, reviews their nodes, enforces the evidence
   gate, reports. Kids do not become parents; the tier is assigned at spawn.
   This is what keeps review motion out of the delegating session, and it is
   the reason the three tiers exist at all.
3. **A model per tier, independently set.** `parent_model` and `kid_model` are
   already in the config and already mean this — they simply have no reader.
   Both modes honour them: mode 1 uses `kid_model` only; mode 2 uses
   `parent_model` for the parents it spawns and `kid_model` for whatever they
   spawn beneath. A parent must not silently inherit the kid model, and a kid
   must not silently inherit the parent's — tiering the model is the whole
   point of having tiers.
4. **Provider-agnostic, and that means an SDK.** Reaching OpenRouter from
   here is `goal:g1.8` item 4, and the decision recorded there stands: **use
   the OpenRouter Python SDK, not raw HTTP**, so a minor change on their side
   cannot silently break the loop. Claude models keep going through the
   subscription; the main chat is never routed anywhere else.

The invariant this must not break: **a runtime flag, not a parallel code
path.** Target selection, the spawn gate, the evidence gate, `post_wire` and
the node format are the same for both runtimes. If the CC dispatcher grows its
own copy of any of them, this goal has failed even if the dispatcher works.

## H4b — traced 2026-08-31, and the diagnosis was half wrong

`driver.sh` called `benchmark.py "$PROJECT_ROOT" ... || true`. The argument was
indeed wrong — `benchmark.py` takes a positional **chain id** (`idea:foo`) and
was handed a directory — but it never got that far: the module `sys.exit(1)`s
at import when `ollama` is missing, which it is, and `|| true` swallowed it.
Confirmed live: one `ERR: ollama package not installed` line, every run, for
however long that call has been there.

**The consequence is real.** `benchmark.py` writes `closed_chains.txt`, and
`dispatch.py` reads it to stop re-picking a chain it has already judged
finished. Nothing has ever written that file, so no chain has ever been closed
and target selection has drawn from the full set every iteration.

**The claim that it reaches `ranking.py` is false.** That module is reached
through `chain_engine/queries.py`; `benchmark.py` does not import it. So the
weighted attractiveness path is not implicated — the scoring `dispatch.py`
actually uses is its own, in `_pick_targets`, and that does run.

The call is removed rather than repaired: re-enabling wants a per-chain loop, a
config gate and the dependency present, which is a design job.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 was two paragraphs of intent written before either runtime had been watched
end to end. This version is written after watching one: two live
`--max-iters 1` runs on 2026-08-31, which is also how every claim added here
was checked rather than reasoned about.

The CC-dispatcher section is here rather than under `goal:g1.8` because the
owner's requirement — spawn kids directly, *and* spawn parents that spawn their
own kids, each tier on its own model — is a statement about the runtime split,
not about credentials. G1.8 only ever owned the question "how does the key get
there". Splitting it that way costs a cross-reference and buys a goal that
still means one thing.

The H4b rewrite is the part worth flagging to a future reader: the previous
text named a consequence that traced false. `benchmark.py` does not import
`ranking.py`, so the attractiveness path was never implicated — the real
casualty is `closed_chains.txt`, which has never been written, so no chain has
ever been closed. Both the old claim and the new one were cheap to check and
only one of them was checked. That is the lesson, and it is the same one this
repo keeps re-learning: anchor the claim before believing it.
<!-- THOUGHT:END -->
