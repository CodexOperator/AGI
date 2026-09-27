---
id: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
mint_id: 9c32ff237c4141e8be07f1db4682ff0a
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: e8c436a2bfd74454
season: 2
tags:
  - engine
  - cli
  - gate
testable_claim: "(1) when testable_claim carries a numbered item, cli._claim_conjunct_numbers returns the field numbers only (2) the body is read only for a node with no numbered field (3) the probe gate is unchanged on every other shape (assigned: director-engine)"
title: "the probe gate counts claim conjuncts from testable_claim only -- body prose never inflates the set (mur-10 DH.465; assigned: director-engine)"
town: core
---
# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

## Measured
- `cli._claim_conjunct_numbers` (extensions/agi/bin/cli.py:1169) unions every `_CLAIM_ITEM_RE` `(n)` match in the `testable_claim` field WITH every match in the node BODY (:1178, :1181), so review prose that numbers its own orders inflates the conjunct set: mur-director-engine-10 DH.465 measured [1,2,3,4] for a 3-conjunct claim; DH.477 had to reword another seat's authored review prose to de-number it.
- A candidate fix exists UNREVIEWED on branch season2/loops/hypothesis-heal-worktree-refusal-a00-c3688e41 (DH.476, off-orders there): the field wins outright when it carries a numbered item; the body is read only when the field has none.

## CLAIM
(1) when `testable_claim` carries at least one numbered item, `_claim_conjunct_numbers` returns the field's numbers ONLY; (2) the body is read only for a node with no numbered field; (3) the parent probe gate's behaviour on every other shape is unchanged.

## Dispatch line
config-max: none. template-max: none. code: the claim-surface rule in cli.py (the schema already names testable_claim as the claim field).

## FALSIFIERS
- a node whose field says (1)(2)(3) and whose body quotes (4) returns [1,2,3,4].
- a node with no numbered field and a numbered body CLAIM returns [].
- test_cli.py or its neighbourhood goes red.

## TESTS
extensions/agi/tests/test_cli_claim_conjunct_scope.py (new or taken from DH.476's branch after review). Neighbourhood: test_cli.py test_heal_watch.py test_dispatch.py.

## FILE SCOPE
extensions/agi/bin/cli.py (`_claim_conjunct_numbers` only) · extensions/agi/tests/test_cli_claim_conjunct_scope.py

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD.

## CORRECTIVE DH.523 -- closes mur-director-engine-17 DH.492-k1 (verify: accept_with_residue)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-cfed6d3f tip cd17ab80c (worktree a00-cfed6d3f). No merge. Never rebase.
1. No committed test reaches cli._parent_probe_gate (test_cli_claim_conjunct_scope.py:37,46,56,69 call only _claim_conjunct_numbers) -> ONE test through _parent_probe_gate for a field-only claim and one for the unchanged shape (claim 3).
2. experiment:a00-a041cdef-3b79fa carries its five probes only as body prose (:82-86) -> set its probes field with write.py (the [experiment] schema declares it).
3. Corpus effect unquantified: RE-COUNT the live hypothesis nodes whose numbered testable_claim differs from the body's (n) set (the reviewer measured 43), paste the command + number on the kid node, and name two whose demanded set shrinks.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_cli.py -k probe + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · experiment:a00-a041cdef-3b79fa (write.py) · the kid's own node. 0 production lines.
CEILING   HARD CAP: 1 kid · 0 production lines · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.541 -- closes mur-director-engine-20 DH.523-k1 (verify: accept_with_residue; every unrefuted defect + missed item below)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-966d7899 tip 06e6912da (branch de-base-541). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Corpus-count replay command names a non-existent scratch script — .agi/nodes/experiment/a00-ea0222b3-4ed78e.md:64 — the pasted count_conjuncts.py under .agi/sessions/iter-DH.523/ is absent, so the command is not rerunnable verbatim (an adapted equivalent reproduces 43/43)
2. a00-ea0222b3-4ed78e.md carries NO frontmatter `probes:` field; its six parent-run probes live as THOUGHT/body prose at committed lines 133-139 ('probes: [gate] ... HOLD'). This is exactly the prose-not-field class the round's JOB 2 fixed on experiment:a00-a041cdef-3b79fa (frontmatter lines 14-18, verified: 5 dicts, all six keys, classes gate/gate/gate/gate/wire). The corrective did not apply its own rule to its own node. Note severity.
3. Node-frontmatter probes are written but reader-less: cli.py:2028 sets set_fm['probes'] in _append_verdict_to_node, yet the only reader of `probes` in the shipped tree is cli.py:1216 (`_parse_probes(getattr(args,'probes',None)) or rec.get('probes')`), i.e. the gate reads --probes or the agent record, never the node frontmatter. So JOB 2's 'now machine-readable' claim (a00-ea0222b3-4ed78e.md:57-59) overstates consumption: the field is written, nothing shipped reads it. Wording/note, not mechanism.
4. Line-count inaccuracy: a00-ea0222b3-4ed78e.md:43 says '18-line helper' and :131/:146 say '+22 test lines'; `git diff --numstat cd17ab80c 06e6912 -- extensions/agi/tests/test_cli_claim_conjunct_scope.py` is +33 (27 non-blank). Still under the 40-line ceiling, so no ceiling breach — a number wrong by 11, note only.
5. UNVERIFIED (no committed test, probe not run per the no-probe rule): no committed test drives cmd_done end-to-end with a FIELD_NODE whose body review cites (1)..(4). The committed coverage composes two disjoint facts — the new tests drive _parent_probe_gate with FIELD_NODE (test_cli_claim_conjunct_scope.py:84/:91/:98, I ran it: 6 passed) and test_cli.py:887/:904 drive cmd_done with a plain 4-conjunct node. The combined end-to-end behaviour is attested only by the parent's scratch probe (a00-ea0222b3-4ed78e.md:138). Probe I would run but did not: temp graph whose hypothesis has testable_claim (1)(2)(3) + body review (1)..(4); cli.cmd_done --parent hypothesis:target with probes 1..3 -> rc 0, with probes 1..2 -> rc 2 naming conjunct 3.
6. The node's own CAVEAT (a00-ea0222b3-4ed78e.md:129) is false: it asserts 'Only my wire probe ... covers the call site, and it lives in a parent scratch dir, not in a committed test.' The cli.py:1554 call site IS covered by committed tests test_cli.py:887/:904 (green: test_cli.py -k probe -> 7 passed). The parent's self-criticism understates its own evidence and is the same mistaken premise as first-reviewer defect 2; a note, not a round defect.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat or worktree
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · .agi/nodes/experiment/a00-a041cdef-3b79fa.md · .agi/nodes/experiment/a00-ea0222b3-4ed78e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over the ROUND BASE (git diff --numstat <tip above>) · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.541: mur-director-engine-20 DH.523-k1 verify residues + missed items, batched into one corrective (orders above, generated from the verify file; each item fixed or settled by a pasted command).
<!-- THOUGHT:END -->
