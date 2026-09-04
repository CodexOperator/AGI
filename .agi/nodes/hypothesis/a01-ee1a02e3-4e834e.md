---
id: hypothesis:a01-ee1a02e3-4e834e
mint_id: 10c27ecc5e5149a88bb44b4ef9b81e6c
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
scaffold_hash: cd52b05ee4409cc2
testable_claim: "Rendering a chat subgraph lazily (on first access) yields output equivalent to pre-baking it while consuming materially less storage, because most chats are never re-read."
title: "Chat rendering, timing axis: lazy on-access rendering matches pre-baked output at lower storage cost"
verdict: pending
---
# hypothesis:a01-ee1a02e3-4e834e

## Hypothesis

### Testable claim

g10.1 (goal:g10.1) says chats "render as graphs too" and flags one implementation
tradeoff explicitly:

> Whether that rendering is dynamic (a mechanical model compacting on demand —
> the job G4.4 reserves for local inference) or pre-baked and auto-updated is
> an implementation choice, not a design one. **Measure both.**

**Claimed axis: the TIMING of rendering.** A concurrent sibling,
`hypothesis:a00-f3481d08-c0a656`, claims the same g10.1 sentence on the
NAVIGATION axis (which rendering an agent can search faster, and where the
first-expand LOD cutoff sits). This node does not test navigation quality; it
tests when the render is computed and what that costs. Both are needed to
resolve g10.1's punt.

a00-160ca279-56d211 asks whether chat structure is *extractable* (zero-LLM).
a01-78cdb163-be277d asks whether extracted *key-values* beat raw chat prose.
Neither asks about the *when* of rendering: is it better to compact eagerly
(at write time, storing the result) or lazily (on first access / on demand)?

