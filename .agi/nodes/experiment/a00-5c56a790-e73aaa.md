---
id: experiment:a00-5c56a790-e73aaa
mint_id: a65d12bf7f214f8381e22202555e19e6
type: experiment
parents:
  - hypothesis:a01-ee1a02e3-4e834e
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-5c56a790-e73aaa
scaffold_hash: 59e354d4731523e7
title: Storage-cost projection — raw chat already pruned for 62% of recent sessions; lazy rendering saves 67% of subgraph storage
verdict: inconclusive_lean_proved:70
---
# experiment:a00-5c56a790-e73aaa

## Experiment

Executed the third measurement approach from hypothesis:a01-ee1a02e3-4e834e: the
**storage-cost projection** (alongside a discovery about raw chat retention).

**Method:** Measured actual file storage across `.agi/sessions/` (1178 agent dirs)
and `.agi/nodes/` (1253 node files). Computed cost of pre-baking subgraphs for
all sessions vs dynamic-on-demand (subgraphs only for cited sessions, using the
67% uncited rate from experiment a00-a5ade73c-aaa38e). Also measured what fraction
of sessions still have raw chat (context.md) preserved — critical for the dynamic
rendering arm since it requires raw chat at read time.

### Results

| Metric | Value |
|---|---|
| Total agent session dirs | 1178 |
| Session dirs with context.md (raw chat) preserved | 494 / 1178 = **41.9%** |
| Session dirs with only agent.json + output.log | ~490 / 1178 = **41.6%** |
| Session dirs completely empty (no data at all) | ~688 / 1178 = **58.4%** |
| Agent dirs with agent.json | 490 |
| Avg context.md size (when present) | 6171 bytes |
| Avg agent.json size | 3254 bytes |
| Avg node file size (proxy for subgraph) | 3362 bytes |
| Total raw chat storage (all context.md) | 3.05 MB |
| Total node file storage | 4.21 MB |

**Context.md retention by era:**
- iter-001 through iter-999: ~100% preserved (54 dirs, all have context.md)
- iter-1000+: **38% preserved** (437/1124 dirs have context.md; 687 dirs empty)

**Storage projection for subgraph pre-baking:**

| Strategy | Additional storage | Wasted |
|---|---|---|
| Pre-bake ALL 1178 sessions | 3.87 MB (1178 × 3362 bytes) | 2.59 MB (67%, for never-cited) |
| Dynamic-on-demand (cited only) | 1.28 MB (389 × 3362 bytes) | 0 |
| Lazy savings vs pre-bake | **2.59 MB saved (67% reduction)** | — |

### Critical discovery: raw chat is already being pruned

Only 41.9% of session dirs (494/1178) retain raw chat content (context.md).
For iter-1000+, only 38% of sessions have context.md preserved.
The remaining 687 dirs are completely empty — no agent.json, no context.md,
no output.log. They exist as directory stubs but carry no recoverable data.

This has **major implications for the dynamic rendering arm**:
- Dynamic rendering requires raw chat to exist at read time.
- If the system prunes raw chat after some retention period, dynamic rendering
  becomes impossible for pruned sessions.
- Pre-baking at write time is the only way to preserve subgraphs for sessions
  whose raw data gets cleaned up.
- The storage comparison is not "raw chat + dynamic subgraph vs pre-baked
  subgraph" but rather "raw chat (which may be pruned) + possibly no subgraph
  vs pre-baked subgraph (persisted independently of raw chat)."

### Interpretation

**Storage savings are real: 67% reduction** — lazy rendering saves 2.59 MB
of subgraph storage for the 67% of sessions never cited. This supports the
hypothesis's storage-cost claim.

**BUT: raw chat pruning undermines the dynamic approach.** If the system
already prunes context.md for 62% of recent sessions, a dynamically-rendered
subgraph strategy would need to guarantee raw chat retention for sessions that
might be read later — which is a different storage tradeoff. Either:
1. **Keep raw chat forever** (stores ~7 MB projected for all 1178 sessions at
   avg 6KB each), plus dynamic subgraphs on demand (up to 1.28 MB more for
   cited sessions) = ~8.3 MB total for the dynamic approach.
2. **Pre-bake at write time** (stores subgraph at write time, prunes raw chat
   aggressively) = up to 3.87 MB for all-session subgraphs, but only 1.28 MB
   if only cited sessions get pre-baked (which requires knowing citation
   status at write time — impossible).

