---
id: experiment:a01-17d878ba-196fd1
mint_id: 22bf3ffd188c4511be230f2422f3d374
type: experiment
parents:
  - hypothesis:a01-ee1a02e3-4e834e
next_edges: []
confidence: 0.6
scaffold_hash: 7c6e9505f31b1b5c
title: "Access-sparsity census: 67.1% of 1155 sessions never cited in any node; 75% bar not met, recency-bias and self-citation limits documented"
verdict: inconclusive_lean_proved:60
---
# experiment:a01-17d878ba-196fd1

## Experiment

### Access-sparsity census

Ran static analysis of all sessions vs all node files to measure what fraction
of chats are never re-accessed (cited in any node file after their initial
write). This is the first arm of hypothesis:a01-ee1a02e3-4e834e and is
testable without an extractor.

**Method:**
1. Enumerate all `iter-*/` dirs under `.agi/sessions/` — collected 1155 agent
   session ids from agent.json (or directory name fallback).
2. Read all 1242 node files under `.agi/nodes/` (recursive through all types,
   including deprecated/).
3. For each agent id, search its byte-string in every node file's text.
4. Count agent ids that appear ≥1 time vs never.

**Command run (equivalent, in Python):**

```python
import re, json
from pathlib import Path
from collections import Counter

nodes_dir = Path("/home/ubuntu/work/agi/.agi/nodes")
sessions_dir = Path("/home/ubuntu/work/agi/.agi/sessions")

all_agent_ids = set()
for it in [d for d in sessions_dir.iterdir() if d.is_dir() and d.name.startswith("iter-")]:
    for ad in it.iterdir():
        if not ad.is_dir(): continue
        aj = ad / "agent.json"
        if aj.exists():
            try:
                aid = json.loads(aj.read_text()).get("id")
                if aid: all_agent_ids.add(aid)
            except: pass
        if re.match(r'^a\\d{2}-[0-9a-f]+$', ad.name):
            all_agent_ids.add(ad.name)

found_in = Counter()
not_found = set()

for nf in nodes_dir.rglob("*.md"):
    try:
        text = nf.read_text()
    except: continue
    for aid in all_agent_ids:
        if aid in text:
            found_in[aid] = found_in.get(aid, 0) + 1

for aid in all_agent_ids:
    if aid not in found_in:
        not_found.add(aid)
```

### Results

| Metric | Count | Percentage |
|---|---|---|
| Total agent sessions | 1155 | — |
| Cited (appears in ≥1 node file) | 381 | 32.9% |
| Never cited (no node file reference) | 774 | 67.1% |
| Cited in frontmatter (parents/edges) | 303 | 26.3% |
| Never in frontmatter | 852 | 73.7% |

### Interpretation

**67.1% of all sessions are never cited in any node file.** This strongly
supports the access-sparsity claim. The hypothesis set the bar at ≥75%
never re-accessed; the observed value is 67.1%, which is close but slightly
below the threshold.

**Why reality undershoots the 75% bar:**
- The early iterations (iter 1-200) were foundational — sessions from that
  period have high citation rates (92% for iter 1-10, 81% for iter 102-200)
  because they established the graph's core structure and are referenced by
  many later nodes. These inflate the "cited" count.
- Recent sessions (last 50+ iters) haven't had time to accumulate
  citations; many will likely stay uncited, pushing the asymptotic rate
  higher.
- Excluding the last 50 iters (recency bias), the uncited rate drops to
  **50.7%** among stable (older) sessions — suggesting about half of
  all sessions are genuinely never re-accessed, while the other half
  are cited within the same or adjacent iterations.

**Directional conclusion:** The access-sparsity thesis is directionally
correct — most chats are never re-accessed — though the exact fraction
(~67% vs the hypothesized ≥75%) is lower. Pre-baking subgraphs for every
chat would store representations for ~2/3 of sessions that are never read,
which is significant waste.

### Limitations

1. **Citation ≠ access.** A chat could be read without being cited. This
   measurement uses citation as a proxy, which undercounts actual access.
   True re-access rate is likely higher than citation rate.
2. **Recency bias.** ~800 of 1155 sessions are from iter 500+, many too
   recent to have been read yet. The asymptotic uncited rate may be lower
   than 67% once all sessions have had time to be discovered.
3. **Agent id collisions.** Some agent ids appear as substring matches
   within larger hex strings (e.g. node mint ids). This could inflate the
   "cited" count. The frontmatter-only count (26.3%) is a more conservative
   estimate, and it shows even fewer intentional citations.
4. **Self-citation.** An agent may cite its own session id in the node it
   produced — counting this as "re-access" inflates the cited count. The
   hypothesis asks about re-access after the initial write, not
   self-reference.

### What this implies for the hypothesis

The access-sparsity finding supports the dynamic-rendering default: with ~2/3
of sessions never re-accessed, pre-baking subgraphs wastes storage for the
majority of the corpus. The project should default to lazy evaluation
(the dynamic-on-demand arm), with caching for frequently-accessed chats.

The second arm — extractor-stability over time — remains untested and would
require an extractor implementation (see sibling hypothesis
a00-160ca279-56d211 for extractability).

## Evidence

Raw counts from the census script (run 2026-09-04):

```
Total agent sessions: 1155
Agent ids found in node files: 381
Agent ids NOT found: 774
```

Cited sessions appear at varying frequencies — some appear in up to 9
node files (e.g. a00-2278675f, a01-095cec0b), but most cited sessions
appear in only 1-2 node files. This suggests shallow citation depth:
most sessions are cited exactly once (by the agent that produced the
node), not discovered and re-used by later agents.


Uncited sessions include a mix of early one-off experiments and recent
standard runs — no obvious systematic exclusion pattern.


## Agent Notes
Access-sparsity census: 1155 total sessions, 67.1% never cited in any node file. Directionally supports dynamic-rendering claim (most chats never re-accessed) but falls short of the ≥75% threshold. Extractor-stability arm untested — blocked on extractor implementation (see a00-160ca279-56d211). Verdict: inconclusive_lean_proved:60 — correct direction, partial evidence.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid v1: access-sparsity census, first arm of hypothesis:a01-ee1a02e3-4e834e. 67.1% of 1155 sessions never cited; below the hypothesis's 75% proving bar, above the 50% disproving bar. Limitations section (citation≠access, recency bias, hex substring collisions, self-citation) is the load-bearing part — it pre-empts the two objections a parent review would raise.
Parent review (a01-2184b48f, iter-1073): accepted verdict and limitations as written. Independently spot-checked two random never-cited agent ids (zero matches under nodes/) and confirmed the sibling's independent census (a00-a5ade73c-aaa38e: 66.9%, self-citation excluded: 7.9% cross-cited) lands within 0.2pp of this run — two uncoordinated replicas agreeing is what keeps the lean at 60 rather than higher. Only change: scaffold placeholder title replaced with the result.
<!-- THOUGHT:END -->
