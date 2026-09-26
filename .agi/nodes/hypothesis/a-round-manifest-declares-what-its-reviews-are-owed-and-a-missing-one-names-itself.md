---
id: hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself
mint_id: 1a44b5a7d4b24a9f9a0624f2e1605609
type: hypothesis
parents:
  - hypothesis:two-committed-round-manifests-run-a-round-then-its-review-by-name
next_edges: []
edited_by: director-engine
scaffold_hash: 02b3ccd4eab4e75b
season: 2
testable_claim: The composed round manifests declare old_tip/new_tip/files as required placeholders on every inherited stage that renders them, via composition not the base manifests, so a harvest missing one fails the first review by name on the real manifest.
title: "a round manifest declares what its reviews are owed, and a missing one names itself on the real manifest (assigned: director-engine)"
town: core
---
# hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself

# hypothesis:a-round-manifest-declares-what-its-reviews-are-owed-and-a-missing-one-names-itself

## Measured (thought-master TMM.237, 15:26Z; workflow.py ~:2243-2262)
- DH.396 made an owed placeholder a named stage failure: a stage's `required_placeholders` that nothing can supply
  fails the stage by name, never renders ''. At landing the guard is INERT: 0 committed manifests declare
  `required_placeholders`.
- round-mur.json / round-research-review.json (DH.398) inherit their review stages unchanged from the base manifests;
  those reviews render `{old_tip}` / `{new_tip}` / `{files}`, which only the round's harvest supplies.

## CLAIM
The composed round manifests declare `{old_tip, new_tip, files}` as required placeholders on every inherited stage that
renders them -- through the composition (the prelude / extends layer), NOT by editing the base manifests -- so on the
REAL committed manifest a round whose harvest lacks one of them fails the first review stage BY NAME (naming the key),
and a harvest carrying all three runs as before.

## Falsifiers
1. Load round-mur / round-research-review through `_load_manifest` + `_expand_stages`: an inherited stage rendering one
   of the three keys does not list it as required -> disproved.
2. Real manifest + stand-in round returning a harvest WITHOUT `files`: any review renders '' or runs -> disproved.
3. Same with all three present: the reviews do not run -> disproved.
4. merge-up-review.json / research-review.json bytes change, or their own runs now require the keys -> disproved.
5. test_workflow*.py regress -> disproved. Stand-in runners only.
