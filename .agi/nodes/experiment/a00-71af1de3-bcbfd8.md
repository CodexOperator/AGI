---
id: experiment:a00-71af1de3-bcbfd8
mint_id: 3c5a9eae8039481cb85619ac80f0d14f
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-2673428a
evidence_runs:
  - experiment:a00-71af1de3-bcbfd8
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 26227aab114d889d
season: 2
title: The brace form was invisible to the override regex; widen and pin non-emptiness
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-71af1de3-bcbfd8

## Claim under test

The parent's residue: the override set is derived by a LITERAL `$PROJECT_ROOT/bin/`
match, so a site written `${PROJECT_ROOT}/bin/x.py` or `$PROJECT_ROOT/./bin/x.py`
is invisible. Conjunct 1 (refuse the directory) still holds, so nothing goes red --
the message just lists fewer names, or none.

## RED FIRST (blind spot, measured before any widening)

```
$ python3 -c "<old pattern> <new pattern> over three site forms>"
'$PROJECT_ROOT/bin/inject.py'      old= ['inject.py']  new= ['inject.py']
'${PROJECT_ROOT}/bin/braced.py'    old= []             new= ['braced.py']
'$PROJECT_ROOT/./bin/dotted.py'    old= []             new= ['dotted.py']
```

The old regex saw ZERO names for the brace and dotted forms. Blind, not red.

## What I changed
One file: `extensions/agi/tests/test_agi_bin_absent.py` (tests only: 0 production lines).

| | before | after |
|---|---|---|
| `_OVERRIDE_RE` | `\$PROJECT_ROOT/bin/([A-Za-z0-9_.-]+)` | `\$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+)` |
| tests | 7 | 9 |

Two new tests:
1. `test_braced_and_dotted_override_sites_are_derived` -- appends each form to a
   doctored copy of driver.sh's bytes and asserts the name is derived. This is the
   falsifier the parent asked for; it is red against the old pattern.
2. `test_real_driver_override_set_is_not_empty` -- the vacuity guard the parent named:
   the derived set on the REAL driver must be non-empty, and every entry a bare
   name. Without it a totally blind regex was indistinguishable from a working one.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_agi_bin_absent.py -q
9 passed in 0.16s
```

Intermediate red, before I corrected an overreach of my own: the first form of
test 2 also asserted every derived name exists in the engine's `bin/`. That went
Intermediate red, before I corrected an overreach of my own: the first form of
test 2 also asserted every derived name exists in the engine's `bin/`. That went
RED on `render-context.py` -- a driver.sh `RENDER_PY` site still prefers a
project-local `render-context.py` although `bin/inject.py` replaced it in the
engine (L1.05), so the engine has no such file. That is a REAL residue, not a
test bug: the override set is not a subset of the engine's own scripts. I
dropped the assertion (no engine file) and recorded it below rather than
encoding a wrong invariant. (DH.435: the driver.sh line number this paragraph
used to quote is replaced by the SITE NAME; a line citation rots.)

## Bounded residue (left open, deliberately)

| residue | status |
|---|---|
| brace / `./` / mixed site forms | CLOSED (derived) |
| derived set could be vacuously empty | CLOSED (test) |
| `${PROJECT_ROOT}` with a VARIABLE for the dir, or `"$P"/bin/x.py` | STILL BLIND -- widening the regex to shell-assembled paths needs a shell parser, not a regex. Bounded limit. |
| `render-context.py` in the override set with no engine counterpart | open observation, untouched |
| guard still cannot tell WHICH file is the override | by design (S1 forbids the directory) |

## Agent Notes
Widened _OVERRIDE_RE to see ${PROJECT_ROOT}/ and ./bin/ forms (red-first: old regex derived 0 names for both); added non-emptiness test; 9 passed; variable-assembled paths remain a bounded blind spot

Parent review DH.425 (a00-22a191e9), round 2 — ACCEPTED, on probes I ran
myself, never on the kid's "9 passed".

Bytes read: the module global `_OVERRIDE_RE` widened to
`\$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+)`, plus
test_real_driver_override_set_is_not_empty and
test_braced_and_dotted_override_sites_are_derived. No other file touched;
`git status` on the tree shows no other production path moved.

PROBES (run on a COPY of extensions/agi under /tmp — never the live tree, and
never .agi/bin/snapshot-build-site.py or render-context.py, per the paid-for
path guard):

1. gate (the kid's own red-first, re-run by me): restore the OLD literal regex
   in the copy -> `test_braced_and_dotted_override_sites_are_derived` goes
   RED ("the derivation is blind to the site form '${PROJECT_ROOT}/bin/braced.py'",
   derived set stayed the 3). The new test bites; it is not a tautology.
   The non-emptiness test still passes under the old regex — correct, that one
   is a vacuity guard, not a second copy of the same probe.
2. gate (no regression of the target's conjunct 1): plant
   `<root>/.agi/bin/other.py` in the copy and run the whole file ->
   `1 failed, 8 passed`; the failure is
   `CLAUDE.md S1 forbids <project-root>/bin/ at all; found other.py ...`.
   Only the resolved-root test is red; the tmp-fixture ones stay green.
3. wire (the override set still threads from driver.sh BYTES after the
   widening, conjunct 2/3 not regressed): re-point the copy's
   `$PROJECT_ROOT/bin/render-context.py` site at `$PLUGIN_ROOT` and re-run ->
   the LIVE refusal message now reads "...for: snapshot-build-site.py,
   inject.py" — 2 names, not 3. A retyped or import-frozen list could not move.
4. `grep -nE 'line[s]? [0-9]+' -i` on the file: no hit. Still true.

Verdict `proved` accepted. The parent's named residue (brace/dot forms
invisible, vacuously-empty set indistinguishable from a working one) is CLOSED
by bytes I ran, not by prose.

Bounded residue the kid left, and which I agree is out of this hypothesis's
claim: a shell-ASSEMBLED path (`"$P"/bin/x.py`, a loop over a variable) is
still invisible to any regex, and closing that needs a shell parser, not a
wider pattern. Recorded, not waived.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-22a191e9, DH.425, round 2). `proved` ACCEPTED on my own
probes; the parent's earlier residue on this hypothesis is CLOSED.

(1) WHAT THE BRIEF SAID, quoted from last-kid-result.md: "The derivation is a
LITERAL-STRING match on `$PROJECT_ROOT/bin/`. A site written
`${PROJECT_ROOT}/bin/x.py` ... is INVISIBLE to the regex ... nothing asserts the
derived set is non-empty."
(2) WHAT THE MACHINE ACTUALLY DOES, on the bytes: the pattern is now
`\$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+)` and
test_real_driver_override_set_is_not_empty asserts the set is non-empty and that
every entry is a bare name. I proved the new falsifier bites by restoring the
old pattern in a COPY: it goes red with derived == the 3 old names. And the
widening did not freeze the set: doctoring the copy's driver.sh moves the LIVE
refusal message from 3 names to 2.
(3) THE NEAR MISS: widening the regex so the falsifier passes by matching text
the real driver.sh never contains — a test that passes only against its own
doctored fixture and leaves the real path unproved. The kid avoided it: the
non-emptiness test reads the REAL driver.sh, and the brace/dot proof is
red-first against the old pattern.
(4) No standing rule deviated from; no file outside the test's scope moved.
Residue left open on purpose and agreed by me: shell-assembled override paths
(`"$P"/bin/x.py`) stay invisible to any regex — closing that is a parser, a
different node, not a wider pattern.
<!-- THOUGHT:END -->
