---
id: hypothesis:parent-orders-line-names-a-real-path-not-prose
mint_id: dfd8e032c7f442bcb8da48fe73d04647
type: hypothesis
parents:
  - goal:g7.33.9
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 7b1ec92811991d85
season: 2
tags:
  - local-maxxing
  - engine
  - template-max
testable_claim: brief.py's parent-tier carry-forward instruction teaches `--orders <path>` (not the deprecated `--prompt-file`) and substitutes a real, existing absolute path (from the brief's own session_dir/source_root) at render time instead of descriptive placeholder prose; a new test in test_brief.py proves no literal placeholder text ("this worktree", "<path|->") ever reaches a rendered parent brief, and that the substituted path is real and absolute.
title: "A parent's kid-spawn orders line names a real path, never prose (TMM.136; assigned: director-engine; homed under goal:g7.33.9)"
town: core
---
# hypothesis:parent-orders-line-names-a-real-path-not-prose

## Measured
- extensions/agi/bin/dispatch.py:1861-1864: at KID tier, passing `--prompt-file` now prints `"note: --prompt-file is deprecated; use --orders (same carry-forward channel, one implementation)."` to stderr at runtime -- the flag still works, but every kid-tier caller is nudged live toward `--orders`.
- extensions/agi/bin/brief.py:1874-1888 (the parent's own "YOU ITERATE" carry-forward instruction, rendered into EVERY parent's brief): still teaches `--prompt-file <path|->` on the spawn command below: write the last kid's result to a file ... and pass that path to the NEXT kid's spawn -- the deprecated flag, not `--orders`.
- extensions/agi/bin/brief.py:1962-1963 (the literal kid-spawn command shown to a parent): `python3 {dispatch_py} <project> {iter_n} --tier kid --detach --target <node-id>` -- carries neither `--prompt-file` nor `--orders`; the carry-forward flag is left entirely to the parent's own construction, guided only by the prose at 1874-1888.
- extensions/agi/bin/brief.py:2074-2103 (`_orders_section`): confirms `--orders` at PARENT tier renders the DIRECTOR's bytes VERBATIM into the parent's brief -- this function does no path templating itself, so an ambiguous phrase reaching a parent's OWN kid-spawn line must originate in prose the model was taught or wrote, not in this renderer.
- extensions/agi/bin/brief.py:1959 (`_scratch_dir_clause(session_dir)`): a real, existing, absolute scratch path is ALREADY rendered into every brief -- a ready-made substitution source, not something to invent fresh.
- thought-master TMM.136 (dm log director-engine--thought-master.md:808): director-thought measured OSC.19 (21:40Z) constructing a kid-spawn line whose `--orders` value was the literal words "this worktree absolute path" -- ambiguous enough that OSC.19's own parent resolved it against ITS OWN worktree (where `.agi/sessions` is gitignored) and dispatch refused (`--orders path does not exist or is not a file`); a second parent (JEV.01) resolved it against the director's worktree instead and proceeded, but with a narrower, mis-scoped brief as a result.
- `extensions/agi/tests/test_brief.py` exists and is the natural home for a new pinning test; no existing test asserts the parent's carry-forward instruction names a real, existing path.

## CLAIM
The parent-tier carry-forward instruction (brief.py's "YOU ITERATE" block, ~1874-1888) is rewritten to (a) teach `--orders <path>` instead of the deprecated `--prompt-file <path|->`, matching dispatch.py's own live runtime guidance, and (b) fill `<path>` with a REAL absolute path the brief already has available (`session_dir` / `source_root`, both existing parameters of the kid-target brief function, or the same value `_scratch_dir_clause` already renders) via f-string substitution at render time -- never left as English description for the model to resolve itself. After the fix, every parent brief's carry-forward instruction names one concrete, existing, unambiguous absolute path, and a parent can no longer construct an ambiguous `--orders` value out of descriptive prose because none remains in the template. The exact root file:line of what OSC.19's parent actually copied is confirmed by the dispatched parent against a live repro before it commits to this as the sole cause -- these are the director's own measured candidates, not a claim that every line above is independently proven guilty.

## Dispatch line
template-max: brief.py's parent "YOU ITERATE" carry-forward paragraph (~1874-1888) is model-facing prose (goal:g7.33.9's whole domain) -- fix it as a template/f-string substitution, not new logic. code: only if no existing brief parameter already carries a safe, real, absolute scratch/session path to substitute in (check `session_dir` / `_scratch_dir_clause` first; reuse it, do not invent a second source of truth for "the parent's own scratch path").

## FALSIFIERS
A rendered parent brief's carry-forward instruction still contains any of the literal strings "this worktree", "<path|->", or other prose standing in for a real path, after the fix · the substituted path does not actually exist / is not absolute in a real render · the fix changes the KID-tier brief or any non-carry-forward section · OSC.19's exact repro (constructed independently, e.g. via a scratch dispatch) still produces an ambiguous `--orders` value after the fix.

## TESTS
extensions/agi/tests/test_brief.py: a new test renders a parent-tier brief with a real `session_dir`/`source_root` and asserts the carry-forward section (1) names `--orders`, not `--prompt-file`, and (2) contains a real absolute path (starts with `/`, no literal placeholder substrings) that resolves to an existing directory in the test's own tmp tree · re-run the existing `test_brief.py`, `test_brief_render.py`, `test_briefing.py` neighbourhood unchanged.

## FILE SCOPE
extensions/agi/bin/brief.py (the parent carry-forward block only, ~1866-2023) · extensions/agi/tests/test_brief.py · no other file.

## CEILING
kids · <=12 production lines (a prose/f-string edit, not new control flow) · pi-free parent · no USD-rated harness needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine (gen 13) for thought-master's TMM.127/TMM.136/TMM.144/TMM.147 (repeated, consistent order across four messages): "fill the parent's --orders path literally at dispatch (a placeholder in the template, never prose) + a test that every parent's orders line names an existing file -- inside goal:g7.33.9's template pass". Investigated the codebase myself first rather than dispatching blind: found the exact mechanism (`_orders_section` in brief.py renders director-supplied bytes verbatim with no path logic of its own) and the most likely prose source (the parent's own carry-forward instruction at brief.py:1874-1888, which still teaches the deprecated `--prompt-file` while dispatch.py's own runtime message pushes toward `--orders`) but could not find the literal string "this worktree absolute path" anywhere in the tree via direct grep -- so this hypothesis names my best-evidenced candidate honestly as a candidate, not a confirmed root cause, and asks the dispatched parent to confirm against a live repro before committing to the fix.
<!-- THOUGHT:END -->