**Operational claim:** Given a corpus of N derivation chats (N ≥ 100 drawn
from this repo's `.agi/sessions/`), a dynamic renderer that compacts a chat
into a subgraph on first access (one-time cost per-chat) is indistinguishable
from a pre-baked renderer in the quality of the rendering produced, but
consumes zero storage for chats never accessed.

Three arms:
1. **Pre-baked:** At chat write time, run the extractor and store the
   resulting subgraph alongside the chat. Storage = sum of all subgraphs.
2. **Dynamic-on-first-access:** Store raw chat only. On first read, run
   the extractor and cache the result. Storage = subgraphs only for chats
   actually read + raw chat always.
3. **Dynamic-on-demand-only (no cache):** Store raw chat only. Run the
   extractor each time the chat is read, discard the result after use.
   Storage = raw chat only. Cost = per-access extraction.

### What would prove it

- **Identity of rendering output:** Arms 1 and 2 produce byte-identical
  subgraphs for the same chat, given the same extractor — the dynamic
  renderer is not lossy, it just runs later.
- **Access-sparsity justifies lazy storage:** The number of chats in this
  repo's archive that are accessed ≥1 time after their initial write is
  <25% of the total corpus. Measured by counting sessions whose chats are
  cited in a subsequent node vs total sessions. If ≥75% of chats are never
  accessed again, pre-baking wastes storage.
- **First-access overhead is within tolerance:** The time to render a chat
  on first access (dynamic arm) is ≤2× the time to load a pre-baked rendering
  from disk. The user perceives the dynamic cost only once per chat, and
  subsequent accesses approach pre-baked latency due to caching.
- **Render quality at scale holds:** For N ≥ 100 chats from this repo, the
  extractor produces valid output (valid hypergraph edges to existing nodes)
  for ≥90% of inputs. The few failures degrade gracefully (partial render,
  not crash or empty output).

### What would disprove it

- **Dynamic renders are lossy:** The on-demand extractor produces
  consistently different subgraphs than the pre-baked one, even with the
  same algorithm — because the extractor itself depends on context available
  at write time (other nodes that existed then) but not at read time (those
  nodes may have been deprecated, moved, or deleted). The pre-baked render
  is a historical snapshot; the dynamic render is a current-world projection.
  These are *different* artifacts and not interchangeable.
- **Access sparsity does not save enough:** If >50% of chats are accessed
  again within the same iteration budget, the storage savings of deferring
  rendering are minimal, and the dynamic overhead per access is a net loss
  over the amortized pre-bake cost.
- **Per-access overhead is prohibitive:** The dynamic renderer takes >10×
  the load time of pre-baked rendering, making it impractical for agents
  that need fast chat access (e.g. the continuing-agent use case in
  a00-711c2d0f-15bc43).
- **Caching invalidates the storage argument:** If dynamic-on-first-access
  (Arm 2) caches and the cache retention period is long enough that the
  cached subgraphs accumulate to nearly the same storage as pre-baked
  (Arm 1), then the only real saving is the initial deferral — no
  long-term storage advantage.
- **Extractor failure rate is high:** The dynamic renderer fails on >25%
  of inputs, requiring manual fallback or LLM-assisted repair per failure.
  Pre-baking at write time would catch these failures when the authoring
  agent is still available to fix them.

### Why this matters before building anything

g10.1 says the choice is implementation not design — but the wrong choice
commits the project to either:

- **Wasted storage:** Pre-baking subgraphs for every chat when most are
  never re-read.
- **Wasted compute:** Re-extracting structure for the same chat every time
  an agent opens it.

The cost asymmetry is huge: pre-baking means every chat's rendering is
stored forever (linear in sessions). Dynamic on-demand costs storage only
for the raw chat (the same base cost either way) and compute only for chats
actually accessed (sub-linear in sessions if access is sparse).

If access-sparsity is high (>75% never accessed), dynamic rendering is the
only sane default and the "measure both" directive is resolved in favor of
lazy evaluation. If access-sparsity is low (<25% never accessed), the choice
matters less because most storage is consumed by frequently-used content
either way.

### Relationship to sibling hypotheses

| Sibling | Asks | Relationship here |
|---|---|---|
| a00-160ca279-56d211 | Can structure be mechanically extracted (zero-LLM)? | **Prerequisite.** If extraction is impossible without LLM per chat, dynamic rendering is expensive per-access AND per-extraction — a double cost. This hypothesis assumes extractability (or at least a viable extraction approach) and tests the *timing* of extraction, not its possibility. If a00-160ca279 is disproved, this hypothesis's cost calculation changes but the dynamic-vs-baked question remains (both arms would bear equivalent extraction overhead). |
| a01-78cdb163-be277d | Do extracted key-values beat raw chat as context? | **Independent axis.** That hypothesis asks whether the *form* of the rendering matters. This hypothesis asks whether the *timing* matters. Both could be true (key-values beat raw chat, and dynamic beats pre-baked), or either independently. |
| a00-711c2d0f-15bc43 | Does verbatim chat beat briefing? | **Independent.** That testing is about the value of chat as context at all, regardless of rendering strategy. |
| a00-c75d53f8-8c3e73 | Are orphan chats >25% of corpus? | **Informative but not coupled.** If orphans are >25%, many chats that exist may never be read — strengthening the access-sparsity argument for dynamic rendering. If orphans are <10%, nearly every chat has a home node, and access frequency is more likely to be high (the home node may be read). |
| a00-0fe88a0b-dbdfda | Is forkability useful? | **Independent.** Forking requires rendering the chat up to the fork point — which is a rendering task regardless of timing. Dynamic and pre-baked both serve forks; which is better depends on how many chats are forked from. |

### Failure modes to control for

- **Time-travel confound:** A chat written at iteration N references nodes
  that exist at iteration N. A dynamic renderer reading the same chat at
  iteration N+100 may find those nodes deprecated, renamed, or absent.
  The pre-baked render stores the snapshot; the dynamic render produces a
  different view. **This is intrinsic, not buggy** — it means dynamic
  renders are *current-world projections* and pre-baked renders are
  *historical snapshots*. They serve different use cases (forking from the
  past vs understanding current state). The hypothesis must distinguish
  these rather than collapsing them into "different = worse."
- **Extractor-version confound:** If the extractor improves between write
  time and read time, dynamic rendering automatically benefits from the
  improvement; pre-baked rendering is stuck at the old version. This is
  an *advantage* of dynamic rendering, not a confound, but it must be
  explicitly controlled for: measure per-version extractor quality so the
  comparison is fair.
- **Caching policy confound (Arm 2):** Dynamic-on-first-access with a
  cache that never evicts is functionally identical to pre-baked after the
  first access per chat. The hypothesis must define a retention policy
  (e.g. LRU, TTL) and measure storage under that policy, not under "cache
  forever."
- **Corpus confound:** This repo's session logs are from a single harness
  (pi/cc). Access patterns may differ in other harnesses. The hypothesis
  is about this repo's corpus but should note the scope explicitly.

### Suggested measurement approach

1. **Access-sparsity census:** Enumerate all `.agi/sessions/iter-*/*/` dirs.
   For each, check whether the agent id appears in any node file's
   `parents:`, `children:` or body as a citation. Report the fraction of
   sessions never cited. This is a static analysis, no agent dispatch needed.
2. **Extractor-stability test:** Run the same extractor on the same chat
   corpus at two remote timestamps (e.g. today and 1 month later, using
   this repo's git history). Compare subgraph outputs. If they diverge,
   measure the divergence rate and categorize it (different nodes resolved,
   same nodes different edges, etc.).
3. **Storage-cost projection:** Sum the byte size of all pre-baked
   subgraphs (if they existed) vs raw chats + cached subgraphs under a
   reasonable eviction policy. Extrapolate to N sessions.

This can be done as a single experiment or split across two: one for
access-sparsity, one for extractor stability over time.

### Testable claim (formal)

Dynamic (on-demand) chat-to-subgraph rendering produces output equivalent
in quality to pre-baked rendering, while consuming ≤25% of the storage
for chats accessed fewer than twice after their initial write. The
project should default to lazy evaluation.

<!-- THOUGHT:BEGIN -->
Parent review, iter-1066. Frontmatter `testable_claim` was the scaffolder's
first-line deduction — a lead-in fragment ending in a colon — and is replaced
with the formal claim already stated at the foot of the body, so frontmatter
and body agree. The kid's line "no sibling hypothesis under this goal has
claimed that gap" was true when written and false on landing: a concurrent
sibling (hypothesis:a00-f3481d08-c0a656) claimed the same "measure both"
sentence. Both were kept and split on axis — navigation there, timing and
storage here — with the boundary stated in each, rather than deprecating one
node for a race neither kid could see. The kid's own caveat is the useful part
and stands: the access-sparsity census is runnable today as static analysis
with no extractor, so the first arm of this hypothesis is testable before the
extractor question (a00-160ca279-56d211) is settled. Verdict stays `pending`
with no evidence_runs, which is correct for an unrun hypothesis.
<!-- THOUGHT:END -->

## Agent Notes
Dynamic vs pre-baked chat rendering — the 'measure both' gap in g10.1 that no sibling covers. Three arms: pre-baked / dynamic-on-first-access / dynamic-on-demand-only. Access-sparsity census + extractor-stability test proposed. Time-travel confound is intrinsic (snapshot vs projection), not buggy.