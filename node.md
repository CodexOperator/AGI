---
id: hypothesis:links-py-flags-live-references-to-retired-goals
mint_id: 81d505c84adf4256a224450b30cf3958
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 09:1xZ, goal:g5): after the brief.py and write.py rounds; build loop; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 4700539a9bc828ba
season: 2
tags:
  - links
  - lint
  - renumber
testable_claim: links.py links reports a retired count — every live frontmatter reference, config cell or live instruction-surface mention of a goal id whose node is retired or absent, with the successor its THOUGHT records — exits 1 under --strict, and exempts deprecated nodes, THOUGHT blocks and history fields.
thought_session: belam-S2-L5-I
title: links.py flags every live reference to a retired or missing goal id — frontmatter, config cells and live instruction surfaces
town: local-maxxing
---
# hypothesis:links-py-flags-live-references-to-retired-goals

# links.py flags every live reference to a retired or missing goal id — frontmatter and live instruction surfaces

**Owner 2026-09-23 09:0xZ-09:1xZ (Prime pane, verbatim on `goal:g5`):** "So no one uses old designations like g14 and g13" then "Assign it, but fix the commands table now."

**Assigned: director-engine** (the Prime, 09-23) · build loop · after the brief.py and write.py rounds · one `[merge-up]` to thought-master.

## Measured (the Prime, 09-23, this tree)
```
by hand today   2 live frontmatter refs to goal:g14 (one minted the same morning) · 3 config:posts owning_goal cells (g14, g14.3, g14.14)
                · 18 live-surface files citing g13/g14 · the commands tables cited 5 dead ids (g9.7, g13.1, g8.2 = no node; g11, g6.5 = retired)
links.py links  0 broken the whole time: a retired node still RESOLVES, so nothing flags its use
```

## CLAIM
`links.py links` gains a `retired` count (and `--strict` exit 1 when it is non-zero): every live reference to a goal id whose node is `retired` or absent, with the successor when the retired node's THOUGHT records one:
```
scanned   live node frontmatter (parents, owning_goal, links) · config cells · extensions/agi/briefs/ · .agi/sessions/quorum/ cards · CLAUDE.md · QUICKSTART.md · SKILL.md
exempt    .agi/nodes/deprecated/ · THOUGHT blocks · history fields (outcome lens / judged_against) · notes on retired nodes
output    one line per hit: <file>:<line> <old id> → <successor | none>
```

## Dispatch line
config-max: the scanned and exempt lists as one config cell / template-max: the output line format as a template line / code: the retired-id resolver in links.py and the --strict exit

## FALSIFIERS
- a live frontmatter reference to a retired goal passes silently
- a history field or a THOUGHT block is flagged
- adding a surface to scan needs a code change

## TESTS
- a tmp graph with a retired goal referenced from a live node, a card and a history field → exactly 2 hits · --strict exits 1 · the successor is read from the THOUGHT · a surface added by config is scanned
- neighbourhood: `test_links*.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/links.py · the one config cell · tests. Nothing else.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
