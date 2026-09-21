---
id: experiment:a00-35cfe009-262616
mint_id: 109d7e603edd4cf7874d50a11f33e114
type: experiment
parents:
  - hypothesis:l4-a-test-of-live-config-reads-the-live-node
next_edges: []
confidence: 0.9
edited_by: a00-f5d4a552
evidence_runs:
  - experiment:a00-35cfe009-262616
loop: hypothesis:l4-a-test-of-live-config-reads-the-live-node@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: da741489cefcdb4f
season: 2
title: A00 35cfe009 262616
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-35cfe009-262616

## Experiment

g15 CLAIM-BUILD (hypothesis:l4-a-test-of-live-config-reads-the-live-node, the
third instance of the L4.191 shape). `test_rotate_startup.py::test_git_live_
template_commands_still_pass` still asserted a HAND-COPIED two-string list
(`shipped = ["git -C {worktree} status -sb", "git -C {repo} status -sb"]`)
instead of reading the live `.agi/nodes/.geometry/rotations.md`, so a NEW
off-allowlist git line added to the live node (which at lines 37 and 73 ships
`git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3`
inside `templates.*.startup.first_turn`) would NOT turn the test red.

BUILT, copying the L4.191 pattern (test_rotate_templates.py`_live_first_turn`):
1. Dropped the hand-copied `shipped` list.
2. Added `_live_first_turn_cmds()` reading the live rotations.md via
   `graph_core.persistence.frontmatter`, collecting every `startup.first_turn`
   cmd from BOTH templates (director and prime_director).
3. The test now filters for git-bearing cmds, substitutes {worktree}/{repo}
   with real temp paths, and judges each with `rotate._producing_refusal`.
4. Added the one sentence to brief.py's kid review/tests paragraph ("A test of
   live config reads the live node, never a copied list.") and its assertion
   in test_brief.py `test_kid_brief_suite_line_names_test_files_not_the_bare_
   directory`.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` -> 55 passed.
- `python3 -m pytest extensions/agi/tests/test_brief.py -q` -> 118 passed.
- FALSIFIER: backed up live rotations.md, sed-replaced one git-state line to
  `git -C {worktree} fetch` (2 occurrences), re-ran the test -> FAILED
  (`AssertionError: git -C /tmp/tmpoo4lm82r/worktree fetch`,
  `'producer git -C .../worktree fetch' is None`). Restored node byte-
  identical from backup -> 55 passed again. Drift in the live node now turns
  the test red; a hand-copied list could not.

## Agent Notes
test_rotate_startup git_live_template_commands_still_pass now reads the live rotations.md (frontmatter loader, both templates, real temp paths) instead of a hand-copied list; falsifier (git fetch drift) turns it red; brief.py suite paragraph gains the live-config sentence + test_brief assertion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f5d4a552, L4.237). ACCEPTED proved, confidence 0.9.

(1) THE INSTRUCTION SAID (target testable_claim): "the test parses the live rotations node (the same reader L4.191's test uses), substitutes {worktree}/{repo} with real paths, and judges every git-bearing cmd it finds -- a template edit that adds an off-allowlist git line turns the test red without touching the test; AND the kid brief (brief.py, the review/tests paragraph) carries one sentence: a test of live config reads the live node, never a copied list. TESTS: the rewritten test passes on the live node; a fixture rotations node carrying `git log -p` makes it fail; test_brief asserts the sentence renders for a kid."

(2) WHAT THE MACHINE ACTUALLY DOES, read from the round bytes and re-run by me: `_live_first_turn_cmds()` (extensions/agi/tests/test_rotate_startup.py:841-862) loads `<test>/parents[3]/.agi/nodes/.geometry/rotations.md` through graph_core.persistence.frontmatter.load_node_file and returns every template's startup.first_turn cmd; `test_git_live_template_commands_still_pass` (lines 865-879) filters git-bearing cmds, asserts the set is non-empty, substitutes {worktree}/{repo} with tempfile dirs, and judges each with rotate._producing_refusal -- the hand-copied `shipped` list is GONE from that test. I RAN `pytest extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_brief.py -q` on this checkout -> 173 passed. I REPRODUCED THE FALSIFIER INDEPENDENTLY, not on the kid's word: copied extensions/ + .agi/nodes/.geometry/rotations.md + .agi/config.json to /tmp/proof-l4237, rewrote exactly the live git-state line to `git -C {worktree} fetch; git -C {repo} status -sb | head -3`, ran the suite -> 1 failed, 54 deselected, the failure being `assert 'producer git -C .../worktree fetch' is None` from this test. brief.py:1340-1341 now carries "A test of live config reads the live node, never a copied list." inside the kid suite segment, and test_brief.py:606 asserts the exact sentence renders for a kid.

(3) NEAR MISS: keeping the two-string `shipped` list as a "canonical shipped shape" and ADDING a live-node assertion beside it. That satisfies the words and loses the mechanism -- the plainest way a live-config guard rots is exactly the original bug: the mirror stays green while the node drifts (L4.179/L4.191 are instances two and one of the same shape). This version reads only the live node, so the mirror cannot survive beside it. A second near miss I checked for: asserting merely that the live node PARSES (e.g. file loads) rather than judging each cmd -- that would be green on `git fetch` in the node. This test judges the commands through the allowlist, which is what makes it bite.

(4) DEVIATIONS FROM THE CLAIM I noted and did not penalise: (a) the claim's fixture says a node carrying `git log -p` makes the test fail -- the kid used `git fetch`, which is off-allowlist for the same reason (fetch is a network-writing producer, `hypothesis:l4-the-git-allowlist-has-no-network-write`); mechanically equivalent, and I reproduced it. (b) The git filter is a substring test (`"git" in c`) rather than a parse of the unit's argv0; a cmd that merely CONTAINS "git" (not runs it) would be judged too, which over-includes rather than under-includes -- the failure direction is safe. (c) The other `shipped` list still in the file (line 64, `test_producing_refusal_allows_shipped_commands`) is the allowlist unit fixture, NOT a live-config mirror; it is outside this claim's scope and was correctly left alone.

Residue: none. parents resolves to the target hypothesis; evidence_runs is experiment:a00-35cfe009-262616, a real node.
<!-- THOUGHT:END -->

REVIEWED by parent a00-f5d4a552 (L4.237): accepted proved 0.9. Independent re-run: 173 passed (test_rotate_startup.py + test_brief.py); scratch copy with the live git-state line drifted to 'git -C {worktree} fetch' fails this test (1 failed, 54 deselected). Hand-copied shipped list gone; brief.py:1340 sentence + test_brief.py:606 assertion land.
