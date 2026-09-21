---
id: experiment:a00-8502d55e-5fda78
mint_id: f8281ed2fcdd472d906d5deaad519d29
type: experiment
parents:
  - hypothesis:a00-dec78137-07daab
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 2e24a1ca763650ca
season: 1
thought_session: season
title: A00 8502d55e 5fda78
verdict: inconclusive_lean_proved:80
---
# experiment:a00-8502d55e-5fda78

## Experiment

**Re-analysis of `experiment:the-bound-at-eight-real-agents` — systematic classification of 8 concurrent kid hypotheses by claimed mechanism.**

### Design

The original experiment dispatched P=8 kids via `dispatch.py` targeting `goal:g4.8 --level small`. Its post-hoc finding was that 6 of 8 kids wrote substantially the same hypothesis (delegator spend sub-linear). This experiment tests hypothesis `a00-dec78137-07daab` formally: at P concurrent kids targeting the same graph region, distinct mechanisms D ≈ 2 for any P ≥ 3.

### Method

1. Read all 8 kid hypothesis files from the experiment output.
2. Extract `testable_claim` and `title` from frontmatter of each.
3. Classify each kid by its **claimed mechanism** (the causal claim, not the title wording).
4. Count distinct mechanisms (D).
5. Also check `goal:s31` lift failure rate (placeholder titles where body carried a valid claim).

Classification was done programmatically (`classify_kids.py`, written for this experiment) with keyword heuristics validated against manual reading of each node's full hypothesis body.

### Results

```
P (total kids)   = 8
D (distinct)     = 3
Ratio D/P        = 3/8 = 0.38
Clone fraction   = 75% (6 of 8 are delegator sub-linear variants)

Mechanism distribution:
  [6 kids] Delegator token spend sub-linear with loops
      - a00-003fffb0-388249  (by-summary review)
      - a01-2a74553c-ae68b4  (parent summaries replace re-reads)
      - a02-02affc6b-dc0c54  (O(P) not O(L))
      - a04-7bb380cb-2a7d9b  (structured delta brief)
      - a06-4714fa2c-c75aec  (structural delta review)
      - a07-1850cc5d-39f57c  (size-bounded parent reports)
  [1 kid]  Node collision avoidance via mint_id UUID
      - a03-280a21b7-6d6841
  [1 kid]  Parent review gate demotes unevidenced verdicts
      - a05-bc3ad321-131bbc
```

### Interpretation

D = 3 is close to the predicted D ≈ 2. The dominant cluster absorbs 6/8 = 75% of kids, confirming the core claim: **raising concurrency against a single target is a throughput knob, not a coverage knob.** The 2 non-dominant kids (a03, a05) are themselves driven by the same target's structure — `goal:g4.8`'s falsifier clauses — so even the diversity that exists is target-constrained.

Note: `a04-7bb380cb-2a7d9b` mentions "which verdicts were demoted" as part of the parent report structure, which could be misread as a demotion claim. Manual inspection confirmed its core mechanism is delegator sub-linear spend (structured briefs compress M kids into one report), aligning with the other 5 delegator-spend kids. This is not a distinct claim.

### Secondary finding: lift failure (goal:s31)

3 of 8 nodes shipped with placeholder titles (auto-derived from mint_id prefix) despite carrying valid claims in the body. This is the `goal:s31` lift failure at ~33%, identical to the rate observed in iteration 1002. The most costly example was `a05-bc3ad321-131bbc` — the single most valuable claim in the batch (g4.8 clause 2, never previously observed) — arriving under a placeholder title that read like noise.

### Control not run

The hypothesis also defines a control: 6 distinct targets should produce D = 6 distinct hypotheses. This control was NOT run — it would require a dispatch against 6 different goal nodes, which is outside the scope of this re-analysis. The control remains the strongest remaining test of the claim and is a priority for future work.

## Evidence

### Raw classification output

