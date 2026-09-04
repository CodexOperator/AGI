---
id: verdict:a01-1b0831eb-9027d1
mint_id: d382816a44cb4674a39958f03433a251
type: verdict
parents:
  - experiment:a00-9f243a1c-7ba585
next_edges: []
confidence: 0.75
scaffold_hash: 6fa9983469bfd941
title: A01 1b0831eb 9027d1
verdict: inconclusive_lean_proved:75
---
# verdict:a01-1b0831eb-9027d1

## Verdict

inconclusive_lean_proved:75

## Evidence

1. **Coverage gap confirmed:** Bounded (max_wait_s=1, sim 30s) detected 2/4 (0.50); continuous (max_wait_s=60, sim 600s) detected 4/4 (1.00). +50% improvement in detection coverage — exact claim hypothesis makes.

2. **Late deaths are real:** Agents dying at 15s and 45s were missed by the bounded phase, matching the scenario where a pi agent dies mid-run after the 30s reaper window closes.

3. **Falsifier points NOT tested:** No real pi agents, no main-thread blocking measurement, no heal.py race condition probe, no post_wire ordering test. The experiment proves detection coverage only — not real healing.

4. **Simulation scope:** Script at `.agi/tmp_reaper_gap_v4.py` uses mocked time, fake adapter, no real Popen restarts. Valid for the bounded-vs-continuous coverage question; invalid for production safety claims.

## Limitations

- Mocked time compresses 45s into milliseconds — real 600s continuous run was not tested
- No real agent restarts — adapter always returns a new pid
- No heal.py concurrency test — manifest is never written concurrently
- No post_wire test — harvest after restart not exercised

## Confidence

0.75


## Agent Notes
Experiment confirms detection coverage gap (0.50 bounded vs 1.00 continuous) but does not test falsifier points: main-thread blocking, heal.py races, post_wire ordering, stale restart context. Simulation-only with mocked time and fake adapter. Core claim proven at detection level; production viability unproven.
