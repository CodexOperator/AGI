---
id: experiment:a00-0afd3916-9569b1
mint_id: e74fb726ffae4a17a43fca1988cbb5f7
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.85
edited_by: a00-0de3f8d9
evidence_runs:
  - experiment:a00-0afd3916-9569b1
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f860273c073e3d5f
season: 2
title: The chain probe cells become six-key dicts that pass cli._probe_defect, and three false node sentences are corrected
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0afd3916-9569b1 — DH.EG.100 corrective: the chain's probe cells now pass the engine's own reader

```
measure (engine reader) ─▶ convert 3 cells ─▶ fix 3 false sentences ─▶ pin with a test ─▶ re-measure
 9 entries 'not a dict'     9 six-key dicts    write.py sub, 2 nodes     3 params, live nodes    '' x9
```

## Pre-fix measurement (the reader the gate runs, not yaml)
`cli._probe_defect(p)` (cli.py:1118-1136) over every `probes:` entry on this hypothesis's experiment nodes, at the cut tip:
```
a00-0581fdf8-2bb4d2.md 1 ['not a dict']      <- not in the brief; the new test found it
a00-139dd5f6-df3721.md 4 ['not a dict', 'not a dict', 'not a dict', 'not a dict']
a00-68041083-03040f.md 4 ['not a dict', 'not a dict', 'not a dict', 'not a dict']
```

## Items
| # | item | settled by | fix (write.py) |
|---|---|---|---|
| 1 | verdict:274 "previous THOUGHT above is preserved" | `grep -c THOUGHT:BEGIN` on the verdict = `1`: only one block, so no prior THOUGHT is "above" | `sub`: the prior THOUGHT lives only in grid history (a THOUGHT is rewritten whole) |
| 2 | probes landed as prose strings | table above | `set probes` with six-key dicts on a00-68041083 (4), a00-139dd5f6 (4) and a00-0581fdf8 (1) |
| 3 | a00-139dd5f6:17 cites a reader it never ran | EG.03 ran `yaml.safe_load` only | that probe now names `cli._probe_defect` as its cmd; observed `'not a dict' x4` at EG.03, then `'' x4`; result `FAIL at EG.03, PASS after EG.100` |
| M1 | verdict:270 "returns nothing" | `grep -rn 3035-3036 .agi/nodes/verdict/ .agi/nodes/experiment/` = **12 hits**, every one a quote, a before-column or the a00-139dd5f6:109 caveat | `sub`: "leaves no LIVE citation: 12 hits remain ..."; the a00-139dd5f6 grep probe says the same |
| M2 | a00-139dd5f6:132 accepted the 4-entry list | same reader, same table | `sub`: an inline EG.100 CORRECTION after the claim; EG.03's text is left in place, with a marker that says it is false |

Conjunct numbers in the new dicts count the items of the round each probe belonged to. The hypothesis has no numbered `(n)` CLAIM items, so `_claim_conjunct_numbers` returns `[]` and the parent gate does not run on this chain. Because of that, the cells are pinned by a test and not by the gate.

## Post-fix measurement (CORRECTED at EG.125)
The `['OK']` below was a LABEL, not a return value: `_probe_defect` returns `''`
for a valid entry and never `'OK'`, while `_probe_defect('')` -- the EMPTY STRING
-- is `'not a dict'`, what the prose cells were failing with. The test below
asserts `== ""`. Re-measured at EG.125:
```
a00-0581fdf8-2bb4d2.md 1 ['']
a00-139dd5f6-df3721.md 4 ['', '', '', '']
a00-68041083-03040f.md 4 ['', '', '', '']
_probe_defect('') -> 'not a dict'   # the empty string is NOT a valid entry
```
New test `test_this_chains_probe_cells_pass_the_engines_own_reader` (parametrized over the 3 FILE SCOPE nodes). It reads the live node files and runs `_probe_defect` on each entry. RED on the cut tip is the pre-fix table: the first draft of the test caught a00-0581fdf8, which the brief never named.

```
$ env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/pytest-a00-0afd3916
FAILED extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
1 failed, 84 passed, 6 skipped in 5.27s
```
The one red is the pre-existing `suite_guards.py --help` (exit 0, empty stdout). It is the same red EG.03 named, and it is outside FILE SCOPE.

## CEILING
```
$ git diff --numstat 039140151
2	2	.agi/nodes/experiment/a00-0581fdf8-2bb4d2.md
6	6	.agi/nodes/experiment/a00-139dd5f6-df3721.md
5	5	.agi/nodes/experiment/a00-68041083-03040f.md
3	3	.agi/nodes/verdict/a00-29a5edeb-7b795d.md
15	0	extensions/agi/tests/test_round_own_path_set_fails_closed.py
```
0 production lines (cap 15) · 15 test lines (cap 40) · 1 kid · 0 USD. The range is uncommitted working-tree bytes against the cut tip. The parent commits.

## OUTSIDE (director findings rows)
- `.agi/nodes/experiment/a00-06eab0c0-78596f.md` (3), `.agi/nodes/experiment/a00-1389258c-50f93f.md` (4) and `.agi/nodes/experiment/a00-ee2d4cb1-6cecb8.md` (4): the same chain, and the same prose-string `probes:` cells (`'not a dict'`, 11 entries). They are not in FILE SCOPE, so I did not touch them. Once they are converted, add them to the test's parametrize list.
- Across other chains, 7 more `a00-*` experiment nodes carry prose-string probe entries. A splitter-on-`---` read of that set also crashes on probe text that contains `---`, so any audit must split frontmatter on `\n---\n`.
- `extensions/agi/bin/suite_guards.py`: `--help` prints nothing, so test_bin_help_smoke stays red (pre-existing).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.100 corrective: EG.03 checked the probes cell with yaml rather than with the reader the gate runs, so prose strings passed as a machine cell. This version measures with cli._probe_defect, converts every in-scope cell, and pins it with a test that reads the live nodes.
<!-- THOUGHT:END -->

## Agent Notes
DH.EG.100: 9 prose probe entries (3 in-scope nodes) measured 'not a dict' by cli._probe_defect, converted to six-key dicts, re-measured '' x9; verdict:270/274 + a00-139dd5f6:132 false sentences corrected via write.py sub; new parametrized test pins the 3 cells; 0 prod / 15 test lines; 1 failed 84 passed (pre-existing suite_guards --help red); 3 OUTSIDE chain nodes still hold 11 prose probes
