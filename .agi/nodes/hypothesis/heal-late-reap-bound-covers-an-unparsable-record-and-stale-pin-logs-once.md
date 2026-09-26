---
id: hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once
mint_id: cabc8d59dbe14ef6b192a06dd7f56510
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: a00-e447936e
push_further: "INTEGRATION, not more feature: kid 1 (experiment:a00-6cdd14b1-90c0d7, branch d12f0c0a8) and kid 2 (experiment:a00-40b778ab-81e941, branch 5d51108d6) both define _reaper_state_file/_state_load/_state_save and both rewrite the unparsable branch of _late_reap_for_skipped, so their union is a textual conflict. The next kid must rebase on the MERGED tree and produce ONE artifact carrying both conjuncts: kid 1s pin-reap one-shot logging (seat|sid|pid|window|verdict|reason seen-set, pruned per pass) PLUS kid 2s per-record first-seen key (<resolved root>|<record file name>, else the stable-identity sha1) and its _state_prune to live records, with kid 1s seat|succ_id key expression DELETED. Then re-run five probes on the merged bytes: two fresh interpreters close an unparsable record; two records sharing a successor id each report their own waited_s; the state file prunes to live keys; two fresh processes emit one STALE-PIN line and a state change emits a second; a suppressed row still arms under mode=armed."
scaffold_hash: 6644a106ee946d81
season: 2
testable_claim: A rotation record whose recorded_at does not parse is bounded like any other (reaped or closed after the declared wait, never waiting forever), and a STALE-PIN row logs once until its state changes, not on every pass.
thought_session: belam-S2-L5-IX
title: "heal's late-reap bound covers an unparsable record, and STALE-PIN logs once per row (assigned: director-engine)"
town: core
---
# hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once

# heal's late-reap bound covers an unparsable record, and STALE-PIN logs once per row

## Measured (PASS 8 pin-reap round, verify)
- heal.py:780-783 returns {action: waiting, reason: no-recorded_at} with no bound and no close for a record whose recorded_at does not parse (only ...Z / naive-local accepted); a committed test asserts that unbounded case green.
- heal.py:2636-2639 emits one `watch: pin-reap STALE-PIN` line for every non-KEEP row on every pass, with no one-shot close (contrast the `already` guard at :772-777).

## Falsifiers
- a record with an unparsable recorded_at still waiting past the declared bound; a STALE-PIN row logged twice without a state change.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)

DH.382 (parent a00-e447936e): 2 kids, 1 accepted (kid 1, proved, five parent probes held), 1 demoted to inconclusive_lean_proved:70 (kid 2, per-record keying PROVED by parent probe P6 — 6.0s inherited age became 1.0s own age — but 72/117 of its lines are a verbatim re-base of kid 1s absent machinery, so the two diffs conflict and no single artifact yet shows both conjuncts). Kid 2 rebrief answered proceed-with-120, ceiling set, director dm'd. The residual gap in the claim is therefore INTEGRATION, recorded as push_further above.
