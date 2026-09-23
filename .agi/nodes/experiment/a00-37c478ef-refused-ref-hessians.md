---
id: experiment:a00-37c478ef-refused-ref-hessians
mint_id: d1b54389b95b440dbb9669a2e4f21419
type: experiment
parents:
  - hypothesis:a00-37c478ef-06ded4
next_edges: []
edited_by: a00-37c478ef
evidence_runs: experiment:a00-37c478ef-refused-ref-hessians
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 5457f26134fe32d4
season: 2
title: "\"Built and proved: refused profile_ref writes nothing, missing node is a named refusal\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-37c478ef-refused-ref-hessians

## Experiment

DH.88 on `goal:g7.31.5.1`. Pre-fix, both residues were reproduced on the built
bytes in a scratch repo; then the fixes were built and the same probes re-run.
Production diff: `profile_sync.py` 4+/1-, `write.py` 35+/0- = **39 lines**,
tests excluded (ceiling 40). No production write other than the two fixes.

**Pre-fix probes (the defect, as measured).**

```
$ python3 .../bin/write.py hypothesis:h1 'note a new note'    # profile_ref: "../escape.md"
ERR: profile projection refused: profile_ref '../escape.md' resolves outside the repo root
rc=2
$ grep -n "a new note" .agi/nodes/hypothesis/h1.md
17:a new note                       # <-- the body ALREADY landed: a partial write

$ python3 .../bin/profile_sync.py hypothesis:nope
Traceback (most recent call last):
  ...
  File ".../profile_sync.py", line 48, in project
    raise FileNotFoundError(node_id)
FileNotFoundError: hypothesis:nope
rc=1                               # <-- the one uncaught crash, rc=1 not 2
```

**Post-fix probes (the same commands, on the changed bytes).**

```
$ python3 .../bin/write.py hypothesis:h1 'note a new note'
ERR: profile projection refused: profile_ref '../escape.md' resolves outside the repo root
rc=2
node sha before=226a86e5... after=226a86e5... unchanged=YES
                               # node byte-identical; nothing happened at all

$ python3 .../bin/write.py hypothesis:h1 'note n2 && set profile_ref .agi/nodes/x.md'
ERR: profile projection refused: profile_ref '.agi/nodes/x.md' resolves under .agi/nodes/
rc=2 ; node unchanged (diff -q SAME)
                               # the EFFECTIVE ref is validated, so a bad ref
                               # set in the SAME edit refuses pre-write too

$ python3 .../bin/profile_sync.py hypothesis:nope
REFUSED: no such node 'hypothesis:nope' — nothing to project
rc=2                           # named refusal, no traceback

$ python3 .../bin/write.py hypothesis:nope 'note x'
ERR: no node file for hypothesis:nope
rc=2                           # write.py cannot reach project() with a
                               # missing node: update_node refuses first
```

**Why (a) pre-validate and not (b) land-and-name.** The module's own invariant
already reads "Everything that can refuse, refuses BEFORE anything is written",
so (a) extends a rule rather than adding a fourth exit code; rc=2 keeps one
meaning ("nothing happened") everywhere instead of splitting into 2 and 3; and
a partial write with a false failure signal is what the goal's "Never invent a
second SoT" guards against — a graph that moved while the caller was told it
did not.

**Green assertions.** `write.py` still contains no direct file write (the
`test_edit_py_contains_no_file_write` ast guard is in `test_write.py`, 117
passed). The valid-ref same-action projection, the no-ref no-op, `--check`
drift without writing, the outside-repo / `.agi/nodes/` / directory refusals,
the `--all` sweep, the rotate guard and the malformed-unlinked no-op all stay
green in `test_profile_sync.py` (20 passed). Combined run: 137 passed.

## Evidence

- `extensions/agi/tests/test_profile_sync.py::test_a_refused_profile_ref_writes_nothing_at_all`
  — locks residue A: rc=2, named refusal, node sha unchanged, no artifact, no
  traceback.
- `extensions/agi/tests/test_profile_sync.py::test_a_missing_node_is_refused_by_name`
  — locks residue B: rc=2, `REFUSED` naming `hypothesis:nope`, no
  `Traceback`, no `FileNotFoundError`.
- Suites: `python3 -m pytest extensions/agi/tests/test_profile_sync.py
  extensions/agi/tests/test_write.py -q` -> 137 passed.
- production_lines: 39 (`git diff --numstat -- extensions/agi/bin/profile_sync.py
  extensions/agi/bin/write.py` = 4/1 + 35/0).

Raw output, screenshots, logs.
