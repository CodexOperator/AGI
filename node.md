---
id: experiment:a00-b0c8c6f7-ad2e7a
mint_id: bf552e25d00c466486db4df934922591
type: experiment
parents:
  - hypothesis:l4-sm62-repins-the-branch-spelling-grep-inventory-for-the-legacy-town-less-rename-arm
next_edges: []
confidence: 0.9
edited_by: a00-ce1a43b4
evidence_runs:
  - experiment:a00-b0c8c6f7-ad2e7a
line_ceiling: 2
loop: hypothesis:l4-sm62-repins-the-branch-spelling-grep-inventory-for-the-legacy-town-less-rename-arm@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 0, "class": "wire", "cmd": "scratch copy of bin/ + tests/, re-insert ORIGINAL docstring literal, rerun _scan()", "expected": "rotate.py regains extra season2/p -> RED", "observed": "rotate.py extra=['season2/p'] -> RED", "result": "refused"}
  - {"conjunct": 0, "class": "wire", "cmd": "scratch copy, substitute a NOVEL season-first spelling season3/postref in the same docstring, rerun _scan()", "expected": "detector still bites the novel shape", "observed": "rotate.py extra=['season3/p'] -> RED", "result": "refused"}
  - {"conjunct": 0, "class": "gate", "cmd": "git diff 048ef593d --name-only (production surface) + grep season2/posts rotate.py", "expected": "only rotate.py changes; literal gone", "observed": "only rotate.py + the kid node; grep returns nothing", "result": "refused"}
production_lines: 1
profile: balanced
role: kid
scaffold_hash: b98684d3ebf4dee3
season: 2
title: rotate.py:3484 docstring reworded so the legacy town-less ref is described, not spelled
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b0c8c6f7-ad2e7a

## Experiment

Build order: measure the pre-fix state, implement the reword, prove it on the
built bytes. Scope was held to `extensions/agi/bin/rotate.py` line 3484 ONLY --
the docstring, not the logic; `test_branch_spelling_grep.py` untouched.

### Pre-fix measurement (the defect, reproduced)

Ran the test's own scanner directly rather than reasoning about the regex:

```
python3 -c "import sys; sys.path.insert(0,'extensions/agi/tests');
  import test_branch_spelling_grep as t; f=t._scan(); p=t.PINNED; ..."
```

Output (rotate.py only, everything else identical):

```
--- rotate.py
 found:  [... 'season2/m' x8, 'season2/p']
 pinned: [... 'season2/m' x8]
MATCH -> MISMATCH
```

The single extra hit is `season2/p` -- the `season[0-9]+/[A-Za-z_0-9]`
spelling matching `season2/posts/<name>` inside the docstring of
`_rename_post_segment`. Grep confirms it is the only occurrence in the file:

```
$ grep -n 'season2/posts' extensions/agi/bin/rotate.py
3484:    legacy town-less `season2/posts/<name>` ref has no town segment, so its
```

The other `season2/*` lines (`season2/main` at 8127/8155/8462/8529/8668, and
line 8121) are real constants and prose about the trunk pair, pinned as debt
by L4.332 -- not this arm's business. `season2/<town>` at 15060-15061 does not
match the regex at all (`<` is outside the character class).

So the hypothesis is confirmed on its core point: the hit is a DOCSTRING
mention, not a string built or returned by legacy-arm code. The correct fix is
rewording, not a `PINNED` entry -- grandfathering a docstring would have frozen
prose as debt and been the falsifier.

### The fix

Reworded line 3484 so the docstring no longer spells a season-first path shape:

```diff
-    legacy town-less `season2/posts/<name>` ref has no town segment, so its
+    legacy town-less post ref has no town segment, so its
```

Deliberately a single-line edit. The first draft expanded the sentence to
two lines and then three, which measured 3 changed lines against a ceiling of
2 (`git diff --numstat` -- `3  3`); the wording was compressed back until the
diff was `1  1`. The remaining fragment reads continuously with the two
untouched lines below it: "...has no town segment, so its / shape is preserved
verbatim by swapping the post segment alone (the / real ref is never re-spelled
into a town-first one)."

### Post-fix measurement

```
$ git diff --numstat -- extensions/agi/bin/rotate.py
1	1	extensions/agi/bin/rotate.py

$ python3 <scanner>
MATCH

$ grep -n 'season2/posts' extensions/agi/bin/rotate.py
  (none)

$ git diff --numstat -- extensions/agi/tests/test_branch_spelling_grep.py
(empty = untouched)
```

### Tests

```
$ python3 -m pytest extensions/agi/tests/test_branch_spelling_grep.py \
    extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_verb_resolvers.py -q
325 passed, 354 warnings in 41.01s
```

