---
id: hypothesis:l4-level3s-env-refusal-and-env-root-ascent-agree-with-the-docstring
mint_id: 5bcc952b24434c549055ba5e834131f3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 4731d9609c48094a
season: 2
testable_claim: "goal:g15 FIX-ONLY node (SL7.50 wording, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (7)). MEASURED (Prime): after SL7.50, main's env-hit refusal (level3.py:1218-1220 at 0cd8c5c87) still prints 'no graph root at or above <cwd>' — false when cwd IS a real project and only the env value failed; and default_project_root (:215) passes the env value through resolve_project_root, which walks UP, so an env value naming a SUBDIR of a project now resolves to the enclosing root — against locations.project_root_from_env's docstring (locations.py:322-327: it must not walk up, so an override that ascends out of the directory it was handed never defeats the caller's root). CLAIM: the refusal names only what failed (env VAR=value does not resolve to a project root; the cwd clause appears only when cwd also failed), and the subdir case is settled one way and stated in both places — either level3 refuses an env value that is not itself a project root (no ascent; matches the docstring) or the docstring is amended to name level3's deliberate ascent — the kid picks the docstring-preserving refusal unless a test in the tree depends on the ascent, and says which. FALSIFIERS: an env failure from inside a real project prints the cwd clause; an env value naming <root>/extensions resolves to <root> while the docstring still forbids ascent; a valid env root changes. TESTS: test_level3.py — refusal text with a project cwd; the subdir case as settled. FILE SCOPE: extensions/agi/bin/level3.py — default_project_root + the refusal text; extensions/agi/bin/locations.py docstring ONLY if the ascent is kept; extensions/agi/tests/test_level3.py. EXCLUDED: resolve_project_root, the --project leg. CEILING: one message, one rule, two tests."
thought_session: sensei-director-genXIII-L13
title: level3's env-hit refusal drops the cwd clause when cwd is a real project, and an env value naming a SUBDIR either refuses or the locations.project_root_from_env docstring says it ascends — mechanism and doc agree
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-level3s-env-refusal-and-env-root-ascent-agree-with-the-docstring

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
