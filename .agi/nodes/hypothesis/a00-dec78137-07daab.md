---
id: hypothesis:a00-dec78137-07daab
mint_id: 64b7726c5563437abb43bc9016f2f0d9
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
scaffold_hash: d7a20d06113e3193
title: "Concurrent dispatch needs target diversity to convert throughput into coverage"
testable_claim: "With P concurrent parents targeting the same graph region, at least (P-1)/P kids independently re-derive the same one or two hypotheses, because the subtree visible to each kid at --level small contains the same open questions — clones of each other rather than complementary coverage. Raising spawn.parallel against a single target is a throughput knob, not a coverage knob."
verdict: pending
confidence: 0.0
---

# hypothesis:a00-dec78137-07daab

## Hypothesis

### Testable claim

With P concurrent parents targeting the same graph region at `--level small`, at least (P-1)/P of the spawned kids independently re-derive the same one or two hypotheses. The kids are clones of each other, not complementary coverage — each reads the same 2-hop subtree, finds the same salient open question, and writes whatever variant of it the model produces independently. Raising `spawn.parallel` against a single target is a throughput knob, not a coverage knob.

Formally: let `D` = number of *distinct* hypothesis claims produced by P kids targeting the same goal node. The baseline is D ≈ 2 for any P ≥ 3, because (a) the most salient open thread attracts most of the kids, (b) a second thread attracts a smaller fraction, and (c) additional threads are rare because the 2-hop subtree has a bounded set of open questions. The number of distinct claims grows with the number of *distinct targets*, not with the number of kids.

### What would prove it

An experiment reproducing the finding from `experiment:the-bound-at-eight-real-agents` at a controlled scale:

1. Dispatch P=6 concurrent kids (one parent tier, no real parent, just kids aimed at the same target) against `goal:g4.8 --level small`.
2. All 6 complete and write hypothesis nodes.
3. Classify each kid's hypothesis by its *claimed mechanism* (the "what would prove it" test), not its title. Count distinct mechanisms among the 6.

**Proved if:**
- Distinct mechanisms D ≤ 2 for P=6 (6 kids produce at most 2 distinct claims) — replicating the `experiment:the-bound-at-eight-real-agents` finding that 6 of 8 wrote the same clause-4 hypothesis.
- A control run: dispatch P=6 kids, each targeting a *different* goal node (`goal:g4.1`, `goal:g4.2`, `goal:g4.3`, `goal:g4.5`, `goal:g4.6`, `goal:g4.7`) at the same concurrency, produces D=6 distinct hypotheses — proving the bottleneck is target scope, not model capability.
- The ratio D/P for single-target runs converges to a constant well below 1.0 as P increases (e.g., D≈2 for P=8, D≈3 for P=16), while P artificially grows only the redundancy.

### What would disprove it

- D = P at P≥3 for single-target dispatch — each kid finds a genuinely distinct open question in the same 2-hop subtree (highly unlikely given bounded subtree size, but disproves the claim).
- D grows linearly with P (D ≈ P/2 or better) — the subtree has more orthogonal threads than the experiment at 8 observed.
- The control run (distinct targets) produces D < P — the model cannot produce distinct hypotheses even when given distinct targets, disproving the "it's the target, not the model" part.
- A single target with a large subtree (e.g., `--level full` instead of `--level small`) produces D ≈ P — the bottleneck is not the target per se but the zoom level restricting the field of view.

### What this hypothesis is NOT

It is **not** a claim that concurrency is useless at single-target — throughput still matters for building confidence in one result (reproducibility, statistical verification). It is a claim about **coverage**: that the marginal value of the Nth kid targeting the same region approaches zero in *novel content* terms. The economic argument for g4.8 ("functional output per token") requires coverage, not just throughput, because duplicate hypotheses produce duplicate tokens without duplicate function.

### Relation to g4.8

This hypothesis tests a **prerequisite** for two of g4.8's falsifier clauses, rather than any single clause directly:

- **Clause 4 (delegator sub-linear spend):** If P concurrent loops targeting the same region produce ~2 distinct outputs, the delegator's token cost to review those 2 outputs is constant regardless of P — which *looks* like sub-linear scaling but is actually wasted throughput. The hypothesis makes explicit that sub-linear delegator spend relative to loops is the *wrong metric* if the loops produce clones. The right metric is sub-linear spend relative to **novel content**, which requires target diversity.

- **Clause 1 (no kid node collisions):** This hypothesis establishes that collisions are structurally avoided (mint_id paths, `a03`'s claim) while also establishing that *the content isn't worth colliding over anyway* — most kids at the same target are duplicates.

- **The `superlinear-threat`:** The worst case for g4.8's objective function is when P loops produce D and D grows slower than P: token spend grows linearly (P×cost_per_kid) while functional output converges to constant (D ≈ 2). This degrades the ratio, and the hypothesis names the mechanism.

### How it differs from existing siblings

| Existing hypothesis | Claim | Overlap |
|---|---|---|
| `a03-280a21b7-6d6841` | mint_id paths prevent file collisions | No overlap — that is about *files*, this is about *content* |
| `a00-07b2223d-b21977` | Parent review gate demotes unevidenced | No overlap — that is about *review*, this is about *what is worth reviewing* |
| `a05-bc3ad321-131bbc` | Same clause-3 claim, different framing | No overlap — this hypothesis is about a *coverage prerequisite* all clauses depend on |
| `a00-003fffb0-388249` and four siblings | Clause 4 delegator sub-linear spend | **Complementary** — those claim sub-linear spend *is achievable*; this claims the prerequisite for it to buy anything |

The closest relation is to the clause-4 hypotheses: they assume that an Nth parent produces Nth-distinct outputs worth compressing into an Nth report. This hypothesis challenges that assumption directly: without target diversity, the Nth parent produces a clone of the first parent, and compressing a clone does not increase functional output.

### Control design rationale

The control — distinct targets producing distinct kids — is the critical part. Without it, a finding of D ≈ 2 at single target is ambiguous: it could mean kids are incapable of diversity (a model limitation) or that the single target provides only 2 open threads. The control distinguishes these: if 6 distinct targets produce 6 distinct hypotheses, the bottleneck is the target scope, and the fix is target diversity in the parent brief. If the control also produces few distinct hypotheses, the bottleneck is the kid model itself, which is a harder fix and a different conclusion.

## Agent Notes
Hypothesis: concurrent dispatch against single target produces clones not coverage — inspired by 6/8 duplicate finding in experiment:the-bound-at-eight-real-agents. Target diversity is prerequisite for g4.8 objective function. Fresh angle not covered by 5 existing clause-4 siblings
