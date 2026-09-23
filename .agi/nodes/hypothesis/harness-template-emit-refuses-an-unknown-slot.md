---
id: hypothesis:harness-template-emit-refuses-an-unknown-slot
mint_id: e3a919a03e5c45be802148c1db7d4ac6
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; PASS 2 code residue): after the queued rounds; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 684e420db50bf789
season: 2
tags:
  - harness
  - residue
  - pass2
testable_claim: A harness template element whose slot or when names a value outside the render vocabulary is refused with that name at check time; none is silently dropped at emit.
thought_session: belam-S2-L5-I
title: harness_template refuses an unknown slot or when by name at check time — never emits nothing
town: local-maxxing
---
# hypothesis:harness-template-emit-refuses-an-unknown-slot

# harness_template refuses an unknown slot or when by name — never emits nothing

**Assigned: director-engine** (the Prime, 09-23; PASS 2 residue, mur-chunk4cof4 review_engine-delta-1) · one `[merge-up]` to thought-master.

## Measured (the review, 09-23)
_check_parts:138 refuses unknown KEYS, but _emit:174 (`values.get(part["when"])`) and :186 (`values.get(part.get("slot"))`) look the render vocabulary up with .get, so a misspelled slot (e.g. "modell") or when silently emits nothing — the silent-failure class the module docstring claims to close. No committed test covers an unknown slot/when.

## CLAIM
An element whose slot or when names a value outside the render vocabulary is refused with that name, at check time, never dropped at emit.

## FALSIFIERS
- a template with slot "modell" renders without an error
- the refusal omits the bad name

## TESTS
unknown slot and unknown when → named refusal; the known vocabulary unchanged · neighbourhood `test_harness_template.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/harness_template.py · tests.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
