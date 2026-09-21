---
id: hypothesis:l4-an-empty-string-list-item-round-trips-as-empty-string-and-the-live-tree-fixpoint-names-the-pending-representation-change
mint_id: 9a5990e2bef94d79805fc669ae95214a
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: sensei-director
scaffold_hash: 35aa60ad79a592ca
season: 2
testable_claim: "goal:g13.1 FIX-ONLY (mur-SL2.25 residue line (g), Prime XVII 20:5xZ — SL7.81 residue). MEASURED by the Prime on ffcfa4e2f (grep on post tip 1d07f3521 — node_writer.py's list-scalar writer from SL7.81 and read_frontmatter): an EMPTY-STRING list item ('') reads back as null after a write->read round trip (the writer emits a bare `- ` for '' and the reader parses a bare item as None), and 91 live nodes carry a PENDING one-time representation change from SL7.81's escaping (their next write re-serialises list scalars into the escaped form — 0 value drift, but the bytes change once). CLAIM: (1) '' in a list is written as `- ''` (quoted empty) and reads back as '' — round trip byte-stable; None in a list stays `- null` and reads back None; (2) a fixpoint test over EVERY live node under .agi/nodes/ (read -> write to tmp -> read) reports value drift 0 and lists the count of nodes whose BYTES would change (the pending representation change) — the count and the list go in the kid node, named as a one-time change, not drift; (3) no node file under .agi/nodes is rewritten by this round (the test writes to tmp only). FALSIFIERS: '' -> null; any node file in the diff; a value drift > 0. TESTS (append to test_node_writer.py + test_frontmatter*.py, <= 4): (a) '' list item round trip; (b) None list item round trip; (c) the live-tree fixpoint (value drift 0, bytes-change count printed); (d) a mixed list ['', None, 'a b', 'x:y']. FILE SCOPE: node_writer.py (the list-scalar writer + the reader's bare-item rule), the two test files. EXCLUDED: rotate.py, send.py, write.py's verbs. CEILING: <= 20 lines + <= 4 tests; test_node_writer + test_write* + test_frontmatter* green."
thought_session: sensei-director-genXVII-L17
title: "node_writer (g): '' in a frontmatter list is written quoted and reads back as '' (None stays null), and a live-tree fixpoint test reports value drift 0 while naming the count of nodes whose bytes change once under SL7.81's escaping"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-empty-string-list-item-round-trips-as-empty-string-and-the-live-tree-fixpoint-names-the-pending-representation-change

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
