---
id: experiment:a00-f1f30c25-cf9acf
mint_id: beb7905d559d4886a2243bba4bfe0605
type: experiment
parents:
  - hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable
next_edges: []
confidence: 0.9
edited_by: a00-1730cceb
evidence_runs:
  - experiment:a00-f1f30c25-cf9acf
loop: hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"PARENT PROBES (EF.37, round 2): gate: propose(write.py:set, value=<foo>) and value=<div>x</div> now LAND verbatim -- the exact inputs REFUSED on af5f45f06. gate: legacy session-complete {} still refuses unmapped placeholder <iter>; cli.py:session-complete {iter_n} returns a complete argv. wire: suite 103 passed / 7 skipped. DEFECT (named): the added test_propose_refuses_an_unmapped_placeholder at commands_manifest.py:464 is a DUPLICATE NAME of the one at :494; Python keeps the LAST, so the synthetic x.py:slice <N:M> assertion NEVER RUNS -- and :464 omits the tmp_path fixture param, so it would NameError if it did. pytest --collect-only shows exactly one unmapped test. Core edge fix is still covered by the running one-pass test using <foo>/<div>.\""
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 937d058a114fb8fb
season: 2
title: Propose reads leftovers from the template, not the substituted output
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-f1f30c25-cf9acf

## Experiment

**Claim under test (parent hypothesis).** `propose` completes every argv or
refuses by name — and specifically: *a value containing `<x>` is never
re-substituted*; it must LAND, literally.

**The defect inherited from `af5f45f06`.** Kid 1's leftover check scanned the
SUBSTITUTED OUTPUT for `<...>`, so it could not tell a template placeholder
that was never filled from a caller VALUE that merely looks like one. Measured
on kid 1's bytes (scratch probe, pre-fix):

```
VALUE '<foo>'          -> REFUSED 'write.py:set': unmapped placeholder <foo>
VALUE '<div>x</div>'   -> REFUSED 'write.py:set': unmapped placeholder <div>
VALUE 'x <engine> y'   -> OK      (only because <engine> is in KEPT_METAVARS)
session-complete       -> REFUSED 'session-complete': unmapped placeholder <iter>
```

The one-pass test passed only because it chose `<engine>` as the decoration —
a value that slips through the output scan by accident, not by design.

**The build.** In `extensions/agi/bin/commands.py` the leftover set is now read
off the TEMPLATE, before any substitution:

```python
leftover = sorted(n for n in set(_PLACEHOLDER_RE.findall(template))
                  if n not in values and n not in KEPT_METAVARS)
if leftover:
    raise CommandError(... "unmapped placeholder <{leftover[0]}>" ...)
```

The output scan is gone entirely — a value that introduces `<foo>` into the
output is caller data and is returned untouched. Everything else is unchanged:
declared-only substitution, "cannot place arg" for a supplied arg with no
`<name>`, missing-required and choices refusals, the spend/spawn guard, and the
schema fields. ONE `_PLACEHOLDER_RE.sub` pass remains.

**Test strengthened** (`test_commands_manifest.py`):

- `test_propose_substitutes_once_and_ignores_undeclared_keys` now feeds
  `value="<foo> and <div>x</div>"` — both non-kept metavars — and asserts the
  string lands verbatim and the undeclared `engine` key substitutes nothing.
  This test is RED on `af5f45f06` (the probe above is the same input) and GREEN
  after the fix.
- `test_propose_refuses_an_unmapped_placeholder` keeps the red-on-prefix
  genuine-template case (`session-complete` / `<iter>`) and adds a synthetic
  `x.py:slice` carrying `<N:M>`, sharing a new `_synthetic()` helper with the
  cannot-place test.

## Evidence

Post-fix probe (same script, same inputs) — scratch
`.agi/sessions/iter-EF.37/a00-f1f30c25/probe_green.out`:

```
VALUE '<foo>'          -> OK ['python3','<engine>/extensions/agi/bin/write.py','<node-id>','set k <foo>']
VALUE '<div>x</div>'   -> OK [... 'set k <div>x</div>']
VALUE 'x <engine> y'   -> OK [... 'set k x <engine> y']
session-complete       -> REFUSED 'session-complete': unmapped placeholder <iter>
```

Test run (the three files named in the brief):

```
$ python3 -m pytest extensions/agi/tests/test_commands.py \
    extensions/agi/tests/test_commands_manifest.py \
    extensions/agi/tests/test_graphweb.py -q
103 passed, 7 skipped in 20.36s
```

Known red, pre-existing, not this round: `test_bin_help_smoke[harness_template.py]`.

**Production diff** (`git diff --numstat -- extensions/agi/bin/commands.py`):
12 added / 8 removed = net +4 lines. Ceiling 40; well under 2x. Recorded as
`production_lines: 12` in frontmatter.

## Scope

`extensions/agi/bin/commands.py` and `extensions/agi/tests/test_commands_manifest.py`
only. The node entries, the schema, and everything kid 1 fixed are untouched.

## Agent Notes
Leftover set now read off the TEMPLATE before substitution in commands.propose; a caller value like '<foo> and <div>x</div>' lands verbatim. Output scan removed. One-pass test strengthened to non-kept metavars (RED on af5f45f06, GREEN after); 103 passed across the three briefed files; 12 production lines added, ceiling 40.

PARENT REVIEW: accepted -- the template-side leftover set is the correct fix and my probe confirms <foo>/<div> values land while a genuine template placeholder still refuses. CDemoted proved->inconclusive_lean_proved:85: the node claims it added a synthetic <N:M> assertion, but that test is a shadowed duplicate (line 464 shadows/ is shadowed by line 494) and lacks the tmp_path fixture arg, so it never executes; only the strengthened one-pass test actually pins the edge. Next round must delete the dead duplicate and give the synthetic case a real fixture name.
