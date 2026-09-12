---
id: hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write
mint_id: 41b834baf8f14ea5835e326ff7cc2d29
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 64eb84754cc0af44
season: 2
testable_claim: "FIX-ONLY ROUND (g15) for the mur-48 by name residue (c) on RUNG 2b, verbatim (Prime XVII, wf_a6c4237e-9a7): \"L4.329: a set_fm key named _fresh is displaced in the signed decision (written value uncovered by the quorum); a key in both set_fm and unset_fm signs as unset but writes the set value; nonce_ledger.remember() swallows write failures (replayable); declared-but-EMPTY written_by now refuses every writer where it admitted all — check no live schema has an empty list; ring-nonces.json under .agi/nodes/.geometry will churn commits once a ring is live — move it under .agi/sessions; write.py --dry-run never previews a ring/freshness refusal.\" Source: hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself (L4.329, merged a182e966a). Anchors @61311b2c2: src/seatsig/rings.py (canonical_bytes, the decision record, nonce_ledger, remember), extensions/agi/bin/write.py ring-gate region (_config_write_fields, --ring-sig/--ring-fresh/--ring-fields, --dry-run), .agi/nodes/.geometry/ring-nonces.json (if present), every .agi/context/schemas/[*].md written_by cell. CLAIM: (1) a user key named _fresh cannot displace the freshness field -- the decision namespaces its own fields (or refuses a colliding key by name) so every written value is covered by the quorum; (2) a key present in both set_fm and unset_fm is refused by name before signing; (3) nonce_ledger.remember() raises (and the write is refused) when the ledger cannot be written -- a nonce is never spent silently; (4) an EMPTY declared written_by refuses every writer BY NAME with a message that says the list is empty, and a scan proves no live schema declares an empty list (list them); (5) the nonce ledger lives under the shared sessions dir (locations.shared_sessions_dir), never under .agi/nodes; (6) write.py --dry-run previews the ring/freshness refusal it would raise. FILE SCOPE: src/seatsig/rings.py, write.py ring-gate region ONLY (not the veto gate, not the create gate), the ledger path constant + its migration note, tests test_rings*.py test_write_ring_cli.py test_ring_cli_seam.py + new. NOT: veto.py, towns.py, branches.py, cli.py, any schema cell edit (report the scan only), rotate.py. LIVE INVARIANT: rings.load_rings on the live tree = [] and stays so; no ring decision made live; no live schema edited. KIDS (<=3): A decision fields + collisions (1,2); B ledger (3,5); C written_by scan (4) + dry-run preview (6). PROOF: fixture tests for each numbered clause, named refusals, the scan output pasted on the node; touched suites green; live tree byte-identical outside the round's own files. DISPROOF: any written key uncovered by the signed bytes; a spent nonce on a failed write; a ledger under .agi/nodes."
title: "RUNG 2b residues: a signed decision covers every written key, set/unset collisions refused, the nonce ledger raises on write failure and lives under sessions, empty written_by refuses by name, --dry-run previews ring refusals"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-signed-decision-covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
