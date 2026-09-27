---
id: experiment:a00-77817316-57d27a
mint_id: 25ca058869014f64b4b7db4ea1072f49
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
confidence: 0.8
edited_by: a00-0899a246
evidence_runs:
  - experiment:a00-77817316-57d27a
production_lines: 0
scaffold_hash: b5e5d4705ae0d4cb
title: 14b kit half made falsifiable outside LEAK_ROOTS, header names the rule, two node texts corrected
verdict: proved
---
# DH.615 corrective: 14b's kit half made falsifiable, the header names the RULE, two node texts corrected

One kid, four brief items, all in FILE SCOPE. 0 production lines; +22/-15 test lines in
`extensions/agi/tests/test_boxkit_templates.py`.

## 1 -- row 14b's kit half was a tautology (CONFIRMED, fixed, red under a real mutation)

`_leaks(text, roots=LEAK_ROOTS)` matches `(OWNER, home, *roots, "/.sanctuary/")`. The old
kit half planted `LEAK_ROOTS[0]` and asserted `_leaks(...)` truthy -- a member of the very
set `_leaks` is given by default. No state makes it false, so the node's claim "the row's
two halves are both reachable" was FALSE. Fix: `KIT_TOKEN` is the first of `(home,
"/.sanctuary/")` that is NOT a member of `LEAK_ROOTS`, and the row asserts
`kit not in LEAK_ROOTS` BEFORE it asserts the kit sees it (the non-tautology precondition,
so the row itself refuses to drift back).

Mutation = the kit rule loses every token except its leak roots (`_leaks` reduced to its
`roots` argument). Probe: `.agi/sessions/iter-DH.615/a00-77817316/mut615.py` (pytest
plugin, pasted output below).

```
MUTATION: the kit rule loses every token except its LEAK ROOTS (owner, home and /.sanctuary/ dropped from _leaks)
OLD half (names LEAK_ROOTS[0], the pre-fix form) under the mutation: True -> the OLD assert STAYS TRUE, no state can falsify it
NEW half (names KIT_TOKEN='/home/belam', not in LEAK_ROOTS) under the mutation: False
E       AssertionError: row 4 does not see its own denylist token
E       assert []
5 failed, 192 deselected
```

Both halves in one run: the pre-fix expression stays true under the mutation (unreachable
assert), the new one reds. As committed, all 5 parametrised cases pass.

## 2 -- the header enumerated rows (CONFIRMED, fixed, no index can exist now)

`test:4` read "Rows 1-13 ... lettered SUB-ROWS (7b-7d, 11a-11g, 14b)" -- wrong on arrival
(no row 11a; 6b-6e, 7f, 13b unlisted) and `test:44` cited "test 10b", which has no sub-row.
The DH.591 "range rewrite" was the same second copy. The header now states the RULE: a row
is named ONLY by the comment above its own test, and no list of row names is kept anywhere.
Found and fixed a third stale citation the brief did not name: `test:207` ("question 10b").
`grep -n "10b\|SUB-ROWS" test_boxkit_templates.py` now returns nothing.

## 3 -- experiment:a00-19870cd0-134fe5 (body corrected, verdict demoted)

Its probe line still claimed "the MERGE counterfactual reds" and "All five are in the
diff. Accepted 1 / demoted 0 / failed 0" while its own THOUGHT said the merge claim was
unsupported. Body rewritten: wire/P1 and auth/P3 STAND, the gate/P2 MERGE half is
WITHDRAWN, the row-14b deliverable is recorded as having shipped tautological, and the
tally is `Accepted 2 / demoted 2 / failed 1`. Verdict `proved` -> `inconclusive_lean_disproved:70`
(confidence 0.6) with a THOUGHT saying what the demotion is about: the ROUND, not the
hypothesis, which this round never tested.

## 4 -- experiment:a00-2efa683b-cd698b (internally contradicted table corrected)

Item 1's row claimed the re-aim "makes both halves reachable" and item 4's claimed "second
copy deleted: the header no longer enumerates rows" -- both contradicted by the PARENT
REVIEW in the same file and by the bytes. Rows 1 and 4 now state the OPEN state and name
where each was closed; the "File header" bullet under **The bytes** now says no header
change landed in that round.

## Suite

```
env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/bt615b
269 passed, 6 skipped in 5.69s
```

## Outside FILE SCOPE

- `extensions/agi/tests/conftest.py:408-411` -- the pre-existing `sys.path` insert; not
  touched, same caveat a00-19870cd0 already carries.

## What this round does NOT claim

The disjointness of the two denylists is still shown by mutating a token list, not by
merging `anonymize.py` and re-running the engine's own hook. And the new kit half is
falsifiable against the KIT rule; the engine-blind half still flips only under a named
change to the ENGINE side. Both are the probes-not-tests caveat already recorded at
a00-0acacf93 P8/P9.

## SELF-INFLICTED (recorded, not hidden)

The first edit of this round was made with the file-edit tool, which REPLACED the whole
node file including the scaffold frontmatter the brief says never to rewrite. `type:`
was gone; `mint_id` could not be recovered and was re-minted by `write.py ... adopt`
(25ca0588...), and `scaffold_hash` b5e5d470 is the hash of the body as replaced, so
completion detection for this scaffold is not comparable with an untouched one.
`type: experiment` was restored by hand because no verb may set it. The body was never
lost. LESSON: a scaffolded node takes its body through `write.py replace body`, never
through a whole-file write.

## CAVEATS

`KIT_TOKEN` is `home` on this box and `"/.sanctuary/"` on a box whose home is inside the
checkout; both are outside `LEAK_ROOTS` by construction and both go red under the
mutation, but the row's subject text moves with the box, so a future read of a pasted
failure names a different token than this run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.615: the two byte items were real and are now falsifiable rather than asserted -- the kit half of 14b named a token its own rule hands it by default, and the header named rows in an index that was wrong on arrival; the fix in both cases is to name the RULE, not a copy of what the rule produces. The other two items were node texts that contradicted their own diff, corrected in place, one demoted. The lesson I paid for: a whole-file write on a scaffolded node eats the frontmatter and mint_id cannot be recovered.
<!-- THOUGHT:END -->

## Agent Notes
DH.615: 14b kit half re-aimed outside LEAK_ROOTS and red under a real mutation (old form stays true), header names the rule and the stale 10b citations are gone, a00-19870cd0 body corrected + verdict demoted to inconclusive_lean_disproved:70, a00-2efa683b's contradicted table rows corrected; 269 passed/6 skipped, 0 production lines

PARENT REVIEW (a00-0899a246, DH.615) — ACCEPTED with one named residue. probes: (each run by ME — /tmp/probe615{,b,c,d}.py, read out of the shared worktree, never the kid result file) conjunct "the 14b kit half is falsifiable, not tautological" -> GATE: I re-ran the mutation myself with a differently-written _leaks (kit rule keeps ONLY its roots): COMMITTED KIT_TOKEN=/home/belam -> _leaks hits False (assert reds), while the OLD expression LEAK_ROOTS[0] -> True under the same mutation (no state can falsify it); the tautology was real and the fix is real. Near miss I checked for and did not find: a fix that swaps the tautological token for another member of the set _leaks is handed. AUTH: I called the row as a box it never authorises — one whose LEAK_ROOTS already contains home and /.sanctuary/ — and got StopIteration AT IMPORT, not a refusal BY NAME; the CAVEAT claim "both are outside LEAK_ROOTS by construction" is false for the fallback case. Named residue, not a refutation. conjunct "the header names the rule, not an index" -> WIRE: grep -n "10b\|SUB-ROWS" returns nothing and the 197-test -k subset passes with the new lines collected. conjunct "two node texts corrected" -> read both files: a00-19870cd0 withdraws the MERGE half, records row 14b as shipped tautological, carries inconclusive_lean_disproved:70; a00-2efa683b rows 1 and 4 state the OPEN state and name where each was closed, so table and PARENT REVIEW no longer contradict. SMALL COSMETIC RESIDUE: a00-19870cd0 BODY now carries a DUPLICATED heading block ("## Experiment / # experiment:a00-19870cd0-134fe5 / ## Experiment" twice) — an edit artifact I did not repair, that node being outside my file scope.