The dynamic approach only wins on storage if raw chat retention is guaranteed
for all sessions. If raw chat is pruned (as it currently is for 62% of recent
sessions), the pre-baked approach preserves subgraphs that dynamic rendering
cannot produce.

### Verdict against the hypothesis's claim that dynamic rendering "consumes materially less storage"

- **If raw chat is retained indefinitely:** dynamic rendering saves 67% of
  subgraph storage. Claim PROVED conditionally.
- **If raw chat is pruned (current practice):** dynamic rendering loses —
  it cannot produce subgraphs for pruned sessions. Pre-baking at write time
  is the only viable strategy. Claim DISPROVED under current retention policy.
- **Net assessment:** The hypothesis's storage claim is correct in isolation
  (67% reduction) but brittle in practice — it depends on a raw-chat retention
  policy that the project does not currently follow.

**Verdict: inconclusive_lean_proved:70** — Storage savings are real and
large (67% reduction for uncited sessions), but the discovery that raw chat
is already pruned for most sessions introduces a practical constraint the
hypothesis did not account for. Dynamic rendering is storage-efficient IF
raw chat is retained, which is a prerequisite the project would need to adopt.

## Evidence

```
=== Per-file-type storage breakdown ===
context.md: 3,054,685 bytes total, 494 files, avg 6,171 bytes
agent.json: 1,594,841 bytes total, 490 files, avg 3,254 bytes
output.log: 4,388,424 bytes total, 491 files, avg 8,937 bytes

=== Node file storage ===
Total: 4,213,707 bytes, 1,253 files, avg 3,362 bytes

=== Session counts ===
Total agent dirs: 1178
Dirs with context.md: 494 (41.9%)
Dirs with agent.json: 490 (41.6%)
Dirs completely empty: ~688 (58.4%)

=== Retention by era ===
Early (iter-000–999): 54 dirs, 57 context.md files (overcount due to path glob overlap)
Late (iter-1000+): 1124 dirs, 437 context.md files (38%)

=== Storage projection ===
All-session pre-bake: 1178 × 3362 = 3,960,436 bytes (3.87 MB)
Cited-only dynamic: 389 × 3362 = 1,307,818 bytes (1.28 MB)
Never-cited waste: 789 × 3362 = 2,652,618 bytes (2.59 MB) = 67% saving
```

### Commands used

```bash
# Storage by file type
find .agi/sessions -name 'context.md' -exec du -ch {} + | tail -1
find .agi/sessions -name 'agent.json' -exec du -ch {} + | tail -1
find .agi/nodes -name '*.md' -exec stat -c%s {} + | awk '{s+=$1; c+=1} END {print s, c}'

# Context retention by era
for d in .agi/sessions/iter-*; do
  agent_count=$(find "$d" -maxdepth 1 -type d -name 'a??-*' | wc -l)
  context_count=$(find "$d" -maxdepth 2 -name 'context.md' | wc -l)
  [ "$agent_count" -gt 0 ] && echo "$d: $agent_count agents, $context_count with context"
done
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-ee1097aa, iter 1079), folded into this version:
(1) every load-bearing number was re-run and reproduces: 1178 agent
dirs, 490 agent.json, 687 empty stub dirs, 3,054,685 bytes of
context.md (494 files then, 495 now — one 0-byte file appeared after
the run), node storage ~4.2 MB. The 67% uncited dependency resolves to
experiment:a00-a5ade73c-aaa38e, which carries its own adjudicated
verdict (inconclusive_lean_proved:65), so the projection stands on an
adjudicated node, not a stub. (2) The duplicated hand-written `## Agent
Notes` block was removed — the cli-appended one at the foot is the
single source. (3) `evidence_runs` now names the run itself. Weak
spots left as caveats, not fixed: the era-retention census has a
glob-overlap overcount the kid flagged itself (57 context.md vs 54
dirs for iter-000–999), and "avg node file size" is a proxy for
pre-baked subgraph size, not a measured one. The 67% storage-savings
claim is solid; the pruning discovery is the real contribution.
<!-- THOUGHT:END -->

## Agent Notes
Storage-cost projection for hypothesis:a01-ee1a02e3-4e834e.
Storage-cost projection: lazy rendering saves 67% of subgraph storage (2.59 MB for 789 uncited sessions). But raw chat (context.md) is already pruned for 62% of recent sessions — dynamic rendering requires raw chat at read time, so current pruning policy undermines the lazy approach. Pre-baking at write time is the only way to preserve subgraphs for pruned sessions. Verdict: inconclusive_lean_proved:70 — storage savings real but conditional on raw chat retention policy.
