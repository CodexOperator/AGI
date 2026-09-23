---
id: hypothesis:lm-grid-storage-trunk-code-fix-remaining-literal-sites
mint_id: 35847a42efe2458d9bbea475d439da2f
type: hypothesis
parents:
  - goal:g7.33.7
next_edges: []
confidence: 0.7
edited_by: thought-master
scaffold_hash: 6d7b22d4cccdbae8
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source, re-counted independently, not assumed from the earlier residue note: grep -c refs/grid across rotate.py/unify.py/cli.py/verify_unified.py totals 33 occurrences (5+15+5+8), matching the number thought-master cited, but MOST are docstrings, comments or print labels. Only SIX are real behavior -- a live git command or a module constant that determines ref resolution: cli.py:4057 (git for-each-ref ... refs/grid, inside a function that is the byte source of truth for the namespace); rotate.py:9071 (git push origin refs/grid/*:refs/grid/*, inside the Prime rotation closeout push -- sensitive, must not change behavior on this unconfigured box); unify.py:129 (GRID_REF_NAMESPACE = refs/grid) and :130 (GRID_FETCH_REFSPEC = refs/grid/*:refs/grid/*), both module constants used elsewhere in that file for a DIFFERENT kind of migration (moving a whole graph repo, not the storage-trunk feature); unify.py:339 (a live git cat-file call building a ref path with a hardcoded refs/grid/node/ prefix); verify_unified.py:126 (git for-each-ref refs/grid/ ...). unify.py:1059 LOOKS like a seventh site but is inside a docstring documenting a manual rehearsal procedure, not executed code -- explicitly NOT in scope, to avoid this rounds own falsifier(ii) repeating G14.14.7s original global-vs-scope mistake. CLAIM: each of the six sites reads its refs/grid string through grid.ref_ns_for(root) or grid.push_spec_for(root) (grid.py, landed in G14.14.7) instead of the literal, and on THIS box, which has no storage_trunk configured, every one of the six sites resolves to exactly the same bytes as today (refs/grid, refs/grid/*:refs/grid/*) -- the six behavior sites change their SOURCE, not their OUTPUT, on an unconfigured tree. FALSIFIER: (a) any of the six sites still contains a literal refs/grid string after the fix (grep confirms 0 across only these 6 call-site lines, not the whole 33); (b) on this unconfigured box, any of the six sites resolves to a DIFFERENT ref path or refspec than before the change (the closeout push in rotate.py is the falsifier with the most weight -- it must push the exact same refspec it does today); (c) unify.py behavior for its OWN kind of migration (whole-repo move) changes for a project with no storage_trunk configured. TEST (committed, <=4 fixtures): each of the six call sites, mocked/probed to confirm it now calls grid.ref_ns_for or grid.push_spec_for rather than a literal; a probe on an unconfigured scratch tree showing rotate.py closeout push still targets literally refs/grid/*:refs/grid/*; the existing rotate.py/unify.py/verify_unified.py suites stay green. FILE SCOPE: extensions/agi/bin/rotate.py (~line 9071), extensions/agi/bin/unify.py (~lines 129-130, 339), extensions/agi/bin/cli.py (~line 4057), extensions/agi/bin/verify_unified.py (~line 126), plus their existing test files. NOT IN SCOPE, explicitly: the 27 comment/docstring/print-label occurrences (cosmetic only, no falsifier fires on them); this boxs own migration to a real non-default storage_trunk (a separate, later round -- moving THIS boxs live grid ref history is not a build-and-test task, it needs its own explicit go-ahead). CEILING: <=200 engine lines (source-suffix lines; data files never count), 1 pi parent, cap 1 USD."
title: "G14.14.7 residue (EF.02b, code only): the 6 real refs/grid behavior literals outside grid.py/crons.py resolve through grid.ref_ns_for/push_spec_for instead"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-grid-storage-trunk-code-fix-remaining-literal-sites

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 06:1xZ 09-21 -- EF.07 ACCEPTED (merge 17c0932c2; verdict proved; kids a00-a8960e30 + a00-fa442289 -> experiment nodes): of 33 refs/grid literals outside the EF.02 scope, 6 carried behaviour (cli.py, rotate.py:9071 the Prime rotation-closeout push, unify.py, verify_unified.py) and now route through grid.ref_ns_for / grid.push_spec_for; 27 confirmed cosmetic. The parent's review caught a 1-byte regression on its seventh check (unify.fetch_grid_refs gained a force-fetch '+' the literal never had) and kid2 removed it in 5 lines -- the review chain worked as designed. rotate.py:9071 spot-checked by the director in the merged code: push_spec_for(_shared_graph_root(root)) -- the graph-root resolver, not git toplevel. 312 named tests re-run by the director; engine suite on the merged trunk: goal:g14.14 note. G14.14.7's code residue is CLOSED; the box migration is EF.08 (go-ahead given with conditions).
