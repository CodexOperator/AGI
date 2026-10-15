---
id: experiment:a00-f33d3b0a-cab1c4
mint_id: 619847894eea479eb91cc25eec5c45e2
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.8
edited_by: a00-f33d3b0a
evidence_runs:
  - experiment:a00-f33d3b0a-cab1c4
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "in-process locations.resolve_storage_category(pick, None, cfg, None) for pick in ² ⑴ 1 \"1 \" ٣ ٢, cfg = this checkout .agi/config.json", "expected": "the resolver ANSWERS every pick; no isdigit()-but-not-int() string can raise out of it", "observed": "BEFORE: ² RAISED ValueError invalid literal for int() with base 10: ²; ⑴ RAISED the same; ٣ -> skills (row 3); ٢ -> tests (row 2); 1 and \"1 \" -> engine_code. AFTER: ² ⑴ ٣ ٢ all -> custom with payload_ref == the pick; 1 and \"1 \" -> engine_code unmoved", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "locations.py <temp project> --storage-pick ² | ٣ | 3 | 99", "expected": "a non-ASCII digit is a NAME at the CLI too, and main() no longer catches an opaque invalid-literal error for it", "observed": "² -> custom source_root ² rc=0; ٣ -> custom source_root ٣ rc=0; 3 -> skills source_root skills rc=0 (control unchanged); 99 -> custom source_root <empty> rc=0, the parent probe B residue, unchanged and still named", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_storage_categories.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp=/tmp/pt659 (and /tmp/pt659b after the change)", "expected": "the directors 103 passed / 6 skipped harvest REPRODUCES at my tip; after the guard and one new test it is 104/6", "observed": "103 passed, 6 skipped in 14.02s at the harvested tip BEFORE my change; 104 passed, 6 skipped in 5.08s after, i.e. the +1 is my one new test and nothing else moved", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "season._agent_notes_block(.agi/nodes/experiment/a00-eea0b2c4-0b4709.md) after the reorder, plus a THOUGHT:BEGIN count of the file", "expected": "the ## Agent Notes block extracts WITHOUT the THOUGHT region, so a conflicted merge cannot delete the DH.618 parent review", "observed": "after the splice: notes lines 1, marker lines in the block [], THOUGHT:BEGIN count 1 in the whole file, and ## Agent Notes is the last heading. Before: the block was 4 lines ending in the THOUGHT:END marker", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "yaml.safe_load of a00-82e7d5d4-3feda4 frontmatter after the probes conversion", "expected": "probes are the schema dicts {conjunct, class, cmd, expected, observed, result}, and conjunct 2 keeps result fail", "observed": "5 probe dicts, every key set equal to the six the schema names, frontmatter still parses as YAML, results [pass, fail, pass, pass, pass] -- the fail is the parents digit-with-no-tail residue and was NOT relabelled", "result": "pass"}
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 49d38b0f82b4acf5
season: 2
title: "The isdigit guard made a name out of a row index: ASCII-only digits, the Agent Notes region un-swallowed, and 103/6 reproduced"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-f33d3b0a-cab1c4

## Experiment

DH.659 corrective, one kid, four orders. **Production lines: 10 added / 3 removed
against the 40-line ceiling** (`locations.py` only; the test file's 17 lines are
test lines, ceiling 40), measured once by `git diff --numstat`, the only git this
round ran.

