---
id: experiment:a00-71af1de3-bcbfd8
mint_id: 3c5a9eae8039481cb85619ac80f0d14f
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-71af1de3
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

One file: `extensions/agi/tests/test_agi_bin_absent.py` (tests only, production_lines 0).

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
RED on `render-context.py` -- driver.sh line 265 still prefers a project-local
`render-context.py` although `bin/inject.py` replaced it in the engine (L1.05),
so the engine has no such file. That is a REAL residue, not a test bug: the
override set is not a subset of the engine's own scripts. I dropped the assertion
(no engine file) and recorded it below rather than encoding a wrong invariant.

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
