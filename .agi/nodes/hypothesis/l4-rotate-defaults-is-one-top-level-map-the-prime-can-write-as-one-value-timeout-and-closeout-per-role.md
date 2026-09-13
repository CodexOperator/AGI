---
id: hypothesis:l4-rotate-defaults-is-one-top-level-map-the-prime-can-write-as-one-value-timeout-and-closeout-per-role
mint_id: 3b09e68640c24947bd17818242352106
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 269c2013e98b808e
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (SM order 23:43Z; master-sensei verified 23:42Z by write.py --dry-run on MAIN: write.py has NO dotted nesting — 'set templates.director.timeout_s 900' writes a FLAT key and 'set templates director.timeout_s 900' DESTROYS the templates map — so the SL7.114/115 readers read keys the Prime can never write). MEASURED on the post tip: `_role_timeout(root, role)` rotate.py:14400-14415 reads `_load_templates(root)[role]['timeout_s']`; `cmd_rotate` :16656, closeout block :16702-16715 reads `_load_templates(root)[role]['rotate_defaults']` (a map, closeout: bool); `_ranks(root)` :14359 reads the TOP-LEVEL `ranks:` (already writable as one value — unchanged); tests test_rotate_verb_resolvers.py:153 `test_role_timeout_from_template_or_default`, :178 the digit-string test, test_rotate_verb.py closeout coverage around :216. CLAIM: (1) ONE top-level config:rotations map `rotate_defaults` the Prime writes as ONE JSON value — shape {\"timeout_s\": {\"prime_director\": 900, \"director\": 900, \"helper\": 600}, \"closeout\": {\"<role>\": bool}} — replaces both per-template reads: `_role_timeout` reads rotate_defaults.timeout_s.<role> (int or digit-only string, else 600), cmd_rotate's closeout default reads rotate_defaults.closeout.<role> (else False); the old templates.<role>.timeout_s / templates.<role>.rotate_defaults reads are DELETED, not kept as fallbacks (a key nobody can write is dead code); (2) `_load_rotate_defaults(root) -> dict` is the ONE reader both call (frontmatter top-level `rotate_defaults`, {} when absent/not a map); (3) ranks stays top-level and untouched; (4) the kid node body carries EXACTLY TWO 0a lines for the Prime, each PROVEN by `write.py config:rotations '<line>' --dry-run` on the round's tree with the dry-run output quoted in the node: `set ranks [\"prime_director\",\"director\",\"helper\"]` and `set rotate_defaults {\"timeout_s\": {\"prime_director\": 900, \"director\": 900, \"helper\": 600}, \"closeout\": {}}` — the round NEVER writes config:rotations, and the lines must not run until this lands on main. FALSIFIERS: a dotted-key read left anywhere; a fallback to templates.<role>.*; a third reader; an unproven 0a line; a write to config:rotations. TESTS: update the two timeout tests (:153, :178) to the new shape + 1 closeout test reading rotate_defaults.closeout.<role> true/false/absent; <= 4 total touched. FILE SCOPE: rotate.py (`_load_rotate_defaults`, `_role_timeout`, the closeout block in cmd_rotate), test_rotate_verb_resolvers.py, test_rotate_verb.py. EXCLUDED: `_ranks`, `_caller_post`, `_rank_gate`, `_default_stops_text`, cmd_rotate_self, the checklist, config:rotations itself, `_compose_after_join_dm` (SM.01). CEILING: <= 30 lines; rotate nbhd green."
thought_session: sensei-director-genXVIII-L18
title: rotate_defaults is ONE top-level config:rotations map the Prime writes as one JSON value (timeout_s + closeout per role) — the SL7.114/115 per-template reads named keys write.py cannot nest (SM 23:43Z; master-sensei 23:42Z dry-run)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-defaults-is-one-top-level-map-the-prime-can-write-as-one-value-timeout-and-closeout-per-role

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