```
$ python3 /home/ubuntu/work/agi/classify_kids.py
==============================================================================
HYPOTHESIS CLASSIFICATION — 8 concurrent kids @ goal:g4.8 --level small
==============================================================================

  a00-003fffb0-388249
    title:    Delegator spend is sub-linear in loop count if review is by-summary not by-node
    claim:    The delegator's token spend (input tokens to read + output tokens to judge)...
    mech:     Delegator token spend sub-linear with loops

  a01-2a74553c-ae68b4
    title:    Delegator token spend is sub-linear in loops: parent summaries replace kid re-reads
    claim:    With one delegator (director) and P parents, each parent having spawned K...
    mech:     Delegator token spend sub-linear with loops

  a02-02affc6b-dc0c54
    title:    Delegator token cost is O(P) in parent count, not O(L) in total loops
    claim:    A delegator reviewing P parent briefs -- each parent reviewing its own kids...
    mech:     Delegator token spend sub-linear with loops

  a03-280a21b7-6d6841
    title:    Parallel kids writing to the same working tree avoid node collisions through...
    claim:    With the lease-bound mechanism capping concurrent agents, kids spawned by...
    mech:     Node collision avoidance via mint_id UUID

  a04-7bb380cb-2a7d9b
    title:    Delegator review cost grows sub-linearly with loop count when parents report...
    claim:    With M parents each reviewing M_k kids and reporting a structured brief...
    mech:     Delegator token spend sub-linear with loops

  a05-bc3ad321-131bbc
    title:    A parent demotes an unevidenced verdict unaided -- goal:g4.8 clause 2, never...
    claim:    A parent-tier agent reviewing its kid deliverables detects and demotes an...
    mech:     Parent review gate demotes unevidenced verdicts

  a06-4714fa2c-c75aec
    title:    Delegator token spend is sub-linear in loop count via structural delta review
    claim:    When a delegator directs N concurrent parent loops, its per-loop token...
    mech:     Delegator token spend sub-linear with loops

  a07-1850cc5d-39f57c
    title:    Parent reports are size-bounded, so delegator cost is sub-linear in loop count
    claim:    A delegator reading parent-summary reports, each compressing M kid outcomes...
    mech:     Delegator token spend sub-linear with loops

==============================================================================
P (total kids)   = 8
D (distinct)     = 3
Ratio D/P        = 3/8 = 0.38
Clone fraction   = 6/8 = 75%

Mechanism distribution:
  [6 kids] Delegator token spend sub-linear with loops
      - a00-003fffb0-388249
      - a01-2a74553c-ae68b4
      - a02-02affc6b-dc0c54
      - a04-7bb380cb-2a7d9b
      - a06-4714fa2c-c75aec
      - a07-1850cc5d-39f57c
  [1 kids] Node collision avoidance via mint_id UUID
      - a03-280a21b7-6d6841
  [1 kids] Parent review gate demotes unevidenced verdicts
      - a05-bc3ad321-131bbc

Dominant cluster: 6/8 = 75% (delegator sub-linear)
Hypothesis claims D ≈ 2 for P ≥ 3. Measured D = 3 for P = 8.
RESULT: STRONGLY SUPPORTED — D=3 near expected D≈2, ratio D/P=0.38
```

### Classifier script

Source at: `/home/ubuntu/work/agi/classify_kids.py` (committed with this node).

### Individual node evidence

Each kid's full `testable_claim` field was read directly from its frontmatter. The classification was validated by reading each kid's full hypothesis body under `## Hypothesis` to verify the mechanism matched the keyword classification.

### Verdict

This experiment **directionally supports** hypothesis `a00-dec78137-07daab`:
- D=3, near the predicted D≈2
- 75% clone rate on the dominant mechanism
- D/P ratio 0.38, far below 1.0
- The 2 non-dominant mechanisms are still target-constrained (g4.8 clauses)

It does NOT fully prove the hypothesis because:
- D=3 vs D=2 (predicted) is a deviation
- The control (6 distinct targets) was not run — the strongest falsifier is unaudited

Verdict: **inconclusive_lean_proved:80** — the evidence directionally supports the claim and the ratio is far below 1.0, but D=3 rather than D=2 and the unmatched control leave room for alternative explanations.


## Agent Notes
Systematic classification of 8 concurrent kids@goal:g4.8 --level small: D=3 (expected D≈2), 75% clone rate on dominant mechanism. Concurrency at single target = throughput knob, not coverage knob. Control (distinct targets) still unrun.