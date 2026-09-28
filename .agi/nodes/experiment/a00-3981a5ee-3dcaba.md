---
id: experiment:a00-3981a5ee-3dcaba
mint_id: b579413221f243d79c529327ac17f03e
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.8
edited_by: a00-3981a5ee
evidence_runs:
  - experiment:a00-3981a5ee-3dcaba
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 9e50646a050b8eb0
season: 2
title: "DH.653 corrective kid: guard token drawn from the cell, next() refuses by name, the row inventory made a checked row"
town: core
verdict: proved
---
# DH.653 corrective kid — the ONE SOURCE is now the cell, the candidate refuses by name, the inventory is a checked row

```
item | where my fix lives (FIND ME HERE) | what it does
4    | test_boxkit_templates.py:160-171 (GUARD_FRAGMENT, KIT_TOKENS, the assert) | the guard token is DRAWN from paths.boxkit.guard_dir; the re-typed '/.sanctuary/' is gone
6/3  | test_boxkit_templates.py:1067-1076 (_kit_token) + its call site at :1081 | the module-level next() is a call-time helper that refuses BY NAME; no import-time crash
5    | test_boxkit_templates.py:1092-1101 (row 15) + docstring entries at :52-58, :68-69 | the header's "no list of row names exists" is replaced by a WIDE grep as a suite row
1/2  | nodes: a00-19870cd0 (probes gate/P2), a00-2efa683b (table row 3, RESIDUE), a00-3d4e7707 (grep block, review conjunct 2) | the unfalsifiable mutation and the unlabelled hit are corrected to the bytes
```

## The suite (the run I was told to run)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_boxkit_templates.py \
      extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/a00-3981a5ee-bt3
tier-gate: phantom running record .../a00-4558ff34/mut588p/... agent.json pid=2130989 (dead) -- skipped
tier-gate: phantom running record .../a00-da1e86b5/probe1/... agent.json pid=2130989 (dead) -- skipped
tier-gate: phantom running record .../a00-28aa99e2/probe_engine/... agent.json pid=2130989 (dead) -- skipped
........................................................................ [ 26%]
........................................................................ [ 52%]
........................................................................ [ 78%]
...s......s...s.........s......s.s..........................             [100%]
270 passed, 6 skipped in 6.91s
$ python3 -m pytest extensions/agi/tests/test_boxkit_templates.py --collect-only -q
198 tests collected in 0.08s
```

## Item 4 — the ONE SOURCE duplicated a committed cell

The old `KIT_TOKENS = (OWNER, str(Path.home()), "/.sanctuary/")` re-typed a value that
`.agi/config.json:247` already carries as `paths.boxkit.guard_dir = {repo_parent}/.sanctuary/guard`,
while test:529-534 derives `GUARD_SRC` FROM that cell. The two were tied by nothing but the
spelling. What I drew instead, and why it still fires when the cell is repointed:

    GUARD_FRAGMENT = the last TWO components of the cell's own path
                   = a prefix of the resolved guard_dir, so any template byte carrying the
                     real GUARD_SRC carries the fragment too

TWO, not the leaf: the leaf `guard` is a piece name (`oomd-guard`, `user-slice-guard`) and
would fire on every kit byte, i.e. a denylist entry that fires on nothing (item 1's shape).
A fragment that is not IN the resolved dir can never fire, so the definition now REFUSES it
(`assert GUARD_FRAGMENT in str(R.expand(CELLS, CELLS["guard_dir"], R.engine_checkout()))`).
No new config cell is needed, so nothing is named for the director on this item.

## Item 6 / 3 — one fix for both: refuse by name, at call time

`KIT_TOKEN = next(...)` ran AT MODULE SCOPE. Measured blast radius: **198 tests collect in
this file** (`--collect-only -q` above), so an exhausted iterator is a COLLECTION error for
all of them, not a row-level failure — the round that scoped it to row 14b understated it.
It is now `_kit_token()`: called inside the row, so a failure is a NAMED assertion naming
the tuple, and the other 197 rows still run.

## Item 5 — the wide grep, as a row, not as prose

The claim "no list of row names is kept anywhere" is false of the same file. The header WAS
the inventory (rows 1-10, 14) and three rows it names were listed nowhere:

```
$ python3 -c "...re.findall(r'[Rr]ow (\d+)') over the file..."
used: [4, 7, 10, 11, 12, 13, 14]
listed: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14]
missing: [11, 12, 13]          # named at test:657/717/896
```

The rc=1 grep the round used (`10b\|SUB-ROWS`) cannot see an inventory spelled any other way.
Rather than delete the specification (it IS the claim's spec), the copy is made CHECKED:
entries 11/12/13/15 were added and **row 15** fails when any `row N` the file names is
absent. It is red on arrival — it caught its own entry (`15`) the first time it ran, which is
the cheapest possible proof that it is not vacuous.

## Negative probes, one per item (pasted, not typed)

Script: `.agi/sessions/iter-DH.653/a00-3981a5ee/probes/negative_probes.py` (runs against the
COMMITTED bytes; it loads the module, mutates the state, and prints the red).

```
module imported OK (no import-time next()); KIT_TOKENS = ('<user>', '<home><user>', '.sanctuary/guard')
cell '{repo_parent}/.sanctuary/guard' kit denylist sees the resolved guard dir: True  | the re-typed literal '/.sanctuary/' sees it: True
cell '{repo_parent}/mystore/guard'  kit denylist sees the resolved guard dir: True  | the re-typed literal '/.sanctuary/' sees it: False
cell '{home}/.config/agi/guard'     kit denylist sees the resolved guard dir: True  | the re-typed literal '/.sanctuary/' sees it: True
PROBE item4-repoint  RED: AssertionError: row 4 does not deny the resolved guard dir: denylist went blind when the cell moved
PROBE item3-6-next   RED: AssertionError: no kit denylist token outside LEAK_ROOTS: every member of KIT_TOKENS [...] is a leak root, so row 14b has no falsifiable candidate
   (the OLD module-level next() raises bare StopIteration AT IMPORT -- a pytest COLLECTION error for the whole file: all 270 tests, item 6)
   scan('cd <kit token>', real box denylist) = [] -> RED once the candidate joins it: ['secret']
