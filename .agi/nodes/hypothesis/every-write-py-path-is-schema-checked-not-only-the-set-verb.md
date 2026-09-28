---
id: hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb
mint_id: 9481a26261524c0c86d840541798ba50
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass9-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 446f96b63737e313
season: 2
testable_claim: "write.submit() -- the library path rotate.py and every engine caller write through -- runs the same _schema_field_refusal check the CLI's set and create verbs run, so a refuse: annotation, a value failing the schema regex/type, or a raw scalar for a list-typed field written through submit() is refused with one line naming the row and the rule, exactly as through the CLI."
thought_session: belam-S2-L5-X
title: "every write.py write path is schema-checked, not only the set verb (assigned: director-engine)"
town: core
---
# hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb

# hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb

# every write.py write path is schema-checked, not only the set verb

## Measured (PASS 9 write-py-set-is-schema-checked, verify defect 3 stands; confirmed by the Prime on the TIP bytes)
- At TIP 9e16b8ed9 the per-field check _schema_field_refusal (write.py:1800) is reached only through _enforce_create_schema_gate (:1860) and _enforce_set_schema_gate (:1930), and both are called only from main (:2920) -- the CLI. submit() (:2040), the library path engine code writes through, never reaches it (an AST walk of the file), and rotate.py:9518 writes list cells straight through write.submit. A refuse: annotation, a value failing the schema regex/type, or a raw scalar for a list-typed field -- each refused by name on the CLI -- is written unchecked by any engine caller.

## Falsifiers
- a fixture write.submit() of a raw scalar into a list-typed field (or of a value the schema regex refuses) writes the node instead of refusing with one line naming the row and the rule.

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk1of28)