`test_branch_spelling_grep.py` contributes three tests, all green: the
inventory test (`found == PINNED`), the non-vacuity test, and the
resolver-documents test. `test_rotate.py` plus the verb-resolver suite cover
`_rename_post_segment`'s callers -- a docstring-only change cannot move them,
and did not. The 354 warnings are pre-existing `datetime.utcnow()`
DeprecationWarnings from rotate.py, unrelated to this edit.

## Evidence

Every falsifier named in the hypothesis, checked against the built bytes:

| Falsifier | Result |
|---|---|
| `PINNED` gains a new entry | NOT triggered -- `test_branch_spelling_grep.py` is byte-identical, `PINNED` unchanged |
| any file other than rotate.py touched | NOT triggered -- `git diff --numstat` lists rotate.py only |
| docstring still spells the literal after the edit | NOT triggered -- `grep 'season2/posts'` returns nothing |
| either `test_branch_spelling_grep.py` test fails | NOT triggered -- 3/3 green, 325 passed overall |

Production cost: **1 line** (`1  1` numstat), against a ceiling of 2.

Raw scanner output, post-fix:

```
KEYS DIFF []
MATCH
total found 58
```

(58 vs the pre-fix 59 -- exactly the one hand-spelled spelling removed, with
the pinned multiset otherwise untouched. The pin still holds `total >= 40`.)

Not done, on purpose: no new test. The hypothesis says "no new test needed",
and `test_no_new_hand_spelled_branch_spelling` already fails on exactly this
shape, which is why the pre-fix state was red -- adding a test would assert a
property the existing pin already enforces, and the pin is the stronger form
(it would also catch a re-introduction anywhere else in `bin/`).

One caveat worth carrying: this removed a hit from the inventory WITHOUT
burning down any of the frozen `season2/m` debt in `rotate.py`, which is the
bulk of it. That debt is held for a later Prime-only pass by design.

## Agent Notes
Reworded rotate.py:3484 docstring to drop hand-spelled 'season2/posts/<name>' literal; 1 production line, PINNED unchanged (no new entry), test file untouched, 325 tests green incl. both test_branch_spelling_grep tests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID: "do NOT add an entry to PINNED ... Fix: reword the docstring line at rotate.py:3484 so it no longer spells the literal path shape" and "FILE SCOPE: extensions/agi/bin/rotate.py, line 3484 ONLY". (2) WHAT THE MACHINE ACTUALLY DOES: I did not take the kid's result file. `git diff 048ef593d -- extensions/agi/tests/` is empty (byte-identical test file), and `git diff 048ef593d --name-only` returns exactly two paths: extensions/agi/bin/rotate.py and this node -- so production_lines=1 is the size of the change, not a claim about it. I re-derived the defect independently: a Counter diff of `_scan()` against PINNED, run pre-spawn, gave rotate.py EXTRA {"season2/p":1} MISSING {}. The kid's fix removes exactly that one item; the two named tests now pass 3/3. (3) THE NEAR MISS: a kid could have satisfied every word of the brief by adding "season2/posts/<name>" to PINNED["rotate.py"] and calling it "the docstring hit is now triaged" -- the docstring would still spell the literal, the graded falsifier, and the test would go green by freezing prose as debt. That is why I probed the DETECTOR rather than the fix: I copied bin/ + tests/ into a scratch dir, restored the original literal into the copy and confirmed the scan goes RED again (['season2/p']), then substituted a novel season-first spelling (season3/postref) and confirmed the scan catches that too (['season3/p']). The fix is what turns the scan green; the scan was not narrowed. (4) DEVIATION: none from the brief. The one thing I changed on this node is its title -- it arrived carrying the derived "A00 b0c8c6f7 ad2e7a", which is a harvest defect, and a review edit through write.py is the sanctioned way to fix it. (5) CONJUNCTS: the target hypothesis has no numbered CLAIM items (dry-run: "target hypothesis has no claim conjuncts to count"), so cli.py required no probes; I recorded three anyway in `probes:` above because a proved verdict with no negative probe is worth less than one with them.
<!-- THOUGHT:END -->

REVIEW (parent a00-ce1a43b4, SM.64): ACCEPTED proved. Bytes checked, not the report: 1 production line, extensions/agi/bin/rotate.py:3484, docstring only -- "legacy town-less `season2/posts/<name>` ref" -> "legacy town-less post ref". Test file byte-identical (empty diff). Both falsifiers the brief named are cleared: the docstring no longer spells the literal (grep returns nothing), and neither named test still fails (3/3 pass). Three parent-run negative probes recorded in `probes:`; the key one restores the literal in a scratch copy and shows the scan goes RED again, so the fix is not a weakened detector. Title reset from the derived "A00 b0c8c6f7 ad2e7a".
