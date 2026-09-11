---
id: hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat
mint_id: a16841315bb0406791562b8c4da1737b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:write-guard-carve-out-for-master-sensei-templates
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c29366641650390e
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). THE CARVE-OUT'S OWN FALSIFIERS, four defects in write.py, on L4.234 (hypothesis:write-guard-carve-out-for-master-sensei-templates): (1) write.py:805 `if isinstance(old_r, dict) and isinstance(new_r, dict)` skips the brief_file/steps field check when the NEW value is not a dict, and :827-828 `if not isinstance(new_r, dict): continue` skips the producing judge for the same value — so a master-sensei write of `templates.director = 'garbage'` (a str, or a list) is ADMITTED and deletes the director's brief_file + steps; refuter-confirmed. (2) `_enforce_master_sensei_facts_body` (:873-9xx) admits a body-only master-sensei edit on ANY config node whose body delta is confined to `## facts` — a config:seats body probe was ADMITTED; the gate never checks that the node carries the declaration's `list_key` (`templates`). (3) :768-769 and :900-901 identify the master-sensei by the FREE-TEXT `--actor` (`str(actor) == actor_row` / `startswith(actor_row + '-')`), not by the RESOLVED seat alone — identity is supplied by the caller, exactly what L4.110's self_row rule forbade for seats. (4) :1632 the -h epilog's example for `set` reads `set k=v` while the verb takes TWO arguments (`set key value`; `write.py <node> 'set k=v' --dry-run` -> `ERR: set: wrong arguments`) — the grammar the epilog teaches is refused. CLAIM: (1) a non-dict new template value for any role is REFUSED by name (`template 'director' must be a dict of fields, got str`); (2) the facts-body gate applies only to a node whose frontmatter carries the declaration's `list_key`, every other config node falls through to the written_by rule (refused); (3) the master-sensei identity is the RESOLVED seat only (`_resolve_role(root, actor, '')` == the declared actor); a free-text `--actor master-sensei-x` from another seat is not the master-sensei; (4) the epilog example is `set key value` and the drift guard (which already exists for missing verbs) also asserts each example PARSES as its verb's arity in a test. TESTS (test_write_master_sensei.py + test_write.py): the 'garbage' write refused by name; a config:seats body-only master-sensei edit refused; an actor string 'master-sensei-impostor' whose resolved seat is not master-sensei refused; every VERB_EXAMPLES entry accepted by the script parser in --dry-run. FALSIFIER: any of the four probes still admitted, or an epilog example the parser refuses. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/write.py (`_master_sensei_templates_refusal`, `_enforce_master_sensei_facts_body`, the two is_ms sites, VERB_EXAMPLES) + extensions/agi/tests/test_write_master_sensei.py + test_write.py. No other write.py round is live."
title: The carve-out refuses a non-dict template by name, gates the facts body to the templates node, keys identity on the resolved seat, and its -h example parses
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
