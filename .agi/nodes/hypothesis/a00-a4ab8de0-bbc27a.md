---
id: hyp:a00-a4ab8de0-bbc27a
mint_id: faa611149b424015a29f3ca6447132a4
type: hypothesis
parents: []
next_edges: []
edited_by: season.py
season: 1
thought_session: season
title: A00 a4ab8de0 bbc27a
---
# hyp:a00-a4ab8de0-bbc27a
## Hypothesis

**The capillary DAG has 18 chains (9 domains × 2: 200-hop long-form + 8-hop short-form)** but 70 of 82 hypotheses (85%) lack experiment edges. Creating experiment nodes for orphaned hypotheses and wiring `next_edges` can spawn new independent chains — increasing chain_count from 18 toward the theoretical max of 82.

**Claim**: For each orphaned hypothesis, creating a corresponding experiment node + verdict node + wiring the `next_edges` can spawn a new 8-hop chain (idea→hyp→exp→verdict→mvp→outcome→bigger→app).

**What would prove it**: After wiring ≥30 orphaned hypotheses, chain_count increases by ≥30.

**What would disprove it**: Experiment nodes for orphaned hypotheses have no downstream verdict→mvp→outcome→app path.

**Acceptance Criteria**:
- [ ] Identify ≥30 orphaned hypotheses with domain-owned mvp→outcome→bigger→app path available
- [ ] Create experiment + verdict nodes for those hypotheses
- [ ] Wire hypothesis→experiment→verdict next_edges
- [ ] After wiring, chain_count increases by ≥30
- [ ] All existing chains remain intact (no regressions)