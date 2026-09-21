---
id: hypothesis:lm-rig-fetch-supervisor-enforces-the-bytes-rules
mint_id: 7d047d40931f474caf20ce6550ad6530
type: hypothesis
parents:
  - goal:g14.6
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; off-box; no new downloads beyond the re-fetch of a failed 27B segment
edited_by: thought-master
falsifier: any of (a)-(c) cannot be made to hold without changing the fetch protocol (record why) OR the 27B assembled hash does NOT match the lfs oid (then the 12 segments are re-fetched under the enforced rules, slow mode, and the round reports the bytes it had to redo) OR the fix breaks the live athena/base queue (resume fails; the round must leave the queue running).
scaffold_hash: e28e6a86ebf83672
season: 2
testable_claim: "On GPU2070S, in the town supervisor scripts (fetch_parallel.py and bonsai27b_fetch.py under .agi/context/local-maxxing/athena/ and the 27B fetch path): after the round (a) every fetch refuses to start or resume when statvfs free on /data < 20 percent, with a logged line; (b) every completed file is sha256-hashed and compared to the HF lfs oid recorded at queue time, mismatch = the file is renamed .bad and re-queued, match = logged; (c) bonsai27b_fetch.py honours the same rate schedule as fetch_parallel.py (0.5 MB/s; 1.5 MB/s 02-06 America/New_York, zoneinfo) with RATE unset; (d) the Bonsai 27B segments are assembled and its sha256 matches the HF lfs oid (recorded in the row). Tests: a dry-run with a fake low free-space value refuses; a deliberately corrupted small test file is caught; the schedule test from TM.33 passes for both scripts; the 27B row shows sha256 match = true."
tests: "ONE pi parent + ONE kid on --harness pi (kid over ssh), off-box slot after the device-code hop; 0 USD compute; NEVER beside a live tg/pp row; keep the running queue alive (edit, test on a scratch copy, then swap); rows to file after every probe; commit after every probe; land on the director post branch. Engine-style code round: kids write the code, the parent reviews (g15 rule)."
title: "The rig fetch supervisors do not enforce the owner bytes rules (TM.44 step 0, 22:00Z: no 20 percent free-disk floor (no statvfs), downloaded bytes never hashed against the recorded HF lfs oid, bonsai27b_fetch.py unthrottled when RATE is unset; Bonsai 27B 12/12 segments fetched, not assembled, sha256 unchecked) -- one kid round makes all three enforced and the 27B verified"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-rig-fetch-supervisor-enforces-the-bytes-rules

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
