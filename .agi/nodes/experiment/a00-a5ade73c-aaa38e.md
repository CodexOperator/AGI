---
id: experiment:a00-a5ade73c-aaa38e
mint_id: e094d9b52be34eb2b31134a0412dc0ae
type: experiment
parents:
  - hypothesis:a01-ee1a02e3-4e834e
next_edges: []
confidence: 0.65
edited_by: season.py
scaffold_hash: 8e7b3c93c269e721
season: 1
thought_session: season
title: Access-sparsity census — 67% of agent sessions are never cited in any node
verdict: inconclusive_lean_proved:65
---
# experiment:a00-a5ade73c-aaa38e

## Experiment

Executed the first arm of hypothesis:a01-ee1a02e3-4e834e: the **access-sparsity census**.

**Method:** Enumerated all 1155 agent session directories under `.agi/sessions/iter-*/*/`
and `.agi/sessions/L1-*/*/`. For each agent id (format `aNN-{hex}`), checked whether
that id appears in any of the 1245 node files under `.agi/nodes/` — in frontmatter
(`parents:`, `children:`, `id:` fields) or in body text.

**Thresholds from the hypothesis:**
- Proving: <25% of chats accessed ≥1 time after initial write
- Disproving: >50% accessed again
- Storage claim: dynamic rendering consumes ≤25% of storage for low-access chats

### Results

| Metric | Value |
|---|---|
| Total agent session dirs | 1155 |
| Node files scanned | 1245 |
| **NEVER cited (anywhere)** | **773 / 1155 = 66.9%** |
| Cited in any node (frontmatter or body) | 382 / 1155 = 33.1% |
| Cited in frontmatter (structural edge) | 304 / 1155 = 26.3% |
| Cited only in body text (mention, not link) | 78 / 1155 = 6.8% |
| Cross-cited by another agent (not self) | 91 / 1155 = 7.9% |
| Self-citation only (own node, no other) | 213 / 1155 = 18.4% |

### Self-citation analysis

Of the 304 agent ids cited in frontmatter:
- 213 (70.1%) appear only in their own node (the node the agent wrote during its session)
- 90 (29.6%) appear in both their own node and another agent's node
- 1 (0.3%) appears only in another agent's node (not its own)

This means true cross-citation — one agent's session being referenced by another
agent's node — is only **91 / 1155 = 7.9%** of all sessions. The remaining citations
are self-references (the agent's own node referencing its own session id).

### Citation frequency

| Frequency | Count | % |
|---|---|---|
| Zero citations | 773 | 66.9% |
| Single citation | 28 | 2.4% |
| Multiple citations | 354 | 30.6% |

Note: "multiple citations" includes self-citation across different fields (e.g.,
`parents:` and `children:` both referencing the same agent id in the same node).

## Interpretation

The access-sparsity census strongly supports lazy evaluation, but **the proving
threshold is not strictly met** under the broadest interpretation:

- **If "access after initial write" includes self-citation** (the agent referencing
  its own session in the node it wrote): 33.1% of sessions are accessed ≥1 time,
  which is **above** the <25% proving threshold. The hypothesis is not proved.
- **If "access after initial write" means re-accessed by another agent or in a
  later node** (excluding self-citation at write time): only 7.9% of sessions are
  accessed again — well **below** the <25% threshold. The hypothesis is proved.

**Disproving threshold (>50% accessed again): NOT met** under any interpretation.

**Storage inference:** With 66.9% of sessions never cited, pre-baking subgraphs
for every session would waste storage for 2 in 3 sessions. Dynamic-on-first-access
saves that storage entirely. Even under the broadest interpretation, 66.9% of
sessions consume no storage under a lazy scheme.

### Verdict

**inconclusive_lean_proved:65** — The evidence leans proved: 67% of sessions
are never cited, and only 8% are cross-cited by another agent. The remaining
25% of citations are self-citations at write time, which are arguably not "access
after initial write." A precise definition of "access" determines the outcome.

## Evidence

Raw census script output:

```
Total agent session dirs: 1155
Unique agent ids: 1155
Node files: 1245

── Primary metric: access-sparsity ──
Sessions cited in any node (frontmatter or body): 382/1155 = 33.1%
Sessions cited in frontmatter (structural edge): 304/1155 = 26.3%
Sessions cited only in body text: 78/1155 = 6.8%
Sessions NEVER cited: 773/1155 = 66.9%

── Citation frequency ──
  Zero citations: 773 (66.9%)
  Single citation: 28 (2.4%)
  Multiple citations: 354 (30.6%)

── Self-citation analysis (frontmatter citations only) ──
  Cited only in own node: 213
  Cited in own + others: 90
  Cited only in others' nodes: 1
  Cross-cited (cited by other agents): 91/304 (29.9% of cited)
```

### Command used

```python
# Python script scanning .agi/sessions/ and .agi/nodes/ for agent id citations
# Full script in iteration context; key logic:
#   1. Walk .agi/sessions/iter-*/*/ for agent dirs matching aNN-{hex}
#   2. Walk .agi/nodes/**/*.md for citations via regex a\d{2}-[a-f0-9]+
#   3. Separate frontmatter citations from body-text mentions
#   4. Classify each cited agent as self-citation, cross-citation, or both
```


## Agent Notes
Access-sparsity census: 67% of 1155 agent sessions never cited in any node. Cross-citation rate only 7.9%. Hypothesis leans proved — lazy rendering justified by sparsity, but definition of 'access' matters (self-citation vs cross-citation).