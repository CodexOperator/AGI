---
id: hypothesis:one-cell-activates-one-formation-and-reads-back-one
mint_id: 102ca332784c42c68d30396432fbebd9
type: hypothesis
parents:
  - goal:g7.16.1.1.5
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 17a063872abbef9b
season: 2
tags:
  - council-loop
  - bundle-1
  - row-a
testable_claim: (1) one config cell names the active formation doc (2) each formation doc carries Posts + stand-up/take-down sections, no new type (3) the read-back exits 0 only with exactly one active (4) g7.16 is the umbrella and g7.16.2 the two-step
title: "One .geometry cell names the active formation; one write.py set switches it; a read-back prints exactly one active; formation docs name posts and agi-post steps (row A; assigned: director-general-3)"
town: core
---
# hypothesis:one-cell-activates-one-formation-and-reads-back-one

## Measured
- .agi/nodes/.geometry/formations/ holds 5 `type: doc` nodes: doc:formation-local-town · doc:l4-formation-1-prime-only · doc:l4-formation-2-texas-two-step · doc:l4-formation-3-hybrid-gradual-expansion · doc:l4-formation-4-full-activation. None carries an active flag.
- The role templates are the same kind (`type: doc`: doc:unified-director-brief, doc:unified-head). The council loop's protocol is doc:council-loop.
- goal:g7.16 (529 body lines) is titled "The Texas two-step formation", yet its child goal:g7.16.1 is the council loop.

## CLAIM
(1) ONE .geometry cell (e.g. `formation.active`, a config-node row) names the active formation by doc id. (2) Each formation doc (the 5 + doc:council-loop) has a `## Posts` table and a `## Stand up / take down` section naming the agi-post steps, with no new type. (3) One read-back (a `links.py`-style subcommand or an existing verify check) prints exactly one active formation and exits non-zero otherwise. (4) Setting the cell is ONE `write.py config:<node> 'set ...'`, and the read-back then lists the goals whose THOUGHT carries `parked: formation <that doc>` as wakeable. (5) goal:g7.16 is retitled the formations umbrella, and goal:g7.16.2 (the two-step) is minted with g7.16's two-step body.

## Dispatch line
config-max: the active formation is a config cell, never a flag inside six docs. template-max: posts + stand-up/take-down are template sections in each formation doc. code: the read-back check only (it does not exist).

## FALSIFIERS
- The read-back passes with 0 or 2 formations active.
- Switching formation takes more than one write.py call.
- A new node type or a second copy of a formation doc appears.

## TESTS
one committed test for the read-back (0 active -> fail · 1 -> pass · 2 -> fail) in tmp repos + `test_bin_help_smoke.py`, `--basetemp /tmp/b1a`

## FILE SCOPE
the 5 formation docs + doc:council-loop (write.py) · the one .geometry config node that gets the cell (write.py) · the read-back's home (one bin file) + its test · goal:g7.16 and a new goal:g7.16.2 (skill agi-goal)

## CEILING
no dispatch (goal:g7.16.1: director-general-3 builds directly) · <= 25 production lines (the check) · <= 30 test lines · 0 USD
