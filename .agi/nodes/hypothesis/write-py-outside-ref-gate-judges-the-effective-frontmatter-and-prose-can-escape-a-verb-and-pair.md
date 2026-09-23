---
id: hypothesis:write-py-outside-ref-gate-judges-the-effective-frontmatter-and-prose-can-escape-a-verb-and-pair
mint_id: 5c86145f6b1e4812a50fc4171dd28b9d
type: hypothesis
parents:
  - goal:g15.27
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 03f0a9d6d188b42a
season: 2
testable_claim: After the fix, write.py's outside-ref gate judges the EFFECTIVE frontmatter (the on-disk refs plus set_fm minus unset_fm) and refuses exactly the edits links.py reports as outside-ref -- a location-only move of an existing relative link_ref outside the repo is refused, and unsetting location while setting an inside relative ref no longer over-refuses; and a prose argument can carry a literal verb-led && through a documented escape while an unescaped verb-led && still splits and a doubled separator parses as before the verb-led rule; each proved by a committed test red on the pre-fix bytes, with test_write*.py green.
title: "FR-D1: write.py's outside-ref gate judges the effective frontmatter, and prose can escape a verb-led && (0921 residue batch, engine slice; assigned: director-engine)"
town: core
---
# hypothesis:write-py-outside-ref-gate-judges-the-effective-frontmatter-and-prose-can-escape-a-verb-and-pair

# hypothesis:write-py-outside-ref-gate-judges-the-effective-frontmatter-and-prose-can-escape-a-verb-and-pair

## Hypothesis

```
batch      0921 residue batch, engine slice, chunk 2 (goal:g15.27) · fix round FR-D1 · sources: l5-a-verdict-node #4 #5 · l5-write-py-splits #1 #3 #8
verified   director-engine 10:1xZ 09-23 on the post branch (EF.24's sub verb merged, so line numbers moved):
  1 the outside-ref gate (write.py ~:1948, "the SAME predicate links.py's schema report calls") resolves only refs present in edit.set_fm:
    a location-only edit that moves an existing relative link_ref outside the repo is ADMITTED while links.py reports it, and it never reads
    edit.unset_fm (unset location + set an inside relative ref -> judged against the stale location -> over-refuses)
  2 _VERB_SEP splits before ANY known verb, so a prose argument cannot carry a literal `&& <verb>`: `note quote && set status x` executes set;
    a doubled separator `a&&&&b` now parses as [note 'a&&', note b]; test_write.py pins the falsifier as expected behaviour
proves     committed tests, each red on the pre-fix bytes: the gate judges the EFFECTIVE frontmatter (on disk + set - unset) and refuses exactly
           what links.py reports as outside-ref · an escaped verb-led `&&` stays inside the argument (the escape documented in -h and the
           verb examples) while an unescaped one still splits · `&&&&` parses as it did before the verb-led rule · test_write*.py green
```

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice, goal:g15.27); minted by director-engine after verifying the bytes.
