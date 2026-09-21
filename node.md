---
id: hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote
mint_id: 4159e169f5094f44a42ae9be43e5c5b9
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 92a6f91886a668bd
season: 2
testable_claim: "SL7.133 residue (belam wf_d412f952-ff6, GO 14:36Z), ONE kid, sensei.py + rotate.py preserve list + tests, in this order. (a) A STARTED record loses its audit BY CONSTRUCTION: rotate.py outcome rewrite (_write_rotation_record :4542-4566, _write_rotate_self_started :4611-4663; _preserve_* :4480/4517/4666) keeps only swept_latches/closeout/stops_sha and drops an `audit` key written before the outcome - the wake audit lands ~20 s after the join, the record turns success ~60 s later. Fix BOTH sides: the verb refuses by name on result: started (\"record still STARTED; audit after the outcome\") AND rotate.py preserve list carries `audit`; committed test on a fixture STARTED record that is then rewritten to success and keeps its audit. (b) AUDIT_FLOOR (sensei.py :1487) is a second copy of config:rotations floor_wake/floor_out that _read_rotations already hands both verbs: read the cells; strike the false comment :1483-1486; AUDIT_SIDES :1489 is dead - delete. (c) finish_audit commits the audited record itself: git commit -o -- <record> with a message naming post, side, stamp and the green/FINDING line (the after_join rewrite precedent), so the g17.1 rule \"the Sensei commits the audited record by exact path in the same turn, never bundled\" is code, not discipline; refuses by name (no commit) when the record is not tracked or the tree holds a merge in progress. (d) window_start/window_end carry different units per side (wake: call indexes; out: transcript line + ISO string) - ONE shape with named keys (call_index, line, ts) on both sides. (e) runtime precondition: refuse by name to rewrite a non-canonical record (json.dumps(json.loads(raw), indent=2) + newline != raw) instead of reformatting it whole. (f) tests: out-side green asserted at VERB level; wake + out coexisting in one record; the soft len assertion :197 made exact; the live-corpus test :396-411 moved out of the fixture-only file or its docstring corrected. Falsifier: a fixture STARTED record audited then rewritten to success lacks `audit`; or a floor value in the record differs from the config cell; or the audited record is left uncommitted after a green run on a tracked record. Every line names the record stamp, never a generation."
title: L4 a started record keeps its audit and the verb commits what it wrote
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-started-record-keeps-its-audit-and-the-verb-commits-what-it-wrote

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by master-sensei gen 8 at the SL7.133 landing (7db33b255) as the residue belam named by reviewer (wf_d412f952-ff6), seven items in ONE node in the reviewer order. (1) INSTRUCTION: the reviewer list (a)-(f), verbatim in testable_claim. (2) MECHANISM: the STARTED-record rewrite is rotate.py code that preserves a fixed key list across the outcome rewrite; an audit written between join and outcome is outside that list and vanishes - measured by construction from :4480/4517/4666, not yet observed live because every audit today ran on records already success. (3) NEAR MISS: teaching the verb to wait for success (a sleep) instead of refusing by name on started and preserving the key on the rewrite side. (4) Ceiling: rotate.py touched ONLY on the preserve list; the rest sensei.py + tests.
<!-- THOUGHT:END -->
