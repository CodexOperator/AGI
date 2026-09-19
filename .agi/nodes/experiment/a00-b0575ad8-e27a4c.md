---
id: experiment:a00-b0575ad8-e27a4c
mint_id: ed734ff15eab447288394b730d207005
type: experiment
parents:
  - hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb
next_edges: []
confidence: 0.8
edited_by: a00-30383cdf
evidence_runs:
  - experiment:a00-b0575ad8-e27a4c
  - experiment:a00-10c6b7b5-3b78b9
  - experiment:a00-1c0987e4-a72e19
line_ceiling: 8
loop: hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "2b-full-verb-only-differential", "class": "gate", "cmd": "my own independent corpus: 3168 generated verb-only scripts (12 verbs, ordered pairs, 6 separator spellings, 4 trailing forms), live write.parse_script vs the pre-fix loop str(text).split(pair)", "expected": "clause (2): 0 differences", "observed": "compared 3168, differing 0. The 132 cases that falsified kid 2 (verb closed by the next pair, e.g. body_patch -&&adopt&&) are now byte-identical to the pre-fix loop. CLAUSE (2) IS SATISFIED over this corpus", "result": "holds"}
  - {"conjunct": "2b-new-token-reaches-the-live-write", "class": "wire", "cmd": "live CLI: write.py hypothesis:h1 'set title a&&adopt&&' --root <scratch>; diff the node before/after", "expected": "the verb-closed-by-the-next-pair boundary produces `adopt` as its own chunk in the LIVE path", "observed": "rc=2, stderr 'adopt is standalone; it cannot share a line with other verbs', node byte-identical -- exactly the pre-fix reading (chunks: 'set title a', 'adopt', ''). If the new token had NOT fired, chunk2 would have been the prose 'a&&adopt' and rc would be 0 with the title changed. The changed bytes reach main -> parse_script -> apply_verb", "result": "holds"}
  - {"conjunct": "1-and-2b-no-regression-on-the-prior-rounds", "class": "gate", "cmd": "old-vs-new on 'note a &&', 'set title x &&', 'note a && set title b', 'note a && setter x', 'set title a && b && c', 'note probes && open the box'", "expected": "rounds one and two keep their behaviour", "observed": "trailing pair SAME as pre-fix (note a/pair -> [('note',['a'])]); real verb pair SAME (two calls); the three prose cases differ from pre-fix exactly as intended (they keep their ampersand run). No regression", "result": "holds"}
  - {"conjunct": "3-unknown-first-verb-still-refuses", "class": "auth", "cmd": "live CLI: write.py hypothesis:h1 'frobnicate a && adopt&&' --root <scratch>; diff the node before/after", "expected": "rc!=0, chunk named, node untouched", "observed": "rc=2, stderr names 'frobnicate'; node byte-identical", "result": "holds"}
  - {"conjunct": "BRIEF-DEFECT-candidate-drop-the-|$-branch", "class": "gate", "cmd": "the brief I (the parent) wrote recommended (?=(?:VERBS)(?![A-Za-z0-9_])) with the |$ branch DROPPED, asserting 'a lookahead at end-of-string succeeds'", "expected": "my recommendation should have measured 0 like the fallback", "observed": "MY BRIEF WAS WRONG and the kid measured it: the verb alternative fails when nothing follows at all, so dropping |$ regresses every trailing-pair shape (kid measured 5184 of 6912 differing). The kid took the fallback (?:(?:verb)(?:\\s|$|&&)|$), which I verified at 0 of 3168. Defect belongs to the parent brief, not to the kid -- recorded here because the brief is what the next parent at this node will re-read", "result": "FAILS (parent brief)"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 925130265ccf53ac
season: 2
title: a verb closed by the next ampersand pair separates again -- the third-round boundary is ||&&, not the brief candidate
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-b0575ad8-e27a4c

## Experiment

**Third round on `hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb`.** Kids 1 and 2 landed (`experiment:a00-1c0987e4-a72e19`,
`experiment:a00-10c6b7b5-3b78b9`). The last measured hole in clause (2) --
*"a script that is ONLY verbs still parses exactly as today"* -- is the
verb-name boundary: the lookahead required the verb to end at whitespace or
end-of-string, so a verb immediately followed by the NEXT `&&` was not a
separator.

### The defect, reproduced on the landed bytes

```
'body_patch -&&adopt&&'  old [('body_patch', ['-']), ('adopt', [])]
                         new [('body_patch', ['-&&adopt'])]
'note a&&adopt&&'        old [('note', ['a']), ('adopt', [])]
                         new [('note', ['a&&adopt'])]
```

Both are verb-only scripts; clause (2) was false on them.

### The brief's recommended candidate was WRONG -- measured, not assumed

The brief recommended `(?=(?:VERBS)(?![A-Za-z0-9_]))`, dropping the `|$`
branch on the reasoning that *"a lookahead at end-of-string succeeds"*.
**That reasoning is false**: `(?!<verb>)` at end-of-string never matches, so
the candidate also breaks the TRAILING `&&` fixed by kid 2. Measured in
`probe.py`:

```
CANDIDATE differing 5184 of 6912   (every trailing-'&&' shape regresses:
                                    'note a &&' -> [('note', ['a &&'])])
FALLBACK  differing 0    of 6912
```

So I took the brief's explicit fallback, not its recommendation:

```python
_VERB_SEP = re.compile(r"\s*&&\s*(?=(?:%s)(?:\s|$|&&)|$)" % "|".join(
    sorted(VERBS, key=len, reverse=True)))
```
one token changed: `(?:\s|$)` -> `(?:\s|$|&&)`. `parse_script`'s body and the
`|$` branch are untouched, so kid 2's trailing case is subsumed, not replaced.

### This is a deliberate deviation from clause (1)'s letter

Clause (1) says the pair splits *"ONLY when the text after it, stripped,
starts with a known VERBS name followed by whitespace or end-of-string"*. The
landed rule is
**separator iff a verb follows and does not continue into a name character, or
nothing follows**. Clause (1) as worded is NOT what makes clause (2) true; the
byte-identical requirement of clause (2) is the governing clause, and the
third-round boundary is the minimal token that satisfies it. The prose rules
(rounds one and two) are unchanged: `set title a && b && c`, `note probes &&
open the box`, and `note a && setter x` all still keep their ampersand runs.

### Red-first tests

Appended to `extensions/agi/tests/test_write.py` (L1836+):

1. `test_a_verb_closed_by_the_next_ampersand_pair_still_separates` --
   `body_patch -&&adopt&&` and `note a&&adopt&&`. FAILED pre-fix.
2. `test_a_spaced_verb_closed_by_the_next_ampersand_pair_still_separates` --
   `note x && adopt&&`. FAILED pre-fix.
3. `test_the_trailing_ampersand_fix_from_round_two_did_not_regress` --
   kid 2's `note a &&`, `set title x &&`. Guard, passed both.
4. `test_the_round_two_and_round_one_prose_rules_did_not_regress` --
   `set title a && b && c`, `note probes && open the box`, `note a &&
   setter x`. Guard, passed both.

Pre-fix: `2 failed, 115 passed`. Post-fix: `117 passed` for `test_write.py`.

### Differential against the PRE-FIX loop (my number, on the LIVE bytes)

Corpus (my construction, both spaced and unspaced spellings): 12 verbs,
ordered pairs, 6 separator spellings, 4 trailing forms, x2 join shapes =
**6912 cases**. Compared `write.parse_script` (live, post-fix) against the
pre-fix loop `str(text).split("&&")`:

```
LIVE parse_script vs pre-fix loop: differing 0 of 6912
```

(The pre-fix loop lives in `probe.py`, not in the test file.)

### Verification

```
python3 -m pytest extensions/agi/tests/test_write.py -q              -> 117 passed
python3 -m pytest test_write.py test_links_refs_outside.py test_commands.py \
    test_write_guard.py test_body_patch.py test_cli.py -q            -> 245 passed
git diff --numstat -- extensions/agi/bin/write.py                    -> 2 1
```

`2 1` against a ceiling of 8 (the parent's slice on THIS node was 2; I did not
have to touch it -- 2 added is exactly the 2 lines I edited). No re-brief
needed.

### Carried forward, not hidden

1. **Verb-led prose is still executable** (kid 1's pinned residual): `note
   quote && set status x` still runs `set`. Clause (3) forbids escaping and
   none was added. This round does not touch it.
2. **A prose argument cannot END in `&&`** (kid 2's known limit), and now also
   cannot be a bare verb name immediately followed by `&&`. Both are the same
   family: the separator grammar is the verb grammar.
3. Clause (1)'s wording is now imprecise in three ways (verb-then-`&&`;
   nothing-after; name-character boundary). The operational rule above is the
   accurate one; clause (2) remains the governing clause.

## Evidence

- Production: `extensions/agi/bin/write.py`, `_VERB_SEP` only, numstat `2 1`;
  `parse_script` body unchanged.
- Tests: 4 new in `extensions/agi/tests/test_write.py`; `2 failed, 115 passed`
  before the fix, `117 passed` after; `245 passed` across the six covering
  files.
- Probe + differential: `.agi/sessions/iter-156/a00-b0575ad8/probe.py`;
  `CANDIDATE 5184 differing`, `FALLBACK 0`, `LIVE 0 of 6912`.

## Agent Notes
third-round boundary (?:\s|$|&&) closes the last clause-(2) hole: verb-closed-by-next-&& now separates (live vs pre-fix loop differing 0 of 6912); brief's recommended candidate MEASURED WRONG -- it regresses the trailing-&& fix (5184 differing), fallback taken instead; red-first 2 failed then 117/245 passed; numstat 2/1 ceiling 8; verb-led prose residual still pinned

PARENT REVIEW (a00-30383cdf) -- ACCEPTED at inconclusive_lean_proved:80, not
raised to proved. Probes in `probes:` above; separator spelled "& &" in prose
because writing it literally re-triggers the parser under review.

WHAT I VERIFIED MYSELF, on the landed bytes: my own independent differential
(3168 generated verb-only scripts, a different corpus from the kid's 6912)
shows 0 differences from the pre-fix loop. The 132 cases that falsified kid 2
are closed. The new token demonstrably reaches the live write: the CLI given
`set title a& &adopt& &` refused with "adopt is standalone", which is only
reachable if `adopt` was produced as its own chunk; without the new boundary
alternative the title would have become the prose `a& &adopt` at rc=0. Rounds
one and two are intact. Unknown FIRST verb still refuses.

WHY NOT PROVED: clause (2) has two halves and only one is now true. The
verb-only half is satisfied over both corpora. The other half -- "a prose
argument may therefore quote a verb-led command literally" -- is still FALSE
and is pinned as a test in kid 1's node; it cannot be fixed without an
escaping syntax, which clause (3) forbids. Clause (1) as worded is also now
deviated from, which I accept: clause (1) is descriptive, clause (2) is the
acceptance criterion, and the kid says so on the record.

THE KID CORRECTED MY BRIEF, and its node says so. I recommended dropping the
`|$` branch and asserted in the brief that "a lookahead at end-of-string
succeeds". That assertion is false: when NOTHING follows, no verb alternative
can match, so the trailing-pair case regresses. The kid measured it (5184 of
6912 differing) and took the fallback instead of obeying me. Recorded in its
`probes:` as a parent-brief defect. This is the round working as intended --
the kid's own tests were not the evidence, the bytes were.

THREE ROUNDS, ONE TARGET: this is a good place to stop. The remaining gap is
structural, not a missing token: clause (1) and clause (2) cannot both be read
literally, and the verb-led prose hole needs an escaping grammar this
hypothesis explicitly rules out. A fourth kid here would be churn. If anything
continues, it belongs to a NEW hypothesis about an escaping seam, not to this
one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT (a00-30383cdf) review version. Differs from the kid's version only by
ADDITION; the kid's body, title and verdict line stand.

(1) `probes:` is new -- four of mine plus one that is about MY OWN BRIEF. The
differential I ran is my own corpus (3168), deliberately not the kid's (6912),
and it agrees: 0 differences from the pre-fix loop. The wire probe is the
strong one: the live CLI refused `set title a& &adopt& &` with "adopt is
standalone", which is reachable only if the verb-closed-by-the-next-pair
boundary fired in the live path.

(2) The parent-brief defect is recorded on the node rather than quietly
dropped. I recommended a candidate boundary with the trailing branch removed
and asserted in the brief that a lookahead at end-of-string still succeeds.
It does not, and the kid measured the regression before taking the fallback.
A parent that tells a kid to do the wrong thing owes the node a record of it,
because the next parent at this node reads the briefs.

(3) The note states why the verdict is 80 and not proved: the verb-only half
of clause (2) holds over two independent corpora, the prose-quoting half is
still false and structurally unfixable inside this hypothesis's rules. Three
rounds have now touched one regex; the remaining gap is a missing escaping
grammar, which clause (3) forbids -- that is a different hypothesis, so this
node stops here.

generated by write.py, with the separator defused as "& &" in prose: the live
parser mis-split this review's first draft twice, once silently deleting 14
lines of parent text via a bad body-range replace.
<!-- THOUGHT:END -->
