---
id: hypothesis:l4-replace-api-drops-source
mint_id: 1c238a313fa04eeeb6aa719c8ace5f5b
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 510a8ca0901ce536
season: 2
status: pending
tags:
  - l4
  - g13
  - write
  - data-loss
  - defect
testable_claim: "`write.py`'s `replace` verb DELETES the target range instead of replacing it when driven through the Python API, and reports success while doing it. MEASURED, not theorised -- this happened to a real payload in this repo today: `verb_replace(e, \"payload\", \"26:26\", <path>)` then `submit(...)` returned `status='updated' payload_changed=True` and `git diff --numstat` read `0 1` -- ZERO insertions, ONE deletion. The file lost line 26 and gained nothing. THE CAUSE, read in the source: `verb_replace` (`write.py:329-355`) records `edit.replace_from = source` and NOTHING ELSE. The only code that turns `replace_from` into `edit.replace_text` lives in `main()` at `write.py:1184-1191` -- the CLI path. `submit` (`:616-625`) then splices `edit.replace_text`, which for an API caller is still `\"\"`, and `_splice_range` (`:700-727`) faithfully splices nothing: `\"\".split(chr(10))` is `[\"\"]`, the trailing-empty pop makes it `[]`, and the range is dropped. 🔴 THIS IS A LOADED GUN IN THE DIRECTOR BRIEF ITSELF. The brief tells directors to drive the Python API for long prose (because the script form splits on the doubled ampersand) AND names `replace` as the partial-write verb to use. Following both instructions destroys the range. WHAT MUST BE TRUE WHEN THIS ROUND IS DONE: (1) ONE resolver turns `replace_from` into text, used by BOTH the CLI and `submit`, so the API and the CLI cannot disagree again -- do NOT fix this by copying the read into a second place; (2) an ABSENT, UNREADABLE or EMPTY source REFUSES with an EditError naming the source, and writes NOTHING -- deleting a range because the replacement was empty is the bug, not a feature, and this must hold for the CLI path too; (3) `replace <target> N:M -` (stdin) keeps working exactly as it does now; (4) a deliberate deletion, if the verb is to support one at all, requires an explicit signal and is NOT the silent consequence of an empty source -- if you add none, say so. PROVED BY: (a) a test that drives the PYTHON API -- `write.Edit` + `write.verb_replace` + `write.submit`, no argv -- against a fixture payload and asserts the line is REPLACED, which is the exact path that has no coverage today and is why this shipped; (b) a test that an empty/missing source REFUSES and leaves the file byte-identical; (c) the existing CLI behaviour unchanged, shown by `pytest extensions/agi/tests/test_write.py -q` green with NO assertion weakened, removed or retargeted; (d) run the API-path reproduction BEFORE the fix and paste the `0 1` numstat, then after the fix and paste the `1 1`. DISPROVED IF: the fix adds a second reader instead of one shared resolver, an empty source still deletes, or stdin stops working. HARD CEILING: 2 kids. Run `pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_guard.py -q` and NOTHING else -- do NOT run the full suite, and say so in the node. Do NOT touch `.agi/nodes/.geometry/*`. Reproduce by READING the code path and by writing to a FIXTURE payload -- never against a real node or a real payload in this repo."
thought_session: sanctuary-director-genII-L4
title: write.py replace silently deletes the target range when driven through the Python API, because only the CLI reads the replacement source
---
<!-- BODY:BEGIN -->
# hypothesis:l4-replace-api-drops-source

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
FOUND BY BEING BITTEN, not by review. The owner asked for a one-line change to the default director brief. I drove `write.py`'s Python API to make it -- exactly what the brief tells a director to do for prose that the script parser would split on the doubled ampersand -- and `submit` returned `status='updated' payload_changed=True` while deleting line 26 of `extensions/agi/briefs/prime-director-successor.md`. I caught it only because I greped the bytes afterwards (trap 0ah) instead of trusting the status. `git checkout --` restored it, the owner's edit then landed correctly through an explicit `e.replace_text`, and nothing was lost -- but the loss was silent, and a director who trusted the return value would have committed a file with a line missing.

WHY IT SURVIVED THIS LONG: the CLI path is covered and correct, and the API path has no test. `verb_replace` is the only verb whose payload arrives by PATH rather than as a value, so it is the only one where 'the CLI resolves it' and 'the API does not' can diverge without anything looking wrong at the call site. The other verbs take their content as an argument and cannot have this shape.

THE FIX IS ONE RESOLVER, NOT A SECOND READ, and the claim says so explicitly because the obvious patch -- copy `:1184-1191` into `submit` -- would leave two readers of one field and reproduce the divergence the moment either changes. The second half of the claim matters as much: an empty source must REFUSE. Today an empty replacement is indistinguishable from a deliberate deletion, and the engine resolves that ambiguity by destroying data. Fail-closed is the house rule everywhere else in this repo and it should hold here.
<!-- THOUGHT:END -->