| # | order | what happened, and what I did |
|---|---|---|
| 1 | `a00-82e7d5d4`'s `probes:` are prose strings, not the schema's probe dicts | **FIXED IN BYTES.** Converted to the schema shape from `.agi/context/schemas/[experiment].md` (`probes: additive ... each = {conjunct:int, class, cmd, expected, observed, result}`), copying the shape of a node that already satisfies it (`experiment:a00-cb88d326-21c0cc`). Five dicts, keys verified equal to the six the schema names, and the file still parses as YAML |
| 2 | `locations.py:638` `int(text)` guarded by `text.isdigit()` raises for `'²'` | **FIXED IN BYTES.** Reproduced at my tip, then fixed: the resolver now computes `num = int(text) if text.isascii() and text.isdigit() else None` ONCE and never calls `int()` on a string it has not already converted. Both branches that read the digits (`row["n"]` match, and the tail-vs-text choice for a custom row) use `num`, so the two places can no longer disagree |
| 3 | `a00-eea0b2c4`'s `## Agent Notes` sits BEFORE its THOUGHT pair, so extraction swallows the pair | **FIXED IN BYTES.** Reordered: the one real THOUGHT region (the DH.618 parent review) now sits immediately before `## Agent Notes`, which is the last heading in the file. Extraction measured with `season._agent_notes_block` on the bytes AFTER the splice: **1 line, no marker line in it, 1 `THOUGHT:BEGIN` in the file** |
| 4 | director's harvest of 103 passed / 6 skipped is UNVERIFIED | **SETTLED BY RUN.** Reproduced exactly at my tip BEFORE my code change: `103 passed, 6 skipped in 14.02s`. After the change and the new test: `104 passed, 6 skipped in 5.08s` (my +1 test) |

### Item 2, the fix in the bytes

```
+    # ASCII digits only. `str.isdigit()` is TRUE for '²' and '⑴', which
+    # `int()` then refuses with ValueError -- and for '٣', which `int()`
+    # silently accepts as 3, so a NAME typed in another script is read as a
+    # row index. Both are answered here, never raised out of the resolver.
+    num = int(text) if text.isascii() and text.isdigit() else None
     for row in rows:
-        if text == row["key"] or (text.isdigit() and int(text) == row["n"]):
+        if text == row["key"] or (num is not None and num == row["n"]):
...
-    ref = str(tail or "").strip() if text.isdigit() else text
+    ref = str(tail or "").strip() if num is not None else text
```

Plus two docstring lines, because the call site reads the docstring and not the
round's notes: "Digits" means ASCII 0-9 and nothing else -- `'٣'` is a NAME to
this resolver, not row 3, and `'²'` is a name too rather than a ValueError.

### Was `'٣'` -> row 3 intended? NO -- an accident, and this round fixes it

The parent asked. It was not intended and not a documented contract: the table
is keyed by ASCII `n` printed by `--storage-categories`, and the docstring's own
sentence is "a pick that is a NUMBER naming no cell is not a path but a stale
list index" -- a name typed in another script is not a stale list index, it is a
name. `str.isdigit()` is True for the whole Unicode Nd class, so every
non-ASCII digit was silently being read as a row number: `'٣'` -> row 3
(skills), `'٢'` -> row 2 (tests). Both are now `custom` names, carrying
themselves as the `payload_ref` -- which is the branch the resolver already has
for every other name.

The smallest true change is the ASCII test rather than a `try/except`:
`try: int(text) except ValueError` would fix the RAISE and leave `'٣'` -> row 3,
so it closes half of what is actually wrong.

## Evidence

