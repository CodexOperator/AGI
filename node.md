---
id: goal:g4.3
mint_id: 486acf4bc70c403aa16c9d1efdcb8107
type: goal
parents:
  - goal:g4
next_edges:
  - hypothesis:a00-652a7e70-1adcde
confidence: 1.0
edited_by: season.py
goal_id: G4.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G4.3: Finish the runtime split: pi and Claude Code as one path"
---

> **⚠ SUPERSEDED IN INTENT by `goal:g4.6` (2026-09-01), and still open as
> stated.** Read that goal before doing work here. This one is framed as *two
> named runtimes reaching parity* — the frame the Claude Code adaptation had
> when it was a stop-gap at the start of the project. Under it, "unify" reads
> as "make the second runtime work like the first", which is why the CC half
> stayed configuration with nothing behind it. `goal:g4.6` keeps this goal's
> invariant verbatim ("a runtime flag, not a parallel code path") and moves the
> seam: **one** spawn path, *N* harnesses declared in config as adapters, with
> pi and Claude Code the first two and neither privileged. The drift is
> recorded rather than edited away because this text steered real work — kids
> aimed at this goal produced CC-framed nodes, correctly, because that is what
> it asks for. Its own remaining items (H4b's `closed_chains.txt`, hook parity,
> H9's question channel) are unaffected and still live here.

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

   **Caveat added 2026-09-01: calling OpenRouter directly means inheriting the
   transcript problem pi currently solves for us.** pi writes a full JSONL
   session log per run to `~/.pi/agent/sessions/`, unasked — that is the only
   record of how a kid reasoned, and this session needed it (a kid wrote
   `bin/completion.py` in full, died on a 403, and its 204 KB transcript was
   the sole account of the design). A raw/SDK harness gets no such log by
   default, so **leaving pi is not purely a simplification; it trades a free
   subsidy for infrastructure we would have to run.**

   What the direct path gains in exchange is the *link* `goal:g2.7` wants.
   OpenRouter accepts a caller-chosen session id in the request body, placed
   last, after `model` and `messages`:

   ```jsonc
   {
     "model": "qwen/qwen3.8-27b",
     "messages": [ /* ... */ ],
     "session_id": "my-session-123"
   }
   ```

   Because we choose that value, it can simply **be the node's mint id**, and
   node-to-chat cross-linking exists by construction rather than by
   bookkeeping — which is strictly better than anything achievable under pi,
   where the session id is generated after launch and never told to the
   engine.

   Retrieving the transcripts is then the open piece: a webhook we host, or one
   of the OpenRouter-compatible observability platforms already available at no
   cost (**Sentry**, **New Relic**). Not chosen, and not urgent — **while the
   loop runs on pi, the logs are already being kept**, which is the concrete
   reason this clause is not blocking.

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
This version adds one thing to clause 4 and it inverts part of that clause's
premise. Reaching OpenRouter directly had been framed as purely a robustness
and provider-agnosticism decision. Running the loop on OpenRouter through pi
all day on 2026-09-01 showed a second, larger axis nobody had priced: pi is
silently providing the session transcripts, and a raw/SDK harness gets none.
That is a cost of leaving, not a benefit — and this session needed those logs
concretely, when a kid wrote `bin/completion.py` in full, died on a provider
403, and its 204 KB transcript was the only surviving account of the design.

The compensating gain is recorded with it because it is not obvious and it is
strictly better than what pi can do: OpenRouter takes a caller-chosen
`session_id` in the request body, so the id can BE the node's mint id and
`goal:g2.7`'s cross-link exists by construction. Under pi the id is minted
after launch and never told to the engine, so that link can only ever be
reconstructed after the fact — which is exactly the mtime forensics this
session had to perform.

Recorded on the goal rather than left in a handoff because it changes what
"provider-agnostic" costs, and the next person to weigh leaving pi should see
both sides on the goal that proposes it.

The prior version's reasoning, kept only in the grid as this block is rewritten
per version: it was written after watching two live `--max-iters 1` runs on
2026-08-31, and placed the CC-dispatcher section here rather than under
`goal:g1.8` because tier-per-model is a statement about the runtime split, not
about credentials.

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