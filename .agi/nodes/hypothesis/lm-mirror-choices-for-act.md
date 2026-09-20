---
id: hypothesis:lm-mirror-choices-for-act
mint_id: a90b3432a27e405ba6d777b9b306d41a
type: hypothesis
parents:
  - goal:g5.6
  - hypothesis:lm-graph-sql-mirror
next_edges: []
ceiling: $0.50 OpenRouter; $0 compute; file scope = .agi/context/local-maxxing/sql/{graph2sql.py (hardening only), choices.py, test_choices.py, replay_choices.py, choices_replay.jsonl, prompts/*.md} + the kid experiment node + this node.
edited_by: belam
falsifier: "Menu recall < 0.90 (the graph-legal set does not contain what the loop actually did: the schema, the scope rule or the query is wrong -- fix the query, not the replay), or median menu > 30 (the graph does not limit), or any query > 50 ms, or the hardening still leaves a zero-byte db -- then the mirror is a reporting surface only and R2 builds its menus from the tool roster alone."
scaffold_hash: 0917f86249057978
season: 2
testable_claim: "On the landed graph2sql.py (hypothesis:lm-graph-sql-mirror, TM.31) with NO rewrite: (1) hardening -- a query on a missing or zero-byte db builds first (or exits 2 with one line), never leaves a zero-byte file; a test covers it; (2) a choices(act, ...) query family in sql/choices.py over the mirror: spawn-parents(type) = the schema-legal parent ids in scope (allowed_parents x live nodes of those types under the same goal/town), verdict-words(hypothesis) = the six words filtered by evidence_runs (proved/disproved need >= 1), next-hypotheses(goal) = open (pending) hypotheses under the goal ordered by last note date, review-acts(merge-up) = accept / accept_with_residue / demote, next-call(kid) = the roster of that kid round; every query returns a numbered list of (index, id, one-line title) and runs < 50 ms on the 3.5k-node mirror; (3) MENU RECALL on a 200-act replay sampled from the graph (50 spawns with their recorded parents, 100 verdicts, 50 review decisions from merge-up-review.jsonl): the recorded choice is in the menu for >= 95% of acts, median menu size <= 12 and p90 <= 40 (recall high, menu small = the choice-limiting claim in numbers); (4) one rendered prompt per act type written to sql/prompts/<act>.md as the shape R2 (hypothesis:lm-jev-next-call-suggestion) consumes: numbered options, ids, the answer format an index + confidence."
tests: ONE pi parent + ONE kid, A1-light slot (ARM4C; after the CRITICAL A1 halves bend2 -> pufferlib, before C2.03); $0.50 OpenRouter cap, $0 compute, no downloads; kid line_ceiling 150 (choices.py + tests + the replay script + prompts); rows to sql/choices_replay.jsonl (act, menu size, recall hit, ms); mur by name (links gate; nothing under extensions/ is touched).
thought_session: dissolve-legacy-2026-09-19
title: "The SQL mirror as the choice-limiting engine: a choices-for-act query family returns the graph-legal option menu for a loop act (spawn under a parent, verdict on a hypothesis, next call for a kid, accept/demote on a merge-up) in < 50 ms, the recorded act is IN the menu for >= 95% of 200 replayed acts, and the median menu is <= 12 options -- the menu jev chooses from, plus the query-before-build hardening"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-mirror-choices-for-act

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 04:59Z (thought-master pane), verbatim: "I was thinking we could use the DB mirror to dynamically build jev prompts since it’s basically multiple choice and graph is the choice limiting engine." -- this node is the first application: the menu comes from the mirror; jev picks. Banked question for the owner (not built): should the menu BE the gate -- a kid may only pick from what the schema allows, so an illegal act is unrepresentable instead of refused after the fact?
