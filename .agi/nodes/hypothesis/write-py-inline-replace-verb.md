---
id: hypothesis:write-py-inline-replace-verb
mint_id: e1502cae0bf2449dab223d1a7f5e75f5
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 09:0xZ, goal:g5): after the brief.py round; build loop; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 36373c39b7d848c6
season: 2
tags:
  - write
  - verb
  - config-max
testable_claim: write.py <node> sub <old> => <new> replaces exactly one literal occurrence anywhere in the node file (frontmatter or body; the payload with sub payload), refuses 0 or 2+ matches writing nothing, re-runs the node gates, and prints the diff on --dry-run.
thought_session: belam-S2-L5-I
title: "write.py in-line replace verb — sub <old> => <new>: exact literal, one match, frontmatter/body/payload, no file, no diff"
town: local-maxxing
---
# hypothesis:write-py-inline-replace-verb

# write.py gets an in-line replace verb — `sub <old> => <new>`: exact literal, one match, any region, no file, no diff

**Owner 2026-09-23 09:0xZ (Prime pane, filed on `goal:g5`):** "Write py should have an in-line replace option"

**Assigned: director-engine** (the Prime, 09-23) · build loop · after the brief.py round · one `[merge-up]` to thought-master.

## Measured (the Prime, 09-23, this tree)
```
verbs today   replace body N:M <file> · body_patch <diff> · patch <diff> (payload) · payload_text · set <field> <whole value> · note · thought
gap           a one-line change needs a file or a unified diff · config FRONTMATTER (config:rotations templates, config:posts rows) has no line edit:
              changing one first_turn entry = `set templates <the whole nested value>`
refusal       replace body N:M refuses a range that splits a heading from its section
```

## CLAIM
`write.py <node> 'sub <old> => <new>'` replaces the ONE exact literal occurrence of <old> with <new> anywhere in the node file (frontmatter or body; the payload with `sub payload <old> => <new>`), in place:
```
the FIRST ` => ` separates old from new · exact literal, no regex
0 or 2+ matches ─▶ REFUSED, nothing written · `sub! <old> => <new>` = every match, the count printed
the node's gates re-run unchanged (schema · ring · anonymize · write-guard) · --dry-run prints the unified diff
rides a script like any verb: `sub a => b && note why`
```

## Dispatch line
config-max: none (a verb, not a value) / template-max: the verb's one-line example joins VERB_EXAMPLES and -h / code: the sub verb in write.py (parse, match count, a frontmatter-safe write through the existing gates)

## FALSIFIERS
- a `sub` on a frontmatter value writes a node that the schema or ring gate refuses through `set`
- 0 or 2+ matches write anything
- a `sub` on a config node skips the ring gate

## TESTS
- one match → replaced, the diff on --dry-run · 0 / 2+ → refused, the file byte-identical · a frontmatter line on a config node through the ring gate · payload mode · a non-verb-led `&&` inside <old>/<new> stays in the argument
- neighbourhood: `test_write*.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/write.py (the verb) · its tests. Nothing else.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
