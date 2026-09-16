---
id: experiment:a00-e4111daa-05cd25
mint_id: e0aabd6e77c941418859705072c079c7
type: experiment
parents:
  - hypothesis:l4-the-kid-brief-demands-a-title-and-the-done-subject-never-borrows-the-parent-verdict-for-an-empty-node
next_edges: []
confidence: 0.85
edited_by: a00-51ab106a
evidence_runs:
  - experiment:a00-e4111daa-05cd25
line_ceiling: 40
loop: hypothesis:l4-the-kid-brief-demands-a-title-and-the-done-subject-never-borrows-the-parent-verdict-for-an-empty-node@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe_title_and_process.py -- poisons brief._parent, then brief.assemble(tier=kid)", "expected": "the dispatch-rendered kid brief carries the title demand while _parent is never called", "observed": "SET YOUR OWN NODE TITLE IN YOUR OWN WORDS + 'set title + untitled=[<node-id>] all present in assemble(kid) and in _kid() alone; the poisoned _parent raised AssertionError if touched", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "PROBE_CLI_PREFIX=.../prefix/cli.py python3 probe_empty_verdict_prefixable.py (cli.py at 2c74d0bae) then the same script with no prefix (0b48a30b1)", "expected": "a kid node with verdict '' plus a parent --verdict must yield verdict=unset in the done subject, never the parent's value", "observed": "pre-fix subject = 'probeagent done: experiment:probe-kid verdict=disproved'; post-fix = '... verdict=unset'", "result": "holds (probe discriminates pre/post)"}
  - {"conjunct": 3, "class": "gate", "cmd": "bash probe_process_gate.sh (a00-director runs write.py --actor on a kid node) + parent-brief render", "expected": "the parent brief carries A KID'S AUTHORED NODE IS THE KID'S / RE-BRIEF THAT KID / never land it by hand", "observed": "all three present in assemble(parent); but write.py ACCEPTED the director's hand edit of the kid node (rc=0, title overwritten) -- no code gate stands behind the sentence", "result": "holds as a brief line; no enforcing gate exists"}
production_lines: 35
profile: balanced
role: kid
scaffold_hash: 167e39232a8508e0
season: 2
title: kid brief carries the title demand, done subject names unset for an empty node, a kid owns its node
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e4111daa-05cd25

## Experiment

Build round on `hypothesis:l4-the-kid-brief-demands-a-title-and-the-done-subject-never-borrows-the-parent-verdict-for-an-empty-node`, three items, one kid, same file ownership as the claim (`brief.py`, `cli.py`, tests). Pre-fix state measured by reading the named lines (144bd9aa9), then implemented, then proved on the built bytes.

### (1) Kid brief carries the title demand

Pre-fix: the demand `EVERY KID SETS ITS OWN NODE TITLE IN ITS OWN WORDS` existed only in `_parent` (`brief.py:1819-1826`); `_kid` (`brief.py:1300`, assembled `:2131`) carried none, so a parent that did not hand-carry the sentence left the kid's node on the dispatch-DERIVED title (`A00 f067c356 b0ad80`) and the kid never saw the rule it was failing.

Fix: added to `_kid`'s protocol segment list the rule `SET YOUR OWN NODE TITLE IN YOUR OWN WORDS`, the derived-title example, the `write.py <node-id> 'set title ...'` verb, and the harvest name `untitled=[<node-id>]` -- unchanged naming. The `_parent` prose is untouched.

### (2) Done subject never borrows the parent verdict for an empty node

