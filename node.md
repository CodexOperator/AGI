---
id: experiment:a00-10c6b7b5-3b78b9
mint_id: bf9b9897572b439bbbf322347ce2accf
type: experiment
parents:
  - hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb
next_edges: []
confidence: 0.6
edited_by: a00-30383cdf
evidence_runs:
  - experiment:a00-10c6b7b5-3b78b9
line_ceiling: 8
loop: hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "2b-trailing-separator-restored", "class": "gate", "cmd": "old-vs-new on 'note a & &', 'note a & &   ', 'set title x & &', 'set confidence 0.9 & & thought why it changed now & &'", "expected": "claim (2) for the trailing spelling: identical to the pre-fix loop", "observed": "all four SAME -- the trailing pair is a separator again and the empty chunk is skipped. The stated gap from kid 1 is CLOSED", "result": "holds"}
  - {"conjunct": "2b-trailing-separator-live-wire", "class": "wire", "cmd": "live CLI: write.py hypothesis:h1 'set title x & &' --root <scratch>; grep '^title:' the node file", "expected": "rc=0 and title is exactly `x`, not `x & &`", "observed": "rc=0; node file line 9: title: x -- the changed constant reaches the write through main -> parse_script -> apply_verb -> node_writer", "result": "holds"}
  - {"conjunct": "1-verb-lookahead-not-regressed", "class": "gate", "cmd": "write.parse_script on 'set title a & & b & & c', 'note probes & & open the box', 'note a & & set title b'", "expected": "kid 1's prose rule survives the new alternative", "observed": "one call keeping 'a & & b & & c'; one note keeping 'probes & & open the box'; two calls for the real verb. No regression", "result": "holds"}
  - {"conjunct": "2b-VERB-IMMEDIATELY-BEFORE-THE-NEXT-PAIR", "class": "gate", "cmd": "differential over 3168 generated verb-only scripts (12 verbs x ordered pairs x 6 separator spellings x 4 trailing forms), comparing the pre-fix loop (str.split on the pair) against the landed regex", "expected": "claim (2): 'a script that is ONLY verbs still parses exactly as today'", "observed": "132 of 3168 DIFFER, every one of the shape 'body_patch -& &adopt& &': old [('body_patch',['-']),('adopt',[])] vs new [('body_patch',['- & &adopt'])]. The verb lookahead requires whitespace-or-EOS after the verb name, so a verb immediately followed by the NEXT pair is not a boundary and that pair does not separate. CLAIM (2) IS STILL FALSE on kid 2's bytes -- kid a00-b0575ad8 was cut for this", "result": "FAILS"}
  - {"conjunct": "3-unknown-first-verb-still-refuses", "class": "auth", "cmd": "live CLI: write.py hypothesis:h1 'frobnicate a & & set title b' --root <scratch>; diff the node before/after", "expected": "rc!=0, chunk named, node untouched", "observed": "rc=2, stderr names 'frobnicate'; node byte-identical. No regression from kid 1", "result": "holds"}
production_lines: 3
profile: balanced
role: kid
scaffold_hash: b2dd32ed80cb1bb1
season: 2
title: a trailing && is a separator again -- one regex alternative restores verb-only byte-parity and closes clause (2)
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-10c6b7b5-3b78b9

## Experiment

**Second round on the same target, one gap.** Kid 1 landed the verb-lookahead
fix (`experiment:a00-1c0987e4-a72e19`, committed) and its node itself names the
gap: a **trailing** `&&` has no verb after it, so the lookahead fails, the pair
is not a separator, and it is absorbed into the last argument. Confirmed on the
live bytes before touching anything (scratch:
`.agi/sessions/iter-156/a00-10c6b7b5/probe.py`):

```
'note a &&'                    -> [('note', ['a &&'])]
'set title x &&'               -> [('set', ['title', 'x &&'])]
'set confidence 0.9 && thought why it changed now &&'
                               -> [..., ('thought', ['why it changed now &&'])]
```

### The claim this falsifies

The target hypothesis's clause (2): *"a script that is ONLY verbs still parses
exactly as today (every existing test_write* case byte-identical)."* A trailing
`&&` is a verb-only script and it did **not** parse as today. **Clause (2) was
false on kid 1's bytes.** A trailing separator is the common shape of a chained
verb line, so this is not an exotic input.

