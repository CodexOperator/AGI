---
confidence: 1.0
goal_id: S19
goal_kind: short-term
heading_level: 2
id: "goal:s19"
mint_id: ed6a7e053b2e4959aa04ade37256b53c
order: 82
origin: goals-doc
parents: []
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S19: Contract derivation depends on which interpreter ran it"
type: goal
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
