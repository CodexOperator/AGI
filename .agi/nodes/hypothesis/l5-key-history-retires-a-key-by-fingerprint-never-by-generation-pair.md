---
id: hypothesis:l5-key-history-retires-a-key-by-fingerprint-never-by-generation-pair
mint_id: cabe8ac491c840fea3cb44d434e9e576
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: db69e264fb318407
season: 2
testable_claim: "(1) rotate.py's identity-cells write (the key_rotation branch, ~L9465) appends the retired predecessor entry unless an existing key_history entry carries the SAME fp (or pub); the (from,to) generation pair is never the identity of a key. (2) MEASURED: sanctuary-master's pushed row (origin/season2/main, gen 3) holds key_history pairs (1,2),(2,3),(3,4),(4,5),(5,6),(0,1): after the gen-count reset the 0->1 rotation appended, then 1->2 and 2->3 were dropped as (from,to) duplicates of the old count -- the gen-8 key fp fee749794ea8f153 is absent from the row, so the predecessor's 22:48:26Z '[SM] SM.126 LANDED @c247f0fd2 ... GO on SM.127' (which VERIFIES under that key: in-process probe, send._canonical_msg + seatsig ed25519, live_verify=True on the trunk's gen-2 row) labelled FORGED at director-sanctuary (send._label_for_sig: the RETIRED path had no entry to match, the live path failed under the gen-9 key) and was withheld to its quarantine under comms.verify enforcing. Same drop on every post whose gen count reset. (3) Post-fix a retired entry whose (from,to) repeats an earlier epoch's pair is appended; a retried row write re-offering the SAME fp is still a no-op -- history never shrinks and never duplicates a key. (4) TESTS: a row whose key_history already holds (from 2,to 3) under fp A; rotate out fp B with from 2/to 3 -> B appended (len+1); offer B again -> len unchanged; a message signed by B labels RETIRED:<fp> against the post-fix row, never FORGED (send._label_for_sig direct). FILE SCOPE: extensions/agi/bin/rotate.py (the one dedupe predicate), extensions/agi/tests/test_rotate*.py. No repair of already-dropped entries (those keys signed only the last lines of two past gens; the dropped pubs remain in posts.md's git history if ever needed). CEILING 4 production lines."
title: "SM.128 (measured 22:5xZ 09-18 from the gen-8 quarantine; goal:g15.25 line 2): the rotate-out key_history append dedupes by the retired key's fp, never by the (from,to) generation pair -- after a gen-count reset every retired key is silently dropped and the outgoing post's last lines read FORGED at an enforcing reader"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-key-history-retires-a-key-by-fingerprint-never-by-generation-pair

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
