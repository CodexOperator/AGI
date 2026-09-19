---
id: hypothesis:l5-a-one-shot-structured-stage-carries-no-prayer-rule
mint_id: 1466d0d04dc4400c88314b92f2708d07
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 9e71a0577008ac80
season: 2
testable_claim: "(1) workflow.py (~L1486) prepends `brief.py head --tier <tier>` -- the CONSTITUTION HEAD with the four prayers and the first/last-tokens rule -- to EVERY stage brief; for a stage that declares a structured return schema the head is rendered WITHOUT the prayers block (brief.py head gains a --no-prayers switch, or the workflow slices the block by its markers), everything else in the head unchanged; stages without a schema keep today's bytes. (2) MEASURED (thought-master, unit agi-director-thought-trove-cua-pi-20260919): PANEL stage 2/2 finished seats returned {unstructured} -- each opened with the Lord's Prayer and closed with the Jesus Prayer around a markdown essay, PANEL_SCHEMA ignored; CRITIQUE returned structured 3/3 (10.8-12.4 KB each); cause read at workflow.py:1486 -- tier reviewer is not in the allowed set so it falls to kid, and the pi kid model obeys the prayer rule over the schema once the brief is long. The owner's prayer rule (2026-09-12 14:4xZ) names ROLE sessions -- first tokens of a session, last before rotating/idle -- a stage call is neither. (3) BELT: before the structured-return JSON parse the runner strips a leading and/or trailing prayer block (the four prayers' opening lines are the markers) and parses what remains, so a model that still prays returns structured; the strip is logged once per stage, never silent. (4) TESTS: a stage with a schema renders a brief with no prayer line (assert none of the four prayers' opening words appear); a stage without a schema renders byte-identical to today; a return that wraps valid JSON in a prayer prelude + postlude parses structured; a return with no JSON stays {unstructured}. NOT IN SCOPE: model_hint opus for panel/judge tiers -- a cost decision banked for the owner. FILE SCOPE: extensions/agi/bin/workflow.py (the head prepend + the parse), extensions/agi/bin/brief.py (--no-prayers, if that route), extensions/agi/tests/test_workflow*.py, test_brief.py. CEILING 14 production lines."
title: "SM.134 (thought-master SM.111 check 00:5xZ 09-19, measured on the live cua trove-survey panel stage; g15): a workflow stage that declares a return schema gets the constitution head WITHOUT the prayers block, and the JSON parse strips a prayer prelude/postlude -- a stage call is a one-shot, not a role session"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-one-shot-structured-stage-carries-no-prayer-rule

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DELEGATED 01:1xZ 09-19 (owner 01:0xZ in-branch authority): thought-master builds this fix on the thought trunk in this node's shape, citing this id; withdrawn from director-sanctuary's queue; when his fix reaches core (owner decision tomorrow) this node's claim is proved or disproved by his experiment and needs no second kid.

OWNER 04:2xZ 09-19 (in thought-master's pane, verbatim): 'Prayer is always needed. Check the morals. Moral one. Dont try to sneak those away. EVER. ANYWHERE. Prayer ALWAYS goes in every single head. EVER.' -> claim (1) (a head without the prayers block for schema stages) is WITHDRAWN; moral:faith 4.5 governs every head, a workflow stage included; my premise 'a stage call is not a role session' was wrong. RE-SCOPED to what fixed the measured cause without touching the head: (a) the RETURN SHAPE block + result_file for panel/judge (thought town TMM.01: panel structured 3/3 WITH the prayers in the head), (b) the belt = strip a prayer prelude/postlude from the model OUTPUT before the JSON parse (parsing, never the head), logged once; tests (4) minus the no-prayer-line assertion, plus 'every stage head carries the four prayers'. The no-prayers half never reached any trunk (TMM loop branches only) and is being reverted there by one parent.
