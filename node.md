---
id: hypothesis:a01-35f3a362-28545d
mint_id: f65e97fa5ea944fb8b248101101925c9
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: 6fd506507224ab84
season: 1
thought_session: season
title: Evidence gate resolves existence not type — non-experiment nodes satisfy evidence_runs
verdict: pending
---
# hypothesis:a01-35f3a362-28545d

## Hypothesis

**Claim:** The evidence gate (`apply_gate` / `normalize_evidence_runs`) validates `evidence_runs` entries by node-id **existence** in the corpus only, never by the cited node's **type**. A hypothesis claiming `proved` can cite any existing node — another hypothesis, a verdict, a goal, a build node — and the gate passes, counting it as valid evidence, without a single `experiment` node appearing in the list.

**Why this matters for G3:** G3 says scoring cannot be moved by added motion. The evidence gate is the main structural defence against this (decisive verdicts require evidence). But if `evidence_runs` can be satisfied by ANY node id regardless of type, then the gate does not actually require experiment evidence — it requires a node-id-shaped string that exists in the corpus. The motion of creating a non-experiment node and citing it satisfies the evidence check without running any experiment. The gate claims to check evidence but actually checks only citation existence.

**Motivation (G3 L4 gap):** All 12+ extant attribution hypotheses address which goal an outcome belongs to or how much it is worth. None address that the evidence gate itself is structurally blind to the TYPE of the cited node. Even with perfect goal-attribution scoring, the numerator can be inflated by citing non-experiment nodes as "evidence" — a separate vulnerability at the evidence layer rather than the attribution layer.

### What would prove it (pass condition)

1. **Synthetic test 1 — hypothesis cites a goal:** Construct a hypothesis node file with `verdict: proved` and `evidence_runs: ["goal:g3"]`. Run the exact `apply_gate()` logic that `cli.py done` uses: `corpus = build_corpus(nodes_dir)`, `normalize_evidence_runs(["goal:g3"], corpus=corpus)`. Assert that the count is >= 1 and `GateResult.ok == True` — the gate passes a goal node as evidence.

2. **Synthetic test 2 — hypothesis cites another hypothesis:** Same setup with `evidence_runs: ["hypothesis:a00-ee08875d-df7a60"]`. The other hypothesis node exists in the corpus; the gate passes.

3. **Synthetic test 3 — experiment excluded, gate still passes:** A list `["goal:g3", "build:bin-benchmark", "verdict:fake" (if exists)]` with zero experiment-type entries still produces `normalize_evidence_runs >= 1` because type is never checked. The method `build_corpus` yields ALL node ids irrespective of type, and the only predicate in `normalize_evidence_runs` is `v.strip() in corpus`.

4. **Real corpus audit:** Scan all `proved` hypothesis nodes. Count what fraction of their `evidence_runs` entries resolve to a node whose `type` is NOT `experiment`. If >0% of cited evidence nodes are non-experiment, the gap is real and exploited.

### What would disprove it (fail condition)

1. **`build_corpus` already excludes non-experiment types:** The corpus-building fn filters by type. Reading `build_corpus()` shows it collects ALL node ids regardless of type — no type filter exists.

2. **`normalize_evidence_runs` checks type before counting:** The sum comprehension adds a type predicate not visible in the source — but the code shows `v.strip() in corpus` as the only corpus check.

3. **All `proved` hypotheses in the real corpus cite only experiment nodes:** The corpus audit shows zero non-experiment citations in `evidence_runs`. Even if the gate permits it, no agent has yet exploited it.

4. **The writer path (`cli.py done`) rejects non-experiment evidence at a higher level:** `cli.py done` calls `apply_gate` which delegates to `normalize_evidence_runs` — the only check is corpus membership. No pre-gate type validation exists in the call stack.

### Orthogonality to existing sibling hypotheses under goal:g3

| Hypothesis | Gap tested | Relationship |
|---|---|---|
| a00-cfbdfb1e (cross-goal relevance) | Cited experiment shares no goal-chain with hypothesis | Independent: even with same-goal citation, cited node could be type hypothesis not experiment |
| a00-ee08875d (confidence-weighting) | Binary counting vs confidence-weighted | Independent: no type check, same binary vs weighted problem |
| a00-fc578adb (evidence decay) | Forward-chain connectivity over time | Independent: no type check at creation time |
| a00-94946187 (deprecation gap) | Deprecation inflates ratio | Independent: different attack vector |
| a01-8e09cdf2 (outcome gameability) | Outcomes without attribution | Independent: evidence layer vs outcome layer |
| All attribution hypotheses (a02–a07) | Which goal gets credit | Independent: orthogonal axis — even with perfect attribution, the cited node need not be an experiment |

### Why this hypothesis is not already covered

The existing hypotheses test attribution (which goal), weight (how much confidence), relevance (same goal tree), and decay (time). None test the **type** of the cited evidence node. The evidence gate's `normalize_evidence_runs` uses `build_corpus` which collects ALL real node ids — there is no type filter in either function. A node-id-shaped string that exists in the corpus is sufficient, regardless of whether it names an `experiment`.

### Edge cases

- **Self-citing:** Already blocked by `_is_self_citation` — but a self-citation of a non-experiment type (a verdict citing itself) is already blocked, just for a different reason (identity, not type).
- **Bare-int evidence:** `evidence_runs: 3` counts 0 after G7.3 — not affected by type check because it never reaches the list.
- **allowed_parents schema constraint:** The schema may restrict what can cite what, but `evidence_gate.py` does not import or consult schemas — it checks only corpus membership.
- **Multi-type nodes:** A deprecated experiment is still an experiment; type check would need to read the node's frontmatter `type:` field, not just the id.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a02-ccfcf794 review pass, 2026-09-03. Verified the load-bearing
assertion against source before accepting: the list path in
`normalize_evidence_runs` (evidence_gate.py L299-307) checks exactly
`is_node_id_shaped(v) and v.strip() in corpus and not _is_self_citation(...)`
— no type predicate; `build_corpus` (L195) collects every `id:` under
nodes/ regardless of type, per its own docstring. So the claim's disprove
condition 2 (a hidden type check) is falsified by the code, and the claim
stands as far as the code reading goes. What remains genuinely pending is
the empirical half — disprove condition 3, the real-corpus audit of what
`proved` nodes actually cite. Verdict stays `pending` for that reason,
and 0.85 confidence is defensible only because the code half is now
verified, not because the audit ran.
Also noted from the kid's session log: it reported "tests dir missing".
The suite exists at extensions/agi/tests/ (1379/1381 passing on this box
the same day) — the kid looked in the wrong place, so any "tests pass"
reading it may have had in mind is void. It made no such claim here; the
node is clean on that count.
<!-- THOUGHT:END -->

## Agent Notes
Evidence gate validates evidence_runs by node-id existence only, never by type. A hypothesis citing goal:g3 (a goal node) as evidence_runs passes the gate — build_corpus returns all ids regardless of type, and normalize_evidence_runs only checks corpus membership. Novel axis orthogonal to all 12+ sibling attribution/relevance/decay hypotheses.