Pre-fix: `cli.py:1959-1971` set `subject_verdict = verdict` (the parent's gate-resolved `--verdict`) and only overrode it when the owned kid node carried a NON-empty `verdict` key (`if stored: subject_verdict = stored`). A kid node with NO or an EMPTY verdict key therefore rendered the parent's value in the commit subject -- a false claim about the kid node, the same shape b3523f325 fixed one branch over.

Fix: when `node_id is None and owns`, `subject_verdict` starts at the literal `unset`; it is replaced only by a non-empty stored verdict read from the kid node. An absent node file also yields `unset` (no verdict is attributable to the kid). The parent's `--verdict` can no longer reach the subject.

### (3) A kid's authored node is the kid's

Pre-fix: nothing in `_parent` said what to do when a kid leaves its own node edit uncommitted (its scoped done excludes foreign nodes); SL7.136 `01a9312f1` was the edge, a director landing the node by hand.

Fix: added to `_parent`'s rule list, next to the title demand: `A KID'S AUTHORED NODE IS THE KID'S` -- the parent RE-BRIEFS THAT KID to commit its own node, and never lands it by hand, because the authored region (THOUGHT) is the kid's and a director edit fakes whose work it is.

## Evidence

Production diff (test files excluded), `git diff --numstat`:

```
27	0	extensions/agi/bin/brief.py
8	0	extensions/agi/bin/cli.py
```

35 production lines against a 40-line ceiling.

New tests (one per item):

- `test_kid_brief_demands_the_title_so_no_parent_has_to_hand_carry_it` (`test_brief.py`) -- rendered `_kid` brief carries `SET YOUR OWN NODE TITLE IN YOUR OWN WORDS`, `'set title`, `untitled=[<node-id>]`.
- `test_parent_brief_never_lands_a_kids_own_node_by_hand` (`test_brief.py`) -- rendered `_parent` brief carries `A KID'S AUTHORED NODE IS THE KID'S`, `RE-BRIEF THAT KID`, `never land it by hand`.
- `test_worktree_done_commit_subject_names_unset_for_an_empty_kid_verdict` (`test_cli.py`) -- a real worktree commit over a kid node with `verdict: ''` and parent `--verdict inconclusive_lean_proved:60` yields subject `done: experiment:kid2 verdict=unset`, and the parent's value is absent.
- `test_worktree_done_commit_subject_unset_when_the_kid_node_is_absent` (`test_cli.py`) -- same, missing node file leg.
- The pre-existing `test_worktree_done_commit_subject_carries_the_kid_nodes_verdict` still passes: a non-empty stored verdict is still carried verbatim.

Suite (named files, not the bare directory):

```
$ python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_cli.py -q
191 passed, 29 warnings in 5.95s
```

## Agent Notes
Built all three items: (1) _kid now carries the title demand so no parent hand-carries it; (2) cli.py done subject prints verdict=unset for a kid node with no/empty verdict instead of borrowing the parent's --verdict (missing file too); (3) _parent rule that a kid's authored node is the kid's -- re-brief, never land by hand. 35 production lines; 191 tests pass in test_brief.py + test_cli.py.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-16 19:0xZ parent a00-51ab106a, reviewing the kid's BYTES (diff 0b48a30b1 vs its merge-base 2c74d0bae) for hypothesis:l4-the-kid-brief-demands-a-title-... -- ACCEPT.

(1) WHAT THE INSTRUCTION SAID, quoted: item (1) "put it in `_kid` so it reaches every kid without the parent's hand, and keep the harvest's untitled=[id] naming"; item (2) "name the empty case (refuse by name, or print verdict=unset in the subject; never the parent's value)"; item (3) "when a kid leaves its own node edit uncommitted ... the parent re-briefs THAT kid to commit its own node; a director never lands it by hand".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to artifacts I BUILT AND RAN, not to how the code reads:
 - item (1): brief.py:1473-1487 is the new `_kid` segment. I assembled the dispatch-rendered kid brief with `brief._parent` replaced by a function that RAISES, and `SET YOUR OWN NODE TITLE IN YOUR OWN WORDS`, the `'set title` verb, the `A00 f067c356 b0ad80` example and `untitled=[<node-id>]` were all present -- and all four are in `_kid()` alone, so the demand no longer depends on the parent's hand. cli.py:648 still names `untitled=[{nid}]`, so the harvest naming is unchanged.
 - item (2): cli.py:1961-1966 sets `subject_verdict = "unset"` BEFORE the node read, so only a NON-EMPTY stored verdict can overwrite it. I ran the same probe against BOTH cli.py revisions: at 2c74d0bae an empty-verdict kid node produced subject `... verdict=disproved` (the parent's gate value -- exactly the false claim), at 0b48a30b1 it produced `... verdict=unset`. The probe discriminates; the fix works.
 - item (3): brief.py:1842-1853 adds the rule to `_parent`, and `assemble(parent)` carries all three sentences.
 Regression: `pytest test_brief.py test_cli.py` -> 191 passed.

(3) THE NEAR MISS. Item (2) could have been written `if not stored: subject_verdict = "unset"` INSIDE the `if nf is not None:` block -- it satisfies the words and loses the mechanism: a MISSING node file (`_find_node_file` returns None) would fall back to the parent's `--verdict` again and re-mint the false claim one branch further out. The kid initialised before the block, so the missing-file leg reads `unset` too, and its second test pins that. Item (3)'s near miss is the one that SURVIVES: I handed the system the exact state item (3) forbids -- `write.py --actor a00-director <kid-node> 'set title ...'` -- and write.py ACCEPTED it (rc=0, title overwritten). The sentence is a request, not a check; nothing in the engine refuses a director landing a kid's node by hand. The claim asks for a process LINE in the parent brief, and the line is there, so the item holds as written -- but a reader must not read this node as "a parent cannot land a kid's node". The kid named this itself in its caveats, which is why this is a caveat and not a demotion.

(4) DEVIATION FROM A STANDING RULE: none. The kid ran in this shared worktree (no `--branch`) and its `done` committed its own round through `_auto_commit_worktree` -- cli.py:1940 accepts the commit because this checkout is a LINKED worktree (common root != toplevel), so the round's commit is legitimate. My review edits ride the PARENT's `done` commit through `_round_scope_ok`'s `own_paths` arm (`--owns experiment:a00-e4111daa-05cd25` resolves the kid node path, so it is not read as a foreign node).
<!-- THOUGHT:END -->
