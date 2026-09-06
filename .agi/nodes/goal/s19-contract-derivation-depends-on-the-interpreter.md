---
id: goal:s19
mint_id: ed6a7e053b2e4959aa04ade37256b53c
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S19
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S19: Contract derivation depends on which interpreter ran it"
---
🔴 **`level3.py`'s `how` field is not a function of the payload alone. It is a
function of the payload *and* whichever `python3` ran the scan.**

`ast.unparse` normalizes f-string quoting differently across CPython versions
(PEP 701 rewrote f-string parsing in 3.12). Same file, same AST node, two
interpreters, measured 2026-08-27:

    3.11.15  ->  (d / name).write_text(f"---\nfields:\n  {fields}: ...
    3.12.3   ->  (d / name).write_text(f'---\nfields:\n  {fields}: ...

3.12's output is not even valid 3.11 syntax — an unescaped `'` inside a
`'`-quoted f-string is exactly what PEP 701 legalised — so this is not a
formatting preference that happens to differ, it is two genuinely different
renderings of one AST.

## Why it matters more than a quoting nit

This is **G6.5's failure mode with a new cause**: a stored value the
derivation does not reproduce leaves the graph permanently dirty, and
`publish-engine.sh`'s first gate then refuses **silently, every hour**. G6.5's
original instance was one character of YAML quoting and it cost 40 consecutive
silent refusals with 0 successful publishes.

**This instance is worse, because it is intermittent rather than permanent.**
The `:37` cron runs `/usr/bin/python3` (3.12). An interactive shell here picks
up 3.11 from a venv earlier on `PATH`. So the graph flaps: cron rewrites the
node, the next manual run rewrites it back, each flap burning a real grid
version on a file nobody edited (`build:tests-schema-registry-test-brackets`
reached v16 this way). Gate 1 therefore passes or fails depending on **who ran
last**, so the cron looks healthy half the time — which is precisely the
condition under which nobody investigates.

Both interpreters pass the suite identically (723 passed, 1 skipped), so
nothing about this is caught by tests. It is invisible to every gate the
project has except `git status`.

## Blast radius, measured rather than assumed

**Exactly 1 node**, 1 hunk, across 190 build nodes and 2,692 derivable
contract entries. The corpus is otherwise interpreter-stable, because almost
no engine file contains an f-string with nested quotes. That is why this
survived undetected — and also why it is safe to fix without a mass rewrite.

## The fix, and why the obvious one is wrong

**Rejected: pin the interpreter.** Tried first and it does not hold. Pinning by
convention fails the moment anything runs from a shell whose `PATH` differs,
which happened twice in the session that found this. Pinning `/usr/bin/python3`
inside the scripts contradicts **G8**'s forkability commitment — a fresh clone
on a machine whose system Python lacks `pyyaml` would break outright, and the
engine must not encode one machine's layout.

**The fix: stop re-rendering the AST.** Derive the code snippet in `how` from
`ast.get_source_segment(source, node)` — the literal source slice — instead of
`ast.unparse(node)`. Source bytes are interpreter-independent by construction,
and strictly more faithful: they show what is actually written rather than a
normalization of it. `_unparse_safe` in `level3.py` is the single chokepoint
that every `how` passes through, so this is one function.

Not done in the same pass as **G2.10** on purpose: `get_source_segment`
preserves original whitespace and line breaks where `unparse` normalizes them,
so it rewrites a large share of all 2,692 entries. That is a legitimate
one-time churn but it wants its own commit and its own before/after count, not
to be buried inside a change about node bodies.

Falsifier: run `level3.py` under two CPython versions in sequence and diff
`nodes/`. It must be empty. Today it is one hunk.

## What shipped 2026-08-28 — `how` quotes the payload, and the flap is gone

`_render(source, node)` replaces `_unparse_safe(node)` as the chokepoint every
`how` — and every derived entry `name` — passes through. It returns
`ast.get_source_segment(source, node)`, the literal slice of the payload's own
bytes, joined onto one line. `source` was threaded into `_scan_io_calls` and
`_scan_top_level_defs` as a **required** parameter, not a defaulted one: a
caller that forgot it would silently fall back to `ast.unparse` and restore
this defect invisibly, which is the exact shape of the original bug. Eight call
sites moved; `_unparse_safe` survives only as the fallback.

**The falsifier passes.** Three runs against the live corpus, from
`/home/ubuntu/work/agi-tree`, all with
`--project . --engine-root /home/ubuntu/work/agi --from-grid`:

    /usr/bin/python3 payloads/extensions/agi/bin/level3.py ...              (3.12.3)
    /home/ubuntu/.hermes/hermes-agent/venv/bin/python3 ... level3.py ...    (3.11.15)
    /usr/bin/python3 payloads/extensions/agi/bin/level3.py ...              (3.12.3)

`diff -r` of `nodes/` across all three: **empty**. Before the change the same
sequence moved `build:tests-schema-registry-test-brackets` by 1 hunk, 2 lines,
every single time. **Fixed point:** a second run under the same interpreter
also produced zero change, so the derivation reproduces its own stored value —
the G6.5 property, checked against a second *run* as well as a second
*interpreter*.

**Blast radius, re-measured.** The estimate in this node was taken before the
fix and both halves of it were wrong. Measured 2026-08-28 by deriving every
payload from a single grid read and running the old and new code over the same
bytes (so the 5-minute grid cron could not race the count): **186 payloads,
2,821 contract entries before and after — the entry set is unchanged; 363
entries (12.9%) changed value, across 55 of 186 build nodes.** 177 of the 363
were the `name` half. On disk the churn is 56 node files, +830/-761. The
corpus totals in the paragraph above (190 nodes, 2,692 entries) were stale:
190 is the node-file count (185 live + 5 retired), and the entry count is now
2,824.

Almost all of the 363 are `'` becoming `"`, because this codebase writes double
quotes and `ast.unparse` normalises to single. That is the churn predicted
above, and it is the point: those entries were never *wrong*, they were
rendered rather than quoted.

**YAML round-trip: verified, zero drift.** The hazard was that a source slice
carries quotes, `#`, backslash escapes and newlines into `yaml.safe_dump`, and
a value that did not survive write-then-read would leave the graph
**permanently** dirty — strictly worse than the intermittent flap being fixed.
`stitch.py --verify --from-grid --strict` reports `stale_contracts: 0` across
all 2,824 entries, with `missing_payload`, `orphan_files` and
`duplicate_payload_ref` also 0. Exit 0.

**`ast.arguments` keeps `ast.unparse`, and that is a decision.**
`get_source_segment` returns `None` for all 1,241 top-level signatures in this
engine — `arguments` is neither a `stmt` nor an `expr` and carries no
`lineno`/`col_offset`. Naively swapping the implementation would have emptied
every signature in every contract. The two obvious repairs are both wrong: a
span built from the child nodes drops the `*`, because `vararg`'s own position
starts at the *name* (checked: `get_source_segment` on the vararg of
`def f(*args)` returns `args`, not `*args`), and it cannot see the `/` in a
positional-only list at all; matching parentheses in the header text needs a
tokenizer, i.e. a second renderer, which is the class of thing this goal
removed. So the fallback stays, and the justification is measured rather than
assumed: `ast.unparse(node.args)` is byte-identical under 3.11.15 and 3.12.3
for all 1,241 signatures, and **zero** of them contain an f-string — the only
construct these versions render differently. **0 signature entries changed** in
the whole re-derivation, which is the same claim from the other direction.
`test_no_engine_signature_contains_an_fstring` now guards that premise on the
real corpus, so a future `def f(x=f"...")` fails a test instead of silently
restoring the flap.

**Whitespace is normalised, and the first attempt at it was a bug worth
recording.** `how` is one YAML scalar; ~7% of call sites span more than one
line, and `_cap`'s 240-char budget is meant to bound content, not indentation.
The first version collapsed `\s+` — and that silently rewrote
`f"---\nfields:\n  {fields}:"` to `...\n {fields}:`, because the `\n` in that
template is two characters and the spaces after it are **content**. Most of
what this engine writes is indentation-sensitive text, so a contract that
quietly alters what it quotes is worse than one that quotes too much. The
shipped `_LINE_JOIN` collapses only whitespace runs that *contain* a line
break, leaving everything inside a line exactly as the payload has it. Caught
by the new test asserting the quoted fragment is a verbatim substring of the
payload — written before the bug existed, which is why it was caught at all.

**Not done, deliberately:** comments are not stripped from joined multi-line
slices. 38 of 10,099 call sites span lines *and* carry a `#` comment, and
joining those reads as if the comment swallowed the rest of the call. It is
cosmetic, deterministic, and honest; removing it would mean rebuilding the text
from tokens, i.e. the second renderer this goal exists to avoid.

**One exposure named but not paid.** Derived entry `name`s go through the same
chokepoint, and `name` is what `_prior_index` keys the `why`/`perf`/`security`
carry-over on — so 177 changed names would have dropped authored fields if any
existed. Measured: 8,427 authored fields in the corpus, **0** filled. Nothing
was lost. The exposure is real for any future rendering change, and this is the
cheapest moment it will ever be paid.

**Tests: 801 passed / 1 skipped → 811 passed / 1 skipped, identical under both
interpreters.** Ten added, none deleted, none weakened. No existing test failed
against the new code — every pre-S19 fixture in `test_level3.py` used single
quotes, which is precisely why the suite could not tell a source slice from a
re-render and why this defect reached the corpus. Six of the ten new tests fail
against the pre-fix `level3.py`, checked by running them against a pristine
copy; the other four are property guards (round-trip, fixed point) that were
already true and are now pinned.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The brief named three hazards and all three were real, but the one that
actually bit was a fourth one I created myself. I wrote the whitespace
normaliser as `re.sub(r"\s+", " ", s)` — the obvious reading of "collapse
newlines and runs of spaces" — and it corrupted the indentation *inside*
string literals, because in `f"a:\n  b"` the `\n` is two characters and the
following spaces are content. It reported an indentation the payload does not
have, in an engine whose main output is YAML and markdown. I only caught it
because I had written the assertion as "the quoted fragment is a verbatim
substring of the payload" rather than the weaker "it contains a double quote";
the strong form failed immediately, the weak form would have passed and shipped
a contract that lies about what it quotes. That is the thing I would warn the
next agent about: on this file, assert the property, not a symptom of it.

The second judgement call was `ast.arguments`, and I nearly over-engineered it.
I worked out a tokenizer-based scheme to slice the parameter list out of the
header text and had convinced myself it was the "complete" fix. I stopped when
I noticed I was about to add a second renderer to close a hole whose measured
size is zero — 1,241 signatures, byte-identical across both interpreters, zero
f-strings among them. The honest move was to keep `ast.unparse` there, say so,
and convert "zero today" into a test that fails the day it stops being zero.
I also checked and discarded the cheaper idea of building the span from the
child nodes: `vararg`'s position starts at the name, so it silently drops the
`*`. Silently is the operative word — that would have been this same bug again,
in a new place.

One test of mine was itself interpreter-dependent and I should have seen it
sooner. I asserted the source slice must differ from `ast.unparse` of the same
node, using the real bug's f-string as the fixture — and it failed under 3.11,
because 3.11 happens to reproduce that construct exactly and 3.12 does not.
That asymmetry *is* the defect, so the test was asserting the bug's presence.
Moved the discriminator to a plain double-quoted string, where both versions
agree that unparse normalises to single quotes.

I did not touch `stitch.py`, though it is the thing that consumes `how`: it
compares `(name, how)` pairs opaquely and needed nothing. Ran it as the
round-trip gate instead, which is stronger evidence than any unit test I could
write, because it checks the real 2,824 entries through the real serializer.

Left `status: complete` because the goal wrote its own falsifier — two
interpreters, diff `nodes/`, must be empty — and it passes. The signature
fallback is a named residual with a guard, not unfinished work; if it ever
fires, it fires as a test failure with instructions attached.
<!-- THOUGHT:END -->