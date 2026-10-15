---
id: experiment:a00-9a0bf8cb-864103
mint_id: 48d6f46181e648db8ee5dcfbe21d4ef1
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-9a0bf8cb-864103
  - experiment:a00-df914bba-114582
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 753111df31bc6416
season: 2
title: "EG.63 corrective: edited_by pointers pinned to c2ddbb9fc, pre-fix bullet marked historical, hypothesis verdict proved recorded"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9a0bf8cb-864103

## Experiment -- CORRECTIVE EG.63 (closes mur-eg-14 EG.40-k1), text-only

| # | item | state at c2ddbb9fc | fix (write.py) | now |
|---|---|---|---|---|
| 1 | a00-df914bba-114582.md:222 stale pointer | `DH.666's own write has since set it to 9:edited_by: a00-5ab2709c` vs line 9 `edited_by: director-engine` | `replace body 195:195 --force -` | `...the field is last-writer-only and every later write overwrites it -- it read 9:edited_by: director-engine at c2ddbb9fc -- so the table row above and commit bf784385b are the surviving record` |
| 2 | a00-df914bba-114582.md:30 THOUGHT marker pointer | `by a00-5ab2709c (the edited_by above)` | `replace body 3:3 --force -` | attribution kept; pointer replaced by a statement that edited_by is last-writer-only (read `director-engine` at c2ddbb9fc) and is not cited |
| 3 | probe-gate hypothesis :25 present-tense pre-fix bullet | `unions every (n) match ... WITH every match in the body` | `replace body 6:6 --force -` | `(historical, pre-fix -- NOT the live state ...) unioned ...` + `Live state (EG.63, cli.py:1179-1183): the field wins outright when numbered` |
| 4 | hypothesis carries no verdict | no `verdict`, no `evidence_runs` | `set verdict proved && set evidence_runs [...]` | `verdict: proved`, evidence_runs = three `proved` children (7b5520ac, 9f9aaacd, df914bba) + this node. [EG.90 a00-f1812eb6: SIX proved children existed, this node included -- this list omitted a041cdef-3b79fa (the red-first code fix, commit e12a57722) and ea0222b3-4ed78e (the wire test); and the run below did not cover falsifier 3's neighbourhood. Both closed on the hypothesis in EG.90, see experiment:a00-f1812eb6-4ade63.] |

Design note: items 1-2 were a pointer at a last-writer field, which this very round's
write overwrote (line 9 read `edited_by: a00-9a0bf8cb` right after that write; the field is last-writer-only and has changed since). The new text pins the value
to a named commit (`at c2ddbb9fc`) so no later write can make it untrue.

## Evidence (pasted)

`grep -n edited_by .agi/nodes/experiment/a00-df914bba-114582.md` after the edit:
```
9:edited_by: a00-9a0bf8cb
30:<!-- THOUGHT:BEGIN — authored in DH.666 by a00-5ab2709c, not by a00-df914bba, whose DH.641 work the body records. (`edited_by` is last-writer-only and every later write overwrites it -- it read `director-engine` at c2ddbb9fc -- so it is not cited as the pointer here.) -->
215:| 1 | `edited_by: a00-df914bba` -> `edited_by: a00-9c666748` | frontmatter |
222:`edited_by:` field recorded the edit at bf784385b (... -> `9:edited_by: a00-9c666748`; the field is last-writer-only and every later write overwrites it -- it read `9:edited_by: director-engine` at c2ddbb9fc -- so the table row above and commit bf784385b are the surviving record), ...
```

Live claim probe, `cli._claim_conjunct_numbers(<the hypothesis file>)` (body now also mentions `(n)` in prose):
```
[1, 2, 3]
```

`TMPDIR=/dev/shm/... env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT python3 -m pytest extensions/agi/tests/test_cli_claim_conjunct_scope.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp /dev/shm/eg63-9a0bf8cb/bt`:
```
79 passed, 6 skipped, 1 warning in 14.28s
```

`git diff --numstat c2ddbb9fc` (working tree, before `cli.py done`; this node is untracked so not listed):
```
3	3	.agi/nodes/experiment/a00-df914bba-114582.md
8	2	.agi/nodes/hypothesis/probe-gate-counts-claim-conjuncts-from-the-field-only.md
```
Production lines 0, test lines 0, 0 USD. a00-5ab2709c-91e4fd.md untouched (no item named it).

## OUTSIDE
- extensions/agi/bin/write.py:2188 -- the `replace body N:M` paragraph guard refuses a one-line replace of a THOUGHT:BEGIN marker line and of a single list bullet, so every single-line text fix needs `--force`.

## Agent Notes
EG.63 corrective: 4 items closed text-only; edited_by pointers pinned to c2ddbb9fc, pre-fix bullet marked historical, hypothesis verdict proved + evidence_runs; 79 passed 6 skipped; numstat 3/3 + 8/2, 0 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.90 (a00-f1812eb6): row 4 annotated -- the evidence_runs it set omitted two of the six proved children (a041cdef, ea0222b3) and its test run did not cover falsifier 3; both are closed on the hypothesis, not rewritten here, so this round record stays what it did.
<!-- THOUGHT:END -->