**Item 2 -- the probe, at MY tip, before the fix** (`locations.resolve_storage_category(pick, None, cfg, None)`, cfg = this checkout's `.agi/config.json`):

```
'²' RAISED ValueError invalid literal for int() with base 10: '²'
'⑴' RAISED ValueError invalid literal for int() with base 10: '⑴'
'1' -> engine_code 'extensions/agi/bin' 'extensions/agi/bin' custom=False
'1 ' -> engine_code 'extensions/agi/bin' 'extensions/agi/bin' custom=False
'٣' -> skills 'skills' 'skills' custom=False
'٢' -> tests 'extensions/agi/tests' 'extensions/agi/tests' custom=False
```

**The same probe after the fix** -- identical command, same config:

```
'²' -> custom '' '²' custom=True
'⑴' -> custom '' '⑴' custom=True
'1' -> engine_code 'extensions/agi/bin' 'extensions/agi/bin' custom=False
'1 ' -> engine_code 'extensions/agi/bin' 'extensions/agi/bin' custom=False
'٣' -> custom '' '٣' custom=True
'٢' -> custom '' '٢' custom=True
```

The ASCII control (`'1'`, `'1 '`) is unmoved, so the fix is not a widening of
the table's numbering.

**The same cases at the CLI, on a temp project, after the fix:**

```
== ²
custom	source_root	²
rc=0
== ٣
custom	source_root	٣
rc=0
== 3
skills	source_root	skills
rc=0
== 99
custom	source_root	
rc=0
```

`'²'` no longer reaches `main`'s `except ValueError` (locations.py:1147-1150)
and no longer prints an opaque `ERR: invalid literal for int() with base 10`.
Note `'²'` is now a NAME that a caller can write to disk as a file called `²` --
previously the resolver refused to answer it at all, so this is a widening of
what is spellable, not a narrowing.

**Item 4 -- the two suite runs, both mine, both in this worktree:**

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest \
    extensions/agi/tests/test_storage_categories.py \
    extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider \
    --basetemp=/tmp/pt659b
103 passed, 6 skipped in 14.02s      # at the harvested tip, before my change
104 passed, 6 skipped in 5.08s       # after the ASCII guard + 1 new test
```

The director's 103/6 REPRODUCES EXACTLY. 104 is 103 plus
`test_digits_are_ascii_only_and_never_raise_out_of_the_resolver`.

**The new test** (`test_storage_categories.py`, 17 lines, one test): four picks
(`'²'`, `'⑴'`, `'٣'`, `'٢'`) must all come back `custom` with
`payload_ref == pick`, and `'3'` must still resolve to `skills`. It is a real
guard, not a pin of the new behaviour only: on the pre-fix bytes `'²'` raises,
so the test is red there.

**Item 3 -- extraction measured after the splice:**

```
$ python3 -c "import season; season._agent_notes_block(<the file>)"
notes lines: 1 markers: [] thought regions: 1
```

Before the splice the block was 4 lines ending in the `THOUGHT:END` marker, so
`season.py:1639-1648` on a conflicted merge would have replaced the notes text
AND the THOUGHT region with the union -- deleting the DH.618 parent review's
reasoning from the node. The fenced `<!-- THOUGHT:END -->` at :105 of that file
is inside a pasted `grep` output, not a region, and was left exactly as it is.

**Item 1 -- the frontmatter after conversion:**

```
$ python3 -c "yaml.safe_load(...)['probes']"
probes ok: 5 ['pass', 'fail', 'pass', 'pass', 'pass']
```

Conjunct 2 keeps `result: fail` on purpose: it is the parent's probe B, the
digit-with-no-tail residue, and relabelling it `pass` because the strings became
dicts would be the falsification this round exists to stop.

## Caveats

- I changed BEHAVIOUR, not prose, in `locations.py`: before this, `--storage-pick ٣`
  meant row 3. That is a contract change on a resolver three rounds have argued
  about, and I took it because the alternative (a `try/except` around `int`) fixes
  only the raise and leaves the row-index reading of a name. The parent may want
  to rule on it; the diff is 10 lines and the docstring states the rule at the
  call site.
- Non-ASCII digits were never a supported spelling, but they were ACCEPTED
  silently. Someone typing `'٣'` has, until now, been getting `skills` and will
  now get a file named `٣`. No test on the chain covered it, so no test
  regressed; I am flagging it because a silent change of answer is still a change.
- The item-3 fix is a REORDER on someone else's node, inside FILE SCOPE. I did
  not touch its prose, its title or its numbers -- only the position of one
  region relative to one heading, plus the Caveats bullet that records why.
- I did not fix `season.py` itself, and I did not try to work around the reader
  trap (`:1557-1571`) at the node level either. See OUTSIDE.

## OUTSIDE (named for the director's findings row, not touched)

- `extensions/agi/bin/season.py:1557-1571` -- `_agent_notes_block` stops at the
  first line starting with `#`, so a heading nested under `## Agent Notes`
  silently truncates the block. My fix removes the instance; the rule that made
  the instance possible is still there.
- `extensions/agi/bin/season.py:1636-1648` -- `_resolve_node_conflict` DELETES
  `lines[i+1:end]` on a conflicted merge, so whatever sits after `## Agent Notes`
  is lost. Reordering hides this for the one node; any other node in the graph
  with the same shape is still armed. One file:line change (stop the span at the
  next `## ` heading, or at a `<!-- THOUGHT:` marker) would close both, and it
  is the owner's window, not mine.

## Struggles

- `write.py`'s anchor guard refused THREE ranges that were each, I believed, a
  blank line plus a heading: `179:180` ("starts on the heading"), `178:179`
  ("ends on the heading"), and my first splice `197:203` ("starts inside a
  paragraph"). The guard was right about the paragraph one and, for the other
  two, teaching me a shape I did not have: a range may neither begin nor end on
  a heading unless it spans that heading's whole section. The way in ended up
  being a one-line range on the blank line alone.
- The body/file line offset cost me a wrong splice: I assumed +23 (body 1 = the
  `<!-- BODY:BEGIN -->` marker) and the guard told me it was +22, and the first
  `replace` that PASSED the guard still produced a wrong file, because I had
  saved lines 222/225 into a scratch file intending 224/225 and pasted the pair
  back without its `THOUGHT:BEGIN`. I caught it only because I re-read the tail
  and counted `THOUGHT:BEGIN` occurrences. This is the same failure class the
  previous round wrote a whole Struggles bullet about, and I reproduced it in
  the very node I was sent to repair.
- The parent's item-2 probe output was handed to me pre-run. I re-ran it rather
  than pasting it, which is the right call and cost a turn: it also produced a
  case the parent had not listed (`'٢'` -> row 2), which is what showed the `'٣'`
  row reading is a whole-class accident and not a one-glyph curiosity.
- `git diff --numstat` counts ADDED lines, so the guard fix reads as 10/3 and I
  reported it that way rather than as a net +7; if the ceiling is meant as net,
  the honest figure is 7 and the looser one is 10, and both are under 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.659 corrective. (1) The load-bearing judgement is item 2, and it is not the
one the brief led with. The brief called `'²'` a note-level defect because main()
catches the ValueError, and then asked whether `'٣'` -> row 3 is intended. Those
two halves of the question have one answer, and answering only the raised half
with a `try/except` would have been the trap: `int()` is perfectly happy with
`'٣'`, so a try/except closes the crash and leaves the machine reading a NAME as
a ROW INDEX. The real bug is that the code asked `isdigit()` a question about
NUMBERS and got an answer about UNICODE. `text.isascii() and text.isdigit()` is
the smallest true change, it moves the conversion to one place so the match and
the tail branch cannot disagree again, and it makes both halves of the parent's
question fall out of one expression. I also wrote the rule into the docstring,
because that is the surface a caller actually reads, and the previous three
rounds on this chain all discovered that a contract nobody is told about is a
contract that changes under the next kid.
(2) Item 3 is the round's own lesson applied to the round's own node, and it is
worth being precise about what I did NOT do: I did not patch season.py to be
defensive, because a fix in the engine would silence the symptom everywhere
while the armed shape stays reachable by the next node, and because the file is
outside my scope. I moved one region relative to one heading so the extraction is
correct ON THE BYTES, and named the writer that would still delete it. The
honest limit: I fixed the instance I was shown and left the class armed, and I
said so in OUTSIDE rather than letting the node read as a closure.
(3) The `probes:` conversion is bookkeeping with a trap inside it: five of the
five probes are the parent's, and turning prose strings into dicts is exactly the
move that invites relabelling `fail` to `pass`. I kept conjunct 2 at `fail`,
because the digit-with-no-tail residue is real and the schema exists to make it
readable rather than to make the table tidy.
(4) Verdict: three of four orders are closed in the bytes with a command pasted
for each, and the fourth (the 103/6 harvest) reproduces exactly. The lean is
high but not absolute because item 2 is a behaviour change and I argued for it
rather than deriving it from a stated contract -- the parent may rule it back.
<!-- THOUGHT:END -->

## Agent Notes
ASCII-only digit guard in locations.resolve_storage_category (isdigit/isint disagreement: ² no longer raises, ٣ is a name not row 3), a00-82e7d5d4 probes converted to schema dicts, a00-eea0b2c4 Agent Notes no longer swallows its THOUGHT region, 103/6 harvest reproduced; 10 prod / 17 test lines
