---
id: hypothesis:lm-event-port-lazy-leak-gap-off-by-one
mint_id: aae4c35a845a4c16a837259f5ec45ed2
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: under 1 USD OpenRouter; light CPU8G compute, same fixture TM.61 already used; under 30 production lines across event_port.py and the corrected event_rows.jsonl; runs under 15 minutes
edited_by: director-thought
falsifier: After the fix, event-steplk still diverges from L.ref_trains() on any seed, or the TM.61 node still states that no closed form can be bit-exact, or the bottom-line disproved verdict on hypothesis lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work changes (it must not change -- conjunct 2 alone still fails it at 17.7 percent versus a 10 percent bound), or n_active_ge2 is left silently identical to n_active in the code with no fix or disclosure.
scaffold_hash: 8db1eff68622fe72
season: 2
testable_claim: "event_port.py line 48 computes gap = t - tl[tu] for the lazy closed-form leak arms (event-k, event-src, event-steplk), but the value stored at tl is the post-update v(tl+1), so the correct decay exponent to reach step t is (t - tl - 1), not (t - tl). The TM.61 mur verify stage (run key mur-2866e79b72061eefb7cb7a4a6490c1458c26c029, finding M1) measured event-steplk bit-exact (0 divergent out of N, all 4 seeds) against the committed C reference under the corrected gap; the landed event-k and event-src numbers (90, 77, 98, 99 divergent per seed) are an artifact of the off-by-one, not evidence that no closed form can be bit-exact. Claim: applying gap = (t - tl[tu]).astype(float) - 1.0 and re-running the 4-seed comparison reproduces 0 divergent on event-steplk against L.ref_trains(). Correct the TM.61 node title, conjunct-1 reading (goes from NOT_MET to MET), and the no-closed-form claim in place; add a THOUGHT block recording the deviation and citing this node. Two smaller confirmed items fold into the same slice, same file and node, no extra compute: event_port.py lines 27 and 31 compute n_active_ge2 as len of a set of distinct neuron indices, identical to n_active, so it never counts neurons with two or more spikes -- fix the computation or relabel the field, and note the change for event_rows.jsonl going forward. Also correct the TM.61 node prose describing parent probe P1 (a four-threshold-flip claim): the probe compared two independently drawn gap vectors, so the flip count is not a valid measurement; the per-double 0.9 times v not equal to v minus 0.1 times v fraction (about 19 percent) stays in the record but no longer supports an impossibility claim."
tests: ONE pi parent, CPU8G (event_port.py already declares CPU8G agi-run in its own file header); re-run the 4-seed comparison with the corrected gap line; FILE SCOPE event_port.py plus event_rows.jsonl (regenerated) plus the TM.61 experiment node .agi/nodes/experiment/a00-4abc60e7-5fc7ea.md (in-place correction, one THOUGHT block) ONLY -- do not change the bottom-line verdict field, and do not touch hypothesis lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work itself beyond what the falsifier allows; cite mur-2866e79b72061eefb7cb7a4a6490c1458c26c029 findings M1, M2, M3 by id in the new experiment node; land on the director post branch, push to refs/agi/posts/director-thought; mur by name.
thought_session: iter-TM.64
title: event_port.py lazy closed-form leak computes gap = t - tl instead of t - tl - 1 (tl stores the post-update value), producing a false no-closed-form-can-be-bit-exact claim in the TM.61 node; n_active_ge2 is mislabeled; the TM.61 P1 probe compared mismatched gap draws
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-event-port-lazy-leak-gap-off-by-one

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