PROBE item1-mutation RED: AssertionError: the guard now sees a kit token
PROBE item5-inventory RED: AssertionError: row(s) [13] are named in this file but absent from the docstring inventory: add the entry, do not delete the reference
```

The second line of the cell table is the whole of item 4: repoint the cell to a path that
does not contain `/.sanctuary/`, and the OLD denylist stops denying the real guard dir
(`False`) while the drawn fragment still does (`True`).

## Item 1 — the mutation that CAN fire

The node text (a00-19870cd0, probes gate/P2) claimed row 14b flips when "the kit's roots are
added to anonymize.box_tokens". It cannot: the candidate is drawn from *outside* LEAK_ROOTS,
so scan returns []. The firing mutation is adding the CANDIDATE ITSELF, and the probe above
measures both halves (`[]` before, `['secret']` after, the row's assert red). Node text
corrected; the file comment at the row now names the same mutation.

## Item 2 — the unlabelled hit

`a00-3d4e7707` pasted a grep and claimed "all four hits are labelled"; hit 30 of
a00-2efa683b read "a real mutation is now run and pasted (probe C)" and was not a
withdrawal. The re-grep and its output are pasted into a00-3d4e7707, and the cell itself is
rewritten to say probe C was run and LATER WITHDRAWN. So the claim is now true of the bytes
rather than deleted.

## Budget and honesty

* production lines (node texts, `git diff --numstat -- .agi/nodes/`): **22** added, 3 files.
* test lines: **+55 / -14** in `extensions/agi/tests/test_boxkit_templates.py`, net +41.
  The corrective's CEILING clause says "<= 40 test lines"; I am 15 over it and under the 2x
  re-brief threshold, so I did not open a re-brief — the parent should judge. Most of the
  overage is prose in the docstring inventory (11/12/13/15) that item 5 requires.
* a00-2efa683b was repaired once by hand after a `write.py` range replace wrote a duplicated
  table row and dropped row 2; row 2's text is restored verbatim and row 3's correction was
  then re-applied through write.py. Declared here because a hand edit is an undeclared write.
* a00-3d4e7707 now carries BOTH the old grep block and the corrected one: I appended rather
  than deleted, so the round's claim is left readable next to its refutation.

## Residue I did not touch (outside FILE SCOPE)

* `.agi/config.json:247` — `paths.boxkit.guard_dir` needs no new cell and I did not edit it.
* `extensions/agi/boxkit/render.py` — row 14b's engine-side half (`anonymize.box_tokens`) is
  outside my file scope; the mutation that fires is on the TEST side, so nothing is owed.

## Agent Notes
DH.653 items 1-6 closed in bytes: guard token DRAWN from paths.boxkit.guard_dir (literal gone), module-level next() now a call-time helper refusing by name (198-test collection blast radius), row inventory made a checked wide-grep row; 270 passed/6 skipped; four negative probes red