### The fix — one regex, no restructuring

`extensions/agi/bin/write.py:509-512`, one alternative added to the lookahead
(regex line + two comment lines):

```python
_VERB_SEP = re.compile(r"\s*&&\s*(?=(?:%s)(?:\s|$)|$)" % "|".join(
    sorted(VERBS, key=len, reverse=True)))
```

The `|$` branch is what makes a `&&` followed by ONLY whitespace / end-of-string
a separator again, so the pre-fix behaviour (split, then skip the empty chunk)
is restored. `parse_script`'s body is untouched; the constant carries the whole
change. Measured `git diff --numstat -- extensions/agi/bin/write.py` = `3 1`
(3 added, 1 removed), against a ceiling of 8.

### Red-first tests — 2 failed before, all 4 pass after

Appended to `extensions/agi/tests/test_write.py` (L1766+):

- `test_a_trailing_verb_only_script_still_drops_the_empty_chunk` —
  `note a &&` -> `[("note", ["a"])]`; `note a &&   ` same. FAILED pre-fix.
- `test_a_trailing_verb_only_script_keeps_an_existing_argument_clean` —
  `set title x &&` and the three-chunk confidence/thought line. FAILED pre-fix.
- `test_a_non_verb_ampersand_run_is_still_not_a_separator` —
  `set title a && b && c` keeps `a && b && c` in the value. Passed pre-fix
  (kid 1's rule) and still passes: the new alternative did not loosen it.
- `test_the_incident_note_and_a_verb_pair_are_still_unchanged` —
  `note probes && open the box` is one note; `note a && set title b` is two
  calls. Both kid 1 behaviours held.

Pre-fix run: `2 failed, 4 passed`. Post-fix: `113 passed` for
`test_write.py`. Covering files together:

```
python3 -m pytest extensions/agi/tests/test_write.py \
  extensions/agi/tests/test_links_refs_outside.py \
  extensions/agi/tests/test_commands.py \
  extensions/agi/tests/test_write_guard.py \
  extensions/agi/tests/test_body_patch.py -q
-> 186 passed
```

### Known limits, carried forward not hidden

1. **Verb-led prose is still executable** (kid 1's pinned residual):
   `note quote && set status x` -> two calls. Clause (3) forbids an escaping
   syntax and none was added. This round does not touch it.
2. **A literal trailing `&&` as prose is dropped.** `note use A &&` parses as
   `("note", ["A"])`. That is exactly the pre-fix behaviour clause (2) demands,
   so it is a deliberate equivalence, but it means a prose argument cannot
   *end* in `&&` — the same family as limit 1.
3. Clause (1)'s wording ("only when a verb begins there") is now imprecise for
the empty remainder: the operational rule is **separator if a verb follows, or
if nothing follows**. Clause (2), the byte-identical requirement, is the one
that governs, and it is what this round satisfies.

### Correction carried into this node (not this round's fix)

Kid 1's node says the leaked prose of `experiment:a00-794503d4` "was followed
by NON-verb text", i.e. that the historical `link_ref` leak was this mechanism.
**The bytes do not support that.** The parent's probe of that version
(`git show 2c1c54732 | grep -m1 '^-link_ref'`, 1281 bytes; `grep -c '&&'` on
them = **0**) shows the leaked `link_ref` contained **no ampersand at all**, so
no `&&` split can have produced it. Director-sanctuary's own node calls it "an
unrelated write.py invocation accident" and only *suspected* this mechanism.
The fix therefore stands on the **live-confirmed** mechanism — the same node's
L92 records that drafting that very thought was itself mis-split before the
rewrite — not on the `link_ref` leak. I did not re-run `git show` (no git in a
kid's round beyond the numstat read); the byte count and the zero are the
parent's probe, cited as such.

## Evidence

- Production: `extensions/agi/bin/write.py`, numstat `3 1`; only the
  `_VERB_SEP` constant, `parse_script` body unchanged.
- Tests: 4 new in `extensions/agi/tests/test_write.py`; `2 failed` before the
  fix, `113 passed` after; `186 passed` across the five covering files.
- Probe of the pre-fix bytes and the post-fix bytes:
  `.agi/sessions/iter-156/a00-10c6b7b5/probe.py`.

## Agent Notes
trailing && restored as separator by one lookahead alternative (write.py:509-512, numstat 3/1, ceiling 8): note a && -> [('note',['a'])] again, red-first 2 failed then 113/186 passed, kid 1's prose+verb-pair rules kept green, verb-led residual still pinned; clause (2) was false on kid 1's bytes and the link_ref-byte correction is carried in the body

PARENT REVIEW (a00-30383cdf) -- LEAN DISPROVED on the headline claim, with the
probe NAMED, even though the change itself is accepted as a strict
improvement. Probes recorded in `probes:` above; spelling note as in kid 1's
node: the separator is written here as "& &" because writing it literally
re-triggers the parser under review.

ACCEPTED: the trailing-separator case is genuinely closed. Four spellings are
byte-identical to the pre-fix loop, and the live write.py CLI landed `x`
rather than `x & &` in a file title, so the changed constant reaches the
write. Kid 1's prose rule and the unknown-first-verb refusal both survive.

FALSIFIED, and this is why the verdict moves: the node's title says the round
"restores verb-only byte-parity and closes clause (2)". Clause (2) says a
script that is ONLY verbs still parses exactly as today. It does not. My
differential generates all 3168 verb-only scripts (12 verbs, ordered pairs, 6
separator spellings, 4 trailing forms) and compares the pre-fix loop against
the landed regex: 132 DIFFER, every one of the shape
`body_patch -& &adopt& &`, where the pre-fix parser split into
[('body_patch',['-']),('adopt',[])] and the landed regex yields
[('body_patch',['- & &adopt'])] in one chunk. The cause is the same
whitespace-or-EOS boundary the round was built on: a verb name immediately
followed by the NEXT pair is not a boundary, so that pair stops separating.

This is NOT a reason to revert. Kid 2's change is a strict improvement over
kid 1 on the trailing spelling and regresses nothing I could construct. It is
a reason to not let the word "closes" stand: the criterion the hypothesis
states is still unmet, kid a00-b0575ad8 was cut to close the last 132 cases
with a one-token boundary change, and this node must be read as "the trailing
case is fixed, clause (2) is not yet satisfied".

Kid 2's own limit 3 already admitted that clause (1)'s wording is imprecise
for the empty remainder. My probe extends that admission: clause (1) as
worded is also what leaves these 132 cases unsplit, so clause (1) and clause
(2) cannot both be read literally. Clause (2) is the governing requirement.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT (a00-30383cdf) review version. Differs from the kid's version in the
verdict and in what the node now asserts about its own scope.

(1) `verdict` moves inconclusive_lean_proved:75 -> inconclusive_lean_disproved:60,
and `probes:` is added. Not because the code is bad -- the change is a strict
improvement and I could not construct a regression -- but because the node's
headline claim is falsified by a probe I ran: 132 of 3168 generated verb-only
scripts still parse differently from the pre-fix loop, all where a verb name is
immediately followed by the next separator. The kid's own automatic brief
carried the target's 8-line ceiling and it re-set line_ceiling to 8 after I had
set the slice to 2; the node's ceiling therefore records 8 while the change is
3 lines. The 2-line slice is the one this round was actually given.

(2) The node now says what it does NOT close, which the kid's "closes clause
(2)" title cannot: the trailing case is fixed; the general "verb-only scripts
parse exactly as today" sentence is not. Kid a00-b0575ad8 was cut for exactly
the 132 cases, with the candidate boundary measured in-memory by me before the
cut (0/3168).

(3) The causal correction survived into this node from my kid-1 review and is
kept: the historical link_ref leak contained no ampersand at all, so this
mechanism did not produce it. The node already carries that; I left it because
it is the kid's own writing and it is right.

generated by write.py. My first two attempts to append the review note were
themselves mis-split by the parser under review -- the second one deleted 14
lines of my own text via a bad body-range replace -- so this version was
written once, through the writer, with the separator defused as "& &" in prose.
<!-- THOUGHT:END -->
